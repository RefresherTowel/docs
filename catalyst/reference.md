---
layout: default
title: Catalyst Scripting Reference
parent: Catalyst
nav_order: 3
---

# Catalyst API Reference

This page lists the main types, enums, and methods provided by Catalyst.

It is organized as:

- [Enums](#enums)
- [Statistic](#statistic)
- [Modifier](#modifier)
- [ModifierTracker](#modifiertracker)

---

## Enums

### `eMathOps`

```gml
enum eMathOps {
    ADD,
    MULTIPLY,
    FORCE_MIN,
}
```

- `ADD` - flat addition  
- `MULTIPLY` - multiplicative scaling (applied as `(1 + value) ^ stacks`)  
- `FORCE_MIN` - enforces a minimum value (applied after ADD/MULTIPLY)

---

### `eStatLayer`

```gml
enum eStatLayer {
    BASE_BONUS, // attributes, level scaling, etc.
    WANDS,      // wand / weapon bonuses
    RUNES,      // runes / talents
    TEMP,       // short buffs / debuffs
    GLOBAL,     // late-stage global modifiers
}
```

Layers are applied in the order listed above.

---

### `eFamilyStackMode`

```gml
enum eFamilyStackMode {
    STACK_ALL,
    HIGHEST,
    LOWEST,
}
```

- `STACK_ALL` - all modifiers in the family apply as usual.  
- `HIGHEST` - only the strongest modifier in the family applies (per layer, per context).  
- `LOWEST` - only the weakest modifier in the family applies (per layer, per context).

---

## Statistic

### Construction

```gml
var stat = new Statistic(_value, _min_value, _max_value);
```

- `_value` - starting base value.
- `_min_value` - minimum allowed value when clamped (default `-infinity`).
- `_max_value` - maximum allowed value when clamped (default `infinity`).

### Core fields

These fields are typically not mutated directly; use methods instead.

- `base_value` - current base value.
- `starting_value` - initial base value (used by `ResetToStarting` / `ResetAll`).
- `current_value` - cached canonical value (contextless).
- `min_value`, `max_value` - clamp bounds.
- `clamped` - whether clamp is active.
- `rounded` - whether rounding is active.
- `round_step` - step used for rounding.
- `modifiers` - array of `Modifier` structs.
- `altered` - flag indicating that the numeric value needs recomputation.
- `name` - debug/display name.
- `post_process` - optional soft-cap/curve function: `fn(stat, raw_value, context)`.
- `base_func` - optional derived base function: `fn(stat, context)`.
- `tags` - array of tag strings.

### Getting values

```gml
stat.GetValue();
stat.GetValue(context);
```

- `GetValue()` - returns the canonical cached value, recomputing if `altered` is true.
  - Updates `current_value`.
  - Clears `altered`.
  - Fires any on-change callbacks if the numeric value changed.

- `GetValue(context)` - returns a freshly evaluated value for the given context.
  - Does *not* touch `current_value` or `altered`.
  - Does *not* fire on-change callbacks.

### Modifier management

```gml
stat.AddModifier(mod);
stat.RemoveModifierById(mod);
stat.RemoveAllModifiers();
stat.RemoveModifierBySource(source_id);
stat.RemoveModifierByPosition(pos);

stat.FindModifiersBySource(source_id);
stat.FindModifiersById(mod);
stat.HasModifierFromSource(source_id);
stat.HasModifier(mod);
```

- `AddModifier(mod)` - attaches a `Modifier` and marks the stat as altered.
- `RemoveModifierById(mod)` - removes the specific modifier instance.
- `RemoveAllModifiers()` - removes and destroys all modifiers.
- `RemoveModifierBySource(source_id)` - removes modifiers whose `source_id` matches.
- `RemoveModifierByPosition(pos)` - removes modifier at index `pos` in the array.

- `FindModifiersBySource(source_id)` - returns array of matching modifiers.
- `FindModifiersById(mod)` - returns array of modifiers equal to `mod`.
- `HasModifierFromSource(source_id)` - true if there is at least one modifier from that source.
- `HasModifier(mod)` - true if the modifier is attached.

### On-change callbacks

```gml
var ids = stat.AddOnChangeFunction(fn1, fn2, ...);
var ok  = stat.RemoveOnChangeFunction(id);
```

- Callbacks are functions of the form: `fn(stat, old_value, new_value)`.
- `AddOnChangeFunction(...)` returns an array of numeric IDs (one per function).
- `RemoveOnChangeFunction(id)` removes the callback with that ID.

Callbacks only fire when:

- You call `GetValue()` with no context, and  
- The numeric value actually changed.

### Previews

```gml
stat.PreviewChange(
    _mod_value,
    _mod_op,
    _layer,
    _stacks,
    _max_stacks,
    _condition,
    _stack_func,
    _context,
    _family,
    _family_mode
);

stat.PreviewChanges(extra_ops, context);
```

- `PreviewChange(...)` - preview a single hypothetical modifier/op.
- `PreviewChanges(extra_ops, context)` - preview many hypothetical ops.

Both:

- Do not mutate the stat.
- Respect layers, conditions, stack_func, families and tags.

`extra_ops` is an array of lightweight structs with fields:

- `value`
- `operation`
- Optional: `layer`, `stacks`, `max_stacks`, `condition`, `stack_func`, `family`, `family_mode`

### Configuration helpers

```gml
stat.SetClamped(bool);
stat.SetRounding(enabled, step);
stat.SetName(name);

stat.SetBaseValue(amount);
stat.SetMaxValue(amount);
stat.SetMinValue(amount);

stat.ChangeBaseValue(delta);
stat.ChangeMaxValue(delta);
stat.ChangeMinValue(delta);

stat.ResetToStarting();
stat.ResetAll();
```

- `SetClamped(bool)` - enables/disables clamping to `min_value` / `max_value`.
- `SetRounding(enabled, step)` - enables/disables rounding, with step (e.g. 1, 0.1, 0.01).
- `SetName(name)` - sets debug/display name.

- `SetBaseValue(amount)` - sets `base_value` directly.
- `SetMaxValue(amount)`, `SetMinValue(amount)` - set clamp bounds.
- `ChangeBaseValue(delta)` - adds to `base_value`, applying clamp/round if enabled.
- `ChangeMaxValue(delta)`, `ChangeMinValue(delta)` - adjust clamp bounds.

- `ResetToStarting()` - sets `base_value` back to `starting_value`.
- `ResetAll()` - resets base, current, modifiers, clamp, rounding, post_process, base_func, tags.

### Derived base & post-process

```gml
stat.SetBaseFunc(fn);
stat.ClearBaseFunc();

stat.SetPostProcess(fn);
stat.ClearPostProcess();
```

- `SetBaseFunc(fn)` - `fn(stat, context) -> base_value`.
- `SetPostProcess(fn)` - `fn(stat, raw_value, context) -> final_value`.

### Tags

```gml
stat.AddTag(tag);
stat.RemoveTag(tag);
stat.HasTag(tag);
stat.ClearTags();
```

Tags are free-form strings. Catalyst itself doesn't interpret them; they're for your rules/UI.

### Debug

```gml
stat.DebugDescribe();
```

Logs a human-readable dump of the stat and its modifiers to the debug output.

---

## Modifier

### Construction

```gml
var mod = new Modifier(_value, _math_operation, _source_text, _duration, _source_id);
```

- `_value` - the magnitude of the modifier.
- `_math_operation` - one of `eMathOps.ADD`, `MULTIPLY`, `FORCE_MIN`.
- `_source_text` - human-readable source label (e.g. `"Bronze Wand"`).
- `_duration` - positive number for timed effects, `-1` for permanent.
- `_source_id` - optional source handle (instance, item struct, etc.).

### Core fields

- `source` - human-readable label.
- `source_id` - opaque source identifier.
- `value` - base value for this modifier.
- `operation` - math operation (ADD / MULTIPLY / FORCE_MIN).
- `duration` - remaining duration (ticks).
- `duration_max` - initial duration.
- `duration_applied` - whether it was registered with `ModifierTracker`.
- `stacks` - current stacks for this modifier.
- `max_stacks` - maximum stacks.
- `layer` - one of the `eStatLayer` values.
- `condition` - optional function: `fn(stat)` or `fn(stat, context)`.
- `stack_func` - optional function: `fn(stat, context) -> stacks`.
- `family` - optional family key (string or enum).
- `family_mode` - one of `eFamilyStackMode`.
- `tags` - array of tag strings.
- `applied_stat` - the `Statistic` this modifier is attached to (or `noone`).
- `remove_from_stat` - whether to remove from the stat when destroyed via tracker.

### Methods

```gml
mod.ApplyDuration();
mod.SetDuration(duration);

mod.SetValue(value);
mod.SetMathsOp(op);
mod.SetSource(text);
mod.SetSourceId(id);

mod.SetLayer(layer);

mod.SetStacks(stacks);
mod.AddStacks(delta);
mod.SetMaxStacks(max);

mod.SetCondition(fn);
mod.ClearCondition();

mod.SetStackFunc(fn);
mod.ClearStackFunc();

mod.SetFamily(family, mode);
mod.ClearFamily();
mod.SetFamilyMode(mode);

mod.AddTag(tag);
mod.RemoveTag(tag);
mod.HasTag(tag);
mod.ClearTags();

mod.Destroy(remove_from_stat);
mod.ResetDuration();
```

Notes:

- `SetDuration(duration)`:
  - Sets `duration` and `duration_max`.
  - Registers the modifier with `global.__modifier_tracker` (via `ApplyDuration()`).
- `SetLayer(layer)`:
  - Changes the layer; marks the owning stat as altered.
- `SetStacks`, `AddStacks`, `SetMaxStacks`:
  - Used for stateful stacks; `stack_func` is for context-driven stacks.
- `SetCondition(fn)`:
  - Sets a predicate controlling whether this modifier applies.
- `SetStackFunc(fn)`:
  - Sets a function to compute stacks from context.
- `SetFamily(family, mode)`:
  - Sets `family` and `family_mode` (defaults to `HIGHEST` if not provided).
- `Destroy(remove_from_stat)`:
  - Removes the modifier from the tracker and, if `remove_from_stat` is true, from its owning `Statistic`.

---

## ModifierTracker

`ModifierTracker` is a small helper used to manage timed modifiers.

### Construction

Catalyst typically creates a global instance:

```gml
global.__modifier_tracker = new ModifierTracker();
```

You can also construct your own if you want multiple trackers.

### Fields

- `modifiers` - array of tracked `Modifier` structs.

### Methods

```gml
tracker.AddModifier(mod);
tracker.RemoveModifierById(mod);
tracker.RemoveModifierByPos(pos);
tracker.Countdown();
tracker.DebugDump();
```

- `AddModifier(mod)` - registers a modifier for duration tracking.
- `RemoveModifierById(mod)` - removes the given modifier wherever it appears.
- `RemoveModifierByPos(pos)` - removes modifier at index `pos`.
- `Countdown()` - decrements `duration` for all modifiers; removes those reaching 0.
- `DebugDump()` - logs the current contents of the tracker.

### Typical usage

```gml
/// Global or controller Create
if (!variable_global_exists("__modifier_tracker")) {
    global.__modifier_tracker = new ModifierTracker();
}

/// Global or controller Step
if (variable_global_exists("__modifier_tracker")) {
    global.__modifier_tracker.Countdown();
}
```

When a `Modifier` is created with `duration > 0`, Catalyst automatically calls
`ApplyDuration`, which registers it with the tracker.
