---
layout: default
title: Scripting Reference
parent: Whisper
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

# Scripting Reference

This page documents the public Whisper API.

Everything here is listed in alphabetical order so you can Cmd+F your way to victory.

<!--
/// references.md - Changelog:
/// - 25-01-2026: Add manual tick functions (WhisperTick/WhisperTickManual).
-->

---

## Public API (Alphabetical)

### `WhisperContextMinimal(_subject, _location)`

Create a minimal context with subject + location only.

**Arguments**

* `_subject` `Any` Main subject (player, NPC, etc.).
* `_location` `Any` Location identifier.

**Returns**: `Struct`

---

### `WhisperContextSimple(_subject, _location, _story = undefined)`

Create a simple Whisper context struct (subject/location/story fields).

**Arguments**

* `_subject` `Any` Main subject (player, NPC, etc.).
* `_location` `Any` Location identifier.
* `[_story]` `Struct,Undefined` Optional story/state struct.

**Returns**: `Struct`

---

### `WhisperDebugMatch(_storylet, _ctx = undefined, _now = undefined, _filter = undefined)`

Debug a single storylet match (returns reasons for failure/success).

**Arguments**

* `_storylet` `Struct.__WhisperStorylet,Any` Storylet struct or storylet id.
* `[_ctx]` `Struct,Undefined` Context struct passed to predicates and hooks.
* `[_now]` `Real,Undefined` Time value used for cooldown checks.
* `[_filter]` `Struct,Undefined` Filter struct ({ tags_all, tags_any, tags_not, tags_prefer, prefer_weight, custom }).

**Returns**: `Struct`

---

### `WhisperDebugQuery(_ctx = undefined, _now = undefined, _filter = undefined)`

Debug a global query (returns details about candidates and why they matched/failed).

**Arguments**

* `[_ctx]` `Struct,Undefined` Context struct passed to predicates and hooks.
* `[_now]` `Real,Undefined` Time value used for cooldown checks.
* `[_filter]` `Struct,Undefined` Filter struct ({ tags_all, tags_any, tags_not, tags_prefer, prefer_weight, custom }).

**Returns**: `Struct`

---

### `WhisperFilter()`

Convenience builder for Whisper filter structs.

**Arguments**

* None.

**Returns**: `Struct`

* **Additional details:**

  * This returns a plain struct with fields Whisper understands:

    * `tags_all`: array of tags the storylet must have all of
    * `tags_any`: array of tags the storylet must have at least one of
    * `tags_not`: array of tags the storylet must not have
    * `tags_prefer`: array of tags to prefer when choosing (soft preference)
    * `prefer_weight`: optional weight multiplier when a preferred tag matches
    * `custom`: optional function `function(_storylet, _ctx) -> Bool` for custom filtering

---

### `WhisperGetRunId()`

Get the current run/session id.

**Arguments**

* None.

**Returns**: `Real`

---

### `WhisperInsertAdd(_key, _value, _lang = "en")`

Register an insertion value for a key.

**Arguments**

* `_key` `String` Insertion key (no brackets).
* `_value` `String` Replacement text.
* `[_lang]` `String` Language code.

**Returns**: `Real` (ignored)

---

### `WhisperInsertResolve(_key, _lang = "en")`

Resolve a single insertion key for a given language.

**Arguments**

* `_key` `String` Insertion key.
* `[_lang]` `String` Language code.

**Returns**: `String,Undefined`

---

### `WhisperInsertSetList(_key, _array, _lang = "en")`

Register an insertion list for a key, used for random selection.

**Arguments**

* `_key` `String` Insertion key.
* `_array` `Array<String>` List of possible replacement strings.
* `[_lang]` `String` Language code.

**Returns**: `Real` (ignored)

---

### `WhisperLineExplicit( _pool_id, _storylet_id, _text, _tags = undefined, _weight = 1, _once_only = false )`

Create a storylet with an explicit id and add it to a pool (track).

**Arguments**

* `_pool_id` `Any` Pool / track identifier (e.g. "npc_bridge").
* `_storylet_id` `Any` Storylet identifier (e.g. "npc_bridge_hello_1").
* `_text` `String` Text for this line (may include verbs and inserts).
* `_tags` `Array<String>,String,Undefined` Tags for filtering (array or single string).
* `_weight` `Real,Undefined` Relative selection weight (> 0).
* `_once_only` `Bool,Undefined` If true, this line can fire only once ever.

**Returns**: `Struct.__WhisperStorylet`

---

### `WhisperLineSimple( _pool_id, _text, _tags = undefined, _weight = 1, _once_only = false )`

