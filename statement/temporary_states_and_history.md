---
layout: default
title: Temporary States & History
parent: Statement
nav_order: 6
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Temporary States & History

Suppose we have a state machine that controls game-flow with three states: `Gameplay`, `Pause` and `Settings`. The player is in `Gameplay`, and then the player opens `Pause`:

```text
Gameplay
    ↓
Pause
```

From `Pause` they open `Settings`:

```text
Gameplay
    ↓
Pause
    ↓
Settings
```

Closing ``Settings` should return to `Pause`. Closing `Pause` should return to Gameplay.

If `Settings` can only ever be opened from `Pause`, hard-coding `ChangeState("Pause")` works fine, but it stops working as soon as `Settings` can also be opened from the title screen, an accessibility menu, or somewhere else. `Settings` doesn't really have one fixed destination. It needs to remember who opened it.

Statement's Push/Pop stack is for that kind of temporary detour.

---

## Pushing a temporary state

If Gameplay is active:

```js
state_machine.PushState("Pause");
```

attempts a normal transition to `Pause`. When the transition succeeds, Statement remembers the state that was left:

```text
active state: Pause
return stack: [Gameplay]
```

`Pause` can then open `Settings`:

```js
state_machine.PushState("Settings");
```

and the stack becomes:

```text
active state: Settings
return stack: [Gameplay, Pause]
```

The state at the end of that stack is the next return destination.

A blocked Push doesn't add anything. If Gameplay is exit-locked and `PushState("Pause")` fails, `Pause` was never entered, so there stack would stay empty.

---

## `PopState()` returns to the last pushed state

From `Settings`:

```js
state_machine.PopState();
```

attempts to return to `Pause`:

```text
active state: Pause
return stack: [Gameplay]
```

Then another Pop:

```js
state_machine.PopState();
```

returns to `Gameplay`:

```text
active state: Gameplay
return stack: []
```

Settings doesn't need to know that `Pause` opened it and `Pause` doesn't need to know that `Gameplay` opened it. Each Push records the state being left and each successful Pop simply consumes the most recent recorded return destination.

---

## Push and Pop still run the normal lifecycle

`PushState()` won't freeze `Gameplay` halfway through its code and suspend it in place. A successful Push is simply a normal Statement transition:

```text
Gameplay Exit
    ↓
Pause becomes active
    ↓
Pause Enter
```

A successful Pop does the same lifecycle in the other direction, just like any other transition types.

This means transition payloads work normally, state age resets when the destination becomes active, hooks can observe the transition, and hosted child machines follow their reset mode just as they would for `ChangeState()`.

The Push/Pop stack only remembers **where a temporary detour should return**. It won't preserve the source state's running lifecycle.

---

## Sending data into and back out of a temporary state

Push accepts the same transition payload as `ChangeState()`:

```js
state_machine.PushState("Pause", {
	source: "combat"
});
```

`Pause` reads it from the Enter transition:

```js
var _pause = new StatementState(self, "Pause")
	.AddEnter(function(_state, _transition) {
		var _data = _transition.GetData();
		pause_source = _data.source;
	});
