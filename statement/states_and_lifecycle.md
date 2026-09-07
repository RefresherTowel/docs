---
layout: default
title: States & Lifecycle
parent: Statement 2
nav_order: 2
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# States & Lifecycle

The landing page kept the machine tiny. We made one state, gave it some Update code, added it to a machine, then updated it in the Step Event. But a real state machine will have more than one state in it, and the states will actually have active code running. An attack might set its animation when it begins, handle the attack while it is active, then restore a few values when it ends.

Statement gives a state four places for that code:

```text
state begins
    ↓
  Enter
    ↓
  Update
  Update
  Update
    ↓
state changes
    ↓
   Exit
```

With an optional Drawing stsep that sits beside that flow and lets you execute any visuals that belong to a specific state.

These four parts are usually called the state's **lifecycle**, allowing you to organise your code in clearly defined, well-partitioned sections instead of jamming everything into a complicated mess in the Step Event.

---

## Enter: when the state begins

Suppose entering `Attack` should start the attack animation:

```js
var _attack = new StatementState(self, "Attack")
	.AddEnter(function() {
		sprite_index = spr_player_attack;
		image_index = 0;
	});
```

Enter runs once when `Attack` actually becomes active.

Making the state does not run Enter:

```js
var _attack = new StatementState(self, "Attack")
	.AddEnter(...);
```

Adding it to the machine does not run Enter either:

```js
state_machine.AddState(_attack);
```

It runs when the machine enters `Attack`, either because the machine starts there or because something changes to it later.

Enter is a natural place for code such as choosing an animation, resetting an animation frame, capturing a target, starting a timer, or setting up values that belong to the new state.

---

## Update: while the state is active

Update contains the code that should keep running while the state remains active. This is your "Step Event" for the state:

```js
var _move = new StatementState(self, "Move")
	.AddUpdate(function() {
		var _direction = keyboard_check(vk_right) - keyboard_check(vk_left);
		x += _direction * move_speed;
	});
```

The object's Step Event still only needs:

```js
state_machine.Update();
```

Statement handles which state's Update code should run.

Movement, aiming, checking input, steering AI, checking a timer, and deciding to change into another state are all common Update jobs. If a state has nothing to do while it sits there, it doesn't need an Update handler.

> A "handler" is simply a function you're provided to Statement, which contains the code you want to run for a particular scenario. In the above code, the handler is:
> ```js
> function() {
>	var _direction = keyboard_check(vk_right) - keyboard_check(vk_left);
>	x += _direction * move_speed;
>}
>```
> And, as you can see, we've provided that as the argument to the `AddUpdate()` method. So whenever we reference a "handler" from now on, we're talking about a function you've created and given to Statement which is intended to exercise code for your game.
{: .note}

By default, one call to `Update()` gives the machine one logical update, just like ordinary Step Event code. Statement can also use real elapsed frame time to decide how often these logical updates happen, which means time scale and slow motion can affect the whole state without every line of state code having to multiply by a delta value.

It's essentially a state machine derived variation on `delta_time` (if you don't know what `delta_time` is, don't worry, it's not a detail you need to learn to use Statement). We will get deeper into that on the timing page, after the basic state-machine behaviour is familiar.

---

## Exit: when the state ends

Let's imagine that `Attack` changes a couple of values when it begins, but those changes are temporary and some should get swapped back when the state changes to another state (whatever that new state may be):

```js
var _attack = new StatementState(self, "Attack")
	.AddEnter(function() {
		image_speed = 0.5;
		can_turn = false;
	})
	.AddExit(function() {
		image_speed = 1;
		can_turn = true;
	});
```

Exit runs when Statement successfully leaves that state.

It's a good place to undo the things that only belonged to the state, such as restoring movement, clearing a temporary target, ending an effect, or returning a visual setting to normal (as you can see, we halved the `image_speed` when we entered the state, and then restored it back to normal when we exited).

---

## Draw: visuals that belong to one state

Some visuals only make sense while a particular state is active. For instance, a targeting state might draw a reticle:

```js
var _targeting = new StatementState(self, "Targeting")
	.AddDraw(function() {
		draw_circle(mouse_x, mouse_y, 12, true);
	});
```

