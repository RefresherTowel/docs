---
layout: default
title: Usage & Examples
parent: Statement
nav_order: 2
---

# Usage & Examples

This page shows how to use Statement in practice, split into:

- **Core usage** - basic patterns.
- **Advanced usage** - optional patterns for more complex behaviour.
- **Gotchas** - things to keep in mind.

---

## Core Usage

### 1. Basic Hello World

**Create Event**
```gml
state_machine = new Statement(self);

var _idle = new StatementState(self, "Idle")
    .AddEnter(function() {
        EchoDebugInfo("Entered Idle");
    })
    .AddUpdate(function() {
        image_angle += 1;
    });

state_machine.AddState(_idle);
```

**Step Event**
```gml
state_machine.Update();
```

**Draw Event (optional)**
```gml
state_machine.Draw();
```

This sets up:

- A `Statement` state machine bound to `self`.
- One state, `Idle`, with `Enter` + `Update` handlers.
- The state machine driven from Step (and optionally Draw).

---

### 2. Multiple States with Simple Transitions

**Create Event**
```gml
state_machine = new Statement(self);

// Idle
var _idle = new StatementState(self, "Idle")
    .AddEnter(function() {
        sprite_index = spr_player_idle;
        hsp = vsp = 0;
    })
    .AddUpdate(function() {
        if (keyboard_check_pressed(vk_anykey)) {
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
```

**Step Event**
```gml
state_machine.Update();
```

**Draw Event**
```gml
state_machine.Draw();
```

Now if you press any key while in the Idle state, it will transition to the Move state automatically. If you're not pressing a movement key while in the Move state, it will transition back to the Idle state.

---

### 3. Using `GetStateTime()` for Behaviour

```gml
var _attack = new StatementState(self, "Attack")
    .AddEnter(function() {
        sprite_index = spr_player_attack;
        image_index = 0;
    })
    .AddUpdate(function() {
        // Stay in Attack for 20 frames
        if (state_machine.GetStateTime() >= 20) {
            state_machine.ChangeState("Idle");
        }
    });

state_machine.AddState(_attack);
```

Because `state_machine` resets `state_age` automatically on state change, you don't need to call `SetStateTime(0)` when changing into/out of a state.

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

Because transitions are queued, the rest of the current event runs with the **old** state, and `Attack` starts cleanly next frame.

---

### 5. Manual Queue Processing

If you want explicit control over when queued transitions happen:

**Create Event**
```gml
state_machine = new Statement(self)
    .SetQueueAutoProcessing(false);
```

**Step Event**
```gml
// Do your own logic...
// When ready to apply queued transitions:
state_machine.ProcessQueuedState();
state_machine.Update();
```

Now you can insert queue processing at a specific spot in your step pipeline.

---

### 6. Pausing a State Machine

You can pause automatic processing (Update/queue/declarative transitions) while still allowing manual transitions.

```gml
// e.g., global pause toggle
if (game_paused) {
    state_machine.SetPaused(true);
} else {
    state_machine.SetPaused(false);
}

// Step Event
if (!state_machine.IsPaused()) {
    state_machine.Update();
}
```

Pausing does **not** prevent manual `ChangeState` calls or `Draw()`; it just freezes the automatic flow inside `Update()`.

---

### 7. Using Push/Pop for Overlays (Pause State)

**Create Event**
```gml
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
```

**Step Event**
```gml
if (keyboard_check_released(vk_escape)
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

### 8. Per-State Timers for More Complex Timing

**Create Event**
```gml
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

If you need to access a state from its own handlers or from other events, store it in an instance variable (like `charge` and `release` above), not a local `var`. Local variables only exist for the duration of the event or function where they are declared, while instance variables live for the lifetime of the instance. Alternatively, if you have access to the state machine itself, you can retrieve specific states via the `GetState()` method.
{: .note}

Almost all of the time you can rely on `GetStateTime()` on the machine instead and skip per-state timers entirely, they are implemented for very niche circumstances.

---
### 9. State Change Hook for Logging & Signals

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

> The function given as the argument for `SetStateChangeBehaviour()` is **NOT** automatically bound to the owner of the state. This is done to allow you greater expression in how you might want it scoped (for instance, scoping it to your debug logger or something). This is why we are using `method()` explicitly to bind the scope in this example.
{: .warning}

---

### 10. Declarative transitions

Add transitions to a state that fire automatically when conditions pass. They are evaluated after each `Update()`.

