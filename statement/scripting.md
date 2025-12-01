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


#### `IsInState(name_or_state)`

Check whether the current state matches the supplied name or state struct.

```gml
if (state_machine.IsInState("Hurt")) {
    // Already in the Hurt state.
}

if (state_machine.IsInState(my_attack_state)) {
    // Using a direct state reference.
}
```

- `name_or_state`: `String` or `Struct.StatementState`
- **Returns:** `Bool`

Accepts either a state name or a `StatementState` struct. If called with an unsupported type or when there is no active state, it returns `false` (and logs a warning for unsupported types).

---

#### `EnsureState(name, [data], [force])`

Ensure that the current state matches the supplied name. If it is already active, no transition occurs.

```gml
// Make sure we are in Idle; only changes if needed.
state_machine.EnsureState("Idle");

// Ensure Hurt with a payload.
state_machine.EnsureState("Hurt", { damage: _damage; });
```

- `name`: `String`
- `data` *(optional)*: `Any` - payload attached to the transition if a change is required.
- `force` *(optional)*: `Bool`
- **Returns:** `Struct.StatementState` or `Undefined` if the target does not exist.

Internally this is equivalent to checking the current state's name and only calling `ChangeState` when different, which avoids redundant transitions and Exit/Enter calls.


#### `ChangeState(name, [data], [force])`

Immediately change to another state, optionally with a transition payload.

```gml
state_machine.ChangeState("Attack");
state_machine.ChangeState("Hitstun", { damage: 5 }, true); // payload + force
```

- `name`: `String`  
- `data` *(optional)*: `Any` - payload retrievable via `GetLastTransitionData()`.  
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
  - Runs optional state-change hook (see `SetStateChangeBehaviour`).
  - Runs new state `Enter` (if present).

If an `Exit` handler changes state itself, the outer `ChangeState` respects that redirect and returns immediately.

---

#### `Update()`

Drive the state machine for one Step.

```gml
// Step Event
state_machine.Update();
```

