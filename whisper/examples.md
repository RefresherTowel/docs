---
layout: default
title: Examples
parent: Whisper
nav_order: 6
---

<!--
/// examples.md - Changelog:
/// - 25-01-2026: Document manual tick time option.
-->

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
{: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Examples

This page is a little recipe book. It's to show patterns that feel like they belong in an actual game, and that you can lift into your project to easily get started.

We'll start dead simple, then gradually add the stuff that makes Whisper shine: context, tags, cooldowns, per-run limits, and (finally) verbs + insertions.

One note before we start: I'm going to assume you have some kind of dialogue UI function. I'll call it `Dialogue_Show(text)` and move on with our lives.

---

## Example 1: Ambient barks in a town square (basic)

You're in a town square. The player walks through. Every so often, you want a quick line from a nearby NPC so the place doesn't feel like a cardboard set.

Setup (run once at startup):

```js
WhisperLineSimple("town_square_barks", "Fresh bread! Still warm!", "vendor");
WhisperLineSimple("town_square_barks", "Keep moving, please. You're blocking the stall.", "vendor");
WhisperLineSimple("town_square_barks", "If you hear the bells, get under cover.", "guard");
WhisperLineSimple("town_square_barks", "The fountain's been acting up again. Weird noise at night.", "gossip");
```

Runtime (called when you decide a bark should happen):

```js
var _ctx = WhisperContextMinimal(obj_player, "town_square");
var _text = WhisperSayTextSimple("town_square_barks", _ctx, "en", "");

if (_text != "") {
	Dialogue_Show(_text);
}
```

Now you can keep easily adding new barks as you think of them forever and you never have to touch the selection logic again.

---

## Example 2: Same pool, different mood (basic -> intermediate)

Now you want the town square to feel different depending on what's going on. Not a whole new system. Just "people are tense right now" versus "people are relaxed".

Give the storylets some mood tags:

```js
WhisperLineSimple("town_square_barks", "Nice day for it, yeah?", ["smalltalk", "mood:calm"]);
WhisperLineSimple("town_square_barks", "You feel that? Something's off.", ["smalltalk", "mood:tense"]);
WhisperLineSimple("town_square_barks", "They're saying the road's not safe anymore.", ["gossip", "mood:tense"]);
WhisperLineSimple("town_square_barks", "Heard the caravans are running again. Finally.", ["gossip", "mood:calm"]);
```

At runtime, if you just want "pick anything that matches at least one of these tags", the quick helper is `WhisperSayTaggedSimple`:

```js
var _ctx = WhisperContextMinimal(obj_player, "town_square");

var _tense = global.threat_level >= 2;
var _want_tags = _tense ? ["mood:tense"] : ["mood:calm"];

var _out = WhisperSayTaggedSimple("town_square_barks", _want_tags, _ctx);
if (!is_undefined(_out)) {
	Dialogue_Show(_out.text);
}
```

This is a small change, but it makes the world react without turning your bark code into a full on state machine.

---

## Example 3: A hint system that doesn't spam (intermediate)

Hints are useful. Hints that repeat every five seconds are the fastest way to make players hate you.

This example does three things: only provides hints when hint mode is on, has cooldowns so the same hint doesn't spam, and caps usage per run so hints don't dominate a whole play session.

> By default, Whisper's cooldowns "tick" in seconds. You can take manual control of the tick by setting `WhisperTickManual(true)` and then calling `WhisperTick(_dt)` whenever you want time to advance (for turn-based systems, `WhisperTick(1)` is common). If you want the manual tick to start from 0, call `WhisperTickReset()` after enabling manual ticking.
{: .note}

Setup:

```js
WhisperStorylet("hint_map")
	.SetWeight(2)
	.SetCooldown(20)
	.SetMaxUsesPerRun(2)
	.SetPredicate(function(_ctx) {
		return _ctx.story.hints_enabled;
	})
	.AddText("If you're lost, open the map and look for the lit paths.")
	.AddToPool("hints");

WhisperStorylet("hint_inventory")
	.SetWeight(2)
	.SetCooldown(30)
	.SetMaxUsesPerRun(2)
	.SetPredicate(function(_ctx) {
		return _ctx.story.hints_enabled;
	})
	.AddText("Some items have passive effects. Check your inventory details.")
	.AddToPool("hints");

WhisperStorylet("hint_dodge")
	.SetWeight(1)
	.SetCooldown(45)
	.SetMaxUsesPerRun(1)
	.SetPredicate(function(_ctx) {
		return _ctx.story.hints_enabled && _ctx.story.player_is_in_combat;
	})
	.AddText("Dodging costs stamina. Don't mash it, time it.")
	.AddToPool("hints");
```

When you start a new run/session (however you define it), reset per-run usage:

```js
WhisperNewRun();
```

Runtime:

```js
var _ctx = WhisperContextSimple(obj_player, room_get_name(room), global.story);
var _text = WhisperSayTextSimple("hints", _ctx, "en", "");

if (_text != "") {
	Dialogue_Show(_text);
}
```

The big win here is you didn't write a single "have we shown hint X recently" variable. Whisper did the bookkeeping.

---

## Example 4: A reactive encounter that only exists until you solve it (advanced)

This is the sort of thing that usually becomes a mess in if-land.

You're exploring a sewer area. There's a loose grate you can pry open. You want a storylet that keeps nudging the player toward it, but once they open it, the nudges should stop forever.

Setup:

```js
WhisperStorylet("sewer_grate_nudge")
	.SetWeight(3)
	.SetCooldown(25)
	.SetAvoidImmediateRepeat(true)
	.SetPredicate(function(_ctx) {
		// This is the important part: the nudge only exists while unresolved.
		return (_ctx.location == "sewers") && (!_ctx.story.sewer_grate_opened);
	})
	.AddText("A cold draft slips through the bars of a loose grate nearby.")
	.AddText("You hear metal creak. Something in here isn't secured properly.")
	.AddToPool("sewer_ambient");
```

Runtime:

```js
var _ctx = WhisperContextSimple(obj_player, "sewers", global.story);
var _text = WhisperSayTextSimple("sewer_ambient", _ctx, "en", "");

if (_text != "") {
	Dialogue_Show(_text);
}
```

Then when the player finally opens the grate in gameplay code:

```js
global.story.sewer_grate_opened = true;
```

And that's it. The predicate blocks it forever after that, without you having to delete storylets or remember to flip five different flags.

---

## Example 5: One conversation, multiple "beats" without repeating yourself (advanced)

Let's say the player talks to a tired engineer on the bridge. You want the conversation to feel like it progresses, but you don't want a strict tree. You just want beats that unlock as the chat goes on.

We'll treat "one conversation" as one run, so we can do per-run limits cleanly.

At the start of the conversation:

```js
WhisperNewRun();
```

Setup:

```js
WhisperStorylet("eng_greeting")
	.SetMaxUsesPerRun(1)
	.SetWeight(10)
	.AddText("Yeah? Make it quick. I'm in the middle of recalibrating the stabilisers.")
	.AddToPool("eng_chat");

WhisperStorylet("eng_problem")
	.SetMaxUsesPerRun(1)
	.SetWeight(6)
	.SetPredicate(function(_ctx) {
		return _ctx.story.chat_count >= 1;
	})
	.AddText("The port thrusters keep drifting. It's not dangerous, it's just... annoying.")
	.AddToPool("eng_chat");

WhisperStorylet("eng_soft_reveal")
	.SetMaxUsesPerRun(1)
	.SetWeight(4)
	.SetPredicate(function(_ctx) {
		return _ctx.story.chat_count >= 2;
	})
	.AddText("Look, between you and me? This ship's held together with optimism and cable ties.")
	.AddToPool("eng_chat");
```

Runtime (each time the player asks "Talk"):

```js
var _ctx = WhisperContextSimple(obj_player, "bridge", global.story);

var _out = WhisperSaySimple("eng_chat", _ctx);
if (!is_undefined(_out)) {
	Dialogue_Show(_out.text);
	global.story.chat_count += 1;
}
```

What this gives you is a conversation that feels like it moves forward, but stays flexible. And because of the per-run limits, you won't get the same beat twice in the same conversation. (I am slightly cheating by using `story.chat_count` as a simple progression counter.)

---

## Example 6: Insertions for dynamic names and places (advanced, but friendly)

Insertions are for templated text. This is the "don't hardcode the player's name in 40 separate strings" feature.

Setup:

```js
WhisperInsertSetList("player_name", ["Morgan", "Alex", "Sam"]);
WhisperInsertSetList("district", ["Old Dock", "Glassway", "Lower Market"]);
```

Use them in storylets:

```js
WhisperStorylet("guard_greeting")
	.SetWeight(3)
	.AddText("Evening, ##player_name##. Keep your coin close in ##district##.")
	.AddToPool("city_guard");
```

Runtime:

```js
var _ctx = WhisperContextMinimal(obj_player, "city");
var _text = WhisperSayTextSimple("city_guard", _ctx, "en", "");

if (_text != "") {
	Dialogue_Show(_text);
}
```

If you want insertions to reflect the actual player name, just set it from your save data instead of a random list. The feature doesn't care where the values came from.

---

## Example 7: Verbs for timed SFX during typewriter text (advanced)

This is the "ok, now Whisper is doing something cool" moment.

Scenario: you have a dialogue UI with a typewriter effect. You want a small beep when the radio kicks in, right in the middle of the line, without splitting the line into chunks.

Register the verb:

```js
WhisperAddVerb("radio_beep", function(_ctx, _ev) {
	audio_play_sound(snd_radio_beep, 1, false);
});
```

Write a line with an inline verb marker:

```js
WhisperStorylet("radio_message_1")
	.SetMaxUsesPerRun(1)
	.AddText("... ##player_name##? #?radio_beep## Come in. Are you there?")
	.AddToPool("radio");
```

When you pick it:

```js
var _ctx = WhisperContextSimple(obj_player, "anywhere", global.story);
var _say = WhisperSaySimple("radio", _ctx);

if (!is_undefined(_say)) {
	Dialogue_StartTypewriter(_say.text);

	// Store _say.events somewhere in your dialogue UI state.
	global.dialogue_events = _say.events;
	global.dialogue_ctx = _ctx;
	global.dialogue_cursor = -1;
}
```

Then inside your typewriter step logic:

```js
var _old = global.dialogue_cursor;
global.dialogue_cursor = min(global.dialogue_cursor + 1, string_length(Dialogue_GetFullText()));

// This fires any verb events we crossed this tick.
WhisperVerbRunRange(global.dialogue_events, _old, global.dialogue_cursor, global.dialogue_ctx);
```

And that's the whole trick. Whisper isn't running your dialogue UI. It's just giving you a clean, reliable way to attach timed events to a single line of text.

---

## Example 8: When nothing matches, use debug instead of guessing (advanced sanity saver)

This isn't a gameplay example, but it is a real dev workflow example.

If you expected a pool to produce something and it returned `undefined`, don't guess. Ask Whisper.

```js
var _ctx = WhisperContextSimple(obj_player, "sewers", global.story);
var _rows = WhisperPoolDebugQuery("sewer_ambient", _ctx);

for (var i = 0; i < array_length(_rows); i++) {
	var _r = _rows[i];

	if (!_r.ok) {
		show_debug_message("BLOCKED: " + string(_r.id));
		for (var j = 0; j < array_length(_r.reasons); j++) {
			show_debug_message("  - " + string(_r.reasons[j]));
		}
	}
}
```

This will usually reveal something obvious, like "predicate failed" or "cooldown is active", and you'll fix it in two minutes instead of wandering around your codebase for an hour.
