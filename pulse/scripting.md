# Scripting Reference

This page documents the public API of Pulse - Signals & Events for GameMaker.

It is split into:

- **Core API** – recommended reading for everyone.
- **Advanced API** – optional tools for more complex behaviour, debugging, or tooling.

---

## Core API

### Signals and Results

#### `ePulseResult`

Enum that describes the outcome of subscription, unsubscription, and dispatch operations.

Values include:

- `ePulseResult.LST_ADDED`  
- `ePulseResult.LST_ALREADY_EXISTS`  
- `ePulseResult.LST_REMOVED_FROM_SIGNAL`  
- `ePulseResult.LST_REMOVED_COMPLETELY`  
- `ePulseResult.LST_DOES_NOT_EXIST_IN_SIGNAL`  
- `ePulseResult.LST_DOES_NOT_EXIST`  
- `ePulseResult.SGL_DOES_NOT_EXIST`  
- `ePulseResult.SGL_NOT_SENT_NO_SGL`  
- `ePulseResult.SGL_NOT_SENT_NO_LST`  
- `ePulseResult.SGL_SENT`  

You will see these returned from functions like `PulseSubscribe`, `PulseUnsubscribe`, `PulseRemove`, and `PulseSend`.

---

### Core Subscribe / Unsubscribe

#### `PulseSubscribe(id, signal, callback, [from])`

Register a **persistent** listener for a signal.

```gml
PulseSubscribe(id, SIG_DAMAGE_TAKEN, function(_data) {
    hp -= _data.amount;
});
```

- `id`: `Id.Instance` – the instance that will receive the callback.  
- `signal`: `Any` – the signal identifier (usually a macro or enum).  
- `callback`: `Function` – the function to invoke when the signal is dispatched.  
- `from` *(optional)*: `Id.Instance` – sender filter; `noone` (default) means “accept from any sender”.  
- **Returns:** `ePulseResult` – typically `LST_ADDED` or `LST_ALREADY_EXISTS`.

**Callback context:** callbacks are invoked inside a `with (id)` block, so `self` behaves as that listener instance. The payload is passed as the first argument.

---

#### `PulseSubscribeOnce(id, signal, callback, [from])`

Register a **one-shot** listener that automatically unsubscribes itself after the first matching event.

```gml
PulseSubscribeOnce(id, SIG_LEVEL_UP, function(_data) {
    EchoDebugInfo("First level up!");
    give_special_reward();
});
```

- Parameters are the same as `PulseSubscribe`.  
- **Returns:** `ePulseResult` – typically `LST_ADDED` or `LST_ALREADY_EXISTS`.

The listener is removed after the first time it receives a signal that matches both the `signal` and `from` filter.

---

#### `PulseUnsubscribe(id, signal, [from], [tag])`

Unsubscribe a listener from a specific signal, with optional sender and tag filters.

```gml
// Remove all subscriptions for this id on this signal
PulseUnsubscribe(id, SIG_DAMAGE_TAKEN);

// Remove only subscriptions from a specific sender
PulseUnsubscribe(id, SIG_DAMAGE_TAKEN, boss_id);

// Remove only subscriptions with a specific tag (advanced feature)
PulseUnsubscribe(id, SIG_DAMAGE_TAKEN, undefined, TAG_BOSS_INTRO);
```

- `id`: `Id.Instance` – instance id to remove.  
- `signal`: `Any` – signal identifier.  
- `from` *(optional)*: `Id.Instance` – if provided, only listeners bound to this sender are removed.  
- `tag` *(optional)*: `Any` – if provided, only listeners with this tag are removed.  
- **Returns:** `ePulseResult` – for example:
  - `LST_REMOVED_FROM_SIGNAL` – one or more listeners removed.
  - `SGL_DOES_NOT_EXIST` – no such signal exists.
  - `LST_DOES_NOT_EXIST_IN_SIGNAL` – signal exists, but no matching listeners for that id/filter.

