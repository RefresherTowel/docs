---
layout: default
title: Advanced Implementation
parent: Pulse
nav_order: 3
---

<!--
/// advanced_implementation.md - Changelog:
/// - 20-02-2026: New Advanced Implementation page.
-->

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>


# Advanced Implementation

This page covers the rest of Pulse.

Everything here is optional. You're not "doing it wrong" if you never touch most of these features. That being said, these are the tools that make Pulse feel really good in bigger projects, plus a few handy helpers.

---

## Queued dispatch: doing reactions on your terms

`PulseSend` runs listeners immediately.

Sometimes that's perfect. Sometimes you want more control.

The queue lets you say "store this event now, but handle it later", which gives you a clean phase of the frame where your reactions happen.

### PulsePost + PulseFlushQueue

Posting:

```js
PulsePost(SIG_ENEMY_KILLED, { xp: 10, enemy_id: id }, id);
```

Flushing (recommended once per frame):

```js
/// End Step on an always-alive controller
PulseFlushQueue();
```

If you're already flushing every frame, `PulsePost` becomes an easy way to avoid "listener chain explosions", because all the reactions happen during the flush instead of recursively inside sends.

### PulsePostAfterFrames: delayed posts without alarms

Pulse can schedule a queued post to happen after N flushes.

```js
/// Knockback ends 6 frames after we apply it
knockback_handle = PulsePostAfterFrames(6, SIG_KNOCKBACK_END, { target: target_id }, id);
```

You get a handle back. You can cancel it if plans change:

```js
if (knockback_handle.IsActive()) {
	knockback_handle.Cancel();
}
```

Or you can check it's result:

```js
var _result = knockback_handle.Result();
```

Delays are flush-driven. If you flush once per frame, the delay behaves like "frames" and so you can think of them as timers.

### PulsePostLatest: coalescing spam

Some signals are "latest state" signals.

A slider that changes 60 times a second. A camera target. Mouse position. Analog stick aim.

If you Post those normally, you'll fill the queue with junk you never wanted.

`PulsePostLatest` keeps only the newest payload per `(signal, from)` pair.

```js
PulsePostLatest(SIG_CAMERA_TARGET, { x: x, y: y }, id);
```

When you flush, you get one event, and it's always the newest one.

---

## Queue controls: budgets and overflow

If you want to make sure your game never spends too long reacting to queued events, you can cap how much work happens per flush.

```js
/// Process at most 200 events per flush (0 means unlimited)
PulseSetFrameEventBudget(200);
```

You can also cap the queue size:

```js
PulseSetQueueLimit(1000);
```

If the queue is full, Pulse needs to decide what to drop.

```js
PulseSetOverflowPolicy(ePulseOverflowPolicy.DROP_OLDEST);
```

"Drop oldest" is often the right call for queues full of stale, out-of-date events.

---

## Priority, cancellation, and "first handler wins"

Pulse runs listeners in descending priority order (higher first). If priorities match, older subscriptions run first.

You can set priority via the listener builder (covered next), or by editing the handle you get back.

Pulse also supports cancellation. If a listener returns `true`, remaining listeners won't run for that send. You can also cancel by using a struct payload that contains a `consumed` field and setting it to `true`.

This is useful when you want multiple systems to compete to handle something, but only one should win.

Example: "who claims this input press?"

```js
/// Listener A: UI wants to eat the input first
PulseSubscribe(id, SIG_INPUT_CONFIRM, function(_data) {
	if (ui_is_open) {
		_data.consumed = true;
		return true;
	}
});
```

Then gameplay listeners won't run for that press.

If you use the `consumed` style, make sure the payload includes `consumed` when you send it:

```js
PulseSend(SIG_INPUT_CONFIRM, { consumed: false }, id);
```

---

## The listener builder: config without long argument lists

When you want more control over a subscription, use `PulseListener` and then call `PulseSubscribeConfig`.

It reads nicer, and it avoids constantly remembering optional argument order.

```js
var _cfg = PulseListener(id, SIG_MENU_TOGGLE, function(_data) {
	is_open = _data.is_open;
})
	.From(obj_menu_controller)
	.Tag("ui")
	.Priority(50)
	.Enabled(true);

var _handle = PulseSubscribeConfig(_cfg);
```

