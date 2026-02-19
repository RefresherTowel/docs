---
layout: default
title: Scripting Reference
parent: Catalyst
nav_order: 3
---


<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

## Catalyst Scripting Reference

Callback notes:
- Bind explicit scope with `method(self, function(...) {})` for instance scope.
- If you need access to more than one scope, bind a struct that contains references to all the different scopes you might want with `method(scope_struct, function(...) {})` (for instance, you might want to save the values from local variables alongside a reference to the owner, or want to perform actions on another stat plus the owner).

---

## Enums

### `eCatMathOps`

- `ADD`
  - Adds `value * stacks` to the running value.
- `MULTIPLY`
  - Multiplies the running value by `power(1 + value, stacks)`.
  - Values less than or equal to `-1` are clamped to `-0.999999` before applying.
- `FORCE_MIN`
  - Applied after all ADD and MULTIPLY layers.
  - If the current value is less than the modifier value, the value is raised to the modifier value.
  - Stacks do not scale FORCE_MIN thresholds; raw `value` is used.
  - Excluded from family comparisons.
- `FORCE_MAX`
  - Applied after all ADD, MULTIPLY, and FORCE_MIN passes.
  - If the current value is greater than the modifier value, the value is lowered to the modifier value.
  - Excluded from family comparisons.

### `eCatStatLayer`

Layers control when modifiers apply during evaluation. Catalyst processes layers in this order:

- `BASE_BONUS`
- `EQUIPMENT`
- `AUGMENTS`
- `TEMP`
- `GLOBAL`

### `eCatFamilyStackMode`

- `STACK_ALL`
  - All modifiers in the family apply.
- `HIGHEST`
  - Only the strongest modifier in the family applies (per layer, per family_mode).
- `LOWEST`
  - Only the weakest modifier in the family applies (per layer, per family_mode).

---

## Macros and globals

### `CATALYST_COUNTDOWN`

Macro alias for the global tracker instance.

- Definition: `#macro CATALYST_COUNTDOWN global.__catalyst_modifier_tracker`
- Used by `CatalystModifier.ApplyDuration()` and `CatalystModCountdown(_step_size)`.

### `global.__catalyst_modifier_tracker`

Default global tracker instance.

- Created at load time in `scr_catalyst_macro`.
- Recreated on demand if missing when a timed modifier is applied.
- You can replace it with your own `CatalystModifierTracker`, but the macro will still point at this global.

---

## Constructors

### `CatalystStatistic(_value, _min_value, _max_value)`

Creates a numeric stat container with modifiers, clamping, rounding, and callbacks.

**Arguments**
- `_value` `Real` Initial base value.
- `_min_value` `Real` Optional minimum clamp value (defaults to `-infinity`).
- `_max_value` `Real` Optional maximum clamp value (defaults to `infinity`).

**Returns**: `Struct.CatalystStatistic`

**Core fields**
- `base_value` `Real` Base (pre modifier) value.
- `starting_value` `Real` Base value at construction time.
- `current_value` `Real` Cached canonical value from the last `GetValue()` call without context.
- `base_func` `Function,Noone` Optional base override function `fn(stat, context) -> Real`.
- `min_value` `Real` Minimum clamp value.
- `max_value` `Real` Maximum clamp value.
- `clamped` `Bool` Whether clamping is enabled (default `false`).
- `rounded` `Bool` Whether rounding is enabled (default `true`).
- `round_step` `Real` Rounding step (default `1`).
- `modifiers` `Array<Struct.CatalystModifier>` Attached modifiers.
- `altered` `Bool` Whether the cached value needs recomputing (default `true`).
- `name` `String` Human readable label (default empty string).
- `on_change_callbacks` `Array<Struct>` Entries are `{ ident, fn }`.
- `on_change_next_id` `Real` Internal id counter for callbacks.
- `post_process` `Function,Noone` Optional post process `fn(stat, raw_value, context) -> Real`.
- `tags` `Array<String>` Stat tags.

**Evaluation pipeline**
- Start from `base_value` or `base_func(stat, context)` when `base_func` is callable.
- Stage 1: Apply ADD and MULTIPLY modifiers by layer order.
- Stage 2: Apply FORCE_MIN modifiers (all layers).
- Stage 3: Apply FORCE_MIN extra ops (all layers).
- Stage 4: Apply FORCE_MAX modifiers (all layers).
- Stage 5: Apply FORCE_MAX extra ops (all layers).
- Stage 6: Apply `post_process` if callable.
- Stage 7: Apply clamping and rounding if enabled.

