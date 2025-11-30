---
layout: default
title: Usage & Examples
parent: Pulse
nav_order: 2
---

# Usage & Examples

This page shows how to use Pulse in practice, split into:

- **Core usage** – basic patterns.
- **Advanced usage** – optional patterns for more complex behaviour.
- **Gotchas** – things to keep in mind.

---

## Core Usage

### 1. Basic subscribe and send

Define a signal identifier and wire up a simple listener + sender.

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

This sets up:

- A signal identifier `SIG_DAMAGE_TAKEN`.
- The player listening to that signal for **any sender**.
- The enemy sending the signal with a data payload and its own `id` as the `from` value.

---

### 2. Listening to a specific sender (`from` filter)

Use the optional `from` parameter when subscribing if you only care about events from a particular source. Some practical patterns:

```gml
/// obj_door Create
// Only react to this door's paired switch
PulseSubscribe(id, SIG_SWITCH_TOGGLED, function(_data) {
    if (_data.on) open_door(); else close_door();
}, switch_id);
```

```gml
/// obj_player Create (local co-op)
// Only process input routed for this player
PulseSubscribe(id, SIG_INPUT_MOVE, function(_data) {
    hsp = _data.dx;
    vsp = _data.dy;
}, my_input_router_id);
```

```gml
/// obj_pet Create
// Only obey commands sent by this pet's owner
PulseSubscribe(id, SIG_PET_COMMAND, function(_data) {
    ExecuteCommand(_data.cmd);
}, owner_id);
```

- If the same signal is sent from other senders, these listeners will **ignore** those events unless `from` matches.
- Using `noone` as the `from` value when subscribing means “accept from any sender”.

---

### 3. One-shot listeners

Use `PulseSubscribeOnce` to react exactly once to an event, then automatically unsubscribe.

```gml
/// obj_player Create
PulseSubscribeOnce(id, SIG_LEVEL_UP, function(_data) {
    EchoDebugInfo("First time level up! Special reward granted.");
    give_special_reward();
});
```

```gml
/// Somewhere in your XP system
if (player_just_leveled_up) {
    PulseSend(SIG_LEVEL_UP, undefined, player_id);
}
```

The callback will run only for the first `SIG_LEVEL_UP` that matches the subscription’s `from` filter (or any sender if you used the default).

---

### 4. Basic queued events with PulsePost / PulseFlushQueue

Use `PulsePost` + `PulseFlushQueue` when you want to process events at a controlled part of your frame rather than immediately.

`PulsePost` is fire-and-forget: it enqueues the event and returns `Undefined` (it does not return an `ePulseResult`).

```gml
/// obj_game_controller Create
// No special setup needed; we just decide to flush in Step.
```

```gml
/// obj_game_controller Step
// Process up to 128 queued events per frame
PulseFlushQueue(128);
```

```gml
/// obj_enemy: when it dies
var _payload = { x: x, y: y };
PulsePost(SIG_ENEMY_DIED, _payload, id);
```

```gml
/// obj_loot_manager Create
PulseSubscribe(id, SIG_ENEMY_DIED, function(_data) {
    spawn_loot(_data.x, _data.y);
});
```

Here:

- Enemies **post** `SIG_ENEMY_DIED` events as they die.
- The controller **flushes** the queue once per Step.
- The loot manager reacts when events are flushed, not at the moment of death, which can help simplify ordering or avoid deep call stacks.

---

## Advanced Usage

### 5. Using the builder for complex listeners

For more complex cases, use `PulseListener` as a builder, then subscribe the result.

```gml
/// obj_player Create

// A one-shot, high-priority listener for the first hit from this boss.
PulseListener(id, SIG_DAMAGE_TAKEN, function(_data) {
        EchoDebugInfo("First hit from boss; trigger cutscene.");
        trigger_boss_intro_cutscene();
    })
    .From(boss_id)
    .Once()
    .Tag(TAG_BOSS_INTRO)
    .Priority(10)
    .Subscribe();
```

