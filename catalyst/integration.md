---
layout: default
title: Using Catalyst with Other Frameworks
parent: Catalyst
nav_order: 5
---

# Using Catalyst with Other Frameworks

Catalyst keeps your numbers consistent - stats, modifiers, layers, and
previews.

On its own it is already useful, but it becomes much more powerful when it
works alongside the other frameworks:

- **Statement** - interprets stat values as behavioural states.
- **Whisper** - uses stats as gates or scales narrative outcomes.
- **Pulse** - broadcasts that stats or buffs changed.
- **Echo** - shows how and when stats are evaluated.

This page shows patterns for using Catalyst with the rest of the toolkit.

---

## How Catalyst fits into the toolkit

You can think of the split like this:

- **Catalyst** answers questions like "how much damage?", "do we have enough
  fuel?", "how long does this buff last?".
- **Statement** decides "given these answers, which state are we in?".
- **Whisper** decides "given these answers, which encounter should appear?".
- **Pulse** says "this stat changed" or "this buff started/ended".
- **Echo** tells you what the current stat values and modifier stacks are.

---

## Catalyst + Whisper - stats and story

Whisper cares about "is this storylet allowed?" and "what happens if it
fires?". Catalyst is a natural input and output for both.

### Pattern 1 - Predicates based on stats (Advanced)

Use Catalyst statistics inside Whisper predicates:

```gml
// Storylet that only appears for low morale crews
WhisperStorylet("overworked_crew")
    .TagsSet(["location:bridge"])
    .SetPredicate(function(_ctx) {
        var _morale = _ctx.subject.stats.morale.GetValue();
        return (_morale <= 0.25);
    })
    .TextAdd("Crew voices are tight and clipped; everyone looks exhausted.")
    .AddToPool("bridge_barks");
```

As morale changes, the storylet automatically moves in and out of
eligibility.

### Pattern 2 - Outcomes that scale with stats (Advanced)

In `on_fire`, use Catalyst to scale rewards or penalties:

```gml
WhisperStorylet("find_cache")
    .TagsSet(["location:planet_surface", "outcome:salvage"])
    .SetOnFire(function(_ctx, _s) {
        var _scavenging = _ctx.subject.stats.scavenging;
        var _amount     = _scavenging.GetValue();

        GiveScrap(_amount);
    })
    .TextAdd("You stumble across a half-buried supply cache.")
    .AddToPool("surface_events");
```

You can also use Catalyst previews when deciding whether to *offer* a risky
encounter in the first place.

---

## Catalyst + Statement - behaviour from numbers

Statement turns numeric conditions into discrete behaviours.

### Pattern 3 - Using stats for state changes (Core)

Use Catalyst values directly in state transitions:

```gml
/// obj_enemy Create
stats = {
    hp : new CatalystStatistic(30).SetName("HP")
};

state_machine = new Statement(self);

var _alive = new StatementState(self, "Alive")
    .AddUpdate(function() {
        if (stats.hp.GetValue() <= 0) {
            state_machine.ChangeState("Dead");
        }
    });

var _dead = new StatementState(self, "Dead")
    .AddEnter(function() {
        sprite_index = spr_enemy_dead;
        hspeed = vspeed = 0;
    });

state_machine.AddState(_alive);
state_machine.AddState(_dead);
state_machine.ChangeState("Alive");
```

The stat holds the numeric truth, Statement decides what that means.

### Pattern 4 - Ability windows and resource checks (Advanced)

Use Catalyst layers and durations inside states that represent temporary
modes, like "Overcharge" or "Guard Break".

