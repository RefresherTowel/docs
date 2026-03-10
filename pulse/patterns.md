---
layout: default
title: Common Patterns and Recipes
parent: Pulse
nav_order: 4
---

<!--
/// patterns.md - Changelog:
/// - 20-02-2026: New patterns/recipes page.
-->

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>


# Common Patterns and Recipes

This page is meant to be stolen from.

These aren't toy examples. They're the kinds of shapes Pulse ends up taking once you start using it for real.

The recipes start simple and ramp up.

---

## Recipe: one gameplay moment, many reactions

Problem: the player takes damage and you want multiple systems to react.

Don't hard-call UI, audio, and VFX from inside your damage code. Send one signal and let everyone else decide what to do.

Signals:

```js
#macro SIG_PLAYER_DAMAGED	"player_damaged"
```

Sender (combat code):

```js
var _payload = {
	amount: amount,
	source_id: source_id,
};

PulseSend(SIG_PLAYER_DAMAGED, _payload, id);
```

Listener (HUD):

```js
PulseSubscribe(id, SIG_PLAYER_DAMAGED, function(_data) {
	hp = max(0, hp - _data.amount);
	hud_flash_timer = 10;
});
```

Listener (audio):

```js
PulseSubscribe(id, SIG_PLAYER_DAMAGED, function(_data) {
	audio_play_sound(snd_hit, 0, false);
});
```

Listener (VFX):

```js
PulseSubscribe(id, SIG_PLAYER_DAMAGED, function(_data) {
	effect_create_above(ef_explosion, x, y, 1, c_red);
});
```

Each system stays in its own lane.

---

## Recipe: queue all reactions into End Step

Problem: you want a predictable "reaction phase" each frame.

Use `PulsePost` to enqueue events, and flush once per frame in End Step.

Controller:

```js
/// obj_game_controller End Step
PulseFlushQueue();
```

Sender:

```js
PulsePost(SIG_PLAYER_DAMAGED, { amount: amount, source_id: source_id }, id);
```

Now every reaction happens during the flush, not mid-collision, not mid-draw, not mid-whatever.

---

## Recipe: state-scoped subscriptions with PulseGroup

Problem: a state (or room) sets up a bunch of listeners, and you don't want to manually remember every unsubscribe.

Use a group.

```js
/// Create (or state enter)
pulse_group = PulseGroup();

pulse_group.Add([
	PulseSubscribe(id, SIG_PAUSE, OnPause),
	PulseSubscribe(id, SIG_RESUME, OnResume),
	PulseSubscribe(id, SIG_OPEN_MENU, OnOpenMenu),
]);
```

On state exit (or room end):

```js
pulse_group.Clear();
```

It's simple and reduces boilerplate.

---

## Recipe: input "first claim wins" with cancellation

Problem: multiple systems can handle the same input, but only one should.

Send an input signal. UI listens at higher priority. If UI consumes it, gameplay never sees it.

Sender:

```js
PulseSend(SIG_INPUT_CONFIRM, { consumed: false }, id);
```

UI:

```js
var _cfg = PulseListener(id, SIG_INPUT_CONFIRM, function(_data) {
	if (ui_is_open) {
		_data.consumed = true;
		return true;
	}
})
	.Priority(100)
	.Tag("ui_input");

PulseSubscribeConfig(_cfg);
```

Gameplay:

```js
var _cfg = PulseListener(id, SIG_INPUT_CONFIRM, function(_data) {
	DoGameplayConfirm();
})
	.Priority(0);

PulseSubscribeConfig(_cfg);
```

---

## Recipe: late subscribers that need the current value (sticky)

Problem: a system comes online later and needs the current setting immediately.

Example: language, graphics quality, accessibility toggles, current profile, current music theme.

Send sticky when it changes:

```js
PulseSendSticky(SIG_CURRENT_LANGUAGE, { lang: "en" });
```

Subscribe with sticky opt-in:

```js
var _cfg = PulseListener(id, SIG_CURRENT_LANGUAGE, function(_data) {
	current_lang = _data.lang;
}).Sticky(true);

PulseSubscribeConfig(_cfg);
```

If the sticky value exists, the listener gets it right away.

---

## Recipe: coalesce "latest state" spam (PostLatest)

Problem: you're changing something constantly and only the most recent value matters.

Example: camera target, analog stick aim, mouse position, sliders.

Use PostLatest:

```js
PulsePostLatest(SIG_CAMERA_TARGET, { x: x, y: y }, id);
```

Flush once per frame as usual. You get one queued event per `(signal, from)`, and it's always the newest payload.

---

## Recipe: delayed posts with cancellation (PostAfterFrames)

Problem: you want "do X later", but you also want to cancel it if something changes.

Example: delayed respawn, delayed tooltip, delayed combo timeout.

```js
combo_timeout = PulsePostAfterFrames(30, SIG_COMBO_EXPIRE, { combo_id: combo_id }, id);
```

If the combo continues:

```js
if (combo_timeout.IsActive()) {
	combo_timeout.Cancel();
}
```

Then schedule a new one.

---

## Recipe: "ask the project" queries

Problem: you want information from whatever systems exist right now, without keeping a central registry.

Example: "who can sell me potions in this zone?" or "what loot modifiers apply to this roll?"

Query:

```js
var _offers = PulseQueryAll(SIG_GET_SHOP_OFFERS, { item_id: item_id, zone: zone_id });
```

Listener:

```js
PulseSubscribe(id, SIG_GET_SHOP_OFFERS, function(_ctx) {
	if (zone_id != _ctx.payload.zone) exit;

	if (HasItem(_ctx.payload.item_id)) {
		_ctx.Add({ shop_id: id, price: GetPrice(_ctx.payload.item_id) });
	}
});
```

Now your caller doesn't need to know who the shops are.

---

## Recipe: debugging a weird chain with Trace

Problem: you're sure a signal is firing, but you can't see who is sending it, or why.

Turn on trace recording:

```js
PulseTraceStart(256);
```

Reproduce the bug, then dump:

```js
PulseTraceDump();
```

If you want to filter to certain kinds of tap events, pass a kind or array of kinds when you start tracing (see the API reference for the available kinds).

---

## Recipe: isolate a subsystem with a custom bus

Problem: you want Pulse inside a subsystem, but you don't want it sharing signal space with the rest of the game.

Create a private bus:

```js
global.minigame_bus = PulseBusCreate();
```

Use it:

```js
global.minigame_bus.Subscribe(id, SIG_MINIGAME_START, OnStart);
global.minigame_bus.Send(SIG_MINIGAME_START, { seed: seed }, id);
```

If the minigame goes away, you can drop the bus and everything attached to it disappears with it.

---

## When you need the exact details

The [Scripting Reference](scripting) page is the authoritative list of everything Pulse exposes.
