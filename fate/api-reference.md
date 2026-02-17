---
layout: default
title: Scripting Reference
parent: Fate
nav_order: 6
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# API Reference

This page documents Fate's public API surface in this repository.

Callback note:
- When passing function refs for policy callbacks, it's usually a good idea to bind scope with `method(scope, fn)`, so that you have direct control over which scope the function runs in.

---

## Result wrapper contract

Most helper functions return one of Fate's return contract constructors.
Each return contract includes:

```js
{ ok, code, data, kind }
```

- `ok` `Bool`: operation success.
- `code` `String`: stable outcome code.
- `data` `Struct|Any`: payload for success/failure context.
- `kind` `String`: return contract family.

These contracts are separated into families, sometimes called "pools". Use `GetReturnKind()` when branching behavior by contract family if you need to.

You can still read `data` directly, and each family also exposes helper methods tailored to its payload shape.

For beginners, the safest default flow is to check `IsOk()` to see if the result passed or failed, inspect `code` on failure, and then use helper methods in lieu of reading raw `data`.

Common `kind` values:

- `roll`
- `file`
- `registry_mutation`
- `registry_keys`
- `prune`
- `capture`
- `restore`
- `pipeline`
- `generic`

---

## Enums

### `FateStrictness`

- `FateStrictness.SILENT`
- `FateStrictness.DEBUG`
- `FateStrictness.ERROR`

---

## Constructors

### `new FateEntry()`

Base entry with weight, guaranteed, uniqueness, and hook methods.

**Returns**: `Struct.FateEntry`

---

### `new FateValueEntry(_value)`

Entry wrapper for plain values.

**Arguments**
- `_value` `Any`

**Returns**: `Struct.FateValueEntry`

---

### `new FateTableEntry(_table, _count = 1)`

Entry wrapper for nested tables.

**Arguments**
- `_table` `Struct.FateTable`
- `_count` `Real`

**Returns**: `Struct.FateTableEntry`

---

### `new FateCreatorEntry(_ctor, _args = undefined)`

Entry that creates a new payload value when selected. You can supply either an object type or a constructor. If you provide an object type, an instance is created at `x = 0`, `y = 0`, `depth = 0`, so position and depth or layer should be handled after instantiation.

**Arguments**
- `_ctor` `Any` (callable constructor or object type)
- `_args` `Any` (must be a `Struct` if `_ctor` is an object index)

**Returns**: `Struct.FateCreatorEntry`

**Additional Details**: When Fate instantiates a creator entry, it will follow one of two paths. If the `_ctor` is an object index, it will instantiate an instance of that object (with the above caveats about position and depth), while also injecting the `_args` into the instance like this: `instance_create_depth(0, 0, 0, _ctor, _args)`. This means that you **must** provide a struct for the `_args` argument, as that is what GM will expect. You'll have access to the variables in the `_args` struct you provide during the Create Event of that object. If the `_ctor` is a constructor, then the constructor will be provided with args during it's construction: `new _ctor(_args)`. As a final note, if you provide a constructor, remember to NOT include the brackets `()` with the constructor name, you should just provide the constructor plainly: `new FateCreatorEntry(ConstructorName, _args_struct)`. It's a common error to include the brackets, so do **not** do this: `new FateCreateEntry(ConstructorName(), _args_struct)`.

---

### `new FateTable(_entries = [])`

Weighted selection table.

**Arguments**
- `_entries` `Array<Struct.FateEntry>`

**Returns**: `Struct.FateTable`

---

### `new FateRng(_seed)`

Deterministic RNG with `NextUnit()` values in `[0, 1)`.

**Arguments**
- `_seed` `Real`

**Returns**: `Struct.FateRng`

---

## `FateEntry` methods

All setters return `Struct.FateEntry` for chaining.

- #### `SetEnabled(_enabled = true)`
	- **Arguments:** `_enabled` `Bool`
	- **Returns:** `Struct.FateEntry`

- #### `GetEnabled()`
	- **Arguments:** None.
	- **Returns:** `Bool`

- #### `SetWeight(_weight)`
	- **Arguments:** `_weight` `Real`
	- **Returns:** `Struct.FateEntry`

- #### `GetWeight()`
	- **Arguments:** None.
	- **Returns:** `Real`

- #### `SetGuaranteed(_guaranteed = true)`
	- **Arguments:** `_guaranteed` `Bool`
	- **Returns:** `Struct.FateEntry`

- #### `GetGuaranteed()`
	- **Arguments:** None.
	- **Returns:** `Bool`

- #### `SetGuaranteedPriority(_priority = 0)`
	- **Arguments:** `_priority` `Real`
	- **Returns:** `Struct.FateEntry`

