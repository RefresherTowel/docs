---
layout: default
title: Scripting Reference
parent: Statement
nav_order: 1
---

<!--
/// scripting.md - Changelog:
/// - 23-12-2025: Updated Statement public API coverage and requirements.
-->

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>


# Scripting Reference

This page documents the public API of the state machine system.

It's split into:

- **Core API** - recommended reading for everyone.
- **Advanced API** - optional tools for more complex behaviours.

---

## Core API

### Core Types

---

#### `Statement(owner)`

Create a state machine bound to the given owner instance or struct.

```js
state_machine = new Statement(self);
```

- `owner`: `Id.Instance` or `Struct`  
- **Returns:** `Struct.Statement`

---

#### `StatementState(owner, name)`

Create a new state bound to the given owner.

```js
idle = new StatementState(self, "Idle");
```

- `owner`: `Id.Instance` or `Struct`  
- `name`: `String`  
- **Returns:** `Struct.StatementState`

If `owner` is neither an existing instance nor a struct, the constructor logs a severe debug message and returns `undefined`.

---

#### `eStatementEvents`

Event slots used by states.

Values include:

- `eStatementEvents.ENTER`
- `eStatementEvents.EXIT`
- `eStatementEvents.STEP`
- `eStatementEvents.DRAW`
- `eStatementEvents.NUM` - sentinel for internal sizing.

---

#### `eStatementUpdateMode`

Controls how `UpdateDelta` processes accumulated time.

Values include:

- `eStatementUpdateMode.ACCUMULATED`
- `eStatementUpdateMode.PER_FRAME`

---

#### `eStatementResetMode`

Controls how a submachine is reset or paused when its host state exits or enters.

Values include:

- `eStatementResetMode.RESET_ON_EXIT`
- `eStatementResetMode.REMEMBER`
- `eStatementResetMode.RESET_ON_ENTER`

---

#### `eStatementErrorBehavior`

Controls how caught errors are handled in debug mode.

Values include:

- `eStatementErrorBehavior.PAUSE`
- `eStatementErrorBehavior.RETHROW`

---

#### `eStatementLensMode`

Lens layout modes.

Values include:

- `eStatementLensMode.FULL`
- `eStatementLensMode.EGO`
- `eStatementLensMode.RADIAL`
- `eStatementLensMode.CLOUD`

---

#### `eStatementLensOverlay`

Lens overlay modes.

Values include:

- `eStatementLensOverlay.NONE`
- `eStatementLensOverlay.HEATMAP`

---

#### `eStatementHeatMetric`

Heatmap metrics used by the Lens overlay.

Values include:

- `eStatementHeatMetric.TIME`
- `eStatementHeatMetric.VISITS`

---

#### `eStatementDebugEdgeKind`

Edge types used in debug graphs.

Values include:

- `eStatementDebugEdgeKind.DECLARATIVE`
- `eStatementDebugEdgeKind.OBSERVED`
- `eStatementDebugEdgeKind.MANUAL`

---

#### `eStatementDebugEdgeStyle`

Edge style categories used by the Lens renderer.

Values include:

- `eStatementDebugEdgeStyle.STRUCTURAL`
- `eStatementDebugEdgeStyle.LAST_TRANSITION`
- `eStatementDebugEdgeStyle.QUEUED`
- `eStatementDebugEdgeStyle.HISTORY`

---

#### `STATEMENT_DEBUG`

Global toggle for Statement debug features.

Set to 0 to compile without debug tracking.

---

#### `STATEMENT_TIME_GLOBAL_SCALE`

Global time scale applied to all Statement machines. This is used by `StatementSetGlobalTimeScale`.

---

### Core Statement Methods

#### `AddState(state)`

Register a `StatementState` on this machine.

```js
state_machine.AddState(idle);
```

- `state`: `Struct.StatementState`  
- **Returns:** `Struct.Statement`

The first state added becomes the default initial state. If `auto_enter_first_state` is true (default) and there is no active state yet, the machine enters it immediately and runs its `Enter` handler if defined.
Set `auto_enter_first_state` to false if you want to delay entry until you call `ChangeState` or `SetInitialState`.

If a state with the same name already exists, it is replaced (with a warning).

Requires a state struct built from `StatementState`.

---

#### `SetInitialState(name)`

Set which state name should be treated as the initial state when the machine starts.

```js
state_machine.SetInitialState("Idle");
```

- `name`: `String`
- **Returns:** `Struct.Statement`

If you do not call this, the first state added becomes the default initial state.
If the named state does not exist yet, it will be used when it is added.

---

#### `SetResetMode(mode)`

Set how this machine behaves when it is hosted as a submachine and the parent state exits or enters.

```js
state_machine.SetResetMode(eStatementResetMode.RESET_ON_EXIT);
```

- `mode`: `Constant.eStatementResetMode`
- **Returns:** `Struct.Statement`

Modes:

- `RESET_ON_EXIT`: stop the submachine when the host exits.
- `REMEMBER`: pause the submachine when the host exits and resume on enter.
- `RESET_ON_ENTER`: stop the submachine and restart fresh when the host enters.

Default is `RESET_ON_EXIT`.

---

#### `SetInheritPause(enabled)`

Control whether a submachine inherits pause state from its parent machine.

```js
state_machine.SetInheritPause(true);
```

- `enabled`: `Bool`
- **Returns:** `Struct.Statement`

Default is true.

---

#### `SetInheritTimeScale(enabled)`

Control whether a submachine inherits time scaling from its parent machine.

```js
state_machine.SetInheritTimeScale(false);
```

- `enabled`: `Bool`
- **Returns:** `Struct.Statement`

Default is false.

---

#### `GetState([name])`

Get a state by name, or the current state if no name is provided.

```js
var _current = state_machine.GetState();
var _idle    = state_machine.GetState("Idle");
```

- `name` *(optional)*: `String`  
- **Returns:** `Struct.StatementState` or `Undefined` if not found / no current state.

Logs a warning if a named lookup fails.

---

#### `GetStateName()`

Get the name of the current state.

```js
var _name = state_machine.GetStateName();
```

- **Returns:** `String` or `Undefined`.

---


#### `IsInState(name_or_state)`

Check whether the current state matches the supplied name or state struct.

```js
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
If you pass a struct, it must be built from `StatementState`.

---

#### `GetChildMachine()`

Return the active submachine hosted by the current state, if any.

```js
var _child = state_machine.GetChildMachine();
```

- **Returns:** `Struct.Statement` or `Undefined`.

---

#### `GetChildState()`

Return the active state of the current state's submachine, if any.

```js
var _child_state = state_machine.GetChildState();
```

- **Returns:** `Struct.StatementState` or `Undefined`.

---

#### `IsInPath(path)`

Check whether the machine is in a nested state path such as `Idle/Move/Run`.

```js
if (state_machine.IsInPath("Combat/Attack")) {
    // Host in Combat and submachine in Attack
}
```

- `path`: `String`
- **Returns:** `Bool`

The path is split on `/` and compared against the current state and any nested submachines in order.

---

#### `IsIn(name_or_state)`

Alias for `IsInState`.

```js
if (state_machine.IsIn("Hurt")) {
    // same as IsInState
}
```

- `name_or_state`: `String` or `Struct.StatementState`
- **Returns:** `Bool`

---

#### `GetCurrentStateName()`

Alias for `GetStateName`.

```js
var _name = state_machine.GetCurrentStateName();
```

- **Returns:** `String` or `Undefined`.

---

#### `EnsureState(name, [data], [force])`

Ensure that the current state matches the supplied name. If it is already active, no transition occurs.

```js
// Make sure we are in Idle; only changes if needed.
state_machine.EnsureState("Idle");