**Evaluation rules**
- Condition callbacks run only when callable. If `context` is `undefined`, the condition is called as `fn(stat)`; otherwise it is called as `fn(stat, context)`.
- Stacks are computed as follows:
  - Start from `stacks` (default `1` when missing in extra ops).
  - If `stack_func` is callable and a context is provided, stacks become `stack_func(stat, context)`.
  - If `stack_func` is callable and no context is provided, stacks become `0`.
  - If `max_stacks` is defined, stacks are clamped to `[0, max_stacks]`. If it is missing, stacks are only clamped to `>= 0`.
- MULTIPLY values less than or equal to `-1` are clamped to `-0.999999` before applying.
- FORCE_MIN and FORCE_MAX use raw `value` and do not scale by stacks.
- Family stacking applies only when `family` is set and `family_mode` is `HIGHEST` or `LOWEST`.
  - Family comparisons are per layer and include both real modifiers and preview ops.
  - The strength comparison uses `abs(value * stacks)` for ADD and `abs(power(1 + value, stacks) - 1)` for MULTIPLY.
  - `FORCE_MIN` and `FORCE_MAX` are excluded from family comparisons.

**Public methods**

- #### `StaticSetup()`
  - **Arguments:** None.
  - **Returns:** `Undefined`
  - **Additional details:**
    - Reapplies the `CatalystModifier` static methods to all current modifiers.
    - Call this after loading serialized stats and modifiers from disk.

- #### `AddModifier(_mod)`
  - **Arguments:**
    - `_mod` `Struct.CatalystModifier` Modifier to attach.
  - **Returns:** `Struct.CatalystStatistic`
  - **Additional details:**
    - If the modifier is already attached to a different stat, the call is ignored and `EchoDebugWarn` logs a warning.
    - If the modifier is already attached to this stat, the call is a no op.
    - Sets `_mod.applied_stat = self` and marks the stat as altered.

- #### `AddOnChangeFunction(fn1, fn2, ...)`
  - **Arguments:**
    - `fn*` `Function` One or more callback functions. Each is called as `fn(stat, old_value, new_value)`.
  - **Returns:** `Array<Real>` Array of callback ids, one per function added.
  - **Additional details:**
    - Callbacks fire only when `GetValue()` is called with no context and the cached value changes.
    - `undefined` arguments are skipped, but non-callable values are stored as-is and will error when fired.
    - Use `method(self, function(...) {})` if you need instance scope.

- #### `RemoveOnChangeFunction(_id)`
  - **Arguments:**
    - `_id` `Real` Callback id returned by `AddOnChangeFunction`.
  - **Returns:** `Bool`

- #### `RemoveModifierById(_mod_id)`
  - **Arguments:**
    - `_mod_id` `Struct.CatalystModifier` Modifier instance to remove.
  - **Returns:** `Bool`
  - **Additional details:**
    - Destroys the modifier via `Destroy(false)` and removes it from the stat.

- #### `RemoveAllModifiers()`
  - **Arguments:** None.
  - **Returns:** `Struct.CatalystStatistic`
  - **Additional details:**
    - Calls `Destroy(false)` on each modifier, then clears the modifiers array.

- #### `RemoveModifierBySourceLabel(_source_label)`
  - **Arguments:**
    - `_source_label` `String` Source label to match.
  - **Returns:** `Real` Number of modifiers removed.

- #### `RemoveModifierBySourceId(_source_id)`
  - **Arguments:**
    - `_source_id` `ID.Instance|Struct` Source id to match.
  - **Returns:** `Real` Number of modifiers removed.

- #### `RemoveModifierBySourceMeta(_source_meta_func)`
  - **Arguments:**
    - `_source_meta_func` `Function` Predicate called as `fn(source_meta) -> Bool`.
  - **Returns:** `Real` Number of modifiers removed.
  - **Additional details:**
    - The predicate is called for every modifier.
    - The function is not validated. It must be callable.

- #### `RemoveModifierByPosition(_pos)`
  - **Arguments:**
    - `_pos` `Real` Index in the modifiers array.
  - **Returns:** `Bool` True if an entry existed and was removed.

