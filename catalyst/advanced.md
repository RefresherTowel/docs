---
layout: default
title: Catalyst Advanced Topics
parent: Catalyst
nav_order: 2
---

# Catalyst Advanced Topics

This page covers the more powerful features in Catalyst:

- Context-aware evaluation
- Context-driven stacks with `stack_func`
- Conditional modifiers
- Modifier families and stacking rules
- Derived base values (`base_func`)
- Soft caps and curves (`post_process`)
- Tags on stats and modifiers

---

## 1. Context-aware evaluation

Many effects depend on the *situation*, not just static gear:

- Number of burning enemies nearby
- Whether the target is frozen
- Current HP percentage
- Zone or biome

Catalyst lets you pass a **context** struct into `GetValue` and into
your modifier functions:

```gml
var ctx = {
    burning_enemy_count : 3,
    target_is_frozen    : false,
    player_hp_ratio     : hp_current / stats.max_hp.GetValue()
};

var dmg_hit = stats.damage.GetValue(ctx);
```

The context is not inspected by Catalyst itself; it is passed through
to your `condition` and `stack_func` callbacks.

```gml
// condition(stat, context) -> bool
// stack_func(stat, context) -> real (effective stacks)
```

`GetValue(ctx)`:

- Does a **fresh evaluation** for that context.
- Does **not** touch the cached canonical value or fire on-change callbacks.

`GetValue()` with no arguments:

- Uses the cached canonical value.
- Updates `current_value` and clears `altered` when needed.
- Fires on-change callbacks if the numeric value changed.

---

## 2. Context-driven stacks with `stack_func`

Sometimes stacks are purely event-driven:

- "On crit, gain a stack of +5% damage for 5 seconds, up to 5 stacks."

For those, you update `stacks` manually from your game logic:

```gml
crit_rune.AddStacks(1).ResetDuration();
```

Other times, stacks are purely **environment-driven**:

- "+2% move speed per burning enemy near you, up to 10 enemies."

For those, Catalyst lets the modifier compute stacks directly from context using `stack_func`.

```gml
var rune_speed = new Modifier(0.02, eMathOps.MULTIPLY, "Scorched Momentum")
    .SetLayer(eStatLayer.RUNES)
    .SetMaxStacks(10)
    .SetStackFunc(function(_stat, _ctx) {
        if (is_undefined(_ctx) || !variable_struct_exists(_ctx, "burning_enemy_count")) {
            return 0;
        }
        return clamp(_ctx.burning_enemy_count, 0, 10);
    });
```

Then build a context and use it when you query the stat:

```gml
function BuildCombatContextForActor(_actor) {
    var radius = 200;
    var burning_count = 0;

    with (obj_enemy) {
        if (burning && point_distance(x, y, _actor.x, _actor.y) <= radius) {
            burning_count++;
        }
    }

    return {
        burning_enemy_count : burning_count
    };
}

/// In obj_player Step:
var ctx = BuildCombatContextForActor(self);
var move_speed = stats.move_speed.GetValue(ctx);
```

In this setup:

- You don't manually touch `.stacks` at all.
- The rune *internally* decides how many stacks to use for that context.

If no context is supplied, `stack_func`-based modifiers behave as if they have 0 stacks
(they do nothing).

---

## 3. Conditional modifiers

A `condition` function lets a modifier apply only when a predicate is true.

```gml
var low_hp_damage = new Modifier(0.25, eMathOps.MULTIPLY, "Desperation")
    .SetLayer(eStatLayer.RUNES)
    .SetCondition(function(_stat, _ctx) {
        if (is_undefined(_ctx)) return false;
        if (!variable_struct_exists(_ctx, "hp_ratio")) return false;
        return (_ctx.hp_ratio <= 0.30); // 30% or less
    });
```

Usage:

```gml
var ctx = {
    hp_ratio : hp_current / stats.max_hp.GetValue()
};

var dmg = stats.damage.GetValue(ctx);
```

If `condition` returns `false`, the modifier is skipped.

You can use both `condition` and `stack_func` on the same modifier if you want:
`condition` decides whether it applies at all, `stack_func` decides how strongly.

---

## 4. Modifier families & stacking rules

Some effects of the "same family" should not stack:

- Two haste auras where only the strongest applies.
- Multiple armor auras where only the lowest applies (for downsides).
- Named buff families that should not "double-stack".

Catalyst pairs two fields on `Modifier` for this:

