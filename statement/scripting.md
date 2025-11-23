---
layout: default
title: Scripting Reference
parent: Statement
nav_order: 1
---

# Scripting Reference

This page documents the public API of the state machine system.

It’s split into:

- **Core API** – recommended reading for everyone.
- **Advanced API** – optional tools for more complex behaviours.

---

## Core API

### Core Types

#### `StateMachine(owner)`

Create a state machine bound to the given owner instance or struct.

```gml
var sm = StateMachine(self);
```

- `owner`: `Id.Instance` or `Struct`  
- **Returns:** `Struct.StateMachine`


#### `State(owner, name)`

Create a new state bound to the given owner.

```gml
var idle = State(self, "Idle");
```

- `owner`: `Id.Instance` or `Struct`  
- `name`: `String`  
- **Returns:** `Struct.State`

If `owner` is neither an existing instance nor a struct, the constructor logs a severe debug message and returns `undefined`.

---

### Core StateMachine Methods

#### `AddState(state)`

Register a `State` on this machine.

```gml
sm.AddState(idle);
```

- `state`: `Struct.State`  
- **Returns:** `Struct.StateMachine`

The **first** state added becomes the active state and runs its `Enter` handler (if defined).

If a state with the same name already exists, it is replaced (with a warning).

---

#### `GetState([name])`

Get a state by name, or the current state if no name is provided.

```gml
var current = sm.GetState();
var idle    = sm.GetState("Idle");
```

- `name` *(optional)*: `String`  
- **Returns:** `Struct.State` or `Undefined` if not found / no current state.

---

#### `GetStateName()`

Get the name of the current state.

```gml
var name = sm.GetStateName();
```

- **Returns:** `String` or `Undefined`.

---

#### `ChangeState(name, [force])`

Immediately change to another state.

```gml
sm.ChangeState("Attack");
sm.ChangeState("Hitstun", true); // force, ignoring can_exit
```

- `name`: `String`  
- `force` *(optional)*: `Bool`  
- **Returns:** `Struct.State` or `Undefined` if target doesn’t exist.

Behaviour:

- If target doesn’t exist: logs a warning and returns `undefined`.
- If target is already active: does nothing and returns current state.
- If current state has `can_exit == false` and `force == false`: refuses to change and returns current state.
- Otherwise:
  - Runs old state `Exit` (if present).
  - Updates history (`previous_state`, `previous_states`).
  - Switches `state` to the new state.
  - Resets `state_age` to 0.
  - Runs optional state-change hook.
  - Runs new state `Enter` (if present).

---

#### `Update()`

Drive the state machine for one Step.

```gml
// Step Event
state_machine.Update();
```

- Processes any queued state (if auto-processing enabled).
- Runs the current state’s `Update` handler (if present).
- Increments `state_age` (if there’s an active state).
- **Returns:** whatever the state’s Update handler returns, or `Undefined`.

---

#### `Draw()`

Optional helper to run the current state’s Draw handler.

```gml
// Draw Event
state_machine.Draw();
```

- **Returns:** whatever the state’s Draw handler returns, or `Undefined` if not implemented.

Use only if you want per-state drawing.

---

#### `GetStateTime()`

Get how long (in frames) the current state has been active.

```gml
if (state_machine.GetStateTime() > 30) {
    // half a second at 60 FPS
}
```

- **Returns:** `Real`

Automatically reset on each state change.

---

#### `SetStateTime(time)`

Manually set the current state’s age.

```gml
state_machine.SetStateTime(0);
```

- `time`: `Real`  
- **Returns:** `Struct.StateMachine`

---

#### `ClearStates()`

Clear all states and reset the machine.

```gml
sm.ClearStates();
```

Clears:

- `states`, `states_array`
- `state`, `previous_state`, `previous_states`
- `state_stack`
- any queued state
- `state_age`

Returns the machine for chaining.

---

### Core State Methods

#### `AddEnter(fn)`

Bind an `Enter` handler that runs once when the state becomes active.

```gml
idle.AddEnter(function() {
    sprite_index = spr_player_idle;
});
```

- `fn`: `Function` — automatically `method(owner, fn)` bound.  
- **Returns:** `Struct.State`

---

#### `AddUpdate(fn)`

Bind an `Update` handler that runs every Step while the state is active.

```gml
idle.AddUpdate(function() {
    // Idle behaviour
});
```

- **Returns:** `Struct.State`

---

#### `AddExit(fn)`

Bind an `Exit` handler that runs once when the state stops being active.

```gml
idle.AddExit(function() {
    DebugInfo("Leaving Idle");
});
```

- **Returns:** `Struct.State`

---

#### `AddDraw(fn)`

Bind a `Draw` handler that runs each Draw while the state is active if you call `StateMachine.Draw()`.

```gml
idle.AddDraw(function() {
    draw_self();
});
```

- **Returns:** `Struct.State`

---

## Advanced API

The following features are optional. You can ignore them unless your project specifically benefits from them.

---

### Queueing

#### `SetQueueAutoProcessing(enabled)`

Control whether queued transitions are automatically processed inside `Update()`.

```gml
sm.SetQueueAutoProcessing(true);
```

- `enabled`: `Bool`  
- **Returns:** `Struct.StateMachine`

Default: `true`.

---

#### `QueueState(name, [force])`

Queue a state change to be processed later.

```gml
sm.QueueState("Attack");
```

- `name`: `String`  
- `force` *(optional)*: `Bool`  
- **Returns:** `Struct.StateMachine`

---

#### `ProcessQueuedState()`