```

Pop can carry a different payload back to the restored state:

```js
state_machine.PopState({
	settings_changed: true
});
```

If `Pause` is the saved destination, `Pause`'s Enter handler receives that Pop transition and can inspect and act upon the new payload.

---

## Locks and guards still apply

Push and Pop use normal transition rules for leaving the active state, so exit locks and guards can block them.

If `Gameplay` is locked:

```js
var _result = state_machine.PushState("Pause");
```

the Push will return `EXIT_LOCKED`, and the stack stays unchanged.

The same is true while trying to Pop out of a locked temporary state: Being on the return stack doesn't give the destination permission to bypass the active state's exit rules.

Forced Push and Pop calls are available when you genuinely need to ignore those rules:

```js
state_machine.PushState("Pause", undefined, true);
state_machine.PopState(undefined, true);
```

The third Push argument and second Pop argument are the same force flag used by the other transition APIs.

---

## A blocked Pop keeps its destination

Suppose `Pause` is active and the stack contains `Gameplay`:

```text
active state: Pause
return stack: [Gameplay]
```

`Pause` is currently exit-locked, so:

```js
var _result = state_machine.PopState();
```

is blocked.

Statement leaves the stack alone:

```text
active state: Pause
return stack: [Gameplay]
```

The failed attempt hasn't invalidated the return destination. Once `Pause` can be left, calling `PopState()` again tries `Gameplay` again.

Statement only removes the top stack entry after the Pop transition succeeds and actually enters that saved state.

---

## Popping an empty stack

When there is no saved return destination:

```js
var _result = state_machine.PopState();
```

Statement returns a blocked result with:

```js
eStatementTransitionBlockReason.STACK_EMPTY
```

The active state doesn't change.

In a fixed pause/settings flow, an empty Pop usually means the caller's logic is wrong somewhere.

---

## Looking at the return stack

Get the number of saved return states:

```js
var _depth = state_machine.GetStateStackDepth();
```

Peek at the state the next Pop would try to restore:

```js
var _return_state = state_machine.PeekStateStack();
```

`PeekStateStack()` returns the `StatementState` struct, or `undefined` if the stack is empty.

You can also discard the whole return path without changing the active state:

```js
state_machine.ClearStateStack();
```

Use that when the game flow changes direction and old temporary-state returns should no longer be valid.

---

## The previous state

Push/Pop only remembers a return destination when you explicitly use `PushState()`.

Statement separately remembers the most recent **different state** left by any successful transition.

If the machine moves through:

```text
Idle -> Move -> Attack
```

then while Attack is active:

```js
state_machine.GetPreviousStateName();
```

returns:

```text
Move
```

You can ask Statement to transition back to that state:

```js
state_machine.PreviousState();
```

This is still a normal transition, so it can be blocked by the current state's locks or guards and it can carry data:

```js
state_machine.PreviousState({ reason: "cancel" });
```

---

## `PreviousState()` isn't a return stack

From Attack, this:

```js
state_machine.PreviousState();
```

takes the machine back to Move.

That successful transition makes Attack the state that was just left. Calling `PreviousState()` again can therefore take the machine back toward Attack.

```text
Move -> Attack
PreviousState()
Attack -> Move
PreviousState()
Move -> Attack
```

Push/Pop behaves differently because it keeps its own stack of future return destinations and removes each destination after a successful Pop.

Use `PreviousState()` when the behaviour really means "go back to the state I just came from." Use Push/Pop for a temporary detour that may be nested and needs a stable return path.

---

## State history

The same successful transitions that update the singular previous state also build a longer history.

Suppose the machine travels through:

```text
Idle -> Move -> Attack -> Hitstun -> Idle
```

Every time it leaves one state for a different state, Statement records the state that was left. By default it keeps the most recent 32 entries.

Ask how many are stored:

```js
var _count = state_machine.GetHistoryCount();
```

Read one by zero-based index:

```js
var _old_state = state_machine.GetHistoryAt(0);
```

`GetHistoryAt()` returns the stored `StatementState`, not just its name. Index `0` is the oldest retained entry, and `GetHistoryCount() - 1` is the newest.

If the index you provide is outside the stored history, Statement reports the bad index and returns `undefined`.

---

## Checking a recent history position by state name

When you only need to ask whether a particular state appears at one recent position, use:

```js
state_machine.WasPreviouslyInState("Attack");
```

With no depth supplied, this means:

```text
Was the most recently left state Attack?
```

Pass a larger depth to look farther back:

```js
state_machine.WasPreviouslyInState("Attack", 2);
```

Depth `1` is the newest history entry, depth `2` is the one before that, etc. This reads from the recent end of the same history that `GetHistoryAt()` exposes from oldest to newest.

---

## History records visits, including repeated names

If the machine follows:

```text
Idle -> Move -> Idle -> Move -> Attack
```

then Idle and Move will appear more than once in history.

`ReenterState()` is a little different. A re-entry restarts the lifecycle of the current state, but the machine didn't leave one state for a different one, so it doesn't add another previous-state history entry. This lets you to distinguish between "This was a natural flow of states" versus "I purposefully re-entered a historical state that I don't want to be considered part of the flow", if that distinction ends up being useful for you for some reason.

---

## Push and Pop also appear in ordinary history

Push and Pop are normal transitions, so they update the machine's previous-state history as well as the separate return stack.

For:

```text
Gameplay
    Push Pause
    Push Settings
    Pop Pause
