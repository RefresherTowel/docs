---
layout: default
title: Catalyst Patterns & Recipes
parent: Catalyst
nav_order: 4
---

# Catalyst Patterns & Recipes

This page shows some common patterns built with Catalyst, focusing on
"rune-like" effects for an action / roguelike / ARPG style game.

- Burning enemies increase move speed
- Low HP damage boost
- Crit-based stacking damage buff
- Highest-of-kind global movement aura
- Tag-based dispels / cleanses

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

```gml
// Base move speed
stats.speed = new CatalystStatistic(4).SetName("Move Speed");

// +5% speed per burning enemy nearby, up to 10 enemies
var burn_speed = new CatalystModifier(1.05, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.AUGMENTS)
    .SetMaxStacks(10)
    .SetSourceLabel("Burning Momentum")
    .AddTag("buff")
    .AddTag("movement");

burn_speed.SetStackFunc(function(_stat, _ctx) {
    // _ctx.burning_enemy_count should be provided when we ask for the value
    var count = _ctx.burning_enemy_count;
    return clamp(count, 0, 10);
});

stats.speed.AddModifier(burn_speed);
```

### Using it

Wherever you actually *use* the move speed (for example, the player's `Step`
event), build a context and pass it into `GetValue`:

```gml
// Count nearby burning enemies (implementation is up to your game)
var burning_count = scr_CountBurningEnemiesNear(id);

// Build a context and query the stat
var ctx = { burning_enemy_count : burning_count };
var move_speed = stats.speed.GetValue(ctx);

// Use move_speed for movement
x += lengthdir_x(move_speed, direction);
y += lengthdir_y(move_speed, direction);
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

```gml
stats.damage = new CatalystStatistic(10).SetName("Damage");

var low_hp_boost = new CatalystModifier(1.50, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.AUGMENTS)
    .SetSourceLabel("Desperation")
    .AddTag("buff");

low_hp_boost.SetCondition(function(_stat, _ctx) {
    // Expect hp and hp_max in the context
    var frac = _ctx.hp / _ctx.hp_max;
    return (frac <= 0.3); // 30% HP or less
});

stats.damage.AddModifier(low_hp_boost);
```

### Using it

Whenever you compute outgoing damage, pass a context containing HP:

```gml
var ctx = {
    hp     : hp,
    hp_max : max_hp
};

var dmg = stats.damage.GetValue(ctx);
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

```gml
stats.damage = new CatalystStatistic(10).SetName("Damage");

// Crit buff: +10% damage per stack, up to 5 stacks, lasting 5 ticks
crit_buff = new CatalystModifier(1.10, eCatMathOps.MULTIPLY, 0)
    .SetLayer(eCatStatLayer.TEMP)
    .SetMaxStacks(5)
    .SetStacks(0) // start at 0 stacks
    .SetSourceLabel("Sharpened Instinct")
    .AddTag("buff");

stats.damage.AddModifier(crit_buff);
```

In a global controller (or similar), make sure you are calling the countdown:

```gml
// obj_game_controller Step event
CatalystModCountdown();
```

### On crit

Wherever you handle crits (for example in a hit resolution script):

```gml
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

```gml
stats.speed = new CatalystStatistic(4).SetName("Move Speed");
```

Define two global auras in the GLOBAL layer:

```gml
var haste_minor = new CatalystModifier(1.10, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.GLOBAL)
    .SetFamily("movement_aura", eCatFamilyStackMode.HIGHEST)
    .SetSourceLabel("Minor Haste Aura")
    .AddTag("buff")
    .AddTag("aura")
    .AddTag("movement");

var haste_major = new CatalystModifier(1.25, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.GLOBAL)
    .SetFamily("movement_aura", eCatFamilyStackMode.HIGHEST)
    .SetSourceLabel("Major Haste Aura")
    .AddTag("buff")
    .AddTag("aura")
    .AddTag("movement");

stats.speed.AddModifier(haste_minor);
stats.speed.AddModifier(haste_major);
```

Even though both auras are attached:

- Only the **stronger** `1.25` multiplier is applied.
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

```gml
// A burning debuff that reduces movement temporarily
var burn_slow = new CatalystModifier(0.8, eCatMathOps.MULTIPLY, 3)
    .SetLayer(eCatStatLayer.TEMP)
    .SetSourceLabel("Burning Slow")
    .AddTag("debuff")
    .AddTag("fire")
    .AddTag("movement");

stats.speed.AddModifier(burn_slow);
```

Now you can create simple dispel helpers:

```gml
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

```gml
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
