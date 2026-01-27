---
layout: default
title: Integration and Debugging
parent: Whisper
nav_order: 2
---

<!--
/ integration_debugging.md - Changelog:
/ - 25-01-2026: Initial draft (install, bootstrapping, run ids, debugging helpers).
-->

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
   {:toc}

</details>
</div>

# Integration and Debugging

This page is the "make it actually work in your game" page.

We are going to cover:

* How to drop Whisper into a project cleanly
* Where to put your storylet setup code
* How to debug "why is Whisper returning nothing"
* A practical pattern for verbs when you have a typewriter / reveal effect

---

## Installing Whisper

Whisper comes alongside a free copy of Echo as a local package. The installation steps are:

1. Open your GM project (make sure you are on a modern GameMaker version with struct constructors + methods).
2. Click Tools > Import Local Package.
3. Find the Whisper local package wherever you downloaded it to.
4. Select it and wait for GM to open the package.
5. Click Add All.
6. Click Import.

Whisper sets up its global singletons automatically when the script is loaded, so you do not need to create an object just to "start Whisper".

That said, you *do* need a place to register your content (storylets, verbs, insertions). That is the next section.

---

## Where your Whisper setup should live

If you write your storylets inside random object Create events, you will eventually lose track of what exists and why.

A cleaner pattern is:

* One setup script (or one controller object) that runs once.
* All Whisper content registration happens there.

Example (create a function like this with all your Whisper content inside it and then run it once in the Game Start Event or something like that):

```js
/// scr_game_bootstrap.gml (or obj_game_controller Create)

function GameBootstrapWhisper() {
	// Register verbs
	WhisperVerbAdd("give_gold", function(_ctx, _ev) {
		// Your game logic here
		_ctx.subject.gold += real(_ev.args[0]);
	});

	// Register insertions (random text variants)
	WhisperInsertAdd("creature", ["rat", "spider", "slime"]);

	// Register storylets
	WhisperStorylet("sewer_creature")
		.TagAdd("sewers")
		.SetWeight(10)
		.SetCooldown(30)
		.SetPredicate(function(_ctx) {
			return _ctx.location == "sewers";
		})
		.TextAdd("A ##creature## scurries past... " + WhisperVerbMarker("give_gold"))
		.AddToPool("sewer_events");
}
```

A couple of notes:

* `WhisperStorylet(id)` returns the existing storylet if that id already exists.

  * That prevents duplicate storylets, which is nice.
  * But if you run your bootstrap twice, you can still accidentally add extra text variations/tags twice.
* If you are doing live-reload style dev workflows, `WhisperResetAll()` exists to wipe everything and recreate the singletons. That is more of a dev tool than a normal gameplay tool.

---

## Basic gameplay wiring (pick -> resolve -> display)

Most games follow this loop:

1. Build a context (what is happening right now).
2. Ask Whisper to pick something.
3. Resolve the text.
4. Show it in your UI.
5. Fire any verbs tied to the text (optional, depending on your UI style).

Minimal example using the pool API:

```js
/// Wherever you want to trigger a story moment

var _ctx = WhisperContextSimple(player, "sewers");

var _storylet = WhisperPoolPickAndFire("sewer_events", _ctx);

if (!is_undefined(_storylet)) {
	var _resolved = _storylet.TextResolve(); // returns { text, events }
	ShowDialogue(_resolved.text);

	// If you are not doing a typewriter effect, you will typically fire
	// verbs at "completion" (see typewriter section below for the fancy version).
	WhisperVerbRunRange(_resolved.events, -1, string_length(_resolved.text), _ctx);
}
```

A beginner-friendly way to think about this:

* The **context** is "what Whisper is allowed to know about the current situation".
* The **storylet** is "a little packet of narrative + rules for when it can happen".
* The **resolved text** is "the final output after insertions are filled in".

---

## Runs, run ids, and why they matter

Whisper supports "per run" limits. This is for roguelikes / runs / loops where you might want:

* A storylet that can only happen once per run
* But can happen again on a future run

Whisper tracks a `run_id` internally.

Useful calls:

* `WhisperNewRun()` -> increments the run id (new run)
* `WhisperGetRunId()` -> read current run id (useful for saving)
* `WhisperSetRunId(id)` -> restore a run id (useful for loading)

