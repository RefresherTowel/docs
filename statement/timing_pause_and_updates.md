---
layout: default
title: Timing, Pause & Update Behaviour
parent: Statement 2
nav_order: 7
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Timing, Pause & Update Behaviour

Up to this point, the Step Event has just called:

```js
state_machine.Update();
```

and we've treated that as "give Statement its update." With Statement's default settings, that's exactly how it behaves: each time your Step Event runs `Update()`, it gives the machine one logical update opportunity. If you call it once from the Step Event, then it behaves like ordinary Step-driven GameMaker code.

Time scale can change how often those opportunities become whole state-machine updates, and Statement can also switch globally to using GameMaker's `delta_time` when you want elapsed frame time to decide the pace instead. Statement will try to make it so that if a frame takes longer to update, it has the chance to run the state multiple times in a frame, if it runs too quickly, it will try to run the state fewer times (skipping updates occasionally when a frame runs).

Statement can't apply `delta_time` to the code inside your Update handlers, so `ELAPSED_TIME` mode instead uses a fixed-step approximation: It measures how much real frame time has passed and runs as many ordinary logical updates as that time represents.

This preserves the average rate of ordinary step-based behaviour, but it isn't the same as writing properly delta-aware code. Fast frames can produce no logical update, while slow frames can produce several, so input checks and other once-per-Step behaviour need particular care when Statement is running in `ELAPSED_TIME` mode (for instance, if you are checking for player input with `keyboard_check_pressed()` inside of Update for a state and Statement happens to skip a logical update for that frame because of fast running frames, that input can be completely missed, or conversely, if Statement runs multiple logical updates during one frame, the same input can potentially be seen more than once, so a combination of code outside of Statement and inside of Statement can be better here).

The state code itself still looks like normal step-based GameMaker code:

```js
var _move = new StatementState(self, "Move")
	.AddUpdate(function() {
		x += hsp;
	});
```

