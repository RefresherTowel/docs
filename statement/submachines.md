---
layout: default
title: Nested State Machines
parent: Statement
nav_order: 8
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Nested State Machines

A flat state machine is easy to picture:

```text
Idle
Move
Attack
Hitstun
Dead
```

As a controller grows, one of those broad states can develop choices that only make sense while that state is active.

Suppose the player can be either:

```text
Grounded
Airborne
```

and the grounded behaviour has its own modes:

```text
Idle
Walk
Sprint
```

You could flatten the names into one machine:

```text
GroundedIdle
GroundedWalk
GroundedSprint
Airborne
```

but `Idle`, `Walk`, and `Sprint` are all repeating the same larger fact: the player is grounded. Once more grounded-only behaviour appears, the flat machine starts carrying that relationship in names, transition rules, and duplicated checks.

Statement lets `Grounded` host another Statement machine:

```text
Grounded
    ├── Idle
    ├── Walk
    └── Sprint

Airborne
```

The root machine handles the broad mode. The child machine only exists as active behaviour inside its **host state**.

---

## Creating a child machine

Create the host state first:

```js
var _grounded = new StatementState(self, "Grounded");
```

Then ask that state to create its child machine:

```js
var _grounded_machine = _grounded.CreateSubMachine("Ground movement");
```

The optional name is for debugging. `_grounded_machine` is an ordinary `Statement` state machine, so child states are created and registered exactly the same way as any other states:

```js
var _idle = new StatementState(self, "Idle");
var _walk = new StatementState(self, "Walk");
var _sprint = new StatementState(self, "Sprint");

_grounded_machine
	.AddState(_idle)
	.AddState(_walk)
	.AddState(_sprint);
```

At this point the hierarchy is:

```text
Grounded
    │
    └── Ground movement
            ├── Idle
            ├── Walk
            └── Sprint
```

`Grounded` owns the child machine. When `Grounded` becomes active, Statement handles that child's runtime lifecycle along with it.

Calling `CreateSubMachine()` again on the same state returns the child it already has rather than creating a second one.

---

## Build the hierarchy before starting the root

A hosted child normally starts as part of its host state's Enter lifecycle. Its states therefore need to exist before the host is entered.

A typical Create Event builds both levels, then starts only the root machine:

```js
state_machine = new Statement(self);

var _grounded = new StatementState(self, "Grounded");
var _airborne = new StatementState(self, "Airborne");

var _grounded_machine = _grounded.CreateSubMachine("Ground movement");

_grounded_machine
	.AddState(new StatementState(self, "Idle"))
	.AddState(new StatementState(self, "Walk"))
	.AddState(new StatementState(self, "Sprint"));

state_machine
	.AddState(_grounded)
	.AddState(_airborne)
	.Start(); // We call start after everything has been setup, or we could just leave it to automatically start on the first logical update.
```

`Grounded` is the first root state, so the final `Start()` enters it. Statement then starts Grounded's child machine, whose first registered child state is `Idle`.

You wouldn't normally start the child machine yourself, like this:

```js
_grounded_machine.Start();
```

and you don't add a second child update to the object's Step Event. The Step Event call is still simply:

```js
state_machine.Update();
```

When Grounded is active, Statement gives its active child machine the appropriate update opportunities.

If the child is paused at the moment Grounded enters, Statement doesn't force it to start through that pause. It can start on a later parent update once its effective pause has cleared.

---

## A grounded movement example

Here's the same hierarchy with behaviour attached.

**Create Event**

```js
move_speed = 4;
sprint_speed = 7;

state_machine = new Statement(self);

var _grounded = new StatementState(self, "Grounded")
	.AddTransition(
		new StatementTransitionRule("Airborne", function() {
			return !place_meeting(x, y + 1, obj_solid);
		})
	);

var _grounded_machine = _grounded.CreateSubMachine("Ground movement");

var _idle = new StatementState(self, "Idle")
	.AddEnter(function() {
		sprite_index = spr_player_idle;
	})
	.AddTransition(
		new StatementTransitionRule("Walk", function() {
			var _direction = keyboard_check(vk_right) - keyboard_check(vk_left);
			return _direction != 0;
		})
	);

var _walk = new StatementState(self, "Walk")
	.AddEnter(function() {
		sprite_index = spr_player_walk;
	})
	.AddUpdate(function() {
		var _direction = keyboard_check(vk_right) - keyboard_check(vk_left);
		x += _direction * move_speed;
	})
	.AddTransition(
		new StatementTransitionRule("Idle", function() {
			var _direction = keyboard_check(vk_right) - keyboard_check(vk_left);
			return _direction == 0;
		})
	)
	.AddTransition(
		new StatementTransitionRule("Sprint", function() {
			return keyboard_check(vk_shift);
		})
	);

var _sprint = new StatementState(self, "Sprint")
	.AddEnter(function() {
		sprite_index = spr_player_sprint;
	})
	.AddUpdate(function() {
		var _direction = keyboard_check(vk_right) - keyboard_check(vk_left);
		x += _direction * sprint_speed;
	})
	.AddTransition(
		new StatementTransitionRule("Idle", function() {
			var _direction = keyboard_check(vk_right) - keyboard_check(vk_left);
			return _direction == 0;
		})
	)
	.AddTransition(
		new StatementTransitionRule("Walk", function() {
			return !keyboard_check(vk_shift);
		})
	);

_grounded_machine
	.AddState(_idle)
	.AddState(_walk)
	.AddState(_sprint);

var _airborne = new StatementState(self, "Airborne")
	.AddEnter(function() {
		sprite_index = spr_player_airborne;
	})
	.AddTransition(
		new StatementTransitionRule("Grounded", function() {
			return place_meeting(x, y + 1, obj_solid);
		})
	);

state_machine
	.AddState(_grounded)
	.AddState(_airborne)
	.Start();
```

