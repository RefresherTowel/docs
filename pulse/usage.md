---
layout: default
title: Usage & Examples
parent: Pulse
nav_order: 4
---

<!--
/// usage.md - Changelog:
/// - 23-12-2025: Updated Pulse API references and requirements.
-->

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Usage & Examples

This page walks through Pulse in three layers, from "I just want events to work" up to "I'm doing weird advanced nonsense on purpose":

- **Beginner** -> core patterns: subscribe and send.
- **Intermediate** -> one shots, queueing, simple debugging.
- **Advanced** -> custom busses, queries, and the fancy tools.

You don't need to use everything on this page. If all you ever touch is the Beginner section, that is already a big win.

---

## Beginner: Signals, Subscribe, Send

The beginner layer is about one simple story:

> Something yells, something else hears the yelling.

### 1. Defining a signal

A signal is just an identifier. The usual pattern is to define macros in a shared script:

```js
// sig_pulse.gml
#macro SIG_DAMAGE_TAKEN     0
#macro SIG_PLAYER_JUMP      1
#macro SIG_UI_BUTTON_CLICK  2
```

These can be any unique values (numbers, strings, enums). Macros keep your callsites readable.

Optional: register metadata so dumps and Vitals show friendly names.

```js
PulseSignalMeta(SIG_DAMAGE_TAKEN, "Damage Taken", "COMBAT", "{ amount: real }");
```

For custom buses, register metadata on the controller:

```js
global.BusGame.SetSignalMeta(SIG_DAMAGE_TAKEN, "Damage Taken", "COMBAT");
```

### 2. Subscribing to a signal

To listen for a signal, use `PulseSubscribe(id, signal, callback, [from])`.

```js
/// obj_player Create
PulseSubscribe(id, SIG_DAMAGE_TAKEN, function(_data) {
    // You can pass anything as payload; structs are common.
    var _amount = is_struct(_data) ? _data.amount : _data;
    hp -= _amount;
});
```

The important bits:

- `id` -> who is listening (usually `id` for the current instance).
- `SIG_DAMAGE_TAKEN` -> which signal to react to.
- Callback -> small function that will run when the signal is fired.

Behind the scenes, Pulse stores this in an internal table on the global `PULSE` bus.

### 3. Sending a signal

To trigger every listener of a signal, call `PulseSend(signal, [data], [from])`.

```js
/// obj_enemy: when it hits the player
var _payload = { amount: 5 };
PulseSend(SIG_DAMAGE_TAKEN, _payload, id);
```

Parameters:

- `signal` -> which event you are sending.
- `data` (optional) -> payload, anything you want to attach.
- `from` (optional) -> who is sending this (often `id`).

Every subscribed listener for `SIG_DAMAGE_TAKEN` will run its callback in priority order.

### 4. Listening to a specific sender (`from`)

If you only care about events from a particular source, pass a `from` filter when you subscribe.

```js
/// obj_door Create
// Only react to this door's paired switch
PulseSubscribe(id, SIG_SWITCH_TOGGLED, function(_data) {
    if (_data.on) open_door(); else close_door();
}, switch_id);
```

```js
/// obj_player Create (local co-op)
// Only process movement routed for this specific player
PulseSubscribe(id, SIG_INPUT_MOVE, function(_data) {
    handle_movement(_data);
}, player_id);
```

Any time you send:

```js
PulseSend(SIG_INPUT_MOVE, input_data, player_id);
```

only the matching player will run their callback. Everyone else subscribed to `SIG_INPUT_MOVE` with a different `from` will ignore it.

### 5. Multiple listeners and ordering

Signals can have many listeners. They run in **descending priority** order (higher runs earlier), and the default priority is `0`.

If you start thinking "this one should run before that one", that's your cue to head into the Intermediate section where priorities and cancellation live. In general, do not rely on tie ordering when multiple listeners share the same priority - set explicit priorities when ordering matters.

---

## Intermediate: One Shots, Queueing, Simple Debugging

This layer adds a bit more control, but still sticks to patterns you'll use every day.

