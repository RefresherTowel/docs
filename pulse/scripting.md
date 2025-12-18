---
layout: default
title: Scripting Reference
parent: Pulse
nav_order: 3
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

This page documents the public API of Pulse - Signals & Events for GameMaker.

It is split into:

- **Core API** - recommended reading for everyone.
- **Advanced API** - optional tools for more complex behaviour, debugging, or tooling.

---

## Core API

### Signals and Results

#### `ePulseResult`

Enum that describes the outcome of subscription, unsubscription, and dispatch operations.

Values include:

- `ePulseResult.LST_ADDED`  
- `ePulseResult.LST_REMOVED_FROM_SIGNAL`  
- `ePulseResult.LST_REMOVED_COMPLETELY`  
- `ePulseResult.LST_DOES_NOT_EXIST_IN_SIGNAL`  
- `ePulseResult.LST_DOES_NOT_EXIST`  
- `ePulseResult.SGL_DOES_NOT_EXIST`  
- `ePulseResult.SGL_NOT_SENT_NO_SGL`  - the signal has no entry in the controller yet.  
- `ePulseResult.SGL_NOT_SENT_NO_LST`  - the signal exists but currently has zero listeners.  
- `ePulseResult.SGL_SENT`  

You will see these returned from functions like `PulseUnsubscribe`, `PulseRemove`, and `PulseSend`.

Subscribe functions like `PulseSubscribe` return a subscription handle struct; the `ePulseResult` for the subscribe attempt is available on that handle as `handle.result`.

---

### Core Subscribe / Unsubscribe

#### `PulseSubscribe(id, signal, callback, [from])`

Register a **persistent** listener on the default `PULSE` bus. The `id` can be an instance id or a struct; structs are wrapped in weak references so they can be garbage-collected automatically if destroyed.

```js
PulseSubscribe(id, SIG_DAMAGE_TAKEN, function(_data) {
    hp -= _data.amount;
});
```

- `id`: `Id.Instance or Struct` - receiver; structs are weak-ref wrapped for GC.  
- `signal`: `Any` - the signal identifier (usually a macro or enum).  
- `callback`: `Function` - the function to invoke when the signal is dispatched.  
- `from` *(optional)*: `Id.Instance or Struct` - sender filter; `noone` (default) means "accept from any sender".  
- **Returns:** `Struct` - a subscription handle with:
  - fields: `controller`, `uid`, `id`, `signal`, `from`, `once`, `tag`, `priority`, `enabled`, `active`, `result`
  - method: `Unsubscribe()`

The `result` field in the returned struct contains an `ePulseResult` enum entry for the subscribe attempt. In the current Pulse codebase, subscribing always reports `ePulseResult.LST_ADDED` (duplicates log a warning in debug builds, but are still added).

**Callback context:** callbacks are invoked inside a `with (id)` block, so `self` behaves as that listener instance. The payload is passed as the first argument.

**Auto-cleanup:** weak references mean Pulse will prune listeners whose targets are collected/destroyed. It is still good practice to unsubscribe when you're done, but Pulse will attempt to keep things tidy.

---

#### `PulseSubscribeOnce(id, signal, callback, [from])`

Register a **one-shot** listener on the default `PULSE` bus that automatically unsubscribes itself after the first matching event. `id` can be an instance id or struct (weak-ref wrapped).

```js
PulseSubscribeOnce(id, SIG_LEVEL_UP, function(_data) {
    EchoDebugInfo("First level up!");
    give_special_reward();
});
```

- Parameters are the same as `PulseSubscribe`.  
- **Returns:** `Struct` - subscription handle (same shape as `PulseSubscribe`).

The listener is removed after the first time it receives a signal that matches both the `signal` and `from` filter.

---

#### `PulseUnsubscribe(id, signal, [from], [tag])`

Unsubscribe a listener from a specific signal, with optional sender and tag filters.