Create a simple storylet and add it to a pool (track), with an auto generated id.

**Arguments**

* `_pool_id` `Any` Pool / track identifier (e.g. "npc_bridge").
* `_text` `String` Text for this line (may include verbs and inserts).
* `_tags` `Array<String>,String,Undefined` Tags for filtering (array or single string).
* `_weight` `Real,Undefined` Relative selection weight (> 0).
* `_once_only` `Bool,Undefined` If true, this line can fire only once ever.

**Returns**: `Struct.__WhisperStorylet`

---

### `WhisperNewRun()`

Start a new run/session. This resets per-run usage tracking.

This also clears pool repeat-suppression state (the last picked storylet), so a new run does not remember previous picks.

**Arguments**

* None.

**Returns**: `Real` (ignored)

---

### `WhisperNow()`

Simple time helper for Whisper cooldowns and usage.

By default, this returns seconds since game start. If manual ticking is enabled via `WhisperTickManual(true)`, this returns the current manual tick counter.

**Arguments**

* None.

**Returns**: `Real`

---

### `WhisperPick(_ctx = undefined, _now = undefined, _filter = undefined)`

Pick a storylet from the global storylet list (does not fire it).

**Arguments**

* `[_ctx]` `Struct,Undefined` Context struct passed to predicates and hooks.
* `[_now]` `Real,Undefined` Time value used for cooldown checks.
* `[_filter]` `Struct,Undefined` Filter struct ({ tags_all, tags_any, tags_not, tags_prefer, prefer_weight, custom }).

**Returns**: `Struct.__WhisperStorylet,Undefined`

---

### `WhisperPickAndFire(_ctx = undefined, _now = undefined, _filter = undefined)`

Pick and immediately fire a storylet (updates usage/cooldown).

**Arguments**

* `[_ctx]` `Struct,Undefined` Context struct passed to predicates and hooks.
* `[_now]` `Real,Undefined` Time value used for cooldown checks.
* `[_filter]` `Struct,Undefined` Filter struct ({ tags_all, tags_any, tags_not, tags_prefer, prefer_weight, custom }).

**Returns**: `Struct.__WhisperStorylet,Undefined`

---

### `WhisperPickAndFireOr(_ctx = undefined, _now = undefined, _filter = undefined, _fallback_fn = undefined)`

Pick and fire a storylet or call a fallback function when nothing matches.

**Arguments**

* `[_ctx]` `Struct,Undefined` Context struct passed to predicates and hooks.
* `[_now]` `Real,Undefined` Time value used for cooldown checks.
* `[_filter]` `Struct,Undefined` Filter struct ({ tags_all, tags_any, tags_not, tags_prefer, prefer_weight, custom }).
* `_fallback_fn` `Function,Undefined` Function called when no storylet matches.

**Returns**: `Struct.__WhisperStorylet,Any,Undefined`

* **Additional details:**

  * `_fallback_fn` is only called when nothing matches. Signature: `function() -> Any`.

---

### `WhisperPickOr(_ctx = undefined, _now = undefined, _filter = undefined, _fallback_fn = undefined)`

Pick a storylet or call a fallback function when nothing matches.

**Arguments**

* `[_ctx]` `Struct,Undefined` Context struct passed to predicates and hooks.
* `[_now]` `Real,Undefined` Time value used for cooldown checks.
* `[_filter]` `Struct,Undefined` Filter struct ({ tags_all, tags_any, tags_not, tags_prefer, prefer_weight, custom }).
* `_fallback_fn` `Function,Undefined` Function called when no storylet matches.

**Returns**: `Struct.__WhisperStorylet,Any,Undefined`

* **Additional details:**

  * `_fallback_fn` is only called when nothing matches. Signature: `function() -> Any`.

---

### `WhisperPoolDebugQuery(_pool_id, _ctx = undefined, _now = undefined, _filter = undefined)`

Debug a pool query (returns details about candidates and match results).

**Arguments**

* `_pool_id` `Any` Pool identifier.
* `[_ctx]` `Struct,Undefined` Context struct passed to predicates and hooks.
* `[_now]` `Real,Undefined` Time value used for cooldown checks.
* `[_filter]` `Struct,Undefined` Filter struct ({ tags_all, tags_any, tags_not, tags_prefer, prefer_weight, custom }).

**Returns**: `Struct`

---

### `WhisperPoolPick(_pool_id, _ctx = undefined, _now = undefined, _filter = undefined)`

Pick a storylet from a pool (does not fire it).

**Arguments**

