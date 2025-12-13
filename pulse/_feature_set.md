---
layout: default
title: Feature Set
parent: Pulse
nav_order: 2
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Pulse - Feature Set

## High-level

Pulse is a signal / event bus for GameMaker that gives you:

* Persistent and one-shot listeners for any signal.
* Priority-ordered dispatch with cancellation.
* Optional deferred (queued) dispatch.
* A builder-style API for advanced listener configuration.
* A query API that collects structured responses from listeners.
* Introspection utilities for debugging and tooling.
* Group management for bulk subscription cleanup.
* Multiple independent buses via `PulseController` and `PulseBusCreate`.
* Safety features: weak refs for structs / instances, automatic pruning, and result enums for error checking.

Everything below is just those ideas broken out in detail.

---

## Core signal model

### Signals

* Any value can be used as a signal identifier (typically macros / enums).
* Signals carry:

  * A `signal` identifier.
  * Optional `data` payload (any type).
  * Optional `from` sender filter (instance or struct).

### Result enum: `ePulseResult`

Operations that subscribe, unsubscribe, remove, or dispatch return an `ePulseResult` so you can programmatically detect what happened:

* `LST_ADDED`
* `LST_REMOVED_FROM_SIGNAL`
* `LST_REMOVED_COMPLETELY`
* `LST_DOES_NOT_EXIST_IN_SIGNAL`
* `LST_DOES_NOT_EXIST`
* `SGL_DOES_NOT_EXIST`
* `SGL_NOT_SENT_NO_SGL`  (no such signal registered)
* `SGL_NOT_SENT_NO_LST`  (signal exists but has no listeners)
* `SGL_SENT`             (at least one listener ran)

These show up in:

* `PulseSubscribe`
* `PulseSubscribeOnce`
* `PulseUnsubscribe`
* `PulseRemove`
* `PulseSend`
* All equivalent `PulseController` methods.

---

## Core subscription features

### Persistent listeners: `PulseSubscribe`

* Register a listener for a `signal` on the default `PULSE` bus.
* `id` can be:

  * Instance id.
  * Struct (wrapped in a weak ref for GC).
* Optional `from` filter to only accept events from a specific sender.
* Returns a **subscription handle struct** with:

  * Fields: `controller`, `id`, `signal`, `from`, `once`, `tag`, `priority`, `active`, `result`.
  * Method: `Unsubscribe()`.
* `result` is an `ePulseResult` describing the outcome.

### One-shot listeners: `PulseSubscribeOnce`

* Same as `PulseSubscribe`, but:

  * Listener auto-unsubscribes after the first matching event (signal + from filter).
  * Still returns a subscription handle with `Unsubscribe()` and `result`.

### Callback context

* Callbacks run inside `with (id)`:

  * `self` is the listener instance/owner.
* First argument to the callback is the payload data.
* The same `signal`, `data`, and `from` are seen by all listeners for a given dispatch.

### Sender filtering

* Optional `from` parameter on subscribe:

  * `noone` means “accept from any sender”.
  * A specific id/struct means “only accept events from this sender”.
* `from` is also used in query functions and controller methods.

### Tags and priorities (via builder / config)

* Each listener has:

  * `priority` (higher runs first).
  * Optional `tag` (for grouping / targeted removal).
* Can be controlled explicitly via the listener builder (`PulseListener`) or equivalent controller features.

---

## Unsubscription and lifetime management

### Explicit unsubscribe: `PulseUnsubscribe(id, signal, [from], [tag])`

* Remove listeners for a particular `id` on a given `signal`.
* Optional filters:

  * `from` – only remove listeners bound to a specific sender.
  * `tag` – only remove listeners with a specific tag.
* Return value (`ePulseResult`) tells you:

  * `LST_REMOVED_FROM_SIGNAL` (removed something).
  * `SGL_DOES_NOT_EXIST` (signal not tracked at all).
  * `LST_DOES_NOT_EXIST_IN_SIGNAL` (signal exists but no matching listeners).
* If both `from` and `tag` are `undefined`, all subscriptions for that `id` on that signal are removed.

### Full removal: `PulseRemove(id)`

