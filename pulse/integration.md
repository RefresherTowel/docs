---
layout: default
title: Using Pulse with Other Frameworks
parent: Pulse
nav_order: 5
---

# Using Pulse with Other Frameworks

Pulse exists to move information around your project without creating a nest
of direct references.

Combined with the rest of the RefresherTowel frameworks:

- [![Statement icon]({{ '/assets/statement_icon.png' | relative_url }}){: .framework-icon-small } **Statement**](https://refreshertowel.itch.io/statement) decides *what mode* the game is in.
- [![Pulse icon]({{ '/assets/pulse_icon.png' | relative_url }}){: .framework-icon-small } **Pulse**](https://refreshertowel.itch.io/pulse) glues everything together with signals.
- [![Echo icon]({{ '/assets/echo_icon.png' | relative_url }}){: .framework-icon-small } **Echo**](https://refreshertowel.itch.io/echo) explains what actually happened.

This page shows practical patterns for using Pulse alongside the other
frameworks.

---

## How Pulse fits into the toolkit

At a high level:

- Use **Pulse** whenever something in the game should say “this happened” or
  “please do this” without caring *who* handles it.
- Use **Statement** to interpret those signals as state changes.
- Use **Echo** to log signal traffic and hard-to-see behaviour.

---

## Pulse + Statement - signals and states

### Pattern 1 - Signals request state changes (Core)

Let anyone request a state change without needing a direct pointer to the
state machine.

Signal definition:

```js
#macro SIG_ENTER_COMBAT "enter_combat"
```

Subscription (e.g. in the player or a controller):

```js
/// obj_player Create
state_machine = new Statement(self);

PulseSubscribe(id, SIG_ENTER_COMBAT, function(_data) {
    state_machine.ChangeState("Combat");
});
```

Any system can now request combat:

```js
// From an enemy AI, UI button, or Whisper storylet hook
PulseSend(SIG_ENTER_COMBAT, { reason: "ambush" });
```

### Pattern 2 - States broadcast lifecycle signals (Advanced)

Have Statement announce interesting lifecycle events via Pulse.

```js
#macro SIG_STATE_ENTERED "state_entered"

var _idle = new StatementState(self, "Idle")
    .AddEnter(function() {
        PulseSend(SIG_STATE_ENTERED, {
            owner : id,
            state : "Idle"
        });
    });

var _combat = new StatementState(self, "Combat")
    .AddEnter(function() {
        PulseSend(SIG_STATE_ENTERED, {
            owner : id,
            state : "Combat"
        });
    });
```

Elsewhere:

```js
PulseSubscribe(id, SIG_STATE_ENTERED, function(_data) {
    ui_state_label_set(_data.owner, _data.state);
});
```

The UI, audio, and other systems stay decoupled from the state machine.

---

## Pulse + Echo - debugging signal flows

Pulse traffic can be invisible when something goes wrong. Echo makes it
visible again.

### Pattern 1 - Log specific signals (Core)

Subscribe a small debug listener:

```js
PulseSubscribe(id, "stat_changed", function(_data) {
    EchoDebugInfo(
        "stat_changed: " + string(_data.stat_name)
        + " " + string(_data.old_value) + " -> " + string(_data.new_value),
        ["Pulse"]
    );
});
```

You can leave this in your debug builds and disable it in release by
wrapping the subscription in a macro check.

### Pattern 2 - Wrap PulseSend with logging (Advanced)

Create a helper to log calls before dispatching:

```js
function PulseSendLogged(_signal, _data, _from) {
    EchoDebugInfo(
        "PulseSend: " + string(_signal),
        ["Pulse"]
    );

    return PulseSend(_signal, _data, _from);
}
```

Replace calls to `PulseSend` in the systems you are diagnosing. Combined
with Echo's configurable debug level, this gives you a clear picture of
which signals fired and in what order.