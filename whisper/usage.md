---

layout: default
title: Usage
parent: Whisper
nav_order: 4
------------

<!--
/// usage.md - Changelog:
/// - 25-01-2026: Initial Whisper usage docs.
/// - 25-01-2026: Add manual tick time option.
-->

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
   {:toc}

</details>
</div>

# Usage & Examples

This page walks through Whisper in three layers, from "I just want random barks" up to "ok, now my dialogue is reacting to the game state on purpose":

* **Beginner** -> pools + simple lines + "just give me text"
* **Intermediate** -> tags, context, and filters (still pretty painless)
* **Advanced** -> real storylets: predicates, cooldowns, usage limits, and manual pick flows

You don't need all of this. If you only use the Beginner layer, you'll still be saving a lot of time and effort when it comes to what to show when.

---

## Beginner: Pools + simple lines

The beginner layer is about one simple story:

> Put a bunch of lines in a pool, then ask Whisper to pick one.

### 1. Create some lines

You usually do this once at startup (game controller Create, or wherever you set up your content).

```js
/// obj_game Create (or scr_init_dialogue)

WhisperLineSimple("npc_bridge", "Hey.", "greeting");
WhisperLineSimple("npc_bridge", "Another shift, another headache.", ["greeting", "mood:tired"]);
WhisperLineSimple("npc_bridge", "Keep your eyes open out there.", ["warning"]);

WhisperLineSimple("npc_engineering", "Do not touch that button.", ["warning", "npc:engineer"]);
WhisperLineSimple("npc_engineering", "If it starts smoking, it's probably fine.", ["joke"]);
// Etc
```

Notes:

* Pool ids are just identifiers. Strings are usually the nicest to work with.
* Tags are optional. If you pass a string, it's treated as a single tag. If you pass an array, it's treated as many tags.
* Weight is optional (defaults to 1). Weight <= 0 means "not eligible".

### 2. Ask Whisper for a line (resolved result)

`WhisperSaySimple` picks and fires a storylet from a pool, then resolves it into:

* `text` -> what you show to the player
* `events` -> verb events (you can ignore this for now)
* `storylet` -> the storylet that was chosen (optional extra info)

```js
/// Somewhere in your dialogue trigger

var _ctx = WhisperContextMinimal(player_id, "bridge");
var _out = WhisperSaySimple("npc_bridge", _ctx);

if (!is_undefined(_out)) {
	ShowDialogue(_out.text);
}
```

If nothing matches, it returns `undefined`. That's normal.

### 3. "Just give me text" (with a fallback)

If you don't care about events or the chosen storylet, use `WhisperSayTextSimple`.

```js
var _ctx  = WhisperContextMinimal(player_id, "bridge");
var _text = WhisperSayTextSimple("npc_bridge", _ctx, "en", "...");
ShowDialogue(_text);
```

That fallback is handy for UI barks where you never want "nothing happened".

### 4. Quick tag filtering (one-liner)

If you only need "must have at least one of these tags", `WhisperSayTaggedSimple` is the fast path.

```js
var _ctx = WhisperContextMinimal(player_id, "bridge");

// Must match at least one tag in tags_any
var _out = WhisperSayTaggedSimple("npc_bridge", ["warning", "mood:tired"], _ctx);

if (!is_undefined(_out)) {
	ShowDialogue(_out.text);
}
```

Under the hood this is building a filter with `tags_any` and doing a pool pick.

---

## Intermediate: Context + filters (without pain)

Once you're past "random barks", the next step is: "pick something that fits what's happening".

### 1. Context is just a struct you control

Whisper passes `_ctx` into predicates and hooks. You decide what goes in there.

Two helpers exist:

* `WhisperContextMinimal(subject, location)`
* `WhisperContextSimple(subject, location, story)`

```js
var _ctx = WhisperContextSimple(player_id, "bridge", global.story);
```

Beginner note:

* "Context" here just means "extra info". It's not magic. It's literally a struct you pass in so your storylets can check things.

### 2. Filters let you narrow down by tags (and more)

Use `WhisperFilter()` to build a filter struct:

```js
var _filter = WhisperFilter();
_filter.tags_any = ["warning", "combat"];
_filter.tags_not = ["spoiler"];
```

To use a filter, you generally switch from `WhisperSaySimple` to the "advanced pick" flow for a pool:

```js
var _ctx    = WhisperContextMinimal(player_id, "bridge");
var _now    = WhisperNow();
var _filter = WhisperFilter();
_filter.tags_any = ["warning", "combat"];

var _storylet = WhisperPoolPickAndFire("npc_bridge", _ctx, _now, _filter);

if (!is_undefined(_storylet)) {
	var _out = _storylet.TextResolve("en");
	if (!is_undefined(_out)) {
		ShowDialogue(_out.text);
	}
}
```

What the filter fields mean:

* `tags_all` -> must include every tag in this list
* `tags_any` -> must include at least one tag in this list
* `tags_not` -> must include none of these tags
* `tags_prefer` -> "try to prefer these" (soft preference)
* `prefer_weight` -> how strong that preference is (optional)
* `custom` -> a function for extra filtering (advanced)

