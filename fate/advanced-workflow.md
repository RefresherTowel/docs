---
layout: default
title: Advanced Workflow
parent: Fate
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

# Advanced Workflow

This page is for projects that need tighter control over behavior, diagnostics, and persistence.

## 1. Strictness strategy

Each table has a strictness mode: `FateStrictness.SILENT`, `FateStrictness.DEBUG`, or `FateStrictness.ERROR`.

Set per table:

```js
table.SetStrictness(FateStrictness.DEBUG);
```

A good default is `DEBUG` during development, then `SILENT` for live release (or `ERROR` if you'd rather fail fast).

## 2. Detailed roll telemetry

Use `RollDetailed(...)` when you need full traces.

```js
var _detail = table.RollDetailed(10, _context, _rng);

// _detail has:
// results, roll, diagnostics, selected_events, table_summaries
```

This is useful for debugging policy interactions and nested roll behavior.

## 3. Preview and probability queries

For UI previews and balancing tools, use `Preview(_count, _context)`, `GetEntryProbability(_entry, _context)`, and `GetValueProbability(_value, _context)`.

Example:

```js
var _chance = table.GetValueProbability("RARE");
show_debug_message("Rare chance: " + string(_chance));
```

## 4. Manual state bundles

If you need full save-pipeline control, use the map-based bundle helpers `FateAdvancedCaptureTableStates(_table_map)` and `FateAdvancedRestoreTableStates(_table_map, _bundle_state)`.

```js
var _map = {
	main: table_a,
	weapon: table_b
};

var _capture = FateAdvancedCaptureTableStates(_map);
if (_capture.ok) {
	var _state = _capture.GetState();
	FateAdvancedSaveStateFile("state.json", _state);
}
```

## 5. Registry-backed snapshots

For weakref-based registry flows, use the advanced registry helpers below. This is the advanced form of the beginner `FateTrackTable` + `FateSaveSnapshotFile` flow.

```js
// Register a single table state
FateAdvancedRegisterTableState(...)

// Capture/restore all registered table states
FateAdvancedCaptureRegisteredTableStates(...)
FateAdvancedRestoreRegisteredTableStates(...)

// File wrappers
FateAdvancedSaveRegisteredTableStatesFile(...)
FateAdvancedLoadRegisteredTableStatesFile(...)
```

## 6. Validation boundaries

Validate configuration/state before applying unknown data with `FateAdvancedValidateTableConfig(_table, _opts)` and `FateAdvancedValidateTableState(_table, _state, _opts)`. Use the validation reports to block bad payloads at your boundaries.

## 7. Custom policy authoring checklist

Before shipping a custom policy:

1. Keep `ResolveForRoll` pure.
2. Do state mutation in `OnSelected` and `OnRollFinished`.
3. Implement `GetState`/`SetState` for persistence-sensitive behavior.
4. Implement `ValidateForTable` so bad configs are rejected early.
5. Bind callback scope using `method(scope, fn)` for any function refs.

For simulation and balance QA workflows, see [Simulation Testing](./simulation-testing.md).