Statement isn't giving that handler a delta value (you can easily get that yourself with the `delta_time` variable GM gives you if you need it). It simply changes how often the machine's logical Update runs. If you want to implement a proper version of `delta_time`, then you should use the default Step based update mode and then do the usual `x += hps * _dt;` style code that delta time actually requires (we'll touch on this in more detail a little later).

---

## One logical Statement update

When these docs say **logical update**, they mean one complete pass through Statement's update behaviour, not necessarily one GameMaker Step Event.

During one logical update, Statement can process the configured queue phase and automatic-transition phases, advance the active state's age and timer, run the active state's Update handler, and give its hosted child machine an update opportunity (a child machine is a state machine that is owned by another state machine, we'll get to know a lot more about them on the next page).

With the default update mode, a root machine called once per Step and left at a time scale of `1` processes one logical update per Step:

```text
GameMaker Step
    ↓
state_machine.Update()
    ↓
one Statement logical update
```

Once time scale, pause, elapsed-time scheduling, or nested machines get involved, those two counts can diverge. `GetStateTime()` and Statement's state timer count logical updates, not raw Step Events.

---

## Choosing how Statement updates

Statement has one update mode shared by every state machine. The default is:

```js
eStatementUpdateMode.EVENT
```

In **EVENT** mode, every call to `Update()` begins with one update opportunity. In the normal setup where an object's Step Event calls its root machine once, that means one opportunity per Step before time scale is applied.

You can read the current mode with:

```js
var _mode = StatementGetUpdateMode();
```

If you want Statement to use real elapsed frame time instead, switch the whole library to:

```js
StatementSetUpdateMode(eStatementUpdateMode.ELAPSED_TIME);
```

In **ELAPSED_TIME** mode, a root machine being updated by your game compares the current `delta_time` with GameMaker's target frame duration and turns that into update credit.

Imagine the current call contributes half an update:

```text
0.5 update credit
    ↓
not enough for a logical update
    ↓
keep 0.5
```

If the next call contributes another half:

```text
stored 0.5
+ new 0.5
= 1.0
    ↓
run one logical update
```

A slow frame can contribute more than one whole update. If the machine reaches `2.5` updates of credit, Statement can run two logical updates during that one call and keep the fractional `0.5` for later.

The important part is that the state itself doesn't have to care which mode Statement is using. Code such as:

```js
x += 4;
```

still runs once for each logical update. `EVENT` mode starts from one opportunity per call, while ELAPSED_TIME mode starts from however much frame time has actually passed.

Because the update mode is global, you don't set `EVENT` or `ELAPSED_TIME` separately on individual machines. Switching it changes where all Statement machines get their update timing from.

---

## Several updates in one call have a cap

One call to `Update()` can sometimes produce several logical updates. In `ELAPSED_TIME` mode that can happen while catching up after a slow frame, and in either mode a high enough time scale can create several updates from one opportunity.

Statement limits the number of whole updates one `Update()` call may process with:

```js
STATEMENT_MAX_UPDATES_PER_CALL
```

The macro is in Statement's editable settings and defaults to `8`.

If a call owes more whole updates than the cap allows, Statement runs up to the cap and drops the extra whole backlog. It keeps only the fractional remainder.

For example, with a cap of 8:

```text
12.4 updates due
    ↓
run 8
    ↓
drop the extra 4 whole updates
    ↓
keep 0.4 credit
```

That lets `ELAPSED_TIME` mode catch up after an ordinary slow frame, while preventing a very large hitch or extreme time scale from turning one call into an essentially unlimited replay loop.

---

## Changing one machine's speed

Every machine has a local time scale:

```js
state_machine.SetTimeScale(0.5);
```

At `0.5`, the machine processes logical updates at half its normal rate. In the default EVENT mode, a machine called once per Step gets `0.5` of an update from the first call, keeps that half, then reaches a whole update on the second call. In other words, it updates once every two Steps.

At:

```js
state_machine.SetTimeScale(2);
```

that same `EVENT`-mode machine can process two logical updates from each ordinary call to `Update()`.

`ELAPSED_TIME` mode uses the same scale in exactly the same place. A scale of `0.5` halves the updates produced by elapsed frame time, while `2` doubles them. Both update modes behave the same in regards to the time scaling.

Read the current value with:

```js
var _scale = state_machine.GetTimeScale();
```

Negative values are clamped to `0`.

Because the scale changes the cadence of the **whole machine**, everything driven by its logical updates stays together: Update handlers, state age, state timers, automatic transition checks, queue processing, and child timing.

---

## A scale of zero stops logical updates

In either update mode:

```js
state_machine.SetTimeScale(0);
```

stops the machine reaching new logical updates.

Its active state's Update handler doesn't run, state age doesn't advance, state timers don't advance, and its child isn't given new timing opportunities because the parent isn't processing logical updates in the first place.

This isn't the same mechanism as `SetPaused(true)`. Pause has special behaviour for hosted children that opt out of inherited pause, which we'll get to below.

---

## Global time scale for root machines

Statement also has a global scale:

```js
StatementSetGlobalTimeScale(0.5);
```

The global value is applied when your game updates a **root machine** directly (a root machine simply being a state machine that is not a child of another state machine). In the normal setup where each object calls its root machine from Step, this gives you one place to slow or speed every Statement hierarchy without changing each root's local scale.

Read it's current value with:

```js
var _global_scale = StatementGetGlobalTimeScale();
```

Hosted child machines don't multiply the global value again. Neither does an independent machine whose `Update()` is called from inside another Statement machine's logical update. In both cases the outer machine has already been slowed or sped up before that inner update opportunity exists.

So with:

```text
global scale = 0.5
root local scale = 1
child local scale = 1
```

the root runs at half its normal rate in `EVENT` mode, and the child follows the logical updates the root actually processes. The child doesn't apply another `0.5` on top simply because the global scale exists.

---

## State age counts logical updates

We've already used:

```js
state_machine.GetStateTime();
```

to time states.

Statement resets state age to `0` when a state becomes active. Each logical update of that state advances the age by `1` before the state's Update handler runs.

So:

```js
if (state_machine.GetStateTime() >= 20) {
	state_machine.ChangeState("Idle");
}
```

will become true during the twentieth logical update of that state.

In the default `EVENT` mode, with a scale of `1` and one `Update()` call per Step, that lines up with the twentieth Step exactly. At `0.5`, reaching age `20` takes twice as many update calls. At `2`, it takes half as many. `ELAPSED_TIME` mode can produce zero, one, or several logical updates during a Step depending on how much real frame time passed, but the state age still counts those logical updates in exactly the same way.

You can replace the current age manually when you have a reason to:

```js
state_machine.SetStateTime(10);
```

Most gameplay timing only needs `GetStateTime()`.

---

## Per-state timers

State age is always the age of the currently active state. Sometimes one piece of a state needs a clock that can be started, paused, resumed, or reset separately.

A charge state can use its own timer:

```js
var _charge = new StatementState(self, "Charge")
	.AddEnter(function(_state) {
		_state.TimerStart();
	})
	.AddUpdate(function(_state) {
		aim_angle = point_direction(x, y, mouse_x, mouse_y);

		if (_state.TimerGet() >= 30) {
			state_machine.ChangeState("Release");
		}
	});
```

`TimerStart()` does three things:

```text
timer value -> 0
timer enabled -> true
timer running -> true
```

While that state remains active, every logical update advances the running timer by `1`.

Pause only the timer:

```js
_state.TimerPause();
```

Resume it without resetting:

```js
_state.TimerResume();
```

Read or replace its value:

```js
var _time = _state.TimerGet();
_state.TimerSet(10);
```

Stop the timer completely:

```js
_state.TimerStop();
```

`TimerStop()` disables it and resets the value to `0`. Check its current running state with:

```js
_state.TimerIsRunning();
```

When a state is left, Statement resets that state's timer value to `0` and pauses it. If the timer had previously been enabled, Statement resumes it automatically when that state becomes active again. Calling `TimerStart()` in Enter is the usual choice when every entry should explicitly begin a fresh timer.

Use state age when the clock is just "how many logical updates has this state been active?" Use the state timer when the clock needs controls of its own.

---

## Pausing machine updates

Pause a machine with:

```js
state_machine.SetPaused(true);
```

and resume its local pause with:

```js
state_machine.SetPaused(false);
```

Check the machine's effective pause state with:

```js
state_machine.IsPaused();
```

While a machine is paused, Statement suppresses that machine's normal logical update work. Its state age and timer don't advance, its Update handler doesn't run, and its automatic queue/rule processing doesn't continue.

Pause doesn't disable the whole object or block every Statement method. Code can still call:

```js
state_machine.ChangeState("Menu");
```

directly while the machine is paused, and `Draw()` can still dispatch Draw handlers. `SetPaused()` controls normal runtime update processing.

---

## A machine can be paused for several reasons

`SetPaused(true)` is the machine's **local** pause. A hosted child can also be inactive because its host state has been left, and a running child can inherit a pause from its parent machine.

`IsPaused()` gives you the final runtime answer after those causes are combined.

Those causes don't overwrite each other. If a child is locally paused, then its parent is paused as well, later resuming the parent doesn't clear the child's local pause. The child stays paused until its own `SetPaused(false)` removes that reason.

Hosted children inherit parent pause by default.

---

## Letting a child run while its parent is paused

A child machine can opt out of inherited parent pause:

```js
_child_machine.SetInheritPause(false);
```

Now imagine the parent itself is paused. When it receives a logical update opportunity, it suppresses its own state Update but still gives the active hosted child an opportunity. A child with pause inheritance disabled can use that opportunity and continue running.

```text
parent receives logical opportunity
    ↓
parent is paused -> parent Update does not run
    ↓
active child still receives an opportunity
    ↓
child doesn't inherit parent pause -> child can update
```

Restore the default behaviour with:

```js
_child_machine.SetInheritPause(true);
```

This only changes inherited **pause**. Time scale composes through the hierarchy differently.

---

## Child timing comes from parent updates

A hosted child doesn't use `EVENT` or `ELAPSED_TIME` to decide its timing separately. Every time its parent actually processes one logical update opportunity, Statement calls the child once, and the child applies its own local time scale to those parent opportunities.

Suppose:

```js
world_machine.SetTimeScale(0.5);
player_machine.SetTimeScale(0.5);
```

where `player_machine` is a hosted child of the world machine.

The root gets half its normal number of logical updates in EVENT mode:

```text
world local scale 0.5
    ↓
half the normal parent updates
```

The child is called on those parent opportunities, then applies its own `0.5`:

```text
half the normal parent updates
    ↓
player local scale 0.5
    ↓
half of those child updates
```

So the child ends up at one quarter of the normal update rate. The same relationship holds in `ELAPSED_TIME` mode: the root is simply following elapsed frame time instead of beginning each ordinary `Update()` call with a flat `1`.

A child with local scale `1` simply follows the parent's actual cadence. A grandchild repeats the same process from its own parent. There is no `SetInheritTimeScale()` switch because a child is already driven by the updates that make it through the hierarchy above it.

---

## Using GameMaker's `delta_time` inside state code

If your own state code already uses GameMaker's `delta_time`, the default `EVENT` mode is usually what you want. The machine runs once for each ordinary `Update()` call, then your state code decides how much real elapsed time that one run represents.

For example:

```js
var _move = new StatementState(self, "Move")
	.AddUpdate(function() {
		var _seconds = delta_time / 1000000;
		x += move_speed * _seconds;
	});
```

If the object's Step Event calls `state_machine.Update()` once, this handler runs once per Step at the normal time scale, and the movement line handles the frame duration itself.

You generally wouldn't combine that style with Statement's `ELAPSED_TIME` mode for the same piece of behaviour. `ELAPSED_TIME` mode already changes how often the handler runs according to elapsed frame time, so multiplying the movement by `delta_time` inside the handler as well would apply the same rough idea twice.

---

## When one state machine directly updates another

Suppose a state machine isn't hosted through `CreateSubMachine()`. Instead, its `Update()` call lives directly inside another machine's Update handler:

```js
var _outer = new StatementState(self, "Running")
	.AddUpdate(function() {
		inner_machine.Update();
	});
```

The outer machine has already decided that this logical update is happening. When it calls another Statement machine from inside that Update, Statement treats the inner call as one new update opportunity. It doesn't look back at the original Step and calculate its timing again.

With the inner machine at a local scale of `1`, the relationship is:

```text
one outer logical update
    ↓
one call to inner_machine.Update()
    ↓
one inner logical update
```

You don't need to configure that inner machine differently.

This matters most in `ELAPSED_TIME` mode. A slow frame can make the outer machine process several logical updates in one Step, which means the inner machine may be called several times. Those inner calls each receive one opportunity; they don't each read and apply the same GameMaker `delta_time` again. The global Statement scale isn't applied again either, although the inner machine's own local time scale still is.

A normal child created with:

```js
_state.CreateSubMachine();
```

follows the same timing relationship automatically. If the inner machine genuinely represents behaviour inside one of the outer machine's states, a hosted child is still usually the cleaner choice because Statement can also manage its startup, reset, pause, and hierarchy. You just don't need to make it a child purely to avoid applying `delta_time` twice.

---

## Switching update modes keeps fractional credit

A machine can be holding a fraction of a future update:

```text
stored credit: 0.4
```

Changing the global update mode doesn't clear that partial progress:

```js
StatementSetUpdateMode(eStatementUpdateMode.ELAPSED_TIME);
```

The machine still has its `0.4` afterward. That stored fraction means the same thing in either mode, so there is nothing to clear when you switch.

The same is true when switching back to:

```js
StatementSetUpdateMode(eStatementUpdateMode.EVENT);
```

Changing the update mode changes where future update opportunities come from. It doesn't reset the machines that are already running.

---

## Debug Step runs one logical update

Statement Lens can pause a machine for debugging and advance it once. The code-side equivalent is:

```js
state_machine.DebugStep();
```

A debug step runs exactly one logical machine update. It doesn't wait for the normal update mode or time scale to decide whether that step should happen, and it doesn't apply the machine or global time scale to that step.

It still respects normal gameplay pause. If `IsPaused()` is true because of the machine's runtime pause rules, `DebugStep()` doesn't override that gameplay state.

Debug pause and gameplay pause are separate because they answer different questions: one stops execution so you can inspect it, and step through it one logical update at a time, while the other is part of the game's own runtime behaviour.

---

## Putting it together: a timed attack

An attack that lasts 18 logical updates can use state age directly:

```js
var _attack = new StatementState(self, "Attack")
	.AddEnter(function() {
		sprite_index = spr_player_attack;
		image_index = 0;
	})
	.AddUpdate(function() {
		if (state_machine.GetStateTime() >= 18) {
			state_machine.ChangeState("Idle");
		}
	});
```

In the default EVENT mode, with a scale of `1` and one `Update()` call per Step, the transition happens during the eighteenth Step of the attack.

If you set:

```js
state_machine.SetTimeScale(0.5);
```

the machine processes one logical update for every two ordinary `Update()` calls. With one call per Step, it now takes 36 Steps to reach state age `18`. Nothing inside the attack had to multiply its timer by a scale. Its Update code and age are both running on the slower machine clock.

---

## Next: nested state machines

The timing model becomes especially useful once one state owns another state machine.

[**Nested State Machines**](submachines) builds a `Grounded` state with its own `Idle`, `Walk`, and `Sprint` child machine, then follows that child's startup, reset, pause, and timing behaviour through the hierarchy.