- #### `RemoveModifiersByTag(_tag)`
  - **Arguments:**
    - `_tag` `String` Tag string to remove.
  - **Returns:** `Real` Number of modifiers removed.

- #### `FindModifiersBySourceId(_source_id)`
  - **Arguments:**
    - `_source_id` `ID.Instance|Struct`
  - **Returns:** `Array<Struct.CatalystModifier>`

- #### `FindModifiersBySourceLabel(_source_label)`
  - **Arguments:**
    - `_source_label` `String`
  - **Returns:** `Array<Struct.CatalystModifier>`

- #### `FindModifiersBySourceMeta(_predicate_func)`
  - **Arguments:**
    - `_predicate_func` `Function` Predicate called as `fn(source_meta) -> Bool`.
  - **Returns:** `Array<Struct.CatalystModifier>`
  - **Additional details:**
    - The function is not validated. It must be callable.

- #### `FindModifiersById(_id)`
  - **Arguments:**
    - `_id` `Struct.CatalystModifier`
  - **Returns:** `Array<Struct.CatalystModifier>`

- #### `HasModifierFromSourceId(_source_id)`
  - **Arguments:**
    - `_source_id` `ID.Instance|Struct`
  - **Returns:** `Bool`

- #### `HasModifierFromSourceLabel(_source_label)`
  - **Arguments:**
    - `_source_label` `String`
  - **Returns:** `Bool`

- #### `HasModifierFromSourceMeta(_predicate_func)`
  - **Arguments:**
    - `_predicate_func` `Function` Predicate called as `fn(source_meta) -> Bool`.
  - **Returns:** `Bool`
  - **Additional details:**
    - The function is not validated. It must be callable.

- #### `HasModifier(_mod)`
  - **Arguments:**
    - `_mod` `Struct.CatalystModifier` Modifier instance.
  - **Returns:** `Bool`

- #### `SetPostProcess(_fn)`
  - **Arguments:**
    - `_fn` `Function` Callback `fn(stat, value, context) -> Real`.
  - **Returns:** `Struct.CatalystStatistic`
  - **Additional details:**
    - Logs a debug message and ignores the call if `_fn` is not callable.

- #### `ClearPostProcess()`
  - **Arguments:** None.
  - **Returns:** `Struct.CatalystStatistic`

- #### `GetValue(_context)`
  - **Arguments:**
    - `_context` `Any` Optional evaluation context.
  - **Returns:** `Real`
  - **Additional details:**
    - If `_context` is `undefined` or omitted, returns the cached canonical value and fires on change callbacks when the value changes.
    - If `_context` is provided, evaluates a preview value without caching or callbacks.
    - Passing `undefined` explicitly is treated the same as omitting the argument.

- #### `GetValuePreview(_context)`
  - **Arguments:**
    - `_context` `Any` Optional evaluation context.
  - **Returns:** `Real`
  - **Additional details:**
    - Always evaluates without caching or callbacks.

- #### `PreviewChange(_mod_value, _mod_op, _layer, _stacks, _max_stacks, _condition, _stack_func, _context, _family, _family_mode)`
  - **Arguments:**
    - `_mod_value` `Real` Modifier value to apply.
    - `_mod_op` `eCatMathOps` Math operation.
    - `_layer` `eCatStatLayer` Optional layer (defaults to `AUGMENTS`).
    - `_stacks` `Real` Optional stacks (defaults to `1`).
    - `_max_stacks` `Real` Optional max stacks (defaults to `_stacks` when negative).
    - `_condition` `Function` Optional condition `fn(stat, context) -> Bool`.
    - `_stack_func` `Function` Optional stack function `fn(stat, context) -> Real`.
    - `_context` `Any` Optional evaluation context.
    - `_family` `Any` Optional family key.
    - `_family_mode` `eCatFamilyStackMode` Optional family mode (defaults to `STACK_ALL`).
  - **Returns:** `Real`
  - **Additional details:**
    - Builds a temporary op struct and evaluates it without mutating the stat.