```gml
/// obj_player Create
stats = {
    stamina : new CatalystStatistic(100).SetName("Stamina"),
    damage  : new CatalystStatistic(10).SetName("Damage")
};

state_machine = new Statement(self);

var _overcharge = new StatementState(self, "Overcharge")
    .AddEnter(function() {
        // Pay stamina cost before entering the state
        stats.stamina.ChangeBaseValue(-25);

        // Apply damage buff with duration
        var _buff = new CatalystModifier(0.4, eCatMathOps.MULTIPLY, 5)
            .SetLayer(eCatStatLayer.TEMP)
            .SetSourceLabel("Overcharge");
        stats.damage.AddModifier(_buff);
    })
    .AddUpdate(function() {
        // Leave the state once the buff expires
        if (array_length(stats.damage.FindModifiersBySourceLabel("Overcharge")) == 0) {
            state_machine.ChangeState("Normal");
        }
    });

var _normal = new StatementState(self, "Normal");

state_machine.AddState(_normal);
state_machine.AddState(_overcharge);
state_machine.ChangeState("Normal");
```

A separate controller drives `CatalystModCountdown()` each step. Catalyst
tracks timing, Statement handles the behaviour.

---

## Catalyst + Pulse - announcements and UI

Catalyst works well with Pulse when you want other systems to react to stat
changes or buff lifecycles.

### Pattern 5 - Announce stat changes (Core)

Wrap stat adjustments in helpers that send signals:

```gml
function ActorApplyDamage(_actor, _amount) {
    var _old_hp = _actor.stats.hp.GetValue();

    var _mod = new CatalystModifier(-_amount, eCatMathOps.ADD)
        .SetSourceLabel("Damage");
    _actor.stats.hp.AddModifier(_mod);

    var _new_hp = _actor.stats.hp.GetValue();

    PulseSend("stat_changed", {
        actor     : _actor,
        stat_name : "hp",
        old_value : _old_hp,
        new_value : _new_hp
    });
}
```

UI or gameplay systems subscribe:

```gml
PulseSubscribe(id, "stat_changed", function(_data) {
    if (_data.stat_name == "hp") {
        ui_hp_bar_set(_data.actor, _data.new_value);
    }
});
```

### Pattern 6 - Buff applied / expired events (Advanced)

When you apply a buff, send a signal. When it expires (as determined by
`CatalystModCountdown`), send another.

```gml
function ApplyShieldBuff(_actor) {
    var _mod = new CatalystModifier(15, eCatMathOps.ADD)
        .SetLayer(eCatStatLayer.TEMP)
        .SetDuration(3)
        .SetSourceLabel("ShieldBuff");

    _actor.stats.shield.AddModifier(_mod);
    _mod.ApplyDuration();

    PulseSend("buff_applied", {
        actor : _actor,
        name  : "ShieldBuff"
    });
}
```

In the controller that drives the countdown, you can compare which modifiers
were active before and after each tick and emit `buff_expired` signals when
they vanish. This keeps the UI and audio layers in sync with Catalyst.

---

## Catalyst + Echo - visibility into stats

Echo is your friend when you are not sure why a stat ended up with a
particular value.

### Pattern 7 - Log stat snapshots (Core)

When debugging, log stat values at interesting times:

```gml
EchoDebugInfo(
    "Player stats - hp=" + string(stats.hp.GetValue())
    + ", damage=" + string(stats.damage.GetValue()),
    ["Catalyst"]
);
```

### Pattern 8 - Dump modifiers for a stat (Advanced)

Write a small helper to describe modifiers:

```gml
function CatDebugDescribeStat(_name, _stat) {
    EchoDebugInfo("Stat: " + _name
        + " base=" + string(_stat.base_value)
        + " value=" + string(_stat.GetValuePreview()),
        ["Catalyst"]);

    var _mods = _stat.modifiers;
    for (var i = 0; i < array_length(_mods); i++) {
        var _m = _mods[i];
        EchoDebugInfo(
            " - " + _m.source_label
            + " layer=" + string(_m.layer)
            + " op=" + string(_m.operation)
            + " value=" + string(_m.value)
            + " duration=" + string(_m.duration),
            ["Catalyst"]
        );
    }
}
```

Call this when something looks wrong to get a readable dump of what is
affecting a given stat.

---

You do not need to wire every system to Catalyst on day one. Start by using
stats in one place - a Whisper predicate, a Statement transition, or a Pulse
signal - and grow from there.