This is equivalent to configuring everything manually, but reads much more clearly at the call site:

- It only reacts to `SIG_DAMAGE_TAKEN` from `boss_id`.
- It runs **before** lower-priority listeners (because of `Priority(10)`).
- It removes itself after the first matching event (`Once()`).
- It carries the tag `TAG_BOSS_INTRO`, which can be used later when unsubscribing.

You can also keep a listener config around and subscribe it later:

```gml
player.boss_intro_listener = PulseListener(id, SIG_DAMAGE_TAKEN, BossIntroDamage)
    .From(boss_id)
    .Once()
    .Tag(TAG_BOSS_INTRO)
    .Priority(10);

// Later, when the fight starts:
player.boss_intro_listener.Subscribe();
```

---

### 6. Cancellation: stopping propagation

Sometimes you want the first listener that “claims” an event to prevent others from seeing it.

Example: layered UI panels reacting to click input.

```gml
#macro SIG_INPUT_CLICK 1
```

```gml
/// obj_ui_top_panel Create
PulseSubscribe(id, SIG_INPUT_CLICK, function(_ev) {
    if (point_in_rectangle(_ev.x, _ev.y, x, y, x + w, y + h)) {
        handle_top_panel_click(_ev);
        return true; // consume; no lower-priority listeners run
    }
}, noone);
```

```gml
/// obj_ui_background_panel Create
PulseSubscribe(id, SIG_INPUT_CLICK, function(_ev) {
    if (point_in_rectangle(_ev.x, _ev.y, x, y, x + w, y + h)) {
        handle_background_click(_ev);
        // No return => this will only run if higher-priority listeners did not consume
    }
}, noone);
```

```gml
/// obj_input_router Step
var _ev = { x: device_mouse_x_to_gui(0), y: device_mouse_y_to_gui(0), consumed: false };
if (mouse_check_button_pressed(mb_left)) {
    PulseSend(SIG_INPUT_CLICK, _ev);
}
```

Cancellation rules:

- If a callback **returns true**, Pulse stops notifying remaining listeners.
- If a struct payload has `consumed == true` after a callback, Pulse also stops.

Use `Priority` on listeners to control which callbacks get first chance to consume an event.

---

### 7. Grouping subscriptions for cleanup

`PulseGroup()` lets you collect multiple subscription handles (the structs returned by `PulseSubscribe`, `PulseSubscribeOnce`, or `listener.Subscribe()`) and dispose of them together.

```gml
/// obj_player Create
sub_group = PulseGroup()
    .Add(PulseSubscribe(id, SIG_INPUT_MOVE, OnMove, my_input_router))
    .Add(PulseSubscribeOnce(id, SIG_FIRST_HIT, OnFirstHit));
```

When the state ends or the object is destroyed:

```gml
/// obj_player Destroy
if (!is_undefined(sub_group)) {
    sub_group.UnsubscribeAll();
}
```

- `Add` (or `Track`) accepts a single handle or an array.
- `UnsubscribeAll` calls `Unsubscribe()` on each tracked handle (safe if already inactive).
- `Clear` forgets the handles without unsubscribing.
- `Destroy` unsubscribes everything then clears.

Pulse will still prune dead weakrefs automatically, but groups keep explicit cleanup straightforward when swapping states or rooms.

---

### 8. Cleanup and unsubscribe patterns

Make sure listeners don’t linger longer than intended:

```gml
/// Destroy Event of an object that subscribes to signals
PulseRemove(id); // remove this instance from all signals
```

Selective unsubscribe examples:

```gml
// Remove only subscriptions for this sender
PulseUnsubscribe(id, SIG_DAMAGE_TAKEN, boss_id);

// Remove only subscriptions with a specific tag
PulseUnsubscribe(id, SIG_UI_EVENT, undefined, TAG_MENU_OPEN);
```

---

### 9. Priorities for ordering

By default, listeners share a priority of `0`. Higher numbers are run earlier.

