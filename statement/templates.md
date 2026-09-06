---
layout: default
title: State Templates
parent: Statement
nav_order: 9
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# State Templates

Suppose a player has three attack states:

```text
LightAttack
HeavyAttack
ChargedAttack
```

They aren't identical, but their lifecycle is mostly the same. Each attack needs to choose its own animation and damage, run for its own duration, then return to Idle.

Writing three separate states works, but most of the code would be copies with a few numbers and sprites changed.

A `StatementStateTemplate` lets you store and reuse that shared state setup. You give it a different config when you build from it, and it produces ordinary `StatementState` structs that you can add to your state machine.

The template is never active in a machine itself. It's the thing that **builds** the real states.

---

## A first attack template

Start with the values that are different for one attack:

```js
{
	sprite: spr_attack_light,
	damage: 4,
	duration: 10
}
```

We'll store that struct as the built state's config, then let the shared handlers read it.

```js
attack_template = new StatementStateTemplate("Attack")
	.AddEnter(function(_state) {
		var _config = _state.GetConfig();

		sprite_index = _config.sprite;
		image_index = 0;
		attack_damage = _config.damage;
		_state.TimerStart();
	})
	.AddTransition(
		new StatementTransitionRule("Idle", function(_state) {
			var _config = _state.GetConfig();
			return _state.TimerGet() >= _config.duration;
		})
	);
```

There is no `LightAttack` or `HeavyAttack` in this code. The template only describes the behaviour they share:

```text
Enter
    use this state's configured sprite and damage
    start this state's timer

While active
    return to Idle when this state's configured duration is reached
```

Now build two actual states from it:

```js
var _light_attack = attack_template.Build(
	self,
	{
		sprite: spr_attack_light,
		damage: 4,
		duration: 10
	},
	"LightAttack"
);

var _heavy_attack = attack_template.Build(
	self,
	{
		sprite: spr_attack_heavy,
		damage: 9,
		duration: 18
	},
	"HeavyAttack"
);
```

`Build()` returns a `StatementState`. Register those states normally:

```js
state_machine
	.AddState(_light_attack)
	.AddState(_heavy_attack);
```

Once they're registered, the machine treats them like states you wrote by hand:

```js
state_machine.ChangeState("LightAttack");
state_machine.ChangeState("HeavyAttack");
```

The template isn't involved at runtime every time the state updates. It's job is simply to build the state.

---

## The owner is supplied when you build

Notice that the template constructor only needed a name:

```js
new StatementStateTemplate("Attack")
```

A normal state needs an owner:

```js
new StatementState(self, "Attack")
```

The template doesn't have that owner yet because it may be used to build states for different instances or structs. `Build()` supplies the owner for the particular state being created:

```js
attack_template.Build(self, _config, "LightAttack");
```

The handlers stored by the template are bound to that owner when the state is built. Inside a built attack, ordinary instance variables such as `sprite_index` and `attack_damage` therefore refer to the owner of that built state.

---

## Config belongs to the built state

The second `Build()` argument becomes the new state's config:

```js
var _light = attack_template.Build(
	self,
	light_attack_config,
	"LightAttack"
);
```

Inside that state:

```js
var _config = _state.GetConfig();
```

returns the config supplied for LightAttack.

You can also set config directly on a state:

```js
var _attack = attack_template.Build(
	self,
	undefined,
	"LightAttack"
);

_attack.SetConfig({
	sprite: spr_attack_light,
	damage: 4,
	duration: 10
});
```

Passing it through `Build()` is usually easier to read because the values that make the new state different sit beside the state name they're configuring. But you may dynamically want to change the config at some point (perhaps the light attack gets a damage upgrade or something like that).

Config can be any value your state understands. A struct is commonly used because it allows you to store several related values with readable names.

---

## Config is cloned by default

Built states clone the supplied config unless you tell them not to.

```js
var _light_config = {
	damage: 4,
	tags: ["melee", "quick"]
};

var _light = attack_template.Build(
	self,
	_light_config,
	"LightAttack"
);
```

