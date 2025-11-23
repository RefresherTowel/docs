---
layout: default
title: Catalyst          # children will use this as `parent:`
nav_order: 4              # order among top-level items
has_children: true        # marks this as a section (still supported)
---

# Catalyst - Stats & Modifiers for GameMaker

**Catalyst** is a flexible statistics and modifier engine for GameMaker.

It sits between your *base stats* and all the gear, runes, buffs, auras, and debuffs that react with them - and gives you a clean, predictable way to get the final value.

Catalyst is part of the **RefresherTowel Games** suite of reusable frameworks for GameMaker.

Think of Catalyst as:

> A tiny math-reactor that takes a base value, runs it through layered modifiers,
> conditions, stacks, and soft caps, and hands you back the result.

Catalyst is designed to be:

- **Game-focused** - built for typical action / roguelike / RPG stat needs.
- **Composable** - layers, families, tags and context let you express complex rules cleanly.
- **Safe to query** - supports previews and context-based evaluation without mutating state.
- **Engine-agnostic inside GameMaker** - works with structs and methods, no object-type assumptions.

---

## Core concepts

Catalyst has three main building blocks:

### 1. `Statistic`

A `Statistic` represents a single numeric stat: damage, cooldown, max HP,
move speed, crit chance, armor, etc.

It knows about:

- `base_value` - your starting value.
- `modifiers` - things that change the value (flat, percentage, clamping, etc.).
- `layers` - the order in which different groups of modifiers are applied.
- `post_process` - an optional soft-cap / curve function applied at the end.
- `base_func` - an optional derived-base formula (e.g. max HP from vitality + level).
- `tags` - labels you can use for grouping, UI, and rules.

You ask a `Statistic` for its value via:

```gml
// canonical, cached value
var dmg = stats.damage.GetValue();

// situational value for a specific context
var dmg_hit = stats.damage.GetValue(hit_ctx);
```

### 2. `Modifier`

A `Modifier` describes *how* to change a stat:

- operation: `ADD`, `MULTIPLY`, or `FORCE_MIN`
- layer: where in the pipeline it applies (BASE_BONUS, WANDS, RUNES, TEMP, GLOBAL)
- stacks: how many times it applies (stateful or context-driven)
- condition: when it is allowed to apply
- stack_func: how many stacks to use for a given context
- duration: optional lifetime in "ticks", managed by `ModifierTracker`
- family + family_mode: how modifiers of the same family combine (STACK_ALL, HIGHEST, LOWEST)
- tags: labels like `"buff"`, `"debuff"`, `"fire"`, `"movement"`

Modifiers are attached to a `Statistic`:

```gml
var damage = new Statistic(10).SetName("Damage");

var wand_bonus = new Modifier(5, eMathOps.ADD, "Bronze Wand")
    .SetLayer(eStatLayer.WANDS)
    .AddTag("wand");

damage.AddModifier(wand_bonus);
```

### 3. `ModifierTracker`

`ModifierTracker` is a small helper that tracks duration-based modifiers
and counts them down. It is usually created as `global.__modifier_tracker`
and used automatically when a `Modifier` with a positive duration is created.

You can tick it in whatever time-step makes sense for your game loop:

```gml
// e.g. in a global controller object, once per turn / wave / second / step:
global.__modifier_tracker.Countdown();
```

Any modifiers whose `duration` reaches 0 are removed from both the tracker
and their owning `Statistic`.

---

## Features at a glance

- Flat and multiplicative modifiers
- Ordered layers:
  - `BASE_BONUS` - attributes, level, ancestry
  - `WANDS`      - weapons or items
  - `RUNES`      - talents / runes / passives
  - `TEMP`       - short-lived buffs / debuffs
  - `GLOBAL`     - late-stage global effects and auras
- Context-aware evaluation via `GetValue(context)`
- Stateful stacks *and* context-driven stacks (`stack_func`)
- Conditional modifiers (`condition(stat, context)`)
- Modifier families with stacking rules (`STACK_ALL`, `HIGHEST`, `LOWEST`)
- Derived base values via `base_func(stat, context)`
- Soft caps & curves via `post_process(stat, raw_value, context)`
- Tags on both stats and modifiers
- Safe "what-if" previews:
  - `PreviewChange(...)`
  - `PreviewChanges([...])`

---

## Typical use cases

Catalyst is intended for things like:

- Damage calculation with gear, runes, and elemental modifiers.
- Movement speed modified by buffs, debuffs, and environment.
- Cooldowns that shrink with combo stacks.
- HP, armor, and resistance systems with diminishing returns.
- "Highest-of-kind" auras where only the strongest effect applies.
- Mouseover previews when hovering items: "20 → 28 damage".

See the other pages for details:

- [Quickstart](./catalyst_quickstart.md) - basic setup and simple examples.
- [Advanced Topics](./catalyst_advanced.md) - layers, families, derived stats, curves, context.
- [API Reference](./catalyst_reference.md) - full list of methods and fields.
- [Patterns & Recipes](./catalyst_patterns.md) - example runes and abilities built on Catalyst.
