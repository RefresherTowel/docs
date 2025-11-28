---
layout: default
title: Usage & Examples
parent: Statement
nav_order: 2
---

# Usage & Examples

This page shows how to use Statement in practice, split into:

- **Core usage** – basic patterns.
- **Advanced usage** – optional patterns for more complex behaviour.
- **Gotchas** – things to keep in mind.

---

## Core Usage

### 1. Basic Hello World

```gml
/// Create Event
state_machine = new Statement(self);

var _idle = new StatementState(self, "Idle")
    .AddEnter(function() {
        EchoDebugInfo("Entered Idle");
    })
    .AddUpdate(function() {
        image_angle += 1;
    });

state_machine.AddState(_idle);


/// Step Event
state_machine.Update();


/// Draw Event (optional)
state_machine.Draw();
```

This sets up:

- A `Statement` bound to `self`.
- One state, `Idle`, with `Enter` + `Update` handlers.
- The machine driven from Step (and optionally Draw).

---

### 2. Multiple States with Simple Transitions

```gml
/// Create Event
state_machine = new Statement(self);

// Idle
var _idle = new StatementState(self, "Idle")
    .AddEnter(function() {
        sprite_index = spr_player_idle;
        hsp = vsp = 0;
    })
    .AddUpdate(function() {
        if (keyboard_check_any_pressed()) {
            state_machine.ChangeState("Move");
        }
    });

// Move
var _move = new StatementState(self, "Move")
    .AddEnter(function() {
        sprite_index = spr_player_move;
    })
    .AddUpdate(function() {
        var _dx = keyboard_check(ord("D")) - keyboard_check(ord("A"));
        var _dy = keyboard_check(ord("S")) - keyboard_check(ord("W"));

        hsp = _dx * 4;
        vsp = _dy * 4;

        x += hsp;
        y += vsp;

        if (_dx == 0 && _dy == 0) {
            state_machine.ChangeState("Idle");
        }
    });

state_machine
    .AddState(_idle)
    .AddState(_move);


/// Step Event
state_machine.Update();


/// Draw Event
state_machine.Draw();
```

---

### 3. Using `GetStateTime()` for Behaviour

```gml
var _attack = new StatementState(self, "Attack")
    .AddEnter(function() {
        sprite_index = spr_player_attack;
        image_index = 0;
        // state_machine.SetStateTime(0); // optional: age is already reset on ChangeState
    })
    .AddUpdate(function() {
        // Stay in Attack for 20 frames
        if (state_machine.GetStateTime() >= 20) {
            state_machine.ChangeState("Idle");
        }
    });

state_machine.AddState(_attack);
```

Because `state_machine` resets `state_age` automatically on state change, you can often skip the explicit `SetStateTime(0)`.

---

## Advanced Usage

### 4. Queued Transitions to Avoid Mid-Update Re-entry

```gml
var _move = new StatementState(self, "Move")
    .AddUpdate(function() {
        // movement logic...

        if (mouse_check_button_pressed(mb_left)) {
            // Queue an attack; actual change happens at next Update
            state_machine.QueueState("Attack");
        }
    });

var _attack = new StatementState(self, "Attack")
    .AddEnter(function() {
        sprite_index = spr_player_attack;
        image_index = 0;
    })
    .AddUpdate(function() {
        if (image_index >= image_number - 1) {
            state_machine.ChangeState("Idle");
        }
    });

state_machine
    .AddState(_move)
    .AddState(_attack);
```

Because transitions are queued, the rest of the current `Update` runs in the **old** state, and `Attack` starts cleanly next frame.

---

### 5. Manual Queue Processing

If you want explicit control over when queued transitions happen:

```gml
/// Create
state_machine = new Statement(self)
    .SetQueueAutoProcessing(false);


/// Step
// Do your own logic...
// When ready to apply queued transitions:
state_machine.ProcessQueuedState();
state_machine.Update();
```

Now you can insert queue processing at a specific spot in your step pipeline.

---

### 6. Using Push/Pop for Overlays (Pause State)

```gml
/// Create
state_machine = new Statement(self);

// Existing states: Idle, Move, Attack... (omitted)

// Pause overlay
var _pause = new StatementState(self, "Pause")
    .AddEnter(function() {
        hsp = vsp = 0;
    })
    .AddUpdate(function() {
        if (keyboard_check_pressed(vk_escape)) {
            state_machine.PopState();
        }
    })
    .AddDraw(function() {
        draw_set_alpha(0.5);
        draw_rectangle(0, 0, display_get_gui_width(), display_get_gui_height(), false);
        draw_set_alpha(1);
        draw_text(32, 32, "PAUSED");
    });

state_machine.AddState(_pause);


/// Step
if (keyboard_check_pressed(vk_escape)
&& state_machine.GetStateName() != "Pause") {
    state_machine.PushState("Pause");
}

state_machine.Update();


/// Draw
state_machine.Draw();
```

- `PushState("Pause")` saves the current state and enters `Pause`.
- `PopState()` returns to exactly that state.

---

### 7. Per-State Timers for More Complex Timing

```gml
/// Create Event
state_machine = new Statement(self);

charge = new StatementState(self, "Charge")
    .AddEnter(function() {
        charge.TimerStart(); // per-state timer
    })
    .AddUpdate(function() {
        // Charge for at least 60 frames, regardless of how often Update runs
        if (charge.TimerGet() >= 60) {
            state_machine.ChangeState("Release");
        }
    });

release = new StatementState(self, "Release")
    .AddEnter(function() {
        // some effect...
    })
    .AddUpdate(function() {
        // ...
    });

state_machine
    .AddState(charge)
    .AddState(release);
```