```js
// Remove all subscriptions for this id on this signal
PulseUnsubscribe(id, SIG_DAMAGE_TAKEN);

// Remove only subscriptions from a specific sender
PulseUnsubscribe(id, SIG_DAMAGE_TAKEN, boss_id);

// Remove only subscriptions with a specific tag (advanced feature)
PulseUnsubscribe(id, SIG_DAMAGE_TAKEN, undefined, TAG_BOSS_INTRO);
```

- `id`: `Id.Instance or Struct` - listener id/struct to remove.  
- `signal`: `Any` - signal identifier.  
- `from` *(optional)*: `Id.Instance or Struct` - if provided, only listeners bound to this sender are removed.  
- `tag` *(optional)*: `Any` - if provided, only listeners with this tag are removed.  
- **Returns:** `ePulseResult` - for example:
  - `LST_REMOVED_FROM_SIGNAL` - removed at least one matching listener.
  - `SGL_DOES_NOT_EXIST` - no such signal exists.
  - `LST_DOES_NOT_EXIST_IN_SIGNAL` - signal exists, but no matching listeners for that id/filter.

If both `from` and `tag` are `undefined`, all subscriptions for `id` on that signal are removed.

If you provide either `from` or `tag`, Pulse removes the first matching subscription only (so duplicates are not all removed in one call). If you need exact or repeatable cleanup, prefer calling `handle.Unsubscribe()` on the subscription handle returned from `PulseSubscribe`/`PulseSubscribeOnce`/`PulseSubscribeConfig`, or track multiple handles in a `PulseGroup()`.

---

#### `PulseRemove(id)`

Completely remove an instance id from all signals it is currently listening to.

```js
/// Destroy Event
PulseRemove(id);
```

- `id`: `Id.Instance or Struct` - listener id/struct to remove.  
- **Returns:** `ePulseResult` - either:
  - `LST_REMOVED_COMPLETELY` - at least one listener was removed, or  
  - `LST_DOES_NOT_EXIST` - this id was not subscribed to any signal.

Recommended for use in Destroy events of parent objects to avoid dangling listeners. Pulse will prune dead weak references automatically, but explicit cleanup keeps things predictable.

---

### Core Dispatch

#### `PulseSend(signal, [data], [from])`

Dispatch a signal **immediately**, invoking all matching listeners in priority order.

```js
var _payload = { amount: 10 };
PulseSend(SIG_DAMAGE_TAKEN, _payload, id);
```

- `signal`: `Any` - signal identifier.  
- `data` *(optional)*: `Any` - payload passed to listeners.  
- `from` *(optional)*: `Id.Instance or Struct` - sender id/struct used for `from` filtering; default `noone`.  
- **Returns:** `ePulseResult` - for example:
  - `SGL_SENT` - at least one listener ran.  
  - `SGL_NOT_SENT_NO_SGL` - no such signal exists.  
  - `SGL_NOT_SENT_NO_LST` - signal exists, but has no listeners.

**Dispatch rules:**

- Listeners are run in **descending priority** order (higher `priority` first).  
- Each listener sees the same `signal`, `data`, and `from` values.  
- If a listener returns `true`, or if a struct payload has `consumed == true`, remaining listeners are not invoked (cancellation). For the payload method, make sure the payload already includes a `consumed` field when you send it (for example `{ ..., consumed: false }`).  
- Subscriptions changed during dispatch take effect on the **next** send, not the current one.

---

## Advanced API

The following features are optional but powerful when you need more control, structure, or visibility.

### Queued Dispatch

#### `PulsePost(signal, [data], [from])`

Enqueue a signal for **later** processing via `PulseFlushQueue`.

```js
PulsePost(SIG_ENEMY_DIED, { x: x, y: y }, id);
```

- Parameters are the same as `PulseSend`.  
- **Returns:** `Undefined`.

The event is added to an internal FIFO queue and will not run listeners until you call `PulseFlushQueue`.

