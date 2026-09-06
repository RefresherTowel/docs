---
layout: default
title: Statement Lens
parent: Statement
nav_order: 11
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Statement Lens

A state machine can be completely sensible to look at in code and still be awkward to debug while the game is running.

Maybe the player is stuck in `Attack`. The code says an automatic rule should return to `Idle`, but staring at that rule doesn't tell you what the machine actually did. You want to know whether the rule was evaluated, whether something blocked the transition, whether an old request is sitting in the queue, or whether a child machine is paused somewhere below the state you're looking at.

**Statement Lens** is Statement's live visual debugger. It shows the running machines, their states and connections, recent transitions, failed attempts, timing and pause information, queues, history, rules, breakpoints, and the rest of the debug data Statement records while `STATEMENT_DEBUG` is enabled.

Most things you do in Lens are inspection. Selecting a state or connection, moving around the graph, searching, and changing the graph layout don't alter the state machine. Controls that do change the machine use explicit actions such as **Jump to state**, **Process queue**, or **Clear state stack**.

I encourage you to play around with Lens. Right click things to see if they have a context menu, try running your state machine through Lens, try pausing the state machine and stepping through its logical updates one at a time and so on. You can't break your state machines through Lens (everything will go right back to normal the next time you boot your game).

The rest of this page is just detailing the specifics, so use it for reference if there's something in Lens that you don't quite understand.

---

## Turning Statement debugging on

Lens only exists while:

```text
STATEMENT_DEBUG = 1
```

`STATEMENT_DEBUG` is one of the editable macros at the top of Statement's macro script. When you turn it off, the Lens UI and the debug records it relies on are left out of normal use.

You'll normally leave it on while developing and turn it off for a release build if you don't want Statement's debugging machinery running there.

---

## Opening Lens

Lens is an Echo Chamber window. If you're using the Echo Chamber setup bundled with Statement, you don't need to add anything to your Create, Step, or Draw GUI Events to run it.

Press **F1** to open Echo Console, then choose **Statement Lens**. Statement creates the Lens window the first time you open it and keeps Lens updated automatically from then on. If you close the window and open it again later, the existing window is brought back to the front.

If you're using your own Echo Chamber root instead of the bundled controller, you can open Lens on that root directly:

```js
StatementLensOpen(ui_root);
```

Statement still takes care of updating Lens after it has been opened. Your Echo Chamber setup is only responsible for running that root's desktop in Draw GUI:

```js
ui_root.RunDesktop();
```

`RunDesktop()` belongs to Echo Chamber rather than Lens, and you only want one desktop call for a given root. If you're using Echo Chamber's bundled controller, it already runs the default root's desktop, so don't add another `RunDesktop()` just for Lens.

Older versions of Statement required `StatementLensUpdate()` in a Step Event. The current version doesn't. Existing projects can remove that call; if it's still present, Statement ignores it once Lens's automatic updates are running.

There is no `StatementLensDraw()` call in the current version (there was in previous versions). Lens is drawn as part of the Echo Chamber desktop now.

---

## What you're looking at

The Lens window is built around the state graph:

```text
┌─────────────────────────────────────────────────────────────┐
│ Machine picker       pause status       Pause / Step        │
├─────────────────────────────────────────────────────────────┤
│ Layout / Activity / Connections / Search / Settings         │
├─────────────────────────────────────┬───────────────────────┤
│                                     │                       │
│                                     │   Details             │
│            State graph              │                       │
│                                     │ Machine / Selection   │
│                                     │ / States              │
│                                     │                       │
├─────────────────────────────────────┴───────────────────────┤
│ Transition trace                                            │
└─────────────────────────────────────────────────────────────┘
```

The graph shows the states and the connections Statement knows about. The active state is highlighted, and selecting a state or connection fills the Details panel with the information for that item.

The transition trace along the bottom shows successful transitions, newest first. It answers a different question from **Latest attempt** in the Machine panel. The trace tells you what actually happened. Latest attempt also records a transition that was requested and then blocked.

The Details and trace panels can be resized or collapsed if you want more room for the graph.

