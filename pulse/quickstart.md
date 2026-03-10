---
layout: default
title: Quickstart
parent: Pulse
nav_order: 1
---

<!--
/// quickstart.md - Changelog:
/// - 20-02-2026: New Quickstart page.
-->

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>


# Quickstart

This page gets Pulse running with the smallest, most useful setup.

By the end you'll have:

1. A shared signal list (so you don't end up with random magic values everywhere).
2. A queue flush in End Step (so queued work actually runs).
3. A real subscribe + send in-game.

---

## 1. Define your signals

Make a script called `sig_pulse` (or whatever you like) and put your signal ids in it.

Use anything unique (numbers, strings, enums). I like macros because they're quick, readable, and portable.

```js
/// sig_pulse.gml
#macro SIG_PLAYER_DAMAGED	"player_damaged"
#macro SIG_PLAYER_DIED		"player_died"
#macro SIG_OPEN_MENU		"open_menu"
```

That's it. The only hard requirement is "unique".

Optional (but nice): register friendly names so dumps and debug tools are more easily readable:

```js
/// Somewhere that runs once (game start is perfect)
PulseSignalMeta(SIG_PLAYER_DAMAGED, "Player Damaged", "COMBAT", "{ amount: real, source_id: id }");
PulseSignalMeta(SIG_OPEN_MENU, "Open Menu", "UI");
```

---

## 2. Flush the queue once per frame

Pulse has both immediate sends and queued posts.

Immediate sends happen right now. Queued posts wait (either until you next flush or for a specified amount of time).

Create (or pick) one always-alive controller object and add this:

```js
/// obj_game_controller End Step
PulseFlushQueue();
```

If you never use PulsePost, delayed posts, or PostLatest, you might not notice the difference. But there are situations in which Pulse will automatically queue signals for you (which need to be flushed), so it's always good to get it setup first so you don't forget later on.

End Step is a good default because most gameplay changes for the frame have happened, and now you're letting "reactive stuff" run in a predictable place. Another option might be Post-Draw as it's the last event that runs per frame.

---

## 3. Subscribe

Subscribe in Create. The callback runs inside a `with (id)` on the listener, so you have access to your instance variables directly in the function.

```js
/// obj_player Create
PulseSubscribe(id, SIG_PLAYER_DAMAGED, function(_data) {
	hp -= _data.amount;

	if (hp <= 0) {
		PulseSend(SIG_PLAYER_DIED, { killer_id: _data.source_id }, id);
	}
});
```

---

## 4. Send

Send from wherever the event actually happens.

```js
/// obj_enemy Collision with obj_player
var _payload = {
	amount: 5,
	source_id: id,
};

PulseSend(SIG_PLAYER_DAMAGED, _payload, id);
```

---

## 5. Clean up

Pulse will try to auto-prune dead listeners (struct listeners are weak-ref wrapped, and dead instances get cleaned too). Still, you can manually force clean up, if you want to take control yourself:

```js
/// obj_player Clean Up
PulseRemove(id);
```

That removes all subscriptions registered for this instance.

If you want to remove only one signal:

```js
PulseUnsubscribe(id, SIG_PLAYER_DAMAGED);
```

---

## Where to go next

If this all made sense, jump to [Beginner Implementation](beginner_implementation). That's the "learn Pulse without the fancy stuff" page.

If you're already thinking "cool, but I want delayed events, coalescing, and debugging taps", go to [Advanced Implementation](advanced_implementation).