### 1. One-shot listeners with `PulseSubscribeOnce`

Sometimes you want a listener that only fires once and then cleans itself up.

```js
/// obj_player Create
PulseSubscribeOnce(id, SIG_LEVEL_UP, function(_data) {
    EchoDebugInfo("First time level up! Special reward granted.");
    give_special_levelup_reward();
});
```

```js
/// Somewhere in your XP system
if (player_just_leveled_up) {
    PulseSend(SIG_LEVEL_UP, undefined, player_id);
}
```

That callback will run only for the first matching `SIG_LEVEL_UP` event. After that, Pulse automatically unsubscribes it. My favourite use for this is tutorial stuff. Subscribe as a one shot to some event (player takes damage, or whatever), then when it triggers, you show your little tutorial popup: "Uh-oh, looks like you took damage! Try to avoid that in the future!" and then the tutorial automatically unsubscribes itself so it doesn't pop the next time the player takes damage. There's tons of little use cases like that where `PulseSubscribeOnce` shines.

### 2. Tagging and unsubscribing

You can group listeners by tag and remove them later with `PulseUnsubscribe`.

The builder form gives you more control:

```js
var _cfg = PulseListener(id, SIG_DAMAGE_TAKEN, function(_data) {
    handle_damage(_data);
})
    .From(enemy_id)
    .Tag(TAG_COMBAT_TEMPORARY); // tag is defined by you

var _handle = PulseSubscribeConfig(_cfg);
```

Later, if you kept the handle, you can unsubscribe that exact subscription:

```js
_handle.Unsubscribe();
```

Handles created via `PulseSubscribeConfig` or `PulseGroup.SubscribeConfig` also include `SetEnabled(enabled)`, `Enable()`, `Disable()`, and `IsEnabled()` for listener gating.

You can also remove by filters:

```js
PulseUnsubscribe(id, SIG_DAMAGE_TAKEN, enemy_id, TAG_COMBAT_TEMPORARY);
```

Note: when you provide `from` and/or `tag`, `PulseUnsubscribe` removes the first matching subscription only. If you expect multiple matches, track handles (for example in a `PulseGroup()`) and unsubscribe them explicitly.

For broad cleanup, `PulseRemove(id)` removes all subscriptions for an id across every signal on the default bus. A good pattern is to call this in a parent `Destroy` event:

```js
/// Parent object Destroy
PulseRemove(id);
```

Child objects can override or extend this if they need something fancier (or additional things to happen in the Destroy Event).

> Pulse will try its darndest to remove listeners that are no longer active (garbage collected structs, destroyed instances, etc), so consider this function to be a "fallback" for situations where Pulse might mistakenly let something linger longer than it should. It's generally good to explicitly destroy things anyway, but if you forget to do so, or are feeling pretty lazy, you can rely on Pulse to attempt to clean up after you automatically.
{: .note}

### 3. Queued events with `PulsePost` and `PulseFlushQueue`

`PulseSend` fires immediately. Sometimes that is not what you want:

- You want to process all events in a predictable phase of the frame.
- You want to collect a bunch of events and then handle them in a batch.
- You want to avoid weird reentrancy when listeners send more signals.

For that, use `PulsePost` + `PulseFlushQueue`.

```js
/// Wherever the event happens
PulsePost(SIG_ENEMY_KILLED, { xp: 10, loot: some_loot }, id);
```

```js
/// obj_game_controller End Step
PulseFlushQueue();
```

Notes:

- `PulsePost` always returns `undefined` (it does not report `ePulseResult`).
- `PulseFlushQueue([max_events])` processes queued events in FIFO order.
  - Pass a negative or undefined `max_events` to flush everything.
  - Pass a positive number to cap how many events you handle per frame.

You can inspect the size of the queue for debugging:

```js
var _pending = PulseQueueCount();
draw_text(16, 16, "Pending Pulse events: " + string(_pending));
```

`PulseClearQueue()` will drop everything without dispatching, which is occasionally useful when hard-resetting a game state.

### 4. Cancellation: stopping propagation

Sometimes the first listener that handles an event should prevent others from seeing it. Classic example: layered UI panels reacting to clicks.

