---
layout: default
title: Locks & Queues
parent: Statement 2
nav_order: 5
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Locks & Queues

Imagine the player has started a heavy attack. During the committed part of the animation, pressing a movement key shouldn't immediately cancel it:

```text
Attack
    ↓
player requests Move
    ↓
stay in Attack for now
```

Throwing the input away entirely can feel just as bad. If the player presses Move a moment before the attack becomes interruptible, we may want the game to remember that request and use it as soon as Attack can be left for better game-feel.

```text
Attack begins
    ↓
Attack can't be left yet
    ↓
player requests Move
    ↓
remember Move
    ↓
Attack becomes interruptible
    ↓
enter Move
```

Those are two different jobs in Statement. **Exit locks and guards** control whether the active state may be left. The **queue** stores one transition request so it can be attempted later.

---

## Locking a state while something is in progress

A state can block ordinary transitions with:

```js
_state.LockExit();
```

Because a state handler receives its own `StatementState` struct, Attack can claim and release the lock itself:

```js
var _attack = new StatementState(self, "Attack")
	.AddEnter(function(_state) {
		_state.LockExit();
		sprite_index = spr_player_attack;
		image_index = 0;
	})
	.AddUpdate(function(_state) {
		if (image_index >= 4) {
			_state.UnlockExit();
		}
	});
```

`LockExit()` without a name uses the default lock name. Until `UnlockExit()` removes it, a normal request such as:

```js
var _result = state_machine.ChangeState("Move");
```

is blocked with:

```js
eStatementTransitionBlockReason.EXIT_LOCKED
```

The same lock also blocks ordinary automatic transition rules, Push/Pop, queued transitions, and all other **non-forced** ways of leaving the state.

---

## Named locks can handle overlapping locking reasons

One simple "locked" boolean becomes awkward as soon as two unrelated things both need to lock the state seperately, and unlocking the state requires both to unlock.

Suppose your player is stunned because they have been hit by a freezing spell **and** snared at the same time. If both systems toggle the same flag, whichever one finishes first would accidentally unlock the state while the other is still active.

Statement gives you the opportunity to name each lock:

```js
_stunned
	.LockExit("frozen")
	.LockExit("snared");
```

When the freeze effect wears off:

```js
_stunned.UnlockExit("frozen");
```

`Stunned` is still exit-locked because `"snared"` is still present. Later:

```js
_stunned.UnlockExit("snared");
```

removes the last reason and ordinary transitions can leave again.

Calling `LockExit()` twice with the same name won't create two copies of that lock. The name identifies the reason, so the code that owns `"frozen"` can add and remove that one reason without disturbing anything else, and vice versa for `"snared"`.

---

## Inspecting exit locks

You can check whether any lock exists:

```js
_state.IsExitLocked();
```

Check whether a single named locked reason is active:

```js
_state.HasExitLock("frozen");
```

Count the currently active lock names:

```js
var _count = _state.GetExitLockCount();
```

or clear every lock on the state (perhaps you cast "Dispel stun"):

```js
_state.ClearExitLocks();
```

When a transition is blocked by a lock, `GetBlockDetail()` contains one of the active lock names, which can be useful in debugging:

```js
var _result = state_machine.ChangeState("Move");

if (_result.GetBlockReason() == eStatementTransitionBlockReason.EXIT_LOCKED) {
	EchoDebugInfo("Blocked by lock: " + string(_result.GetBlockDetail()));
}
```

Most gameplay code only needs to add and remove the lock it owns. The inspection methods are mostly useful when UI, diagnostics, or more dynamic systems need to see the state of the gate.

---

## Use an exit guard when leaving depends on a condition

A lock fits something with a beginning and an end:

```text
animation commitment starts -> add "animation" lock
release frame is reached     -> remove "animation" lock
```

Sometimes there is nothing to add or remove. The state can leave whenever some condition is true at the moment a transition is attempted.

Suppose `Climb` may only be left while the player's hands are free:

```js
var _climb = new StatementState(self, "Climb")
	.AddExitGuard("hands_free", function() {
		return !hands_busy;
	});
```

Every ordinary attempt to leave Climb asks that function:

```text
hands_busy == true
    -> guard returns false
    -> transition is blocked

hands_busy == false
    -> guard returns true
    -> transition may continue
```

---

## A guard can inspect the transition being attempted

When the answer depends on the destination, the guard can receive both the current state and the in-progress transition:

```js
_climb.AddExitGuard("safe_destination", function(_state, _transition) {
	if (_transition.GetTargetName() == "Dead") {
		return true;
	}

	return !hands_busy;
});
```

Statement supplies `_state` as the first argument and the `StatementTransitionResult` as the second. Here the guard allows `Dead` regardless of `hands_busy`, while other ordinary destinations still require free hands.

Most guards don't need these arguments. You can just use `function()` without the arguments instead, if the condition can answer from owner variables alone.

---

## Several guards can protect the same state

Exit guards are named too, and every attached guard must return `true` before an ordinary transition can leave.