- #### `GetGuaranteedPriority()`
	- **Arguments:** None.
	- **Returns:** `Real`

- #### `SetUnique(_unique = true)`
	- **Arguments:** `_unique` `Bool`
	- **Returns:** `Struct.FateEntry`

- #### `GetUnique()`
	- **Arguments:** None.
	- **Returns:** `Bool`

- #### `SetUniqueKey(_key = undefined)`
	- **Arguments:** `_key` `Any`
	- **Returns:** `Struct.FateEntry`

- #### `GetUniqueKey()`
	- **Arguments:** None.
	- **Returns:** `Any`

- #### `ResolveForRoll(_context)`
	- **Arguments:** `_context` `Any`
	- **Returns:** `Struct`

- #### `OnSelected(_context, _event)`
	- **Arguments:** `_context` `Any`, `_event` `Struct`
	- **Returns:** `Void`

- #### `OnRollFinished(_context, _summary)`
	- **Arguments:** `_context` `Any`, `_summary` `Struct`
	- **Returns:** `Void`

---

## `FateValueEntry` methods

- #### `SetValue(_value)`
	- **Arguments:** `_value` `Any`
	- **Returns:** `Struct.FateValueEntry`

- #### `GetValue()`
	- **Arguments:** None.
	- **Returns:** `Any`

---

## `FateTableEntry` methods

- #### `SetTable(_table)`
	- **Arguments:** `_table` `Struct.FateTable`
	- **Returns:** `Struct.FateTableEntry`

- #### `GetTable()`
	- **Arguments:** None.
	- **Returns:** `Struct.FateTable`

- #### `SetCount(_count = 1)`
	- **Arguments:** `_count` `Real`
	- **Returns:** `Struct.FateTableEntry`

- #### `GetCount()`
	- **Arguments:** None.
	- **Returns:** `Real`

- #### `ResolveForRoll(_context)`
	- **Arguments:** `_context` `Any`
	- **Returns:** `Struct`

---

## `FateCreatorEntry` methods

- #### `SetConstructor(_ctor)`
	- **Arguments:** `_ctor` `Any`
	- **Returns:** `Struct.FateCreatorEntry`

- #### `GetConstructor()`
	- **Arguments:** None.
	- **Returns:** `Any`

- #### `SetArgs(_args = undefined)`
	- **Arguments:** `_args` `Any`
	- **Returns:** `Struct.FateCreatorEntry`

- #### `GetArgs()`
	- **Arguments:** None.
	- **Returns:** `Any`

- #### `ResolveForRoll(_context)`
	- **Arguments:** `_context` `Any`
	- **Returns:** `Struct`

---

## `FateRng` methods

- #### `NextUnit()`
	- **Arguments:** None.
	- **Returns:** `Real`

- #### `GetState()`
	- **Arguments:** None.
	- **Returns:** `Struct` (`{ seed }`)

- #### `SetState(_state)`
	- **Arguments:** `_state` `Struct`
	- **Returns:** `Struct.FateRng`

---

## `FateTable` methods

All mutating methods return `Struct.FateTable` for chaining unless noted.

### Configuration

- #### `SetStrictness(_mode)`
	- **Arguments:** `_mode` `FateStrictness`
	- **Returns:** `Struct.FateTable`

- #### `GetStrictness()`
	- **Arguments:** None.
	- **Returns:** `Real`

- #### `SetConstructEntries(_construct = true)`
	- **Arguments:** `_construct` `Bool`
	- **Returns:** `Struct.FateTable`
	- **Additional Notes:** When true, `FateCreatorEntry` selections instantiate and append their payload outputs to roll results. When false, creator entries are returned as entry structs without instantiation.

- #### `GetConstructEntries()`
	- **Arguments:** None.
	- **Returns:** `Bool`

- #### `GetTableId()`
	- **Arguments:** None.
	- **Returns:** `Real`

- #### `GetLastRollDiagnostics()`
	- **Arguments:** None.
	- **Returns:** `Struct`

### Entry management

- #### `AddEntry(_entry)`
	- **Arguments:** `_entry` `Struct.FateEntry`
	- **Returns:** `Struct.FateTable`
	- **Notes:** direct `FateTable` entries are rejected; wrap nested tables with `FateTableEntry`.

- #### `ClearEntries()`
	- **Arguments:** None.
	- **Returns:** `Struct.FateTable`

- #### `GetEntries()`
	- **Arguments:** None.
	- **Returns:** `Array<Struct.FateEntry>` (copy)

### Policy management

- #### `AddPolicy(_policy)`
	- **Arguments:** `_policy` `Struct`
	- **Returns:** `Struct.FateTable`