```gml
var _run = new StatementState(self, "Run")
    .AddUpdate(function() {
        // run logic...
    })
    .AddTransition("Idle", function() {
        return abs(hsp) < 0.05; // condition bound to owner via method()
    })
    .AddTransition("Jump", function() {
        return keyboard_check_pressed(vk_space);
    });
```

- Transitions are checked in the order they were added; the first that returns `true` fires.
- You can attach a payload via `ChangeState` or `EvaluateTransitions(payload)`, then read it in the next state's `Enter` via `GetLastTransitionData()`.
- If you need to disable automatic evaluation (for custom ordering), set `SetQueueAutoProcessing(false)` and call `EvaluateTransitions()` manually.

---

### 11. Transition payloads & ensuring states

Carry data across transitions and avoid redundant changes.

```gml
// When taking damage, carry a payload into the new state.
state_machine.ChangeState("Hitstun", { damage: last_damage });

// In the Hitstun state's Enter
hitstun.AddEnter(function() {
    var _payload = state_machine.GetLastTransitionData();
    if (is_struct(_payload)) hp -= _payload.damage;
});

// Only change if not already in Idle
state_machine.EnsureState("Idle");

// Quick checks
if (state_machine.IsInState("Attack")) {
    // do something
}
```

Use `GetQueuedStateData()` when inspecting queued transitions, and `WasPreviouslyInState(name, depth)` when reasoning about history.

---

### 12. Custom state events (advanced)

You can define your own event index and bind/run it manually. For example, add an `ANIMATION_END` enum:

**`scr_statement_macro` Script**
```gml
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

**Create Event**
```gml
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

**Animation End Event**
```gml
if (state_machine.GetState().HasStateEvent(eStatementEvents.ANIMATION_END)) {
    state_machine.RunState(eStatementEvents.ANIMATION_END);
}
```

This pattern lets you hook into additional event points (like Animation End) while keeping logic organized in your states.

---

### 13. Inspecting or clearing a queued state

If you're queuing transitions manually, you can inspect or clear the pending change:

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

### 14. History peek (previous states)

You can check where you've been:

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

// Quick debug dump
state_machine.PrintStateHistory(5); // or state_machine.DebugDescribe();
```

Use `SetHistoryLimit(limit)` if you want to cap how many entries are kept.

---

### 15. Resetting / cleaning up a machine

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

1. **Don't forget to call `Update()`**  
   If you don't call `state_machine.Update()` each Step, your states will never run their Update handlers and queued transitions won't process (unless you call `ProcessQueuedState()` manually).

2. **Draw is optional**  
   Only call `state_machine.Draw()` if you're using per-state `AddDraw()` handlers. Combining regular object drawing and per-state drawing is fine, but be consistent.

3. **Owner must be valid**  
   Create states from valid contexts (where `self` exists) or pass a struct as the owner. Passing destroyed IDs or invalid values logs a severe warning and returns `undefined`.

4. **Debug helpers are your friend**  
   `DebugDescribe()` and `PrintStateHistory([limit])` emit quick summaries to your debug logger, which helps confirm wiring during development.

---

### Advanced Gotchas

1. **Locked states (`can_exit` flag) gates transitions**  
   If a state is locked via `LockExit();` (or `SetCanExit(false);`), then `ChangeState("Other")` will do nothing unless the `force` argument is true. Make sure to set `UnlockExit()` (or `SetCanExit(true);`) again when you actually want to leave.

2. **Queued transitions are one-shot**  
   Once a queued state is processed (or cleared), it's gone.
   If you want repeated attempts, call `QueueState()` again from your logic.

3. **History is for introspection, not control flow**  
   `previous_states` is great for debugging and analysis.  
   For actual control (e.g. temporary overlays), prefer `PushState` / `PopState` or `PreviousState()`.

4. **Per-state timers are independent of `GetStateTime()`**  
   Per-state timers use `Timer*` methods and GMs underlying `time_source` functionality. Once started, they tick based on the time-source, not on how often you call `Update()`.  
   They do not automatically match `GetStateTime()`; in almost all cases you should prefer `GetStateTime()` and only reach for per-state timers when you need that extra flexibility.

5. **Clean up when resetting**  
   - Use `ClearStates()` when you want to fully reset the machine's states.
   - Call `state_machine.Destroy()` in your instance's Destroy/Cleanup event when you are done with a machine so that any per-state timers owned by its states are cleaned up.
   - Use `StatementStateKillTimers()` if you want to globally destroy all state timers for all machines (e.g. when restarting a run).
