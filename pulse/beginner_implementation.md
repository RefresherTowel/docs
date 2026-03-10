---
layout: default
title: Beginner Implementation
parent: Pulse
nav_order: 2
---

<!--
/// beginner_implementation.md - Changelog:
/// - 20-02-2026: New Beginner Implementation page.
-->

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>


# Beginner Implementation

This is the "normal use" of Pulse.

No custom buses. No query collectors. No queue limits. Just sending signals and reacting to them in a clean, predictable way.

If you already did the Quickstart, you're most of the way there.

---

## The core pieces

Pulse has a few words you'll see repeatedly. Here's what they mean in plain language.

A signal is the name of the thing that happened. It can be a macro, enum, number, or string.

A payload is the data you send along with the signal. It can be anything, but a struct is usually the least painful option.

A listener is the callback that runs when the signal fires.

A sender (the `from` value) is optional. It's just "who said this". You can filter on it if you want.

Sometimes you'll see me refer to "event" when talking about Pulse. If I'm talking directly about Pulse, usually "event" means "action" or essentially, the thing that happened that should make you send a signal. Obviously, GM has its own version of "event". I'll try to make sure it's obvious which I am referring to.

Pulse itself is the middleman. You don't call other objects directly. You tell Pulse, and Pulse tells everyone who's subscribed. This is how decoupling works and why signals can be such a game changer. It seems like a small change, but it can have big, positive ripple effects through your workflow.

---

## Where to put things in a project

You'll save yourself a lot of grief if you follow a simple layout.

1. One script that defines signal ids (macros or enums).
2. One always-alive controller object that calls `PulseFlushQueue()` in End Step.
3. Subscriptions in Create, cleanup in Clean Up.

This keeps your Pulse usage sane and predictable.

---

## Signals: pick a style and commit

Here's a small macro set:

```js
/// sig_pulse script
#macro SIG_HP_CHANGED		"hp_changed"
#macro SIG_INVENTORY_CHANGED	"inventory_changed"
#macro SIG_MENU_TOGGLE		"menu_toggle"
```

Strings are nice because they don't collide with unrelated enums, and they're readable in debug output. Numbers are fine too. The main rule is "unique".

If you want nicer debug output, register metadata once:

```js
PulseSignalMeta(SIG_HP_CHANGED, "HP Changed", "PLAYER", "{ hp: real, max_hp: real }");
```

This doesn't change how Pulse behaves. It just makes your tools and dumps easier to read.

---

## Subscribing: what your callback actually runs inside

A subscribe call looks like this:

```js
PulseSubscribe(id, SIG_HP_CHANGED, function(_data) {
	hp = _data.hp;
	max_hp = _data.max_hp;
});
```

Two important details:

First, the callback runs inside a `with (id)` on the listener. That means `hp` and `max_hp` above are the player's instance variables, not some magic names declared somewhere else.

Second, the payload is passed as the first argument. If you send a struct, read fields from it. If you send a number, you'll get a number. Pulse doesn't police your payload shape.

---

## Sending: keep payloads boring and consistent

A send call looks like this:

```js
var _payload = { hp: hp, max_hp: max_hp };
PulseSend(SIG_HP_CHANGED, _payload, id);
```

If you're sending the same signal from multiple places, be consistent about what fields exist. Don't make one sender use `{ value: 10 }` and another use `{ amount: 10 }` and then wonder why your game crashes.

If you want to keep it extra clean, treat payloads like tiny structs with a stable "schema", even if it's just a mental promise. I sometimes (rarely but when I'm feeling extra unlazy) keep a document with signals and the shape their payloads take so I have a quick and easy reference to keep them consistent. Notes in GM itself can be a nice place to keep this stuff.

---

## Filtering by sender (the `from` argument)

Sometimes you only care about signals from one specific thing.

Example: a UI panel that only listens to the currently opened menu instance.

```js
/// obj_menu_panel Create
menu_id = instance_create_layer(0, 0, "UI", obj_menu);

PulseSubscribe(id, SIG_MENU_TOGGLE, function(_data) {
	is_open = _data.is_open;
}, menu_id);
```

That last argument is the `from` filter. If someone else sends `SIG_MENU_TOGGLE`, this panel won't react.

If you leave `from` out, or pass `noone`, the listener accepts the signal from anyone.

---

## One-shot listeners

If you only want a listener to run once, use `PulseSubscribeOnce`.

```js
/// obj_door Create
PulseSubscribeOnce(id, SIG_BOSS_DIED, function(_data) {
	OpenDoor();
});
```

This can essentially be a cheat code for easy tutorials. Simply subscribe once to all your tutorial signals and then the tutorial only ever triggers that once, instead of every time the player performs the action you want to give them tutorial feedback on. There's obviously many reasons why you might want to subscribe once, but the tutorial thing is honestly killer workflow improvement.

---

## Unsubscribing and cleanup

Pulse will attempt to prune dead listeners automatically, but you should still clean up intentionally. It's easier to understand later, and it avoids surprises.

The simplest cleanup is:

```js
/// Clean Up
PulseRemove(id);
```

That removes every subscription registered for this instance.

If you only want to remove one signal:

```js
PulseUnsubscribe(id, SIG_HP_CHANGED);
```

---

## Subscription handles (optional, but handy)

`PulseSubscribe` returns a handle struct. Most beginners can ignore it, but it's useful to know that it exists.

```js
/// Create
hp_handle = PulseSubscribe(id, SIG_HP_CHANGED, function(_data) {
	hp = _data.hp;
});
```

You'd then deal with the handle `hp_handle` sometime later.

Handles carry fields like `signal`, `from`, `once`, and `result` (you can inspect those when you're debugging), plus a number of methods.

---

## What we didn't cover yet

At this point you can build a whole game with Pulse.

The next layer is about control and polish: queueing (PulsePost), delayed posts, coalescing latest-state spam, priority and tags, sticky signals, queries, groups, extra buses, and debugging traces.

That's all in [Advanced Implementation](advanced_implementation).
