# Statement

A lightweight, reusable **state machine system** for GameMaker.  
Designed to be copy-pasted into any project, play nicely with Feather, and stay out of your way when you only need something simple.

Statement is part of the **Towel** suite of reusable systems for GameMaker.

Statement gives you:

- A `StateMachine` bound to an instance or struct.
- Named `State` objects with **Enter / Update / Exit / Draw** handlers.
- Built-in **state age** timing.
- Optional **queued transitions**, **state stacks**, **history**, and **per-state timers** for more advanced use cases.

---

## Introduction

Statement replaces scattered `if (state == ...)` checks with a clear structure:

- Each object (or struct) owns a `StateMachine`.
- Each machine manages one active `State` at a time.
- States can define:
  - `Enter` (runs once when entered)
  - `Update` (runs each Step)
  - `Exit` (runs once when leaving)
  - `Draw` (optional, runs each Draw if you use it)

You can keep things **very simple** (just one state and `Update`) or layer on more advanced features as your project grows.

---

## Basic Features (Core)

These are the features most users will use day-to-day:

- **Owner-bound states**  
  States are bound to an instance or struct; handlers are automatically `method(owner, fn)` wrapped so `self` behaves as expected.

- **Clear lifecycle**  
  Per-state handlers:
  - `Enter` — one-time setup when the state becomes active.
  - `Update` — per-step logic while active.
  - `Exit` — one-time cleanup when the state stops being active.
  - `Draw` — optional per-state drawing.

- **Simple state timing**  
  Each machine tracks **how long the current state has been active** (in frames):
  - `GetStateTime()` / `SetStateTime()` on the `StateMachine`.

- **Named states & transitions**  
  - `StateMachine.AddState(state)`
  - `StateMachine.ChangeState("Name")`
  - `StateMachine.GetStateName()`

- **Feather-friendly**  
  Types are annotated for better autocompletion and linting in the GameMaker code editor.

If you’re a beginner or just need something straightforward, you can safely stop at these features.

---

## Advanced Features

These features are entirely optional. You only need them if your project calls for more control or introspection.

- **Queued transitions**
  - `QueueState()` to request a state change.
  - `ProcessQueuedState()` to apply it later.
  - `SetQueueAutoProcessing()` to have `Update()` handle it automatically.

- **State stack (Push / Pop)**
  - `PushState("Menu")` / `PopState()` for temporary overlays like pause menus, cutscenes, or modals.
  - Preserves clean Enter/Exit lifecycles.

- **History & introspection**
  - `previous_state` + `previous_states[]` history.
  - `SetHistoryLimit(limit)` to cap memory usage.
  - Helpers like `GetHistoryCount()` / `GetHistoryAt()` / `GetPreviousStateName()`.

- **Per-state timers**
  - Optional timers on each `State` backed by `time_source`.
  - `TimerStart()`, `TimerGet()`, `TimerPause()`, `TimerRestart()`, `TimerKill()`.
  - Global `StateKillTimers()` to clean up all state timers at once.

- **State-change hook**
  - `SetStateChangeBehaviour(fn)` to run custom logic whenever the state changes (for logging, analytics, signals, etc).

You can completely ignore these until you actually need them.

---

## Requirements

- **GameMaker version:**  
  Any version that supports:
  - Struct constructors: `function Name(args) constructor { … }`
  - `method(owner, fn)`
  - `time_source` APIs

- **Scripts you need:**
  - The state system script (containing `StateMachine`, `State`, `StateKillTimers`, etc.).
  - Your debug system script (providing `DebugInfo`, `DebugWarn`, `DebugSevere`).

No additional extensions or assets are required.

---

## Quick Start (Core)

A minimal example: single machine, single state.

```gml
/// Create Event
state_machine = StateMachine(self);

var idle = State(self, "Idle")
    .AddEnter(function() {
        DebugInfo("Entered Idle");
    })
    .AddUpdate(function() {
        // Simple idle behaviour
        image_angle += 1;
    });

state_machine.AddState(idle);


/// Step Event
state_machine.Update();


/// Draw Event (optional)
state_machine.Draw();
```

That’s all you need to get a basic state machine up and running.

---

## FAQ (Core)

### Do I need one `StateMachine` per object?

Yes, that’s the intended pattern:

- In an object’s Create event: `state_machine = StateMachine(self);`
- Then add states to that machine for that object.

You *can* bind a machine to a pure struct if you’re doing headless logic, but “one object, one machine” is the most common.

---

### Do I have to use the Draw support?

No. Draw is completely optional.

Common patterns:

- **Logic only**: call `Update()` in Step and ignore Draw.
- **Logic + visuals**: call `Update()` in Step and `Draw()` in Draw, with per-state `AddDraw()` handlers.

---

### What’s the difference between `GetStateTime()` and per-state timers?

- `GetStateTime()` / `SetStateTime()` live on the **StateMachine**:
  - Represent “how long the current state has been active (in frames)”.
  - Automatically reset on state change.
  - Incremented in `Update()` while a state is active.

- Per-state timers (`TimerStart()`, `TimerGet()`, etc.) live on the **State**:
  - Optional, more flexible timers backed by `time_source`.
  - Good for complex behaviour that needs pausing, restarting, or independent ticking.

If you’re unsure, start with `GetStateTime()` and ignore per-state timers.

---

## FAQ (Advanced)

### When should I use queued state changes?

Use **queued changes** when:

- You’re inside a state’s `Update` and want to change state *next* frame.
- You want to avoid “mid-update” re-entrancy issues where code before and after `ChangeState()` runs in different states.

Use **immediate `ChangeState()`** when:

- You’re doing a hard switch (spawning, respawning, teleporting).
- You know you’re at a safe point in your logic.

---

### When do I need Push/Pop instead of `ChangeState`?

Use `PushState` / `PopState` for:

- Temporary overlays (pause, menu, inventory, cutscenes).
- Situations where you want to “return to whatever state we were in before”.

Use `ChangeState` when:

- You’re switching between normal, “flat” states (Idle → Move → Attack).

---

## Help & Support

- **Bug reports / feature requests:**  
  Use the GitHub Issues page for this repository.

- **Questions / discussion / examples:**  
  Join the project’s Discord (link in the repository README).  
  That’s where you can:
  - Ask implementation questions.
  - Share snippets and patterns.
  - See example integrations from other users.

If you hit behaviour that looks wrong, include:

- A short code snippet.
- Which functions you called (`ChangeState`, `QueueState`, etc).
- Any relevant debug output from `DebugInfo/Warn/Severe`.
