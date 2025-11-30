---
layout: default
title: Scripting Reference
parent: Statement
nav_order: 1
---

# Scripting Reference

This page documents the public API of the state machine system.

It's split into:

- **Core API** - recommended reading for everyone.
- **Advanced API** - optional tools for more complex behaviours.

---

## Core API

### Core Types

#### `Statement(owner)`

Create a state machine bound to the given owner instance or struct.

```gml
state_machine = new Statement(self);
```

- `owner`: `ID.Instance` or `Struct`  
- **Returns:** `Struct.Statement`


#### `StatementState(owner, name)`

Create a new state bound to the given owner.

```gml
idle = new StatementState(self, "Idle");
```

- `owner`: `ID.Instance` or `Struct`  
- `name`: `String`  
- **Returns:** `Struct.StatementState`

If `owner` is neither an existing instance nor a struct, the constructor logs a severe debug message and returns `undefined`.

---

### Core Statement Methods

#### `AddState(state)`

Register a `StatementState` on this machine.

```gml
state_machine.AddState(idle);
```

- `state`: `Struct.StatementState`  
- **Returns:** `Struct.Statement`

The **first** state added becomes the active state and runs its `Enter` handler (if defined).

If a state with the same name already exists, it is replaced (with a warning).

---

#### `GetState([name])`

Get a state by name, or the current state if no name is provided.

```gml
var _current = state_machine.GetState();
var _idle    = state_machine.GetState("Idle");
```

- `name` *(optional)*: `String`  
- **Returns:** `Struct.StatementState` or `Undefined` if not found / no current state.

---

#### `GetStateName()`

Get the name of the current state.

```gml
var _name = state_machine.GetStateName();
```

- **Returns:** `String` or `Undefined`.

---

#### `ChangeState(name, [force])`

Immediately change to another state.

```gml
state_machine.ChangeState("Attack");
state_machine.ChangeState("Hitstun", true); // force, ignoring can_exit
```

- `name`: `String`  
- `force` *(optional)*: `Bool`  
- **Returns:** `Struct.StatementState` or `Undefined` if target doesn't exist.

Behaviour:

- If target doesn't exist: logs a warning and returns `undefined`.
- If target is already active: does nothing and returns current state.
- If current state has `can_exit == false` and `force == false`: refuses to change and returns current state.
- A manual `ChangeState` clears any queued transition.
- Otherwise:
  - Runs old state `Exit` (if present).
  - Updates history (`previous_state`, `previous_states`).
  - Switches `state` to the new state.
  - Resets `state_age` to 0.
  - Runs optional state-change hook.
  - Runs new state `Enter` (if present).

If an `Exit` handler changes state itself, the outer `ChangeState` respects that redirect and returns immediately.

---

#### `Update()`

Drive the state machine for one Step.

```gml
// Step Event
state_machine.Update();
```