- #### `PreviewChanges(_extra_ops, _context)`
  - **Arguments:**
    - `_extra_ops` `Array<Struct>` Array of op structs with fields:
      - `value` `Real`
      - `operation` `eCatMathOps`
      - `layer` `eCatStatLayer` Optional, defaults to `AUGMENTS`.
      - `stacks` `Real` Optional, defaults to `1`.
      - `max_stacks` `Real` Optional, when omitted no max clamp is applied.
      - `condition` `Function` Optional, `fn(stat, context) -> Bool`.
      - `stack_func` `Function` Optional, `fn(stat, context) -> Real`.
      - `family` `Any` Optional family key.
      - `family_mode` `eCatFamilyStackMode` Optional, defaults to `STACK_ALL`.
    - `_context` `Any` Optional evaluation context.
  - **Returns:** `Real`
  - **Additional details:**
    - If `_extra_ops` is `undefined`, it is treated as an empty array.

- #### `SetClamped(_bool)`
  - **Arguments:**
    - `_bool` `Bool` Optional, defaults to `true`.
  - **Returns:** `Struct.CatalystStatistic`
  - **Additional details:**
    - Use `SetClamped(false)` to disable clamping.

- #### `SetRounding(_enabled, _step)`
  - **Arguments:**
    - `_enabled` `Bool` Whether rounding is enabled.
    - `_step` `Real` Optional step (defaults to `1`).
  - **Returns:** `Struct.CatalystStatistic`
  - **Additional details:**
    - If `round_step <= 0`, the evaluation step uses `1` to avoid division by zero.

- #### `SetName(_name)`
  - **Arguments:**
    - `_name` `String` Name to assign.
  - **Returns:** `Struct.CatalystStatistic`

- #### `SetBaseValue(_amount)`
  - **Arguments:**
    - `_amount` `Real` New base value.
  - **Returns:** `Struct.CatalystStatistic`

- #### `SetBaseFunc(_fn)`
  - **Arguments:**
    - `_fn` `Function` Callback `fn(stat, context) -> Real`.
  - **Returns:** `Struct.CatalystStatistic`
  - **Additional details:**
    - Logs a debug message and ignores the call if `_fn` is not callable.

- #### `ClearBaseFunc()`
  - **Arguments:** None.
  - **Returns:** `Struct.CatalystStatistic`

- #### `SetMaxValue(_amount)`
  - **Arguments:**
    - `_amount` `Real` New max value.
  - **Returns:** `Struct.CatalystStatistic`

- #### `SetMinValue(_amount)`
  - **Arguments:**
    - `_amount` `Real` New min value.
  - **Returns:** `Struct.CatalystStatistic`

- #### `ChangeBaseValue(_amount)`
  - **Arguments:**
    - `_amount` `Real` Amount to add.
  - **Returns:** `Struct.CatalystStatistic`
  - **Additional details:**
    - Applies clamping and rounding to `base_value` if enabled.

- #### `ChangeMaxValue(_amount)`
  - **Arguments:**
    - `_amount` `Real` Amount to add.
  - **Returns:** `Struct.CatalystStatistic`

- #### `ChangeMinValue(_amount)`
  - **Arguments:**
    - `_amount` `Real` Amount to add.
  - **Returns:** `Struct.CatalystStatistic`

- #### `ResetToStarting()`
  - **Arguments:** None.
  - **Returns:** `Struct.CatalystStatistic`

- #### `ResetAll()`
  - **Arguments:** None.
  - **Returns:** `Struct.CatalystStatistic`
  - **Additional details:**
    - Resets base and cached values to `starting_value`.
    - Clears modifiers, callbacks, tags, base_func, and post_process.
    - Resets clamping and rounding to defaults.

- #### `GetStartingValue()`
  - **Arguments:** None.
  - **Returns:** `Real`

- #### `GetBaseValue()`
  - **Arguments:** None.
  - **Returns:** `Real`

- #### `GetMaxValue()`
  - **Arguments:** None.
  - **Returns:** `Real`

- #### `GetMinValue()`
  - **Arguments:** None.
  - **Returns:** `Real`

- #### `GetName()`
  - **Arguments:** None.
  - **Returns:** `String`

- #### `DebugDescribe()`
  - **Arguments:** None.
  - **Returns:** `Undefined`
  - **Additional details:**
    - Logs the stat and modifier details using `GetValuePreview()`.
    - Does not change cached values or fire callbacks.

- #### `AddTag(_tag)`
  - **Arguments:**
    - `_tag` `String`
  - **Returns:** `Struct.CatalystStatistic`