Process any pending queued state change immediately.

```gml
sm.ProcessQueuedState();
```

- **Returns:** `Struct.State` or `Undefined`

Clears the queue before calling `ChangeState()`.

---

#### `HasQueuedState()`

Check if a queued state is pending.

```gml
if (sm.HasQueuedState()) { /* … */ }
```

- **Returns:** `Bool`

---

#### `GetQueuedStateName()`

Get the name of the queued state, if any.

```gml
var next = sm.GetQueuedStateName();
```

- **Returns:** `String` or `Undefined`

---

#### `ClearQueuedState()`

Cancel any queued state without processing it.

```gml
sm.ClearQueuedState();
```

- **Returns:** `Struct.StateMachine`

---

### History & Introspection

#### `SetHistoryLimit(limit)`

Set how many previous states to keep in history.

```gml
sm.SetHistoryLimit(32);
```

- `limit`: `Real`  
- **Returns:** `Struct.StateMachine`

`limit <= 0` means unlimited history.

---

#### `GetHistoryCount()`

```gml
var count = sm.GetHistoryCount();
```

- **Returns:** `Real` – length of `previous_states`.

---

#### `GetHistoryAt(index)`

Get a previous state by history index.

```gml
var st = sm.GetHistoryAt(0);
```

- `index`: `Real`  
- **Returns:** `Struct.State` or `-1` if invalid.

---

#### `PreviousState()`

Quickly switch back to `previous_state`.

```gml
sm.PreviousState();
```

- **Returns:** `Struct.State` or `Undefined`.

---

#### `GetPreviousStateName()`

Name of the most recent previous state.

```gml
var prev = sm.GetPreviousStateName();
```

- **Returns:** `String` or `Undefined`.

---

#### `PrintStateNames()`

Print all state names registered on this machine (via debug system).

```gml
sm.PrintStateNames();
```

- **Returns:** `Struct.StateMachine`

---

### State Stack (Push / Pop)

#### `PushState(name, [force])`

Push current state onto a stack and change to `name`.

```gml
sm.PushState("Pause");
```

- `name`: `String`  
- `force` *(optional)*: `Bool`  
- **Returns:** `Struct.State` or `Undefined`.

---

#### `PopState([force])`

Pop the last pushed state from the stack and change back to it.

```gml
sm.PopState();
```

- `force` *(optional)*: `Bool`  
- **Returns:** `Struct.State` or `Undefined`.

Handles empty stacks and invalid entries safely.

---

### State Change Hook

#### `SetStateChangeBehaviour(fn)`

Register a callback to be run whenever the machine changes state.

```gml
sm.SetStateChangeBehaviour(method(self, function() {
    DebugInfo("Now in state: " + string(state_machine.GetStateName()));
}));
```

- `fn`: `Function`  
- **Returns:** `Struct.StateMachine`

Called after the old state’s `Exit`, after `state` is updated, and before new state `Enter`.

---

### Low-Level Event Running

#### `RunState(event)`

Run a specific `eStateEvents` index on the current state.

```gml
sm.RunState(eStateEvents.ENTER);
```

- `event`: `Real`  
- **Returns:** Any or `Undefined` if:
  - No active state, or
  - Event not implemented.

Normally you don’t need this; use `Update()` / `Draw()` instead.

---

### Per-State Timers (Advanced)

These live on `State` and are considered **advanced**. If you only need “time in state”, prefer `GetStateTime()` on the machine.

#### `TimerStart()`

Create and start a per-state timer (if not already created), resetting it to 0.

```gml
state.TimerStart();
```

- **Returns:** `Struct.State`

---

#### `TimerSet(time)`

Set the per-state timer value.

```gml
state.TimerSet(30);
```

- `time`: `Real`  
- **Returns:** `Struct.State`

---

#### `TimerGet()`

Get the current per-state timer value.

```gml
var t = state.TimerGet();
```

- **Returns:** `Real`

---

#### `TimerPause()`

Pause the per-state timer.

```gml
state.TimerPause();
```

- **Returns:** `Struct.State`

---

#### `TimerRestart()`

Restart the per-state timer if it exists.

```gml
state.TimerRestart();
```

- **Returns:** `Struct.State`

---

#### `TimerKill()`

Kill (destroy) the per-state timer.

```gml
state.TimerKill();
```

- **Returns:** `Struct.State`

---

### Machine-Level Access to Per-State Timer

#### `AdvGetStateTimer()`

Get the current state’s per-state timer value (advanced feature).

```gml
var t = sm.AdvGetStateTimer();
```

- **Returns:** `Real` or `Undefined` if there is no active state.

---

#### `AdvSetStateTimer(time)`

Set the current state’s per-state timer value (advanced feature).

```gml
sm.AdvSetStateTimer(0);
```

- `time`: `Real`  
- **Returns:** `Struct.StateMachine`

---

### Cleanup & Global Helpers

#### `RemoveState(name)`

Remove a state by name from this machine.

```gml
sm.RemoveState("Debug");
```

- `name`: `String`  
- **Returns:** `Struct.StateMachine`

---

#### `Destroy()`

Helper to clean up state-specific timers for all states registered on this machine (current and history).

```gml
sm.Destroy();
```

Call this if you are discarding a machine and want to ensure no associated timers continue ticking.

---

#### `StateKillTimers()`

Global helper: destroy all state timers registered in `global.__state_timers` and clear the array.

```gml
StateKillTimers();
```

Use this if you want a global “nuke all state timers” reset, e.g. when restarting a run or unloading a big system.

---
