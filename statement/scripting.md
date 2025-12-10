---
layout: default
title: Scripting Reference
parent: Statement
nav_order: 1
---

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

- `owner`: `ID.Instance` or `Struct`  
- **Returns:** `Struct.Statement`

---

#### `StatementState(owner, name)`

Create a new state bound to the given owner.

```js
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

```js
state_machine.AddState(idle);
```

- `state`: `Struct.StatementState`  
- **Returns:** `Struct.Statement`

The **first** state added becomes the active state and runs its `Enter` handler (if defined).

If a state with the same name already exists, it is replaced (with a warning).

---

#### `GetState([name])`

Get a state by name, or the current state if no name is provided.

```js
var _current = state_machine.GetState();
var _idle    = state_machine.GetState("Idle");
```

- `name` *(optional)*: `String`  
- **Returns:** `Struct.StatementState` or `Undefined` if not found / no current state.

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

```js
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

```js
// Draw Event
state_machine.Draw();
```

- **Returns:** whatever the state's Draw handler returns, or `Undefined` if not implemented.

Use only if you want per-state drawing.

---

#### `GetStateTime()`

Get how long (in frames) the current state has been active.

```js
if (state_machine.GetStateTime() > game_get_speed(gamespeed_fps) * 0.5) {
    // half a second at 60 FPS
}
```

- **Returns:** `Real`

Automatically reset on each state change.

---

#### `SetStateTime(time)`

Manually set the current state's age.

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

- **Returns:** `Struct.StatementState`

---

#### `AddExit(fn)`

Bind an `Exit` handler that runs once when the state stops being active.

```js
idle.AddExit(function() {
    EchoDebugInfo("Leaving Idle");
});
```

- **Returns:** `Struct.StatementState`

---

#### `AddDraw(fn)`

Bind a `Draw` handler that runs each Draw while the state is active if you call `Statement.Draw()`.

```js
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

---

#### `ProcessQueuedState()`

Process any pending queued state change immediately.

```js
state_machine.ProcessQueuedState();
```

- **Returns:** `Struct.StatementState` or `Undefined`

If the current state cannot exit (and `force` was not set when queuing), the queued transition remains pending. Otherwise the queue entry is cleared before calling `ChangeState()`.

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

Return a one-line debug description of this state machine, including owner, current state, previous state, age, queued state (if any), state stack depth, and history count.

```js
EchoDebugInfo(state_machine.DebugDescribe());
```

- **Returns:** `String`

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

#### `PushState(name, [force])`

Push current state onto a stack and change to `name`.

```js
state_machine.PushState("Pause");
```

- `name`: `String`  
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

Handles empty stacks and invalid entries safely.

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

### State Change Hook

#### `SetStateChangeBehaviour(fn)`

Register a callback to be run whenever the machine changes state.

```js
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

#### `AddTransition(target_name, condition, [force])`

Add a declarative transition that will be evaluated each `Update()` while the state is active. When the condition returns true, the machine changes to `target_name`.