- `family` - a string or enum key (e.g. `"haste_aura"`)
- `family_mode` - how members of that family combine:
  - `eFamilyStackMode.STACK_ALL` - default, everything stacks as usual
  - `eFamilyStackMode.HIGHEST`  - only the strongest effect applies
  - `eFamilyStackMode.LOWEST`   - only the weakest effect applies

Example: two haste auras, only the stronger should apply per layer:

```gml
var haste_minor = new Modifier(0.10, eMathOps.MULTIPLY, "Minor Haste")
    .SetLayer(eStatLayer.GLOBAL)
    .SetFamily("haste_aura", eFamilyStackMode.HIGHEST)
    .AddTag("buff")
    .AddTag("aura");

var haste_major = new Modifier(0.25, eMathOps.MULTIPLY, "Major Haste")
    .SetLayer(eStatLayer.GLOBAL)
    .SetFamily("haste_aura", eFamilyStackMode.HIGHEST)
    .AddTag("buff")
    .AddTag("aura");

stats.move_speed.AddModifier(haste_minor);
stats.move_speed.AddModifier(haste_major);
```

In any context where both would apply, Catalyst:

- Computes each modifier's **effective magnitude** for that context.
- Keeps only the one with the highest magnitude in that family + layer.

Families are evaluated *per layer* - a family in `RUNES` is separate from a family in `GLOBAL`.

---

## 5. Derived base values (`base_func`)

Sometimes a stat's "base" is itself a function of other stats or fields:

- Max HP from vitality + level.
- Evasion from agility.
- Spell power from intelligence and rune bonuses.

Catalyst supports a `base_func` override per stat:

```gml
stats.max_hp.SetBaseFunc(function(_stat, _ctx) {
    var vitality = owner.stats.vitality.GetValue();
    var level    = owner.level;
    return 50 + vitality * 10 + level * 5;
});
```

Implementation details:

- If `base_func` is `noone`, Catalyst starts from `base_value`.
- If `base_func` is set, Catalyst calls it as:
  ```gml
  var base = base_func(self, context);
  ```
- That result is then passed through all modifiers, post_process, clamp and rounding.

This is especially handy for derived stats where you don't want to manually recompute
the base every time another stat changes.

---

## 6. Soft caps & curves (`post_process`)

Hard caps (min/max) are useful, but many games want **diminishing returns**:

- "Armor gives less damage reduction as you get more of it."
- "You can never get more than 75% damage reduction."

Catalyst provides a `post_process` hook on `Statistic`:

```gml
stats.armor.SetPostProcess(function(_stat, _raw, _ctx) {
    // Example: simple DR curve
    var A   = max(0, _raw);
    var K   = 100;     // tuning constant
    var dr  = A / (A + K);   // 0..1
    var cap = 0.75;

    dr = clamp(dr, 0, cap);
    return dr;
});
```

Here:

- `_raw` is the value after all modifiers and FORCE_MIN.
- The return value is what `GetValue` will hand back (after clamp/round).

You can also use context in your curve if needed, e.g. different caps per zone.

---

## 7. Tags on stats and modifiers

Tags are free-form strings you can use to categorize stats and modifiers.

### 7.1. Stat tags

```gml
stats.damage
    .AddTag("offense")
    .AddTag("fire");

if (stats.damage.HasTag("offense")) {
    // Show it in a specific section of your UI
}
```

Available helpers:

```gml
stat.AddTag(tag);
stat.RemoveTag(tag);
stat.HasTag(tag);
stat.ClearTags();
```

### 7.2. Modifier tags

```gml
var burn_debuff = new Modifier(-0.20, eMathOps.MULTIPLY, "Scorched")
    .SetLayer(eStatLayer.TEMP)
    .AddTag("debuff")
    .AddTag("fire");
```

Helpers on `Modifier`:

```gml
mod.AddTag(tag);
mod.RemoveTag(tag);
mod.HasTag(tag);
mod.ClearTags();
```

A common use case is removing whole groups at once.

```gml
/// In Statistic:
static RemoveModifiersByTag = function(_tag) {
    var removed = 0;
    for (var i = array_length(modifiers) - 1; i >= 0; i--) {
        var m = modifiers[i];
        if (m.HasTag(_tag)) {
            m.Destroy(false);
            array_delete(modifiers, i, 1);
            removed++;
        }
    }
    if (removed > 0) altered = true;
    return removed;
};
```

Then:

```gml
// Cleanse all debuffs on this stat
stats.damage.RemoveModifiersByTag("debuff");
```

Tags are purely for your game logic - Catalyst itself doesn't interpret them,
but many patterns (dispels, "only fire buffs", "remove all movement effects") become
much easier when you have them.
