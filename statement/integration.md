---
layout: default
title: Using Statement with Other Frameworks
parent: Statement
nav_order: 4
---

# Using Statement with Other Frameworks

Statement works best when it is not doing everything by itself.

It is happiest when:

- [![Statement icon]({{ '/assets/statement_icon.png' | relative_url }}){: .framework-icon-small } **Statement**](https://refreshertowel.itch.io/statement) owns the flow of behaviour and modes.
- [![Pulse icon]({{ '/assets/pulse_icon.png' | relative_url }}){: .framework-icon-small } **Pulse**](https://refreshertowel.itch.io/pulse) moves information around without tight coupling.
- [![Echo icon]({{ '/assets/echo_icon.png' | relative_url }}){: .framework-icon-small } **Echo**](https://refreshertowel.itch.io/echo) keeps you honest by logging what actually happened.

This page shows practical ways to connect Statement to the rest of the
RefresherTowel frameworks.

---

## How Statement fits into the toolkit

A high level view:

- **Statement** - drives *when* things happen and *what mode* the game is in.
- **Pulse** - passes around “this happened” signals without hard references.
- **Echo** - explains what the machine actually did and why.

In practice you will usually:

1. Use Statement to decide *when* to ask Whisper for encounters.
2. Use Pulse to trigger state changes or broadcast that states changed.
3. Use Echo to debug state transitions and odd behaviours.

---

## Statement + Pulse - signals describe flow

Pulse is a natural partner for Statement whenever you want other systems to
request or react to state changes.

### Pattern 3 - Signals trigger state changes (Core)

Use Pulse to ask a state machine to move into a state, without calling it
directly.

Define a signal id in a shared script:

```js
#macro SIG_ENTER_COMBAT "enter_combat"
```

In a controller or in the object that owns the machine:

```js
/// obj_player Create
state_machine = new Statement(self);

PulseSubscribe(id, SIG_ENTER_COMBAT, method(self, function(_data) {
	state_machine.ChangeState("Combat", _data);
}));
```

`PulseSubscribe` callbacks are not auto-bound, so `method(self, ...)` keeps the handler scoped to the owning instance.

Elsewhere in the game:

```js
// A Whisper encounter, an AI controller, or UI element can do:
PulseSend(SIG_ENTER_COMBAT, { reason: "ambush" });
```

Now anything that knows the signal id can trigger the state change without
needing to know where the machine lives.

### Pattern 4 - States broadcast signals (Advanced)

You can also emit signals *from* state handlers so other systems can react
without being tightly coupled to the machine.

For example, broadcasting an event whenever a new state is entered:

```js
#macro SIG_STATE_CHANGED "state_changed"

/// obj_player Create
state_machine = new Statement(self);

var _idle = new StatementState(self, "Idle")
	.AddEnter(function() {
		PulseSend(SIG_STATE_CHANGED, {
			owner          : id,
			new_state_name : "Idle"
		});
	});

var _combat = new StatementState(self, "Combat")
	.AddEnter(function() {
		PulseSend(SIG_STATE_CHANGED, {
			owner          : id,
			new_state_name : "Combat"
		});
	});

state_machine.AddState(_idle);
state_machine.AddState(_combat);
```

Some other system can subscribe to `SIG_STATE_CHANGED` to update UI, music,
or AI hints without needing a direct reference to the player object.

---

## Statement + Echo - debugging state flows

Echo is extremely useful when you are not sure why a machine is stuck,
oscillating, or skipping states.

### Pattern 7 - Log transitions (Core)

Wrap `ChangeState` or add logging inside your handlers:

```js
state_machine.ChangeState("Hitstun");
EchoDebugInfo("State change -> Hitstun");
```

Or build it into a helper:

```js
function StateChangeLogged(_sm, _name) {
	EchoDebugInfo("State change -> " + _name, ["Statement"]);
	_sm.ChangeState(_name);
}
```

Then call `StateChangeLogged(state_machine, "Hitstun");` instead of
`ChangeState` directly.

### Pattern 8 - Trace behaviour from handlers (Advanced)

Use `EchoDebugInfo` inside `AddEnter` and `AddUpdate` callbacks:

```js
var _combat = new StatementState(self, "Combat")
	.AddEnter(function() {
		EchoDebugInfo("Entered Combat", ["Statement"]);
	})
	.AddUpdate(function() {
		EchoDebugInfo("Combat.Update - hp=" + string(stats.hp.GetValue()), ["Statement"]);
		// combat logic here
	});
```

Combined with `EchoDebugSetLevel(__ECHO_eDebugLevel.COMPLETE);` in your
debug builds, this gives you a clear picture of how each state behaves
over time.

---

You do not have to adopt all of these patterns at once. Start with a single
integration (for example Statement + Whisper or Statement + Pulse) and add
more connections as your project grows.