Practical pattern:

* When starting a brand new run: call `WhisperNewRun()`
* When loading a save: call `WhisperSetRunId(saved_run_id)`

This keeps "per run" usage limits behaving the way you expect.

---

## Debugging: "why did nothing match"

This is the most common Whisper bug report:

> "WhisperPick returns undefined. But I swear I added storylets."

Whisper gives you debug helpers that answer that question directly.

### 1) Turn on debug logging

At the top of the script there is a macro:

* `#macro WHISPER_DEBUG 0`

Set it to `1` while you are developing.

When debug is enabled, Whisper logs extra information via Echo-style functions (for example `EchoDebugInfo`, `EchoDebugWarn`).

If you are not using Echo yet, you have two options:

* Add Echo to your project (recommended long-term if you like having nice logs).
* Or stub the functions temporarily:

```js
function EchoDebugInfo(_msg, _tags) { show_debug_message(_msg); }
function EchoDebugWarn(_msg, _tags) { show_debug_message(_msg); }
```

### 2) Use `WhisperDebugQuery` (global) or `WhisperPoolDebugQuery` (pool)

These return an array of structs describing what happened for each storylet.

Each entry contains:

* `id`
* `ok` (overall match)
* `can_fire` (passes predicate/cooldown/uses rules)
* detailed flags like `predicate_ok`, `cooldown_ok`, `uses_total_ok`, `uses_run_ok`
* tag filter flags like `tags_all_ok`, `tags_any_ok`, `tags_not_ok`
* `reasons` (an array of short strings like `"cooldown_active"`)

Example:

```js
var _ctx = WhisperContextSimple(player, "sewers");

var _report = WhisperPoolDebugQuery("sewer_events", _ctx);

for (var i = 0; i < array_length(_report); i++) {
	var _r = _report[i];
	if (!_r.ok) {
		show_debug_message("Whisper blocked: " + string(_r.id) + " -> " + string(_r.reasons));
	}
}
```

Now you are not guessing. You will see the exact reason list per storylet.

### 3) Use `WhisperDebugMatch` for one specific storylet

If you already know which storylet you care about:

```js
var _ctx = WhisperContextSimple(player, "sewers");
var _info = WhisperDebugMatch("sewer_creature", _ctx);

show_debug_message(string(_info.ok));
show_debug_message(string(_info.reasons));
```

---

## Advanced: verbs with a typewriter / reveal effect

Whisper verbs are stored as "events" inside the resolved result:

```js
var _resolved = _storylet.TextResolve();
// _resolved.text   -> final text
// _resolved.events -> event list, with positions and triggers
```

If you have a typewriter effect, you can fire verbs as the cursor crosses specific positions:

* Track the previous character index (`_from_pos`)
* Track the new character index (`_to_pos`)
* Call `WhisperVerbRunRange(events, _from_pos, _to_pos, ctx)`

Example sketch:

```js
// When you start showing the line:
_from_pos = -1;
_to_pos = 0;
WhisperVerbRunRange(_resolved.events, _from_pos, _to_pos, _ctx);

// Each time you reveal more characters:
var _next_pos = min(_to_pos + reveal_step, string_length(_resolved.text));
WhisperVerbRunRange(_resolved.events, _to_pos, _next_pos, _ctx);
_to_pos = _next_pos;

// When the line finishes:
WhisperVerbRunRange(_resolved.events, _to_pos, string_length(_resolved.text), _ctx);
```

Important note (because it will bite you otherwise):

* `WhisperVerbRunRange` does **not** remember what already fired.
* If you call it twice with overlapping ranges, you can double-fire verbs.
* Your UI code should make sure `_from_pos` -> `_to_pos` is always moving forward cleanly.

---

## Quick checklist when Whisper "does nothing"

If `WhisperPick*` returns `undefined`, usually one of these is true:

* Your storylet `weight` is `0` or negative (only positive weights are eligible).
* Your predicate returned false.
* Cooldown is active.
* Max uses (total or per run) has been reached.
* Your tag filter excludes everything (for example `tags_all` requires tags the storylets do not have).
* You are picking from a pool that is empty (you forgot `.AddToPool(...)`).

If you are not sure which one: run `WhisperDebugQuery` / `WhisperPoolDebugQuery` and look at `reasons`.