---

## Give busy machines names

A single Statement machine on one object is easy to recognise. Several machines owned by the same object are much easier to work with if you name them:

```js
state_machine
	.SetDebugName("Player movement")
	.DebugTag("player, movement");
```

Lens uses the friendly name in the machine picker, while tags give you another way to find machines and states during debugging.

The picker can filter machines by:

- instance owners
- struct owners
- whether they currently have an active state

Hosted child machines keep their place in the hierarchy, so you can see a path such as:

```text
Player movement
└── Ground movement
```

When you're looking at a child machine, **Parent machine** moves back to the machine hosting it.

---

## Finding the state you're actually in

The first thing to check when behaviour looks wrong is often the active state.

For a simple machine:

```text
Idle
  ↓
Move
  ↓
Attack
```

Lens highlights whichever state is current.

Turn on **Follow active state** if you want the graph camera to centre itself as the machine changes state. Manual panning or zooming turns Follow active state back off, so the camera won't keep dragging you away from something you're inspecting.

You can also move around manually:

- click a state to inspect it
- click a connection to inspect that route
- click blank graph space to return to the machine selection
- drag blank space to pan
- use the mouse wheel to zoom
- use **Fit graph** to bring all visible states back into view

State cards can carry badges for things such as a Break on Enter breakpoint, a recorded error, a template-built state, or a hosted child machine. Hover information includes the state's debug activity statistics.

---

## Finding a state in a large machine

The search box matches state information such as:

- state names
- debug tags
- template names
- child-machine names

Non-string state names are searchable through the value Lens displays for them.

The default search controls include:

```text
Ctrl+F   focus search
Up/Down  move through results
Enter    select and centre
Escape   clear search
```

The **States** tab in the Details panel gives you another list view of the current search results. Its markers tell you whether a state is active, previous, or queued, and it can also show badges for breakpoints, errors, templates, and child machines.

Selecting a state in this list only inspects and centres it. It doesn't enter the state.

---

## Nested machines show their active path

With nested machines, looking at the root state alone may not tell you where the behaviour is really coming from.

Suppose the root machine is here:

```text
Grounded
└── Sprint
```

`Grounded` may be exactly the state you expected, while the active child `Sprint` explains why the player is still using sprint behaviour.

The Machine panel shows the active child path, and a state that hosts a child machine can open that child directly.

It also shows the machine's reset mode and whether pause inheritance is enabled. Timing is shown separately through Statement's global update mode, the local time scale, the root global scale, and the machine's stored update credit. There isn't a separate child "inherit time scale" setting.

---

## When a transition should have happened

Suppose `Attack` should have returned to `Idle`, but it hasn't.

Start with **Latest attempt** on the Machine page.

Statement records the newest transition request whether it succeeded or not. If it was blocked, Lens shows the same kind of reason you would get from the returned `StatementTransitionResult`, for example:

```text
Exit lock blocked transition
Exit guard blocked transition
Already in target state
Target missing
No queued transition
State stack empty
No previous state
```

A blocked guard also keeps the guard name, so a vague problem like:

```text
Attack won't leave
```

can turn into:

```text
Exit guard blocked transition: animation_finished
```

The selected state's details show its current exit-lock count and exit guards as well, which lets you compare the blocked attempt with the restrictions that are active now.

If Latest attempt already shows a successful `Attack -> Idle` transition, then the problem isn't that this request failed. Something else may have changed the machine again afterward, and the transition trace is the next place to look.

---

## Checking an automatic rule

Automatic rules carry their own debug telemetry.

Consider:

```js
_attack
	.AddTransition(
		new StatementTransitionRule("Dead", function() {
			return hp <= 0;
		})
		.SetPriority(100)
	)
	.AddTransition(
		new StatementTransitionRule("Idle", function(_state) {
			return _state.TimerGet() >= attack_duration;
		})
	);
```

Select `Attack` and its rule list shows the rules in evaluation order.

