---
layout: default
title: Pulse
nav_order: 3
has_children: true
---

# Pulse - Signals & Events for GameMaker

**Pulse** is a lightweight, reusable **signal and event system** for GameMaker.  

Designed to be dropped directly into any project and used immediately, with only a few lines of code.

Pulse is part of the **RefresherTowel Games** suite of reusable frameworks for GameMaker. All of my
frameworks come with extensive documentation and complete integration with Feather to make using them as 
easy as possible.

Pulse gives you:

- A global signal controller you can access from anywhere.
- Simple **subscribe / send** helpers for day-to-day use.
- Optional **builder-based configuration** for advanced listeners.
- Built-in support for **one-shot listeners**, **sender filters**, **tags**, **priorities**, and **cancellation**.
- Both **immediate** and **queued** dispatch modes.
- Handy **introspection utilities** for debugging and profiling.
- Weak-ref subscribers keep the system lean: stale listeners are pruned automatically as you dispatch.

---

## Introduction

Pulse replaces scattered "call this script if X happens" patterns with a small, focused signal layer:

- You define **signal identifiers** (usually macros, enums or plain strings, if you're daring).
- Objects **subscribe** to the signals they care about.
- Anywhere in your project can **send** or **post** those signals.
- Pulse fans signals out to all matching listeners, in priority order, until the event is optionally consumed.
- Pulse uses weak references for its subscribers, so controller structs and instances won't be kept alive just because they're listening on the bus. Dead listeners are automatically pruned as you dispatch signals, keeping the system lean without you having to remember to unsubscribe from every corner of your code.

You can keep things **very simple** (just `PulseSubscribe` + `PulseSend`) or layer on more advanced features as your project grows.

---

## Basic Features (Core)

These are the features most users will interact with day-to-day:

- **Global signal bus**  
  Pulse exposes a single global controller via the `PULSE` macro. You do not need to create or manage a controller yourself.

- **Simple subscribe / send API**  
  - `PulseSubscribe(id, signal, callback, [from])`  
  - `PulseSubscribeOnce(id, signal, callback, [from])`  
  - `PulseSend(signal, [data], [from])`  

- **Simple cleanup helpers**  
  - `PulseUnsubscribe(id, signal, [from], [tag])`  
  - `PulseRemove(id)` for bulk removal (for example, in Destroy events).  
  - Weak references mean Pulse will try to prune dead listeners automatically, but explicit cleanup is still recommended in state/room transitions.

- **Sender filtering (`from`)**  
  Listeners can choose to only react to events from a specific sender id, or use `noone` to accept events from anyone.

- **One-shot listeners**  
  Use `PulseSubscribeOnce` when you want a listener that automatically unsubscribes itself after the first matching event. Perfect for hooking one time tutorial popups into your project.

- **Feather-friendly**  
  Functions are fully annotated with JSDoc-style comments for better autocompletion and linting in GameMaker's code editor.

If you are a beginner or just need straightforward messaging, you can safely stop at these features.

---

## Advanced Features

These features are optional. You only need them if your project calls for more control or introspection.

- **Builder-based configuration**  
  - `PulseListener(id, signal, callback)` creates a listener config struct.  
  - Chain `.From()`, `.Once()`, `.Tag()`, `.Priority()` to customise it.  
  - Call `.Subscribe()` or `PulseSubscribeConfig(listener)` to register it.

- **Subscription groups**  
  - `PulseGroup()` collects multiple subscription handles and lets you `UnsubscribeAll()`/`Destroy()` them together.

- **Tags**  
  Tag listeners (for example `TAG_RUNE_PROC`, `TAG_UI`, `TAG_DEBUG`) so you can selectively unsubscribe or organise your subscriptions.

- **Priorities**  
  Each listener has a numeric `priority`. Higher values run *earlier*. Useful for things like "core gameplay logic first, VFX last".

- **Cancellation / consumption**  
  A listener can **stop further propagation** of a signal by either:
  - Returning `true` from its callback, or
  - Setting `data.consumed = true` on a struct payload.

- **Queued dispatch**  
  - `PulsePost(signal, [data], [from])` enqueues an event.  
  - `PulseFlushQueue([max_events])` processes queued events later, in FIFO order, using the same rules as `PulseSend`.

- **Introspection utilities**  
  - `PulseCount(signal)` and `PulseCountFor(id)` to inspect listener counts.  
  - `PulseDump()` and `PulseDumpSignal(signal)` to log the current wiring through your debug system.

You can completely ignore these until you actually need them.

---

## Requirements

- **GameMaker version**  
  Any version that supports:
  - Struct constructors (`function Name(args) constructor { ... }`)
  - Methods (`method(owner, fn)`)
  - Standard array and struct functions used in modern GML

- **Scripts you need**  
  - The Pulse script (containing `ePulseResult`, `PulseListener`, `PulseSubscribe`, `PulseSend`, etc.).  
  - Your debug system script, providing at least:
    - `EchoDebugInfo(message)`  
    - `EchoDebugWarn(message)`  
    - `EchoDebugSevere(message)`  

Pulse uses these debug functions for dumps and warnings. They must exist (even if they are simple wrappers or no-ops in release builds), but Pulse will still work if you choose not to log anything.

No additional extensions or assets are required.

---

## Quick Start (Core)

A minimal example: one object listening for a signal and another sending it.

```gml
// Somewhere in a shared script:
#macro SIG_DAMAGE_TAKEN 0
```

```gml
/// obj_player Create
PulseSubscribe(id, SIG_DAMAGE_TAKEN, function(_data) {
    var _amount = is_struct(_data) ? _data.amount : _data;
    hp -= _amount;
});
```

```gml
/// obj_enemy: when it hits the player
var _payload = { amount: 5 };
PulseSend(SIG_DAMAGE_TAKEN, _payload, id);
```

That is all you need to get a basic signal flowing through Pulse:

- The player subscribes to `SIG_DAMAGE_TAKEN`.
- The enemy sends that signal with some payload data.
- Pulse calls the player’s callback in a `with (id)` context, where `id` is the instance that subscribed, so `self` inside the callback is that instance.

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

```gml
/// obj_controller Step
var _processed = PulseFlushQueue(128); // process up to 128 events per step
```

and use `PulsePost` elsewhere for “next-frame” style work.

---

### How does cancellation work?

Inside a listener callback you can stop further propagation in two ways:

1. **Return true** from the callback:

   ```gml
   PulseSubscribe(id, SIG_INPUT_CLICK, function(_data) {
       if (hit_my_ui_button(_data)) {
           handle_button_click();
           return true; // stop; do not notify lower-priority listeners
       }
   }, noone);
   ```

2. **Use a struct payload with a `consumed` flag**:

   ```gml
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

## Help & Support

- **Bug reports / feature requests**  
  Use the repository’s issue tracker.

- **Questions / examples / discussion**  
  If you run a community (Discord, forum, etc.), link it here so users can:
  - Ask integration questions.
  - Share patterns and snippets.
  - See how others are using Pulse.

When reporting bugs, it helps to include:

- The relevant `Pulse*` calls you are making.
- Whether you are using immediate or queued dispatch.
- Any debug output from `PulseDump` or your debug logger.