---

#### `PulseFlushQueue([max_events])`

Process queued signals in FIFO order, using the same rules as `PulseSend`.

```js
/// obj_controller Step
var _processed = PulseFlushQueue(128);
```

- `max_events` *(optional)*: `Real` - maximum number of queued events to process this call; negative values (the default `-1`) process **all** pending events.  
- **Returns:** `Real` - the number of events actually processed.

Events posted during `PulseFlushQueue` are appended to the queue and will also be processed in the same call, as long as you have not hit `max_events`.

---

#### `PulseClearQueue()`

Clear all queued signals **without** dispatching them.

```js
PulseClearQueue();
```

- **Returns:** `Undefined`.

Useful when resetting a scene or abandoning pending work (for example, when restarting a run).

---

#### `PulseQueueCount()`

Return the number of events currently queued for deferred dispatch.

```js
var _pending = PulseQueueCount();
```

- **Returns:** `Real` - the number of queued events remaining.

---

### Listener Builder

#### `PulseListener(id, signal, callback)`

Create a listener configuration struct that you can further customise and then subscribe. You can point it at a custom bus with `.Bus(my_bus)`; otherwise it defaults to the global `PULSE`.

```js
var _l = PulseListener(id, SIG_DAMAGE_TAKEN, OnDamage)
    .From(enemy_id)
    .Once()
    .Tag(TAG_RUNE_PROC)
    .Priority(5);
```

- `id`: `Id.Instance or Struct` - listener target; structs are weak-ref wrapped.  
- `signal`: `Any` - signal identifier.  
- `callback`: `Function` - function to invoke when the signal is dispatched.  
- **Returns:** `Struct` - a listener configuration object with fields:
  - `ident`, `signal`, `callback`  
  - `from`, `once`, `tag`, `priority`, `enabled`  
  and methods:
  - `.From(from_id)`  
  - `.Once()`  
  - `.Tag(tag)`  
  - `.Priority(priority)`  
  - `.Enabled(enabled)` / `.Enable()` / `.Disable()`  
  - `.Bus(bus)` - target a specific `PulseController`
  - `.Subscribe()`

This struct is a **builder / config object only**. The signal system copies its values when you subscribe; mutating the struct later does not change already-registered listeners.

---

#### `listener.From(from_id)`

Set a `from` filter on the listener configuration.

```js
listener.From(boss_id);
```

- `from_id`: `Id.Instance or Struct`.  
- **Returns:** `Struct` - the same listener config (for chaining).

---

#### `listener.Once()`

Mark the listener configuration as one-shot.

```js
listener.Once();
```

- **Returns:** `Struct` - the same listener config.

---

#### `listener.Tag(tag)`

Set an arbitrary tag on the listener configuration.

```js
listener.Tag(TAG_UI);
```

- `tag`: `Any`.  
- **Returns:** `Struct` - the same listener config.

Tags are useful for grouping and selective removal via `PulseUnsubscribe`.

---

#### `listener.Priority(priority)`

Set the listener's priority.

```js
listener.Priority(10);
```

- `priority`: `Real` - higher values run earlier.  
- **Returns:** `Struct` - the same listener config.

---

---

#### `listener.Bus(bus)`

Bind a listener configuration to a specific `PulseController`.

```js
var _cfg = PulseListener(id, SIG_DAMAGE_TAKEN, OnDamage)
    .From(enemy_id)
    .Bus(my_bus);
```

- `bus`: `Struct.PulseController` - the bus that this listener should subscribe on.
- **Returns:** `Struct` - the same listener config (for chaining).

You can then call `listener.Subscribe()` or pass the config to `PulseSubscribeConfig` to register it.



#### `listener.Subscribe()`

Subscribe this listener configuration to Pulse.

```js
PulseListener(id, SIG_DAMAGE_TAKEN, OnDamage)
    .From(enemy_id)
    .Priority(5)
    .Subscribe();
```

