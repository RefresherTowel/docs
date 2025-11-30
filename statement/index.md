---
layout: default
title: Statement          # children will use this as `parent:`
nav_order: 2              # order among top-level items
has_children: true        # marks this as a section (still supported)
---

# Statement - State Machine for GameMaker

**Statement** is a lightweight, reusable **state machine system** for GameMaker.  

Designed to be dropped directly into any project and used immediately, with only a few lines of code.

Statement is part of the **RefresherTowel Games** suite of reusable frameworks for GameMaker. All of these
frameworks come with extensive documentation and complete integration with Feather to make using them as 
easy as possible.

Statement gives you:

- A `Statement` state machine bound to an instance or struct.
- Named `StatementState` states with inbuilt **Enter / Update / Exit / Draw** handlers (plus easy extension of adding new handlers).
- Built-in **state machine** timing (i.e. how long a state has been active for).
- Optional **queued transitions**, **state stacks**, **history**, **per-state timers**, and more for advanced use cases.

---

## Introduction

Statement replaces scattered `if (state == ...)` checks or giant switch statements with a clear structure:

- Each object (or struct) owns a `Statement` state machine.
- Each state machine manages one active `StatementState` at a time.
- States can define:
  - `Enter` (runs once when entered)
  - `Update` (runs each when called, usually each Step)
  - `Exit` (runs once when leaving)
  - `Draw` (optional, simply run it in a Draw Event to add an easy to manage drawing handler for a state)

You can keep things **very simple** (just one state and `Update`) or layer on more advanced features as your project grows.

---

## Basic Features (Core)

These are the features most users will use day-to-day:

- **Owner-bound states**  
  State code is automatically scoped to the owner instance or struct. No need to worry about figuring out how to access your instance from within the state.

- **Clear lifecycle**  
  Per-state handlers:
  - `Enter` - one-time setup when the state becomes active.
  - `Update` - per-step logic while active.
  - `Exit` - one-time cleanup when the state stops being active.
  - `Draw` - optional per-state drawing.

- **Simple state timing**  
  Each state machine tracks **how long the current state has been active** (in frames):
  - `GetStateTime()` / `SetStateTime()` on the `Statement` state machine.

- **Named states & transitions**  
  - `Statement.AddState(state)`
  - `Statement.ChangeState("Name")`
  - `Statement.GetStateName()`

- **Feather-friendly**  
  Types are annotated for better autocompletion and linting in the GameMaker code editor.

If you're a beginner or just need something straightforward, you can safely stop at these features.

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
  - Optional advanced timers on each `StatementState` handled via time sources.
  - Helpers like `TimerStart()`, `TimerGet()`, `TimerPause()`, `TimerRestart()`, `TimerKill()`.
  - Global `StatementStateKillTimers()` to clean up all state timers at once (on a change of room, for instance).

- **State-change hook**
  - `SetStateChangeBehaviour(fn)` to run custom logic whenever the state changes (for logging, analytics, signals, etc).

- **Custom state handlers**
  - Add extra handlers beyond the `Begin`, `Update`, `End` and `Draw` easily (for instance, add an `Animation End` handler
    for the state, that runs in the Animation End Event).

You can safely ignore these until you actually need them.

---

## Requirements

- **GameMaker version:**  
  Any version that supports:
  - Struct constructors: `function Name(args) constructor { ... }`
  - `method(owner, fn)`
  - `time_source` APIs

- **Scripts you need:**
  - The Statement  script library.
  - The **Echo** debug helper library (shipped free with Statement). It provides the debug functions used in the examples: `EchoDebugInfo`, `EchoDebugWarn`, and `EchoDebugSevere`.

> Statement's examples and internal debug calls use these Echo helpers. If you remove Echo from your project or choose not to import it, you can either write `show_debug_message()`
> wrappers with the same names, or update the debug calls in Statement to use your own debug system instead.
{: .note}

No additional extensions or assets are required.

