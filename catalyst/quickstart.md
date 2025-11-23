---
layout: default
title: Catalyst Quickstart
parent: Catalyst
nav_order: 1
---

# Catalyst Quickstart

This page walks through the typical steps for using Catalyst in a GameMaker project:

1. Set up stats on an actor
2. Add basic modifiers (flat and percentage)
3. Use layers for gear and runes
4. Integrate duration-based modifiers
5. Do a simple item preview

---

## 1. Creating stats on an actor

A common pattern is to give each actor (player, enemy, NPC) a `stats` struct in its `Create` event.

```gml
/// obj_player Create

stats = {
    damage      : new Statistic(10).SetName("Damage"),
    move_speed  : new Statistic(3).SetName("Move Speed"),
    max_hp      : new Statistic(100).SetName("Max HP"),
    armor       : new Statistic(0).SetName("Armor"),
};

// Optional: configure rounding / clamping per stat
stats.damage.SetRounding(true, 1);          // integers
stats.move_speed.SetRounding(true, 0.01);   // 2 decimal places
stats.max_hp.SetClamped(true);              // will clamp to min/max if set
```

Later, you get the value like this:

```gml
var dmg = stats.damage.GetValue();      // canonical, cached
var spd = stats.move_speed.GetValue();  // canonical, cached
```

---

## 2. Adding basic modifiers

Let's add a flat +5 damage bonus from a weapon, and a +20% bonus from a rune.

```gml
/// Somewhere in player setup / equipment logic:
var dmg_stat = stats.damage;

// +5 flat damage from weapon
var weapon_mod = new Modifier(5, eMathOps.ADD, "Bronze Sword")
    .SetLayer(eStatLayer.EQUIPMENT)
    .AddTag("sword");

dmg_stat.AddModifier(weapon_mod);

// +20% damage from rune
var rune_mod = new Modifier(0.20, eMathOps.MULTIPLY, "Aggression Rune")
    .SetLayer(eStatLayer.RUNES)
    .AddTag("rune");

dmg_stat.AddModifier(rune_mod);
```

Getting the final damage:

```gml
var dmg_final = stats.damage.GetValue(); //  (10 + 5) * 1.2 = 18
```

---

## 3. Using layers for gear vs runes vs temporary effects

Layers let you control the order in which modifiers apply. Out of the box, Catalyst includes:

```gml
enum eStatLayer {
    BASE_BONUS, // attributes, level scaling, etc.
    EQUIPMENT,  // wand / weapon bonuses
    AUGMENTS,   // runes / talents / gems / etc
    TEMP,       // short buffs / debuffs
    GLOBAL,     // late-stage global modifiers
}
```

These are found in `scr_catalyst_macro`

For example, you might decide:

- `BASE_BONUS` - attribute-derived bonuses
- `EQUIPMENT` - weapon affixes
- `AUGMENTS` - talent tree
- `TEMP` - potions, short buffs, debuffs
- `GLOBAL` - auras, curses, global modifiers

```gml
var dmg = stats.damage;

var attr_bonus = new Modifier(2, eMathOps.ADD, "Strength")
    .SetLayer(eStatLayer.BASE_BONUS);

var wand_bonus = new Modifier(5, eMathOps.ADD, "Bronze Wand")
    .SetLayer(eStatLayer.EQUIPMENT);

var rune_bonus = new Modifier(0.20, eMathOps.MULTIPLY, "Aggression Rune")
    .SetLayer(eStatLayer.AUGMENTS);

var temp_buff = new Modifier(0.50, eMathOps.MULTIPLY, "Battle Cry")
    .SetLayer(eStatLayer.TEMP)
    .SetDuration(600)       // 600 ticks, for example
    .AddTag("buff");

dmg.AddModifier(attr_bonus);
dmg.AddModifier(wand_bonus);
dmg.AddModifier(rune_bonus);
dmg.AddModifier(temp_buff);
```

Internally, Catalyst applies modifiers in layer order, and within each layer:

1. All `ADD` modifiers
2. All `MULTIPLY` modifiers
3. Later, FORCE_MIN and post_process

---

## 4. Duration-based modifiers

Any `Modifier` with a positive duration is registered with the global `ModifierTracker`:

```gml
var buff = new Modifier(0.50, eMathOps.MULTIPLY, "Battle Cry")
    .SetLayer(eStatLayer.TEMP)
    .SetDuration(600);  // 600 ticks

stats.damage.AddModifier(buff);
```

Somewhere central (e.g. a controller object) you should tick the tracker:

```gml
/// obj_combat_controller Step
CatalystModCountdown();
```

When a modifier's `duration` reaches 0, Catalyst:

- Removes it from the tracker, and
- Removes it from its owning `Statistic` (if `remove_from_stat` is true).

---

## 5. Simple item preview ("20 → 28 damage")

You often want to preview what a stat *would* be if a modifier were added, without actually changing anything.

Use `PreviewChange` or `PreviewChanges` for this.

```gml
var dmg_stat = stats.damage;

var current = dmg_stat.GetValue();

// Suppose the hovered item grants +2 flat and +10% damage
var preview_ops = [
    {
        value      : 2,
        operation  : eMathOps.ADD,
        layer      : eStatLayer.EQUIPMENT
    },
    {
        value      : 0.10,
        operation  : eMathOps.MULTIPLY,
        layer      : eStatLayer.EQUIPMENT
    }
];

var preview = dmg_stat.PreviewChanges(preview_ops);

draw_text(x, y, "Damage: " + string(current) + " → " + string(preview));
```

You can also use `PreviewChange` for a single op:

```gml
var preview = dmg_stat.PreviewChange(0.15, eMathOps.MULTIPLY, eStatLayer.AUGMENTS);
```

Previews:

- Don't mutate the stat.
- Respect all layers, tags, families, and conditions.
- Can optionally take a context for more advanced aguments (see Advanced Topics).