- #### `ClearPolicies()`
	- **Arguments:** None.
	- **Returns:** `Struct.FateTable`

- #### `GetPolicies()`
	- **Arguments:** None.
	- **Returns:** `Array<Struct>` (copy)

### Beginner policy helpers

- #### `EnablePity(_target_entries, _hard_at = 90, _soft_start = 75, _soft_step = 0.06, _scope_context_key = undefined)`
	- **Arguments:**
		- `_target_entries` `Struct.FateEntry|Array<Struct.FateEntry>`
		- `_hard_at` `Real`
		- `_soft_start` `Real`
		- `_soft_step` `Real`
		- `_scope_context_key` `String|Undefined`
	- **Returns:** `Struct.FateTable`
	- **Additional Notes:** Pity raises consistency for rare targets by increasing effective chance after repeated misses. Use scope keys when pity should be tracked separately per profile or account.

- #### `EnableRateUp(_featured_entries, _rate_up_mult = 1.5, _hard_at = undefined, _reset_on_any_hit = false, _scope_context_key = undefined)`
	- **Arguments:**
		- `_featured_entries` `Struct.FateEntry|Array<Struct.FateEntry>`
		- `_rate_up_mult` `Real`
		- `_hard_at` `Real|Undefined`
		- `_reset_on_any_hit` `Bool`
		- `_scope_context_key` `String|Undefined`
	- **Returns:** `Struct.FateTable`
	- **Additional Notes:** Rate-up is useful for featured banners where a subset of targets should appear more often. A hard threshold can be used when featured fairness must be guaranteed.

- #### `EnableDuplicateProtection(_window = 1, _mode = "penalize", _penalty_mult = 0.25, _key_mode = "entry_id", _intra_roll_unique = true)`
	- **Arguments:**
		- `_window` `Real`
		- `_mode` `String` (`"penalize" | "exclude"`)
		- `_penalty_mult` `Real`
		- `_key_mode` `String` (`"entry_id" | "unique_key"`)
		- `_intra_roll_unique` `Bool`
	- **Returns:** `Struct.FateTable`
	- **Additional Notes:** Duplicate protection helps avoid repeat frustration in short roll windows. Use `unique_key` mode when different entries should share one duplicate bucket.

- #### `EnableBatchGuarantee(_target_entries, _min_count = 1, _roll_count_at_least = 10, _soft_mult = 1, _allow_bypass_filters = true)`
	- **Arguments:**
		- `_target_entries` `Struct.FateEntry|Array<Struct.FateEntry>`
		- `_min_count` `Real`
		- `_roll_count_at_least` `Real`
		- `_soft_mult` `Real`
		- `_allow_bypass_filters` `Bool`
	- **Returns:** `Struct.FateTable`
	- **Additional Notes:** Batch guarantee enforces minimum target hits across a multi-roll size. This is useful for ten-pull style promises and other package fairness rules.

- #### `EnableTenPullGuarantee(_target_entries, _min_count = 1, _soft_mult = 1, _allow_bypass_filters = true, _roll_count = 10)`
	- **Arguments:**
		- `_target_entries` `Struct.FateEntry|Array<Struct.FateEntry>`
		- `_min_count` `Real`
		- `_soft_mult` `Real`
		- `_allow_bypass_filters` `Bool`
		- `_roll_count` `Real`
	- **Returns:** `Struct.FateTable`
	- **Additional Notes:** This is a convenience form of batch guarantee tuned for ten-pull workflows. Use it when your design language is built around fixed multi-pull packs.

- #### `EnableStandardGachaRules(_five_star_entries, _featured_entries = undefined, _pity_hard_at = 90, _pity_soft_start = 75, _rate_up_mult = 1.5)`
	- **Arguments:**
		- `_five_star_entries` `Struct.FateEntry|Array<Struct.FateEntry>`
		- `_featured_entries` `Struct.FateEntry|Array<Struct.FateEntry>|Undefined`
		- `_pity_hard_at` `Real`
		- `_pity_soft_start` `Real`
		- `_rate_up_mult` `Real`
	- **Returns:** `Struct.FateTable`
	- **Additional Notes:** This helper installs a practical baseline policy set quickly. It is a good starting point before tuning individual policy constructors.

### Roll/query surface

- #### `Roll(_count = 1, _context = undefined, _rng = undefined)`
	- **Arguments:** `_count` `Real`, `_context` `Any`, `_rng` `Any`
	- **Returns:** `Array<Struct.FateEntry>`
	- **Additional Notes:** This is the core selection API and returns entries, not plain values. Use `FateRollValues` if beginner code should work directly with values.