```js
#macro SIG_INPUT_CLICK 1
```

```js
/// obj_ui_top_panel Create
PulseSubscribe(id, SIG_INPUT_CLICK, function(_ev) {
    if (point_in_rectangle(_ev.x, _ev.y, x, y, x + w, y + h)) {
        handle_top_panel_click(_ev);
        return true; // consume; lower-priority listeners will not run
    }
});
```

```js
/// obj_ui_background_panel Create
PulseSubscribe(id, SIG_INPUT_CLICK, function(_ev) {
    if (point_in_rectangle(_ev.x, _ev.y, x, y, x + w, y + h)) {
        handle_background_click(_ev);
        // No return -> only runs if nobody above consumed the event
    }
});
```

Pulse treats the event as "consumed" if:

- The callback returns `true`, or
- The payload is a struct with a `consumed` field (for example `{ ..., consumed: false }`) and you set `payload.consumed = true`.

Once consumed, lower-priority listeners for that signal will be skipped.

You will see more details on priorities in the Advanced section; for now you can just imagine it as a queue, e.g. "top-level UI panels use higher priority; background stuff uses default priority".

### 5. Simple introspection and debugging

Pulse exposes a few helpers for checking what is currently wired up on the default bus.

```js
EchoDebugInfo("Damage listeners: " + string(PulseCount(SIG_DAMAGE_TAKEN)));
EchoDebugInfo("Player subscriptions: " + string(PulseCountFor(player_id)));

PulseDump();                    // dump all signals/listeners
PulseDumpSignal(SIG_UI_BUTTON_CLICK);  // dump a single signal
```

Typical uses:

- Spotting accidental double-subscribe.
- Verifying that expected listeners are alive.
- Checking which signals are currently "hot".

These use your debug logger (for example, Echo) so they can be filtered, disabled, or piped into your existing debug UI.

---

## Advanced: Busses, Queries, Groups, And Other Wizardry

This layer is for when you start asking questions like:

- "What if I have a separate bus just for UI?"
- "What if I want listeners to vote on a result instead of just reacting?"
- "What if I want to bundle a bunch of subscriptions and clean them up together?"

Welcome to the Advanced section.

### 1. Custom busses with `PulseBusCreate` and `PulseController`

By default, everything uses the global `PULSE` controller. If you want isolated channels (for example, separate UI vs gameplay vs tools), you can create extra busses.

```js
/// Somewhere in a central setup script
global.BusUI   = PulseBusCreate();
global.BusGame = PulseBusCreate();
```

You can also create a bus with `new PulseController()` if you prefer using the constructor directly.

You then subscribe and send on those busses instead of the global functions:

```js
/// obj_ui_button Create
global.BusUI.Subscribe(id, SIG_UI_BUTTON_CLICK, function(_data) {
    handle_ui_click(_data);
});
```

```js
/// obj_ui_manager Step
global.BusUI.Send(SIG_UI_BUTTON_CLICK, { id: button_id }, id);
```

Every `PulseController` instance has methods that mirror the global API, but only affect that bus:

- `Subscribe(id, signal, callback, [from])`
- `SubscribeOnce(id, signal, callback, [from])`
- `Listener(id, signal, callback)` -> gets you a `PulseListener` builder bound to that bus.
- `Unsubscribe(id, signal, [from], [tag])`
- `Remove(id)`
- `Send(signal, [data], [from])`
- `Post(signal, [data], [from])`
- `FlushQueue([max_events])`
- `ClearQueue()`
- `QueueCount()`
- `Count(signal)`
- `CountFor(id)`
- `Dump()`
- `DumpSignal(signal)`
- `Query(signal, [payload], [from])`
- `QueryAll(signal, [payload], [from])`
- `QueryFirst(signal, [payload], [from], [default])`

Additional controller-only helpers include:

- `AddPhase(name, base_priority)`
- `RemovePhase(name)`
- `HasPhase(name)`
- `GetPhaseBase(name)`
- `DumpPhases()`
- `SetBusName(name)`
- `GetSnapshot()`
- `AddTap(fn)`
- `RemoveTap(fn)`