```js
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

- **Returns:** `Struct` `{ target_name, condition, force }` or `Undefined`.

Normally you do not call this directly; the machine calls `EvaluateTransitions()` after each `Update()` and then applies the transition via `ChangeState`. Use it manually only for custom control.

---

#### `EvaluateTransitions([data])` (machine)

Force evaluation of declarative transitions on the current state and apply the first passing transition.

```js
state_machine.EvaluateTransitions();          // after custom update loop
state_machine.EvaluateTransitions(payload);   // attach payload if a transition fires
```

- `data` *(optional)*: `Any` - payload attached to the transition if one fires.
- **Returns:** `Struct.StatementState` or `Undefined` if no transition fired or no active state.

This is normally called automatically at the end of `Update()`. Use it manually if you disable auto-processing or run custom update ordering.

> This is not the same as `state.EvaluateTransitions();`, as this method actually changes state if a transition fires. This is version of the `EvaluateTransitions()` method, attached to the state machine, is the one that you are most likely to want to use.
{. :warning}

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

```js
state.TimerStart();
```

- **Returns:** `Struct.StatementState`

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

#### `GetGlobalTimeScale()`

Get global time scale.

```js
state_machine.GetGlobalTimeScale();
```

- **Returns:** `Real`

---

#### `GetTimeScale()`

Get per-machine time scale.

```js
state_machine.GetTimeScale();
```

- **Returns:** `Real`

---

#### `IsDebugEnabled()`

Returns whether debug tracking is enabled for this machine.

```js
state_machine.IsDebugEnabled();
```

- **Returns:** `Bool`

---

#### `SetDebugEnabled()`

Enable or disable debug tracking for this machine.

```js
state_machine.SetDebugEnabled();
```

- **Returns:** `Struct.Statement`

---

#### `SetDebugName(name)`

Assign a friendly name for this machine in debug UIs.

```js
state_machine.SetDebugName(name);
```

- `name`: `String`
- **Returns:** `Struct.Statement`

---

#### `SetGlobalTimeScale(scale)`

Set global time scale for all Statement machines (multiplies per-machine scale).

```js
state_machine.SetGlobalTimeScale(scale);
```

- `scale`: `Real`

---

#### `SetTimeScale(scale)`

Set per-machine time scale (affects state age, timers, and debug stats).

```js
state_machine.SetTimeScale(scale);
```

- `scale`: `Real`
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

### Global debug helpers

#### `StatementDebugFindMachinesForOwner(owner)`

Finds Statement machines bound to a specific owner instance/struct.

```js
StatementDebugFindMachinesForOwner(owner);
```

- `owner`: `Id.Instance,Struct` - Owner to search for.
- **Returns:** `Array<Struct.Statement>`

---

#### `StatementDebugGetMachines()`

Returns the global list of Statement machines tracked for debugging.

```js
StatementDebugGetMachines();
```

- **Returns:** `Array<Struct.Statement>`

---


## Visual Debugger & Debug UI

Statement ships with an in-game visual debugger and a small immediate-mode UI helper. You do not need to use these directly to benefit from Statement, but they are available if you want to build your own tooling.

---

### Visualiser entry points

#### `StatementVisualiser()`

Debug visualiser for Statement machines (drawn in GUI space).

```js
var statementVisualiser = new StatementVisualiser();
```

- **Returns:** `Struct.StatementVisualiser`

---

#### `StatementDebugVisUpdate()`

Update hook for the Statement visualiser (call from a Step event when STATEMENT_DEBUG is enabled).

```js
StatementDebugVisUpdate();
```


---

#### `StatementDebugVisDraw()`

Draw hook for the Statement visualiser (call from a Draw GUI event when STATEMENT_DEBUG is enabled).

```js
StatementDebugVisDraw();
```


---

### Visualiser instance helpers

#### `IsVisible()`

Whether the visualiser is visible.

```js
visualiser.IsVisible();
```

- **Returns:** `Bool`

---

#### `SetVisible(visible)`

Set visibility of the visualiser.

```js
visualiser.SetVisible(visible);
```

- `visible`: `Bool` - True to show the visualiser, false to hide it.
- **Returns:** `Struct.StatementVisualiser`

---

### Debug UI theme

#### `DebugUITheme()`

Creates the shared debug UI theme container for Statement visuals.

```js
var debugUITheme = new DebugUITheme();
```

- **Returns:** `Struct.DebugUITheme`

---

#### `RefreshMetrics()`

Recompute row heights based on current fonts and padding.

```js
theme.RefreshMetrics();
```

- **Returns:** `Undefined`

---

### Debug UI helpers (StatementDebugUI)

#### `StatementDebugUI(theme)`

UI helper used by the Statement visualiser (buttons, toggles, overlays).

```js
var statementDebugUI = new StatementDebugUI(theme);
```

- `theme`: `Struct.DebugUITheme` - Theme instance to drive styling.
- **Returns:** `Struct.StatementDebugUI`

---

#### `BeginFrame()`

Begin a new UI frame: cache mouse state and clear consumption.

```js
ui.BeginFrame();
```

- **Returns:** `Undefined`

---

#### `BlurTextInput()`

Release text input focus, returning the final content.

```js
ui.BlurTextInput();
```

- **Returns:** `String`

---

#### `Button(x1, y1, x2, y2, label, style_id, tooltip)`

Simple button. Draws a rectangle with a label, returns true on click.

```js
ui.Button(x1, y1, x2, y2, label, style_id, tooltip);
```

- `x1`: `Real` - Left of the button in GUI space.
- `y1`: `Real` - Top of the button in GUI space.
- `x2`: `Real` - Right of the button in GUI space.
- `y2`: `Real` - Bottom of the button in GUI space.
- `label`: `String` - Button text.
- `style_id` *(optional)*: `String` - Style id from the theme button styles.
- `tooltip` *(optional)*: `String` - Tooltip text to show on hover.
- **Returns:** `Bool` - True if the button was clicked this frame.

---

#### `ConsumeOverlays()`

Run the topmost overlay input handler (if any).

```js
ui.ConsumeOverlays();
```

- **Returns:** `Undefined`

---

#### `DrawOverlays()`

Draw any late UI overlays (e.g. dropdown popups) on top of everything.

```js
ui.DrawOverlays();
```

- **Returns:** `Undefined`

---

#### `Dropdown(x1, y1, x2, y2, options, current_index, id, style_id, tooltip)`

Simple dropdown with popup list. Returns new index.

```js
ui.Dropdown(x1, y1, x2, y2, options, current_index, id, style_id, tooltip);
```

- `x1`: `Real` - Left of the dropdown in GUI space.
- `y1`: `Real` - Top of the dropdown in GUI space.
- `x2`: `Real` - Right of the dropdown in GUI space.
- `y2`: `Real` - Bottom of the dropdown in GUI space.
- `options`: `Array<String>` - List of option labels.
- `current_index`: `Real` - Current selection index.
- `id`: `Any` - Stable id so we can track which dropdown is open.
- `style_id` *(optional)*: `String` - Style id from the theme dropdown styles.
- `tooltip` *(optional)*: `String` - Tooltip text to show on hover.
- **Returns:** `Real` - New selection index.

---

#### `FocusTextInput(id, content, placeholder)`

Claim text input focus for a given id, seeding content and caret.

```js
ui.FocusTextInput(id, content, placeholder);
```

- `id`: `Any` - Unique identifier for the text input.
- `content`: `String` - Initial content to place in the buffer.
- `placeholder`: `String` - Placeholder text to render when empty.
- **Returns:** `Undefined`

---

#### `HeaderBar(x1, y1, x2, y2, title, style_id)`

Draw a header bar with optional title text.

```js
ui.HeaderBar(x1, y1, x2, y2, title, style_id);
```

- `x1`: `Real` - Left of the header bar.
- `y1`: `Real` - Top of the header bar.
- `x2`: `Real` - Right of the header bar.
- `y2`: `Real` - Bottom of the header bar.
- `title` *(optional)*: `String` - Title text to draw.
- `style_id` *(optional)*: `String` - Style key to resolve look.
- **Returns:** `Undefined`

---

#### `Label(x1, y1, x2, y2, text)`

Draw a simple text label centered vertically in the given rect. No interaction, just drawing.

```js
ui.Label(x1, y1, x2, y2, text);
```

- `x1`: `Real` - Left of the rect in GUI space.
- `y1`: `Real` - Top of the rect in GUI space.
- `x2`: `Real` - Right of the rect in GUI space.
- `y2`: `Real` - Bottom of the rect in GUI space.
- `text`: `String` - Text to display.
- **Returns:** `Undefined`

---

#### `MenuToggles(x1, y1, x2, y2, items, id, style_id, label, tooltip)`

Show a menu button that opens a toggle list. Returns toggles array if changed.

```js
ui.MenuToggles(x1, y1, x2, y2, items, id, style_id, label, tooltip);
```

- `x1`: `Real` - Left of the menu button in GUI space.
- `y1`: `Real` - Top of the menu button in GUI space.
- `x2`: `Real` - Right of the menu button in GUI space.
- `y2`: `Real` - Bottom of the menu button in GUI space.
- `items`: `Array<Struct>` - Array of structs with at least { label, value }.
- `id`: `Any` - Stable id for tracking the open menu.
- `style_id` *(optional)*: `String` - Style key to resolve look.
- `label` *(optional)*: `String` - Text to show on the button (defaults to "Settings").
- `tooltip` *(optional)*: `String` - Tooltip text to show on hover.
- **Returns:** `Array<Struct>` - Updated items array (with toggled values).

---

#### `MouseConsumed()`

Returns whether some UI control has already claimed the mouse this frame.

```js
ui.MouseConsumed();
```

- **Returns:** `Bool`

---

#### `OverlayPop(id)`

Pop overlays with a matching id (if present).

```js
ui.OverlayPop(id);
```

- `id`: `Any` - Identifier for the overlay to remove.
- **Returns:** `Undefined`

---

#### `OverlayPush(id, fn)`

Push an overlay input handler onto the stack (topmost handles input first).

```js
ui.OverlayPush(id, fn);
```

- `id`: `Any` - Identifier for the overlay.
- `fn`: `Function` - Handler function to run for the overlay.
- **Returns:** `Undefined`

---

#### `Panel(x1, y1, x2, y2, with_border, style_id)`

Panel helper for filled backgrounds. Optional border and style id.

```js
ui.Panel(x1, y1, x2, y2, with_border, style_id);
```

- `x1`: `Real` - Left of the panel.
- `y1`: `Real` - Top of the panel.
- `x2`: `Real` - Right of the panel.
- `y2`: `Real` - Bottom of the panel.
- `with_border` *(optional)*: `Bool` - Whether to draw the border.
- `style_id` *(optional)*: `String` - Style key to resolve look.
- **Returns:** `Undefined`

---

#### `PopContext()`

Restore the previous UI context (if any).

```js
ui.PopContext();
```

- **Returns:** `Undefined`

---

#### `Popup(x1, y1, x2, y2, title, style_id)`

Popup chrome (background, border, header). Returns body rect.

```js
ui.Popup(x1, y1, x2, y2, title, style_id);
```

- `x1`: `Real` - Left of the popup.
- `y1`: `Real` - Top of the popup.
- `x2`: `Real` - Right of the popup.
- `y2`: `Real` - Bottom of the popup.
- `title` *(optional)*: `String` - Header title.
- `style_id` *(optional)*: `String` - Style key to resolve look.
- **Returns:** `Struct` - { body_x1, body_y1, body_x2, body_y2, header_bottom }

---

#### `PushContext(id)`

Save current UI state and switch to a named context (for multiple windows).

```js
ui.PushContext(id);
```

- `id`: `Any` - Identifier for the context to push and switch to.
- **Returns:** `Undefined`

---

#### `ScrollVertical(x1, y1, x2, y2, value, speed, max)`

Apply vertical scroll to a value if the wheel is used over this rect.

```js
ui.ScrollVertical(x1, y1, x2, y2, value, speed, max);
```

- `x1`: `Real` - Left of the scrollable rect (GUI space).
- `y1`: `Real` - Top of the scrollable rect (GUI space).
- `x2`: `Real` - Right of the scrollable rect (GUI space).
- `y2`: `Real` - Bottom of the scrollable rect (GUI space).
- `value`: `Real` - Current scroll value.
- `speed`: `Real` - Pixels to scroll per wheel notch.
- `max`: `Real` - Maximum scroll value (clamped 0.._max).
- **Returns:** `Real` - Updated scroll value.

---

#### `SetInputProvider(fn)`

Override how mouse input is sampled each frame (supply mx,my,mouse_l_down,mouse_l_pressed,wheel).

```js
ui.SetInputProvider(fn);
```

- `fn`: `Function` - Function returning a struct with mouse data for this frame.
- **Returns:** `Undefined`

---

#### `SetTextInputSeed(fn)`

Override how the text input seeds its buffer on focus (defaults to writing keyboard_string).

```js
ui.SetTextInputSeed(fn);
```

- `fn`: `Function` - Function that seeds the active text buffer.
- **Returns:** `Undefined`

---

#### `SetTextInputSource(fn)`

Override the string source used while a text input is active (defaults to keyboard_string).

```js
ui.SetTextInputSource(fn);
```

- `fn`: `Function` - Provider returning the current text contents.
- **Returns:** `Undefined`

---

#### `Slider(x1, y1, x2, y2, value, min, max)`

Basic horizontal slider returning a new value.

```js
ui.Slider(x1, y1, x2, y2, value, min, max);
```

- `x1`: `Real` - Left of the slider in GUI space.
- `y1`: `Real` - Top of the slider in GUI space.
- `x2`: `Real` - Right of the slider in GUI space.
- `y2`: `Real` - Bottom of the slider in GUI space.
- `value`: `Real` - Current slider value.
- `min`: `Real` - Minimum slider value.
- `max`: `Real` - Maximum slider value.
- **Returns:** `Real` - New slider value after input.

---

#### `TextInput(x1, y1, x2, y2, id, value, placeholder, style_id, tooltip)`

Text input control with simple focus/blur and placeholder.

```js
ui.TextInput(x1, y1, x2, y2, id, value, placeholder, style_id, tooltip);
```

- `x1`: `Real` - Left of the input box in GUI space.
- `y1`: `Real` - Top of the input box in GUI space.
- `x2`: `Real` - Right of the input box in GUI space.
- `y2`: `Real` - Bottom of the input box in GUI space.
- `id`: `Any` - Stable id for focus tracking.
- `value`: `String` - Current string value.
- `placeholder` *(optional)*: `String` - Placeholder when empty.
- `style_id` *(optional)*: `String` - Style key to resolve look.
- `tooltip` *(optional)*: `String` - Tooltip text to show on hover.
- **Returns:** `Struct` - Struct with { value, active }.

---

#### `Toggle(x1, y1, x2, y2, label, value, style_id, tooltip)`

Toggle with a checkbox-style box and label.

```js
ui.Toggle(x1, y1, x2, y2, label, value, style_id, tooltip);
```

- `x1`: `Real` - Left of the toggle row in GUI space.
- `y1`: `Real` - Top of the toggle row in GUI space.
- `x2`: `Real` - Right of the toggle row in GUI space.
- `y2`: `Real` - Bottom of the toggle row in GUI space.
- `label`: `String` - Text for the toggle.
- `value`: `Bool` - Current value.
- `style_id` *(optional)*: `String` - Style id from the theme toggle styles.
- `tooltip` *(optional)*: `String` - Tooltip text to show on hover.
- **Returns:** `Bool` - New value after this frame.

---

#### `ToolbarSeparator(x, y, height)`

Toolbar separator with consistent styling.

```js
ui.ToolbarSeparator(x, y, height);
```

- `x`: `Real` - X coordinate of the separator line.
- `y`: `Real` - Top of the separator line.
- `height`: `Real` - Height of the separator.
- **Returns:** `Undefined`

---

#### `TooltipRequest(text, anchor_x, anchor_y, delay_ms)`

Request a tooltip to display after the default delay (unless another control replaces it).

```js
ui.TooltipRequest(text, anchor_x, anchor_y, delay_ms);
```

- `text`: `String` - Tooltip copy to show.
- `anchor_x`: `Real` - X coordinate in GUI space.
- `anchor_y`: `Real` - Y coordinate in GUI space.
- `delay_ms` *(optional)*: `Real` - Delay before showing, in milliseconds.
- **Returns:** `Undefined`

---

#### `WheelConsumed()`

Returns whether a scroll region has claimed the wheel this frame.

```js
ui.WheelConsumed();
```

- **Returns:** `Bool`

---

#### `Window(x1, y1, x2, y2, style_id)`

Draw the base window background + border using the theme palette.

```js
ui.Window(x1, y1, x2, y2, style_id);
```

- `x1`: `Real` - Left of the window.
- `y1`: `Real` - Top of the window.
- `x2`: `Real` - Right of the window.
- `y2`: `Real` - Bottom of the window.
- `style_id` *(optional)*: `String` - Style key to resolve look.
- **Returns:** `Undefined`

---