You can pause and restart the per-state timer:

```gml
if (game_is_paused) {
    charge.TimerPause();
} else {
    charge.TimerRestart();
}
```

**Please note:** If you need to access a state from its own handlers or from other events, store it in an instance variable (like `charge` and `release` above), not a local `var`. Local variables only exist for the duration of the event or function where they are declared, while instance variables live for the lifetime of the instance.
{: .note}

Most of the time you can rely on `GetStateTime()` on the machine instead and skip per-state timers entirely.

---
### 8. State Change Hook for Logging & Signals

```gml
state_machine.SetStateChangeBehaviour(method(self, function() {
    EchoDebugInfo("State changed to: " + string(state_machine.GetStateName()));
    // You could also emit a signal here, update UI, etc.
}));
```

This runs for every transition, making it useful for:

- Debugging.
- Analytics.
- Emitting events into your own signal/event system.

---

### 9. Custom state events (advanced)

You can define your own event index and bind/run it manually. For example, add an `ANIMATION_END` event:

```gml
// scripts/scr_statement_macro/scr_statement_macro.gml (or your own macro script)
enum eStatementEvents {
    ENTER,
    EXIT,
    STEP,
    DRAW,
    ANIMATION_END, // custom
    NUM            // keep NUM last
}
```

In Create, bind a handler for that event:

```gml
/// obj_player Create
state_machine = new Statement(self);

var _attack = new StatementState(self, "Attack")
    .AddEnter(function() {
        sprite_index = spr_player_attack;
        image_index = 0;
    })
    .AddStateEvent(eStatementEvents.ANIMATION_END, function() {
        // Transition when the attack animation finishes
        state_machine.ChangeState("Idle");
    });

state_machine.AddState(_attack);
```

In the Animation End event of the object, run the custom event if present:

```gml
/// obj_player Animation End Event
if (state_machine.GetStateName() == "Attack"
&& state_machine.state.HasStateEvent(eStatementEvents.ANIMATION_END)) {
    state_machine.RunState(eStatementEvents.ANIMATION_END);
}
```

This pattern lets you hook into additional event points (like Animation End) while keeping logic organized in your states.

---

### 10. Inspecting or clearing a queued state

If you’re queuing transitions manually, you can inspect or clear the pending change:

```gml
/// Debug overlay
if (state_machine.HasQueuedState()) {
    var _queued = state_machine.GetQueuedStateName();
    draw_text(16, 16, "Queued state: " + string(_queued));
}

/// Cancel a queued change (e.g., input cancelled)
state_machine.ClearQueuedState();
```

---

### 11. History peek (previous states)

You can check where you’ve been:

```gml
// Last state name
var _prev = state_machine.GetPreviousStateName();

// All history entries
var _count = state_machine.GetHistoryCount();
for (var i = 0; i < _count; ++i) {
    var _st = state_machine.GetHistoryAt(i);
    if (!is_undefined(_st)) {
        draw_text(16, 48 + i * 16, "History " + string(i) + ": " + _st.name);
    }
}
```

Use `SetHistoryLimit(limit)` if you want to cap how many entries are kept.

---

### 12. Resetting / cleaning up a machine

When restarting or discarding a machine:

```gml
// Fully reset states and queues
state_machine.ClearStates();

// Cleanup timers owned by states on this machine (e.g., in Destroy)
state_machine.Destroy();

// Global nuke of all state timers across machines (e.g., when reloading a run)
StatementStateKillTimers();
```

---

## Gotchas & Best Practices

### Core Gotchas

1. **Don’t forget to call `Update()`**  
   If you don’t call `state_machine.Update()` each Step, your states will never run their Update handlers and queued transitions won’t process (unless you call `ProcessQueuedState()` manually).

2. **Draw is optional**  
   Only call `state_machine.Draw()` if you’re using per-state `AddDraw()` handlers. Combining regular object drawing and per-state drawing is fine, but be consistent.

3. **Owner must be valid**  
   Create states from valid contexts (where `self` exists) or pass a struct as the owner. Passing destroyed IDs or invalid values logs a severe warning and returns `undefined`.

---

### Advanced Gotchas

1. **`can_exit` gates transitions**  
   If a state sets `can_exit = false`, `ChangeState("Other")` will do nothing unless `force == true`. Make sure to set `can_exit = true` again when you actually want to leave.

2. **Queued transitions are one-shot**  
   Once a queued state is processed (or cleared), it’s gone.  
   If you want repeated attempts, call `QueueState()` again from your logic.

3. **History is for introspection, not control flow**  
   `previous_states` is great for debugging and analysis.  
   For actual control (e.g. temporary overlays), prefer `PushState` / `PopState` or `PreviousState()`.

4. **Per-state timers are independent of `GetStateTime()`**  
   Per-state timers use `Timer*` methods and underlying `time_source` objects. Once started, they tick based on the time-source, not on how often you call `Update()`.  
   They do not automatically match `GetStateTime()`; in almost all cases you should prefer `GetStateTime()` and only reach for per-state timers when you need that extra flexibility.

5. **Clean up when resetting**  
   - Use `ClearStates()` when you want to fully reset the machine’s states.  
   - Call `state_machine.Destroy()` in your instance’s Destroy/Cleanup event when you are done with a machine so that any per-state timers owned by its states are cleaned up.  
   - Use `StatementStateKillTimers()` if you want to globally destroy all state timers for all machines (e.g. when restarting a run).

---

That should give you a clean, beginner-friendly path (core sections) with clearly flagged advanced features for power users.