Using custom busses is entirely optional, but very handy for:

- Keeping debug tooling separate from gameplay.
- Making in-editor tools that you can turn on/off as a block.
- Building "mini games" or simulations that should not interfere with the main event flow.

### 2. Listener builders and `listener.Bus(bus)`

`PulseListener(id, signal, callback)` creates a builder struct. You already saw one example in the intermediate section; here is how it looks with a custom bus:

```js
var _cfg = PulseListener(id, SIG_LEVEL_UP, function(_ctx) {
    // handle level up
})
    .From(player_id)
    .Bus(global.BusGame);

var _handle = PulseSubscribeConfig(_cfg);
```

`.Bus(bus)` binds the builder to a specific `PulseController`. Under the hood this is what `bus.Listener(...)` uses too.

Builder configs also support `.Enabled(enabled)`, `.Enable()`, and `.Disable()` to control the initial enabled state.
`PulseSubscribeConfig` requires a listener config struct built from `PulseListener`.
`.Bus(bus)` requires a Pulse controller struct built from `PulseController` or `PulseBusCreate`.

Builder configs are nice when you want to:

- Store subscription plans in data.
- Construct or clone listeners from configuration tables.
- Keep an easy-to-read "subscription recipe" next to your systems.

### 3. Groups of subscriptions with `PulseGroup`

`PulseGroup()` gives you an object that tracks a bunch of subscription handles and can clean them up in one go.

```js
var _group = PulseGroup();

_group.Add(PulseSubscribe(obj_a.id, SIG_DAMAGE_TAKEN, OnDamageA));
_group.Add(PulseSubscribe(obj_b.id, SIG_DAMAGE_TAKEN, OnDamageB));

// Later, maybe when leaving a state or room:
_group.UnsubscribeAll();
_group.Destroy();
```

You can also add arrays of handles:

```js
var _handles = [
    PulseSubscribe(obj_a.id, SIG_DAMAGE_TAKEN, OnDamageA),
    PulseSubscribe(obj_b.id, SIG_DAMAGE_TAKEN, OnDamageB)
];

var _group = PulseGroup().Add(_handles);
```

Methods (high level):

- `Add(handle_or_array)` / `Track(handle_or_array)` -> add one handle or an array of handles.
- `UnsubscribeAll()` -> call `Unsubscribe()` on every tracked handle.
- `Clear()` -> forget the handles without unsubscribing (rare, but there if you need it).
- `Destroy()` -> `UnsubscribeAll()` then `Clear()`.

Additional group helpers (advanced):

- Defaults and setup: `Bus(bus)`, `Name(name)`, `From(from)`, `Tag(tag)`, `Priority(priority)`, `PriorityOffset(delta)`, `Phase(name)`, `PhaseBase(base_priority)`
- Enable and disable: `IsEnabled()`, `SetEnabled(enabled)`, `Enable()`, `Disable()`
- Subscribe helpers: `Listener(id, signal, callback)`, `Subscribe(id, signal, callback, [from])`, `SubscribeOnce(id, signal, callback, [from])`, `SubscribeConfig(listener)`
- Cleanup: `Prune()`
- Counts: `Count()`, `CountActive()`, `CountEnabled()`
- Debug: `Dump()`, `DumpManaged()`
- Bus passthrough: `Send(signal, [data], [from])`, `Post(signal, [data], [from])`, `FlushQueue([max_events])`, `ClearQueue()`, `QueueCount()`
- Query passthrough: `Query(signal, [payload], [from])`, `QueryAll(signal, [payload], [from])`, `QueryFirst(signal, [payload], [from], [default])`

`Add(handle_or_array)` and `Track(handle_or_array)` require subscription handle structs built from `PulseSubscribe`, `PulseSubscribeOnce`, `PulseSubscribeConfig`, or `listener.Subscribe`.
`SubscribeConfig(listener)` requires a listener config struct built from `PulseListener`.
`Bus(bus)` requires a Pulse controller struct built from `PulseController` or `PulseBusCreate`.