```js
_climb
	.AddExitGuard("hands_free", function() {
		return !hands_busy;
	})
	.AddExitGuard("not_tethered", function() {
		return !tethered;
	});
```

If the first guard fails, Statement stops there and reports:

```js
eStatementTransitionBlockReason.EXIT_GUARD
```

`GetBlockDetail()` gives you the name of the guard that returned `false`:

```js
var _result = state_machine.ChangeState("Fall");

if (_result.GetBlockReason() == eStatementTransitionBlockReason.EXIT_GUARD) {
	EchoDebugInfo(
		"Blocked by guard: " + string(_result.GetBlockDetail())
	);
}
```

Guard names need to be unique within the state. Statement will reject a second guard with the same name rather than silently replacing the first.

You can manage them individually or clear the whole set:

```js
_state.RemoveExitGuard("hands_free");
_state.HasExitGuard("hands_free");
_state.GetExitGuardCount();
_state.ClearExitGuards();
```

---

## Choosing between a lock and a guard

Use a lock when some code owns a temporary reason that needs to be claimed and later released:

```js
_state.LockExit("animation");
...
_state.UnlockExit("animation");
```

Use a guard when the answer can be calculated whenever Statement tries to leave:

```js
_state.AddExitGuard("hands_free", function() {
	return !hands_busy;
});
```

A state can use both at the same time. Statement checks for active locks first, then checks each guard. An ordinary transition has to make it through both layers before the state is allowed to exit.

---

## Forced transitions ignore locks and guards

Some transitions deliberately outrank the normal exit restrictions:

```js
state_machine.ChangeState("Dead", undefined, true);
```

The third argument forces the transition, so Statement skips the current state's locks and guards.

Automatic rules can be forced too:

```js
var _death_rule = new StatementTransitionRule(
	"Dead",
	function() {
		return hp <= 0;
	}
)
.SetForce();
```

The locks will prevent all other non-forced transitions from happening, but this particular transition (and all other transitions that have been forced) has essentially been told not to consult them.

---

## Queues & Blocked `ChangeState()`

Suppose Attack is locked and the player asks for Move:

```js
var _result = state_machine.ChangeState("Move");
```

If that returns `EXIT_LOCKED`, Statement won't remember the call and quietly retry it later. The request has finished, and the machine stayed in Attack.

That's usually the best default behaviour for failed transitions. If the player taps something that should be ignored while stunned, there is usually no reason for that input to fire after the stun ends.

If you want the request to specifically survive until a later update, put it in the queue.

---

## Queueing one state change for later

Instead of trying Move immediately, you can queue a state:

```js
state_machine.QueueState("Move");
```

which stores a pending request on the machine.

By default, Statement tries that request before a later logical Update:

```text
next logical update begins
    ↓
try queued Move
    ↓
still locked? keep Move queued
    ↓
otherwise enter Move
```

An `EXIT_LOCKED` or `EXIT_GUARD` result leaves the request in the queue, rather than consuming it, so Statement can try it again on another update.

This is well-suited to input buffering:

```js
if (move_pressed) {
	state_machine.QueueState("Move");
}
```

The input code doesn't need to know which animation frame will unlock Attack. It records the intent once, and Attack releases its own lock when it becomes interruptible.

`QueueState()` only stores existing destinations. If the supplied state name doesn't exist, Statement reports the bad name and leaves the queue unchanged.

---

## The queue holds one request, not a list

A Statement machine has one queued destination, along with that destination's payload and force flag.

```js
state_machine.QueueState("Move");
state_machine.QueueState("Attack");
```

After the second call, the queued request is `Attack`. The newer request replaces the older one.

This is essentially "latest intent" buffering, where the newest input is the one you care about. If your game needs to preserve a sequence such as light attack, light attack, heavy attack and consume every command in order, that sequence should live in its own gameplay data structure that you setup and control rather than in Statement's single transition slot.

---

## Queue data and force

The queued transition can carry a payload, just like normal transitions:

```js
state_machine.QueueState("Attack", {
	target: target_enemy,
	combo: combo_count
});
```

When that request eventually succeeds, Attack receives the payload through its normal Enter transition.

A queued transition can also be forced:

```js
state_machine.QueueState("Dead", undefined, true);
```

Why can we force a queued state? We just spent a while going over how queues are intended to allow input buffering until guards and locks end. Well, queueing and forcing control different parts of a transition: Queueing decides **when** Statement attempts the transition, whereas forcing decides **whether exit locks and guards can block that attempt**.

This is most useful when a transition should happen at a particular queue phase (we will touch on queue phases in a moment) but should still outrank ordinary exit restrictions.

For example, let's say you're doing some important processing in a state's Update callback and want to transition to `"Dead"`, but you don't want the `"Dead"` Enter code to run immediately when the transition is requested. Instead, you want the current state to completely finish its Update first.

Queueing lets you defer the transition until the configured queue phase, while forcing it still allows that transition to break past locks and guards.

So queueing really has two roles: **input buffering** and **deferring transitions until current processing has finished**. Input buffering is the much more common scenario, which is why we've mostly focused on that while discussing queues.

