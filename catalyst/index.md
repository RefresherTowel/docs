---
layout: default
title: Catalyst          # children will use this as `parent:`
nav_order: 4              # order among top-level items
has_children: true        # marks this as a section (still supported)
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

![Catalyst icon](../assets/catalyst_icon.png)
{: .text-center}

*Make your stats react*
{: .text-center}

**Catalyst** is a flexible statistics and modifier engine for GameMaker.

It sits between your *base stats* and all the gear, augments, buffs, auras, and debuffs in your game and gives you a clean, predictable way to get the final value.

Catalyst is part of the **RefresherTowel Games** suite of reusable frameworks for GameMaker.

Think of Catalyst as:

> A tiny math-reactor that takes a base value, runs it through layered modifiers,
> conditions, stacks, and soft caps, and hands you back the result.

Catalyst is designed to be:

- **Game-focused** - built for typical action / roguelike / RPG stat needs.
- **Composable** - layers, families, tags, sources and context let you express complex rules cleanly.
- **Safe to query** - supports previews and context-based evaluation without mutating state.
- **Engine-agnostic inside GameMaker** - works with structs and methods, no object-type assumptions.

---

## Core concepts

Catalyst has three main building blocks:

### 1. `CatalystStatistic` (the stat)

A `CatalystStatistic` represents a single numeric stat: damage, cooldown, max HP,
move speed, crit chance, armor, etc.

It knows about:

#### Core

- `base_value` - your starting value.
- `min_value` / `max_value` - optional clamping bounds.
- `rounded` - whether to round to integer when returning values.
- Attached `CatalystModifier` instances that change the value.

You ask a stat for its value via:

```js
// canonical, cached value
var dmg = stats.damage.GetValue();

// situational value for a specific context
var dmg_hit = stats.damage.GetValue(hit_ctx);
```

#### Advanced

- **Layers** - the order in which groups of modifiers apply
  (`eCatStatLayer.BASE_BONUS`, `EQUIPMENT`, `AUGMENTS`, `TEMP`, `GLOBAL`).
- **Derived base** - `base_func(stat, context)` to compute the base from other stats
  (for example, max HP from vitality and level).
- **Post-processing** - `post_process(stat, raw_value, context)` for soft caps and curves.
- **Tags** - labels on the stat itself for grouping and rules.
- **On-change callbacks** - functions invoked when the cached value changes.
- **Context-aware evaluation** - every condition / stack / base / post function can
  receive an optional `_context` you pass into `GetValue(context)`.

---

### 2. `CatalystModifier` (the change)

A `CatalystModifier` describes *how* to change a stat.

#### Core

- **Amount** - `value`, the number you add or multiply with.
- **Operation** - one of `eCatMathOps.ADD`, `eCatMathOps.MULTIPLY`,
  `eCatMathOps.FORCE_MIN`, or `eCatMathOps.FORCE_MAX`.
- **Duration** - optional lifetime in "ticks", managed by the global `CatalystModifierTracker`.

#### Advanced

- **Layer** - where in the pipeline it applies (`eCatStatLayer.BASE_BONUS`, `EQUIPMENT`,
  `AUGMENTS`, `TEMP`, `GLOBAL`).
- **Stacks** - `stacks` and `max_stacks` control how many times it applies
  (default `max_stacks` is `infinity`).
- **Condition** - `condition(stat, context)` decides whether it applies at all.
- **Context-driven stacks** - `stack_func(stat, context)` computes effective stacks
  from the current situation.
- **Families** - `family` and `family_mode` (`STACK_ALL`, `HIGHEST`, `LOWEST`)
  control how modifiers of the same "kind" combine.
- **Tags** - labels like `"buff"`, `"debuff"`, `"fire"`, `"movement"` used for querying
  and bulk remove / find.
- **Sources** - three separate ways to track where a modifier came from:
  - `source_label` - human-readable label (for example `"Bronze Wand"`).
  - `source_id` - handle (instance, owner struct, inventory item, etc.).
  - `source_meta` - arbitrary metadata (often a struct) for custom logic.
  The stat API includes helpers to find / test / remove modifiers by any of these.
- **Previews** - the stat can simulate modifiers as if they were applied,
  without actually attaching them, via `PreviewChange` and `PreviewChanges`.

Modifiers are attached to a `CatalystStatistic`:

```js
var damage = new CatalystStatistic(10).SetName("Damage");

var wand_bonus = new CatalystModifier(5, eCatMathOps.ADD)
    .SetLayer(eCatStatLayer.EQUIPMENT)
    .SetSourceLabel("Bronze Wand")
    .AddTag("wand");

damage.AddModifier(wand_bonus);
```

---

### 3. `CatalystModifierTracker` (the timer)

`CatalystModifierTracker` is a small helper that tracks duration-based modifiers
and counts them down.

Catalyst ships with one global tracker instance:

- `global.__catalyst_modifier_tracker` - created for you at startup.
- The macro `CATALYST_COUNTDOWN` points at this instance.
- Timed `CatalystModifier` instances register with it automatically
  when their `duration` is greater than 0.

You tick it in whatever time-step makes sense for your game loop:

```js
// e.g. in a global controller object, once per turn / wave / second / step:
CatalystModCountdown();
```

Any modifiers whose `duration` reaches 0 are removed from both the tracker
and their owning `CatalystStatistic`.

---

## Features at a glance

### Core features

- Simple numeric stats via `CatalystStatistic`.
- Flat and multiplicative modifiers via `CatalystModifier`
  (`ADD`, `MULTIPLY`, `FORCE_MIN`, `FORCE_MAX`).
- Ordered layers so different sources of power stack predictably:
  - `BASE_BONUS` - attributes, level scaling, ancestry.
  - `EQUIPMENT`  - weapons, wands, gear.
  - `AUGMENTS`   - runes, talents, gems, passive trees.
  - `TEMP`       - short-lived buffs and debuffs.
  - `GLOBAL`     - late-stage global effects and auras.
- Timed modifiers with durations, tracked by a global `CatalystModifierTracker`
  and advanced by `CatalystModCountdown()`.

### Advanced features

- Context-aware evaluation via `GetValue(context)`.
- Stateful stacks and context-driven stacks (`stack_func(stat, context)`).
- Conditional modifiers (`condition(stat, context)`).
- Modifier families with stacking rules (`STACK_ALL`, `HIGHEST`, `LOWEST`).
- Derived base values via `base_func(stat, context)`.
- Soft caps and curves via `post_process(stat, raw_value, context)`.
- Source-aware management:
  - Track modifiers by `source_label`, `source_id`, or `source_meta`.
  - Find, test, and remove modifiers based on where they came from.
- Tags on both stats and modifiers for grouping, UI, and rule logic.
- Safe "what-if" previews:
  - `PreviewChange(...)` for a single hypothetical modifier.
  - `PreviewChanges([...])` for batches of hypothetical changes.

---

## Typical use cases

Catalyst is intended for things like:

- Damage calculation with gear, runes, augments, and elemental modifiers.
- Movement speed modified by buffs, debuffs, and environment.
- Cooldowns that shrink with combo stacks.
- HP, armor, and resistance systems with diminishing returns.
- "Highest-of-kind" auras where only the strongest effect applies.
- Mouseover previews when hovering items: `20 -> 28 damage`.