Common options:

`From(from_id)` filters by sender.

`Tag(tag)` gives the listener a label you can later target when unsubscribing.

`Priority(priority)` sets ordering when multiple listeners exist.

`Enabled(enabled)` lets you create a disabled listener and turn it on later.

`Once()` makes it a one-shot.

`Bus(bus)` targets a custom controller instead of the global bus.

`Sticky(true)` opts the listener into receiving the last sticky payload (see below).

---

## Sticky signals: late subscribers can catch up

A sticky send stores the most recent payload for a signal.

Then, if a new listener opts in, it immediately receives that latest value.

Sending sticky:

```js
PulseSendSticky(SIG_CURRENT_LANGUAGE, { lang: "en" });
```

Subscribing and opting in:

```js
var _cfg = PulseListener(id, SIG_CURRENT_LANGUAGE, function(_data) {
	current_lang = _data.lang;
}).Sticky(true);

PulseSubscribeConfig(_cfg);
```

Sticky is great for "current state" signals where late subscribers need an instant correct value.

---

## Subscription groups: clean up a whole bundle at once

A group tracks handles so you can unsubscribe everything together.

This is perfect for "a state is active" or "a room is open" situations.

```js
/// Create
pulse_group = PulseGroup();

/// EnterState
pulse_group.Add([
	PulseSubscribe(id, SIG_A, OnA),
	PulseSubscribe(id, SIG_B, OnB),
]);
```

When the state ends:

```js
pulse_group.Clear();	// unsubscribes all tracked handles
```

Groups can also act as a subscription factory with shared defaults, which can be really useful for things like a mini-game or something. Group all the related mini-game signals together, they can share some defaults via the group and then you can easily unsubscribe them all when the mini-game ends.

---

## Custom buses: isolate subsystems

The default Pulse bus is global.

Most of time that's exactly what you want, but sometimes you want a private bus for a subsystem so signals can't accidentally collide.

Create a bus:

```js
global.ui_bus = PulseBusCreate();
```

(or `global.ui_bus = new PulseController();` if you prefer)

Then use bus methods that mirror the global `Pulse*` functions:

```js
global.ui_bus.Subscribe(id, SIG_UI_OPEN, OnUiOpen);
global.ui_bus.Send(SIG_UI_OPEN, { menu: "pause" }, id);
global.ui_bus.FlushQueue();
```

You can also use the listener builder and point it at a bus:

```js
var _cfg = PulseListener(id, SIG_UI_OPEN, OnUiOpen).Bus(global.ui_bus);
PulseSubscribeConfig(_cfg);
```

---

## Queries: asking the project a question

Signals are "I am telling you something".

Queries are "I am asking you something, and I want responses".

Run a query:

```js
var _collector = PulseQuery(SIG_GET_SHOPS, { zone: current_zone });

if (_collector.Count() > 0) {
	var _shops = _collector.ToArray();
}
```

On the listener side, the callback receives a query context object. It can call `ctx.Add(value)`.

```js
PulseSubscribe(id, SIG_GET_SHOPS, function(_ctx) {
	if (zone == _ctx.payload.zone) {
		_ctx.Add(id);
	}
});
```

If you don't need the full collector, use helpers:

```js
var _shops = PulseQueryAll(SIG_GET_SHOPS, { zone: current_zone });
var _best = PulseQueryFirst(SIG_GET_BEST_SHOP, { zone: current_zone }, noone, noone);
```

---

## Debugging tools: dumps, counts, traces, and error taps

Pulse includes a few built-in ways to answer "what is even listening right now?"

`PulseCount(signal)` tells you how many listeners exist for a signal.

`PulseDumpSignal(signal)` logs a readable dump for one signal.

`PulseDump()` logs everything.

If you want to record live traffic, start a trace:

```js
PulseTraceStart(256);
```

Later, dump the trace to Echo:

```js
PulseTraceDump();
```

Pulse also emits a special signal when a listener throws an error: `PULSE_ON_ERROR`. You can subscribe to that to centralize your error reporting.

---

## Next stop: real patterns

Now that you know what the tools do, the useful part is seeing them in actual game-shaped chunks.

Head to [Common Patterns and Recipes](patterns).