- **Returns:** `Struct` - subscription handle (same as `PulseSubscribe`) with `Unsubscribe()`, metadata, and `result` telling you the ePulseResult outcome.

Internally calls `PulseSubscribeConfig(listener)`.

---

#### `PulseSubscribeConfig(listener)`

Subscribe a listener configuration created by `PulseListener`.

```js
var _cfg = PulseListener(id, SIG_DAMAGE_TAKEN, OnDamage)
    .From(enemy_id)
    .Once()
    .Priority(5);
PulseSubscribeConfig(_cfg);
```

- `listener`: `Struct` - configuration from `PulseListener`.  
- **Returns:** `Struct` - subscription handle (same as `PulseSubscribe`) with `Unsubscribe()`, metadata, and `result`.

This is the more explicit form of `listener.Subscribe()` and can be useful when you want to keep a config around for later use.

---

### Query Dispatch (Advanced)

The query API lets you broadcast a signal and collect structured responses from listeners instead of just firing callbacks.

There are two different structs involved:

- **Query context (listener side):** query callbacks receive a context struct (not the raw payload). It includes fields like `payload`, plus methods like `Add()` for submitting responses.
- **Collector (caller side):** `PulseQuery` returns a collector struct that stores the responses and exposes helper methods like `Count()` and `ToArray()`.

The return value of your query callback is ignored; only values you add via the context are collected.

#### `PulseQuery(signal, [payload], [from])`

Run a synchronous query on the default `PULSE` bus and return a collector struct that tracks all listener responses.

```js
var _collector = PulseQuery(SIG_GET_OFFERS, { item_id: item_id });

if (_collector.Count() > 0) {
    var offers = _collector.ToArray();
    // do something with the offers
}
```

- `signal`: `Any` - signal identifier.
- `payload` (optional): `Any` - payload attached to the query.
- `from` (optional): `Id.Instance or Struct` - sender filter; default `noone` (accept from any sender).
- **Returns:** `Struct` - a query collector with helpers such as:
  - `Count()` - number of responses collected.
  - `ToArray()` - all response values as an array.
  - `First(default)` - first response or `default` if none.
  - `Single(default)` - single response if exactly one exists; otherwise `default`.

Each listener that wants to participate in a query should expect a single query-context argument and call `ctx.Add(...)` or `ctx.AddMany(...)` to contribute results. The query context struct includes:

- `ctx.bus`, `ctx.signal`, `ctx.from`, `ctx.payload`
- `ctx.Add(value)`, `ctx.AddMany(array)`, `ctx.HasAny()`, `ctx.Count()`

#### `PulseQueryAll(signal, [payload], [from])`

Convenience wrapper that runs a synchronous query and returns the collected responses as an array.

```js
var offers = PulseQueryAll(SIG_GET_OFFERS, { item_id: item_id });

if (array_length(offers) > 0) {
    var best_offer = offers[0];
}
```

- `signal`: `Any` - signal identifier.
- `payload` (optional): `Any` - payload attached to the query.
- `from` (optional): `Id.Instance or Struct` - sender filter; default `noone`.
- **Returns:** `Array<Any>` - array of all response values in listener priority order.

Internally this calls `PulseQuery` and then `ToArray()` on the collector.

#### `PulseQueryFirst(signal, [payload], [from], [default])`

Run a synchronous query and return only the first response by listener priority, or a default value if no listeners respond.

```js
var target = PulseQueryFirst(SIG_AI_PICK_TARGET, undefined, noone, player_id);
```

- `signal`: `Any` - signal identifier.
- `payload` (optional): `Any` - payload attached to the query.
- `from` (optional): `Id.Instance or Struct` - sender filter; default `noone`.
- `default` (optional): `Any` - value returned when there are no responses.
- **Returns:** `Any` - first response value or `default`.


### Introspection & Debugging

#### `PulseCount(signal)`

