---
layout: default
title: Patterns & Recipes
parent: Catalyst
nav_order: 4
---

# Catalyst Patterns & Recipes

This page shows some common patterns built with Catalyst, focusing on
"rune-like" effects for an action / roguelike / ARPG style game. Of course,
that's not the only style of game that Catalyst is good for. Literally **any**
game that uses stats is a good use case for Catalyst.

- Burning enemies increase move speed
- Low HP damage boost
- Crit-based stacking damage buff
- Highest-of-kind global movement aura
- Tag-based dispels / cleanses
- Derived base values
- Soft caps via post-processing
- Item previews (what-if) for equipping/swapping
- Source-based cleanup and queries
- On-change callbacks

The rest of this page walks through these ideas as concrete snippets you can
copy, tweak, or wrap in your own helper functions.

---

## Pattern 1: Burning enemies increase move speed

> "For every burning enemy nearby, move a little faster (up to a cap)."

This is a **context-driven stacks** pattern:

- Movement speed is a stat (`CatalystStatistic`).
- A modifier (`CatalystModifier`) represents the rule.
- A `stack_func` reads from the evaluation context to decide how many stacks
  apply right now.

### Setup

In the player's `Create` event:

```js
// Base move speed
stats.speed = new CatalystStatistic(4).SetName("Move Speed");

// +5% speed per burning enemy nearby, up to 10 enemies
var _burn_speed = new CatalystModifier(0.05, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.AUGMENTS)
    .SetMaxStacks(10)
    .SetSourceLabel("Burning Momentum")
    .AddTag("buff")
    .AddTag("movement");

_burn_speed.SetStackFunc(function(_stat, _ctx) {
    // _ctx.burning_enemy_count should be provided when we ask for the value
    var _count = _ctx.burning_enemy_count;
    return clamp(_count, 0, 10);
});

stats.speed.AddModifier(_burn_speed);
```

### Using it

Wherever you actually *use* the move speed (for example, the player's `Step`
event), build a context and pass it into `GetValue`:

```js
// Count nearby burning enemies (implementation is up to your game)
var _burning_count = CountBurningEnemiesNear(id);

// Build a context and query the stat
var _ctx = { burning_enemy_count : _burning_count };
var _move_speed = stats.speed.GetValue(_ctx);

// Use move_speed for movement
x += lengthdir_x(_move_speed, direction);
y += lengthdir_y(_move_speed, direction);
```

If you call `stats.speed.GetValue()` **without** a context, this modifier's
`stack_func` will effectively contribute 0 stacks (environment-driven effects
need context to know what is happening).

---

## Pattern 2: Low HP damage boost

> "Deal more damage when you're on low health."

This is a **conditional modifier** pattern:

- Damage is a stat.
- A multiplicative modifier applies only while HP is below a threshold.
- The condition reads from the evaluation context.

### Setup

In the player's `Create` event:

```js
stats.damage = new CatalystStatistic(10).SetName("Damage");

var _low_hp_boost = new CatalystModifier(0.50, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.AUGMENTS)
    .SetSourceLabel("Desperation")
    .AddTag("buff");

_low_hp_boost.SetCondition(function(_stat, _ctx) {
    // Expect hp and hp_max in the context
    var _frac = _ctx.hp / _ctx.hp_max;
    return (_frac <= 0.3); // 30% HP or less
});

stats.damage.AddModifier(_low_hp_boost);
```

### Using it

Whenever you compute outgoing damage, pass a context containing HP:

```js
var _ctx = {
    hp     : hp,
    hp_max : max_hp
};

var _dmg = stats.damage.GetValue(_ctx);
```

If HP is above 30%, the `low_hp_boost` modifier is skipped; if it's 30% or
lower, the 1.5x multiplier is applied.

---

## Pattern 3: Crit-based stacking damage buff

> "On crit, gain a stack of +10% damage for 5 seconds, up to 5 stacks."

This pattern uses **event-driven stacks** plus **duration**:

- A TEMP-layer modifier holds the stacking buff.
- Your crit logic calls `AddStacks` and `SetDuration` when appropriate.
- The global `CatalystModifierTracker` handles ticking and expiration.

### Setup

In the player's `Create` event:

```js
stats.damage = new CatalystStatistic(10).SetName("Damage");

// Crit buff: +10% damage per stack, up to 5 stacks, lasting 5 ticks
// We declare it as an instance variable, since we will be referencing it later outside of the Create Event
crit_buff = new CatalystModifier(0.10, eCatMathOps.MULTIPLY, 0)
    .SetLayer(eCatStatLayer.TEMP)
    .SetMaxStacks(5)
    .SetStacks(0) // start at 0 stacks
    .SetSourceLabel("Sharpened Instinct")
    .AddTag("buff");

stats.damage.AddModifier(crit_buff);
```