- #### `RemoveTag(_tag)`
  - **Arguments:**
    - `_tag` `String`
  - **Returns:** `Struct.CatalystStatistic`

- #### `HasTag(_tag)`
  - **Arguments:**
    - `_tag` `String`
  - **Returns:** `Bool`

- #### `ClearTags()`
  - **Arguments:** None.
  - **Returns:** `Struct.CatalystStatistic`

- #### `_EvaluateWithExtraOps(_extra_ops, _context)`
  - **Arguments:**
    - `_extra_ops` `Array<Struct>` Extra ops array, same format as `PreviewChanges`.
    - `_context` `Any` Optional evaluation context.
  - **Returns:** `Real`
  - **Additional details:**
    - Internal evaluation helper used by `GetValue` and preview methods.
    - Available as a method but usually not called directly.

---

### `CatalystModifier(_value, _math_operation, _duration, _source_label, _source_id, _source_meta)`

Creates a modifier that can be attached to a `CatalystStatistic`.

**Arguments**
- `_value` `Real` Modifier value.
- `_math_operation` `eCatMathOps` How the value applies.
- `_duration` `Real` Optional duration in your chosen countdown units (`-1` for permanent).
- `_source_label` `String` Optional human readable label.
- `_source_id` `ID.Instance|Struct` Optional source handle.
- `_source_meta` `Any` Optional metadata.

**Returns**: `Struct.CatalystModifier`

**Core fields**
- `value` `Real` Modifier value.
- `operation` `eCatMathOps` Math operation.
- `duration` `Real` Remaining duration in the same units as `Countdown(_step_size)` (`-1` for permanent).
- `duration_max` `Real` Original duration in the same units as `duration`.
- `duration_applied` `Bool` Whether the modifier is tracked.
- `stacks` `Real` Current stack count (default `1`).
- `max_stacks` `Real` Max stack count (default `infinity`).
- `layer` `eCatStatLayer` Default layer (default `TEMP`).
- `condition` `Function,Undefined` Optional condition.
- `stack_func` `Function,Undefined` Optional stack function.
- `family` `Any` Family key (default empty string).
- `family_mode` `eCatFamilyStackMode` Family stacking mode (default `STACK_ALL`).
- `tags` `Array<String>` Modifier tags.
- `source_label` `String` Source label.
- `source_id` `ID.Instance|Struct` Source handle.
- `source_meta` `Any` Metadata object.
- `applied_stat` `Struct.CatalystStatistic,Noone` Owning stat.
- `remove_from_stat` `Bool` Internal flag used during destruction.

**Duration behavior**
- A positive duration registers the modifier with the global tracker.
- A negative duration is permanent and not tracked.
- A duration of `0` is not tracked when first created. If already tracked, it will expire on the next countdown.
- Keep duration units matched with the countdown step size.
- `ApplyDuration()` is called at the end of the constructor.

**Public methods**

- #### `ApplyDuration()`
  - **Arguments:** None.
  - **Returns:** `Undefined`
  - **Additional details:**
    - Registers the modifier with `CATALYST_COUNTDOWN` if `duration > 0` and not already applied.
    - Creates the global tracker if missing.

- #### `SetDuration(_duration)`
  - **Arguments:**
    - `_duration` `Real` New duration value.
  - **Returns:** `Struct.CatalystModifier`
  - **Additional details:**
    - Updates `duration` and `duration_max`.
    - Detaches from the tracker when `_duration < 0`.
    - Reapplies tracking when `_duration >= 0` and `duration > 0`.

- #### `ResetDuration()`
  - **Arguments:** None.
  - **Returns:** `Undefined`
  - **Additional details:**
    - Calls `SetDuration(duration_max)`.

- #### `SetValue(_value)`
  - **Arguments:**
    - `_value` `Real`
  - **Returns:** `Struct.CatalystModifier`
  - **Additional details:**
    - Marks the owning stat as altered if attached.

- #### `SetMathsOp(_maths_op)`
  - **Arguments:**
    - `_maths_op` `eCatMathOps`
  - **Returns:** `Struct.CatalystModifier`
  - **Additional details:**
    - Marks the owning stat as altered if attached.

- #### `SetSourceLabel(_source_label)`
  - **Arguments:**
    - `_source_label` `String`
  - **Returns:** `Struct.CatalystModifier`

