---
layout: default
title: Simulation Testing
parent: Fate
nav_order: 5
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Simulation Testing Guide

Fate includes built-in simulation helpers for balance QA and regression checking.

This page explains how to use them, including check composition and deterministic hash workflows.

## What simulation is for

Simulation is for questions like: are observed rates close to expected rates, did a policy change break fairness, did pull behavior drift between versions, and are we hitting exhaustion reasons we should never hit. These APIs are development and QA tools, not hot gameplay loop code.

## Core flow

The usual flow is to run a simulation report with `FateTestSimulate(...)`, build checks (manually or with presets), then assert with `FateTestSimulationAssert(...)` or do it in one shot with `FateTestSimulationRunAndAssert(...)`.

## 1) Run a simulation report

```js
var _sim = FateTestSimulate(loot_table, {
	runs: 20000,
	count: 1,
	seed: 12345,
	restore_state: true,
	collect_mode: "basic"
});
```

### Simulate options

| Option | Default | Meaning |
| --- | --- | --- |
| runs | 10000 | Number of roll runs. |
| count | 1 | Roll count per run. |
| seed | 1 | Deterministic RNG seed. |
| context | undefined | Fixed context passed every run. |
| context_provider | undefined | Optional function called per run (`fn(run_index) -> context`). |
| restore_state | true | Restore table state after simulation. |
| collect_mode | "basic" | `"basic" | "diagnostics" | "full"`. |

### Report fields

`FateTestSimulate(...)` returns a simulation report struct (not one of our usual `{ ok, code, data, kind }` contracts). Key fields include `runs`, `count`, `seed`, `total_rolls`, `total_selected`, `entry_stats` (per root-table entry: `entry_id`, `insertion_order`, `hits`, `hit_rate`), `exhausted_reason_counts`, `diagnostics_totals` (when `collect_mode` is `"diagnostics"` or `"full"`), `selection_totals` (when `collect_mode` is `"full"`), and `result_hash`.

## 2) Build checks

Checks are a struct with optional fields: `entry_rate_min`, `entry_rate_max`, `exhausted_reason_max`, and `expected_hash`.

### Manual checks example

```js
var _checks = {
	entry_rate_min: {},
	entry_rate_max: {},
	exhausted_reason_max: {
		slot_cap: 0,
		pool_empty: 0,
		uniqueness_exhausted: 0
	}
};

_checks.entry_rate_min[$ string(_rare.entry_id)] = 0.045;
_checks.entry_rate_max[$ string(_rare.entry_id)] = 0.075;
```

### Preset helpers (recommended)

Fate includes presets to reduce boilerplate:

```js
FateTestSimulationPresetExpectedHash(...)
FateTestSimulationPresetNoExhaustion()
FateTestSimulationPresetEntryRateRange(...)
FateTestSimulationPresetEntryRateBand(...)
FateTestSimulationPresetEntryRateRanges(...)
FateTestSimulationPresetEntryRateBands(...)
FateTestSimulationPresetStrictFairness(...)
```

You can pass entries, numeric entry IDs, or string IDs where supported.

```js
var _b_no_exhaust = FateTestSimulationPresetNoExhaustion();
var _b_rare_band = FateTestSimulationPresetEntryRateBand(_rare, 0.06, 0.01);
```

## 3) Compose and assert

### Compose bundles

Use `FateTestSimulationComposeChecks(...)` when checks are coming from multiple places.

```js
var _compose = FateTestSimulationComposeChecks([
	_b_no_exhaust,
	_b_rare_band
], {
	warn_on_override: true
});

var _checks = _compose.checks;
```

If later bundles override earlier values, composition warnings are included.

### Assert report against checks

```js
var _assert = FateTestSimulationAssert(_sim, _checks);
if (!_assert.ok) {
	for (var i = 0; i < array_length(_assert.failures); i++) {
		var _f = _assert.failures[i];
		show_debug_message($"SIM FAIL {_f.code} at {_f.path}: {_f.message}");
	}
}
```

### One-shot run + assert

```js
var _out = FateTestSimulationRunAndAssert(
	loot_table,
	{ runs: 20000, count: 1, seed: 12345 },
	[_b_no_exhaust, _b_rare_band],
	{ warn_on_override: true }
);

if (!_out.ok) {
	for (var i = 0; i < array_length(_out.summary_lines); i++) {
		show_debug_message(_out.summary_lines[i]);
	}
}
```

## Deterministic hash workflow

`result_hash` lets you lock expected behavior over time. Pick stable simulation settings (`runs`, `count`, `seed`, context behavior), run simulation once and record `result_hash`, add `FateTestSimulationPresetExpectedHash(hash)` to your check bundles, then keep it there as a regression tripwire. Future runs fail if behavior drifts under those fixed settings.

```js
var _hash_bundle = FateTestSimulationPresetExpectedHash(1234567890);
```

Use this when you intentionally want deterministic behavior under fixed settings.

## Context and scoped-policy simulations

If your policies use scope keys (for example per account/profile), drive contexts per run with `context_provider`:

```js
var _sim = FateTestSimulate(loot_table, {
	runs: 10000,
	count: 1,
	seed: 99,
	context_provider: function(_run_index) {
		return {
			profile_id: string((_run_index mod 5) + 1)
		};
	}
});
```

This is useful when testing how scoped pity/rate-up behavior behaves across mixed traffic.

## collect_mode guidance

Use `basic` for speed when you're just checking rates. Use `diagnostics` when you want diagnostics aggregates. Use `full` when you want everything, including diagnostics plus selection depth/via totals. Start with `basic`, then increase detail as and if you require it.

## Common pitfalls

Common pitfalls include checking entry rates by value string instead of entry ID, forgetting that simulation tracks root table entries in `entry_stats`, setting `restore_state: false` and then reusing the same table state later, changing `runs`, `count`, `seed`, or context rules while expecting the same `expected_hash`, and treating `FateTestSimulate` like a wrapper result (`{ ok, code, data, kind }`) when it returns a report struct directly.

## Recommended baseline profile

For a practical first setup:

```js
var _out = FateTestSimulationRunAndAssert(
	loot_table,
	{ runs: 20000, count: 1, seed: 12345, collect_mode: "basic" },
	[
		FateTestSimulationPresetNoExhaustion(),
		FateTestSimulationPresetEntryRateBand(_rare, 0.06, 0.01)
	],
	{ warn_on_override: true }
);
```

This gives a strong, repeatable baseline for most weighted-table sanity checks.
