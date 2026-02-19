---
layout: default
title: Quickstart
parent: Catalyst
nav_order: 1
---


<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

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

```js
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

```js
var _dmg   = stats.damage.GetValue(); // canonical, cached value
var _speed = stats.speed.GetValue();
```

> I usually store my stats in an enum indexed array, as opposed to a struct, to allow for ease of looping through
> all stats, and for slightly better retrieval speed. However, I will use a struct for these examples, since it is easier to
> read. Either way is almost always fine though, so choose whichever method you prefer.
{: .note}

---

## Optional: Clamping and rounding

Use this when a stat must stay within bounds and round to a step size.

```js
stats.hp = new CatalystStatistic(100, 0, 999).SetName("HP");
stats.hp.SetClamped(true);
stats.hp.SetRounding(true, 1);

// This would go below 0 without clamping.
stats.hp.ChangeBaseValue(-150);

var _hp = stats.hp.GetValue();
```

---

## 2. Adding basic modifiers

To change a stat, you create one or more `CatalystModifier` instances and attach them.

A modifier needs at least:

- `_value` - how much to change the stat by.
- `_math_operation` - how to apply that value.

```js
// A flat +5 damage bonus
var _flat_bonus = new CatalystModifier(5, eCatMathOps.ADD);

// A +20% damage multiplier
var _percent_bonus = new CatalystModifier(0.20, eCatMathOps.MULTIPLY);

// Attach to the damage stat
stats.damage
    .AddModifier(_flat_bonus)
    .AddModifier(_percent_bonus);
```
Note how the MULTIPLY modifier works. To get a 20% increase, you provide 0.20 as the modifier's value (internally applied as `power(1 + value, stacks)`). If you wanted to halve the stat's value, you would provide -0.50 to the modifier (for a 50% reduction).

Now when you query the stat:

```js
var _dmg = stats.damage.GetValue(); // (10 + 5) * 1.20 = 18
```

> `FORCE_MIN` is also available via `eCatMathOps.FORCE_MIN`, which clamps the
> final value to at least the modifier's `value`. You typically use this for floor effects
> such as "always do at least 1 damage".  
> `FORCE_MAX` is available via `eCatMathOps.FORCE_MAX`, which caps the final value
> to at most the modifier's `value`, useful for hard ceilings.
{: .note}

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

```js
// Weapon adds +3 damage as equipment
var _weapon_mod = new CatalystModifier(3, eCatMathOps.ADD)
    .SetLayer(eCatStatLayer.EQUIPMENT)
    .SetSourceLabel("Rusty Sword");

// Rune adds +15% damage as an augment
var _rune_mod = new CatalystModifier(0.15, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.AUGMENTS)
    .SetSourceLabel("Lesser Power Rune");

stats.damage
    .AddModifier(_weapon_mod)
    .AddModifier(_rune_mod);
```

Layers make it easy to reason about the order of operations and to group similar effects together.

---

## 4. Duration-based modifiers

Catalyst ships with a global `CatalystModifierTracker` struct:

- It is created automatically as `global.__catalyst_modifier_tracker`.
- The macro `CATALYST_COUNTDOWN` points at this instance.
- The helper script `CatalystModCountdown(_step_size)` safely calls `Countdown(_step_size)` on the tracker.

Any modifier with a positive `duration` will automatically register with the tracker.
Call `CatalystModCountdown()` once per "tick" (step, turn, second, or whatever makes
sense for your game) to advance all durations. If you run a fractional time-step loop,
pass your step size as an argument. Duration can be in ticks, seconds, milliseconds,
or any other unit as long as your step size uses that same unit:

```js
// Fixed tick style (defaults _step_size to 1):
CatalystModCountdown();

// Fractional / delta-time style (example: seconds):
CatalystModCountdown(_dt_seconds);
```

If you need global control over timed effects, use the tracker:

```js
// Pause all timed modifier countdowns
CATALYST_COUNTDOWN.SetPaused(true);

// Resume and run countdown at half speed
CATALYST_COUNTDOWN.SetPaused(false);
CATALYST_COUNTDOWN.SetTimeScale(0.5);
```

Creating a timed buff looks like this:

```js
// +50% damage buff for 5 ticks
var _buff = new CatalystModifier(0.50, eCatMathOps.MULTIPLY, 5)
    .SetLayer(eCatStatLayer.TEMP)
    .SetSourceLabel("Rage Potion");

stats.damage.AddModifier(_buff);
```

- When `buff.duration` counts down to 0, the tracker will:
  - Remove it from the tracker itself, and
  - Remove it from `stats.damage`, marking the stat as altered.
- Expired modifiers are deleted. Avoid keeping long-lived raw references to timed modifiers; re-query active modifiers by source/tag/id when needed.

Setting `duration` to `-1` (the default) makes a modifier permanent
(it will not be tracked or counted down).

> If you want to "precreate" duration based modifiers (maybe during your level load or something) and then apply them at some later point in time, make sure you **don't** give them a duration until they are actually applied (using `.SetDuration()`). This is because a modifier gets automatically added to the countdown if it's created with a duration, and it will tick down and destroy itself before it ever gets applied. So just remember the rule: Precreated modifiers get their duration given during their application, not their creation.
{: .important}

---

## 5. A simple item preview

A common use case is "hover an item and see what it would do to my stats".

You can use `PreviewChanges` to simulate modifiers as if they were applied,
without actually attaching them to the stat.

```js
// Suppose the player currently has a damage stat:
var _dmg_stat = stats.damage;

// Define how the candidate weapon would change it:
var _preview_ops = [
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
// Usually you would be fetching the modifiers from the weapon and copying them here, instead of simply hard-coding values.
// There is an example of this in the Patterns & Recipes page

// Get the current and previewed values
var _current = _dmg_stat.GetValue();
var _preview = _dmg_stat.PreviewChanges(_preview_ops);

// Draw something like: "Damage: 18 -> 22"
draw_text(x, y, "Damage: " + string(_current) + " -> " + string(_preview));
```

For a single hypothetical modifier, you can use `PreviewChange` instead:

```js
var _preview = _dmg_stat.PreviewChange(
    0.15,
    eCatMathOps.MULTIPLY,
    eCatStatLayer.AUGMENTS
);
```

Previews don't mutate the stat, respect all layers, tags, families and conditions, and can optionally take a context for more advanced arguments (covered on the **Advanced Topics** page).