* `_pool_id` `Any` Pool identifier.
* `[_ctx]` `Struct,Undefined` Context struct passed to predicates and hooks.
* `[_now]` `Real,Undefined` Time value used for cooldown checks.
* `[_filter]` `Struct,Undefined` Filter struct ({ tags_all, tags_any, tags_not, tags_prefer, prefer_weight, custom }).

**Returns**: `Struct.__WhisperStorylet,Undefined`

---

### `WhisperPoolPickAndFire(_pool_id, _ctx = undefined, _now = undefined, _filter = undefined)`

Pick and fire a storylet from a pool (updates usage/cooldown).

**Arguments**

* `_pool_id` `Any` Pool identifier.
* `[_ctx]` `Struct,Undefined` Context struct passed to predicates and hooks.
* `[_now]` `Real,Undefined` Time value used for cooldown checks.
* `[_filter]` `Struct,Undefined` Filter struct ({ tags_all, tags_any, tags_not, tags_prefer, prefer_weight, custom }).

**Returns**: `Struct.__WhisperStorylet,Undefined`

---

### `WhisperPoolPickAndFireOr(_pool_id, _ctx = undefined, _now = undefined, _filter = undefined, _fallback_fn = undefined)`

Pick and fire a storylet from a pool or call a fallback function when nothing matches.

**Arguments**

* `_pool_id` `Any` Pool identifier.
* `[_ctx]` `Struct,Undefined` Context struct passed to predicates and hooks.
* `[_now]` `Real,Undefined` Time value used for cooldown checks.
* `[_filter]` `Struct,Undefined` Filter struct ({ tags_all, tags_any, tags_not, tags_prefer, prefer_weight, custom }).
* `_fallback_fn` `Function,Undefined` Function called when no storylet matches.

**Returns**: `Struct.__WhisperStorylet,Any,Undefined`

* **Additional details:**

  * `_fallback_fn` is only called when nothing matches. Signature: `function() -> Any`.

---

### `WhisperPoolPickOr(_pool_id, _ctx = undefined, _now = undefined, _filter = undefined, _fallback_fn = undefined)`

Pick a storylet from a pool or call a fallback function when nothing matches.

**Arguments**

* `_pool_id` `Any` Pool identifier.
* `[_ctx]` `Struct,Undefined` Context struct passed to predicates and hooks.
* `[_now]` `Real,Undefined` Time value used for cooldown checks.
* `[_filter]` `Struct,Undefined` Filter struct ({ tags_all, tags_any, tags_not, tags_prefer, prefer_weight, custom }).
* `_fallback_fn` `Function,Undefined` Function called when no storylet matches.

**Returns**: `Struct.__WhisperStorylet,Any,Undefined`

* **Additional details:**

  * `_fallback_fn` is only called when nothing matches. Signature: `function() -> Any`.

---

### `WhisperPoolQuery(_pool_id, _ctx = undefined, _now = undefined, _filter = undefined)`

Query eligible storylets inside a specific pool.

**Arguments**

* `_pool_id` `Any` Pool identifier.
* `[_ctx]` `Struct,Undefined` Context struct passed to predicates and hooks.
* `[_now]` `Real,Undefined` Time value used for cooldown checks.
* `[_filter]` `Struct,Undefined` Filter struct ({ tags_all, tags_any, tags_not, tags_prefer, prefer_weight, custom }).

**Returns**: `Array<Struct.__WhisperStorylet>`

---

### `WhisperQuery(_ctx = undefined, _now = undefined, _filter = undefined)`

Query eligible storylets using the global storylet list.

**Arguments**

* `[_ctx]` `Struct,Undefined` Context struct passed to predicates and hooks.
* `[_now]` `Real,Undefined` Time value used for cooldown checks.
* `[_filter]` `Struct,Undefined` Filter struct ({ tags_all, tags_any, tags_not, tags_prefer, prefer_weight, custom }).

**Returns**: `Array<Struct.__WhisperStorylet>`

---

### `WhisperResetAll()`

Destroy and recreate all Whisper singletons (manager, verbs, inserts).

**Arguments**

* None.

**Returns**: `Real` (ignored)

---

### `WhisperSaySimple(_pool_id, _ctx = undefined, _lang = "en")`

Pick and fire a line from a pool and resolve its text. Returns { text, events, storylet } or undefined.

**Arguments**

* `_pool_id` `Any` Pool / track identifier.
* `[_ctx]` `Struct,Undefined` Context struct (optional).
* `[_lang]` `String,Undefined` Language code.

**Returns**: `Struct,Undefined`

---

### `WhisperSayTaggedSimple( _pool_id, _tags_any, _ctx = undefined, _lang = "en" )`

Pick and fire a line from a pool using simple tag filters. Returns { text, events, storylet } or undefined.

