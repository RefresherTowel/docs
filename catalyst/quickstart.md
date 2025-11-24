---
layout: default
title: Catalyst Quickstart
parent: Catalyst
nav_order: 1
---

# Catalyst Quickstart

This page walks through the typical steps for using **Catalyst** in a GameMaker project:

1. Set up stats on an actor (core)
2. Add basic modifiers (flat and percentage) (core)
3. Use layers for gear and augments (core)
4. Integrate duration-based modifiers (core)
5. Do a simple item preview (core, touching one advanced helper)

For more complex features (context, families, soft caps, etc.) see the **Advanced Topics** page.

---

## 1. Setting up stats on an actor

The most common pattern is to store your `CatalystStatistic` instances in a struct, or array (indexed via enums for readability) on your actor,
we'll use a struct for this example in the player object's `Create` event:

```gml
// obj_player Create event

stats = {
    damage : new CatalystStatistic(10).SetName("Damage"),
    speed  : new CatalystStatistic(4).SetName("Move Speed")
};
```

By default:

- `base_value` is the value you pass to the constructor.
- The stat will clamp to `[-infinity, infinity]` (no bounds) unless you change them.
- The stat rounds to an integer when you call `GetValue()`.

You can read values anywhere you have a reference to the stat:

```gml
var dmg   = stats.damage.GetValue(); // canonical, cached value
var speed = stats.speed.GetValue();
```

---

## 2. Adding basic modifiers

To change a stat, you create one or more `CatalystModifier` instances and attach them.

A modifier needs at least:

- `_value` - how much to change the stat by.
- `_math_operation` - how to apply that value.

```gml
// A flat +5 damage bonus
var flat_bonus = new CatalystModifier(5, eCatMathOps.ADD);

// A +20% damage multiplier
var percent_bonus = new CatalystModifier(1.20, eCatMathOps.MULTIPLY);

// Attach to the damage stat
stats.damage
    .AddModifier(flat_bonus)
    .AddModifier(percent_bonus);
```
Note how the MULTIPLY modifier works. To get a 20% increase, you provide 1.2 as the modifiers value. If you wanted to halve the stat's value,
you would provide 0.5 to the modifier. The stat's value is multiplied directly by the mod's value.

Now when you query the stat:

```gml
var dmg = stats.damage.GetValue(); // (10 + 5) * 1.2 = 18
```

> **Note:** `FORCE_MIN` is also available via `eCatMathOps.FORCE_MIN`, which clamps the
> final value to at least the modifier's `value`. You typically use this for floor effects
> such as "always do at least 1 damage".

---

## 3. Using layers for gear and augments

Layers control *when* modifiers apply in the pipeline. This lets you separate
things like base bonuses, gear, augments, temporary buffs, and global effects.

The `eCatStatLayer` enum defines the available layers:

- `eCatStatLayer.BASE_BONUS`
- `eCatStatLayer.EQUIPMENT`
- `eCatStatLayer.AUGMENTS`
- `eCatStatLayer.TEMP`
- `eCatStatLayer.GLOBAL`

For example, you might treat weapons as **EQUIPMENT** and runes as **AUGMENTS**:

```gml
// Weapon adds +3 damage as equipment
var weapon_mod = new CatalystModifier(3, eCatMathOps.ADD)
    .SetLayer(eCatStatLayer.EQUIPMENT)
    .SetSourceLabel("Rusty Sword");

// Rune adds +15% damage as an augment
var rune_mod = new CatalystModifier(1.15, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.AUGMENTS)
    .SetSourceLabel("Lesser Power Rune");

stats.damage
    .AddModifier(weapon_mod)
    .AddModifier(rune_mod);
```

Layers make it easy to reason about the order of operations and to group similar effects together.

---

## 4. Duration-based modifiers

Catalyst ships with a global `CatalystModifierTracker` instance:

- It is created automatically as `global.__catalyst_modifier_tracker`.
- The macro `CATALYST_COUNTDOWN` points at this instance.
- The helper script `CatalystModCountdown()` safely calls its `Countdown()` method.

Any modifier with a positive `duration` will automatically register with the tracker.
Call `CatalystModCountdown()` once per "tick" (step, turn, second, or whatever makes
sense for your game) to advance all durations:

```gml
// obj_game_controller Step event (or wherever your game tick lives)
CatalystModCountdown();
```

Creating a timed buff looks like this:

```gml
// +50% damage buff for 5 ticks
var buff = new CatalystModifier(1.5, eCatMathOps.MULTIPLY, 5)
    .SetLayer(eCatStatLayer.TEMP)
    .SetSourceLabel("Rage Potion");

stats.damage.AddModifier(buff);
```

- When `buff.duration` counts down to 0, the tracker will:
  - Remove it from the tracker itself, and
  - Remove it from `stats.damage`, marking the stat as altered.

Setting `duration` to `-1` (the default) makes a modifier permanent
(it will not be tracked or counted down).

---

## 5. A simple item preview

A common use case is "hover an item and see what it would do to my stats".

You can use `PreviewChanges` to simulate modifiers as if they were applied,
without actually attaching them to the stat.

```gml
// Suppose the player currently has a damage stat:
var dmg_stat = stats.damage;

// Define how the candidate weapon would change it:
var preview_ops = [
    {
        value      : 4,
        operation  : eCatMathOps.ADD,
        layer      : eCatStatLayer.EQUIPMENT,
        stacks     : 1,
        max_stacks : 1,
        condition  : noone,
        stack_func : noone,
        family     : "",
        family_mode: eCatFamilyStackMode.STACK_ALL
    }
];

// Get the current and previewed values
var current = dmg_stat.GetValue();
var preview = dmg_stat.PreviewChanges(preview_ops);

// Draw something like: "Damage: 18 → 22"
draw_text(x, y, "Damage: " + string(current) + " → " + string(preview));
```

For a single hypothetical modifier, you can use `PreviewChange` instead:

```gml
var preview = dmg_stat.PreviewChange(
    0.15,
    eCatMathOps.MULTIPLY,
    eCatStatLayer.AUGMENTS
);
```

Previews:

- Don't mutate the stat.
- Respect all layers, tags, families, and conditions.
- Can optionally take a context for more advanced arguments
  (covered on the **[Advanced Topics](./catalyst_advanced.md)** page).