// Ensure Hurt with a payload.
state_machine.EnsureState("Hurt", { damage: _damage });
```

- `name`: `String`
- `data` *(optional)*: `Any` - payload attached to the transition if a change is required.
- `force` *(optional)*: `Bool`
- **Returns:** `Struct.StatementState` or `Undefined` if the target does not exist.

Internally this is equivalent to checking the current state's name and only calling `ChangeState` when different, which avoids redundant transitions and Exit/Enter calls.

---

#### `ChangeState(name, [data], [force])`

Immediately change to another state, optionally with a transition payload.

```js
state_machine.ChangeState("Attack");
state_machine.ChangeState("Hitstun", { damage: 5 }, true); // payload + force
```

- `name`: `String`  
- `data` *(optional)*: `Any` - payload retrievable via `GetLastTransitionData()`.  
- `force` *(optional)*: `Bool`  
- **Returns:** `Struct.StatementState` or `Undefined` if target doesn't exist.

Behaviour:

- If target does not exist: logs a severe debug message and returns `undefined`.
- If target is already active: does nothing and returns current state.
- If current state has `can_exit == false` and `force == false`: refuses to change and returns current state.
- If the current state hosts a submachine with an exit gate (see `LockExitUntilSubIn` and `LockExitWhileSubNot`) and `force == false`, the change is blocked.
- A manual `ChangeState` clears any queued transition before switching.
- Otherwise:
  - Runs old state `Exit` (if present).
  - Updates history (`previous_state`, `previous_states`).
  - Switches `state` to the new state.
  - Resets `state_age` to 0.
  - Runs optional state-change hook (see `SetStateChangeBehaviour`).
  - Runs new state `Enter` (if present).

If an `Exit` handler changes state itself, the outer `ChangeState` respects that redirect and returns immediately.

---

#### `UpdateDelta([dt])`

Drive the state machine using a delta value. The delta is scaled by the machine time scale and the global time scale.

```js
// Step Event with a real delta source
state_machine.UpdateDelta(delta_time / 1000000);
```

- `dt` *(optional)*: `Real` - unscaled delta to apply. Defaults to 1.
- **Returns:** whatever the state's Update handler returns, or `Undefined` if no Step ran or there is no active state.

When update mode is `eStatementUpdateMode.ACCUMULATED`, the machine runs Step once per whole accumulated tick and advances state age by fractional time. When update mode is `eStatementUpdateMode.PER_FRAME`, the machine runs Step once per call. Use `SetUpdateMode` to control this.

---

#### `Update()`

Drive the state machine for one Step.

```js
// Step Event
state_machine.Update();
```

This is a legacy convenience wrapper for `UpdateDelta(1)`.

---

#### `Draw()`

Optional helper to run the current state's Draw handler.

```js
// Draw Event
state_machine.Draw();
```

- **Returns:** whatever the state's Draw handler returns, or `Undefined` if not implemented.

Use only if you want per-state drawing.

---

#### `GetStateTime()`

Get the scaled time since the current state was entered. This value is advanced by `UpdateDelta` and respects time scaling.

```js
if (state_machine.GetStateTime() > game_get_speed(gamespeed_fps) * 0.5) {
    // half a second at 60 FPS
}
```

- **Returns:** `Real`

Automatically reset on each state change.

---

#### `SetStateTime(time)`

Manually set the current state's age in scaled time units.

```js
state_machine.SetStateTime(0);
```

- `time`: `Real`  
- **Returns:** `Struct.Statement`

---

#### `ClearStates()`

Clear all states and reset the machine.

```js
state_machine.ClearStates();
```

Clears:

- `states`, `states_array`
- `state`, `previous_state`, `previous_states`
- `state_stack`
- any queued state
- `state_age`
- `initial_state_name`
- `last_transition_data`

Returns the machine for chaining.

---

### Core StatementState Methods

#### `AddEnter(fn)`

Bind an `Enter` handler that runs once when the state becomes active.

```js
idle.AddEnter(function() {
    sprite_index = spr_player_idle;
});
```

- `fn`: `Function` - automatically `method(owner, fn)` bound. In other words, the scope of the function runs from whoever has been supplied as the owner of the state (most often the instance running the state machine itself). This behaviour extends through to all the `fn` arguments in the other three `Add*()` methods below.
- **Returns:** `Struct.StatementState`

---

#### `AddUpdate(fn)`

Bind an `Update` handler that runs every Step while the state is active.

```js
idle.AddUpdate(function() {
    // Idle behaviour
});
```

- `fn`: `Function` - automatically `method(owner, fn)` bound.
- **Returns:** `Struct.StatementState`

---

#### `AddExit(fn)`

Bind an `Exit` handler that runs once when the state stops being active.

```js
idle.AddExit(function() {
    EchoDebugInfo("Leaving Idle");
});
```

- `fn`: `Function` - automatically `method(owner, fn)` bound.
- **Returns:** `Struct.StatementState`

---

#### `AddDraw(fn)`

Bind a `Draw` handler that runs each Draw while the state is active if you call `Statement.Draw()`.

```js
idle.AddDraw(function() {
    draw_self();
});
```

- `fn`: `Function` - automatically `method(owner, fn)` bound.
- **Returns:** `Struct.StatementState`

---

## Advanced API

The following features are optional. You can ignore them unless your project specifically benefits from them.

---

### Pausing

#### `SetPaused(paused)`

Pause or resume the state machine. When paused, `Update()` skips queue processing, STEP handlers, declarative transitions, and state age increments. Manual `ChangeState` calls still work.

```js
state_machine.SetPaused(true);  // freeze
state_machine.SetPaused(false); // resume
```

- `paused`: `Bool`
- **Returns:** `Struct.Statement`

---

#### `IsPaused()`

Check whether the machine is currently paused.

```js
if (state_machine.IsPaused()) { /* skip logic */ }
```

- **Returns:** `Bool`

---

### Update Modes and Time Scaling

#### `SetUpdateMode(mode)`

Set how `UpdateDelta` processes the machine.

```js
state_machine.SetUpdateMode(eStatementUpdateMode.ACCUMULATED);
```

- `mode`: `Constant.eStatementUpdateMode`
- **Returns:** `Struct.Statement`

Modes:

- `ACCUMULATED`: accumulate time and run Step once per whole tick.
- `PER_FRAME`: run Step once per call to `UpdateDelta`.

---

#### `GetUpdateMode()`

Get the current update mode for this machine.

```js
var _mode = state_machine.GetUpdateMode();
```

- **Returns:** `Constant.eStatementUpdateMode`

---

#### `StatementSetDefaultUpdateMode(mode)`

Set the global default update mode used by newly created machines.

```js
StatementSetDefaultUpdateMode(eStatementUpdateMode.PER_FRAME);
```

- `mode`: `Constant.eStatementUpdateMode`
- **Returns:** `Undefined`

---

#### `StatementGetDefaultUpdateMode()`

Get the global default update mode that future machines will use.

```js
var _default_mode = StatementGetDefaultUpdateMode();
```

- **Returns:** `Constant.eStatementUpdateMode`

---

#### `SetTimeScale(scale)`

Set per-machine time scale. This multiplies the delta used by `UpdateDelta`.

```js
state_machine.SetTimeScale(0.5);
```

- `scale`: `Real`
- **Returns:** `Struct.Statement`

---

#### `GetTimeScale()`

Get per-machine time scale.

```js
var _scale = state_machine.GetTimeScale();
```

- **Returns:** `Real`

If no global scale is set, this returns 1.

---

#### `StatementSetGlobalTimeScale(scale)`

Set the global time scale for all Statement machines. This multiplies each machine's time scale.

```js
StatementSetGlobalTimeScale(1);
```

- `scale`: `Real`
- **Returns:** `Undefined`

You can also set `STATEMENT_TIME_GLOBAL_SCALE` directly.

---

#### `GetGlobalTimeScale()`

Get the global time scale applied to all machines.

```js
var _global = state_machine.GetGlobalTimeScale();
```

- **Returns:** `Real`

---

### Queueing

#### `SetQueueAutoProcessing(enabled)`

Control whether queued transitions are automatically processed inside `Update()`.

```js
state_machine.SetQueueAutoProcessing(true);
```

- `enabled`: `Bool`  
- **Returns:** `Struct.Statement`

Default: `true`.

---

#### `QueueState(name, [data], [force])`

Queue a state change to be processed later.

```js
state_machine.QueueState("Attack");
```

- `name`: `String`  
- `data` *(optional)*: `Any` - payload retrievable via `GetLastTransitionData()` if the transition succeeds.  
- `force` *(optional)*: `Bool`  
- **Returns:** `Struct.Statement`

Logs a warning and does not queue anything if the state name does not exist.

---

#### `ProcessQueuedState()`

Process any pending queued state change immediately.

```js
state_machine.ProcessQueuedState();
```

- **Returns:** `Struct.StatementState` or `Undefined`

If there is no queued state, this returns the current state. If the current state cannot exit (and `force` was not set when queuing), the queued transition remains pending and the current state is returned. Otherwise the queue entry is cleared before calling `ChangeState()`.

---

#### `HasQueuedState()`

Check if a queued state is pending.

```js
if (state_machine.HasQueuedState()) { /* ... */ }
```

- **Returns:** `Bool`

---

#### `GetQueuedStateName()`

Get the name of the queued state, if any.

```js
var _next = state_machine.GetQueuedStateName();
```

- **Returns:** `String` or `Undefined`

---

#### `GetQueuedStateData()`

Get the payload attached to a queued state, if any.

```js
var _payload = state_machine.GetQueuedStateData();
```

- **Returns:** `Any` or `Undefined`

---

#### `ClearQueuedState()`

Cancel any queued state without processing it.

```js
state_machine.ClearQueuedState();
```

- **Returns:** `Struct.Statement`

---

### History & Introspection

#### `SetHistoryLimit(limit)`

Set how many previous states to keep in history.

```js
state_machine.SetHistoryLimit(32);
```

- `limit`: `Real`  
- **Returns:** `Struct.Statement`

`limit <= 0` means unlimited history.

---

#### `GetHistoryCount()`

Get how many entries are currently stored in the previous state history.

```js
var _count = state_machine.GetHistoryCount();
```

- **Returns:** `Real`

---

#### `GetHistoryAt(index)`

Get a previous state by history index.

```js
var _st = state_machine.GetHistoryAt(0);
```

- `index`: `Real`
- **Returns:** `Struct.StatementState` or `Undefined` if the index is invalid.

Index 0 is the oldest entry. The most recent entry is at `GetHistoryCount() - 1`.

---

#### `ClearHistory()`

Clear the previous state history without affecting the current state.

```js
state_machine.ClearHistory();
```

- **Returns:** `Struct.Statement`

---

#### `PreviousState([data], [force])`

Convenience helper to change back to the most recent previous state.

```js
state_machine.PreviousState();
```

- `data` *(optional)*: `Any` - payload attached to this transition.
- `force` *(optional)*: `Bool`
- **Returns:** `Struct.StatementState` or `Undefined`.

This is roughly equivalent to:

```js
state_machine.ChangeState(state_machine.GetPreviousStateName(), data, force);
```

but is safer and handles edge cases for you.

---

#### `GetPreviousStateName()`

Get the name of the most recent previous state in history.

```js
var _prev = state_machine.GetPreviousStateName();
```

- **Returns:** `String` or `Undefined`.

---

#### `WasPreviouslyInState(name, [depth])`

Check whether the state at the given history depth matches the supplied name.

```js
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