The state stores its own cloned config rather than the original `_light_config` reference. If code later changes the state's stored `tags` array, it doesn't mutate the `_light_config` struct that was passed into `Build()`, and vice versa, mutating `_light_config` won't automatically update the struct data stored in the `_light` state.

This stops two separately built states from accidentally sharing mutable config just because they were given the same source value.

When shared config is deliberate, disable cloning for the template:

```js
attack_template.SetConfigClone(false);
```

Every later build uses that setting unless the individual call overrides it.

For one state only:

```js
var _attack = attack_template.Build(
	self,
	shared_attack_config,
	"SharedAttack",
	false
);
```

The fourth argument is the clone override for that build.

Leave cloning on when config is meant to be the built state's own data. Turn it off when several states are intentionally looking at the same live config value, and changing the config value will ripple through **all** the states.

---

## `Build()` creates the state but doesn't register it

This:

```js
var _light_attack = attack_template.Build(
	self,
	light_attack_config,
	"LightAttack"
);
```

only constructs the new state. The machine doesn't know about it until you add it like any other normal state:

```js
state_machine.AddState(_light_attack);
```

So make sure you add the states built from a template to the state machine.

---

## Building and registering in one call

If you don't need to touch the state between construction and registration, the machine can do both:

```js
state_machine.AddStateTemplate(
	attack_template,
	{
		sprite: spr_attack_light,
		damage: 4,
		duration: 10
	},
	"LightAttack"
);
```

That's the shorter form of:

```js
var _light_attack = attack_template.Build(
	self,
	light_attack_config,
	"LightAttack"
);

state_machine.AddState(_light_attack);
```

Several templated states can be added in one chain:

```js
state_machine
	.AddStateTemplate(
		attack_template,
		light_attack_config,
		"LightAttack"
	)
	.AddStateTemplate(
		attack_template,
		heavy_attack_config,
		"HeavyAttack"
	)
	.AddStateTemplate(
		attack_template,
		charged_attack_config,
		"ChargedAttack"
	);
```

`AddStateTemplate()` returns the machine, not the newly built state. Use `Build()` when you need a reference to the state before or after registration.

`AddStateTemplate()` also accepts the optional fourth clone override if one registered build needs different config-sharing behaviour.

---

## The template name is also the default state name

This template:

```js
attack_template = new StatementStateTemplate("Attack");
```

uses `"Attack"` as its template identity and as the default name for states built without an override.

```js
var _attack = attack_template.Build(self, attack_config);
```

creates a state named `"Attack"`.

Supplying a name replaces that default for this build:

```js
var _light = attack_template.Build(
	self,
	light_attack_config,
	"LightAttack"
);
```

The original value is preserved as the state's template name for debug information, while `"LightAttack"` becomes the actual state name used by the machine.

State names don't have to be strings, so enum-based machines can override the name with an enum value:

```js
var _light = attack_template.Build(
	self,
	light_attack_config,
	ePlayerState.LIGHT_ATTACK
);
```

---

## Templates use the same handler bind modes

A template can compose several handlers of the same type just like an ordinary state.

```js
attack_template
	.AddEnter(function() {
		image_index = 0;
	})
	.AddEnter(
		function(_state) {
			_state.TimerStart();
		},
		eStatementBindMode.APPEND
	);
```

The second call explicitly uses `APPEND`, so the template retains both Enter handlers in that order.

`PREPEND` puts the new handler before the existing one:

```js
attack_template.AddEnter(
	function() {
		attack_target = noone;
	},
	eStatementBindMode.PREPEND
);
```

Without a bind mode, `REPLACE` is the default and the new handler replaces whatever the template previously stored for that event.

The same rules apply to Update, Exit, Draw, and custom state events.

You can **also** do the same thing to the states you build from a template. So if you have build three states from a template, and one of them needs some custom code to run in the Enter handler, you can simple append/prepend it:

```js
var _light = attack_template.Build(
	self,
	light_attack_config,
	ePlayerState.LIGHT_ATTACK
);
_light.AddEnter(
	function() {
		// Only light state gets this extra code that runs
	},
	eStatementBindMode.PREPEND
)
```