**Step Event**

```js
state_machine.Update();
```

The root machine answers whether the player is Grounded or Airborne. While Grounded is active, its child machine answers which grounded movement mode is active.

A child machine is generally a good fit if this sentence makes sense in the context of your state machine:

> While this parent state is active, I need another state machine to choose between behaviours that only make sense given this parent state is active.

---

## Asking what the active child is doing

From the parent machine:

```js
var _child_machine = state_machine.GetChildMachine();
```

returns the submachine hosted by the currently active state, or `undefined` if the active state has no child machine.

That doesn't necessarily mean the returned child already has an active state. A hosted machine can exist while paused or while its host lifecycle is keeping it inactive. To get its active state directly:

```js
var _child_state = state_machine.GetChildState();
```

`GetChildState()` returns `undefined` when there is no active child state.

If you already have the host state itself:

```js
var _child_machine = _grounded.GetSubMachine();
```

returns the machine attached to that state whether or not Grounded is currently active.

---

## Checking a nested active path

For gameplay code that only wants to know where the hierarchy currently is, `IsInPath()` can avoid fetching each machine separately.

```js
if (state_machine.IsInPath("Grounded/Sprint")) {
	// Grounded is active and its child is Sprint.
}
```

With string state names, each slash moves down one hosted child machine, think of it kind of like you would a file directory with nested folders.

If state names are enums or some other non-string values, pass an array instead so Statement compares the original values:

```js
if (state_machine.IsInPath([
	ePlayerState.GROUNDED,
	eGroundState.SPRINT
])) {
	...
}
```

Every supplied part must match. `Grounded/Sprint` is false while the currently active hierarchy is `Grounded/Walk`.

A shorter supplied path can deliberately ask only about the levels it names. `IsInPath("Grounded")` is true while Grounded is active even if Grounded currently has an active child beneath it.

---

## Letting the child decide when the parent may leave

Sometimes the outer state shouldn't finish until its child reaches a particular point.

Suppose `AttackSequence` hosts:

```text
Windup
Strike
Recovery
```

and an ordinary request to leave AttackSequence should only succeed once the child reaches Recovery.

The parent can use the same exit-guard system we already learned:

```js
var _attack_sequence = new StatementState(self, "AttackSequence")
	.AddExitGuard("child_recovered", function(_state) {
		var _child = _state.GetSubMachine();
		return _child.IsInState("Recovery");
	});
```

Any non-forced transition out of AttackSequence now asks its child machine first.

If the guard fails:

```js
var _result = state_machine.ChangeState("Idle");
```

the result reports:

```js
eStatementTransitionBlockReason.EXIT_GUARD
```

and:

```js
_result.GetBlockDetail();
```

returns the guard name:

```text
child_recovered
```

There isn't a separate submachine locking API for this case. The child state is just part of the condition the parent uses to decide whether it may exit.

A forced transition still bypasses the guard:

```js
state_machine.ChangeState("Idle", undefined, true);
```

---

## What happens to the child when its host exits?

A child machine has a **reset mode** that controls what happens when the host state is left and later entered again.

Set it on the child:

```js
_grounded_machine.SetResetMode(...);
```

There are three modes.

### `RESET_ON_EXIT`

This is the default:

```js
_grounded_machine.SetResetMode(
	eStatementResetMode.RESET_ON_EXIT
);
```

When Grounded exits, Statement stops the child immediately. That runs the child's normal Stop lifecycle, including exiting its active child state.

```text
Grounded / Sprint
    ↓
leave Grounded
    ↓
Sprint exits and child machine stops
```

When Grounded is entered later, the child starts again from its configured initial state:

```text
enter Grounded
    ↓
child starts
    ↓
Grounded / Idle
```

Use this when leaving the host should end the child's current runtime completely.

### `REMEMBER`

```js
_grounded_machine.SetResetMode(
	eStatementResetMode.REMEMBER
);
```

Now leaving Grounded doesn't stop the child. Statement marks it inactive through its host and leaves its current child state in place.