- #### `RollDetailed(_count = 1, _context = undefined, _rng = undefined)`
	- **Arguments:** `_count` `Real`, `_context` `Any`, `_rng` `Any`
	- **Returns:** `Struct` (`{ results, roll, diagnostics, selected_events, table_summaries }`)
	- **Additional Notes:** This is intended for debugging and QA. It includes telemetry that is useful for understanding policy interactions and nested selection flow.

- #### `Preview(_count = 1, _context = undefined)`
	- **Arguments:** `_count` `Real`, `_context` `Any`
	- **Returns:** `Struct`
	- **Additional Notes:** Preview evaluates likely outcomes without committing selection side effects. It is useful for UI hints and probability previews.

- #### `GetEntryProbability(_entry, _context = undefined)`
	- **Arguments:** `_entry` `Struct.FateEntry`, `_context` `Any`
	- **Returns:** `Real`
	- **Additional Notes:** This returns chance for one specific entry under the current resolved rules. Use this for balancing tools rather than frame-by-frame gameplay logic.

- #### `GetValueProbability(_value, _context = undefined)`
	- **Arguments:** `_value` `Any`, `_context` `Any`
	- **Returns:** `Real`
	- **Additional Notes:** This is value-oriented probability lookup. It is often easier than entry-based checks when your gameplay logic is keyed by item IDs or strings.

### State and validation

- #### `GetState()`
	- **Arguments:** None.
	- **Returns:** `Struct`
	- **Additional Notes:** State snapshots include policy state that affects future rolls. Capture this before save operations when continuity matters.

- #### `SetState(_state)`
	- **Arguments:** `_state` `Struct`
	- **Returns:** `Struct.FateTable`
	- **Additional Notes:** Apply only validated or trusted state payloads. This method is side-effectful and will alter future roll outcomes.

- #### `ValidateConfig(_opts = undefined)`
	- **Arguments:** `_opts` `Struct|Undefined`
	- **Returns:** `Struct` validation report
	- **Additional Notes:** Use this at setup boundaries to detect invalid policy wiring before runtime rolls begin.

- #### `ValidateState(_state, _opts = undefined)`
	- **Arguments:** `_state` `Struct`, `_opts` `Struct|Undefined`
	- **Returns:** `Struct` validation report
	- **Additional Notes:** Use this before restore calls when payloads come from disk, network, or external tools.

---

### Policy constructors

These are an advanced level manipulation of policies. Beginners should focus first on the `.Enable*()` methods that are attached to the `FateEntry` structs, as they will automatically construct appropriate contracts for you.

- `new FatePityPolicy(_opts = undefined)`
- `new FateDuplicateProtectionPolicy(_opts = undefined)`
- `new FateBatchGuaranteePolicy(_opts = undefined)`
- `new FateFeaturedRateUpPolicy(_opts = undefined)`

These return policy structs compatible with `table.AddPolicy(...)`.

---

### Return contract constructors

These constructors back Fate's `{ ok, code, data, kind }` return contracts. You will never need to create one of these, as Fate does that automatically, but you DO need to know how to work with them.

A lot of Fate functions will return one of these "contracts" when you call them (for example, `FateRollValues()` will return a `FateRollReturn` contract). The contract simply contains some information, like whether the action you wanted to perform succeeded, what data is associated with that action and so on. Each child has a set of specific methods to help you interact with them, as well as the base methods that are shared between all contracts (which can be seen in the base parent `__FateReturn` contract below).

#### `__FateReturn(_ok, _code, _data = undefined, _kind = "generic")`

Base parent contract constructor. This is never returned plainly, but it sets up the shared data / methods that are common to all the child constructors.

**Arguments**
- `_ok` `Bool`
- `_code` `String`
- `_data` `Any`
- `_kind` `String`

**Returns**: `Struct.__FateReturn`

**Methods**
- `IsOk() -> Bool`
- `IsError() -> Bool`
- `GetCode() -> String`
- `CodeIs(_code_to_match) -> Bool`
- `GetData() -> Any`
- `GetReturnKind() -> String`

**Additional Notes**
Use this as the shared language for all Fate helper results. Child contracts include these same methods, so a single error handling pattern can work across roll, file, capture, and restore flows.

---

#### `FateRollReturn(_ok, _code, _data = undefined)`

Roll result contract (`kind = "roll"`).

**Returns**: `Struct.FateRollReturn`

**Methods**
- `GetDrops() -> Array`
- `GetDropCount() -> Real`
- `GetDrop(_index, _default = undefined) -> Any`
- `PeekFirstDrop(_default = undefined) -> Any`
- `GetFirstDrop(_default = undefined) -> Any`
- `PopFirstDrop(_default = undefined) -> Any`
- `RemoveFirstDrop(_default = undefined) -> Any`
- `GetEntries() -> Array`
- `GetNonValueCount() -> Real`