If both `from` and `tag` are `undefined`, all subscriptions for `id` on that signal are removed.

---

#### `PulseRemove(id)`

Completely remove an instance id from all signals it is currently listening to.

```gml
/// Destroy Event
PulseRemove(id);
```

- `id`: `Id.Instance` – instance id to remove.  
- **Returns:** `ePulseResult` – either:
  - `LST_REMOVED_COMPLETELY` – at least one listener was removed, or  
  - `LST_DOES_NOT_EXIST` – this id was not subscribed to any signal.

Recommended for use in Destroy events of parent objects to avoid dangling listeners.

---

### Core Dispatch

#### `PulseSend(signal, [data], [from])`

Dispatch a signal **immediately**, invoking all matching listeners in priority order.

```gml
var payload = { amount: 10 };
PulseSend(SIG_DAMAGE_TAKEN, payload, id);
```

- `signal`: `Any` – signal identifier.  
- `data` *(optional)*: `Any` – payload passed to listeners.  
- `from` *(optional)*: `Id.Instance` – sender id used for `from` filtering; default `noone`.  
- **Returns:** `ePulseResult` – for example:
  - `SGL_SENT` – at least one listener ran.  
  - `SGL_NOT_SENT_NO_SGL` – no such signal exists.  
  - `SGL_NOT_SENT_NO_LST` – signal exists, but has no listeners.

**Dispatch rules:**

- Listeners are run in **descending priority** order (higher `priority` first).  
- Each listener sees the same `signal`, `data`, and `from` values.  
- If a listener returns `true`, or if a struct payload has `consumed == true`, remaining listeners are not invoked (cancellation).  
- Subscriptions changed during dispatch take effect on the **next** send, not the current one.

---

## Advanced API

The following features are optional but powerful when you need more control, structure, or visibility.

### Queued Dispatch

#### `PulsePost(signal, [data], [from])`

Enqueue a signal for **later** processing via `PulseFlushQueue`.

```gml
PulsePost(SIG_ENEMY_DIED, { x: x, y: y }, id);
```

- Parameters are the same as `PulseSend`.  
- **Returns:** `Undefined`.

The event is added to an internal FIFO queue and will not run listeners until you call `PulseFlushQueue`.

---

#### `PulseFlushQueue([max_events])`

Process queued signals in FIFO order, using the same rules as `PulseSend`.

```gml
/// obj_controller Step
var processed = PulseFlushQueue(128);
```

- `max_events` *(optional)*: `Real` – maximum number of queued events to process this call; negative values (the default `-1`) process **all** pending events.  
- **Returns:** `Real` – the number of events actually processed.

Events posted during `PulseFlushQueue` are appended to the queue and will also be processed in the same call, as long as you have not hit `max_events`.

---

#### `PulseClearQueue()`

Clear all queued signals **without** dispatching them.

```gml
PulseClearQueue();
```

- **Returns:** `Undefined`.

Useful when resetting a scene or abandoning pending work (for example, when restarting a run).

---

#### `PulseQueueCount()`

Return the number of events currently queued for deferred dispatch.

```gml
var pending = PulseQueueCount();
```

- **Returns:** `Real` – the number of queued events remaining.

---

### Listener Builder

#### `PulseListener(id, signal, callback)`

Create a listener configuration struct that you can further customise and then subscribe.

```gml
var l = PulseListener(id, SIG_DAMAGE_TAKEN, OnDamage)
    .From(enemy_id)
    .Once()
    .Tag(TAG_RUNE_PROC)
    .Priority(5);
```

- `id`: `Id.Instance` – listener instance.  
- `signal`: `Any` – signal identifier.  
- `callback`: `Function` – function to invoke when the signal is dispatched.  
- **Returns:** `Struct` – a listener configuration object with fields:
  - `id`, `signal`, `callback`  
  - `from`, `once`, `tag`, `priority`  
  and methods:
  - `.From(from_id)`  
  - `.Once()`  
  - `.Tag(tag)`  
  - `.Priority(priority)`  
  - `.Subscribe()`

