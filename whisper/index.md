---
layout: default
title: Whisper
nav_order: 6
has_children: true
---

<!--
/// whisper/index.md - Changelog:
/// - 25-01-2026: Initial Whisper docs draft.
-->

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

![Whisper icon](../assets/whisper_icon.png)
{: .text-center}

*Small story bits, picked at the right moment.*
{: .text-center}

Ever had your dialogue slowly turn into a giant mess of: "if the player did X but not Y unless this line fired in the last 20 seconds but only if we are in the tavern and please don't repeat the same line twice in a row"?

Whisper exists to take that whole vibe and make it feel like you are writing content again, not building a spaghetti-powered slot machine.

**Whisper** is a storylet engine for GameMaker.

If you have never seen the word "storylet" before, don't stress. It isn't a fancy new genre. It's just a useful way to think about content.

---

## What Whisper is

A **storylet** is a small piece of content that can be chosen when its rules say it is allowed.

That is it.

In practice, a storylet is usually:

* A bark ("I hate this place.")
* A line in a conversation track
* A little encounter ("You spot something shiny on the ground.")
* A narration beat ("The wind shifts. Something is off.")
* A gameplay micro-event ("A trader approaches you.")

Each storylet has stuff like:

* A **pool** (which is basically a category / track)
* Some **tags** (words you can filter by)
* A **weight** (how often it should show up compared to others)
* Optional limits like **cooldowns** and **max uses**
* Optional rules (a function that returns true/false)

Then you ask Whisper:

"Hey, give me a line from pool X for the current situation."

Whisper checks the rules, filters, cooldowns, usage limits, etc, and then picks one.

---

## The core idea

You will see these three concepts everywhere:

### 1) Storylets

The content units. Each one is a little "candidate" that might be allowed to fire.

### 2) Pools

Groups of storylets. Think "track" more than "container".

Examples:

* `"npc_blacksmith_barks"`
* `"town_gossip"`
* `"combat_taunts"`
* `"loot_find"`

You usually pick from a pool, not from "everything in the entire game".

### 3) Context

A struct you pass in that represents "what is going on right now".

This is how you give Whisper the information it needs, without Whisper knowing anything about your game.

---

## The 30 second API

If you only learn these first, you can already ship something:

* `WhisperLineSimple(pool_id, text, [tags], [weight], [once_only])`
* `WhisperSayTextSimple(pool_id, [ctx], [lang], [fallback_text])`

Minimal example:

```js
// Add a few barks to a pool (track)
WhisperLineSimple("npc_blacksmith_barks", "Need something sharpened?", "friendly", 1);
WhisperLineSimple("npc_blacksmith_barks", "If it breaks, you bought it.", "grumpy", 1);
WhisperLineSimple("npc_blacksmith_barks", "No refunds.", "grumpy", 2);

// Ask for a random line (with a fallback)
var _text = WhisperSayTextSimple("npc_blacksmith_barks", {}, "en", "...");
show_debug_message(_text);
```

That alone gives you:

* Weighted picking
* Per-line "fire once" if you want it
* A clean place to add tags later
* A pool you can keep growing without rewriting logic

---

## What Whisper gives you

### Basic value (most people start with just this stuff)

* **Pick lines from pools**
  Keep content grouped by where it is used.

* **Tags for simple filtering**
  "Give me any line tagged 'combat' but not 'tutorial'."

* **Weights**
  Some lines should be rare. Some should be common. You decide.

* **Once-only and cooldowns**
  No more manually tracking "did we already say this today".

* **Multiple text variations**
  One storylet can have multiple variants, so it doesn't feel repetitive.

### Advanced value (when you're starting to need more complexity)

* **Per-run usage limits**
  You can say "this can fire twice per run" and then define what a "run" means for your game.

* **Prefer tags (soft bias)**
  Not a hard filter, just a nudge. "Prefer lines tagged 'sad' right now."