For each rule Lens can show the definition and recent evaluation information, including its target, phase, priority, payload or provider information, force setting, how many times the condition has been evaluated, how many times it passed, the latest evaluation result and tick, any block reason from the latest attempt, and a recorded condition error.

That helps with cases where the condition itself looks fine in code but the rule never gets a chance to decide anything.

Statement stops automatic-rule evaluation after the first passing rule is attempted. If a higher-priority rule passes first, a lower rule won't be evaluated during that phase. The rule telemetry lets you see that its evaluation tick didn't move rather than assuming its condition returned false.

Selecting a rule also selects the graph connection that rule contributes to.

---

## Reading the transition trace

The trace at the bottom records successful transitions newest first.

A basic row looks like:

```text
tick   Move -> Attack   Direct
```

The record also carries the payload and force flag when those are relevant.

Statement records why a transition happened, so the cause can distinguish:

```text
Start
Stop
Direct change
Automatic rule
Queued transition
Push state
Pop state
Previous state
Re-enter
Debug jump
```

For example, if `Hitstun` appeared unexpectedly, a `QUEUED` cause points you toward a buffered request rather than the code that normally calls `ChangeState("Hitstun")` directly.

Selecting a trace row selects and centres the matching connection. Its right-click menu can copy the row, copy the payload, filter the state search toward the destination, or clear the trace.

Blocked transitions don't appear in the successful trace because the machine never travelled across that connection. That's why Latest attempt is kept separately.

---

## Checking what is queued

The Machine page shows the pending queue request, including its destination, payload, force flag, and queue processing phase.

The phase is one of:

```text
Before Update
After Update
Manual
```

If the player seems to be carrying an old buffered input, you can see the exact request waiting there instead of inferring it from input code.

The same page has explicit controls to:

```text
Process queue
Clear queue
Clear previous-state history
Clear state stack
Clear transition trace
```

These buttons change the live machine. They are deliberately separate from normal selection and inspection controls.

The stack and previous-state history are displayed on the Machine page too, which is useful when `PopState()` or `PreviousState()` isn't returning where you expected.

---

## When a machine isn't updating

There are two broad things to check: runtime pause and timing.

A machine can be runtime-paused by:

- its own `SetPaused(true)`
- a parent machine whose pause it inherits
- an inactive host state keeping a child paused

Lens breaks those contributors out in the Machine details.

Debug pause is separate. A machine may also be stopped for inspection by:

- **Pause in Lens**
- a state breakpoint
- a connection breakpoint
- a debug error configured to pause
- the global debug pause

The status in the toolbar tells you whether the selected machine is gameplay-paused, paused by a machine-local Lens reason, globally debug-paused, or running.

Timing can also make a machine appear to skip work without being paused. In EVENT mode, a local scale below `1` means one call may only contribute part of a logical update. In ELAPSED_TIME mode, a short frame can also leave only part of an update stored. A local scale of `0` stops the machine from reaching new logical updates at all. The Machine page shows the global update mode, the stored fractional credit, the local time scale, and the global root time scale.

---

## Lens pause and gameplay pause are different

Clicking **Pause in Lens** calls the machine's debug pause:

```js
state_machine.DebugPause();
```

**Resume Lens pause** calls:

```js
state_machine.DebugResume();
```

That only clears the machine-local debug pause. It doesn't undo `SetPaused(true)`, inherited parent pause, host pause, or the global debug-pause setting.

This separation means you can stop a running machine for inspection without changing the pause state your game is using.

---

## Stepping one logical update

The **Step** button uses:

```js
state_machine.DebugStep();
```

It runs exactly one logical machine update, ignoring the normal update mode and time scale for that step, then restores the debug pause state.

Step is available when the machine isn't runtime-paused and either the selected machine or the global debugger is currently debug-paused.

If the machine is gameplay-paused, Step stays disabled. `DebugStep()` doesn't pretend a gameplay pause is only a debugger pause.

Stepping lets you answer questions such as:

```text
What happens on the next Statement update?
```

without changing the machine's normal time scale just to inspect it.

---

## Breaking when a state is entered

If the interesting state only lasts for a moment, set a breakpoint before reproducing the bug.