```js
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

```js
state_machine.PrintStateNames();
```

- **Returns:** `Struct.Statement`

---

#### `DebugDescribe()`

Print a one-line debug description of this state machine, including owner, current state, previous state, age, queued state, state stack depth, and history count.

```js
state_machine.DebugDescribe();
```

- **Returns:** `Undefined`

Useful for quick logging of state machine status without having to inspect multiple values manually.

---

#### `PrintStateHistory([limit])`

Print the previous state history for this machine, from most recent backwards.

```js
// Dump entire history
state_machine.PrintStateHistory();

// Or only the last 5 entries
state_machine.PrintStateHistory(5);
```

- `limit` *(optional)*: `Real` - maximum number of history entries to print. Use 0 or a negative value to print the full history.
- **Returns:** `Struct.Statement`

By default the method prints a short summary (similar to `DebugDescribe()`) and then each history entry with its index.


### State Stack (Push / Pop)

#### `PushState(name, [data], [force])`

Push current state onto a stack and change to `name`.

```js
state_machine.PushState("Pause");
```

- `name`: `String`  
- `data` *(optional)*: `Any` - payload attached to the transition.
- `force` *(optional)*: `Bool`  
- **Returns:** `Struct.StatementState` or `Undefined`.

If the transition is blocked (for example `can_exit == false` and not forced), the current state is **not** pushed.

---

#### `PopState([data], [force])`

Pop the last pushed state from the stack and change back to it.

```js
state_machine.PopState();
```

- `data` *(optional)*: `Any` - payload for this transition.  
- `force` *(optional)*: `Bool`  
- **Returns:** `Struct.StatementState` or `Undefined`.

Returns the current state if the stack is empty or if the target state no longer exists.

---

#### `GetStateStackDepth()`

Number of entries currently on the state stack.

```js
var _depth = state_machine.GetStateStackDepth();
```

- **Returns:** `Real`

---

#### `PeekStateStack()`

Peek at the most recently pushed state without popping it.

```js
var _top = state_machine.PeekStateStack();
```

- **Returns:** `Struct.StatementState` or `Undefined`.

---

#### `ClearStateStack()`

Clear all entries from the state stack without changing the current state.

```js
state_machine.ClearStateStack();
```

- **Returns:** `Struct.Statement`

---

### Submachines (StatementState)

Statement supports nested state machines. A state can host a submachine and optionally control when the host can exit.

#### `CreateSubMachine([name])`

Create and attach a submachine to this state (making it a host state).

```js
var _sub = state.CreateSubMachine("CombatSub");
```

- `name` *(optional)*: `String` - friendly name for debug tools. Defaults to the host state name.
- **Returns:** `Struct.Statement`

If a submachine already exists, this returns the existing submachine.

---

#### `HasSubMachine()`

Check whether this state currently hosts a submachine.

```js
if (state.HasSubMachine()) {
    // has a child machine
}
```

- **Returns:** `Bool`

---

#### `GetSubMachine()`

Get the hosted submachine, if any.

```js
var _sub = state.GetSubMachine();
```

- **Returns:** `Struct.Statement` or `Undefined`

---

#### `OnSubmachineEnter(fn)`

Set a callback that runs when this host state enters and its submachine is started or resumed.

```js
state.OnSubmachineEnter(method(self, function(_sub) {
    EchoDebugInfo("Submachine started");
}));
```

- `fn`: `Function` - called as `fn(submachine)`. This is not auto-bound, so use `method(owner, fn)` if you need scope binding.
- **Returns:** `Struct.StatementState`

---

#### `OnSubmachineExit(fn)`

Set a callback that runs when this host state exits and its submachine is suspended or stopped.

```js
state.OnSubmachineExit(method(self, function(_sub) {
    EchoDebugInfo("Submachine stopped");
}));
```

- `fn`: `Function` - called as `fn(submachine)`. This is not auto-bound, so use `method(owner, fn)` if you need scope binding.
- **Returns:** `Struct.StatementState`

---

#### `LockExitUntilSubIn(state_name)`

Prevent this host state from exiting (unless forced) until the submachine is in the given state.

```js
state.LockExitUntilSubIn("Ready");
```

- `state_name`: `String`
- **Returns:** `Struct.StatementState`

---

#### `LockExitWhileSubNot(fn)`

Prevent this host state from exiting (unless forced) while a predicate returns false for the submachine.

```js
state.LockExitWhileSubNot(function(_sub) {
    return _sub.IsInState("Ready");
});
```

- `fn`: `Function` - called as `fn(submachine)` and should return `Bool`.
- **Returns:** `Struct.StatementState`

Exit locks are respected by `ChangeState`, `QueueState`, `PushState`, and `PopState` unless `force` is true.

---

### State Change Hook

#### `SetStateChangeBehaviour(fn)`

Register a callback to be run whenever the machine changes state.

```js
state_machine.SetStateChangeBehaviour(method(self, function() {
    EchoDebugInfo("Now in state: " + string(state_machine.GetStateName()));
}));
```

- `fn`: `Function` - called as `fn(previous_state, transition_data)`; both may be `undefined`. This function is not auto-bound, so use `method(owner, fn)` if you need scope binding.
- **Returns:** `Undefined`

Called after the old state's `Exit`, after `state` is updated, and before new state `Enter`.

---

### Low-Level Event Running

Behind the scenes, each Statement state uses an array indexed with enums to decide what handler to run. For instance, `Update()`, runs the handler stored in the array position indexed by `eStatementEvents.STEP`. In most circumstances, you don't need to worry about this stuff, simply use `Update()` / `Draw()` and it will be handled automatically.

However, if you're confident editing Statement itself, you can extend `eStatementEvents` with your own custom event types. The enum is defined in `scr_statement_macro`.

> `eStatementEvents` is an enum defined inside the Statement framework (in `scr_statement_macro`) that maps the built-in handler types:
> 
> - `eStatementEvents.ENTER`
> - `eStatementEvents.DRAW`
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
```js
// Assuming you have added ANIMATION_END to the enum list (before NUM)
idle.AddStateEvent(eStatementEvents.ANIMATION_END, function() {
    // custom logic dealing with the end of animations in the idle state
});
```

- `event`: `Real` - one of the `eStatementEvents` values (`ENTER`, `EXIT`, `STEP`, `DRAW` or any custom `eStatementEvents` value you've defined).
- `fn`: `Function` - automatically `method(owner, fn)` bound.
- **Returns:** `Struct.StatementState`

---

#### `HasStateEvent(event)`

**StatementState** method. Check whether this state has a handler for a given `eStatementEvents` index.

```js
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
```js
if (state_machine.GetState().HasStateEvent(eStatementEvents.ANIMATION_END)) {
    state_machine.RunState(eStatementEvents.ANIMATION_END);
}
```