Once you start adding draw functions to your states (even if it's only for one state), you need to start calling the machine from the object's Draw Event:

```js
state_machine.Draw();
```

If you never give your states Draw handlers, you don't need to worry about calling this method at all.

---

## State code runs as the state owner

When you create a state like this:

```js
new StatementState(self, "Move")
```

The first argument is the state owner, usually the instance the state machine is built in (as you can see, we provided the built-in GM variable `self` in this example). Any handlers attached to the state run as that owner, so an instance can use its own variables directly in the handler:

```js
.AddUpdate(function() {
	x += hsp;
	image_xscale = sign(hsp);
})
```

Statement takes care of running the handler as the owner for you.

This is why the examples can use ordinary instance variables such as `x`, `sprite_index`, `hsp`, or `can_turn` without repeatedly going through another instance reference.

---

## When a handler needs its own state

So far none of our functions have needed arguments, which is why we left them out.

However, Statement can pass the current `StatementState` into a handler when you actually need to work with the state itself. A state timer is a good example:

```js
var _charge = new StatementState(self, "Charge")
	.AddEnter(function(_state) { // Notice the _state argument we've added to our handler
		_state.TimerStart();
	})
	.AddUpdate(function(_state) { // Same here
		if (_state.TimerGet() >= 30) {
			state_machine.ChangeState("Fire");
		}
	});
```

Here, the argument we've named `_state` holds the `Charge` state whose code is running. All you need to do is add the `_state` argument to your handler (you could call it something else if you like, the important thing is adding a named argument to your function). Statement then provides the data to that argument, and you can then use it in your function.

In our function, we reference `_state` and the Statement State method `TimerStart()` to allow us to start the states own timer without having to look the state itself up by name first, or some other awkward workaround like that.

The same argument becomes useful later for things such as exit locks, config, hosted child machines, and debug helpers. But until a handler actually needs the state object, `function()` without arguments is fine.

> You might wonder how `_state` magically becomes filled with the state data, because there's no point in the code where `_state` is visibly given a value or anything. This is because it's handled internally by Statement. In the actual internal Statement codebase, Statement will run your function at the appropriate time, and hand it the current state as the first argument, something like this in pseudocode `your_state_handler(current_state);`. **That's** where the current state data gets "injected" into your `_state` variable. All you need to worry about is this: if you need access to the current state in one of the handlers you provide to a Statement State, make sure you give the first argument in your function a suitable name, and then refer to that name in the handlers body.
{: .note}

---

## Enter and Exit can see the state change that caused them

Sometimes the next state needs to know something about the change that brought it there. Hitstun, for example, may need the knockback from the hit that caused it.

Enter and Exit can receive a second argument containing information about that state change:

```js
var _hurt = new StatementState(self, "Hurt")
	.AddEnter(function(_state, _transition) { // Notice now we're giving a _state AND a _transition argument to our handler
		var _hit = _transition.GetData();
		hsp = _hit.knockback_x;
		vsp = _hit.knockback_y;
	});
```

The second `_transition` (again, you can name it anything) argument we've added after our `_state` argument receives the transition information (in the form of a struct) Statement calls that struct a `StatementTransitionResult` (which you can look up in the API Reference page). We don't need to learn everything it contains quite yet. On the next page we will use it to pass data between states and ask whether a requested change actually happened.

Because `_transition` is the second argument, the `_state` argument comes before it even if this particular function does not otherwise need `_state`.

---

## What happens when the machine changes state?

Suppose `Idle` is active and we call:

```js
state_machine.ChangeState("Move");
```

If the change succeeds:

```text
Idle is active
    ↓
Idle Exit runs
    ↓
Move becomes active
    ↓
Move Enter runs
```

Both Idle Exit and Move Enter will receive the same transition result, which is how information passed with the change can travel cleanly from one state to the next.

Statement also keeps its own previous-state information, history, state age, child-machine state, and debug information up to date. You don't need to manually mirror those things in your object just to keep the machine working or track Statement's data, most things you'll need from Statement are accessible with the correct methods.

---

## Adding states before starting the state machine

A newly created state machine has no active state yet:

```js
state_machine = new Statement(self);
```

After creation you then add the states you want it to know about (after having created the states first, of course):

```js
state_machine
	.AddState(_idle)
	.AddState(_move)
	.AddState(_attack);
```

The first state added becomes the default starting state.

For a simple Step-driven machine, you're done. The first `Update()` that runs in the Step Event will "start" the state automatically (which is when it's Enter handler is run).

