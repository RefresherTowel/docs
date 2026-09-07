---
layout: default
title: Hooks & Custom Events
parent: Statement 2
nav_order: 10
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Hooks & Custom Events

Most code in Statement belongs to a particular state. Attack starts its own animation, Move checks movement input, Hitstun decides when it has finished, etc.

Some code doesn't belong to one state, though. You might want to log every successful state change, no matter which two states were involved. You may also have a normal GameMaker event such as Animation End that different states need to handle in different ways.

Statement has two tools for those jobs:

- **machine hooks** run around every successful transition on one machine
- **custom events** let the active state handle an event that came from somewhere else in your game

We'll have a look at both these tools.

---

## Watching every transition on a machine

Suppose you want to keep the latest state change around for a debug display.

You could put this in every state's Enter handler, but then every state has to know about a piece of debugging code that has nothing to do with its behaviour. A machine hook gives you one place to observe the transition instead (and to easily remove or disable for when you release your game):

```js
state_machine.AddAnyTransitionHook(function(_result) {
	last_transition_text =
		string(_result.GetFromName())
		+ " -> "
		+ string(_result.GetToName());
});
```

If the machine changes from `Move` to `Attack`, the hook runs once after `Attack` becomes the active state.

The `_result` argument is the same kind of `StatementTransitionResult` returned by `ChangeState()`, so the hook can inspect the whole transition:

```js
_result.GetFromName();
_result.GetToName();
_result.GetData();
_result.WasForced();
_result.GetCause();
```

You don't have to add anything to `Move` or `Attack` for this to happen. The hook belongs to the machine and observes every successful transition that passes through it.

---

## The three hook points

There are three machine-wide hook lists because sometimes the exact point in the transition matters.

For a normal change from `Move` to `Attack`, Statement runs this sequence:

```text
Move Exit
    ↓
any-exit hooks
    ↓
Attack becomes active
    ↓
any-transition hooks
    ↓
any-enter hooks
    ↓
Attack Enter
```

All three hooks receive the transition result.

### `AddAnyExitHook()`

An any-exit hook runs after the old state's Exit handler, while the old state is still active:

```js
state_machine.AddAnyExitHook(function(_result) {
	show_debug_message(
		"Leaving " + string(_result.GetFromName())
	);
});
```

This is the hook to use when machine-wide code needs to happen on the way out, before Statement commits to the destination state.

### `AddAnyTransitionHook()`

An any-transition hook runs just after Statement switches the machine to the new state:

```js
state_machine.AddAnyTransitionHook(function(_result) {
	transition_count++;
});
```

At this point the transition has happened, but the new state's Enter handler hasn't run yet.

Logging, counters, transition recording, and similar machine-wide observation often fit naturally here.

### `AddAnyEnterHook()`

An any-enter hook runs after the destination becomes active and immediately before its Enter handler:

```js
state_machine.AddAnyEnterHook(function(_result) {
	last_entered_state = _result.GetToName();
});
```

Use this when shared setup needs to happen before each state's own Enter code.

Blocked transitions don't reach any of these hooks. If a lock or guard prevents a transition, there was no successful Exit/Enter lifecycle to observe, so the returned transition result is where you inspect the failure.

---

## Hooks get the transition result

A hook takes one argument:

```js
function(_result) {
	...
}
```

You can ask that result for whichever details the hook needs:

```js
_result.Succeeded();
_result.GetFromState();
_result.GetFromName();
_result.GetToState();
_result.GetToName();
_result.GetRequestedName();
_result.GetTargetName();
_result.GetData();
_result.WasForced();
_result.GetCause();
_result.WasRedirected();
_result.GetRedirectCount();
```

For example, a debug object can keep the result itself instead of copying several fields out of it:

```js
state_machine.AddAnyTransitionHook(function(_result) {
	last_transition_result = _result;
});
```

The transition-result page covered the difference between the requested, target, and final destination names. Those same distinctions still apply here, including redirects.

---

## Hooks run as the machine owner

When you create a machine like this:

```js
state_machine = new Statement(self);
```

`self` becomes the machine owner. Statement binds its hooks to that owner, just as it does with state handlers.

That means instance variables work directly inside the callback:

```js
state_machine.AddAnyTransitionHook(function(_result) {
	transition_count++;
	last_state = _result.GetToName();
});
```

You don't need:

```js
method(self, function(_result) {
	...
})
```

Statement handles that binding when you add the hook.

---

## Adding several hooks

Hooks are lists rather than single callback slots. Adding another one doesn't replace the earlier hook:

```js
state_machine.AddAnyTransitionHook(function(_result) {
	transition_count++;
});

state_machine.AddAnyTransitionHook(function(_result) {
	last_transition_result = _result;
});
```

Both run, in the order they were added.

If you need to rebuild those lists while the game is running, each kind can be cleared separately:

```js
state_machine.ClearAnyExitHooks();
state_machine.ClearAnyTransitionHooks();
state_machine.ClearAnyEnterHooks();
```

Machines that set their hooks up once in the Create Event usually never need the clear methods. Think of them as escape hatches for peculiar situations when your game actually requires them.

---

## An any-exit hook can redirect the transition

The changing-states page showed that a state's Exit handler can call `ChangeState()` to redirect the transition currently in progress.

An any-exit hook runs at the same pre-commit part of the lifecycle, so it can redirect too:

```js
state_machine.AddAnyExitHook(function(_result) {
	if (must_die && _result.GetTargetName() != "Dead") {
		state_machine.ChangeState("Dead");
	}
});
```

Imagine the original request was:

```js
state_machine.ChangeState("Idle");
```

If `must_die` is true, Statement doesn't finish the transition to `Idle` and then start another transition to `Dead`. The in-progress transition changes its target to `Dead`, and the old state's Exit handler isn't run a second time.

The original result records what happened:

```js
_result.WasRedirected();
_result.GetRedirectCount();
_result.GetTargetName();
_result.GetToName();
```

The force setting still comes from the original transition request. Redirecting the destination doesn't silently turn a normal transition into a forced one, or vice versa.

For state-specific redirection, keeping the decision on that state is usually easier to follow. An any-exit redirect is more useful when the same rule genuinely applies across the whole machine.

---

## What if a later hook changes state?

Any-transition and any-enter hooks run after the first transition has already committed. If one of those hooks calls `ChangeState()`, that call starts another transition from the new active state.

For example:

```js
state_machine.AddAnyEnterHook(function(_result) {
	if (_result.GetToName() == "Attack" && stunned) {
		state_machine.ChangeState("Hitstun");
	}
});
```

If this changes `Attack` to `Hitstun`, Statement stops carrying on with the old `Attack` entry sequence. Remaining hooks and `Attack`'s Enter handler don't keep running as though `Attack` were still active.

This is different from an any-exit redirect because the first transition has already committed by the time an any-enter or any-transition hook runs.

---

## Routing a GameMaker event to the active state

Now consider Animation End.

Several states might use animated sprites, but they don't all need the same response:

```text
Attack     -> return to Idle
Reload     -> finish reloading
Idle       -> maybe pause the animation for some period of time
```

You could put a switch on the current state in the object's Animation End Event, but that pulls state-specific behaviour back out of the states.

A `StatementEvent` lets the GameMaker event ask the active Statement state to handle it instead.

Create the event once, usually in the same Create Event where you build the machine:

```js
animation_end_event = new StatementEvent("animation_end");
```

Then give whichever states care about it their own handlers:

```js
var _attack = new StatementState(self, "Attack")
	.AddStateEvent(
		animation_end_event,
		function() {
			state_machine.ChangeState("Idle");
		}
	);
```

In the object's normal GameMaker Animation End Event, send the event through the machine:

```js
state_machine.RunState(animation_end_event);
```

If `Attack` is active, Attack's handler runs. If another active state has a handler for the same event, that state's handler runs instead. A state that hasn't registered that event simply has no state-specific code to run for it.

The GameMaker event stays neat and tidy because the states decide what Animation End means for them and your state code doesn't leak out into the general objects code.

---

## Keep the same `StatementEvent`

This line:

```js
animation_end_event = new StatementEvent("animation_end");
```

creates an event struct.

Statement matches custom events by that struct, not by the text `"animation_end"`. The name is there to make the event recognisable in debugging and tooling.

So create the event once and keep it somewhere both the state setup and the GameMaker event can reach.

This won't match the handler you registered earlier:

```js
// Wrong: this creates a new event struct.
state_machine.RunState(new StatementEvent("animation_end"));
```

Even though the name is identical, it's a different `StatementEvent`.

Use the stored one:

```js
state_machine.RunState(animation_end_event);
```