- `event`: `Real` (usually one of the `eStatementEvents` values)  
- **Returns:** Any or `Undefined` if:
  - There is no active state, or
  - The chosen event is not implemented on the current state.

---

### Exit Control & Declarative Transitions (StatementState)

#### `SetCanExit(can_exit)` / `LockExit()` / `UnlockExit()`

Control whether a state can be exited without forcing.

```js
state.LockExit();      // block transitions unless force == true
state.SetCanExit(true); // equivalent to UnlockExit()
```

- `can_exit`: `Bool`
- **Returns:** `Struct.StatementState`

When `can_exit == false`, `ChangeState`/queued transitions will only leave this state if `force == true`.

---

#### `AddTransition(target_name, condition, [data], [force])`

Add a declarative transition that will be evaluated each `Update()` while the state is active. When the condition returns true, the machine changes to `target_name`.

```js
idle.AddTransition("Run", function() {
    return abs(hsp) > 0.1;
});
```

- `target_name`: `String`
- `condition`: `Function` - automatically bound to the owner via `method(owner, fn)`.
- `data` *(optional)*: `Any` - payload attached to the transition if it fires.
- `force` *(optional)*: `Bool` - ignore `can_exit` when firing.
- **Returns:** `Struct.StatementState`

Transitions are checked in the order they were added; the first condition returning true will fire.
When a transition fires, its `data` payload is passed into `ChangeState`.

