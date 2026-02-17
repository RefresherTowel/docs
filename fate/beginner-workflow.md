---
layout: default
title: Beginner Workflow
parent: Fate
nav_order: 2
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Beginner Workflow

This is the recommended path if you want good defaults without high decision overhead.

## The simple model

Think of Fate in three layers: entries (what can be selected), table (how selection happens), and policies (optional behavior changes like pity and duplicate protection). If you stay inside this model, Fate is easy to reason about.

## Pick the right entry type

Use the smallest entry type that solves your case.

`FateValueEntry(value)` is the most common choice, for plain item IDs, strings, structs, and so on.

`FateTableEntry(table, count)` is for cases where an entry should expand into another table (nested rolls).

`FateCreatorEntry(constructor, args)` is for cases where selection should create a new payload value at roll time. This is useful for when you want something to actually be created when dropped. A use case might be that you are using the weighted drop system to decide what enemies to create. You would supply the object ID (`obj_enemy` or whatever) of the enemy for the constructor argument, and then when you roll, Fate will automatically create an instance of whatever was dropped (please note: the instance will be created at `x = 0`, `y = 0` and `depth = 0`, so you would then have to manually handle the positioning and layer setting of the newly created instance). You can also supply constructors, which will print a struct from the constructor when dropped.

Most beginner projects should start with `FateValueEntry`.

## Start with one table and one policy

```js
var _common = new FateValueEntry("COMMON").SetWeight(94);
var _rare = new FateValueEntry("RARE").SetWeight(6);

loot_table = new FateTable([_common, _rare])
	.EnablePity(_rare, 90, 75, 0.06);
```

Then roll through `FateRollValues(...)`.

## Recommended helper order

When you're stacking helper policies, a solid default order is pity first, then rate-up (if you have featured targets, an example being a limited time promotion when "Beastly" monsters should drop more often during halloween or something), then duplicate protection (if repeats are a problem), and finally any multi-pull guarantee rules (`EnableTenPullGuarantee(...)` or `EnableBatchGuarantee(...)`).

If you want a quick baseline for gacha tables, use:

```js
loot_table.EnableStandardGachaRules(_five_star_entries, _featured_entries, 90, 75, 1.5);
```

(`_five_star_entries` in this case being extremely rare drops that you want to increase the chance of each time a player pulls a drop, and `_featured_entries` being drops that are currently being promoted).

## Save/load without manual table state wiring

Register once:

```js
FateTrackTable("loot.main", loot_table);
```

Then save/load snapshots:

```js
FateSaveSnapshotFile("save_01.json");
FateLoadSnapshotFile("save_01.json");
```

This is usually enough for beginners and avoids hand-written per-table state plumbing.

## Handling failures consistently

Beginner wrappers return contract structs with `ok`, `code`, `data`, and `kind`.

Use this pattern everywhere:

```js
var _out = FateSaveSnapshotFile("save_01.json");
if (!_out.ok) {
	show_debug_message("Fate failed: " + _out.code);
	return;
}
```

Use `GetReturnKind()` if you need to branch by contract family.

## When to move to advanced APIs

Move up only when you actually need it: custom policy logic beyond entry-list targeting, full state bundle control beyond tracked table snapshots, or richer diagnostics and policy event traces.