**Additional Notes**
This is the most common beginner result for loot pulling. `GetFirstDrop()` is a good default when rolling once, and `GetDrops()` is clearer when rolling many values at once.

---

#### `FateFileReturn(_ok, _code, _data = undefined)`

File operation contract (`kind = "file"`).

**Returns**: `Struct.FateFileReturn`

**Methods**
- `GetFilename() -> String`
- `HasState() -> Bool`
- `GetState(_default = undefined) -> Struct|Any`

**Additional Notes**
This contract is used for simple save and load file steps. `HasState()` is especially useful after load calls when you want to confirm that parsed state exists before applying it.

---

#### `FateRegistryMutationReturn(_ok, _code, _data = undefined)`

Registry mutation contract (`kind = "registry_mutation"`).

**Returns**: `Struct.FateRegistryMutationReturn`

**Methods**
- `GetKey() -> String`
- `WasReplaced() -> Bool`
- `WasRemoved() -> Bool`
- `WasMutated() -> Bool`

**Additional Notes**
Use this when managing tracked or registered tables by key. `WasMutated()` gives a quick yes or no answer when you do not need to separate register, replace, or unregister paths.

---

#### `FateRegistryKeysReturn(_ok, _code, _data = undefined)`

Registry keys contract (`kind = "registry_keys"`).

**Returns**: `Struct.FateRegistryKeysReturn`

**Methods**
- `GetKeys() -> Array<String>`
- `GetKeyCount() -> Real`
- `HasKey(_key) -> Bool`

**Additional Notes**
This is useful for debug menus and save tooling. `HasKey()` is usually easier to read than manual array loops in beginner scripts.

---

#### `FatePruneReturn(_ok, _code, _data = undefined)`

Prune summary contract (`kind = "prune"`).

**Returns**: `Struct.FatePruneReturn`

**Methods**
- `GetRegisteredCount() -> Real`
- `GetLiveCount() -> Real`
- `GetPrunedDeadCount() -> Real`

**Additional Notes**
This contract reports registry cleanup outcomes. A non-zero pruned count often means stale weak references were removed (as Fate tries to automatically GC unused tables).

---

#### `FateCaptureReturn(_ok, _code, _data = undefined)`

Capture contract (`kind = "capture"`).

**Returns**: `Struct.FateCaptureReturn`

**Methods**
- `HasState() -> Bool`
- `GetState(_default = undefined) -> Struct|Any`
- `GetTablesMap(_default = undefined) -> Struct|Any`
- `GetCapturedCount() -> Real`
- `GetSkippedCount() -> Real`
- `GetReport() -> Struct`

**Additional Notes**
Use this to prepare state bundles before writing files or moving state across systems. `GetReport()` is convenient when you want a summary for logs or QA output.

---

#### `FateRestoreReturn(_ok, _code, _data = undefined)`

Restore summary contract (`kind = "restore"`).

**Returns**: `Struct.FateRestoreReturn`

**Methods**
- `GetAttemptedCount() -> Real`
- `GetAppliedCount() -> Real`
- `GetInvalidCount() -> Real`
- `GetMissingCount() -> Real`
- `GetSkippedCount() -> Real`
- `HadIssues() -> Bool`
- `GetRegisteredCount() -> Real`
- `GetLiveCount() -> Real`
- `GetPrunedDeadCount() -> Real`

**Additional Notes**
This contract focuses on restore outcomes. `HadIssues()` is a fast check for partial restore scenarios before reading each counter.

---

#### `FatePipelineReturn(_ok, _code, _data = undefined)`

Pipeline contract (`kind = "pipeline"`).

**Returns**: `Struct.FatePipelineReturn`

**Methods**
- `GetFilename() -> String`
- `GetCaptureResult() -> Struct|Undefined`
- `GetSaveResult() -> Struct|Undefined`
- `GetLoadResult() -> Struct|Undefined`
- `GetRestoreResult() -> Struct|Undefined`
- `AllNestedOk() -> Bool`

**Additional Notes**
Pipeline helpers combine multiple operations in one call. `AllNestedOk()` helps beginners confirm that every nested step succeeded without unpacking each nested result manually.

---

## Top-level beginner helpers

### `FateRollValues(_table, _count = 1, _context = undefined, _rng = undefined)`

Rolls a table and returns a roll contract with value helpers (`GetDrops()`, `GetFirstDrop()`).

**Arguments**
- `_table` `Struct.FateTable`
- `_count` `Real`
- `_context` `Any`
- `_rng` `Any`