---

#### `ClearTransitions()`

Remove all declarative transitions from this state.

```js
state.ClearTransitions();
```

- **Returns:** `Struct.StatementState`

---

#### `EvaluateTransitions()`

Evaluate this state's declarative transitions and return the first matching record.

```js
var _tr = state.EvaluateTransitions();
```

- **Returns:** `Struct` `{ target_name, condition, force, data }` or `Undefined`.

Normally you do not call this directly; the machine calls `EvaluateTransitions()` after each `Update()` and then applies the transition via `ChangeState`. Use it manually only for custom control.

---

#### `EvaluateTransitions()` (machine)

Force evaluation of declarative transitions on the current state and apply the first passing transition.

```js
state_machine.EvaluateTransitions();          // after custom update loop
```

- **Returns:** `Struct.StatementState` or `Undefined` if no transition fired or no active state.

This is normally called automatically at the end of `Update()`. Use it manually if you disable auto-processing or run custom update ordering.

> This is not the same as `state.EvaluateTransitions()`, as this method actually changes state if a transition fires. This version attached to the state machine is the one you most likely want to use.
{: .warning}

---

### Per-State Timers (Advanced)

Per-state timers live on individual `StatementState` instances and are considered **advanced**. In almost all cases (99% of use cases) you can ignore them and just use the machine-level state time via `GetStateTime()` / `SetStateTime()`.

Per-state timers are backed by GameMaker **time sources** and tick independently of `Update()`:
- Once a state becomes active and its timer is started, that timer advances every frame until you change out of that state or explicitly stop/pause/reset the timer.
- Because they use time sources internally, they can continue advancing even if the instance is deactivated or you temporarily stop calling `Update()`.