- Processes any queued state (if auto-processing enabled).
- Runs the current state's `Update` handler (if present).
- Increments `state_age` (if there's an active state).
- **Returns:** whatever the state's Update handler returns, or `Undefined`.

---

#### `Draw()`

Optional helper to run the current state's Draw handler.

```gml
// Draw Event
state_machine.Draw();
```

- **Returns:** whatever the state's Draw handler returns, or `Undefined` if not implemented.

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

Manually set the current state's age.

```gml
state_machine.SetStateTime(0);
```

- `time`: `Real`  
- **Returns:** `Struct.Statement`

---

#### `ClearStates()`

Clear all states and reset the machine.

```gml
state_machine.ClearStates();
```

Clears:

- `states`, `states_array`
- `state`, `previous_state`, `previous_states`
- `state_stack`
- any queued state
- `state_age`

Returns the machine for chaining.

---

### Core StatementState Methods

#### `AddEnter(fn)`

Bind an `Enter` handler that runs once when the state becomes active.

```gml
idle.AddEnter(function() {
    sprite_index = spr_player_idle;
});
```

- `fn`: `Function` - automatically `method(owner, fn)` bound. In other words, the scope of the function runs from whoever has been supplied as the owner of the state (most often the instance running the state machine itself). This behaviour extends through to all the `fn` arguments in the other three `Add*()` methods below.
- **Returns:** `Struct.StatementState`

---

#### `AddUpdate(fn)`

Bind an `Update` handler that runs every Step while the state is active.

```gml
idle.AddUpdate(function() {
    // Idle behaviour
});
```

- **Returns:** `Struct.StatementState`

---

#### `AddExit(fn)`

Bind an `Exit` handler that runs once when the state stops being active.

```gml
idle.AddExit(function() {
    EchoDebugInfo("Leaving Idle");
});
```

- **Returns:** `Struct.StatementState`

---

#### `AddDraw(fn)`

Bind a `Draw` handler that runs each Draw while the state is active if you call `Statement.Draw()`.

```gml
idle.AddDraw(function() {
    draw_self();
});
```

- **Returns:** `Struct.StatementState`

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
- **Returns:** `Struct.Statement`

Default: `true`.

---

#### `QueueState(name, [force])`

Queue a state change to be processed later.

```gml
sm.QueueState("Attack");
```

- `name`: `String`  
- `force` *(optional)*: `Bool`  
- **Returns:** `Struct.Statement`

---

#### `ProcessQueuedState()`

Process any pending queued state change immediately.

```gml
sm.ProcessQueuedState();
```

- **Returns:** `Struct.StatementState` or `Undefined`

If the current state cannot exit (and `force` was not set when queuing), the queued transition remains pending. Otherwise the queue entry is cleared before calling `ChangeState()`.

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
var _next = sm.GetQueuedStateName();
```

- **Returns:** `String` or `Undefined`

---

#### `ClearQueuedState()`

Cancel any queued state without processing it.

```gml
sm.ClearQueuedState();
```

- **Returns:** `Struct.Statement`

---

### History & Introspection

#### `SetHistoryLimit(limit)`

Set how many previous states to keep in history.

```gml
sm.SetHistoryLimit(32);
```

- `limit`: `Real`  
- **Returns:** `Struct.Statement`

`limit <= 0` means unlimited history.

---

#### `GetHistoryCount()`

```gml
var _count = sm.GetHistoryCount();
```

- **Returns:** `Real` – length of `previous_states`.

---

#### `GetHistoryAt(index)`

Get a previous state by history index.

```gml
var _st = sm.GetHistoryAt(0);
```

- `index`: `Real`  
- **Returns:** `Struct.StatementState` or `Undefined` if invalid.

Use `is_undefined(st)` to check whether the index was valid before using the result.

---

#### `PreviousState()`

Quickly switch back to `previous_state`.

```gml
sm.PreviousState();
```

- **Returns:** `Struct.StatementState` or `Undefined`.

---

#### `GetPreviousStateName()`

Name of the most recent previous state.

```gml
var _prev = sm.GetPreviousStateName();
```

- **Returns:** `String` or `Undefined`.

---

#### `PrintStateNames()`

Print all state names registered on this machine (via debug system).

```gml
sm.PrintStateNames();
```

- **Returns:** `Struct.Statement`

---

### State Stack (Push / Pop)

#### `PushState(name, [force])`

Push current state onto a stack and change to `name`.

```gml
sm.PushState("Pause");
```

- `name`: `String`  
- `force` *(optional)*: `Bool`  
- **Returns:** `Struct.StatementState` or `Undefined`.

If the transition is blocked (for example `can_exit == false` and not forced), the current state is **not** pushed.

---

#### `PopState([force])`

Pop the last pushed state from the stack and change back to it.

```gml
sm.PopState();
```

- `force` *(optional)*: `Bool`  
- **Returns:** `Struct.StatementState` or `Undefined`.

Handles empty stacks and invalid entries safely.

---

### State Change Hook

#### `SetStateChangeBehaviour(fn)`

Register a callback to be run whenever the machine changes state.

```gml
sm.SetStateChangeBehaviour(method(self, function() {
    EchoDebugInfo("Now in state: " + string(state_machine.GetStateName()));
}));
```

- `fn`: `Function`  
- **Returns:** `Struct.Statement`

Called after the old state’s `Exit`, after `state` is updated, and before new state `Enter`. When the provided function is called, it will be given the previous state as an argument.

---

### Low-Level Event Running

Behind the scenes, each Statement state uses an array indexed with enums to decide what handler to run. For instance, `Update()`, runs the handler stored in the array position indexed by `eStatementEvents.STEP`. In most circumstances, you don't need to worry about this stuff, simply use `Update()` / `Draw()` and it will be handled automatically.

However, if you're confident editing Statement itself, you can extend `eStatementEvents` with your own custom event types. The enum is defined in `scr_statement_macro`.

> `eStatementEvents` is an enum defined inside the Statement framework (in `scr_statement_macro`) that maps the built-in handler types:
> 
> - `eStatementEvents.ENTER`
> - `eStatementEvents.STEP`
> - `eStatementEvents.EXIT`
> - `eStatementEvents.NUM` - a sentinel used internally as a "one past the end" value when looping over event types. It is **not** a real event and should not be passed to `RunState`.
{: .note}

> **Always insert new entries *before* `NUM`**; `NUM` is used as an "end of enum" marker when initialising internal arrays (such as the `state_event` array), so adding entries after `NUM` will break that initialisation. After editing the enum, you can then use
> the following methods to add or run custom state handlers, or check whether they exist.
{: .warning}

---

#### `AddStateEvent(event, fn)`

**StatementState method**. Bind a handler to a specific `eStatementEvents` index. This is your "custom" handler entry point.

**Create Event**
```gml
// Assuming you have added ANIMATION_END to the enum list (before NUM)
idle.AddStateEvent(eStatementEvents.ANIMATION_END, function() {
    // custom logic dealing with the end of animations in the idle state
});
```

- `event`: `Real` - one of the `eStatementEvents` values (`ENTER`, `EXIT`, `STEP`, `DRAW`).
- `fn`: `Function` - automatically `method(owner, fn)` bound.
- **Returns:** `Struct.StatementState`

---

#### `HasStateEvent(event)`

**StatementState** method. Check whether this state has a handler for a given `eStatementEvents` index.

```gml
if (!idle.HasStateEvent(eStatementEvents.ANIMATION_END)) {
    // maybe attach one
}
```

- `event`: `Real` - one of the `eStatementEvents` values (`ENTER`, `EXIT`, `STEP`, `DRAW`).
- **Returns:** `Bool`

---

#### `RunState(event)`

**Statement method**. Run a specific `eStatementEvents` index on the current state. This is scoped to the state machine itself, unlike the other two which are scoped to the state, to keep parity with the other handlers, like `state_machine.Update()`, etc.

**Animation End Event**
```gml
if (state_machine.GetState().HasStateEvent(eStatementEvents.ANIMATION_END)) {
    state_machine.RunState(eStatementEvents.ANIMATION_END);
}
```

- `event`: `Real` (usually one of the `eStatementEvents` values)  
- **Returns:** Any or `Undefined` if:
  - There is no active state, or
  - The chosen event is not implemented on the current state.

---

### Per-State Timers (Advanced)

Per-state timers live on individual `StatementState` instances and are considered **advanced**. In almost all cases (99% of use cases) you can ignore them and just use the machine-level state time via `GetStateTime()` / `SetStateTime()`.

Per-state timers are backed by GameMaker **time sources** and tick independently of `Update()`:
- Once a state becomes active and its timer is started, that timer advances every frame until you change out of that state or explicitly stop/pause/reset the timer.
- Because they use time sources internally, they can continue advancing even if the instance is deactivated or you temporarily stop calling `Update()`.

By contrast, `GetStateTime()` / `SetStateTime()` live on the **Statement** itself:
- Represent "how long the current state has been active (in frames)".
- Reset automatically on state change.
- Only increment when you call `Update()` on the machine.

If you're unsure which to use, start with `GetStateTime()` and ignore per-state timers; they exist mainly for very specialised cases where you need a timer tightly bound to a specific state's lifetime.

#### `TimerStart()`

Create and start a per-state timer (if not already created), resetting it to 0.

```gml
state.TimerStart();
```

- **Returns:** `Struct.StatementState`

---

#### `TimerSet(time)`

Set the per-state timer value.

```gml
state.TimerSet(30);
```

- `time`: `Real`  
- **Returns:** `Struct.StatementState`

---

#### `TimerGet()`

Get the current per-state timer value.

```gml
var _t = state.TimerGet();
```

- **Returns:** `Real`

---

#### `TimerPause()`

Pause the per-state timer.

```gml
state.TimerPause();
```

- **Returns:** `Struct.StatementState`

---

#### `TimerRestart()`

Restart the per-state timer if it exists.

```gml
state.TimerRestart();
```

- **Returns:** `Struct.StatementState`

---

#### `TimerKill()`

Kill (destroy) the per-state timer.

```gml
state.TimerKill();
```

- **Returns:** `Struct.StatementState`

---

### Machine-Level Access to Per-State Timer

### Cleanup & Global Helpers

#### `RemoveState(name)`

Remove a state by name from this machine.

```gml
sm.RemoveState("Debug");
```

- `name`: `String`  
- **Returns:** `Struct.Statement`

---

#### `Destroy()`

Helper to clean up state-specific timers for all states registered on this machine (current and history).

```gml
sm.Destroy();
```

Call this if you are discarding a machine and want to ensure no associated timers continue ticking.

---

#### `StatementStateKillTimers()`

Global helper: destroy all state timers registered in `global.__statement_timers` and clear the array.

```gml
StatementStateKillTimers();
```

Use this if you want a global "nuke all state timers" reset, e.g. when restarting a run or changing rooms.

---