You also don't need to edit Statement's built-in `eStatementEvents` enum to add project-specific events (this was Statement's behaviour prior to Statement 2). `StatementEvent` exists so your game can define these identities itself in a much nicer and more flexible way.

---

## Passing data with an event

`RunState()` takes an optional payload after the event:

```js
state_machine.RunState(
	damage_event,
	{
		amount: 12,
		source: other
	}
);
```

A custom-event handler can receive both its state and that payload:

```js
var _blocking = new StatementState(self, "Blocking")
	.AddStateEvent(
		damage_event,
		function(_state, _payload) {
			var _reduced_damage = _payload.amount * 0.25;
			hp -= _reduced_damage;
		}
	);
```

The first argument is the `StatementState` whose handler is running, just like the optional `_state` argument in Enter or Update. The second is whatever you passed to `RunState()`.

Another state can interpret the same event differently:

```js
var _idle = new StatementState(self, "Idle")
	.AddStateEvent(
		damage_event,
		function(_state, _payload) {
			hp -= _payload.amount;
			state_machine.ChangeState("Hitstun");
		}
	);
```

The code that sends damage doesn't need to ask which state is active. It sends the event and payload, then the active state handles that event according to its own behaviour.

If the handler doesn't need either argument, `function()` without any arguments is still fine.

---

## Adding more than one handler for an event

`AddStateEvent()` uses the same binding modes as Enter, Update, Exit, and Draw.

A second handler replaces the old one by default:

```js
_attack.AddStateEvent(
	animation_end_event,
	function() {
		state_machine.ChangeState("Idle");
	}
);
```

If both should run, append or prepend the new handler:

```js
_attack.AddStateEvent(
	animation_end_event,
	function() {
		audio_play_sound(snd_attack_finish, 0, false);
	},
	eStatementBindMode.APPEND
);
```

`APPEND` runs the existing handler first. `PREPEND` runs the new handler first.

You can ask whether a state has a handler registered for an event:

```js
if (_attack.HasStateEvent(animation_end_event)) {
	// Attack handles Animation End.
}
```

If one composed handler changes state, Statement stops running the rest of the old state's composed handlers. The machine won't continue executing Attack's event code after Attack has already stopped being active.

---

## Sending events through nested machines

A flat machine only has one active state to consider. A nested machine can have an active path:

```text
Grounded
└── Sprint
```

Calling `RunState()` on the root machine can target the root state, the deepest active state, or every state along that path.

`eStatementEventDispatch` chooses which behaviour you want.

### Current state

`CURRENT` only sends the event to the current state on the machine you called:

```js
state_machine.RunState(
	interaction_event,
	_payload,
	eStatementEventDispatch.CURRENT
);
```

For the root of the example above, `Grounded` receives the event.

`CURRENT` is the default, so these are equivalent:

```js
state_machine.RunState(interaction_event, _payload);
```

```js
state_machine.RunState(
	interaction_event,
	_payload,
	eStatementEventDispatch.CURRENT
);
```

### Deepest active state

`DEEPEST` follows active child machines and sends the event to the deepest active state it finds:

```js
state_machine.RunState(
	interaction_event,
	_payload,
	eStatementEventDispatch.DEEPEST
);
```

For:

```text
Grounded
└── Sprint
```

only `Sprint` receives it.

If `Grounded` has a child machine but that child currently has no active state, then `Grounded` is still the deepest active state. The event stays there rather than starting the child.

### The whole active path

`PATH` sends the event from the current state down through each active child:

```js
state_machine.RunState(
	interaction_event,
	_payload,
	eStatementEventDispatch.PATH
);
```

With the same hierarchy, dispatch runs in this order:

```text
Grounded
    ↓
Sprint
```

Both states can respond to the same event.

If `Grounded`'s handler changes state, Statement stops following the old path. It won't then run `Sprint` as though `Grounded` were still the active parent.

---

## Event dispatch doesn't start child machines

`RunState()` only follows states that are already active.

Suppose `Grounded` hosts a child machine but that child is stopped. Calling:

```js
state_machine.RunState(
	interaction_event,
	_payload,
	eStatementEventDispatch.DEEPEST
);
```

doesn't start the child to make it eligible for the event. `Grounded` remains the deepest active state and receives the dispatch if it has the handler.

Starting and stopping a hosted child still comes from the host state's lifecycle and reset mode, as covered on the submachines page.

---

## Draw already uses path dispatch

You don't run Statement's Draw event with `RunState()` yourself, just like you don't use `RunState()` to run Statement's Update event.

The object's Draw Event calls:

```js
state_machine.Draw();
```

Statement dispatches Draw along the active path. A parent state can draw something shared while its active child draws something more specific.

For:

```text
Grounded
└── Sprint
```

a Draw handler on `Grounded` runs before a Draw handler on `Sprint`.

If none of your states use Draw handlers, you don't need to call `state_machine.Draw()`.

---

## Templates can include custom events

A template can define custom-event handlers just like an ordinary state:

```js
attack_template.AddStateEvent(
	animation_end_event,
	function() {
		state_machine.ChangeState("Idle");
	}
);
```

Every state built from that template gets its own bound copy of the handler for the owner it was built with.

That works well when handling the event is part of the shared behaviour the template represents.

---

## Where each kind of code belongs

When behaviour belongs to one state, keep it on that state:

```js
_attack.AddEnter(...);
_attack.AddUpdate(...);
_attack.AddStateEvent(animation_end_event, ...);
```

When code needs to observe transitions across the machine regardless of which state is involved, use a machine hook:

```js
state_machine.AddAnyTransitionHook(...);
```

And when a normal GameMaker event needs state-specific behaviour, route it through a `StatementEvent` rather than rebuilding a state switch outside the machine.

---

## Next: Statement Lens

Next is [**Statement Lens**](visual_debugger_guide).

The Lens lets you inspect machines while the game is running, follow active states, see recent transition attempts, and manually drive a machine when you're debugging it.