**Arguments**

* `_pool_id` `Any` Pool / track identifier.
* `_tags_any` `Array<String>,String,Undefined` At least one of these tags must be present.
* `[_ctx]` `Struct,Undefined` Context struct (optional).
* `[_lang]` `String,Undefined` Language code.

**Returns**: `Struct,Undefined`

---

### `WhisperSayTextSimple( _pool_id, _ctx = undefined, _lang = "en", _fallback_text = undefined )`

Pick and fire a line from a pool and return only the text.

**Arguments**

* `_pool_id` `Any` Pool / track identifier.
* `[_ctx]` `Struct,Undefined` Context struct (optional).
* `[_lang]` `String,Undefined` Language code.
* `[_fallback_text]` `String,Undefined` Fallback text when no line matches.

**Returns**: `String,Undefined`

---

### `WhisperSetRunId(_id)`

Explicitly set the current run/session id.

**Arguments**

* `_id` `Real` New run identifier.

**Returns**: `Real` (ignored)

---

### `WhisperStorylet(_id)`

Public factory to create or fetch a Whisper storylet.

**Arguments**

* `_id` `Any` Storylet identifier.

**Returns**: `Struct.__WhisperStorylet`

* **Additional details:**

  * The returned struct type is named `__WhisperStorylet` in code. Even though it has `__` in the name, it is intended to be the public storylet handle you configure and fire.

**Public methods**

* #### `AddToPool(_pool_id)`: Add this storylet to the named pool.

  * **Arguments:**

    * `_pool_id` `Any` Pool identifier.
  * **Returns:** `Struct.__WhisperStorylet`
* #### `CanFire(_ctx, _now)`: Determine whether the storylet can currently fire.

  * **Arguments:**

    * `_ctx` `Struct` Context struct passed to predicate.
    * `_now` `Real` Current time value for cooldown checks.
  * **Returns:** `Bool`
* #### `DebugAvailability(_ctx, _now, _filter = undefined)`: Debug this storylet's availability given context and filters.

  * **Arguments:**

    * `_ctx` `Struct` Context struct passed to predicates.
    * `_now` `Real` Current time value for cooldowns.
    * `_filter` `Struct,Undefined` Filter struct ({ tags_all, tags_any, tags_not, tags_prefer, prefer_weight, custom }).
  * **Returns:** `Struct`
* #### `Fire(_ctx, _now)`: Fire this storylet, running on_fire and updating usage/cooldown.

  * **Arguments:**

    * `_ctx` `Struct` Context struct passed to hooks.
    * `_now` `Real` Current time value for cooldowns.
  * **Returns:** `Bool`
* #### `HasTag(_tag)`: Check whether this storylet has a given tag.

  * **Arguments:**

    * `_tag` `String` Tag to look for.
  * **Returns:** `Bool`
* #### `SetAvoidImmediateRepeat(_flag = true)`: Avoid picking this storylet twice in a row (per pool).

  * **Arguments:**

    * `[_flag]` `Bool,Undefined` Enable/disable.
  * **Returns:** `Struct.__WhisperStorylet`
* #### `SetCooldown(_cooldown)`: Set cooldown duration in seconds.

  * **Arguments:**

    * `_cooldown` `Real` Cooldown in seconds.
  * **Returns:** `Struct.__WhisperStorylet`
* #### `SetMaxUses(_max_uses)`: Set maximum total uses (ever).

  * **Arguments:**

    * `_max_uses` `Real` Max uses (>= 0).
  * **Returns:** `Struct.__WhisperStorylet`
* #### `SetMaxUsesPerRun(_max_uses)`: Set maximum uses per run/session.

  * **Arguments:**

    * `_max_uses` `Real` Max uses per run (>= 0).
  * **Returns:** `Struct.__WhisperStorylet`
* #### `SetOnAvailable(_func)`: Set hook called when the storylet is eligible during query.

  * **Arguments:**

    * `_func` `Function,Undefined` Callback signature: `function(_storylet, _ctx)`.
  * **Returns:** `Struct.__WhisperStorylet`
* #### `SetOnFire(_func)`: Set hook called when the storylet fires (after selection).

  * **Arguments:**

    * `_func` `Function,Undefined` Callback signature: `function(_storylet, _ctx)`.
  * **Returns:** `Struct.__WhisperStorylet`
* #### `SetOnResolved(_func)`: Set hook called after text is resolved.

  * **Arguments:**

    * `_func` `Function,Undefined` Callback signature: `function(_storylet, _ctx, _result)`.
  * **Returns:** `Struct.__WhisperStorylet`
