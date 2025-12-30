---
layout: default
title: Scripting Reference
parent: Catalyst
nav_order: 3
---

# Catalyst API Reference

This page lists the main types, enums, and methods provided by **Catalyst**.

It is organized as:

- [Enums](#enums)
- [CatalystStatistic](#catalyststatistic)
- [CatalystModifier](#catalystmodifier)
- [CatalystModifierTracker & Countdown](#catalystmodifiertracker--countdown)

The **Quickstart** and **Advanced Topics** pages show how these pieces are used
together in practice. This page is more of a "what exists and what it does"
reference.

---

## Enums

### `eCatMathOps`

```js
enum eCatMathOps {
    ADD,
    MULTIPLY,
    FORCE_MIN,
    FORCE_MAX,
}
```

- `ADD`  
  Flat addition; applied as `value * stacks` and added to the running value.

- `MULTIPLY`  
  Multiplicative scaling; applied as:

  ```js
  _value *= power(1 + value, stacks);
  ```

  So a modifier with `value = 0.20` and `stacks = 2` produces a factor of
  `(1.20 ^ 2)`.

- `FORCE_MIN`  
  Enforces a minimum value **after** all ADD and MULTIPLY effects are applied.
  FORCE_MIN modifiers are applied in a separate stage before post-processing
  and are excluded from family comparisons.

- `FORCE_MAX`  
  Enforces a maximum value **after** ADD/MULTIPLY and FORCE_MIN effects are
  applied. FORCE_MAX modifiers are applied in a separate stage before
  post-processing and are excluded from family comparisons.

---

### `eCatStatLayer`

```js
enum eCatStatLayer {
    BASE_BONUS, // attributes, level scaling, etc.
    EQUIPMENT,  // wand / weapon bonuses
    AUGMENTS,   // runes / talents / gems / etc
    TEMP,       // short buffs / debuffs
    GLOBAL,     // late-stage global modifiers
}
```

Layers control *when* modifiers apply in the pipeline. For example:

- `BASE_BONUS` - base stats, level-based bonuses, ancestry.
- `EQUIPMENT` - weapons, wands, armor, accessories.
- `AUGMENTS` - runes, talents, passive trees, gems.
- `TEMP` - temporary buffs and debuffs.
- `GLOBAL` - global auras and late-stage effects.

Catalyst processes layers in this order when evaluating a stat.

---

### `eCatFamilyStackMode`

```js
enum eCatFamilyStackMode {
    STACK_ALL,  // default: all apply
    HIGHEST,    // only the strongest effect in the family applies
    LOWEST,     // only the weakest effect in the family applies
}
```

- `STACK_ALL` - all modifiers in the family apply as usual.  
- `HIGHEST` - only the strongest modifier in the family applies
  (per layer, per context).  
- `LOWEST` - only the weakest modifier in the family applies
  (per layer, per context).

Family stacking is configured per modifier; see
[Modifier families](#families--stacking) in the `CatalystModifier` section.

---

## `CatalystStatistic`

A `CatalystStatistic` represents a single numeric stat: damage, armor, movement
speed, cooldown, etc.

### Construction

```js
stat = new CatalystStatistic(_value, _min_value, _max_value);
```

- `_value` - starting base value.
- `_min_value` - minimum allowed value when clamped (default `-infinity`).
- `_max_value` - maximum allowed value when clamped (default `infinity`).

In most cases you create stats once (for example in an actor's `Create` event)
and then attach modifiers to them over time.

---

### Core fields

These fields are typically not mutated directly; use methods instead, but it's
useful to know what exists.

- `base_value` - base (pre-modifier) value.
- `starting_value` - initial base value at construction time.
- `current_value` - cached canonical value (result of the last `GetValue()`).
- `base_func` - optional callback `fn(stat, context) -> Real` that overrides
  `base_value` when present.

- `min_value` - minimum allowed value when `clamped` is true.
- `max_value` - maximum allowed value when `clamped` is true.
- `clamped` - whether final values are clamped to `[min_value, max_value]`.

- `rounded` - whether final values are rounded.
- `round_step` - step used for rounding (1 for integers, 0.01 for 2 decimals, etc).

- `modifiers` - array of attached `CatalystModifier` instances.
- `altered` - `true` when the numeric value needs recomputing.

- `name` - optional display name for the stat.
- `on_change_callbacks` - array of `{ ident, fn }` structures registered via
  `AddOnChangeFunction`.
- `on_change_next_id` - internal id counter for callbacks.

- `post_process` - optional callback `fn(stat, raw_value, context) -> Real`
  that runs after all modifiers and families are applied.
- `tags` - array of tag strings assigned to the stat.

---

### Static setup (saves / reload)

If you serialise stats and modifiers (for example, in a save system), the static methods on modifiers need to be reattached after loading. Catalyst provides a helper:

```js
// After loading stats/modifiers from disk
stat.StaticSetup();
```

`StaticSetup()` walks the stat's attached modifiers and re-applies the `CatalystModifier` static methods. Call it once per stat after deserialising.

---

### Modifier management

Attach and remove modifiers from a stat:

```js
stat.AddModifier(mod);

stat.RemoveModifierById(mod);
stat.RemoveAllModifiers();

stat.RemoveModifierBySourceLabel(source_label);
stat.RemoveModifierBySourceId(source_id);
stat.RemoveModifierBySourceMeta(predicate_func);

stat.RemoveModifierByPosition(pos);

stat.RemoveModifiersByTag(tag);

var _mods_by_id    = stat.FindModifiersById(mod);
var _mods_by_label = stat.FindModifiersBySourceLabel(source_label);
var _mods_by_id2   = stat.FindModifiersBySourceId(source_id);
var _mods_by_meta  = stat.FindModifiersBySourceMeta(predicate_func);

var _has_from_id    = stat.HasModifierFromSourceId(source_id);
var _has_from_label = stat.HasModifierFromSourceLabel(source_label);
var _has_from_meta  = stat.HasModifierFromSourceMeta(predicate_func);
var _has_mod        = stat.HasModifier(mod);
```

- `AddModifier(mod)`  
  Attaches a `CatalystModifier` and marks the stat as altered. The modifier's
  `applied_stat` field is set to this stat. If the modifier is already attached
  to another stat, the call is ignored and an `EchoDebugWarn` message is emitted.
  If it is already attached to this stat, the call is a no-op.

- `RemoveModifierById(mod)`  
  Removes the first matching modifier instance from this stat, calls
  `Destroy(false)`, and marks the stat as altered. Returns `true` if a modifier
  was removed.

- `RemoveAllModifiers()`  
  Removes and destroys all modifiers on this stat and marks it as altered.

- `RemoveModifierBySourceLabel(source_label)`  
  Removes all modifiers whose `source_label` equals the provided value.

- `RemoveModifierBySourceId(source_id)`  
  Removes all modifiers whose `source_id` equals the provided value.

- `RemoveModifierBySourceMeta(predicate_func)`  
  Removes all modifiers where `predicate_func(mod.source_meta)` returns `true`.

- `RemoveModifierByPosition(pos)`  
  Removes the modifier at index `pos` in the `modifiers` array, if it exists.

- `RemoveModifiersByTag(tag)`  
  Removes all modifiers that have the given tag.

- `FindModifiersBySourceId(source_id)`  
  Returns an array of modifiers whose `source_id` matches.

- `FindModifiersBySourceLabel(source_label)`  
  Returns an array of modifiers whose `source_label` matches.

- `FindModifiersBySourceMeta(predicate_func)`  
  Returns an array of modifiers whose `source_meta` passes the predicate.

- `FindModifiersById(mod)`  
  Returns an array of modifiers equal to the given instance (either empty or
  containing the instance).

- `HasModifierFromSourceId(source_id)`  
  `true` if any modifier on the stat has that `source_id`.

- `HasModifierFromSourceLabel(source_label)`  
  `true` if any modifier on the stat has that `source_label`.

- `HasModifierFromSourceMeta(predicate_func)`  
  `true` if any modifier's `source_meta` makes the predicate return `true`.

- `HasModifier(mod)`  
  `true` if the given modifier instance is currently attached to this stat.

All removal helpers call `Destroy(false)` on modifiers so that they are
properly removed from the global tracker (if applicable) without triggering
recursive stat cleanup.

---

### On-change callbacks

You can register callbacks that fire when the **canonical value** changes
(i.e. when `GetValue()` is called with no context and produces a new value):

```js
var _ids = stat.AddOnChangeFunction(fn1, fn2, ...);

// Later, to remove a specific callback:
var _removed = stat.RemoveOnChangeFunction(_ids[0]);
```

- `AddOnChangeFunction(fn1, fn2, ...)`  
  Registers one or more functions to be called as:

  ```js
  fn(stat, old_value, new_value);
  ```

  Returns an array of numeric IDs for the registered callbacks.

- `RemoveOnChangeFunction(id)`  
  Removes a previously registered callback by ID. Returns `true` if a callback
  was found and removed.

Callbacks are fired only when `GetValue()` (no context) is called and the
computed value differs from `current_value`.

---

### Getting values and previews

```js
var _base   = stat.GetBaseValue();
var _value  = stat.GetValue();
var _value2 = stat.GetValue(context);
var _value3 = stat.GetValuePreview(context);

var _preview1 = stat.PreviewChange(
    mod_value,
    mod_op,
    layer,
    stacks,
    max_stacks,
    condition,
    stack_func,
    context,
    family,
    family_mode
);

var _preview2 = stat.PreviewChanges(extra_ops_array, context);
```

- `GetValue()`  
  Returns the canonical cached value, recomputing if `altered` is true.
  - Recomputes via `_EvaluateWithExtraOps([], undefined)` if needed.
  - Updates `current_value`.
  - Clears `altered`.
  - Fires on-change callbacks if the numeric value changed.

- `GetValue(context)`  
  Returns a freshly evaluated value for the given context.
  - Uses `_EvaluateWithExtraOps([], context)`.
  - Does **not** change `current_value` or `altered`.
  - Does **not** fire on-change callbacks.

- `GetValuePreview(context)`  
  Returns a freshly evaluated value for the given context without caching or
  callbacks (same evaluation path as `GetValue(context)`).

- `PreviewChange(...)`  
  Simulates what the stat value would be if a **single** extra operation were
  applied on top of existing modifiers. Parameters:

  ```js
  _mod_value,
  _mod_op,
  _layer      = eCatStatLayer.AUGMENTS,
  _stacks     = 1,
  _max_stacks = -1, // defaults to _stacks if negative
  _condition  = undefined,
  _stack_func = undefined,
  _context    = undefined,
  _family     = "",
  _family_mode= eCatFamilyStackMode.STACK_ALL
  ```

  Returns the simulated value without mutating the stat.

- `PreviewChanges(extra_ops_array, context)`  
  Simulates what the stat value would be if **all** extra operations in
  `extra_ops_array` were applied together, in addition to existing modifiers.

  Each `extra_op` is a struct with the same fields as a modifier's core fields:
  `.value`, `.operation`, `.layer`, `.stacks`, `.max_stacks`, `.condition`,
  `.stack_func`, `.family`, `.family_mode`.

  Returns the simulated value without mutating the stat.

---

### Configuration helpers

```js
stat.SetClamped(true);
stat.SetRounding(true, 1);

stat.SetName("Damage");

stat.SetBaseValue(10);
stat.SetBaseFunc(fn);
stat.ClearBaseFunc();
stat.SetPostProcess(fn);
stat.ClearPostProcess();

stat.SetMaxValue(100);
stat.SetMinValue(0);

stat.ChangeBaseValue(5);
stat.ChangeMaxValue(10);
stat.ChangeMinValue(-5);

stat.ResetToStarting();
stat.ResetAll();
```

- `SetClamped(enabled = true)`  
  Enables/disables clamping to `[min_value, max_value]`.

- `SetRounding(enabled, step = 1)`  
  Enables/disables rounding and sets the rounding step.

- `SetName(name)`  
  Sets the stat's human-readable name.

- `SetBaseValue(amount)`  
  Sets `base_value` and marks the stat as altered.

- `SetBaseFunc(fn)`  
  Sets a base-value function `fn(stat, context) -> Real` that overrides
  `base_value` when present. Logs a debug message and ignores the call if
  `fn` is not callable.

- `ClearBaseFunc()`  
  Clears the base-value function so `base_value` is used directly again.

- `SetPostProcess(fn)`  
  Sets a post-process function `fn(stat, raw_value, context) -> Real` that runs
  after all modifiers and family rules, before clamping and rounding. Logs a
  debug message and ignores the call if `fn` is not callable.

- `ClearPostProcess()`  
  Clears the post-process function.

- `SetMaxValue(amount)` / `SetMinValue(amount)`  
  Set clamp bounds; mark the stat as altered.

- `ChangeBaseValue(amount)`  
  Adds `amount` to `base_value`, then reapplies clamping and rounding rules
  and marks the stat as altered.

- `ChangeMaxValue(amount)` / `ChangeMinValue(amount)`  
  Add `amount` to the corresponding bound; mark the stat as altered.

- `ResetToStarting()`  
  Resets `base_value` to `starting_value` and marks the stat as altered.

- `ResetAll()`  
  Restores the stat's base/derived configuration to defaults:

  - Sets `base_value` and `current_value` to `starting_value`.
  - Removes all modifiers.
  - Resets clamp bounds to `[-infinity, +infinity]`.
  - Clears `base_func`, `post_process`, callbacks, and tags.
  - Resets the on-change callback id counter.
  - Marks the stat as altered.

---

### Getters & debug

```js
var _starting = stat.GetStartingValue();
var _base     = stat.GetBaseValue();
var _min_val  = stat.GetMinValue();
var _max_val  = stat.GetMaxValue();
var _name     = stat.GetName();

stat.DebugDescribe();
```

- `GetStartingValue()` - returns `starting_value`.
- `GetBaseValue()` - returns `base_value`.
- `GetMaxValue()` - returns `max_value`.
- `GetMinValue()` - returns `min_value`.
- `GetName()` - returns `name`.

- `DebugDescribe()` - writes a summary of the stat and all attached modifiers
  to the debug output, including value, operation, stacks, layer, duration,
  tags, and source label. Uses `GetValuePreview()` so it does not fire
  on-change callbacks or mutate `current_value`.

---

### Stat tags

```js
stat.AddTag("offense");
stat.AddTag("fire");

if (stat.HasTag("offense")) {
    // show in offensive stats section
}

stat.RemoveTag("fire");
stat.ClearTags();
```

- `AddTag(tag)` - adds a tag if not already present.
- `RemoveTag(tag)` - removes a tag if present.
- `HasTag(tag)` - `true` if the tag is present.
- `ClearTags()` - removes all tags from the stat.

Tags do not affect the math; they are for grouping, UI, and your own logic.

---

## `CatalystModifier`

A `CatalystModifier` represents a single rule for changing a stat.

### Construction

```js
var _mod = new CatalystModifier(
    _value,
    _math_operation,
    _duration      = -1,
    _source_label  = "",
    _source_id     = noone,
    _source_meta   = undefined
);
```

- `_value` - base strength of the modifier.
- `_math_operation` - one of `eCatMathOps.ADD`, `MULTIPLY`, `FORCE_MIN`, or
  `FORCE_MAX`.
- `_duration` - number of ticks the modifier should last.
  - `-1` - permanent (not tracked by the global tracker).
  - `> 0` - timed; will be registered with the global tracker.
- `_source_label` - human-readable label for the source (weapon name, skill, etc.).
- `_source_id` - handle for the source (instance id, owner struct, item reference, etc.).
- `_source_meta` - arbitrary metadata (often a struct) for custom logic.

After construction you usually configure stacks, layers, conditions, etc. and
then call `stat.AddModifier(mod)` to attach it.

---

### Core fields

- `value` - base strength of the modifier.
- `operation` - one of `eCatMathOps.ADD`, `MULTIPLY`, `FORCE_MIN`, or
  `FORCE_MAX`.

- `duration` - remaining duration in ticks.
- `duration_max` - original or "max" duration value for reference.
- `duration_applied` - whether the modifier has been registered with the tracker.

- `stacks` - current stack count (stateful, event-driven).
- `max_stacks` - maximum allowed stack count (defaults to `infinity`).
- `layer` - layer in which this modifier is applied (`eCatStatLayer`).

- `condition` - optional predicate `fn(stat)` or `fn(stat, context) -> Bool`
  controlling whether the modifier applies at all.

- `stack_func` - optional callback `fn(stat, context) -> Real` that can compute
  effective stacks directly from context (environment-driven stacks).

- `family` - family key (string or enum) for family stacking.
- `family_mode` - one of `eCatFamilyStackMode` controlling how this family stacks.

- `tags` - array of tag strings on the modifier.

- `source_label` - human-readable label for where this modifier came from.
- `source_id` - handle for the source object.
- `source_meta` - arbitrary metadata associated with the source.

- `applied_stat` - the `CatalystStatistic` this modifier is currently attached to
  (or `noone` if not attached).
- `remove_from_stat` - internal flag used when destroying the modifier to avoid
  recursive removal loops.

---

### Duration & tracking

```js
mod.ApplyDuration();
mod.SetDuration(5);
mod.ResetDuration();
```

- `ApplyDuration()`  
  Registers the modifier with the global `CatalystModifierTracker` if
  `duration > 0` and it is not already applied. Creates the global tracker
  if it does not exist yet.

- `SetDuration(duration)`  
  Sets `duration` and `duration_max` and re-syncs with the tracker:

  - If the new duration is negative, the modifier is removed from the tracker.
  - If the new duration is positive, it is (re)applied via `ApplyDuration()`.
  - A duration of `0` is not tracked (if it was tracked, it will expire on the
    next `Countdown()` tick).

  Returns the modifier for chaining.

- `ResetDuration()`  
  Resets `duration` back to `duration_max` and re-syncs with the global tracker
  (equivalent to `SetDuration(duration_max)`).

> **Note:** Timed modifiers are automatically registered with the tracker when
> you construct them with a positive `_duration` or when you call `SetDuration`
> with a positive value.

---

### Value, operation, and layer

```js
mod.SetValue(5);
mod.SetMathsOp(eCatMathOps.MULTIPLY);
mod.SetLayer(eCatStatLayer.AUGMENTS);
```

- `SetValue(value)`  
  Sets the modifier's `value`. If the modifier is attached to a
  `CatalystStatistic`, marks that stat as altered.

- `SetMathsOp(maths_op)`  
  Sets the modifier's `operation` (`ADD`, `MULTIPLY`, `FORCE_MIN`, or
  `FORCE_MAX`). Marks the owning stat as altered if attached.

- `SetLayer(layer)`  
  Sets the `eCatStatLayer` this modifier should apply in. Marks the owning stat
  as altered if attached.

---

### Stacks

```js
mod.SetStacks(3);
mod.AddStacks(1);
mod.SetMaxStacks(5);
```

- `SetStacks(stacks)`  
  Sets the current stack count, clamped to `[0, max_stacks]`.

- `AddStacks(delta)`  
  Adds `delta` to the stack count, then clamps to `[0, max_stacks]` if needed.

- `SetMaxStacks(max_stacks)`  
  Sets the maximum stack count. If the current `stacks` exceeds the new max,
  it is clamped down. Defaults are unlimited (`max_stacks = infinity`) until
  you set a cap.

Stacks are used both for stateful buffs (event-driven) and in combination with
`stack_func` for environment-driven stacks.

---

### Conditions

```js
mod.SetCondition(function(_stat, _ctx) {
    return _ctx.target_frozen;
});

mod.ClearCondition();
```

- `SetCondition(fn)`  
  Sets a predicate that decides whether the modifier applies:

  - Called as `fn(stat)` when evaluating without context.
  - Called as `fn(stat, context)` when evaluating with context.

  If the condition returns `false`, the modifier is skipped entirely.

- `ClearCondition()`  
  Clears the condition (equivalent to "always applies").

---

### Context-driven stacks (`stack_func`)

```js
mod.SetStackFunc(function(_stat, _ctx) {
    return clamp(_ctx.burning_enemy_count, 0, 10);
});

mod.ClearStackFunc();
```

- `SetStackFunc(fn)`  
  Sets a stack function `fn(stat, context) -> Real` that computes effective
  stacks from context. Used for environment-driven stacks such as "+5% damage
  per burning enemy nearby".

  When evaluating with a context, Catalyst:

  - Starts from `stacks` as the base.
  - If `stack_func` is set, calls it to get an effective stack count.
  - Clamps the result to `>= 0` and to `max_stacks` (defaults to `infinity`).

- `ClearStackFunc()`  
  Clears the stack function; stacks will then be taken directly from the
  `stacks` field.

---

### Families & stacking

```js
mod.SetFamily("movement_aura", eCatFamilyStackMode.HIGHEST);
mod.SetFamilyMode(eCatFamilyStackMode.LOWEST);
mod.ClearFamily();
```

- `SetFamily(family, mode = eCatFamilyStackMode.HIGHEST)`  
  Sets `family` (string/enum) and `family_mode` for this modifier.

- `SetFamilyMode(mode)`  
  Changes the family stacking mode without altering the family key.

- `ClearFamily()`  
  Clears the family key and resets the stacking mode to `STACK_ALL`.

Family stacking is resolved within each layer, separately for real modifiers
and preview operations. For modes:

- `STACK_ALL` - all modifiers of this family apply normally.
- `HIGHEST` - only the strongest effect in the family applies.
- `LOWEST` - only the weakest effect applies.

Strength is determined by the magnitude of the effect, taking into account:

- Operation (`ADD` vs `MULTIPLY`).
- Effective stack count (including `stack_func`).
- Condition (modifiers that don't apply are excluded).

`FORCE_MIN` and `FORCE_MAX` modifiers do not participate in family comparisons;
they are applied later as a separate floor/ceiling stage before post-processing
and clamping.

---

### Source fields

```js
mod.SetSourceLabel("Bronze Wand");
mod.SetSourceId(owner);
mod.SetSourceMeta({ slot: 2, rarity: "uncommon" });
```

- `SetSourceLabel(label)` - sets the human-readable label for this modifier.
- `SetSourceId(source_id)` - sets the handle/ID representing the source.
- `SetSourceMeta(source_meta)` - sets arbitrary metadata associated with the source.

These fields are used by the `CatalystStatistic` helper functions
(`RemoveModifierBySourceLabel`, `FindModifiersBySourceMeta`, etc.) to query
and clean up modifiers based on where they came from.

---

### Modifier tags

```js
mod.AddTag("buff");
mod.AddTag("fire");

if (mod.HasTag("buff")) {
    // treat as a buff in UI
}

mod.RemoveTag("fire");
mod.ClearTags();
```

- `AddTag(tag)` - adds a tag to this modifier if not already present.
- `RemoveTag(tag)` - removes a tag if present.
- `HasTag(tag)` - `true` if the tag is present.
- `ClearTags()` - removes all tags.

Tags are free-form and for your own logic; Catalyst itself doesn't interpret
them, but the stat's `RemoveModifiersByTag` helper makes tag-based cleanup easy.

---

### Destroying a modifier

```js
mod.Destroy(true);
mod.Destroy(false);
```

- `Destroy(remove_from_stat = true)`  
  Cleans up the modifier:

  - Removes it from the global `CatalystModifierTracker` if present.
  - If `remove_from_stat` is `true` and `applied_stat` is a
    `CatalystStatistic`, removes it from that stat's `modifiers` array and
    marks the stat as altered.
  - If `remove_from_stat` is `false`, the owning stat is left alone (useful
    when the stat is already in the middle of its own cleanup).

---

## `CatalystModifierTracker` & Countdown

`CatalystModifierTracker` tracks timed modifiers (those with `duration > 0`) and
decrements their durations each tick.

### Global tracker & helper

Catalyst uses a single global tracker by default:

- `#macro CATALYST_COUNTDOWN global.__catalyst_modifier_tracker`
- `global.__catalyst_modifier_tracker` - created at load time.
- `function CatalystModCountdown()` - safe helper for driving the countdown.

Typical usage:

```js
// Global or controller Step event
CatalystModCountdown();
```

The helper function:

```js
function CatalystModCountdown() {
    if (variable_global_exists("__catalyst_modifier_tracker")
        && is_instanceof(CATALYST_COUNTDOWN, CatalystModifierTracker)) {
        CATALYST_COUNTDOWN.Countdown();
    }
}
```

In most games you don't need to construct your own tracker; the global one is
sufficient.

---

### `CatalystModifierTracker` structure

```js
tracker = new CatalystModifierTracker();
```

Fields:

- `modifiers` - array of `CatalystModifier` instances being tracked.

Methods:

```js
tracker.AddModifier(mod);
tracker.RemoveModifierById(mod);
tracker.RemoveModifierByPos(index);
tracker.DetachModifier(mod);
tracker.Countdown();
tracker.DebugDump();
```

- `AddModifier(mod)`  
  Registers a modifier with this tracker so its duration will be decremented.

- `RemoveModifierById(mod)`  
  Removes the first matching instance of the given modifier from the tracker.
  Returns `true` if a modifier was removed.

- `RemoveModifierByPos(index)`  
  Removes the modifier at the given index from the tracker array.

- `DetachModifier(mod)`  
  Removes the given modifier from the tracker **without** touching its owning
  stat and clears its `duration_applied` flag. Returns `true` if a modifier
  was removed.

- `Countdown()`  
  Decrements `duration` for each tracked modifier and removes any whose
  duration reaches 0, also removing them from their owning stats.

- `DebugDump()`  
  Writes a summary of all tracked modifiers to the debug output.

---

When a `CatalystModifier` is created with `duration > 0` or has `SetDuration`
called with a positive value, it automatically calls `ApplyDuration`, which
registers it with the global tracker. Driving `CatalystModCountdown()` once per
tick keeps all timed modifiers in sync with your game loop.