By contrast, `GetStateTime()` / `SetStateTime()` live on the **Statement** itself:
- Represent "how long the current state has been active (scaled time units)".
- Reset automatically on state change.
- Only increment when you call `Update()` on the machine.

If you're unsure which to use, start with `GetStateTime()` and ignore per-state timers; they exist mainly for very specialised cases where you need a timer tightly bound to a specific state's lifetime.

#### `TimerStart()`

Create and start a per-state timer (if not already created), resetting it to 0.

```js
state.TimerStart();
```

- **Returns:** `Struct.StatementState`

Requires this state to be added to a `Statement` machine.

---

#### `TimerSet(time)`

Set the per-state timer value.

```js
state.TimerSet(30);
```

- `time`: `Real`  
- **Returns:** `Struct.StatementState`

---

#### `TimerGet()`

Get the current per-state timer value.

```js
var _t = state.TimerGet();
```

- **Returns:** `Real`

---

#### `TimerPause()`

Pause the per-state timer.

```js
state.TimerPause();
```

- **Returns:** `Struct.StatementState`

---

#### `TimerRestart()`

Restart the per-state timer if it exists.

```js
state.TimerRestart();
```

- **Returns:** `Struct.StatementState`

---

#### `TimerKill()`

Kill (destroy) the per-state timer.

```js
state.TimerKill();
```

- **Returns:** `Struct.StatementState`

---

### Cleanup & Global Helpers

#### `RemoveState(name)`

Remove a state by name from this machine.

```js
state_machine.RemoveState("Debug");
```

- `name`: `String`  
- **Returns:** `Struct.Statement`

---

#### `Destroy()`

Helper to clean up state-specific timers for all states registered on this machine (current and history).

```js
state_machine.Destroy();
```

Call this if you are discarding a machine and want to ensure no associated timers continue ticking.

---

#### `StatementStateKillTimers()`

Global helper: destroy all state timers registered in `global.__statement_timers` and clear the array.

```js
StatementStateKillTimers();
```

Use this if you want a global "nuke all state timers" reset, e.g. when restarting a run or changing rooms.

---

## Debug API (Machine & State)

The following helpers are mainly intended for debugging and tooling. They are safe to use in shipping builds, but you will typically guard them behind `#if STATEMENT_DEBUG` checks.

---

### Machine debug controls

#### `ClearDebugTransitionHistory()`

Clear any recorded transition history entries.

```js
state_machine.ClearDebugTransitionHistory();
```

- **Returns:** `Struct.Statement`

---

#### `DebugJumpToState(name, force)`

Jump to a state from debug tooling, using that state's debug payload if set.

```js
state_machine.DebugJumpToState(name, force);
```

- `name`: `String`
- `force` *(optional)*: `Bool`
- **Returns:** `Struct.StatementState,Undefined`

---

#### `DebugPause()`

Pause this machine for debug purposes.

```js
state_machine.DebugPause();
```

- **Returns:** `Struct.Statement`

---

#### `DebugResume()`

Resume this machine from a debug pause.

```js
state_machine.DebugResume();
```

- **Returns:** `Struct.Statement`

---

#### `DebugSetErrorBehavior(behavior)`

Set how the machine reacts to caught errors: PAUSE (default) or RETHROW.

```js
state_machine.DebugSetErrorBehavior(behavior);
```

- `behavior`: `Constant.eStatementErrorBehavior`
- **Returns:** `Struct.Statement`

---

#### `DebugSetLogErrorsToFile(log_to_file)`

Control whether caught errors append to debug_statement_errors.log before optional rethrow.

```js
state_machine.DebugSetLogErrorsToFile(log_to_file);
```

- `log_to_file`: `Bool`
- **Returns:** `Struct.Statement`

---

#### `DebugStep()`

Run exactly one Update tick while paused, then re-pause.

```js
state_machine.DebugStep();
```

- **Returns:** `Any,Undefined`

---

#### `DebugTag(tag)`

Assign a tag (or comma-separated tags) for grouping/filtering in debug UIs.

```js
state_machine.DebugTag(tag);
```

- `tag`: `String`
- **Returns:** `Struct.Statement`

---

#### `GetDebugGraph()`

Get a snapshot of this machine's debug graph: states + edges.

```js
state_machine.GetDebugGraph();
```

- **Returns:** `Struct,Undefined` - A struct { states, edges } or undefined if debug disabled.

---

#### `GetDebugName()`

Get the friendly debug name, or a fallback based on the owner.

```js
state_machine.GetDebugName();
```

- **Returns:** `String,Undefined`

---

#### `GetDebugStateStats()`

Get the per-state debug stats map.

```js
state_machine.GetDebugStateStats();
```

- **Returns:** `Struct,Undefined`

---

#### `GetDebugTag()`

Get the debug tag string, if set.

```js
state_machine.GetDebugTag();
```

- **Returns:** `String,Undefined`

---

#### `GetDebugTransitionHistory()`

Get the recent transition history records.

```js
state_machine.GetDebugTransitionHistory();
```

