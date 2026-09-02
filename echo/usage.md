---
layout: default
title: Using Echo
parent: Echo
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

# Using Echo

This page starts with ordinary logging and adds the rest of Echo when a debugging problem gives you a reason to use it.

---

## Log the thing you care about

When something useful happens in your game, log it with the function that matches how much attention it deserves:

```js
EchoDebugInfo("Player opened inventory");
EchoDebugWarn("Inventory loaded with a missing icon");
EchoDebugSevere("Inventory data could not be loaded");
```

`EchoDebugInfo()` is for ordinary diagnostic information that's useful while you're investigating a feature. `EchoDebugWarn()` is for something that looks wrong but doesn't necessarily stop the game. `EchoDebugSevere()` is for a serious failure where knowing where the call came from is especially useful, so severe messages include a stack trace automatically. Use info messages for frequent "this happened" notes that would be too noisy during normal debugging.

If your code already has an urgency value stored, you can use the general form instead and supply the urgency level yourself:

```js
var _urgency = eEchoDebugUrgency.WARNING;
EchoDebug("Inventory check", _urgency);
```

The four logging functions return `true` when the message passed Echo's current level and tag filters and entered the normal log. They return `false` when the message was filtered out or Echo was disabled. This can be useful when some extra debugging work should only happen for a message that was actually logged.

---

## Decide how much you want to hear

A project can easily produce more useful debug messages than you want to look at all the time. Echo's debug level lets you decide how serious a message has to be before it appears in the normal output and filtered history.

- `eEchoDebugLevel.NONE` lets no messages into the normal filtered log.
- `eEchoDebugLevel.SEVERE_ONLY` lets through only severe messages.
- `eEchoDebugLevel.COMPREHENSIVE` lets through warnings and severe messages. This is the default.
- `eEchoDebugLevel.COMPLETE` lets through info, warnings, and severe messages.

```js
EchoDebugSetLevel(eEchoDebugLevel.COMPLETE);
```

For example, `COMPREHENSIVE` is useful when you want problems to stay visible without filling the output with routine information. Switch to `COMPLETE` while chasing a specific problem and the informational messages become visible too.

Warnings include stack traces in `COMPLETE`. Severe messages include a stack trace whenever they pass the normal filter.

Read the current level when a debug tool needs to show it:

```js
var _level = EchoDebugGetLevel();
var _level_name = EchoDebugGetLevel(true);
```

The level controls the normal filtered log. Raw history, covered later on this page, can deliberately remember messages before this filter is applied.

---

## Focusing on one part of the game

The debug level answers "how important is this message?". Tags answer "what part of the game is this message about?".

```js
EchoDebugInfo("Opened pause menu", "UI");
EchoDebugWarn("Controller disconnected", ["Input", "UI"]);
EchoDebugWarn("Autosave retry", "Save");
```

If the bug you're chasing seems to involve UI and input, tell Echo to let only those tagged messages into the normal log:

```js
EchoDebugSetTags(["UI", "Input"]);
```

This function **always** takes an array, so pass arrays even when setting a single allowed tag: `EchoDebugSetTags(["UI"]);`

A message can have one tag or several. It passes when at least one of its tags appears in the allowed list. While a tag filter is active, an untagged message doesn't pass because Echo has no way to know that it belongs to the part of the game you're asking for.

```js
var _tags = EchoDebugGetTags();
EchoDebugClearTags();
```

`EchoDebugClearTags()` removes the tag filter, so messages from every part of the game can pass again.

---

## Keep enough history to inspect what happened

GameMaker's output keeps moving. A useful message can be gone from sight by the time you realise you need it, and an in-game debug tool may need to inspect messages that happened several seconds ago.

Echo therefore remembers the messages that passed its normal level and tag filters. You can cap how many entries it keeps:

```js
EchoDebugSetHistorySize(500);
```

A history size of `0` means no limit. When a limit is reached, Echo drops the oldest entries first. Long sessions can produce a lot of logs, so set a limit if you leave Echo running for long playtests.

You can inspect or clear the current filtered history directly:

```js
var _max = EchoDebugGetHistorySize();
var _lines = EchoDebugGetHistory();
EchoDebugClearHistory();
```

`EchoDebugGetHistory()` gives you the already-formatted text lines, which a simple log viewer or file-style display can use directly.

If you're building a richer tool, `EchoDebugGetStructuredHistory()` gives you the same logged events as structs with the separate pieces still available: the message, urgency, tags, time, stack information, sequence number, and optional colour. A UI can then colour warnings differently or show tags in their own column without trying to split a formatted string back apart.

`EchoDebugGetRevision()` is a small helper for that kind of tool. The number changes whenever the filtered history changes, so a UI can ask "has the log changed since I last built my rows?" instead of comparing the whole history every frame.

---

## Keep raw history when you want to re-filter later

There are two useful versions of the log:

1. The messages that passed Echo's level and tag filters at the time.
2. The messages your game tried to log before those filters decided what to show.

The first version is the normal filtered history. The second is raw history.

Raw history matters when you're using Echo Console. Imagine your game is currently showing only warnings and severe messages, then you notice a problem and decide you want to inspect the informational messages from the previous few seconds as well. If Echo had thrown those messages away at the original filter, changing the Console view now couldn't bring them back.

Raw capture keeps that earlier information available:

```js
EchoDebugSetRawHistoryCapture(true);
var _enabled = EchoDebugGetRawHistoryCapture();
```

Raw capture is enabled by default. When it's enabled, a message can be kept in raw history even if the current level is `NONE` or its tags don't pass the normal tag filter. That doesn't make the message appear in GameMaker's output or in `EchoDebugGetHistory()`. It only preserves it for tools such as Echo Console that know how to use raw history.

Turn raw capture off when you only care about the live filtered log and don't need to search backward through things that were filtered out.

---

## Dump the filtered log to a file

When you need a permanent copy of what is currently in the normal filtered history:

```js
EchoDebugDumpLog(_raw);
```

Echo writes those formatted history lines to a timestamped text file using GameMaker's text-file API. This defaults to a dump of the filtered history, but setting the `_raw` argument to `true` will dump the separate raw history.

---

## Disable Echo completely

Changing the debug level is useful while the game is running. `ECHO_DEBUG_ENABLED` is different: it's the master switch for Echo logging code.

```js
#macro ECHO_DEBUG_ENABLED 1
```

Set it to `0` when you want Echo's logging API disabled entirely. The logging calls then return `false`, and Echo doesn't create normal or raw log history.

This is different from `eEchoDebugLevel.NONE`. `NONE` keeps Echo running and can still feed raw history when raw capture is enabled, while `ECHO_DEBUG_ENABLED = 0` turns the logger off at the source.

---

## Where to go next

Use the [Echo API Reference](api-reference) when you need exact arguments and return values. If you want to search logs, inspect instances, create tuning panels, or build your own in-game debug tools, continue with [Echo Chamber](../echo-chamber/).
