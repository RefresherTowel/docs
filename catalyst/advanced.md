---
layout: default
title: Advanced Topics
parent: Catalyst
nav_order: 2
---

# Catalyst Advanced Topics

This page covers the more powerful features of **Catalyst**.

All of these build on the core workflow from the Quickstart (stats + modifiers +
layers + durations), and introduce ways to make your stats react to game
state, stack in nuanced ways, and behave more like systems than raw numbers.

Advanced topics:

- Context-aware evaluation
- Context-driven stacks with `stack_func`
- Conditional modifiers
- Modifier families and stacking rules
- Derived base values (`base_func`)
- Soft caps & curves (`post_process`)
- Tags on stats and modifiers

---

## 1. Context-aware evaluation

Many effects depend on the *situation*, not just static gear:

- Number of burning enemies nearby
- Whether the target is frozen
- Current HP percentage
- Zone or biome
- Combo count, streaks, etc.

Catalyst lets you pass a **context** struct into `GetValue` and into all the
callback functions you define (conditions, stack functions, base functions,
post-process functions).

```js
// Build a context for this hit
var _ctx = {
    burning_enemy_count : 3,
    target_frozen       : false,
    zone_tag            : "lava_caves"
};

// Ask for a context-aware value
var _dmg = stats.damage.GetValue(_ctx);
```

Internally, that context is passed to any callbacks you've registered on the
stat or its modifiers:

- `base_func(stat, context)` - see section 5.
- `post_process(stat, raw_value, context)` - see section 6.
- `condition(stat, context)` on modifiers - see section 3.
- `stack_func(stat, context)` on modifiers - see section 2.

If you call `GetValue()` with **no argument** (or with `undefined`), Catalyst:

- Returns the **cached canonical value** (`current_value`).
- Recalculates only if the stat is marked as `altered`.
- Fires any on-change callbacks if the canonical value changed.

If you call `GetValue(context)` **with a context**, Catalyst:

- Evaluates the stat **for that context only**.
- Does **not** change `current_value`.
- Does **not** fire on-change callbacks.

This makes it safe to use contexts for previews, AI evaluation, tooltips, and
anything else where you want "what would this be *right now*?" without
changing the underlying stat.

> Providing a context to `GetValue()` forces it to skip its default optimisation of only recalculating the value when something has changed.
> While this isn't something to stress over, it's something you should consider when using it and only provide a context when it is necessary for the
> situation.
{: .note}

---

## 2. Context-driven stacks with `stack_func`

Sometimes stacks are purely event-driven:

- "On crit, gain a stack of +5% damage for 5 seconds, up to 5 stacks."

For those, you usually use `SetStacks`, `AddStacks`, and `SetMaxStacks` on
the modifier and let your own game logic manage when stacks increase or
decrease. Stacks are unlimited by default (`max_stacks = infinity`), so only
set a max when you want a cap.

Sometimes stacks are driven by **environmental state** instead:

- "+5% damage for every burning enemy nearby, up to 10 enemies."
- "+2% move speed for each ally within 5 tiles."

For those, Catalyst provides `stack_func`:

```js
// +5% damage per burning enemy, up to 10 enemies
var _burn_power = new CatalystModifier(0.05, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.AUGMENTS)
    .SetMaxStacks(10)
    .SetStackFunc(function(_stat, _ctx) {
        var _count = _ctx.burning_enemy_count;
        return clamp(_count, 0, 10);
    });

stats.damage.AddModifier(_burn_power);
```

When evaluating the stat with a context:

```js
var _ctx = { burning_enemy_count : 7 };
var _dmg = stats.damage.GetValue(_ctx);
```

Catalyst will:

1. Start from the modifier's `stacks` field (defaulting to 1).
2. If a `stack_func` is defined, call it as `stack_func(stat, context)`.
3. Clamp the returned value to `>= 0` and to `max_stacks` (defaults to
   `infinity`).
4. Apply the modifier using that effective stack count.