**Returns**: `Struct.FateRollReturn`

**Additional Notes**
Use this instead of `table.Roll()` when you want plain values quickly. `table.Roll()` returns entry structs, while this helper returns value-centric data and methods.

---

### `FateTrackTable(_key, _table)`

Registers a table for beginner snapshot flows.

**Arguments**
- `_key` `String`
- `_table` `Struct.FateTable`

**Returns**: `Struct.FateRegistryMutationReturn`

**Additional Notes**
Call this once for each table you want included in beginner snapshot save and load calls. Reusing stable keys keeps restore behavior predictable.

---

### `FateUntrackTable(_key)`

Removes a tracked table key.

**Arguments**
- `_key` `String`

**Returns**: `Struct.FateRegistryMutationReturn`

**Additional Notes**
Use this when a table should no longer be part of snapshot persistence. This is useful for temporary systems that should not survive between sessions.

---

### `FateListTrackedTables()`

Lists currently tracked keys (`GetKeys()` / `data.keys`).

**Arguments**: None.

**Returns**: `Struct.FateRegistryKeysReturn`

**Additional Notes**
This helper is useful for debug overlays and sanity checks. It lets you verify tracking setup before calling save or load helpers.

---

### `FateSaveSnapshotFile(_filename)`

Captures tracked table states and writes to file.

**Arguments**
- `_filename` `String`

**Returns**: `Struct.FatePipelineReturn`

**Additional Notes**
This helper captures all tracked table state and writes it in one step. The returned pipeline contract also includes nested capture and save results for troubleshooting.

---

### `FateLoadSnapshotFile(_filename)`

Loads snapshot file and restores tracked tables.

**Arguments**
- `_filename` `String`

**Returns**: `Struct.FatePipelineReturn`

**Additional Notes**
This helper loads a snapshot file and restores tracked tables in one call. Check both `ok` and `AllNestedOk()` when you want strict confirmation of every nested stage.

---

## Top-level advanced state helpers

### `FateAdvancedSaveStateFile(_filename, _state)`

Saves a state struct to JSON file.

**Arguments**
- `_filename` `String`
- `_state` `Struct`

**Returns**: `Struct.FateFileReturn`

**Additional Notes**
This is a generic JSON write helper for Fate state structs. It does not choose which tables to capture, so pair it with capture helpers when needed.

---

### `FateAdvancedLoadStateFile(_filename)`

Loads a state struct from JSON file.

**Arguments**
- `_filename` `String`

**Returns**: `Struct.FateFileReturn`

**Additional Notes**
This is a generic JSON load helper. It parses file content into a state struct but does not apply that state to tables by itself.

---

### `FateAdvancedRegisterTableState(_key, _table, _opts = undefined)`

Registers a table key using weak references for registry-backed snapshots.

**Arguments**
- `_key` `String`
- `_table` `Struct.FateTable`
- `_opts` `Struct|Undefined` (supports `allow_replace`)

**Returns**: `Struct.FateRegistryMutationReturn`

**Additional Notes**
This is the advanced registry equivalent of `FateTrackTable`. `allow_replace` is helpful for hot-swapping table instances under a fixed key.

---

### `FateAdvancedUnregisterTableState(_key)`

Removes a registered table key.

**Arguments**
- `_key` `String`

**Returns**: `Struct.FateRegistryMutationReturn`

**Additional Notes**
Unregistering removes the key mapping only. It does not destroy the table instance itself.

---

### `FateAdvancedGetRegisteredTableStateKeys()`

Lists registered keys (`GetKeys()` / `data.keys`).

**Arguments**: None.

**Returns**: `Struct.FateRegistryKeysReturn`

**Additional Notes**
This is useful in advanced tooling to inspect weak-reference registry state before capture or restore operations.

---

### `FateAdvancedPruneRegisteredTableStates()`

Prunes dead/invalid weak references from registry.

**Arguments**: None.

**Returns**: `Struct.FatePruneReturn`

**Additional Notes**
Pruning removes dead weak references from the registry. Running this before capture can reduce noise in operational reports.

---

### `FateAdvancedCaptureRegisteredTableStates(_opts = undefined)`

Captures bundle state for all live registered tables.

**Arguments**
- `_opts` `Struct|Undefined` (supports `prune_dead`)

**Returns**: `Struct.FateCaptureReturn`

**Additional Notes**
This captures state from currently live registered tables only. With `prune_dead = true`, dead keys are cleaned as part of the same call.

---

### `FateAdvancedRestoreRegisteredTableStates(_bundle_state, _opts = undefined)`

Restores all live registered tables from a bundle state payload.