Groups go very well with state machines, menus, and temporary game modes where you want "everything this mode subscribed to" to disappear at once.

### 4. Query dispatch with `PulseQuery`, `PulseQueryAll`, `PulseQueryFirst`

Sometimes you do not just want to shout "something happened". You want to ask a question and get structured responses.

Instead of sending an arbitrary payload, query listeners receive a **query context** struct. They can add responses into it, and you decide what to do with them.

```js
#macro SIG_SHOP_GET_OFFERS 3
```

Listener side:

```js
/// obj_shopkeeper Create
PulseSubscribe(id, SIG_SHOP_GET_OFFERS, function(_q) {
    // Query listeners receive a query context (not the raw payload).
    // `_q.payload` is whatever the caller passed into PulseQuery / PulseQueryAll / PulseQueryFirst.
    var _item_id = _q.payload.item_id;

    if (has_offer_for(_item_id)) {
        // Add one response into the query result set.
        _q.Add({
            item_id: _item_id,
            price: get_price_for(_item_id),
            source: id
        });
    }
});
```

Caller side:

```js
var _payload = { item_id: ITEM_POTION };
var _collector = PulseQuery(SIG_SHOP_GET_OFFERS, _payload);

// PulseQuery returns a collector (the accumulated responses).
if (_collector.Count() > 0) {
    var _offers = _collector.ToArray();
    _offers = sort_offers_by_price(_offers);
    var _best = _offers[0];
}
```

Key pieces you interact with:

- **Listener query context** (argument to the query listener callback):
  - `_q.payload` -> whatever you passed into the query.
  - `_q.Add(value)` / `_q.AddMany(array)` -> add responses.
- **Collector** (returned by `PulseQuery`):
  - `Count()` -> number of responses collected.
  - `ToArray()` -> responses as an array.
  - `First(default)` -> first response or `default`.
  - `Single(default)` -> only response or `default` if there is not exactly one.

Convenience wrappers:

```js
// All responses as an array
var _offers = PulseQueryAll(SIG_SHOP_GET_OFFERS, _payload);

// Only the first response by listener priority, or a fallback
var _target = PulseQueryFirst(SIG_AI_PICK_TARGET, undefined, noone, player_id);
```

Queries are especially handy for:

- AI systems ("ask everyone who wants to attack, pick one").
- Dynamic pricing / loot systems.
- "Who can handle this request" style routing.

### 5. Advanced debugging patterns

Once you have multiple busses and a lot of signals, debugging becomes less about "is anything subscribed" and more about "what is this bus doing right now".

Examples:

```js
// Dump everything on just the UI bus
global.BusUI.Dump();

// Dump a single signal on the gameplay bus
global.BusGame.DumpSignal(SIG_ENEMY_KILLED);

// Count listeners on a signal per bus
EchoDebugInfo("UI clicks: "   + string(global.BusUI.Count(SIG_UI_BUTTON_CLICK)));
EchoDebugInfo("Game clicks: " + string(global.BusGame.Count(SIG_UI_BUTTON_CLICK)));
```

You can combine this with your own debug overlays, in-game consoles, or visual debuggers. Pulse stays out of the way and just answers the questions.

---

If you read all the way down here: congrats, you've officially added a heartbeat to your game. In practice, you will probably pick 1 or 2 patterns from the Advanced section and ignore the rest until some future "hmmm, I bet Pulse can help with this" moment.

If you have any feature requests, or bugs to report please either

- Use the GitHub Issues page: [**Pulse issues**](https://github.com/RefresherTowel/Pulse/issues).
    - It is helpful to include:
      - The relevant `Pulse*` calls you are making, including code snippets you might suspect the problem comes from.
        - Whether you are using immediate or queued dispatch.
        - Any debug output from `PulseDump` or your debug logger.
        - Any relevant debug output from `EchoDebugInfo/EchoDebugWarn/EchoDebugSevere`.

- If you are not comfortable using GitHub, you can also post in [**the Pulse discord channel**](https://discord.gg/acAqBcYHgV) and I can file an issue for you.