* **Debug query**
  Ask Whisper "why didn't this match?" and get a breakdown.

* **Inline verbs (events inside text)**
  Put tiny markers in your text that trigger code while the line is being revealed.

* **Insertions (template replacements)**
  Write `"Hello ##PLAYER_NAME##"` and have Whisper fill it in (with per-language variants if you want).

---

## Quick Start

This version shows the normal "shape" of Whisper usage.

1. Create some lines.
2. Build a context.
3. Say something.

```js
// Step 1: Define content somewhere (Create event, script init, etc)
WhisperLineSimple("town_gossip", "Did you hear about the old well?", ["town", "gossip"], 1);
WhisperLineSimple("town_gossip", "Someone saw lights in the forest again.", ["town", "gossip"], 1);
WhisperLineSimple("town_gossip", "The mayor's acting weird lately.", ["town", "gossip"], 0.5);

// Step 2: Build context for "right now"
// (You can put anything you want in here, Whisper just passes it through)
var _ctx = {
	subject: obj_player,	// could be an instance id, or a struct, or anything
	location: "town_square",
	story: {
		chapter: 2,
		has_seen_well: false
	}
};

// Step 3: Ask Whisper for a line
var _line = WhisperSayTextSimple("town_gossip", _ctx, "en", "...");
```

At this point you're ready for the next step: adding rules.

---

## A tiny taste of rules

Rules are where storylets stop being "random lines" and start being "picked at the right time".

Example: only allow this line if the player hasn't seen the well yet.

```js
WhisperStorylet("gossip_well_hint")
	.AddToPool("town_gossip")
	.TagsAddArray(["town", "gossip"])
	.TextAdd("Did you hear about the old well?")
	.SetPredicate(function(_ctx) {
		return !_ctx.story.has_seen_well;
	});
```

> A predicate is simply a function that returns true or false. `SetPredicate` takes such function. That function returns `true` if the storylet is allowed, `false` if it isn't. `_ctx` is whatever you passed in when you picked.
{: .note}

---

## Verbs and insertions

Whisper supports two kinds of text markup:

### Insertions: "fill this bit in"

Format: `##KEY##`

Example:

```js
WhisperInsertAdd("PLAYER_NAME", "Drew", "en");
WhisperLineSimple("npc_greeter", "Hey, ##PLAYER_NAME##!", "greeting", 1);

var _text = WhisperSayTextSimple("npc_greeter", {}, "en", "...");
```

You can add multiple variants for the same key, and Whisper will pick one. This lets you run the same line of dialogue, but keep it fresh with minor, randomly picked changes.

### Verbs: "trigger code here"

Format: `#?verb_name##` (it looks weird because it's designed to be easy to scan in plain text)

You register verbs like this:

```js
WhisperVerbAdd("SFX_BELL", function(_ctx, _event) {
	// play a sound, spawn VFX, advance a quest, whatever
});
```

Then use it inside text:

```js
WhisperLineSimple("intro", "Welcome! #?SFX_BELL## Let's begin.", "intro", 1);
```

When you resolve a line, Whisper gives you back:

* `text` (with markers removed)
* `events` (a list of verb events with positions in the text)

That means you can do typewriter text and fire verbs as the cursor reaches them.

Don't worry if that sentence sounded like gobbledegook. The "Verbs + Insertions" page walks it step by step.

---

## Where to go next

If you are brand new to storylets:

* Start with **Concepts**: what storylets are, what pools are, and what "pick vs fire" actually means.

If you want to get something working fast:

* Go to **Usage**: the basic workflow (lines -> pools -> context -> say) and then the step up into real storylets.

If you want the text features:

* **Verbs + Insertions**: template replacements and timed events inside text (typewriter-friendly).

If you want help wiring it into a real project (and fixing "why is nothing matching"):

* **Integration + Debugging**: setup patterns, common mistakes, and the debug tools.

If you want the full list of functions:

* **Reference**: everything in alphabetical order, with examples.