Return the number of listeners currently registered for a specific signal.

```js
var _damage_count = PulseCount(SIG_DAMAGE_TAKEN);
```

- `signal`: `Any`.  
- **Returns:** `Real` - number of listeners for that signal.

---

#### `PulseCountFor(id)`

Return the total number of active subscriptions held by an instance id across all signals.

```js
var _my_subscriptions = PulseCountFor(id);
```

- `id`: `Id.Instance or Struct`.  
- **Returns:** `Real` - number of subscriptions for that id.

---

#### `PulseDump()`

Output a debug dump of all registered signals and their listeners via your debug logger (for example, multiple `EchoDebugInfo` lines).

```js
PulseDump();
```

- **Returns:** `Undefined`.

Intended for use in debug builds or console commands.

---

#### `PulseDumpSignal(signal)`

Output a debug dump of a single signal and its listeners via your debug logger.

```js
PulseDumpSignal(SIG_DAMAGE_TAKEN);
```

- `signal`: `Any`.  
- **Returns:** `Undefined`.

---

### Subscription Groups

#### `PulseGroup()`

Create a group for tracking multiple subscription handles so you can clean them up together, and (optionally) act as a managed subscription "factory" with shared defaults.

Handles are the structs returned by `PulseSubscribe`, `PulseSubscribeOnce`, `listener.Subscribe()`, or `PulseSubscribeConfig()`.

```js
group = PulseGroup();

group.Add([
    PulseSubscribe(id, SIG_A, OnA),
    PulseSubscribeOnce(id, SIG_B, OnB)
]);
```

- **Returns:** `Struct` - group object with methods:
  - Tracking: `Add(handle_or_array)` / `Track(handle_or_array)`
  - Cleanup: `UnsubscribeAll()`, `Clear()`, `Destroy()`, `Prune()`
  - Defaults / factory: `Bus(bus)`, `Name(name)`, `From(from)`, `Tag(tag)`, `Priority(prio)`, `PriorityOffset(delta)`, `Phase(name)`, `PhaseBase(base)`
  - Enable/disable: `IsEnabled()`, `SetEnabled(bool)`, `Enable()`, `Disable()`
  - Subscribe via group: `Listener(id, signal, callback)`, `Subscribe(...)`, `SubscribeOnce(...)`, `SubscribeConfig(listener)`
  - Bus passthrough: `Send(...)`, `Post(...)`, `FlushQueue(...)`, `ClearQueue()`, `QueueCount()`, `Query(...)`, `QueryAll(...)`, `QueryFirst(...)`
  - Debug: `Dump()`, `DumpManaged()`, counts (`Count()`, `CountActive()`, `CountEnabled()`)

Groups are handy for bundling subscriptions per state/room. Pulse prunes dead weakrefs automatically, but groups make intentional cleanup straightforward.

---

### Internal Types (Advanced / Optional)

#### `PULSE` macro and `PulseController`

Pulse stores its state in a global controller referenced by:

```js
#macro PULSE global.__pulse_controller
```

and constructed once as:

```js
global.__pulse_controller = new PulseController();
```

These definitions live inside the Pulse script; you do **not** need to duplicate them in your own project.

In normal usage you can stick to the global `PULSE` bus and the `Pulse*` functions. Advanced users can also create additional controllers manually for isolated buses:

```js
my_bus = new PulseController();

// Subscribe on the custom bus
my_bus.Subscribe(player_id, SIG_DAMAGE, OnDamage);

// Or use the builder with a bus target
var _cfg = PulseListener(id, SIG_LEVEL_UP, OnLevelUp).Bus(my_bus);
_cfg.Subscribe();

// Send/queue on that bus
my_bus.Send(SIG_DAMAGE, payload, enemy_id);
my_bus.Post(SIG_SCORE, { points: 10 });
my_bus.FlushQueue();
```

#### `PulseBusCreate()`

