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
- Armor with diminishing returns

All examples assume you have a `stats` struct on your actors and are
comfortable with contexts.

---

## Pattern 1: Burning enemies increase move speed

> "+2% move speed per burning enemy near you, up to 10 enemies."

### Rune modifier

```gml
// Attach this to the actor's move_speed stat
var rune_speed = new Modifier(0.02, eMathOps.MULTIPLY, "Scorched Momentum")
    .SetLayer(eStatLayer.RUNES)
    .SetMaxStacks(10)
    .SetStackFunc(function(_stat, _ctx) {
        if (is_undefined(_ctx)) return 0;
        if (!variable_struct_exists(_ctx, "burning_enemy_count")) return 0;
        return clamp(_ctx.burning_enemy_count, 0, 10);
    })
    .AddTag("buff")
    .AddTag("movement")
    .AddTag("fire");

stats.move_speed.AddModifier(rune_speed);
```

### Context builder

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
```

### Using it in Step

```gml
/// obj_player Step

var ctx = BuildCombatContextForActor(self);
var move_speed = stats.move_speed.GetValue(ctx);

x += lengthdir_x(move_speed, move_direction);
y += lengthdir_y(move_speed, move_direction);
```

The rune is fully self-contained:

- It knows its layer, value, max stacks, and tags.
- It derives stacks from context (no manual `SetStacks` calls).
- It works for any actor you attach it to, as long as you pass a suitable context.

---

## Pattern 2: Low HP damage boost

> "+25% damage while below 30% HP."

```gml
var low_hp_damage = new Modifier(0.25, eMathOps.MULTIPLY, "Desperation")
    .SetLayer(eStatLayer.RUNES)
    .SetCondition(function(_stat, _ctx) {
        if (is_undefined(_ctx)) return false;
        if (!variable_struct_exists(_ctx, "hp_ratio")) return false;
        return (_ctx.hp_ratio <= 0.30);
    })
    .AddTag("buff")
    .AddTag("offense");
```

Context for the player:

```gml
/// obj_player Step
var hp_ratio = hp_current / stats.max_hp.GetValue();
var ctx = {
    hp_ratio : hp_ratio
};

var dmg = stats.damage.GetValue(ctx);
```

When you're not using context-sensitive mods, you can just call `GetValue()` without context.

---

## Pattern 3: Crit-based stacking damage buff

> "On crit, gain a stack of +5% damage for 5 seconds, up to 5 stacks."

This is a **stateful stacks** pattern: stacks depend on discrete events (crits).

```gml
/// In player setup:
var crit_rune = new Modifier(0.05, eMathOps.MULTIPLY, "Killing Spree")
    .SetLayer(eStatLayer.RUNES)
    .SetMaxStacks(5)
    .SetDuration(300)         // 5 seconds at 60 fps, for example
    .AddTag("buff")
    .AddTag("offense");

stats.damage.AddModifier(crit_rune);
```

On crit:

```gml
/// When resolving a crit hit:
crit_rune.AddStacks(1);
crit_rune.ResetDuration();
```

Damage usage (no context needed here):

```gml
var dmg = stats.damage.GetValue();
```

Since this rune doesn't care about the environment, it doesn't use `stack_func` and
you don't need a context for it.

---

## Pattern 4: Highest-of-kind global movement aura

> "You can have multiple movement auras, but only the strongest applies."

```gml
var haste_minor = new Modifier(0.10, eMathOps.MULTIPLY, "Minor Haste Aura")
    .SetLayer(eStatLayer.GLOBAL)
    .SetFamily("haste_aura", eFamilyStackMode.HIGHEST)
    .AddTag("buff")
    .AddTag("aura")
    .AddTag("movement");

var haste_major = new Modifier(0.25, eMathOps.MULTIPLY, "Major Haste Aura")
    .SetLayer(eStatLayer.GLOBAL)
    .SetFamily("haste_aura", eFamilyStackMode.HIGHEST)
    .AddTag("buff")
    .AddTag("aura")
    .AddTag("movement");

stats.move_speed.AddModifier(haste_minor);
stats.move_speed.AddModifier(haste_major);
```

In any context where both would apply:

- Catalyst computes their effective magnitudes.
- Only the stronger one contributes to the final value.

This is per-family, per-layer - you can still have a separate
movement effect in the RUNES layer if you like.

---

## Pattern 5: Armor with diminishing returns

> "Armor reduces damage with diminishing returns, capped at 75% DR."

You can implement this as a post-process curve on the `armor` stat.

```gml
stats.armor.SetPostProcess(function(_stat, _raw, _ctx) {
    var A = max(0, _raw);
    var K = 100;        // tuning constant
    var dr = A / (A + K);
    var cap = 0.75;

    dr = clamp(dr, 0, cap);
    return dr;
});
```

Now:

```gml
var damage_reduction = stats.armor.GetValue(); // 0..0.75
var damage_taken     = incoming_damage * (1 - damage_reduction);
```

You can still apply modifiers to the underlying armor stat (flat additions,
percentage increases), and they'll all flow into the curve.

---

## Pattern 6: Derived max HP from vitality and level

> "Max HP is 50 + vitality * 10 + level * 5."

```gml
/// In player Create:
stats = {
    vitality : new Statistic(10).SetName("Vitality"),
    max_hp   : new Statistic(0).SetName("Max HP"),
};

// Derived base for max_hp
stats.max_hp.SetBaseFunc(function(_stat, _ctx) {
    var vit   = stats.vitality.GetValue();
    var level = owner.level;
    return 50 + vit * 10 + level * 5;
});
```

Usage:

```gml
var max_hp_value = stats.max_hp.GetValue();
```

If you add gear or rune modifiers to `max_hp`, they will apply on top of this derived base.

---

## Pattern 7: Dispel all debuffs on an actor

Suppose you decide that any modifier tagged `"debuff"` should be removable by a cleanse.

First, expose a helper on `Statistic` (if you haven't already):

```gml
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

Then to cleanse an actor:

```gml
/// Script: CleanseActorDebuffs(actor)
function CleanseActorDebuffs(_actor) {
    with (_actor) {
        stats.damage.RemoveModifiersByTag("debuff");
        stats.move_speed.RemoveModifiersByTag("debuff");
        stats.armor.RemoveModifiersByTag("debuff");
        // ... any other stats ...
    }
}
```

You can also have more specific cleanses, like `"fire"` or `"curse"`.

---

These patterns are just starting points - the idea is to let you express
your game's rules as small, composable pieces:

- Stats for the numbers
- Modifiers for the rules
- Context for "what's going on right now?"

If you find yourself repeating a pattern, it probably deserves a helper function
or a wrapper around Catalyst that matches *your* game's vocabulary.