In a global controller (or similar), make sure you are calling the countdown:

```js
// obj_game_controller Step event
CatalystModCountdown();
```

### On crit

Wherever you handle crits (for example in a hit resolution script):

```js
/// @desc Called whenever this player lands a critical hit.
function Player_OnCrit(_attacker, _target, _damage_ctx) {
    // Add a stack and refresh the duration to 5 ticks
    crit_buff
        .AddStacks(1)
        .SetDuration(5);
}
```

- Each crit adds one stack, up to 5.
- Every time you refresh the duration, the buff will last 5 more ticks
  from that point.
- Once the duration reaches 0 (via `CatalystModCountdown()`), the tracker
  removes the modifier from the stat.

---

## Pattern 4: Highest-of-kind global movement aura

> "You can have multiple movement auras, but only the strongest applies."

This is a **family stacking** pattern:

- Several modifiers share a family key, like `"movement_aura"`.
- The family uses `eCatFamilyStackMode.HIGHEST`.
- Only the strongest multiplier in that family is applied.

### Setup

Assume you have a movement speed stat:

```js
stats.speed = new CatalystStatistic(4).SetName("Move Speed");
```

Define two global auras in the GLOBAL layer:

```js
var _haste_minor = new CatalystModifier(0.10, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.GLOBAL)
    .SetFamily("movement_aura", eCatFamilyStackMode.HIGHEST)
    .SetSourceLabel("Minor Haste Aura")
    .AddTag("buff")
    .AddTag("aura")
    .AddTag("movement");

var _haste_major = new CatalystModifier(0.25, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.GLOBAL)
    .SetFamily("movement_aura", eCatFamilyStackMode.HIGHEST)
    .SetSourceLabel("Major Haste Aura")
    .AddTag("buff")
    .AddTag("aura")
    .AddTag("movement");

stats.speed.AddModifier(_haste_minor);
stats.speed.AddModifier(_haste_major);
```

Even though both auras are attached:

- Only the **stronger** 25% multiplier is applied (1.25x total).
- If the major aura is removed, the minor one automatically becomes active.

You can model things like:

- Local vs global auras sharing the same family.
- Temporary bonuses that override permanent ones.

---

## Pattern 5: Tag-based dispels & cleanses

> "Remove all debuffs on this stat" or "cleanse all fire effects".

Tags let you convert many "cleanse" style abilities into simple calls on a
stat, using `RemoveModifiersByTag`.

### Setup

First, make sure your modifiers are tagged appropriately:

```js
// A burning debuff that reduces movement temporarily
var _burn_slow = new CatalystModifier(-0.20, eCatMathOps.MULTIPLY, 3)
    .SetLayer(eCatStatLayer.TEMP)
    .SetSourceLabel("Burning Slow")
    .AddTag("debuff")
    .AddTag("fire")
    .AddTag("movement");

stats.speed.AddModifier(_burn_slow);
```

Now you can create simple dispel helpers:

```js
/// Remove all debuffs from this actor's movement-related stats
function ClearMovementDebuffs(_actor) {
    with (_actor) {
        stats.speed.RemoveModifiersByTag("debuff");
        // If you also have jump height, dash distance etc, clear those too:
        // stats.jump.RemoveModifiersByTag("debuff");
        // stats.dash.RemoveModifiersByTag("debuff");
    }
}
```

You can also have more specific cleanses, like `"fire"` or `"curse"`:

```js
/// Remove all fire-related effects from this actor
function ClearFireEffects(_actor) {
    with (_actor) {
        stats.speed.RemoveModifiersByTag("fire");
        stats.damage.RemoveModifiersByTag("fire");
    }
}
```

Under the hood, `RemoveModifiersByTag`:

- Finds all modifiers on the stat that have the given tag.
- Calls `Destroy(false)` on each one.
- Removes them from the stat and marks it as `altered`.

---

These patterns are just starting points - the idea is to let you express
your game's rules as small, composable pieces:

- Stats for the numbers
- Modifiers for the rules
- Context for "what's going on right now?"

If you find yourself repeating a pattern, it probably deserves a helper function
or a wrapper around Catalyst that matches *your* game's vocabulary.

---

## Pattern 6: Derived base stat (e.g., max HP from vitality + level)

> "Max HP scales off other stats and updates automatically."

Use a `base_func` so the stat's base value is derived from other stats, instead of manually reassigning `base_value` everywhere.

### Setup

```js
// In Create
stats.vitality = new CatalystStatistic(10).SetName("Vitality");
stats.level    = new CatalystStatistic(1).SetName("Level");

// Bind the owning instance so the callback can reach its stats
var _owner = self;
stats.max_hp = new CatalystStatistic(100).SetName("Max HP")
    .SetBaseFunc(method(_owner, function(_stat, _ctx) {
        var _vit   = stats.vitality.GetValue();
        var _level = stats.level.GetValue();
        return 50 + _vit * 10 + _level * 5;
    }));
```