> If a modifier has a `stack_func` **and** you call
> `GetValue()` without a context, Catalyst treats environment-driven stacks
> as **0** (the function isn't called).  
> This is by design: context-free evaluation shouldn't guess about
> environment state. If you rely on `stack_func`, make sure you pass an
> appropriate context when you care about its effect.
{: .important}

You can mix event-driven stacks and context-driven stacks if you want - for
example, use `stacks` as a base (from crit events) and have `stack_func`
add extra stacks based on nearby enemies.

---

## 3. Conditional modifiers

Sometimes a modifier only applies in certain situations:

- "+50% damage against frozen targets."
- "Take 25% less damage while below 20% HP."
- "Extra move speed inside the 'Sanctuary' zone only."

For these, you can attach a **condition** function to a modifier using
`SetCondition`:

```js
// +50% damage if the target is frozen
var _frozen_bonus = new CatalystModifier(0.50, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.AUGMENTS)
    .SetSourceLabel("Frost Hunter Rune")
    .SetCondition(function(_stat, _ctx) {
        return _ctx.target_frozen;
    });

stats.damage.AddModifier(_frozen_bonus);
```

When evaluating:

- Without context (`GetValue()`), Catalyst calls `condition(stat)` if a
  condition exists.
- With context (`GetValue(ctx)`), Catalyst calls
  `condition(stat, ctx)` instead.

If the condition returns `false`, the modifier is skipped completely
(does not contribute to the value or to family comparisons).

You can freely combine `condition` and `stack_func`:

- `condition` decides *whether* the modifier applies at all.
- `stack_func` decides *how strongly* it applies when it does.

---

## 4. Modifier families & stacking rules

Some effects of the "same family" should **not** stack:

- Two haste auras where only the strongest should apply.
- Several overlapping damage-reduction effects where only the lowest
  reduction should count.
- A series of movement buffs where only the best one matters.

Catalyst groups modifiers into **families** by a `family` key (string,
enum, etc.) and a **family stacking mode**:

```js
enum eCatFamilyStackMode {
    STACK_ALL,  // default: all apply
    HIGHEST,    // only the strongest effect applies
    LOWEST      // only the weakest effect applies
}
```

You set these on a modifier using `SetFamily`:

```js
// Movement auras - only the fastest wins
var _walk_aura = new CatalystModifier(0.10, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.TEMP)
    .SetFamily("movement_aura", eCatFamilyStackMode.HIGHEST);

var _sprint_aura = new CatalystModifier(0.25, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.TEMP)
    .SetFamily("movement_aura", eCatFamilyStackMode.HIGHEST);

stats.speed.AddModifier(_walk_aura);
stats.speed.AddModifier(_sprint_aura);
```

When evaluating the stat, Catalyst:

1. Groups modifiers by `family` key within a layer.
2. For each family:
   - If the mode is `STACK_ALL`, all modifiers in the family contribute.
   - If the mode is `HIGHEST`, only the most "powerful" effect
     contributes.
   - If the mode is `LOWEST`, only the weakest effect contributes.
3. Applies remaining modifiers in layer order as usual.

The "power" of a modifier depends on its operation and value
(e.g. bigger multipliers and bigger additive bonuses win), and takes into
account:

- Current stacks (including `stack_func` if a context is provided).
- The modifier's condition, if any.

> **Note:** `FORCE_MIN` and `FORCE_MAX` modifiers are excluded from family comparisons.
> They are applied later as a final floor, regardless of family stacking,
> so you can safely combine them with regular additive/multiplicative
> families.

You can also change the family mode after the fact with
`SetFamilyMode(eCatFamilyStackMode.LOWEST)` if needed.

---

## 5. Derived base values (`base_func`)

Sometimes a stat's "base" is itself a function of other stats or fields:

- Max HP from vitality + level.
- Evasion from agility and equipment weight.
- Spell damage from intelligence and weapon power.

Instead of manually recomputing and assigning `base_value`, you can
configure a **base function** on the stat. Because GameMaker functions
do not capture local scope, bind the owning instance if you need to
reach its stats inside the callback:

```js
// Max HP derived from vitality and level
stats.max_hp = new CatalystStatistic(100).SetName("Max HP");

// If not set, base_value would just stay at 100. Instead:
var _owner = self;
stats.max_hp.SetBaseFunc(method({ owner: _owner }, function(_stat, _ctx) {
    var _vit   = owner.stats.vitality.GetValue();  // canonical value
    var _level = owner.stats.level.GetValue();     // canonical value
    return 50 + _vit * 10 + _level * 5;
}));
```

When evaluating the stat:

1. Catalyst starts from `base_value`.
2. If `base_func` is set, it calls `base_func(stat, context)` and uses
   that return value as the effective base **instead** of `base_value`.
3. All modifiers are applied on top of that effective base.

If you pass a context into `GetValue(ctx)`, the same context is passed
into `base_func(stat, ctx)`. This makes it possible to do things like:

- "Max HP scales differently inside certain zones."
- "Base damage uses a different formula when a special mode is active."

If you clear the base function (via `ClearBaseFunc()`), the stat falls back to
the stored `base_value`.

---

## 6. Soft caps & curves (`post_process`)

Hard caps (min/max) are useful, but many games want **diminishing returns**:

- "Armor gives less damage reduction as it increases."
- "Movement speed bonuses taper off near the cap."
- "Critical chance above 60% grows slower."

Catalyst lets you plug in a **post-process** function that runs after all
modifiers and families are applied, but before clamping/rounding:

```js
// Example: diminishing returns on armor
stats.armor = new CatalystStatistic(0).SetName("Armor");

stats.armor.SetPostProcess(function(_stat, _raw, _ctx) {
    // Simple DR formula: DR = raw / (raw + K)
    var _K = 100;
    var _dr = _raw / (_raw + _K);
    // Convert back into an equivalent "effective armor" if you want,
    // or just return DR directly and use this stat as a percentage.
    return _dr * 100; // treat this stat as "damage reduction %"
});
```

When evaluating:

1. Catalyst computes the raw value from base + modifiers.
2. If `post_process` is set, it calls `post_process(stat, raw_value, context)` and
   uses the return value as the new value.
3. It then applies clamping (`min_value`, `max_value`) if enabled.
4. Finally it applies rounding (`rounded` / `round_step`) if enabled.

As with `base_func`, if you call `GetValue(ctx)`, the same context is
passed into `post_process`.

---

## 7. Tags on stats and modifiers

Tags are free-form strings you can use to categorize stats and modifiers.

Common examples:

- `"offense"`, `"defense"`, `"movement"`
- `"fire"`, `"ice"`, `"poison"`
- `"buff"`, `"debuff"`, `"aura"`, `"equipment"`

### 7.1. Stat tags

Stats support a small tag API:

```js
stats.damage
    .AddTag("offense")
    .AddTag("fire");

if (stats.damage.HasTag("offense")) {
    // Show it in the offensive stats section of your UI
}
```

On `CatalystStatistic`:

- `AddTag(tag)`
- `RemoveTag(tag)`
- `HasTag(tag)`
- `ClearTags()`

These don't affect the math; they're for your own logic and UI.

### 7.2. Modifier tags

Modifiers also have tags, which are especially useful for cleanup and
filtering:

```js
var _burn_debuff = new CatalystModifier(-0.20, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.TEMP)
    .AddTag("debuff")
    .AddTag("fire");

stats.damage.AddModifier(_burn_debuff);
```

On `CatalystModifier`:

- `AddTag(tag)`
- `RemoveTag(tag)`
- `HasTag(tag)`
- `ClearTags()`

### 7.3. Removing by tag

Putting tags on modifiers makes it easy to remove whole groups at once:

```js
/// In CatalystStatistic:
static RemoveModifiersByTag = function(_tag) {
    // (Implementation provided by Catalyst - shown here conceptually)
};
```

Usage:

```js
// Cleanse all debuffs on this stat
stats.damage.RemoveModifiersByTag("debuff");

// Remove all fire-related effects
stats.damage.RemoveModifiersByTag("fire");
```

Tags are purely for your game logic - Catalyst itself doesn't interpret
them - but many patterns (dispels, "only fire buffs", "remove all movement
effects") become much easier when you have them wired into stats and
modifiers.