You can also start it yourself once setup is complete:

```js
state_machine.Start();
```

At the point that code runs, the first state will execute its Enter code.

Explicit `Start()` is useful when you want the first state's Enter code to run immediately during setup rather than waiting for the machine's first update. For instance, you might want the state to initialise some stuff that you then go on to manipulate/access later on in the Create Event.

Building the machine before starting it also means an Enter handler can safely refer to states that were added *after* the initial state's Enter was defined, because they are already there by the time startup happens.

---

## Choosing which state starts first

Without any extra setup, the first state you add is the initial state that the state machine will start running:

```js
state_machine
	.AddState(_idle)
	.AddState(_move);
```

In this case, `_idle` is the state that will start executing once the machine starts running. If you want to choose explicitly:

```js
state_machine
	.AddState(_idle)
	.AddState(_move)
	.SetInitialState("Move")
	.Start();
```

Here, we run `SetInitialState()` to force the initial state into the `"Move"` state (assuming that's what you called the `_move` state that you added), instead of it automatically starting with the `_idle` state, since `_idle` was added first.

`Start()` also returns a transition result, so code that needs to verify startup can inspect it:

```js
var _result = state_machine.Start();

if (!_result.Succeeded()) {
	// The machine could not start.
}
```

Most machines don't need to check this. But it can become more useful in generic systems where, for instance, the initial state may be configured dynamically and the initial state successfully starting might not be guaranteed.

---

## Stopping, resetting, and rebuilding

`Stop()` ends the currently active state and leaves the machine stopped:

```js
state_machine.Stop();
```

The states you added are still there, along with the machine's settings, so it can be started again later, but the state machine will no longer run.

If you want to stop and immediately begin again from the initial state:

```js
state_machine.Reset();
```

Or if you're rebuilding the machine itself and want to remove its registered states:

```js
state_machine.ClearStates();
```

`ClearStates()` also removes machine-wide transition rules. Other machine settings remain available for the rebuilt machine.

An object that creates one machine and keeps it for its whole life will most likely never need any of these methods. They are for machines that have specific reasons they may need to be stopped, restarted, or rebuilt.

---

## Asking which state is active

For a simple check to see if a state machine is in a particular state:

```js
if (state_machine.IsInState("Attack")) {
	// Attack is active.
}
```

To get the active state's name:

```js
var _name = state_machine.GetStateName();
```

`GetStateName()` returns `undefined` while the machine is stopped.

To get the active state struct itself:

```js
var _state = state_machine.GetState();
```

You can also look up a particular registered state (whether or not it is active):

```js
var _attack = state_machine.GetState("Attack");
```

`IsInState()` accepts the state struct as well:

```js
if (state_machine.IsInState(_attack)) {
	// This exact state is active.
}
```

You don't need to worry about tracking a second `current_state` variable and keeping it synchronised because Statement can answer that question for you.

---

## State names do not have to be strings

Strings are easy to read in documentation and don't require any prior setup:

```js
new StatementState(self, "Attack");
```

But Statement also allows you to use enum values:

```js
enum ePlayerState {
	IDLE,
	MOVE,
	ATTACK
}

var _attack = new StatementState(self, ePlayerState.ATTACK);
```

Then use the same value when changing or checking state:

```js
state_machine.ChangeState(ePlayerState.ATTACK);
state_machine.IsInState(ePlayerState.ATTACK);
```

The teaching examples will mostly use strings because `"Attack"` is immediately readable, shorter and doesn't need to be pre-defined, not because Statement requires string names. Enums are often useful because they can use autocomplete, and invalid states are immediately obvious (through syntax colouring).

---

## How long has the state been active?

Statement counts how many logical updates the current state has been active for:

```js
var _time = state_machine.GetStateTime();
```

That makes simple duration checks easy:

```js
var _attack = new StatementState(self, "Attack")
	.AddUpdate(function() {
		if (state_machine.GetStateTime() >= 20) {
			state_machine.ChangeState("Idle");
		}
	});
```

This would exit the `"Attack"` state after the `Update()` handler has been run 20 times (unless you mess with the time scale of Statement, or pause the machine or something, this will correspond to 20 frames).

The age resets when another state becomes active.

You can also set it manually to an arbitrary value:

```js
state_machine.SetStateTime(10);
```

Most gameplay code will really only need `GetStateTime()`, if it needs a timer at all. But later on, the timing page will show how Statement decides when a logical update is due, how time scale changes that rate, and when the separate timer on `StatementState` is more useful than state age.

---

## Adding more than one handler of the same type

Normally, adding a second handler of the same type replaces the first:

```js
_state.AddEnter(_first);
_state.AddEnter(_second);
```

After that, `_second` is the Enter handler. `_first` is completely discarded.

If you actually need both to run sequentially, provide a second argument to choose how they should be combined:

```js
_state.AddEnter(_second, eStatementBindMode.APPEND);
```

or:

```js
_state.AddEnter(_second, eStatementBindMode.PREPEND);
```

`APPEND` runs the existing handler first and the new one afterward. `PREPEND` runs the new one first. `REPLACE`, which is the default, keeps only the new handler.

This is especially useful with templates, where shared behaviour may need a little extra code added before or after it for a specific object that is using the template.

If one handler changes state, Statement stops running any remaining composed handlers that belonged to the old state. Changing state halfway through an Update or Enter chain does not leave the rest of that old state's chain running afterward.

---

## Putting it all together

A small player machine can now look like this:

```js
state_machine = new Statement(self);

var _idle = new StatementState(self, "Idle")
	.AddEnter(function() {
		sprite_index = spr_player_idle;
		image_speed = 0;
	})
	.AddUpdate(function() {
		var _direction = keyboard_check(vk_right) - keyboard_check(vk_left);

		if (_direction != 0) {
			state_machine.ChangeState("Move");
		}
	});
	.AddExit(function() {
		image_speed = 1;
	})

var _move = new StatementState(self, "Move")
	.AddEnter(function() {
		sprite_index = spr_player_move;
	})
	.AddUpdate(function() {
		var _direction = keyboard_check(vk_right) - keyboard_check(vk_left);
		x += _direction * move_speed;

		if (_direction == 0) {
			state_machine.ChangeState("Idle");
		}
	});

var _attack = new StatementState(self, "Attack")
	.AddEnter(function() {
		sprite_index = spr_player_attack;
		image_index = 0;
	})
	.AddUpdate(function() {
		if (state_machine.GetStateTime() >= 20) {
			state_machine.ChangeState("Idle");
		}
		var _enemy_hit = instance_place(x, y, obj_enemy);
		if (instance_exists(_enemy_hit)) {
			_enemy_hit.hp -= 5;
		}
	});

state_machine
	.AddState(_idle)
	.AddState(_move)
	.AddState(_attack);
```

The Step Event doesn't care which one is active and simply needs this tiny chunk of code:

```js
state_machine.Update();
```

We simply update the machine each Step, and Statement ensures each state only runs the code for its behaviour when it's the active state.

Notice how we're not trying to juggle a bunch of "if moving, then use this sprite, or if attacking use this sprite", or worrying about trying the keep relevant state code executing at the correct time in the Step Event. That's the tangled web that leads to bugs.

Instead we sidestep that mess entirely. Each state easily handles it's own little responsibilities in a locally partitioned section of code. We set the sprite we want during Enter, we handle the actual code the state needs to run consistently during the Update and, if necessary, we reset whatever needs to be reset on Exit.

---

## Next: changing states

Next is [**Changing States & Passing Data**](changing_states_and_data).

We will create a hurt state and give the state the hit that caused it as transition data, look at the result returned by `ChangeState()`, and cover the cases where a requested change doesn't happen or where you want to restart the state that is already active.