Right-click the state and enable **Break on Enter**, or select the state and use the same toggle in its Details page.

The next time that state is entered, Statement gives the machine a state-breakpoint debug pause.

Suppose `Dead` is being entered while the player still has health left. Breaking on `Dead` lets you inspect the machine at the transition instead of several frames later. You can look at the incoming connection, transition cause, payload, trace, and the code or rule that led there while the relevant state is still current.

Resume Lens pause when you're ready to continue.

---

## Breaking on one connection

Sometimes the destination is fine, but one route into it looks suspicious.

For example:

```text
Idle -------> Hitstun
Move -------> Hitstun
Attack -----> Hitstun
```

If only `Attack -> Hitstun` is behaving strangely, select that connection and enable **Break on Transition**.

Statement pauses when that endpoint pair is successfully traversed.

The Connection details show information such as:

- source and destination states
- where the graph connection came from
- how many times it has been used
- first and most recent fired ticks
- the most recent transition cause
- last payload and force flag
- breakpoint information
- the latest connection error
- declared rules that contribute to that pair

A connection breakpoint applies to the endpoint pair rather than one particular transition rule. If several routes all produce `Attack -> Hitstun`, the breakpoint observes the transition between those states.

---

## Where graph connections come from

Lens can know about a state connection before the machine has actually travelled across it, or it can discover one from runtime behaviour.

There are three sources.

### Declared

A declared connection comes from a live `StatementTransitionRule`.

For a state-owned rule:

```js
_attack.AddTransition(
	new StatementTransitionRule("Idle", function() {
		return attack_finished;
	})
);
```

Lens can draw:

```text
Attack -> Idle
```

before that rule has ever fired.

Machine-wide rules are declared from every registered source state to their target because any of those states can potentially evaluate the rule.

### Manual links

Some transitions only appear inside ordinary gameplay code:

```js
if (got_hit) {
	state_machine.ChangeState("Hitstun");
}
```

Statement can't infer every possible direct `ChangeState()` destination while building the graph, so you can give the debugger a manual hint:

```js
_attack.DebugLinkTo("Hitstun");
```

That adds the connection to the debug graph without changing gameplay behaviour.

### Observed

Once the machine actually moves across a pair of states, Lens records that pair as observed.

A connection can be declared, manual, observed, or more than one at once.

Lens calls a connection **runtime-only** when it has been observed but has no declared rule or manual link behind it. These are useful for finding routes that only reveal themselves while the game runs.

The **Connections** menu can show or hide declared, manual, and runtime-only connections. The usage filter can narrow them to connections touching the selected state, touching the active state, or used within a recent tick window.

A debugger jump is recorded with the `DEBUG_JUMP` transition cause, but making that jump doesn't turn the route into one of your declared gameplay connections.

---

## Moving the machine from Lens

Inspecting a state never enters it.

If you deliberately want to move the live machine, right-click the state or use its Details page:

```text
Jump to state
Force jump to state
```

A normal debug jump uses Statement's normal exit rules. If the active state is locked or a guard rejects the destination, the jump can be blocked. Latest attempt records that failure.

A forced jump bypasses exit locks and guards, like a forced transition in code.

The two controls answer different debugging needs. A normal jump lets you test whether the machine can legally reach the state right now. A forced jump is for putting the machine somewhere regardless of those exit restrictions.

Both are explicit because they mutate gameplay state.

---

## Choosing a graph layout

Lens has four graph layouts.

### Layered

Layered arranges the graph around a directional flow, using the initial state as the starting root and placing disconnected groups deterministically.

It works well for machines that mostly move through recognisable stages.

### Radial

Radial places the states around a ring.

It can be easier to read when the machine doesn't have a useful left-to-right direction.

### Clustered

Clustered lets strongly connected parts of the machine collect into groups.

A large machine with several dense areas can be much easier to scan this way than as one long layered graph.

### Neighbourhood

Neighbourhood concentrates on one state. Incoming states are placed on one side and outgoing states on the other.

If you haven't selected anything, Lens uses the active state.