* Remove all subscriptions for an `id` across all signals on the bus.
* Returns:

  * `LST_REMOVED_COMPLETELY` if anything was removed.
  * `LST_DOES_NOT_EXIST` if the id had no subscriptions.
* Ideal for Destroy events in parent objects.

### Weak reference cleanup

* Structs and instances are tracked via weak references.
* Pulse prunes listeners whose targets have been garbage-collected / destroyed.
* Cleanup occurs during dispatch / maintenance of signals.
* Manual cleanup via `PulseRemove` is still recommended for clarity, but not strictly required for correctness.

---

## Core dispatch behavior

### Immediate dispatch: `PulseSend(signal, [data], [from])`

* Sends a signal immediately on the default `PULSE` bus.
* Listeners are invoked in **descending priority** order.
* Returns `ePulseResult`:

  * `SGL_SENT` – at least one listener ran.
  * `SGL_NOT_SENT_NO_SGL` – signal not registered at all.
  * `SGL_NOT_SENT_NO_LST` – signal exists but has no listeners.

### Cancellation rules

* If a listener returns `true`, dispatch is cancelled:

  * Remaining listeners are not called.
* If the payload (`data`) is a struct with `consumed == true`, that also cancels dispatch for subsequent listeners.
* Good for “first handler wins” patterns (input, targeting, etc).

### Subscription changes during dispatch

* If listeners subscribe/unsubscribe while a dispatch is in progress:

  * Those changes affect the **next** dispatch.
  * The current dispatch runs against a stable snapshot.

---

## Queued dispatch (deferred sending)

### Post to queue: `PulsePost(signal, [data], [from])`

* Enqueues an event on the default bus.
* Does not trigger listeners immediately.
* Returns `undefined`.

### Flush queue: `PulseFlushQueue([max_events])`

* Processes queued events in FIFO order.
* Uses the same rules as `PulseSend` (priority, cancellation, etc).
* Parameters:

  * `max_events`:

    * Negative (default `-1`) -> process all pending events.
    * Non-negative -> process up to that many events.
* Returns:

  * Number of events actually processed.
* Events posted during flush:

  * Are appended to the queue.
  * Will also be processed in the same flush while within `max_events`.

### Clear queue: `PulseClearQueue()`

* Removes all queued events without dispatching them.
* Useful for:

  * Scene resets.
  * Run restarts.
  * Abandoning pending work.

### Queue count: `PulseQueueCount()`

* Returns the number of events currently queued for deferred dispatch.

---

## Listener builder API

### Builder creation: `PulseListener(id, signal, callback)`

* Returns a **configuration struct** you can chain and then subscribe:

  * Fields: `ident`, `signal`, `callback`, `from`, `once`, `tag`, `priority`.
  * Methods:

    * `.From(from_id)`
    * `.Once()`
    * `.Tag(tag)`
    * `.Priority(priority)`
    * `.Bus(bus)`     (bind to a specific controller)
    * `.Subscribe()`  (subscribe on its chosen bus)

* Builder is “write-once”:

  * Pulse copies the configuration when you subscribe.
  * Changing the builder struct later does not mutate active listeners.

### Builder helpers

* `listener.From(from_id)`:

  * Sets a `from` filter (instance or struct).
  * Returns the builder (for chaining).

* `listener.Once()`:

  * Marks listener as one-shot.
  * Returns the builder.

* `listener.Tag(tag)`:

  * Sets an arbitrary tag on the listener.
  * Returns the builder.

* `listener.Priority(priority)`:

  * Sets listener priority (higher runs first).
  * Returns the builder.

* `listener.Bus(bus)`:

  * Binds the config to a specific `PulseController` instance.
  * Returns the builder.

### Subscribing from a builder

* `listener.Subscribe()`:

  * Subscribes the configured listener.
  * Returns a subscription handle (same shape as `PulseSubscribe`).

* `PulseSubscribeConfig(listener)`:

  * Alternate explicit subscribe call for a builder.
  * Also returns a subscription handle.

---

## Query API (response-collecting signals)

### Query context and callbacks