Create a new independent Pulse bus. Each bus is a separate `PulseController` with its own listeners and queue.

```js
var my_bus = PulseBusCreate();
```

- **Returns:** `Struct.PulseController` - a new, empty controller instance.

This is equivalent to calling `new PulseController()` directly, but keeps your code aligned with the Pulse API.

#### `PulseController` methods

When you have a custom bus (for example `my_bus` from above), you can call methods on it that mirror the global `Pulse*` functions but act only on that bus.

Listener management:

- `Subscribe(id, signal, callback, [from])` - subscribe a persistent listener.
- `SubscribeOnce(id, signal, callback, [from])` - subscribe a one-shot listener.
- `Listener(id, signal, callback)` - create a listener builder already bound to this bus (advanced; same idea as `PulseListener` but scoped to the bus).

Unsubscription:

- `Unsubscribe(id, signal, [from], [tag])` - remove listeners for a signal, with optional sender and tag filters.
- `Remove(id)` - remove all listeners for an id across all signals on this bus.

Dispatch and queue:

- `Send(signal, [data], [from])` - dispatch immediately on this bus (same rules as `PulseSend`).
- `Post(signal, [data], [from])` - enqueue an event on this bus (same idea as `PulsePost`).
- `FlushQueue([max_events])` - process queued events for this bus (same as `PulseFlushQueue` but scoped to the bus).
- `ClearQueue()` - clear this bus queue without dispatching.
- `QueueCount()` - number of events currently queued on this bus.

Query API:

- `Query(signal, [payload], [from])` - run a synchronous query on this bus and return a collector struct (same shape as `PulseQuery`).
- `QueryAll(signal, [payload], [from])` - run a query and return responses as an array.
- `QueryFirst(signal, [payload], [from], [default])` - run a query and return only the first response (or `default`).

Introspection:

- `Count(signal)` - number of listeners registered for a particular signal on this bus.
- `CountFor(id)` - total number of subscriptions held by an id on this bus.
- `Dump()` - log all signals and their listeners for this bus (debug use only).
- `DumpSignal(signal)` - log listeners for a single signal on this bus.

Phase lanes (optional priority tooling):

- `AddPhase(name, base_priority)` - add/replace a named phase lane (case-insensitive).
- `RemovePhase(name)` - remove a phase lane.
- `HasPhase(name)` - check if a phase lane exists.
- `GetPhaseBase(name)` - get a phase lane base priority (returns `0` if missing).
- `DumpPhases()` - dump all phase lanes via Echo.

Phase lanes are used by `PulseGroup().Phase(name)` and exist to give you a consistent "priority band" per system (for example `GAMEPLAY` higher than `UI`), while still letting you set smaller per-listener priorities inside that band.

Debug / tooling helpers:

- `SetBusName(name)` - set a human-friendly name used in visualisers/taps.
- `GetSnapshot()` - returns a struct snapshot (phases, queue size, subscriptions) intended for debug visualisers.
- `AddTap(fn)` / `RemoveTap(fn)` - add/remove a callback invoked with an event struct describing bus activity (subscribe, send, query, flush, etc).

Each `PulseController` is independent: counts, queue, and listeners are per-bus. Choose this only when you need strict isolation (for example, UI vs gameplay events), otherwise the global bus is simpler.

Pulse uses weak references for struct/instance subscribers and prunes dead listeners whenever it dispatches or cleans up a signal. Manual cleanup (for example, `PulseRemove` in Destroy events) remains a good habit, but Pulse will try to keep the bus tidy even if you forget occasionally.

---
<!--
#### `PulseVisualiserOpen(ui_root)`

Open or create the Pulse Visualiser window inside the Echo Debug UI desktop.

```js
PulseVisualiserOpen(global.EchoDesktop);
```

- `ui_root`: `Struct` - the Echo Chamber root / desktop struct.
- **Returns:** `Struct` - the created window, or `undefined` if `ui_root` is not a struct.
-- >