This struct is a **builder / config object only**. The signal system copies its values when you subscribe; mutating the struct later does not change already-registered listeners.

---

#### `listener.From(from_id)`

Set a `from` filter on the listener configuration.

```gml
listener.From(boss_id);
```

- `from_id`: `Id.Instance`.  
- **Returns:** `Struct` – the same listener config (for chaining).

---

#### `listener.Once()`

Mark the listener configuration as one-shot.

```gml
listener.Once();
```

- **Returns:** `Struct` – the same listener config.

---

#### `listener.Tag(tag)`

Set an arbitrary tag on the listener configuration.

```gml
listener.Tag(TAG_UI);
```

- `tag`: `Any`.  
- **Returns:** `Struct` – the same listener config.

Tags are useful for grouping and selective removal via `PulseUnsubscribe`.

---

#### `listener.Priority(priority)`

Set the listener’s priority.

```gml
listener.Priority(10);
```

- `priority`: `Real` – higher values run earlier.  
- **Returns:** `Struct` – the same listener config.

---

#### `listener.Subscribe()`

Subscribe this listener configuration to Pulse.

```gml
PulseListener(id, SIG_DAMAGE_TAKEN, OnDamage)
    .From(enemy_id)
    .Priority(5)
    .Subscribe();
```

- **Returns:** `ePulseResult` – result of the underlying subscription.

Internally calls `PulseSubscribeConfig(listener)`.

---

#### `PulseSubscribeConfig(listener)`

Subscribe a listener configuration created by `PulseListener`.

```gml
var cfg = PulseListener(id, SIG_DAMAGE_TAKEN, OnDamage)
    .From(enemy_id)
    .Once()
    .Priority(5);
PulseSubscribeConfig(cfg);
```

- `listener`: `Struct` – configuration from `PulseListener`.  
- **Returns:** `ePulseResult` – result of the underlying subscription.

This is the more explicit form of `listener.Subscribe()` and can be useful when you want to keep a config around for later use.

---

### Introspection & Debugging

#### `PulseCount(signal)`

Return the number of listeners currently registered for a specific signal.

```gml
var damage_count = PulseCount(SIG_DAMAGE_TAKEN);
```

- `signal`: `Any`.  
- **Returns:** `Real` – number of listeners for that signal.

---

#### `PulseCountFor(id)`

Return the total number of active subscriptions held by an instance id across all signals.

```gml
var my_subscriptions = PulseCountFor(id);
```

- `id`: `Id.Instance`.  
- **Returns:** `Real` – number of subscriptions for that id.

---

#### `PulseDump()`

Output a debug dump of all registered signals and their listeners via your debug logger (for example, multiple `EchoDebugInfo` lines).

```gml
PulseDump();
```

- **Returns:** `Undefined`.

Intended for use in debug builds or console commands.

---

#### `PulseDumpSignal(signal)`

Output a debug dump of a single signal and its listeners via your debug logger.

```gml
PulseDumpSignal(SIG_DAMAGE_TAKEN);
```

- `signal`: `Any`.  
- **Returns:** `Undefined`.

---

### Internal Types (Advanced / Optional)

#### `PULSE` macro and `PulseController`

Pulse stores its state in a global controller referenced by:

```gml
#macro PULSE global.__pulse_controller
```

and constructed once as:

```gml
global.__pulse_controller = new PulseController();
```

In normal usage you never need to touch `PulseController` directly. All interaction should go through the public `Pulse*` functions.

Advanced users who want multiple independent buses can create additional controllers manually:

```gml
var local_signals = new PulseController();
// then call local_signals.__add_listener(...) etc. (advanced, not recommended for most users)
```

However, this is considered an advanced pattern and is not required for standard usage of Pulse.