* #### `SetOnSelected(_func)`: Set hook called when the storylet is selected by a pick.

  * **Arguments:**

    * `_func` `Function,Undefined` Callback signature: `function(_storylet, _ctx)`.
  * **Returns:** `Struct.__WhisperStorylet`
* #### `SetOnce()`: Convenience: set max uses to 1 (ever).

  * **Arguments:**

    * None.
  * **Returns:** `Struct.__WhisperStorylet`
* #### `SetPredicate(_func)`: Set predicate function used for custom availability rules.

  * **Arguments:**

    * `_func` `Function,Undefined` Callback signature: `function(_ctx) -> Bool`.
  * **Returns:** `Struct.__WhisperStorylet`
* #### `SetWeight(_weight)`: Set base selection weight (must be > 0).

  * **Arguments:**

    * `_weight` `Real` New base weight.
  * **Returns:** `Struct.__WhisperStorylet`
* #### `TagAdd(_tag)`: Add a tag to this storylet.

  * **Arguments:**

    * `_tag` `String` Tag to add.
  * **Returns:** `Struct.__WhisperStorylet`
* #### `TagsAddArray(_tags_array)`: Add multiple tags (skips duplicates already present).

  * **Arguments:**

    * `_tags_array` `Array<String>` Tag list to add.
  * **Returns:** `Struct.__WhisperStorylet`
* #### `TagsSet(_tags_array)`: Replace the entire tag array.

  * **Arguments:**

    * `_tags_array` `Array<String>` Tag list.
  * **Returns:** `Struct.__WhisperStorylet`
* #### `TextAdd(_string, _verb = undefined, _lang = "en")`: Add text variation to the main body.

  * **Arguments:**

    * `_string` `String` Raw template string (may contain markers).
    * `[_verb]` `String,Undefined` Verb to trigger on completion.
    * `[_lang]` `String` Language code.
  * **Returns:** `Struct.__WhisperStorylet`
* #### `TextGet(_lang = "en")`: Convenience: get just the text of a random variation.

  * **Arguments:**

    * `_lang` `String` Language code.
  * **Returns:** `String,Undefined`
* #### `TextResolve(_lang = "en")`: Resolve content to { text, events } for this storylet's body.

  * **Arguments:**

    * `_lang` `String` Language code.
  * **Returns:** `Struct,Undefined`

---

### `WhisperTick()`

Advance manual cooldown time by 1 tick (no-op unless manual ticking is enabled).

**Arguments**

* None.

**Returns**: `Real,Undefined`

---

### `WhisperTickManual(_enabled)`

Enable or disable manual ticking for `WhisperNow()`.

When enabled, cooldown time only advances when you call `WhisperTick()`.

**Arguments**

* `_enabled` `Bool` If true, enable manual ticking.

**Returns**: `Real` (ignored)

---

### `WhisperTickReset()`

Reset the manual tick counter used by `WhisperNow()` to 0.

**Arguments**

* None.

**Returns**: `Real` (ignored)

---

### `WhisperTickSet(_num)`

Set the manual tick counter used by `WhisperNow()` to an explicit value.

**Arguments**

* `_num` `Real` New manual tick value.

**Returns**: `Real` (ignored)

---

### `WhisperVerbAdd(_name, _func)`

Register a verb callback.

**Arguments**

* `_name` `String` Verb name.
* `_func` `Function` Callback taking (_ctx, _event).

**Returns**: `Real` (ignored)

* **Additional details:**

  * Verb callbacks run as `function(_ctx, _event)`.
  * `_event` includes at least: `name`, `from_pos`, `to_pos` (cursor range in the resolved string).

---

### `WhisperVerbInsert(_name)`

Build an inline verb marker string for the given verb name, but only if it's registered. Returns "" if the verb isn't registered.

**Arguments**

* `_name` `String` Verb name.

**Returns**: `String`

---

### `WhisperVerbMarker(_name)`

Build an inline verb marker string for the given verb name.

**Arguments**

* `_name` `String` Verb name.

**Returns**: `String`

---

### `WhisperVerbRunRange(_events, _from_pos, _to_pos, _ctx)`

Run verb events whose positions fall between the previous and new cursor.

**Arguments**

* `_events` `Array<Struct>` Events array from resolved text.
* `_from_pos` `Real` Previous cursor position (inclusive lower bound).
* `_to_pos` `Real` New cursor position (inclusive upper bound).
* `_ctx` `Struct` Context passed to verb callbacks.

**Returns**: `Real` (ignored)

* **Additional details:**

  * This is mainly for typewriter text. As your cursor moves forward, call this to fire any verbs that were crossed.

---