---

## Quick Start (Core)

A minimal example: single machine, single state.

**Create Event**
```gml
state_machine = new Statement(self);

var idle = new StatementState(self, "Idle")
    .AddEnter(function() {
        EchoDebugInfo("Entered Idle");
    })
    .AddUpdate(function() {
        // Simple idle behaviour
        image_angle += 1;
    });

state_machine.AddState(idle);
```

**Step Event**
```gml
state_machine.Update();
```

**Draw Event (optional)**
```gml
state_machine.Draw();
```

That's all you need to get a basic state machine up and running.

> If you find `new Statement(self)` and `new StatementState(self, "Idle")` a bit verbose, it's perfectly fine to define your own project-specific helper function (for example `StateM()`) that
> wraps the constructor call. Statement itself does **not** ship any  helpers like this to avoid name clashes with other libraries.
{: .note}

Always construct `Statement` and `StatementState` using the `new` keyword (for example `state_machine = new Statement(self);`). Calling these constructors without `new` will silently fail and your state machine will not work.
{: .warning}

---

## FAQ (Core)

### Do I need one `Statement` per object?

Yes, that's the intended pattern:

- In an object's Create event: `state_machine = new Statement(self);`
- Then add states to that machine for that object.

You *can* bind a machine to a pure struct if you're doing headless logic, but "one object, one machine" is the most common.

---

### Do I have to use the Draw support?

No. Draw is completely optional.

Common patterns:

- **Logic only**: call `Update()` in Step and ignore Draw.
- **Logic + visuals**: call `Update()` in Step and `Draw()` in Draw, with per-state `AddDraw()` handlers.

---

### What's the difference between `GetStateTime()` and per-state timers?

- `GetStateTime()` / `SetStateTime()` live on the **Statement** state machine itself:
  - Represent "how long the current state has been active (in frames)".
  - Automatically reset on state change.
  - Incremented in `Update()` while a state is active.

- Per-state timers (`TimerStart()`, `TimerGet()`, etc.) live on each individual **State** struct:
  - Optional, more flexible timers backed by `time_source`.
  - Once started, a state's timer advances every frame via the time-source system until you change out of that state or explicitly stop/pause/reset the timer, even if `Update()` is not being called for a while.
  - Good for specialised behaviour that needs pausing, restarting, or independent ticking across different update rates (for example, these timers continue ticking even if the instance is disabled).

In 99% of cases you'll just use `GetStateTime()` on the machine and ignore per-state timers entirely.

---

## FAQ (Advanced)

### When should I use queued state changes?

Use **queued changes** when:

- You're inside a state's `Update` and want to change state *next* frame.
- You want to avoid "mid-update" re-entrancy issues where code before and after `ChangeState()` runs in different states.

Use **immediate `ChangeState()`** when:

- You're doing a hard switch (spawning, respawning, teleporting).
- You know you're at a safe point in your logic.
- In general, it's safe to simply use `ChangeState()`, but queueing will occasionally be necessary in some circumstances.

---

### When do I need Push/Pop instead of `ChangeState`?

Use `PushState` / `PopState` for:

- Temporary overlays (pause, menu, inventory, cutscenes).
- Situations where you want to "change to a new state and then return to whatever state we were in before".

Use `ChangeState` when:

- You're switching between normal, "flat" states (Idle -> Move -> Attack).

---

## Help & Support

- **Bug reports / feature requests:**  
  Use the GitHub Issues page for this repository.

- **Questions / discussion / examples:**  
  Join the project's Discord (link in the repository README).  
  That's where you can:
  - Ask implementation questions.
  - Share snippets and patterns.
  - See example integrations from other users.

If you hit behaviour that looks wrong, include:

- A short code snippet.
- Which functions you called (`ChangeState`, `QueueState`, etc).
- Any relevant debug output from `EchoDebugInfo/EchoDebugWarn/EchoDebugSevere`.