* Query callbacks receive a **context struct** instead of just the payload.
* Typical query callback flow:

  * Read `ctx.payload`.
  * Call `ctx.Add(value)` or `ctx.AddMany(values)` to contribute responses.
  * Return value of the callback is ignored; only the added values matter.
* Pulse aggregates all added values in priority order.

### `PulseQuery(signal, [payload], [from])`

* Runs a synchronous query on the default `PULSE` bus.
* Returns a **collector struct** with:

  * `Count()` -> number of responses.
  * `ToArray()` -> all collected values as an array.
  * `First(default)` -> first value or `default` if none.
  * `Single(default)` -> single value or `default` if none, ignoring multi-response cases.

### `PulseQueryAll(signal, [payload], [from])`

* Convenience wrapper:

  * Calls `PulseQuery`.
  * Returns `ToArray()` result directly.
* Returns:

  * Array of values in listener priority order.

### `PulseQueryFirst(signal, [payload], [from], [default])`

* Another convenience wrapper:

  * Runs a query.
  * Returns only the first response (by priority), or `default` if none.
* Good for:

  * “Find me one target.”
  * “Give me the first offer.”

---

## Introspection and debugging

### `PulseCount(signal)`

* Returns the number of listeners currently registered for a signal.

### `PulseCountFor(id)`

* Returns total subscriptions for a specific id across all signals on the bus.

### `PulseDump()`

* Logs all registered signals and their listeners through your debug logger (for example, multiple Echo lines).
* Designed for:

  * Debug builds.
  * Console commands.
  * Inspecting the current wiring of the event bus.

### `PulseDumpSignal(signal)`

* Logs only that signal and its listeners.
* Good for inspecting a single event channel.

---

## Subscription groups

### Group creation: `PulseGroup()`

* Returns a group struct with methods:

  * `Add(handle_or_array)` / `Track(handle_or_array)`:

    * Accepts a single handle or an array of handles.
    * Handles are subscription structs returned by:

      * `PulseSubscribe`
      * `PulseSubscribeOnce`
      * `listener.Subscribe()`
      * `PulseSubscribeConfig()`
  * `UnsubscribeAll()`:

    * Calls `Unsubscribe()` on every tracked handle.
    * Safe if some are already inactive.
  * `Clear()`:

    * Forgets tracked handles without unsubscribing.
  * `Destroy()`:

    * Calls `UnsubscribeAll()` then `Clear()`.

* Ideal for:

  * Room-specific subscriptions.
  * State-specific subscriptions.
  * Temporary UI / systems that must cleanly detach.

---

## Multiple buses and controllers

### Default bus: `PULSE` macro

* Global controller:

  * `#macro PULSE global.__pulse_controller`
  * Constructed once:

    * `global.__pulse_controller = new PulseController();`
* All `Pulse*` functions operate on this default bus internally.

### Custom buses: `PulseBusCreate()`

* `PulseBusCreate()`:

  * Returns a new `PulseController` instance.
  * Independent of the default bus and other controllers.

* Use cases:

  * Separate UI vs gameplay event channels.
  * Isolated minigames.
  * Modular systems with their own messaging layers.

### `PulseController` instance API

For any controller (default or custom), the API mirrors the global functions but is scoped to that bus:

**Listener management**

* `Subscribe(id, signal, callback, [from])`
* `SubscribeOnce(id, signal, callback, [from])`
* `Listener(id, signal, callback)`:

  * Returns a builder bound to that bus (similar to `PulseListener`, but controller-scoped).

**Removal**

* `Unsubscribe(id, signal, [from], [tag])`
* `Remove(id)`

**Dispatch and queue**

* `Send(signal, [data], [from])`
* `Post(signal, [data], [from])`
* `FlushQueue([max_events])`
* `ClearQueue()`
* `QueueCount()`

**Query API**

* `Query(signal, [payload], [from])`
* `QueryAll(signal, [payload], [from])`
* `QueryFirst(signal, [payload], [from], [default])`

**Introspection**

* `Count(signal)`
* `CountFor(id)`
* `Dump()`
* `DumpSignal(signal)`

Each `PulseController`:

* Has its own listener set.
* Has its own queue.
* Has its own counts and debug dumps.
* Is completely independent of others.