Use this layout when the whole graph is too busy and you're currently asking:

```text
What can reach this state, and where can it go?
```

With Follow active state enabled, the neighbourhood can move along with the machine.

---

## Seeing which states are actually used

The **Activity** menu can overlay runtime usage on the graph:

```text
Off
Total active time
Entries
Recent activity
```

**Total active time** reflects how many logical active updates a state has accumulated.

**Entries** reflects how often the state has been entered.

**Recent activity** uses real elapsed wall-clock time to make recently active states stand out and then fade. The half-life can be changed from Lens Settings.

That recent-activity fade is only a debugger visualisation. It doesn't change Statement timers, state age, time scale, or update timing.

---

## The Machine page

Click blank graph space or choose the Machine tab when the problem isn't obviously tied to one state.

The Machine page collects the live information that applies to the machine as a whole.

It includes identity and hierarchy information:

```text
debug name
tags
owner
machine path
```

Execution information includes:

```text
running state
current state
previous state
initial state
queued state
logical state age
pause contributors
```

Timing includes:

```text
update mode
stored update credit
local time scale
global root time scale
```

You'll also find the queue phase and payload, Latest attempt, machine-wide rule count, state stack, previous-state history, transition trace size, active child path, reset mode, pause inheritance, and the machine's debug error configuration.

The action buttons on this page are the ones that deliberately alter queue/history/debug records, so ordinary inspection remains read-only.

---

## The State page

Select a state when the bug belongs to one particular state.

The State page shows whether the state is active or previous, its entry count and total active time, last-enter tick, timer value and status, and the handlers registered on it.

It also shows the state's template/config information, debug tag, default debug-jump payload, manual debug links, exit locks, exit guards, hosted child machine, breakpoint, recorded error, and its automatic transition rules.

The exit values are live inspection. Clicking the state doesn't silently clear a lock or disable a guard.

From this page you can also:

```text
Centre state
Jump to state
Force jump to state
Open child machine
Copy config
Copy last error
```

Only the actions that say they change something actually change the running machine.

---

## The Connection page

Select a graph connection to see the aggregate information for that pair of states.

The Connection page shows:

```text
from / to
declared rule count
manual-link status
observed status
runtime-only status
hit count
first / last fired tick
last cause
last payload
last force flag
breakpoint information
latest error
contributing declared rules
```

When several mechanisms can lead between the same two states, the connection represents the endpoint pair while the contributing-rules list shows the particular automatic rules that declare it.

---

## Errors in Lens

With Statement debugging enabled, errors raised while Statement is invoking state handlers or evaluating transition conditions are recorded against the relevant state or connection before Statement decides what to do with the error.

A new machine's debug error behaviour is `RETHROW`, so the error is rethrown after the debug information is recorded.

If you want Statement to stop in the debugger instead, configure the machine with:

```js
state_machine.DebugSetErrorBehavior(eStatementErrorBehavior.PAUSE);
```

A caught state error then gives the machine a state-error debug pause. A transition-condition error gives it a connection-error debug pause.

State and connection cards can show error badges, and the corresponding Details page keeps the latest error message and context.

You can also ask Statement to append caught debug errors to `debug_statement_errors.log`:

```js
state_machine.DebugSetLogErrorsToFile(true);
```

That logging option is independent of whether the machine pauses or rethrows.

---

## Saved views

If you keep returning to the same corner of a large graph, use **Settings -> Save current view**.

A saved view remembers the current session's:

- graph camera
- layout
- activity mode
- connection visibility
- usage filter

Lens gives the view a label based on the selected or active state, such as:

```text
Near Attack
```

**Load saved view** restores those settings for the same live machine.

These are debugger-session views, not gameplay data you need to save with the game.

---

## A reliable way to chase a state-machine bug

When you don't yet know which part of the machine is wrong, work from what the machine actually recorded.

First, find the machine and check its current state and active child path. If the state is wrong, the transition trace tells you how it got there.

If a transition should have happened but didn't, inspect Latest attempt. A block reason may answer the question immediately.