- #### `SetSourceId(_source_id)`
  - **Arguments:**
    - `_source_id` `ID.Instance|Struct`
  - **Returns:** `Struct.CatalystModifier`

- #### `SetSourceMeta(_source_meta)`
  - **Arguments:**
    - `_source_meta` `Any`
  - **Returns:** `Struct.CatalystModifier`

- #### `SetLayer(_layer)`
  - **Arguments:**
    - `_layer` `eCatStatLayer`
  - **Returns:** `Struct.CatalystModifier`
  - **Additional details:**
    - Marks the owning stat as altered if attached.

- #### `SetStacks(_stacks)`
  - **Arguments:**
    - `_stacks` `Real`
  - **Returns:** `Struct.CatalystModifier`
  - **Additional details:**
    - Clamps to `[0, max_stacks]`.
    - Marks the owning stat as altered if attached.

- #### `AddStacks(_delta)`
  - **Arguments:**
    - `_delta` `Real` Optional delta (defaults to `1`).
  - **Returns:** `Struct.CatalystModifier`

- #### `SetMaxStacks(_max)`
  - **Arguments:**
    - `_max` `Real` New max stack count.
  - **Returns:** `Struct.CatalystModifier`
  - **Additional details:**
    - Uses `max(1, _max)` so the minimum is `1`.
    - Clamps the current stack count if needed.
    - Marks the owning stat as altered if attached.

- #### `SetCondition(_fn)`
  - **Arguments:**
    - `_fn` `Function` Callback `fn(stat)` or `fn(stat, context) -> Bool`.
  - **Returns:** `Struct.CatalystModifier`
  - **Additional details:**
    - Marks the owning stat as altered if attached.

- #### `ClearCondition()`
  - **Arguments:** None.
  - **Returns:** `Struct.CatalystModifier`
  - **Additional details:**
    - Marks the owning stat as altered if attached.

- #### `SetStackFunc(_fn)`
  - **Arguments:**
    - `_fn` `Function` Callback `fn(stat, context) -> Real`.
  - **Returns:** `Struct.CatalystModifier`
  - **Additional details:**
    - When set, the effective stack count comes from this callback when a context is provided.
    - When no context is provided, the effective stack count is `0`.
    - Marks the owning stat as altered if attached.

- #### `ClearStackFunc()`
  - **Arguments:** None.
  - **Returns:** `Struct.CatalystModifier`
  - **Additional details:**
    - Marks the owning stat as altered if attached.

- #### `SetFamily(_family, _mode)`
  - **Arguments:**
    - `_family` `Any` Family key.
    - `_mode` `eCatFamilyStackMode` Optional stacking mode (defaults to `HIGHEST`).
  - **Returns:** `Struct.CatalystModifier`
  - **Additional details:**
    - Marks the owning stat as altered if attached.

- #### `SetFamilyMode(_mode)`
  - **Arguments:**
    - `_mode` `eCatFamilyStackMode`
  - **Returns:** `Struct.CatalystModifier`
  - **Additional details:**
    - Marks the owning stat as altered if attached.

- #### `ClearFamily()`
  - **Arguments:** None.
  - **Returns:** `Struct.CatalystModifier`
  - **Additional details:**
    - Clears the family key and resets the mode to `STACK_ALL`.
    - Marks the owning stat as altered if attached.

- #### `AddTag(_tag)`
  - **Arguments:**
    - `_tag` `String`
  - **Returns:** `Struct.CatalystModifier`

- #### `RemoveTag(_tag)`
  - **Arguments:**
    - `_tag` `String`
  - **Returns:** `Struct.CatalystModifier`

- #### `HasTag(_tag)`
  - **Arguments:**
    - `_tag` `String`
  - **Returns:** `Bool`

- #### `ClearTags()`
  - **Arguments:** None.
  - **Returns:** `Struct.CatalystModifier`

- #### `Destroy(_remove_from_stat)`
  - **Arguments:**
    - `_remove_from_stat` `Bool` Optional (defaults to `true`).
  - **Returns:** `Undefined`
  - **Additional details:**
    - Removes the modifier from the tracker if present.
    - When `_remove_from_stat` is `true`, also detaches it from the owning stat.
    - When `_remove_from_stat` is `false`, the stat is not updated. Use this only when the stat is already handling its own removal.
    - The modifier is deleted and should not be used after this call.
    - Do not keep long-lived raw references to temporary modifiers; query current modifiers by source/tag/id when needed.