```

the history records the states that were actually left during those transitions.

The two records still answer different questions:

```text
Push/Pop stack
    which saved state should a future Pop return to?

history
    which states did the machine leave in the past?
```

A return stack points forward whereas the History looks backward.

---

## Changing the history limit

A new Statement machine keeps 32 previous-state entries.

Change that with:

```js
state_machine.SetHistoryLimit(8);
```

Once the limit is positive, older entries are dropped as new ones arrive so the history stays within that size.

A value of `0` or below removes the limit:

```js
state_machine.SetHistoryLimit(0);
```

That doesn't clear the entries already stored. It only changes how much history Statement will retain from then on.

For long-lived machines, unbounded history will keep growing, so only use it when the full lifetime really is useful to your game or tooling.

---

## Clearing history

Clear the recorded previous-state history with:

```js
state_machine.ClearHistory();
```

This also clears the singular previous-state reference, so:

```js
state_machine.GetPreviousStateName();
```

returns `undefined`, and `PreviousState()` has no destination until another successful transition leaves a state.

`ClearHistory()` doesn't touch the Push/Pop stack. If you want to discard temporary return destinations too, call:

```js
state_machine.ClearStateStack();
```

separately.

Stopping the machine clears its runtime history and return stack as part of stopping.

---

## The three kinds of state memory side by side

For a temporary detour with a known return path:

```js
state_machine.PushState("Settings");
state_machine.PopState();
```

For the state that was left most recently:

```js
state_machine.GetPreviousStateName();
state_machine.PreviousState();
```

For a longer record of where the machine has been:

```js
state_machine.GetHistoryCount();
state_machine.GetHistoryAt(index);
state_machine.WasPreviouslyInState("Attack", depth);
```

They can all contain some of the same state objects because they are observing the same transitions, but they aren't interchangeable. Pick the one that matches the behaviour you're interested in at the time.

---

## Putting it together: Pause and Settings

Here's a simple temporary-state flow:

```js
var _gameplay = new StatementState(self, "Gameplay")
	.AddUpdate(function() {
		if (pause_pressed) {
			state_machine.PushState("Pause");
		}
	});

var _pause = new StatementState(self, "Pause")
	.AddUpdate(function() {
		if (settings_pressed) {
			state_machine.PushState("Settings");
		}
		else if (pause_pressed) {
			state_machine.PopState();
		}
	});

var _settings = new StatementState(self, "Settings")
	.AddUpdate(function() {
		if (back_pressed) {
			state_machine.PopState();
		}
	});

state_machine
	.AddState(_gameplay)
	.AddState(_pause)
	.AddState(_settings)
	.Start();
```

Opening the two temporary states produces:

```text
Gameplay
    Push Pause
        stack [Gameplay]

Pause
    Push Settings
        stack [Gameplay, Pause]

Settings
    Pop
        returns to Pause
        stack [Gameplay]

Pause
    Pop
        returns to Gameplay
        stack []
```

If Settings is later opened from a different state with `PushState("Settings")`, the Settings code doesn't need to change. Its Pop returns to whichever state was actually saved.

---

## Next: timing, pause, and updates

The examples so far have used `GetStateTime()` as a convenient count without spending much time on how Statement decides when an update should happen.

[**Timing, Pause & Update Behaviour**](timing_pause_and_updates) covers that clock, including Statement's default event-based updates, optional elapsed-time scheduling, local and global time scale, state timers, gameplay pause, and how timing moves through nested machines.