### Using it

Any time you call `stats.max_hp.GetValue()`, the base is recomputed from the current vitality/level before modifiers apply. No manual syncing needed when `vitality` or `level` changes.

---

## Pattern 7: Soft cap via post-processing

> "Movement speed climbs with buffs but has diminishing returns past a cap."

Attach a `post_process` function to shape the final value after all modifiers.

### Setup

```js
// In Create
stats.speed = new CatalystStatistic(6).SetName("Move Speed")
    .SetPostProcess(function(_stat, _raw, _ctx) {
        var _cap = 12;
        // Full value up to cap, then 75% DR beyond cap
        return (_raw <= _cap) ? _raw : _cap + (_raw - _cap) * 0.25;
    });
```

### Using it

Modifiers can push `stats.speed` above 12, but the post-process applies diminishing returns. Queries stay the same:

```js
var _speed_final = stats.speed.GetValue();
```

Centralising the cap here keeps the rule in one place instead of scattering "clamp" logic across your code.

---

## Pattern 8: Item previews (what-if equip/swap)

> "Show current -> previewed stats when hovering or comparing items."

Store the modifiers that an item would apply when equipped. On hover, map those modifiers into `PreviewChanges` to simulate equipping without touching the actual stat. The stat's current value is read normally, and the preview value is computed with the extra ops layered on. This respects layers, families, conditions, and stack rules, so the preview matches real equip behaviour. The UI then shows current -> preview. Use this version when adding an item into an empty slot (or where nothing conflicting is equipped).

### Single item preview (hover)

```js
// Item definition (e.g., when generating loot)
var _item_sword = {
    name      : "Rusty Sword",
    modifiers : [
        new CatalystModifier(3, eCatMathOps.ADD)
            .SetLayer(eCatStatLayer.EQUIPMENT)
            .SetSourceLabel("Rusty Sword"),
        new CatalystModifier(0.10, eCatMathOps.MULTIPLY)
            .SetLayer(eCatStatLayer.EQUIPMENT)
            .SetSourceLabel("Rusty Sword")
    ]
};

// On hover: preview current vs with item
var _dmg_stat   = stats.damage;
var _current    = _dmg_stat.GetValue();
var _preview_ops = array_map(_item_sword.modifiers, function(_m) {
    return {
        value      : _m.value,
        operation  : _m.operation,
        layer      : _m.layer,
        stacks     : _m.stacks,
        max_stacks : _m.max_stacks,
        condition  : _m.condition,
        stack_func : _m.stack_func,
        family     : _m.family,
        family_mode: _m.family_mode
    }
});

var _preview = _dmg_stat.PreviewChanges(_preview_ops);

draw_text(x, y, "Damage: " + string(_current) + " -> " + string(_preview));
```

### Gear swap preview (remove old, add new)

To compare a new item against the currently equipped one (involving multiple modifiers being added and removed), simulate the swap in the `PreviewChanges` call: first invert the currently equipped item's modifiers (as if removing them), then append the new item's modifiers (as if equipping). Build a small helper (not included in Catalyst, since each game might handle this differently, although you can use this code here as a starting point) that converts a `CatalystModifier` to an extra-op struct and, when invert is true, negates additive deltas and inverts multiplicative deltas by using the reciprocal. `FORCE_MIN`/`FORCE_MAX` do not have a clean inverse, so skip those in the "remove" pass (or handle them separately based on your rules). The resulting ops array models the net change and `PreviewChanges` returns the would-be value without mutating the stat.

```js
function ModToPreviewOp(_m, _invert = false) {
    var _val = _m.value;
    if (_invert) {
        if (_m.operation == eCatMathOps.ADD) {
            _val = -_val;
        }
        else if (_m.operation == eCatMathOps.MULTIPLY) {
            if (_val <= -1) {
                return undefined;
            }
            _val = (1 / (1 + _val)) - 1;
        }
        else {
            return undefined;
        }
    }
    return {
        value      : _val,
        operation  : _m.operation,
        layer      : _m.layer,
        stacks     : _m.stacks,
        max_stacks : _m.max_stacks,
        condition  : _m.condition,
        stack_func : _m.stack_func,
        family     : _m.family,
        family_mode: _m.family_mode
    };
}

// Assume equipped.sword and loot_hovered both have .modifiers arrays
var _ops = [];

// Remove current item
for (var i = 0; i < array_length(equipped.sword.modifiers); i++) {
    var _op = ModToPreviewOp(equipped.sword.modifiers[i], true);
    if (!is_undefined(_op)) {
        array_push(_ops, _op);
    }
}

// Add new item
for (var j = 0; j < array_length(loot_hovered.modifiers); j++) {
    var _op = ModToPreviewOp(loot_hovered.modifiers[j], false);
    if (!is_undefined(_op)) {
        array_push(_ops, _op);
    }
}

var _current = stats.damage.GetValue();
var _preview = stats.damage.PreviewChanges(_ops);

draw_text(x, y, "Damage: " + string(_current) + " -> " + string(_preview));
```