---

### `CatalystModifierTracker()`

Creates a tracker for timed modifiers.

**Returns**: `Struct.CatalystModifierTracker`

**Fields**
- `modifiers` `Array<Struct.CatalystModifier>` Currently tracked modifiers.
- `paused` `Bool` Whether countdown is paused.
- `time_scale` `Real` Multiplier applied to countdown step sizes.

**Public methods**

- #### `AddModifier(_mod)`
  - **Arguments:**
    - `_mod` `Struct.CatalystModifier`
  - **Returns:** `Undefined`
  - **Additional details:**
    - Simply pushes the modifier into the list.

- #### `RemoveModifierById(_mod)`
  - **Arguments:**
    - `_mod` `Struct.CatalystModifier`
  - **Returns:** `Bool`
  - **Additional details:**
    - Removes the first matching instance, calls `RemoveModifierByPos`, and returns true when a modifier was removed.

- #### `RemoveModifierByPos(_pos)`
  - **Arguments:**
    - `_pos` `Real` Index in the modifiers array.
  - **Returns:** `Bool`
  - **Additional details:**
    - Deletes the modifier and removes it from the tracker.
    - If `remove_from_stat` is true and `applied_stat` is a `CatalystStatistic`, the stat reference is removed as well.

- #### `DetachModifier(_mod)`
  - **Arguments:**
    - `_mod` `Struct.CatalystModifier`
  - **Returns:** `Bool`
  - **Additional details:**
    - Removes the modifier from the tracker without touching its owning stat.
    - Sets `_mod.duration_applied = false`.

- #### `SetPaused(_paused)`
  - **Arguments:**
    - `_paused` `Bool` True pauses countdown, false resumes.
  - **Returns:** `Bool`
  - **Additional details:**
    - Sets and returns the current paused state.

- #### `IsPaused()`
  - **Arguments:** None.
  - **Returns:** `Bool`
  - **Additional details:**
    - Returns whether countdown is currently paused.

- #### `SetTimeScale(_time_scale)`
  - **Arguments:**
    - `_time_scale` `Real` Countdown multiplier (minimum `0`).
  - **Returns:** `Real`
  - **Additional details:**
    - Non-real values are ignored.
    - The stored time scale is clamped to `>= 0`.

- #### `GetTimeScale()`
  - **Arguments:** None.
  - **Returns:** `Real`
  - **Additional details:**
    - Returns the current countdown time scale.

- #### `Countdown(_step_size)`
  - **Arguments:**
    - `_step_size` `Real` Optional decrement amount. Default `1`.
  - **Returns:** `Undefined`
  - **Additional details:**
    - Returns early when paused.
    - Ignores the call when `_step_size` is not a real number or is less than or equal to 0.
    - Applies `time_scale` to `_step_size` before decrementing durations.
    - Returns early when effective step size is less than or equal to `0`.
    - Decrements each tracked modifier duration by the effective step size.
    - Removes and deletes modifiers whose duration reaches 0 or lower.

- #### `DebugDump()`
  - **Arguments:** None.
  - **Returns:** `Undefined`
  - **Additional details:**
    - Writes a summary of all tracked modifiers to the debug output.

---

### `EchoChamberThemeCatalyst()`

Creates a Catalyst themed `EchoChamberTheme` variant with a neon reactor palette.

**Returns**: `Struct.EchoChamberThemeCatalyst`

**Additional details**
- Extends `EchoChamberTheme` and overrides colors, panel styles, button styles, toggles, dropdowns, and text inputs.
- Requires Echo Chamber to be present in your project.

---

## Functions

### `CatalystModCountdown(_step_size)`

Helper for driving the global modifier tracker.

**Arguments**
- `_step_size` `Real` Optional decrement amount. Default `1`.

**Returns**: `Undefined`

**Additional details**
- Calls `global.__catalyst_modifier_tracker.Countdown(_step_size)` when the tracker exists and is a `CatalystModifierTracker`.
- Safe to call once per Step, per tick, or with fractional step sizes from your own delta-time system.
- Tracker pause and time scale settings are respected.
