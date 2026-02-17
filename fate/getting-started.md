---
layout: default
title: Getting Started
parent: Fate
nav_order: 1
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Getting Started

This page gets Fate running quickly in a clean project, with a single simple table you can roll and save.

## 1. Import Fate

In GameMaker, import Fate as a local package:

1. Tools -> Import Local Package.
2. Select the Fate package file.
3. Click Add All.
4. Click Import.

## 2. Create entries and a table

Create entries in a setup place that runs once (usually a Create event).

```js
// obj_ui Create
var _common = new FateValueEntry("COMMON").SetWeight(94);
var _rare = new FateValueEntry("RARE").SetWeight(6);

loot_table = new FateTable([_common, _rare]);
```

## 3. Roll values

Beginner rolls should usually use `FateRollValues(...)` because it returns values directly plus status info.

```js
var _roll = FateRollValues(loot_table, 1);
if (!_roll.IsOk()) {
	show_debug_message("Roll failed: " + _roll.code);
	return;
}

var _value = _roll.GetFirstDrop();
show_debug_message("Pulled: " + string(_value));
```

All beginner/advanced wrapper functions return a "contract". A contract is simply a chunk of information that lets you know various things about what happened when you tried to perform some action with Fate. All contracts have a set of base data that is included with them:

```js
{ ok, code, data, kind }
```

But they will also have specific methods associated with the specific kind of contract that was returned. You can see the kind by checking the return value of `GetReturnKind()` (you can use this to branch depending on the contract family if you need to).

Let's talk about the `_roll` contract we got returned in the above example: `var _roll = FateRollValues(loot_table, 1);`. By checking the API reference page, we can see that `FateRollValues()` returns a `FateRollReturn` contract. Finding that contract in the API page, we can see that it has a bunch of methods associated with examining and retrieving the results of the roll. We use the `GetFirstDrop()` method in the example, so that we can see the first drop that resulted from the roll (in this case, since we only ask for one drop, it's the ONLY drop that was returned).

Contracts might sound scary if you're a beginner, but in reality, they are just a struct which you can access through dot notation (`struct.value`), and you can see exactly what variables and methods you have access to in that struct in the API page.

## 4. Add a beginner policy

Policies are little rules you can set that determine how a weighted drop table will behave over time. It's very common for devs to include things like "pity mechanics" when dealing with drops, and policies are how we implement them in Fate.

Use the table `.Enable*` methods first. They're named-argument friendly and autocomplete cleanly (when GMs autocomplete system is working properly, hahaha). These allow you to easily implement common gacha mechanics for drops, like a pity system, or "rate up" system.

```js
loot_table.EnablePity(_rare, 90, 75, 0.06);
```

To outline what the above code does, it sets hard pity at 90 misses (i.e. a guaranteed drop), soft pity starting at 75 misses, and then +0.06 weight per miss after the soft start.

## 5. Track and save snapshot state

If you want save/load behavior, register the table once and then use snapshot file helpers.

```js
var _track = FateTrackTable("loot.main", loot_table);
if (!_track.ok) {
	show_debug_message("Track failed: " + _track.code);
}

var _save = FateSaveSnapshotFile("save_01.json");
if (!_save.ok) {
	show_debug_message("Save failed: " + _save.code);
}
```

Load and restore:

```js
var _load = FateLoadSnapshotFile("save_01.json");
if (!_load.ok) {
	show_debug_message("Load failed: " + _load.code);
}
```

## Common first-time mistakes

Common first-time mistakes include expecting `table.Roll()` to return plain values (it returns `FateEntry` objects, so use `FateRollValues(...)` if you want direct values), adding a `FateTable` directly into another table (wrap nested tables with `FateTableEntry`), creating tables in Draw/Step events (build once, then reuse), and forgetting to track tables before calling snapshot file helpers.