Previews do **not** mutate the stat and respect layers/families/conditions just like real modifiers.

---

## Pattern 9: Source-based cleanup and queries

> We have three variables related to "source" in modifiers. Let's break them down to understand why they exist better, and then go through some functionality afterwards:

> `source_label`: In general, you want to use `source_label` as a user facing string, for instance, a modifier that increases damage by 1 and comes from a weapon struct could have a `source_label` like this: "+1 damage from Sword". This allows you to always have an accessible string that you can use to show users where a particular modification came from

> `source_id`: `source_id` should generally hold an actual reference to the thing that applied the modifier (for instance, a reference to an enemy that applied a burn DOT effect). This lets you to check for existence, or attempt to read data, etc, from the source of the modifier. We keep the user facing string separate from this, since the reference could become stale and inaccessible, whereas a plain string will always be accessible.

> `source_meta`: This is just storage for any extra meta data you may want to keep related to the source on the modifier. Usually this would be a struct, but it doesn't really matter what's stored here, use it for anything that feels awkward to keep in `source_label` or `source_id`.

> Final note: While Catalyst uses feathers type checking to ensure `source_label` is a string and `source_id` is a struct or id, feel free to ignore these enforced types if you wish to. Storing some other data type in them won't break Catalyst, it'll only cause feather to complain.

> "Remove or inspect modifiers based on where they came from."

Catalyst lets you tag modifiers with `source_label`, `source_id`, and `source_meta`. You can then remove or find them by origin.

### Remove by source_id (e.g., boss aura ends)

```js
// Remove all modifiers added by a specific source instance
var _removed = stats.damage.RemoveModifierBySourceId(boss_aura_id);
```

### Remove by source_label (e.g., unequip an item)

```js
// Unequipping "Bronze Wand" — strip its modifiers from relevant stats
stats.damage.RemoveModifierBySourceLabel("Bronze Wand");
stats.speed.RemoveModifierBySourceLabel("Bronze Wand");
```
(This is the kind of situation where having all the stats stored in an array instead of a struct is useful, as you can just loop over them all easily and run the modifier removal function, although obviously you can do the same for a struct, it's just a slower operation).

### Remove by source_meta (using a predicate function)

`source_meta` can hold arbitrary data (often a struct). Supply a "predicate" function (a function that returns a yes/no answer) that will be provided with the `source_meta` as an argument and makes a determination based on the `source_meta` data as to whether the modifier should be removed. The modifier gets removed if the predicate function returns `true`.

```js
// Remove modifiers whose source_meta.slot == "ring"
var _count = stats.damage.RemoveModifierBySourceMeta(function(_meta) {
    return is_struct(_meta) && _meta[$ "slot"] == "ring";
});
```

### Find modifiers by source_id (inspect active effects)

```js
var _mods_from_pet = stats.speed.FindModifiersBySourceId(pet_id);
if (array_length(_mods_from_pet) > 0) {
    EchoDebugInfo("Pet buffs on speed: " + string(array_length(_mods_from_pet)));
}
```

---

## Pattern 10: On-change callbacks

> "Run code when a stat's canonical value changes."

On-change callbacks fire when you call `GetValue()` with no context and the numeric value changes. Use them to keep UI or related stats in sync.

Because callbacks run with the stat as `self`, bind the owning instance if you
need to touch instance variables inside the callback.

### Update UI when a stat changes

```js
stats.damage = new CatalystStatistic(10).SetName("Damage");

var _owner = self;
stats.damage.AddOnChangeFunction(method( _owner, function(_stat, _old, _new) {
    ui_damage_text = "Damage: " + string(_new);
}));
```

### Keep a dependent stat in sync (max speed vs. current speed)

```js
// Max speed can be modified; current speed is clamped to max speed
stats.max_spd = new CatalystStatistic(6)
    .SetName("Max Speed")
    .SetClamped(true)
    .SetMinValue(0);

stats.spd = new CatalystStatistic(6)
    .SetName("Current Speed")
    .SetClamped(true)
    .SetMinValue(0);

// Whenever max_spd changes, clamp current spd to the new max
var _owner = self;
stats.max_spd.AddOnChangeFunction(method({ owner: _owner }, function(_stat, _old, _new) {
    owner.stats.spd.SetMaxValue(_new);
    owner.stats.spd.GetValue(); // recompute/clamp
}));
```

Use on-change callbacks to react in one place instead of scattering sync logic around your codebase.