```text
Grounded / Sprint
    ↓
leave Grounded
    ↓
Sprint is retained but receives no hosted updates
    ↓
enter Grounded later
    ↓
Grounded / Sprint resumes
```

The child isn't updating while its host is inactive, but its active state, state age, timer state, history, etc. remain available.

Use `REMEMBER` when returning to the host should continue from the child's previous position.

### `RESET_ON_ENTER`

```js
_grounded_machine.SetResetMode(
	eStatementResetMode.RESET_ON_ENTER
);
```

When Grounded is left, the child is retained just like `REMEMBER`. The difference appears when Grounded is entered again.

Statement stops the retained child at that point, then starts it fresh:

```text
Grounded / Sprint
    ↓
leave Grounded
    ↓
Sprint is retained while host is inactive
    ↓
enter Grounded later
    ↓
retained child is stopped and reset
    ↓
child starts from Idle
```

From the gameplay side, both reset modes give you a fresh child on re-entry. The lifecycle timing is different: `RESET_ON_EXIT` ends the child when the host leaves, while `RESET_ON_ENTER` delays that reset until the host is entered again.

That difference can matter if the child's Exit code or runtime history has side effects you care about.

---

## Callbacks around the hosted machine lifecycle

A host state can run code specifically when Statement handles its child machine.

`OnSubmachineEnter()` runs after the host enters and Statement has handled child startup for that entry:

```js
_grounded.OnSubmachineEnter(function(_state, _child, _transition) {
	if (_child.IsRunning()) {
		last_ground_state = _child.GetStateName();
	}
});
```

Under normal unpaused startup, the child is running by this point. If the child is effectively paused and can't start yet, the callback still runs, so check `IsRunning()` before assuming it has an active state.

`OnSubmachineExit()` runs while the host is leaving, after Statement has applied the child's exit/reset behaviour:

```js
_grounded.OnSubmachineExit(function(_state, _child, _transition) {
	grounded_child_left_host = true;
});
```

With `RESET_ON_EXIT`, the child has already been stopped by then, so `GetStateName()` returns `undefined`. With `REMEMBER` or `RESET_ON_ENTER`, the child state is still retained but paused by its inactive host.

Both callbacks run as the same owner as the host state and receive the transition that is moving the host.

Use these when the thing you need to react to is specifically the child machine entering or leaving its hosted lifetime. Ordinary Grounded behaviour still belongs in Grounded's normal Enter, Update, Exit, and Draw handlers.

---

## Pause through a hierarchy

Hosted children inherit their parent's gameplay pause by default.

If a particular child should keep running while the parent is paused:

```js
_grounded_machine.SetInheritPause(false);
```

When the paused parent receives an update opportunity, Statement suppresses the parent's own Update but still gives its active child a chance. Because this child doesn't inherit the parent pause, it can continue processing.

Restore normal inheritance with:

```js
_grounded_machine.SetInheritPause(true);
```

A child's own local pause still applies either way. Turning inheritance off only says that **parent pause** shouldn't be one of the reasons this child is paused.

---

## Time scale through a hierarchy

Children don't have a separate "inherit time scale" switch.

A child receives an opportunity whenever its parent processes a logical update, then applies its own local time scale to those opportunities.

```js
state_machine.SetTimeScale(0.5);
_grounded_machine.SetTimeScale(0.5);
```

The root processes roughly half its normal updates. The child only sees those updates, then processes roughly half of them again, so its real-time rate ends up around one quarter of normal.

With a child scale of `1`, the child follows the parent's actual cadence. The global Statement scale is applied when your game updates the root machine, before the child gets any opportunities of its own, so children don't multiply that global scale a second time.

[Timing, Pause & Update Behaviour](timing_pause_and_updates) covers the timing model in more detail.

---

## Deeper hierarchies

A child state can host its own child machine:

```text
Player
└── Combat
    └── Attacking
        └── Combo
```

Statement follows this active path recursively for hosted updates.

The root can test several levels at once:

```js
if (state_machine.IsInPath("Combat/Attacking/Combo")) {
	...
}
```

Draw also follows the active path from parent to deepest running child. Custom events can choose whether they go only to the current state, only to the deepest active state, or through the whole active path. The hooks and custom events page covers those dispatch modes.

Nesting is useful when one set of states only makes sense inside one parent mode. If two behaviours need to run independently at the same time, separate root machines are usually a better description than forcing one to become the other's child.

---

## A practical hierarchy

A player controller might eventually look like:

```text
Player state machine
├── Grounded
│   ├── Idle
│   ├── Walk
│   └── Sprint
├── Airborne
│   ├── Rise
│   └── Fall
├── Attack
│   ├── Windup
│   ├── Strike
│   └── Recovery
└── Dead
```

The root states stay readable as the player's broad modes. Each child machine contains detail that only exists while its host is active, and the host's reset mode decides whether that detail restarts or resumes the next time the player comes back.

Next: [**State Templates**](templates)