- Skips processing when `IsPaused()` is true.
- Processes any queued state (if auto-processing enabled).
- Runs the current state's `Update` handler (if present).
- Evaluates declarative transitions defined on the current state.
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
if (state_machine.GetStateTime() > get_game_speed(gamespeed_fps) * 0.5) {
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

### Pausing

#### `SetPaused(paused)`

Pause or resume the state machine. When paused, `Update()` skips queue processing, STEP handlers, declarative transitions, and state age increments. Manual `ChangeState` calls still work.

```gml
state_machine.SetPaused(true);  // freeze
state_machine.SetPaused(false); // resume
```

- `paused`: `Bool`
- **Returns:** `Struct.Statement`

---

#### `IsPaused()`

Check whether the machine is currently paused.

```gml
if (state_machine.IsPaused()) { /* skip logic */ }
```

- **Returns:** `Bool`

---

### Queueing

#### `SetQueueAutoProcessing(enabled)`

Control whether queued transitions are automatically processed inside `Update()`.

```gml
state_machine.SetQueueAutoProcessing(true);
```

- `enabled`: `Bool`  
- **Returns:** `Struct.Statement`

Default: `true`.

---

#### `QueueState(name, [data], [force])`

Queue a state change to be processed later.

```gml
state_machine.QueueState("Attack");
```

- `name`: `String`  
- `data` *(optional)*: `Any` - payload retrievable via `GetLastTransitionData()` if the transition succeeds.  
- `force` *(optional)*: `Bool`  
- **Returns:** `Struct.Statement`

---

#### `ProcessQueuedState()`

Process any pending queued state change immediately.

```gml
state_machine.ProcessQueuedState();
```

- **Returns:** `Struct.StatementState` or `Undefined`

If the current state cannot exit (and `force` was not set when queuing), the queued transition remains pending. Otherwise the queue entry is cleared before calling `ChangeState()`.

---

#### `HasQueuedState()`

Check if a queued state is pending.

```gml
if (state_machine.HasQueuedState()) { /* ... */ }
```

- **Returns:** `Bool`

---

#### `GetQueuedStateName()`

Get the name of the queued state, if any.

```gml
var _next = state_machine.GetQueuedStateName();
```

- **Returns:** `String` or `Undefined`

---

#### `GetQueuedStateData()`

Get the payload attached to a queued state, if any.

```gml
var _payload = state_machine.GetQueuedStateData();
```

- **Returns:** `Any` or `Undefined`

---

#### `ClearQueuedState()`

Cancel any queued state without processing it.

```gml
state_machine.ClearQueuedState();
```

- **Returns:** `Struct.Statement`

---

### History & Introspection

#### `SetHistoryLimit(limit)`

Set how many previous states to keep in history.

```gml
state_machine.SetHistoryLimit(32);
```

- `limit`: `Real`  
- **Returns:** `Struct.Statement`

`limit <= 0` means unlimited history.

---

#### `GetHistoryCount()`

Get how many entries are currently stored in the previous state history.

```gml
var _count = state_machine.GetHistoryCount();
```

- **Returns:** `Real`

---

#### `GetHistoryAt(index)`

Get a previous state by history index.

```gml
var _st = state_machine.GetHistoryAt(0);
```

- `index`: `Real`  
- **Returns:** `Struct.StatementState` or `Undefined` if the index is invalid.

---

#### `ClearHistory()`

Clear the previous state history without affecting the current state.

```gml
state_machine.ClearHistory();
```

- **Returns:** `Struct.Statement`

---

#### `PreviousState([data], [force])`

Convenience helper to change back to the most recent previous state.

```gml
state_machine.PreviousState();
```

- `data` *(optional)*: `Any` - payload attached to this transition.
- `force` *(optional)*: `Bool`
- **Returns:** `Struct.StatementState` or `Undefined`.

This is roughly equivalent to:

```gml
state_machine.ChangeState(state_machine.GetPreviousStateName(), data, force);
```

but is safer and handles edge cases for you.

---

#### `GetPreviousStateName()`

Get the name of the most recent previous state in history.

```gml
var _prev = state_machine.GetPreviousStateName();
```

- **Returns:** `String` or `Undefined`.

---

#### `WasPreviouslyInState(name, [depth])`

Check whether the state at the given history depth matches the supplied name.

```gml
// Was the last state "Attack"?
if (state_machine.WasPreviouslyInState("Attack")) {
    // ...
}

// Was the state three transitions ago "Patrol"?
if (state_machine.WasPreviouslyInState("Patrol", 3)) {
    // ...
}
```

- `name`: `String`
- `depth` *(optional)*: `Real` - 1 checks the most recent previous state, 2 checks the one before that, etc. Defaults to 1.
- **Returns:** `Bool`

Returns `false` if there is not enough history, or if the entry at that depth is not a valid `StatementState`.

---

#### `GetLastTransitionData()`

Get the payload attached to the most recent successful state transition, if any.

```gml
var _data = state_machine.GetLastTransitionData();
if (is_struct(_data)) {
    EchoDebugInfo("Last transition damage: " + string(_data.damage));
}
```

- **Returns:** `Any` or `Undefined`.

This works for direct `ChangeState`, queued transitions, stack pushes/pops, and other transitions that go through the machine.

---

#### `PrintStateNames()`

Print all state names registered on this machine (via the debug system).

```gml
state_machine.PrintStateNames();
```

- **Returns:** `Struct.Statement`

---

#### `DebugDescribe()`

Return a one-line debug description of this state machine, including owner, current state, previous state, age, queued state (if any), state stack depth, and history count.

```gml
EchoDebugInfo(state_machine.DebugDescribe());
```

- **Returns:** `String`

Useful for quick logging of state machine status without having to inspect multiple values manually.

---

#### `PrintStateHistory([limit])`

Print the previous state history for this machine, from most recent backwards.

```gml
// Dump entire history
state_machine.PrintStateHistory();

// Or only the last 5 entries
state_machine.PrintStateHistory(5);
```

- `limit` *(optional)*: `Real` - maximum number of history entries to print. Use 0 or a negative value to print the full history.
- **Returns:** `Struct.Statement`

By default the method prints a short summary (similar to `DebugDescribe()`) and then each history entry with its index.


### State Stack (Push / Pop)

#### `PushState(name, [force])`

Push current state onto a stack and change to `name`.

```gml
state_machine.PushState("Pause");
```

- `name`: `String`  
- `force` *(optional)*: `Bool`  
- **Returns:** `Struct.StatementState` or `Undefined`.

If the transition is blocked (for example `can_exit == false` and not forced), the current state is **not** pushed.

---

#### `PopState([data], [force])`

Pop the last pushed state from the stack and change back to it.

```gml
state_machine.PopState();
```

- `data` *(optional)*: `Any` - payload for this transition.  
- `force` *(optional)*: `Bool`  
- **Returns:** `Struct.StatementState` or `Undefined`.

Handles empty stacks and invalid entries safely.

---

#### `GetStateStackDepth()`

Number of entries currently on the state stack.

```gml
var _depth = state_machine.GetStateStackDepth();
```

- **Returns:** `Real`

---

#### `PeekStateStack()`

Peek at the most recently pushed state without popping it.

```gml
var _top = state_machine.PeekStateStack();
```

- **Returns:** `Struct.StatementState` or `Undefined`.

---

#### `ClearStateStack()`

Clear all entries from the state stack without changing the current state.

```gml
state_machine.ClearStateStack();
```

- **Returns:** `Struct.Statement`

---

### State Change Hook

#### `SetStateChangeBehaviour(fn)`

Register a callback to be run whenever the machine changes state.

```gml
state_machine.SetStateChangeBehaviour(method(self, function() {
    EchoDebugInfo("Now in state: " + string(state_machine.GetStateName()));
}));
```

- `fn`: `Function` - called as `fn(previous_state, transition_data)`; both may be `undefined`.  
- **Returns:** `Struct.Statement`

Called after the old state's `Exit`, after `state` is updated, and before new state `Enter`.

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

### Exit Control & Declarative Transitions (StatementState)

#### `SetCanExit(can_exit)` / `LockExit()` / `UnlockExit()`

Control whether a state can be exited without forcing.

```gml
state.LockExit();      // block transitions unless force == true
state.SetCanExit(true); // equivalent to UnlockExit()
```

- `can_exit`: `Bool`
- **Returns:** `Struct.StatementState`

When `can_exit == false`, `ChangeState`/queued transitions will only leave this state if `force == true`.

---

#### `AddTransition(target_name, condition, [force])`

Add a declarative transition that will be evaluated each `Update()` while the state is active. When the condition returns true, the machine changes to `target_name`.

```gml
idle.AddTransition("Run", function() {
    return abs(hsp) > 0.1;
});
```

- `target_name`: `String`
- `condition`: `Function` - automatically bound to the owner via `method(owner, fn)`.
- `force` *(optional)*: `Bool` - ignore `can_exit` when firing.
- **Returns:** `Struct.StatementState`

Transitions are checked in the order they were added; the first condition returning true will fire.

---

#### `ClearTransitions()`

Remove all declarative transitions from this state.

```gml
state.ClearTransitions();
```

- **Returns:** `Struct.StatementState`

---

#### `EvaluateTransitions()`

Evaluate this state's declarative transitions and return the first matching record.

```gml
var _tr = state.EvaluateTransitions();
```

- **Returns:** `Struct` `{ target_name, condition, force }` or `Undefined`.

Normally you do not call this directly; the machine calls `EvaluateTransitions()` after each `Update()` and then applies the transition via `ChangeState`. Use it manually only for custom control.

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

#### `EvaluateTransitions([data])` (machine)

Force evaluation of declarative transitions on the current state and apply the first passing transition.

```gml
state_machine.EvaluateTransitions();          // after custom update loop
state_machine.EvaluateTransitions(payload);   // attach payload if a transition fires
```

- `data` *(optional)*: `Any` - payload attached to the transition if one fires.
- **Returns:** `Struct.StatementState` or `Undefined` if no transition fired or no active state.

This is normally called automatically at the end of `Update()`. Use it manually if you disable auto-processing or run custom update ordering.

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

### Cleanup & Global Helpers

#### `RemoveState(name)`

Remove a state by name from this machine.

```gml
state_machine.RemoveState("Debug");
```

- `name`: `String`  
- **Returns:** `Struct.Statement`

---

#### `Destroy()`

Helper to clean up state-specific timers for all states registered on this machine (current and history).

```gml
state_machine.Destroy();
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
