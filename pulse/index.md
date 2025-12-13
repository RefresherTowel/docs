---
layout: default
title: Pulse
nav_order: 3
has_children: true
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

![Pulse icon](../assets/pulse_icon.png)
{: .text-center}

*The beating heart of your game!*
{: .text-center}

You know that feeling when you change one tiny thing, and then 14 unrelated objects across your project suddenly need updates, or you get a brand new bug in a room you have not opened in three weeks?

Yeah. That sucks. Luckily Pulse is here to save you from yourself!

**Pulse** is a signal and event system for GameMaker. It lets you broadcast "something happened" and have anything that cares react to it, without everything needing to know about everything else.

In other words: less coupling, less spaghetti, more "I can actually change my code without fear".

<iframe frameborder="0" src="https://itch.io/embed/4116520?linkback=true&amp;border_width=2&amp;bg_color=370028&amp;fg_color=ffffff&amp;border_color=ffffff" width="554" height="169"><a href="https://refreshertowel.itch.io/pulse">Pulse by RefresherTowel</a></iframe>

---

## What Pulse is (in human terms)

Pulse is basically a tiny in-game message bus:

* Something happens (player took damage, roll finished, button clicked).
* You **send** a signal.
* Anything that subscribed to that signal runs its callback.
* Nobody has to directly call anyone else.

The sender does not care who is listening.
The listeners do not care who sent it.
All anyone agrees on is the signal identifier (and maybe a payload).

If you have ever thought "I wish my UI, VFX, audio, and gameplay could all react to the same moment without me wiring it all by hand" -> this is that.

---

## The 30 second API

If you only learn two things, learn these:

* `PulseSubscribe(id, signal, callback, [from])`
* `PulseSend(signal, [data], [from])`

That is enough for Pulse to streamline and decouple your project.

Everything else is "nice, but only when you actually need it".

---

## Why you would actually want this

Pulse is for when you want your game to be:

* **Easier to change**
  No more "this fountain needs to read the players inventory" nonsense.

* **Easier to extend**
  Add a new listener (UI tooltip, screen shake, analytics, tutorial popup) without touching the sender.

* **Less fragile**
  Your systems stop being a web of direct calls and special cases.

* **More debuggable**
  Pulse can tell you "what is listening to what" when you inevitably go "why the hell did that fire twice".

---

## This is part of the RefresherTowel Games frameworks

Pulse is part of the **RefresherTowel Games** suite of reusable frameworks for GameMaker. Every tool in the suite is designed to be:

* Easy to drop into a project
* Properly documented
* Feather-friendly (JSDoc annotations everywhere)
* And happy to work alongside the other tools, instead of fighting them

Check out the other frameworks currently available:

- [![Statement icon]({{ '/assets/statement_icon.png' | relative_url }}){: .framework-icon-small } **Statement**](https://refreshertowel.itch.io/statement) - An advanced state machine handler, easy to use for beginners, flexible enough for advanced users, with a fully interactive live visual debugger!
- [![Echo icon]({{ '/assets/echo_icon.png' | relative_url }}){: .framework-icon-small } **Echo**](https://refreshertowel.itch.io/echo) - A lightweight debug logging tool, allowing you to prioritise and filter debug messages, alongside dumping them to file easily.

These frameworks are designed specifically to work together easily, to allow you to focus on actually making your games, rather than inventing tooling! [See how you might use them with Pulse here!]({% link pulse/integration.md %})

> Pulse ships with [**Echo**](../echo/) (a minimalist, yet powerful, debug logging framework) for free!
{: .important}

---

## What Pulse gives you

### Core stuff you will use constantly

* **A global bus by default**
  Pulse ships with an autocreated global controller (via the `PULSE` macro). You do not have to manage anything to start using it.

* **Subscribe and send, nice and clean**
  Subscribe listeners (instances or structs), then send signals from anywhere.

* **One-shot listeners**
  Subscribe something that should run once and then disappear (tutorial popups, one-time cutscene triggers, "first time only" rewards).

* **Sender filtering (`from`)**
  Listen to a signal from anyone, or only from a specific sender (boss only, this UI panel only, this one controller only).

* **Safe cleanup**
  Remove one subscription, or wipe an id from every signal it is on (hello, Destroy event).

* **Callbacks run in the listener's context**
  Callbacks run inside a `with (id)` for the subscriber, so `self` and scope behaves how you intuitively expect.

* **Weak references for listeners**
  Pulse uses weak references so dead listeners can be pruned as you dispatch, instead of being kept alive forever because you forgot to unsubscribe.

### The "ok now we are cooking" features

These are optional, but they are where Pulse stops being "just a signal script" and starts being a real tool:

* **Query signals (ask the room, get answers back)**
  Sometimes you do not want "fire and forget". You want "who has an offer for this item?" or "what target should I pick?"
  Pulse has a query API: `PulseQuery`, plus helpers like `PulseQueryAll` and `PulseQueryFirst`.
  Send a question out to your game, and have everything that might want to answer supply a response back!

* **Priorities**
  Higher priority listeners run first. Great for "gameplay first, UI second, VFX last".

* **Tags**
  Tag subscriptions so you can remove a specific group later (UI, debug, rune procs, tutorial, etc).

* **Cancellation / consumption**
  A listener can stop propagation (either by returning `true`, or by setting `data.consumed = true` on a struct payload).

* **Queued dispatch (post now, process later)**
  Use `PulsePost()` to enqueue events, then process them later with `PulseFlushQueue()`.
  Also includes `PulseQueueCount()` and `PulseClearQueue()` for sanity and resets.

* **Listener builder (for readability)**
  `PulseListener(id, signal, callback)` gives you a config struct you can chain:
  `.From()`, `.Once()`, `.Tag()`, `.Priority()`, and even `.Bus()` for custom controllers, then `.Subscribe()`.

* **Subscription handles and groups**
  Subscribe calls return handles with an `Unsubscribe()` method.
  If you have a bunch of subscriptions, `PulseGroup()` lets you track them and clean them up together.

* **Custom buses when you want isolation**
  Most projects can live on the global bus.
  But if you want strict separation (UI bus vs gameplay bus, or per-system buses), you can create controllers with `PulseBusCreate()` (or `new PulseController()`) and use the same API on that bus.

* **Introspection and debug dumping**
  Count listeners (`PulseCount`, `PulseCountFor`) and dump wiring (`PulseDump`, `PulseDumpSignal`) when things get weird.

---

## Quick Start

Minimal example: enemy sends damage, player reacts.

```js
// Somewhere shared (macros, enums, whatever):
#macro SIG_DAMAGE_TAKEN 0
```

```js
/// obj_player Create
PulseSubscribe(id, SIG_DAMAGE_TAKEN, function(_data) {
    var _amount = is_struct(_data) ? _data.amount : _data;
    hp -= _amount;
});
```

```js
/// obj_enemy: when it hits the player
PulseSend(SIG_DAMAGE_TAKEN, { amount: 5 }, id);
```

That is it. You now have decoupled damage handling.

---

## A slightly more "real game" example

### Only react to a specific sender (boss damage only)

```js
PulseSubscribe(id, SIG_DAMAGE_TAKEN, function(_ev) {
    hp -= _ev.amount;
}, boss_id);
```

### Stop other listeners from reacting (consume the event)

```js
PulseSubscribe(id, SIG_INPUT_CLICK, function(_ev) {
    if (hit_my_button(_ev.x, _ev.y)) {
        DoButtonThing();
        return true; // stop propagation
    }
});
```

### Post now, apply later (queued events)

```js
/// somewhere deep in gameplay code
PulsePost(SIG_ENEMY_DIED, { x: x, y: y }, id);

/// controller Step
PulseFlushQueue(128);
```

### Ask a question instead of sending an event (query)

```js
var _offers = PulseQueryAll(SIG_GET_OFFERS, { item_id: item_id });

if (array_length(_offers) > 0) {
    var _best = _offers[0];
    // do something with it
}
```

---

## FAQ (Core)

### Do I have to use the builder (`PulseListener`)?

No. The builder is entirely optional.

For most simple cases you can stick to:

- `PulseSubscribe(id, signal, callback, [from])`
- `PulseSubscribeOnce(id, signal, callback, [from])`
- `PulseSend(signal, [data], [from])`

The builder exists to make advanced cases (tags, priorities, one-shots, filters) easier to read and maintain.

---

### What does the `from` parameter actually do?

Every listener stores a `from` filter:

- `noone` (the default) means “accept events from any sender”.  
- A specific id (for example `other.id` or `enemy_id`) means “only accept events when that id is passed as the `from` argument to `PulseSend` / `PulsePost`”.

This is helpful when you only want to react to events coming from a specific source (for example, “only take damage from this boss, not from every enemy”).

---

### What value does `PulseSubscribe` return?

Subscription, unsubscription, removal, and immediate send operations return a value from the `ePulseResult` enum, for example:

- `ePulseResult.LST_ADDED`
- `ePulseResult.LST_REMOVED_COMPLETELY`
- `ePulseResult.SGL_SENT`

If you add a duplicate listener tuple (same id + signal + from + tag), Pulse logs a warning in debug builds but still returns `LST_ADDED`.

For simple usage you can ignore these, but they become handy in tools, debug builds, or when you want to assert particular outcomes.

---

## FAQ (Advanced)

### When should I use queued events instead of `PulseSend`?

Use `PulsePost` + `PulseFlushQueue` when:

- You want to decouple *when* an event is sent from *when* its effects apply.  
- You want to avoid deep call stacks or re-entrancy issues (for example, signals that trigger more signals).  
- You want to process a batch of events at a specific point in your Step pipeline.

Use `PulseSend` when:

- You need immediate reactions and you know you are at a safe point in your logic.

A common pattern is:

```js
/// obj_controller Step
var _processed = PulseFlushQueue(128); // process up to 128 events per step
```

and use `PulsePost` elsewhere for “next-frame” style work.

---

### How does cancellation work?

Inside a listener callback you can stop further propagation in two ways:

1. **Return true** from the callback:

   ```js
   PulseSubscribe(id, SIG_INPUT_CLICK, function(_data) {
       if (hit_my_ui_button(_data)) {
           handle_button_click();
           return true; // stop; do not notify lower-priority listeners
       }
   }, noone);
   ```

2. **Use a struct payload with a `consumed` flag**:

   ```js
   var _ev = { x: mouse_x, y: mouse_y, consumed: false };
   PulseSend(SIG_INPUT_CLICK, _ev);

   // Somewhere else
   PulseSubscribe(id, SIG_INPUT_CLICK, function(_ev) {
       if (hit_something(_ev)) {
           _ev.consumed = true;
       }
   });
   ```

After each callback, Pulse checks both:

- the callback’s return value, and  
- the `consumed` field (for struct payloads).

If either indicates consumption, Pulse stops notifying remaining listeners for that signal send.

---

### What happens if I subscribe or unsubscribe inside a callback?

Pulse protects itself by taking a **snapshot** of the listener list before dispatching:

- Changes to subscriptions during a dispatch do **not** affect the current delivery.
- They take effect on the **next** signal delivery.

This means:

- If a listener unsubscribes itself during a callback, it still receives the current event, but not future ones.
- If a listener unsubscribes a different listener, that other listener will still run once for the current event, but not future ones.

This behaviour is predictable and avoids “modified the list I am iterating” crashes.

---

## Notes and requirements

* Pulse expects a modern GameMaker that supports struct constructors and methods.
* Debug dumps use your debug logger functions (Echo style). If you do not care about dumps, those can be simple no-ops.

---

## Where to next?

* If you just want to start using it: read the [Usage & Examples]({% link pulse/usage.md %}) page, check out the examples included with the tool, and go build something.
* If you want every public function documented: the [Scripting Reference]({% link pulse/scripting.md %}) page has the full API list, including queue, queries, builders, groups, custom buses, and introspection. 

---

## Help & Support

- **Bug reports / feature requests**  
 The best place to report bugs and request features is the GitHub Issues page:

  - [**Pulse Github Issues Page**](https://github.com/RefresherTowel/Pulse/issues)
  - If you are not comfortable using GitHub, you can also post in [**the Pulse discord channel**](https://discord.gg/acAqBcYHgV) and I can file an issue for you.

> It is helpful to include:
> - The relevant `Pulse*` calls you are making, including code snippets you might suspect the problem comes from.
> - Whether you are using immediate or queued dispatch.
> - Any debug output from `PulseDump` or your debug logger.
> - Any relevant debug output from `EchoDebugInfo/EchoDebugWarn/EchoDebugSevere`.
{: .note}

- **Questions / examples / discussion**  
  Join [**the Pulse discord channel**](https://discord.gg/acAqBcYHgV) to:
  - Ask integration questions.
  - Share patterns and snippets.
  - See how others are using Pulse.