For an automatic transition, select the source state and look at the rule telemetry. Check whether the rule was evaluated, whether it passed, and whether a higher-priority rule got there first.

If temporary-state behaviour is involved, look at the queue, stack, and previous-state history rather than reconstructing them from memory.

When the machine isn't moving, check its runtime pause contributors and timing information before assuming the Update handler is broken.

And if the interesting moment disappears too quickly, put Break on Enter on the destination state or Break on Transition on the suspicious connection, reproduce the problem, and inspect it while the debugger is stopped there.

---

## Lens keyboard controls

The default Lens key bindings are editable macros near the top of Statement's macro script.

The supplied defaults include:

```text
Ctrl+F       focus state search
Escape       close/clear the active Lens UI context
Page Up      previous machine
Page Down    next machine
F            fit graph
A            select active state
Middle mouse pan graph
Mouse wheel  zoom graph
```

The search result list uses the arrow keys and Enter while the search UI is active.

If those bindings conflict with your project, change the `STATEMENT_LENS_BIND_*` and graph-pan macros rather than editing Lens internals.

---

## If Lens itself looks wrong

### The Lens window doesn't appear

Check that:

```text
STATEMENT_DEBUG == 1
```

If you're using the Echo Chamber setup bundled with Statement, press **F1** to open Echo Console and choose **Statement Lens**. You don't need to open or update Lens anywhere else in your game code.

If you're using your own Echo Chamber root, open Lens on that root directly:

```js
StatementLensOpen(ui_root);
```

Lens won't open when debug support is disabled or when the supplied value isn't an `EchoChamberRoot`.

### Input or drawing happens twice

Check how many times the same Echo Chamber root calls:

```js
ui_root.RunDesktop();
```

If the bundled Echo Chamber controller already owns that desktop, don't add another Draw GUI call for Lens.

### Step is disabled

Step requires a debug pause and a machine that isn't runtime-paused.

Look at the pause status and Machine page. A local gameplay pause, inherited parent pause, or inactive-host pause keeps `DebugStep()` from running.

### A normal jump fails

Check Latest attempt and the active state's exit locks and guards.

Use **Force jump to state** only when you actually want to bypass those restrictions.

### A connection seems to be missing

Check the **Connections** source toggles and the usage filter.

A connection may be declared by a rule, added as a manual debug link, discovered only at runtime, or hidden by the current filter.

### A destroyed machine still appears

Use:

```text
Settings -> Prune stale machines
```

Lens also prunes the debug registry when it opens, but the Settings action lets you do it explicitly while the window is already open.

---

## Code-side debug helpers

Lens covers most day-to-day inspection, but Statement also has debug methods you can use directly in code.

Some useful ones are:

```js
state_machine.SetDebugName(...);
state_machine.DebugTag(...);
state_machine.DebugPause();
state_machine.DebugResume();
state_machine.DebugStep();
state_machine.DebugJumpToState(...);
state_machine.DebugDescribe();
state_machine.PrintStateNames();
state_machine.PrintStateHistory();
```

States also have helpers for graph hints and debugger defaults:

```js
_state.DebugLinkTo(...);
_state.DebugPayload(...);
_state.DebugBreakOnEnter(...);
_state.DebugTag(...);
```

For caught debug errors, the machine controls are:

```js
state_machine.DebugSetErrorBehavior(...);
state_machine.DebugSetLogErrorsToFile(...);
```

Use these when you want a bit of Statement's debugger information without keeping the Lens window open.

---

## Lens doesn't replace the state machine

Your gameplay still uses the normal Statement APIs:

```js
state_machine.ChangeState(...);
state_machine.QueueState(...);
state_machine.PushState(...);
state_machine.PopState(...);

_state.LockExit(...);
_state.AddExitGuard(...);
_state.AddTransition(...);
```

Lens shows what those systems are doing while the game runs and gives you a few deliberate controls for debugging them.

Once the machine is large enough that a transition can fail for several different reasons, or a root state can contain another active machine underneath it, seeing the recorded state of the system is usually more useful than adding another `show_debug_message()` and trying to reconstruct the sequence afterward.