- **Returns:** `Array,Undefined`

---

#### `IsDebugEnabled()`

Returns whether debug tracking is enabled for this machine.

```js
state_machine.IsDebugEnabled();
```

- **Returns:** `Bool`

---

#### `SetDebugEnabled(enabled)`

Enable or disable debug tracking for this machine.

```js
state_machine.SetDebugEnabled(true);
```

- `enabled`: `Bool`
- **Returns:** `Struct.Statement`

Default is true when STATEMENT_DEBUG is enabled.

---

#### `SetDebugName(name)`

Assign a friendly name for this machine in debug UIs.

```js
state_machine.SetDebugName(name);
```

- `name`: `String`
- **Returns:** `Struct.Statement`

---

### State-level debug helpers

#### `DebugBreakOnEnter(break_on_enter)`

Enable or disable "break on enter" for this state in debug builds.

```js
state.DebugBreakOnEnter(break_on_enter);
```

- `break_on_enter` *(optional)*: `Bool` - Defaults to true.
- **Returns:** `Struct.StatementState`

---

#### `DebugLinkTo(target_name)`

Declare a debug-only link from this state to another state for the visualiser.

```js
state.DebugLinkTo(target_name);
```

- `target_name`: `String`
- **Returns:** `Struct.StatementState`

---

#### `DebugPayload(payload)`

Set a default payload used when jumping to this state via debug tools.

```js
state.DebugPayload(payload);
```

- `payload`: `Any`
- **Returns:** `Struct.StatementState`

---

#### `DebugTag(tag)`

Assign a tag (or comma-separated tags) for grouping/filtering in debug UIs.

```js
state.DebugTag(tag);
```

- `tag`: `String`
- **Returns:** `Struct.StatementState`

---

### Global debug helpers

#### `StatementDebugPruneRegistry([prune_destroyed_owners])`

Remove dead entries from the global Statement debug registry.

```js
var _removed = StatementDebugPruneRegistry();
```

- `prune_destroyed_owners` *(optional)*: `Bool` - when true, also removes machines whose owner instances are destroyed.
- **Returns:** `Real` - number of entries removed.

Returns 0 if STATEMENT_DEBUG is false.

---


## Visual Debugger & Debug UI

Statement ships with an in-game visual debugger known as Lens. You do not need to use it directly to benefit from Statement, but it is available if you want.

---

### Lens entry points

#### `StatementLens()`

Debug visualiser for Statement machines (drawn in GUI space).

```js
var statement_lens = new StatementLens();
```

- **Returns:** `Struct.StatementLens`

---

#### `StatementLensGet()`

Get the global Statement Lens instance when STATEMENT_DEBUG is enabled.

```js
var _lens = StatementLensGet();
```

- **Returns:** `Struct.StatementLens` or `Undefined`

---

#### `StatementLensInit()`

Ensure the Lens globals exist and refresh the active machine list.

```js
StatementLensInit();
```

- **Returns:** `Undefined`

---

#### `StatementLensUpdate()`

Update hook for the Statement Lens (call from a Step event when STATEMENT_DEBUG is enabled).

```js
StatementLensUpdate();
```

- **Returns:** `Undefined`

---

#### `StatementLensInputPressed(action_id)`

Return true if a Statement Lens action is pressed in the active Echo Chamber input context.

```js
if (StatementLensInputPressed(STATEMENT_LENS_ACTION_NEXT_MACHINE)) {
    // next machine
}
```

- `action_id`: `String`
- **Returns:** `Bool`

Action ids are defined as `STATEMENT_LENS_ACTION_*` macros in `scr_statement_macro`.
Returns false if no active Echo Chamber root is available.
Default bindings are provided by `STATEMENT_LENS_BIND_*` macros and use input binding structs built from `EchoChamberInputBindingKey`.

---

#### `StatementLensDraw()`

Draw hook for the Statement Lens (call from a Draw GUI event when STATEMENT_DEBUG is enabled).

```js
StatementLensDraw();
```

- **Returns:** `Undefined`

---

#### `StatementLensOpen(ui_root)`

Open or create the Statement Lens window inside the Echo Debug UI desktop.

```js
StatementLensOpen(global.EchoDesktop);
```

- `ui_root`: `Struct.EchoChamberRoot`
- **Returns:** `Struct.EchoChamberWindow` or `Undefined`

Requires an Echo Chamber root struct built from `EchoChamberRoot`.
Returns `Undefined` if STATEMENT_DEBUG is false or `ui_root` is invalid.

---

### Lens instance helpers

#### `IsVisible()`

Whether the lens is visible.

```js
statement_lens.IsVisible();
```

- **Returns:** `Bool`

---

#### `SetVisible(visible)`

Set visibility of the lens.

```js
statement_lens.SetVisible(visible);
```

- `visible`: `Bool` - true to show the lens, false to hide it.
- **Returns:** `Struct.StatementLens`

---
