---
layout: default
title: Changing States & Passing Data
parent: Statement
nav_order: 3
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Changing States & Passing Data

So far we've changed states with calls like:

```js
state_machine.ChangeState("Attack");
```

This is a simple and quick way to change states. The machine leaves whatever state is active and enters the new state.

The call gets more interesting when the state we're entering needs to know what caused the change. A `Hurt` state might need the knockback from the hit that sent us there, whereas a dialogue state might need to know which NPC started the conversation or a room-transition state might need a destination and spawn point. And so on.

Statement carries that information on the transition itself, so the code that requests the change can describe what happened and the new state can decide what to do with it.

---

## Passing information into the next state

Suppose the player takes a hit:

```js
state_machine.ChangeState("Hurt", {
	knockback_x: 6,
	knockback_y: -3
});
```

The second argument is the **transition payload**. It can be any value you want to associate with that particular state change. Here we're using a struct because the hit has two values to carry.

`Hurt` receives the same transition in its Enter handler:

```js
var _hurt = new StatementState(self, "Hurt")
	.AddEnter(function(_state, _transition) {
		var _hit = _transition.GetData();

		hsp = _hit.knockback_x;
		vsp = _hit.knockback_y;
		sprite_index = spr_player_hurt;
	});
```

You can see that we've added a new argument to our handler here, `_transition` (as we have previously touched on). This is only valid for handlers placed in `AddEnter` and `AddExit`.

`_transition.GetData()` returns the payload from the `ChangeState()` call, so in this case we grab the payload struct we created during the `ChangeState()` call and store it in a temporary `_hit` variable. This payload being the exact same struct containing `knockback_x` and `knockback_y` that we created.

The flow is:

```text
a hit happens
    ↓
ChangeState() carries the hit data
    ↓
Hurt becomes active
    ↓
Hurt Enter reads that data and sets itself up
```

The hit code doesn't need to know about how `Hurt` is handling stuff internally. It simply passes the information that belongs to the hit, then `Hurt` handles its own setup.

---

## `ChangeState()` also tells you what happened

`ChangeState()` returns a `StatementTransitionResult`:

```js
var _result = state_machine.ChangeState("Attack");
```

The returned struct stored in `_result` describes this one transition attempt. If the change succeeded:

```js
if (_result.Succeeded()) {
	// Attack really became active.
}
```

If it didn't:

```js
if (_result.Blocked()) { // or alternatively: if (!_result.Succeeded()) {
	// The machine stayed where it was.
}
```

Most gameplay code doesn't need to inspect every transition result. If pressing Attack just asks the machine to enter `Attack`, you can make the call and move on. You'd want to keep the result when the caller needs to behave differently depending on whether the transition actually happened, or whether the state it is trying to transition to is a dynamic one and might not actually exist, or other unusual scenarios like that.

---

## Finding out why a transition was blocked

There are a number of reasons a transition can fail that are actually useful for gameplay scenarios. Suppose we are in the `Attack` state, and it's temporarily locked (meaning, like in a souls-like game, you can't exit an attack once you've started one). We then attempt a request to change to the `Move` state:

```js
var _result = state_machine.ChangeState("Move");
```

The movement transition would fail. We can inspect the reason:

```js
switch (_result.GetBlockReason()) {
	case eStatementTransitionBlockReason.EXIT_LOCKED:
		// Attack is currently locked.
		break;

	case eStatementTransitionBlockReason.EXIT_GUARD:
		// One of Attack's exit guards rejected the change.
		break;
}
```

You'll meet the block reasons as the relevant features come up, but a few common ones are:

```text
SAME_STATE
    the requested state is already active

TARGET_MISSING
    no registered state has that name

EXIT_LOCKED
    the current state has at least one active exit lock

EXIT_GUARD
    one of the current state's exit guards returned false
```

Other operations have reasons of their own. `PopState()`, for example, can report `STACK_EMPTY`, while `ReenterState()` can report `NO_ACTIVE_STATE` if the machine is stopped.

When a block reason has a useful extra detail, `GetBlockDetail()` gives you that too. For instance, Exit guards use it to report the name of the guard that rejected the transition.

---

## Reading the source and destination

For a successful transition:

```js
var _result = state_machine.ChangeState("Attack", { combo: 2 });
```

we can ask where it started, where it ended, and what data travelled with it:

```js
_result.GetFromName();
_result.GetToName();
_result.GetData();
```