```gml
/// obj_player Create

// High-priority damage handler: adjust HP and play hitstun.
PulseListener(id, SIG_DAMAGE_TAKEN, function(_data) {
        apply_damage(_data);
        apply_hitstun();
    })
    .Priority(10)
    .Subscribe();

// Lower-priority VFX handler: spawn blood, shake camera.
PulseListener(id, SIG_DAMAGE_TAKEN, function(_data) {
        spawn_damage_vfx(_data);
        camera_shake_small();
    })
    .Priority(-5)
    .Subscribe();
```

Ordering here:

1. Damage + hitstun runs (priority 10).
2. VFX runs (priority -5).

If the high-priority handler consumes the event (returns true or sets `consumed`), the low-priority handler will not run at all.

---

### 10. Introspection and debugging

Use the introspection helpers when you want to inspect or debug your wiring at runtime.

```gml
/// Somewhere in a debug console command
EchoDebugInfo("Damage listeners: " + string(PulseCount(SIG_DAMAGE_TAKEN)));
EchoDebugInfo("Player subscriptions: " + string(PulseCountFor(player_id)));

PulseDump();                  // dump all signals
PulseDumpSignal(SIG_UI_CLICK); // dump a single signal
```

Typical uses:

- Ensuring you are not accidentally double-subscribing the same listener.
- Checking that expected listeners are still alive.
- Counting how many listeners a “hot” signal currently has.

Remember that these use your debug logger (for example, `EchoDebugInfo`), so log output can be filtered or turned off via your existing debug settings.

Other quick checks:

```gml
// Pending queued events (for debug overlay)
var _pending = PulseQueueCount();
draw_text(16, 16, "Queued events: " + string(_pending));

// Per-signal / per-id counts
EchoDebugInfo("Damage listeners: " + string(PulseCount(SIG_DAMAGE_TAKEN)));
EchoDebugInfo("My subscriptions: " + string(PulseCountFor(id)));

// Trigger a dump on a debug key
if (keyboard_check_pressed(ord("P"))) {
    PulseDumpSignal(SIG_UI_CLICK);
}
```

---

## Gotchas & Best Practices

### 1. You must flush the queue yourself

**Pulse does not automatically flush queued events.** If you use `PulsePost`, you **must** call `PulseFlushQueue` somewhere (usually each frame from a central controller object).

If you never call `PulsePost`, you can ignore the queue entirely.

---

### 2. Changes during dispatch affect the next send, not the current one

**Because Pulse takes a snapshot of listeners before dispatching:**

- Subscribing or unsubscribing during a callback will not affect the *current* event.
- Changes take effect on the next `PulseSend` / `PulseFlushQueue` call.

This is intentional and prevents crashes from modifying the list while it is being iterated.

---

### 3. Be careful with infinite queues

Because events posted during `PulseFlushQueue` are appended to the same queue, it is possible to create feedback loops where listeners continually post new events.

Protect yourself by:

- Passing a sensible `max_events` value to `PulseFlushQueue`, and/or
- Designing your event graph to avoid unbounded “post more of myself” behaviour.

---

### 4. Use tags for selective cleanup

If you create lots of temporary listeners (for example, per-boss or per-cutscene), consider tagging them:

```gml
#macro TAG_CUTSCENE 100

PulseListener(id, SIG_SKIPPABLE_PROMPT, OnCutscenePrompt)
    .Tag(TAG_CUTSCENE)
    .Subscribe();
```

Later, you can selectively remove these:

```gml
PulseUnsubscribe(id, SIG_SKIPPABLE_PROMPT, undefined, TAG_CUTSCENE);
```

Tags are optional but become very handy in large projects.

---

### 5. Always clean up on Destroy (recommended)

Pulse does not automatically remove subscriptions when an instance is destroyed. To avoid dangling listeners on recycled ids, add a pattern like this to your parent objects:

```gml
/// Parent object Destroy
PulseRemove(id);
```

This removes all subscriptions for that `id` across every signal.

You can override or extend this behaviour in child objects if needed, but having a parent-level cleanup avoids many subtle bugs in long-running games.
