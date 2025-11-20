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
state_machine = StateMachine(self);

var idle = State(self, "Idle")
    .AddEnter(function() {
        DebugInfo("Entered Idle");
    })
    .AddUpdate(function() {
        image_angle += 1;
    });

state_machine.AddState(idle);


/// Step Event
state_machine.Update();


/// Draw Event (optional)
state_machine.Draw();
```

This sets up:

- A `StateMachine` bound to `self`.
- One state, `Idle`, with `Enter` + `Update` handlers.
- The machine driven from Step (and optionally Draw).

---

### 2. Multiple States with Simple Transitions

```gml
/// Create Event
state_machine = StateMachine(self);

// Idle
var idle = State(self, "Idle")
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
var move = State(self, "Move")
    .AddEnter(function() {
        sprite_index = spr_player_move;
    })
    .AddUpdate(function() {
        var dx = keyboard_check(ord("D")) - keyboard_check(ord("A"));
        var dy = keyboard_check(ord("S")) - keyboard_check(ord("W"));

        hsp = dx * 4;
        vsp = dy * 4;

        x += hsp;
        y += vsp;

        if (dx == 0 && dy == 0) {
            state_machine.ChangeState("Idle");
        }
    });

state_machine
    .AddState(idle)
    .AddState(move);


/// Step Event
state_machine.Update();


/// Draw Event
state_machine.Draw();
```

---

### 3. Using `GetStateTime()` for Behaviour

```gml
var attack = State(self, "Attack")
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

state_machine.AddState(attack);
```

Because `state_machine` resets `state_age` automatically on state change, you can often skip the explicit `SetStateTime(0)`.

---

## Advanced Usage

### 4. Queued Transitions to Avoid Mid-Update Re-entry

```gml
var move = State(self, "Move")
    .AddUpdate(function() {
        // movement logic...

        if (mouse_check_button_pressed(mb_left)) {
            // Queue an attack; actual change happens at next Update
            state_machine.QueueState("Attack");
        }
    });

var attack = State(self, "Attack")
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
    .AddState(move)
    .AddState(attack);
```

Because transitions are queued, the rest of the current `Update` runs in the **old** state, and `Attack` starts cleanly next frame.

---

### 5. Manual Queue Processing

If you want explicit control over when queued transitions happen:

```gml
/// Create
state_machine = StateMachine(self)
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
state_machine = StateMachine(self);

// Existing states: Idle, Move, Attack... (omitted)

// Pause overlay
var pause = State(self, "Pause")
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

state_machine.AddState(pause);


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
var charge = State(self, "Charge")
    .AddEnter(function() {
        TimerStart(); // per-state timer
    })
    .AddUpdate(function() {
        // Charge for at least 60 frames
        if (TimerGet() >= 60) {
            state_machine.ChangeState("Release");
        }
    });

var release = State(self, "Release")
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

You can pause and restart the timer:

```gml
if (game_is_paused) {
    TimerPause();
} else {
    TimerRestart();
}
```

---

### 8. State Change Hook for Logging & Signals

```gml
state_machine.SetStateChangeBehaviour(method(self, function() {
    DebugInfo("State changed to: " + string(state_machine.GetStateName()));
    // You could also emit a signal here, update UI, etc.
}));
```

This runs for every transition, making it useful for:

- Debugging.
- Analytics.
- Emitting events into your own signal/event system.

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
   Per-state timers are controlled by `Timer*` methods and `time_source`.  
   They do not automatically match `GetStateTime()`; use whichever better fits your logic.

5. **Clean up when resetting**  
   - Use `ClearStates()` when you want to fully reset the machine.  
   - Use `StateKillTimers()` if you want to globally destroy all state timers for all machines.

---

That should give you a clean, beginner-friendly path (core sections) with clearly flagged advanced features for power users.