If you're thinking "cool, but I'd like a friendlier wrapper for that exact pattern", that's a totally fair future helper to add. For now, this is the clean, explicit version.

---

## Advanced: Real storylets (the good stuff)

This is where Whisper stops being "random lines" and becomes "content that reacts to the game".

### 1. Build a storylet explicitly

`WhisperStorylet(id)` creates a storylet you can configure and chain.

```js
WhisperStorylet("bridge_smalltalk_01")
	.TagsAddArray(["bridge", "npc:captain", "mood:neutral"])
	.SetWeight(2)
	.SetCooldown(8)
	.SetAvoidImmediateRepeat(true)
	.SetPredicate(function(_ctx) {
		// Only valid when we're actually on the bridge
		return _ctx.location == "bridge";
	})
	.TextAdd("Keep it steady out there.")
	.TextAdd("All systems nominal. For now.")
	.AddToPool("npc_bridge");
```

A few important knobs:

* `SetPredicate(fn)` -> the "is this allowed right now?" function
* `SetCooldown(x)` -> minimum time between uses (uses the same units as `_now`)
* `SetOnce()` / `SetMaxUses(x)` -> limit total uses
* `SetMaxUsesPerRun(x)` -> limit uses per run (more on runs below)
* `SetAvoidImmediateRepeat(true)` -> pool won't immediately repeat it if it was the last pick

### 2. Per-run limits (roguelikes, chapters, runs, etc)

Whisper tracks a "run id" so storylets can have per-run caps.

At the start of a new run/session:

```js
WhisperNewRun();
```

Then on a storylet:

```js
WhisperStorylet("bridge_hint_once_per_run")
	.SetMaxUsesPerRun(1)
	.TextAdd("If you're stuck, check the map.")
	.AddToPool("npc_bridge");
```

This is a nice middle ground between "only once ever" and "spam forever".

### 3. Global pickers vs pool pickers

You can pick from:

* A specific pool: `WhisperPoolPick...`
* The global storylet list: `WhisperPick...`

If you want "anything in the whole game that matches this situation", global pickers are useful:

```js
var _ctx = WhisperContextMinimal(player_id, "bridge");
var _s = WhisperPickAndFire(_ctx);

if (!is_undefined(_s)) {
	var _out = _s.TextResolve();
	ShowDialogue(_out.text);
}
```

Most projects will mostly use pools (because pools keep content scoped and predictable), but global picking is there when you want it.

### 4. Time and cooldowns

All the advanced pick functions let you pass `_now`. By default, the beginner helpers use:

```js
WhisperNow(); // seconds since game start
```

If your project has its own time system (turn count, in-game clock, whatever), you can pass that instead. The only rule is:

* whatever you pass as `_now`, your cooldown values should be in the same unit.

If you want Whisper's default helpers to run on a manual "tick" clock (turns, steps, whatever), enable manual ticking:

```js
WhisperTickManual(true);

// When your game advances one tick:
WhisperTick();
```

While manual ticking is enabled, `WhisperNow()` returns the current tick counter and does not advance unless you call `WhisperTick()`.

### 5. Verbs and insertions (power features)

Whisper can:

* Replace insertions inside text (like player names, item names, etc)
* Emit verb events while text is being shown (or when it completes)

This is big enough that it has its own page:

* [Verbs & Insertions]({% link whisper/verbs_insertions.md %})

But here's the short version so you know where it fits:

```js
WhisperInsertAdd("player_name", "Drew");

WhisperStorylet("bridge_greeting")
	.TextAdd("Hey, ##player_name##.")
	.AddToPool("npc_bridge");
```

If you resolve that storylet, the text comes out with the insertion applied.

---

## Practical patterns (real games do this stuff)

### Pattern A: NPC barks that respect the room

* One pool per location, or per speaker, or both
* A tiny context struct with `location`
* Optional tags for mood/state

```js
var _ctx = WhisperContextMinimal(player_id, room_get_name(room));
var _text = WhisperSayTextSimple("npc_" + room_get_name(room), _ctx, "en", "");
if (_text != "") {
	ShowDialogue(_text);
}
```

### Pattern B: Hints that do not spam

* `SetCooldown`
* `SetMaxUsesPerRun`
* Optional "avoid repeat"

```js
WhisperStorylet("hint_inventory")
	.SetCooldown(20)
	.SetMaxUsesPerRun(2)
	.SetPredicate(function(_ctx) { return _ctx.story.hint_mode; })
	.TextAdd("Try checking your inventory.")
	.AddToPool("hints");
```

### Pattern C: "I need to know why nothing matched"

That's what the debug helpers are for:

* `WhisperDebugMatch`
* `WhisperDebugQuery`
* `WhisperPoolDebugQuery`

Those are covered here:

* [Integration & Debugging]({% link whisper/integration_debugging.md %})

---

## Where next?

If you have basic barks working, the usual "next step" is:

1. Add tags and use `WhisperSayTaggedSimple` for quick situational solutions.
2. Start writing a couple of real predicates (`SetPredicate`)
3. Add cooldowns and usage limits so your content feels intentional
4. Learn verbs/insertions when you want text to *do* things
