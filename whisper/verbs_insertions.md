---
layout: default
title: Verbs & Insertions
parent: Whisper
nav_order: 3
---

<!--
/// verbs_insertions.md - Changelog:
/// - 25-01-2026: Initial page.
-->

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
{: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Verbs & Insertions

Verbs and insertions are a good way to make Whisper feel "alive".

* **Insertions** let you write templated text like `Hello, ##name##!` and have Whisper fill it in.
* **Verbs** let your text *cause things to happen* at specific points while it is being revealed.

If you are brand new to storylets, do not worry. You can ignore verbs completely at first and still use Whisper fine. Insertions are the most beginner-friendly "power feature", so we will start there.

---

## Insertions

Insertions are a simple text replacement system:

In your text, you write `##key##`. At resolve time, Whisper replaces it with a random value for that key (and language). If the key is not defined, it becomes an empty string (and you can enable debug warnings to inform you if you are trying to access an undefined insertion).

Whisper uses these markers:

* Insertions: `##key##`
* Verbs: `#?verb_name##` (more on that below)

Yes, both end in `##`. The difference is the *start* marker: `##` vs `#?`.

### Beginner: defining and using an insertion

Define one or more variants for a key:

```js
WhisperAddInsert("name", "Captain");
WhisperAddInsert("name", "Chief");
WhisperAddInsert("name", "Boss");
```

Use it in any line:

```js
WhisperLineSimple("npc_bridge", "Hey, ##name##.");
```

When you later resolve text (for example via `WhisperSaySimple`), you might get:

* "Hey, Captain."
* "Hey, Boss."
* etc.

### Replacing the whole list at once

If you want to set a list in one hit (handy for loading from JSON or a spreadsheet export):

```js
WhisperInsertSetList("name", ["Captain", "Chief", "Boss"]);
```

### Language support and fallback

Insertions are stored per language. If you resolve in a language that does not exist for that key, Whisper falls back to `"en"`.

```js
WhisperAddInsert("name", "Captain", "en");
WhisperAddInsert("name", "Capitaine", "fr");
```

### Advanced: insertions inside insertions

Insertion values can themselves contain insertion markers, and Whisper will resolve them (recursively) up to a limit.

Example:

```js
WhisperAddInsert("ship", "The ##ship_class## Horizon");
WhisperAddInsert("ship_class", "Scout");
WhisperAddInsert("ship_class", "Freighter");
```

If you use `##ship##`, Whisper might produce:

* "The Scout Horizon"
* "The Freighter Horizon"

Important: there is a recursion depth cap (currently 10) so you cannot accidentally infinite-loop your game by doing `a -> ##a##` forever. If you hit the cap and `WHISPER_DEBUG` is enabled, Whisper will warn.

> Best practice: avoid self-referential insertions (directly or indirectly). Keep insertion chains short.
{: .note}

### Very important limitation: do not put verb markers inside insertions

Insertions are resolved after Whisper has already parsed verb markers out of the template text.

So if an insertion value contains `#?some_verb##`, it will stay as literal text and it will not generate an event.

If you want a verb, put the verb marker in the main template, not inside the insertion value.

---

## Verbs

A "verb" is just a named callback you register:

```js
WhisperAddVerb("give_xp", function(_ctx, _ev) {
	// do something
});
```

> GameMaker callbacks are not closures. Do not rely on local variables from outside the callback (they will not exist later). If a callback needs values or an instance/struct scope, carry them explicitly (for example via `_ctx`), or bind scope with `method(scope_struct_or_instance, function(...) { ... })`.
{: .note}

Then you reference that verb name from text, and Whisper turns it into an event in the resolved result.

A resolved line can include an `events` array where each event looks like:

* `name`     -> the verb name
* `position` -> where it should fire (0-based character index in the final resolved text)
* `trigger`  -> when it should fire ("on_reach" or "on_complete")
* `meta.args` -> optional args parsed from the marker

You will most commonly see verbs used in two ways:

1. **Inline verbs**: fire mid-line as the cursor reaches a point (great for typewriter text, SFX, UI beats).
2. **Completion verbs**: fire when the line finishes (great for "apply effect after the line is shown").

---

## Beginner: completion verbs (fire at the end)

When you add text to a storylet, you can supply a completion verb:

```js
var _s = WhisperStorylet("bridge_reward_1");

_s.AddText("Nice work out there.", "give_xp");
```

That creates an event with `trigger = "on_complete"` positioned at the end of the resolved text.

Define the verb callback:

```js
WhisperAddVerb("give_xp", function(_ctx, _ev) {
	if (!is_struct(_ctx)) return;
	if (!struct_exists(_ctx, "xp")) _ctx.xp = 0;
	_ctx.xp += 10;
});
```

How do you actually run it? You call `WhisperVerbRunRange` when your line is revealed (see the next section). If you reveal the whole line instantly, you can just run the full range once:

```js
// _result is { id, text, events, data } from WhisperSaySimple / TextResolve
WhisperVerbRunRange(_result.events, -1, string_length(_result.text), _ctx);
```

---

## Intermediate: inline verbs (fire mid-line)

Inline verbs are written directly inside the text, using this format:

* `#?verb_name##`
* `#?verb_name:arg1,arg2##`

Example:

```js
WhisperLineSimple(
	"npc_bridge",
	"Ok. #?beep## Now we can talk.",
	"bridge"
);
```

When Whisper parses this, it removes the marker from the visible text, and adds an event:

* `trigger = "on_reach"`
* `position = (the character index where the marker was)`

So if you are doing a typewriter reveal, you can fire verbs as the cursor advances.

### Running verbs as text reveals

Whisper does not run verbs automatically, because it has no idea how you are presenting text.

Instead, you do this:

* Keep track of the previous reveal position.
* Each step, call `WhisperVerbRunRange(events, old_pos, new_pos, ctx)`.

Example (simple typewriter controller logic):

```js
// Create
say = WhisperSaySimple("npc_bridge", ctx);
cursor = -1;

// Step
if (!is_undefined(say)) {
	var _old = cursor;
	cursor = min(cursor + 1, string_length(say.text));

	WhisperVerbRunRange(say.events, _old, cursor, ctx);

	if (cursor >= string_length(say.text)) {
		// Line is complete. Completion verbs will fire as you cross their position.
	}
}
```

Important note: `WhisperVerbRunRange` does not remember what it fired.
If you call it with the same range twice, it can fire the same events twice.

That is not a bug. It is intentional. It keeps the function simple and lets you decide what "already fired" means in your UI.

> Best practice: store a cursor (or last fired position) per line and only advance it forward.
> {: .note}

### Passing args to inline verbs

Inline markers can include `:arg1,arg2` after the name:

```js
"Warning. #?shake:0.25,6## Incoming!"
```

Whisper parses each token:

* If converting to a number and back to a string matches exactly, it becomes a number.
* Otherwise it stays a string.

Inside the callback, read them from `meta.args`:

```js
WhisperAddVerb("shake", function(_ctx, _ev) {
	var _args = _ev.meta.args;
	var _time = (array_length(_args) > 0) ? _args[0] : 0.2;
	var _pow  = (array_length(_args) > 1) ? _args[1] : 4;

	// do screen shake using _time and _pow
});
```

---

## Advanced: programmatic markers, and "only if registered"

Sometimes you are building text in code and you want to inject a verb marker only if it exists.

* `WhisperVerbInsert(name)` returns the marker string only if the verb is registered, otherwise it returns `""`.

If you want to always inject a marker string, embed `#?name##` directly in your text (or build it manually with `WHISPER_VERB_BEGIN` + name + `WHISPER_VERB_END`).

Example:

```js
var _maybe = WhisperVerbInsert("play_sfx");

WhisperLineSimple(
	"npc_bridge",
	"Door opens. " + _maybe,
	"bridge"
);
```

---

## How insertions and verbs interact (this matters)

When Whisper resolves insertions, it may change the length of the final text.
That would normally break verb positions.

Whisper handles this for you:

* It resolves insertions.
* It remaps event positions so they still point at the right place in the final text.

So you can safely mix them:

```js
WhisperInsertSetList("name", ["Captain", "Chief", "Boss"]);

WhisperLineSimple(
	"npc_bridge",
	"Hey, ##name##. #?beep## All good?",
	"bridge"
);
```

The inline verb will still fire at the right moment, even though "##name##" changes length.

---

## Quick cheat sheet

* Insertions:

  * Define: `WhisperAddInsert(key, value, [lang])`
  * Define list: `WhisperInsertSetList(key, array, [lang])`
  * Use in text: `##key##`

* Verbs:

  * Define: `WhisperAddVerb(name, callback)`
  * Inline in text: `#?name##` or `#?name:arg1,arg2##`
  * Run while revealing: `WhisperVerbRunRange(events, from_pos, to_pos, ctx)`
  * Marker helper: `WhisperVerbInsert(name)`