**Arguments**
- `_bundle_state` `Struct`
- `_opts` `Struct|Undefined` (supports `prune_dead`)

**Returns**: `Struct.FateRestoreReturn`

**Additional Notes**
This restores matching live registered tables from a bundle. The return counters help you see partial-apply cases without reading table internals.

---

### `FateAdvancedSaveRegisteredTableStatesFile(_filename, _opts = undefined)`

Captures all live registered tables and saves JSON.

**Arguments**
- `_filename` `String`
- `_opts` `Struct|Undefined`

**Returns**: `Struct.FatePipelineReturn`

**Additional Notes**
This is a full registry pipeline call that captures and writes in one step. Nested result structs are included so failures can be traced to capture or file write stages.

---

### `FateAdvancedLoadRegisteredTableStatesFile(_filename, _opts = undefined)`

Loads JSON and restores matching live registered tables.

**Arguments**
- `_filename` `String`
- `_opts` `Struct|Undefined`

**Returns**: `Struct.FatePipelineReturn`

**Additional Notes**
This is a full registry pipeline call that loads and restores in one step. Nested result structs are included so failures can be traced to load or restore stages.

---

### `FateAdvancedCaptureTableStates(_table_map)`

Captures bundle state for a provided map of tables.

**Arguments**
- `_table_map` `Struct` (`{ key: FateTable, ... }`)

**Returns**: `Struct.FateCaptureReturn`

**Additional Notes**
Use this when you want explicit control over which tables are captured. It is the low-level capture API behind registry and beginner file helpers.

---

### `FateAdvancedRestoreTableStates(_table_map, _bundle_state)`

Restores a provided map of tables from bundle state.

**Arguments**
- `_table_map` `Struct` (`{ key: FateTable, ... }`)
- `_bundle_state` `Struct`

**Returns**: `Struct.FateRestoreReturn`

**Additional Notes**
Use this when you already have a bundle and a specific table map to restore. It gives detailed counters for missing, invalid, and skipped entries.

---

### `FateAdvancedValidateTableConfig(_table, _opts = undefined)`

Validates table configuration and returns report.

**Arguments**
- `_table` `Struct.FateTable`
- `_opts` `Struct|Undefined`

**Returns**: `Struct` validation report

**Additional Notes**
This checks table configuration and policy setup. It is most useful at integration boundaries before a table is exposed to live content.

---

### `FateAdvancedValidateTableState(_table, _state, _opts = undefined)`

Validates table state payload and returns report.

**Arguments**
- `_table` `Struct.FateTable`
- `_state` `Struct`
- `_opts` `Struct|Undefined`

**Returns**: `Struct` validation report

**Additional Notes**
Use this before applying unknown state payloads. It returns issue details and sanitized data when validation can recover safely.

---

## Top-level simulation helpers (advanced QA)

These helpers are for balance analysis and QA checks. They are usually used in dev tooling, not live gameplay loops.
For step-by-step usage and examples, see [Simulation Testing](./simulation-testing.md).

### `FateTestSimulate(_table, _opts = undefined)`

Runs deterministic roll simulation and returns a simulation report.

**Arguments**
- `_table` `Struct.FateTable`
- `_opts` `Struct|Undefined`

**Returns**: `Struct` simulation report (`{ format, version, table_id, runs, count, seed, total_rolls, total_selected, entry_stats, exhausted_reason_counts, diagnostics_totals, selection_totals, result_hash }`)

**Additional Notes**
This helper is for QA and balancing, not live roll loops. Use a fixed seed for reproducible reports.

---

### `FateTestSimulationAssert(_sim_report, _checks = undefined)`

Evaluates simulation report against checks.

**Arguments**
- `_sim_report` `Struct`
- `_checks` `Any` (check struct when provided)

**Returns**: `Struct` (`{ ok, failure_count, failures }`)

**Additional Notes**
This evaluates a simulation report against thresholds. Each failure entry includes both expected and actual values for direct debugging.

---

### `FateTestSimulationComposeChecks(_bundles, _opts = undefined)`

Merges check bundles into one checks struct.

**Arguments**
- `_bundles` `Any` (`Struct` or `Array<Struct>`)
- `_opts` `Struct|Undefined`

**Returns**: `Struct` (`{ checks, composition_warnings, warning_count }`)

**Additional Notes**
Use this when checks come from several presets or modules. Composition warnings help catch accidental overrides.

---

### `FateTestSimulationRunAndAssert(_table, _sim_opts = undefined, _checks = undefined, _opts = undefined)`

Runs simulation and assertions in one call.

**Arguments**
- `_table` `Struct.FateTable`
- `_sim_opts` `Struct|Undefined`
- `_checks` `Any`
- `_opts` `Struct|Undefined`