---

## Inspecting or cancelling the queue

You can check whether a request is waiting:

```js
state_machine.HasQueuedState();
```

And read its destination and payload:

```js
var _name = state_machine.GetQueuedStateName();
var _data = state_machine.GetQueuedStateData();
```

When the queue is empty, both getters return `undefined`.

Or you can discard the pending request if needed:

```js
state_machine.ClearQueuedState();
```

Clear it when some later piece of gameplay invalidates an old buffered input before it gets a chance to fire.

---

## Choosing when Statement processes the queue

A new machine uses:

```js
eStatementQueuePhase.BEFORE_UPDATE
```

so a pending request gets its first chance before the active state's Update handler runs.

For some states, the thing that makes them interruptible happens inside Update. An attack might remove its commitment lock when its timer reaches the release point. In that case, process the queue afterward:

```js
state_machine.SetQueuePhase(eStatementQueuePhase.AFTER_UPDATE);
```

The order now looks like:

```text
Attack Update runs
    ↓
Attack removes "commit" lock
    ↓
Statement tries queued Move
    ↓
Move can enter on the same logical update
```

For code that wants to decide the exact moment itself:

```js
state_machine.SetQueuePhase(eStatementQueuePhase.MANUAL);
```

and then:

```js
var _result = state_machine.ProcessQueuedState();
```

`MANUAL` disables automatic queue processing. `ProcessQueuedState()` attempts whatever is currently queued immediately, regardless of which queue phase is configured.

You can read the current phase with:

```js
state_machine.GetQueuePhase();
```

---

## Which failed queue attempts stay pending?

A queued request that fails because of an exit lock or exit guard stays in the queue. Those are temporary conditions that may change on a later update.

```text
queued Move
    ↓
Attack still has "commit" lock
    ↓
EXIT_LOCKED
    ↓
Move remains queued
```

Once the lock is gone, another processing attempt can succeed.

If queue processing finds that the destination is already the current state, Statement clears the request rather than retrying the same-state transition forever. A successful queued transition clears the request as part of the change as well.

---

## A later successful transition supersedes old buffered input

Suppose `Move` is waiting in the queue, then damage code successfully sends the machine to `Hitstun`:

```js
state_machine.ChangeState("Hitstun");
```

Statement clears the queued Move when that non-queued transition succeeds. Otherwise an input that belonged to the situation before Hitstun could survive and fire unexpectedly afterward.

A blocked direct transition won't clear the queue because the active state never changed.

The same clearing behaviour applies when an automatic rule, Push/Pop, re-entry, or another successful non-queued transition takes over first.

---

## Queue processing and automatic rules

The queue and transition rules share the same update cycle, so their configured phases decide which gets a chance first.

With the default queue phase, the broad order is:

```text
queued transition BEFORE_UPDATE
    ↓
BEFORE_UPDATE transition rules
    ↓
active state Update
    ↓
AFTER_UPDATE transition rules
```

With `AFTER_UPDATE` queue processing:

```text
BEFORE_UPDATE transition rules
    ↓
active state Update
    ↓
queued transition AFTER_UPDATE
    ↓
AFTER_UPDATE transition rules, if the same state is still active
```

If an earlier successful transition changes the state, the old state's later work doesn't continue as though nothing happened. Statement Lens is especially useful when a queue and several automatic rules are all capable of moving the same machine and you want to see which attempt actually occurred.

---

## Putting it together: a buffered attack

Suppose Attack is committed for its first 60 logical updates (or a second, if you're updating once per Step at 60fps). Movement input during that window should be remembered and used as soon as the commitment ends.

```js
var _attack = new StatementState(self, "Attack")
	.AddEnter(function(_state) {
		_state.LockExit("commit");
		sprite_index = spr_player_attack;
		image_index = 0;
	})
	.AddUpdate(function(_state) {
		if (state_machine.GetStateTime() >= 60) {
			_state.UnlockExit("commit");
		}

		if (move_pressed) {
			state_machine.QueueState("Move");
		}
	})
	.AddExit(function(_state) {
		// A forced interruption should not leave stale locks behind.
		_state.ClearExitLocks();
	});
```

Have the machine process buffered input after Attack's Update:

```js
state_machine.SetQueuePhase(eStatementQueuePhase.AFTER_UPDATE);
```

Now the 60th Attack update can remove the lock and immediately allow a previously queued Move:

```text
player presses Move during Attack
    ↓
Move is queued
    ↓
Attack keeps updating while "commit" exists
    ↓
Attack reaches update 60 and unlocks
    ↓
AFTER_UPDATE queue processing tries Move
    ↓
Move enters
```

Attack owns the restriction and the queue holds the remembered destination, so the input code doesn't need to know the exact update where Attack becomes interruptible.

---

## Next: temporary states and history

A queue remembers a destination that hasn't happened yet. The next page deals with a different kind of memory: entering a temporary state and remembering where to return afterward.

[**Temporary States & History**](temporary_states_and_history) covers `PushState()` / `PopState()`, the immediately previous state, and the longer history of states the machine has left.