Now your light attack will run some additional code when it's entered that the heavy and charged attacks won't, even though they are all built from the same template.

This is extremely useful for templates, as it allows us to both have a default set behaviour, while still being able to add to or replace it, making templates an extremely flexible way to build out many similar states even if they have varied behaviour.

---

## Each built state gets its own transition rules

Templates can contain automatic transition rules:

```js
attack_template.AddTransition(
	new StatementTransitionRule("Idle", function(_state) {
		return _state.TimerGet() >= _state.GetConfig().duration;
	})
);
```

When `Build()` creates a state, Statement clones each template rule and attaches the clone to that new state.

So LightAttack and HeavyAttack don't share one live `StatementTransitionRule` object:

```text
template Idle rule
    ↓ build LightAttack
LightAttack gets its own copy

template Idle rule
    ↓ build HeavyAttack
HeavyAttack gets a different copy
```

A transition rule can be enabled, disabled, reprioritised, or removed after it's been attached, so changing LightAttack's copy mustn't mutate HeavyAttack or the template.

You can also add extra rules to one built state:

```js
var _charged = attack_template.Build(
	self,
	charged_attack_config,
	"ChargedAttack"
);

_charged.AddTransition(
	new StatementTransitionRule("Overheated", function() {
		return heat >= max_heat;
	})
	.SetPriority(20)
);

state_machine.AddState(_charged);
```

Only ChargedAttack receives the new Overheated rule.

---

## Custom events can be part of a template

A custom Statement event can be stored on the template too:

```js
attack_template.AddStateEvent(
	animation_end_event,
	function() {
		state_machine.ChangeState("Idle");
	}
);
```

Every state built after that point receives the handler as part of its state definition.

This works the same way as templated Enter, Update, Exit, and Draw handlers. The next page covers how `StatementEvent` objects are created and run.

---

## Putting it together

Here's the attack template as one complete setup.

```js
state_machine = new Statement(self);

var _idle = new StatementState(self, "Idle")
	.AddEnter(function() {
		sprite_index = spr_player_idle;
	});

attack_template = new StatementStateTemplate("Attack")
	.AddEnter(function(_state) {
		var _config = _state.GetConfig();

		sprite_index = _config.sprite;
		image_index = 0;
		attack_damage = _config.damage;
		_state.TimerStart();
	})
	.AddExit(function() {
		attack_damage = 0;
	})
	.AddTransition(
		new StatementTransitionRule("Idle", function(_state) {
			var _config = _state.GetConfig();
			return _state.TimerGet() >= _config.duration;
		})
	);

state_machine
	.AddState(_idle)
	.AddStateTemplate(
		attack_template,
		{
			sprite: spr_attack_light,
			damage: 4,
			duration: 10
		},
		"LightAttack"
	)
	.AddStateTemplate(
		attack_template,
		{
			sprite: spr_attack_heavy,
			damage: 9,
			duration: 18
		},
		"HeavyAttack"
	)
	.Start();
```

The Step Event stays exactly the same:

```js
state_machine.Update();
```

and input refers to the built states by their real names:

```js
if (keyboard_check_pressed(ord("Z"))) {
	state_machine.ChangeState("LightAttack");
}

if (keyboard_check_pressed(ord("X"))) {
	state_machine.ChangeState("HeavyAttack");
}
```

By the time the machine is running, LightAttack and HeavyAttack are just two normal `StatementState` structs with copied handlers, their own config, and their own transition rules.

---

## When a template is worth making

Templates work best when several states are similar and mostly differ in authored data or have a backbone of shared behaviours.

Attacks with different damage and durations are a natural fit. So are several sizes of hitstun where the same lifecycle uses different timing or knockback config.

Sharing one small line of code isn't enough by itself. If unrelated states all play a sound on Enter, a helper function or appended handler may be easier to understand than turning those states into one template family.

A useful question is whether changing the behaviour of this **kind of state** should normally change all of the states built from it. If the answer is yes, the template gives that shared behaviour one definition while the config keeps the individual states distinct.

Next: [**Hooks & Custom Events**](hooks_and_custom_events)