**Returns**: `Struct` (`{ ok, sim_report, assert_report, checks, failure_count, composition_warning_count, composition_warnings, summary_lines }`)

**Additional Notes**
This is the most practical entry point for automated balance tests. It runs the full simulate and assert flow and returns summary lines ready for logs.

---

### Check preset builders

- `FateTestSimulationPresetExpectedHash(_expected_hash)`
- `FateTestSimulationPresetNoExhaustion()`
- `FateTestSimulationPresetEntryRateRange(_entry_or_entry_id, _min_rate = undefined, _max_rate = undefined)`
- `FateTestSimulationPresetEntryRateBand(_entry_or_entry_id, _target_rate, _tolerance = 0)`
- `FateTestSimulationPresetEntryRateRanges(_ranges_map)`
- `FateTestSimulationPresetEntryRateBands(_bands_map)`
- `FateTestSimulationPresetStrictFairness(_entries_map, _tolerance = 0)`

Each preset builder returns a check bundle struct compatible with `FateTestSimulationComposeChecks(...)`.
A common beginner workflow is to combine `FateTestSimulationPresetNoExhaustion()` with one or more rate band presets, then compose and assert.

---

## Policy constructor options

### `new FatePityPolicy(_opts = undefined)`

**Required**
- `_opts.target_matcher(_entry, _ctx) -> Bool`

**Optional**
- `_opts.scope_key(_ctx) -> Any`
- `_opts.soft_start` (default `0`)
- `_opts.soft_step` (default `0`)
- `_opts.hard_at` (default `undefined`)
- `_opts.reset_mode` (default `"target_hit"`, values: `"any_hit" | "target_hit" | "never"`)
- `_opts.policy_name` `String`
- `_opts.priority` `Real`

**Returns**: `Struct` policy

Pity policy is usually the first advanced policy to author manually. It is a good fit when beginner helper inputs are not flexible enough for your targeting logic.

---

### `new FateDuplicateProtectionPolicy(_opts = undefined)`

**Required**
- `_opts.entry_key(_entry, _ctx) -> Any`

**Optional**
- `_opts.scope_key(_ctx) -> Any`
- `_opts.window` (default `0`)
- `_opts.mode` (default `"penalize"`, values: `"penalize" | "exclude"`)
- `_opts.penalty_mult` (default `0.25`)
- `_opts.intra_roll_unique` (default `true`)
- `_opts.owned_check(_entry, _ctx) -> Bool`
- `_opts.owned_penalty_mult` (default `0.5`)
- `_opts.policy_name` `String`
- `_opts.priority` `Real`

**Returns**: `Struct` policy

Duplicate protection policies are useful when design requires controlled repetition behavior across recent pulls, owned content, or both.

---

### `new FateBatchGuaranteePolicy(_opts = undefined)`

**Required**
- `_opts.matcher(_entry, _ctx) -> Bool`

**Optional**
- `_opts.min_count` (default `1`)
- `_opts.only_when_roll_count_at_least` (default `2`)
- `_opts.soft_mult` (default `1`)
- `_opts.allow_bypass_filters` (default `true`)
- `_opts.policy_name` `String`
- `_opts.priority` `Real`

**Returns**: `Struct` policy

Batch guarantee policies are useful for enforcing minimum quality in fixed-size roll batches, such as ten-pull systems.

---

### `new FateFeaturedRateUpPolicy(_opts = undefined)`

**Required**
- `_opts.is_featured(_entry, _ctx) -> Bool`

**Optional**
- `_opts.scope_key(_ctx) -> Any`
- `_opts.rate_up_mult` (default `1`)
- `_opts.hard_at` (default `undefined`)
- `_opts.reset_mode` (default `"featured_hit"`, values: `"featured_hit" | "any_hit" | "never"`)
- `_opts.policy_name` `String`
- `_opts.priority` `Real`

**Returns**: `Struct` policy

Featured rate-up policies are useful for event banners where highlighted targets need higher exposure while preserving weighted randomness.

---

## Shared policy method contract

Each policy struct can expose:
Beginner code paths do not need to implement these directly, but custom policy authors should keep this contract stable and predictable.

### Required

- `ResolveForRoll(_context, _event)`
- `OnSelected(_context, _event)`
- `OnRollFinished(_context, _summary)`

### Optional metadata/lifecycle

- `GetPolicyId()`
- `GetPolicyName()`
- `GetPriority()`
- `ValidateForTable(_strictness, _table_id)`
- `GetState()`
- `SetState(_state)`
- `ResetScope(_scope_key)`
- `ResetAll()`