There are state-object versions as well:

```js
_result.GetFromState();
_result.GetToState();
```

Code that isn't specific to one state can use those fields directly, for example a transition log:

```js
if (_result.Succeeded()) {
	EchoDebugInfo(
		string(_result.GetFromName())
		+ " -> "
		+ string(_result.GetToName())
	);
}
```

The result also records what kind of operation started the transition:

```js
_result.GetCause();
```

That returns an `eStatementTransitionCause` value. A normal `ChangeState()` is `DIRECT`, while queued transitions, Push/Pop, startup, automatic rules, re-entry, and debug jumps have their own causes. Most state code won't need to branch on this, but it's useful for logging and, internally, for Statement Lens because two transitions between the same states can have very different origins.

---

## Accessing the last transition payload externally

Statement also exposes the payload from the most recent successful transition:

```js
state_machine.GetLastTransitionData();
```

Use that when some unrelated code needs to ask what data arrived most recently. In our prior example, this would contain the `{ knockback_x, knockback_y }` struct we created.

Inside Enter or Exit, though, you already have the transition that caused that lifecycle call:

```js
.AddEnter(function(_state, _transition) {
	var _data = _transition.GetData();
})
```

The payload contained in `GetLastTransitionData()` gets overwritten with each state change, so it always refers to the most recent transition Statement has processing. If you cycled through a number of transitions rapidly, `GetLastTransitionData()` only returns the transition data for the last transition that occurred, whereas accessing the `GetData()` from the `_transition` argument will always refer to the exact transition data handed through to that particular state.

---

## Payloads are entirely optional

You don't need to invent an empty payload for state changes that have nothing to carry:

```js
state_machine.ChangeState("Idle");
```

For that transition:

```js
_transition.GetData();
```

returns `undefined`.

---

## Changing state doesn't return from your function

One ordinary GML control-flow detail is easy to forget when the machine itself changes immediately.

```js
.AddUpdate(function() {
	if (hp <= 0) {
		state_machine.ChangeState("Dead");
	}

	hp_regen += 1;
})
```

If the transition succeeds, `Dead` is active as soon as `ChangeState()` finishes, however GM still carries on with the rest of this function, so `hp_regen += 1` still runs.

If the old state's code should stop there, return yourself:

```js
.AddUpdate(function() {
	if (hp <= 0) {
		state_machine.ChangeState("Dead");
		return;
	}

	hp_regen += 1;
})
```

Statement can stop later functions in an `APPEND` or `PREPEND` handler chain after the state changes because Statement owns that chain. It can't decide where the control flow inside one of your functions already running should end.

---

## Requesting the state that's already active

Suppose `Hurt` is active and another hit arrives:

```js
var _result = state_machine.ChangeState("Hurt", {
	knockback_x: 3,
	knockback_y: -2
});
```

A normal `ChangeState()` doesn't restart `Hurt`. Statement returns a blocked result with:

```js
eStatementTransitionBlockReason.SAME_STATE
```

No Exit or Enter lifecycle runs, and the new payload isn't delivered through a fresh Enter because the machine never left and re-entered the state.

So code can repeatedly ask for `Attack` without accidentally resetting the state every time that code runs.

---

## Restarting the current state purposefully

Sometimes a same-state restart **is** what you want. If another hit should restart `Hurt`'s animation and duration, use:

```js
state_machine.ReenterState({
	knockback_x: 3,
	knockback_y: -2
});
```

`ReenterState()` deliberately runs the active state's Exit and Enter lifecycle again:

```text
Hurt is active
    ↓
ReenterState(new hit)
    ↓
Hurt Exit
    ↓
Hurt becomes freshly active
    ↓
Hurt Enter receives the new hit
```

The state age resets as part of the re-entry, just as it does when another state becomes active.

If the machine has no active state, there is nothing to re-enter, so the returned result is blocked with `NO_ACTIVE_STATE`.

---

## `EnsureState()` uses the normal non-reentering behaviour

Statement also provides:

```js
state_machine.EnsureState("Attack");
```

At the moment this uses the same transition behaviour as `ChangeState()`. If `Attack` is already active, the result reports `SAME_STATE` and the lifecycle doesn't restart.

`EnsureState()` can read nicely in code whose intent is "make sure we're in this state," which can be useful for code external to the state machine. Use `ReenterState()` when the intent is specifically to restart the state that's already running.

---

## Missing targets

A typo such as:

```js
var _result = state_machine.ChangeState("Atack");
```

can't resolve to a registered state. Statement returns a blocked result with:

```js
eStatementTransitionBlockReason.TARGET_MISSING
```

and Statement reports the missing state through its debug logging.

For hard-coded state names, that's normally a simple bug to fix (and can often be avoided entirely by using enums with autocomplete instead of a string). The structured result can be useful here, but it's often more useful when the destination is chosen dynamically and failure is something the caller can legitimately handle.

---

## Forced transitions

The third `ChangeState()` argument controls whether the transition ignores the current state's exit locks and guards:

```js
state_machine.ChangeState("Dead", undefined, true);
```

Here the `true` means **force this transition**.

A common use is a state that should resist ordinary interruptions but still allow something more important to take over, such as an attack that might be locked against movement until its committed frames are over, while death should still be allowed immediately.

The transition result remembers that the original request was forced:

```js
_result.WasForced();
```

Force doesn't bypass a missing destination or make an otherwise invalid request valid. It's specifically designed as an escape hatch for exit locks and exit guards.

---

## Exit code can redirect an in-progress transition

Exit code has one extra transition behaviour to account for.

Suppose `Normal` is leaving for `Attack`, but its Exit handler notices that the player has died:

```js
var _normal = new StatementState(self, "Normal")
	.AddExit(function() {
		if (hp <= 0) {
			state_machine.ChangeState("Dead");
		}
	});
```

If `Normal` is already in the middle of leaving, that nested `ChangeState("Dead")` redirects the transition that's already happening. Statement doesn't recursively run `Normal`'s Exit handler again.

So this request:

```js
var _result = state_machine.ChangeState("Attack");
```

can finish like this:

```text
original request: Attack
final target:      Dead
entered state:     Dead
```

The result keeps both pieces of information:

```js
_result.GetRequestedName();
_result.GetTargetName();
_result.GetToName();
```

and tells you whether a redirect happened:

```js
_result.WasRedirected();
_result.GetRedirectCount();
```

A redirect can replace the transition payload, but it doesn't replace the original force setting. An ordinary transition stays ordinary after a redirect, while a transition that started forced stays forced.

Most machines won't need to write redirect logic, but knowing how it behaves prevents Exit code from feeling mysterious if it ever requests another state while a transition is already underway.

---

## Putting it together: Hitstun

Here's a small `Hurt` state that uses transition data and deliberately re-enters when another hit arrives.

```js
var _idle = new StatementState(self, "Idle")
	.AddEnter(function() {
		sprite_index = spr_player_idle;
		image_speed = 1;
	})
	.AddUpdate(function() {

		// When we get hit we create the payload and enter the hurt state
		if (place_meeting(x, y, obj_enemy_bullet)) {
			var _hit_data = {
				knockback_x: 6,
				knockback_y: -3
			};

			state_machine.ChangeState("Hurt", _hit_data);
			exit;
		}
	});

var _hurt = new StatementState(self, "Hurt")
	.AddEnter(function(_state, _transition) {
		hit = _transition.GetData();

		hsp = hit.knockback_x;
		vsp = hit.knockback_y;
		
		sprite_index = spr_player_hurt;
		image_index = 0;
	})
	.AddUpdate(function() {
		x += hsp;
		y += vsp;

		hit.knockback_x *= 0.95;
		hit.knockback_y *= 0.95;

		hsp = hit.knockback_x;
		vsp = hit.knockback_y;

		// If we get hit again while in the hurt state, we reenter the hurt state
		if (place_meeting(x, y, obj_enemy_bullet)) {
			var _hit_data = {
				knockback_x: 6,
				knockback_y: -3
			};
			state_machine.ReenterState(_hit_data);
		}

		if (state_machine.GetStateTime() >= 12) {
			state_machine.ChangeState("Idle");
		}
	});

state_machine
	.AddState(_idle)
	.AddState(_hurt)
	.Start();
```

The hit code provides the hit. `Hurt` owns the knockback setup, animation reset, and duration. A second hit uses the explicit re-entry because restarting the state is the intended behaviour.

---

## Next: automatic transitions

So far every transition has been requested from a particular piece of code. The next page covers conditions that belong to a state for as long as it remains active, such as "leave Move when movement input reaches zero."

[**Automatic Transitions**](automatic_transitions) turns those conditions into `StatementTransitionRule` objects that Statement can evaluate during its normal update cycle.
