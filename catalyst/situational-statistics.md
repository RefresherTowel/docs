---
layout: default
title: Situational Statistics
parent: Catalyst
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

# Situational Statistics

Statistics and Resources can already respond to explicit gameplay changes: A sword adds damage because its Modifier is attached, while an HP Resource drops because an attack calls `Decrease()`.

However, plenty of game rules depend on the current situation rather than on something being directly added or removed. A weapon might deal more damage only when its target is frozen, armour might increase while the player's HP is low, or a bonus might become stronger as a target builds up stacks of some status.

In each case we still want to use Modifiers on a Statistic. The difference is that the Modifier needs to look at what is true in the game right now before deciding whether, or how strongly, it should apply.

Catalyst handles that through Oracle. The game stores facts that Catalyst might want to know in Oracle, a Statistic gets a view of the facts that matter to it, and Catalyst checks that view whenever the Statistic needs to be recalculated.

Let's build that up from a simple example.

---

## A bonus that only applies sometimes

Suppose the player normally deals 10 damage, but a Frostbreaker weapon deals 25% more damage to frozen targets.

The weapon is still equipped whether the current enemy is frozen or not, so we don't want to add and remove its Modifier every time the player changes targets. Instead, we want the Modifier to stay attached and ask one question whenever damage is calculated: **is the current target frozen?**

Start with the Statistic and Modifier we've already been using:

```js
damage = new CatalystStatistic(10);
frozen_bonus = new CatalystModifier(0.25, eCatMathOps.MULTIPLY);
```

At the moment, `frozen_bonus` would always apply. Before we make it conditional, though, we need somewhere for the answer to that question to come from.

The target already knows whether it is frozen, so that information should live with the target rather than being worked out again by every Statistic that cares about it.

---

## Letting an enemy describe its current state

Oracle stores related pieces of game state in `OracleFacts`. Oracle calls one of these objects a **fact scope**.

For example, an enemy could create a fact scope alongside the rest of its state, and publish it's `frozen` statistic as a fact:

```js
// obj_enemy Create event

frozen = new CatalystStatistic(0);

facts = new OracleFacts();

frozen.PublishToFact(
	facts,
	"frozen",
	function(_stat) {
		return _stat.GetValue() > 0;
	}
);
```

We've introduced several new concepts here, so let's slow down and take a look at them. The enemy has a variable called `facts` which starts off as an empty set of Oracle Facts about this particular enemy instance. We can add or remove various facts that we care about from this Fact set.

Statistics have the method `PublishToFact()`, which takes the set of Oracle Facts we care about (the enemies `facts` here), the name of the variable we want to publish as a string (since we care about `frozen`, we have it `"frozen"`), and then a function you create that returns whatever value you want Oracle to receive (in this case a boolean true/false value for whether the target is frozen or not).

In this circumstance, the function will automatically get handed the `frozen` stat that we are publishing to Oracle as it's first argument, so you can read the value of the stat and decide how you want Oracle to view the stat. We will make it so that if `frozen` has any value above `0`, the enemy is considered to be frozen, otherwise it's not, so we simply return `_stat.GetValue() > 0` (which returns `true` if it is above `0` or `false` if it's not).

Those facts describe this particular enemy instance. Another enemy instance has its own `OracleFacts`, so it can have completely different values for the same names.

Whenever something in the game freezes the enemy, we just add a timed (or permanent if the frozen state doesn't have a duration) Modifier to the `freeze` Statistic:

```js
// When the enemy gets hit by a freezing spell
frozen.AddModifier(
    new CatalystModifier(1, eCatMathOps.ADD, game_get_speed(gamespeed_fps) * 5)
);
```

That modifier adds 1 to frozen for 5 seconds (using default timing), and the Oracle fact would automatically update alongside it.

Two useful things have happened so far. We now have a way of an enemy knowing it is frozen (if `frozen.GetValue() > 0`), so we can make the enemies actions stop. If you're using [Statement]({{ '/statement/' | relative_url }}) you could change the state of the enemy to a frozen state, for example. And we have an Oracle fact that stays in sync with the enemies frozen state, which we can then read in our damage calculation to know if we should apply the Frostbreaker modifier.


The same idea applies to the other values, if they are just plain values, we keep them updated manually:

```js
facts.Set("is_boss", true);
```

Or if they are Catalyst Statistics, we can bind them to Oracle automatically as we just did for `frozen`.

At this point Oracle knows what is true about the enemy, but our damage Statistic still needs to know **which** enemy it should be looking at.

---

## Building a view of the current situation

A Statistic doesn't normally need access to every fact in the game. Player damage might care about the player who is attacking and the enemy currently being targeted, while a building's production speed might care about the building and the city around it.

An `OracleFactView` describes which fact scopes should be visible from one particular point of view.

Suppose the player's Create event already has a fact scope for information about the player:

```js
// obj_player Create event
facts = new OracleFacts();
target = noone;
```

We can create a Fact View for the player's combat Statistics and add those player facts to it:

```js
combat_fact_view = new OracleFactView()
    .AddTo("player", facts);
```

`AddTo()` gives the scope a name inside the view. Here, anything stored in the player's `facts` scope can be read through the name `"player"`.

The name becomes useful as soon as another object enters the situation. When the player selects an enemy as their target, the targeting code can place that enemy's fact scope under a separate `"target"` name. Here, `_enemy` is simply the enemy instance selected by your own targeting code:

```js
target = _enemy_id;
combat_fact_view
    .ClearFrom("target")
    .AddTo("target", target.facts);
```

`ClearFrom("target")` removes whatever target scope the view was using before, then `AddTo("target", target.facts)` makes the newly selected enemy visible as the current target.

Nothing has been copied out of the enemy. The view is looking at the enemy's actual `OracleFacts`, so later changes made with `target.facts.Set(...)` are still changes to the same scope the view can see.

We can now give that view to the damage Statistic:

```js
damage.SetFactView(combat_fact_view);
```

The Statistic now has a current situation consisting of two separately named parts:

```text
player -> the player's facts
target -> the current enemy's facts
```

For this example each name contains one fact scope. Oracle can combine several scopes under the same name as well, but we don't need that yet. And, more importantly, you do not have to keep updating the damages fact view. Once you have set it once, damage will continue to read that fact view automatically whenever you call `GetValue()` on it.

## Making the Modifier ask about the target

Now that `damage` can see the current target's facts, we can make Frostbreaker conditional.

Call `SetCondition()` and give the Modifier a function that answers whether it should apply:

```js
frozen_bonus.SetCondition(function(_stat, _facts) {
    return _facts.GetFrom("target", "frozen") ?? false;
});
```

Then attach the Modifier as usual:

```js
damage.AddModifier(frozen_bonus);
```

There are two callback arguments worth unpacking here from the function we supply to `SetCondition()`. Both of these arguments get supplied to the callback function you create when Catalyst runs it, so all you have to do is name them what you want and then you can use them if you need access to that data. In this example we have named them `_stat` and `_facts`.

`_stat` is the `CatalystStatistic` currently being calculated. We don't need it for Frostbreaker, but it's available when a rule needs to inspect the Statistic itself.

`_facts` contains the facts Catalyst resolved from the Statistic's Fact View for this calculation. Rather than being one large flat collection, our view has named parts, so `GetFrom()` lets us say exactly where a fact should come from:

```js
_facts.GetFrom("target", "frozen")
```

The first argument chooses the `"target"` part of the view, we often call this the "named chain" of the `OracleFacts`. The second asks for the `"frozen"` fact inside it.

If there is no current target, or the target doesn't contain a fact called `"frozen"`, `GetFrom()` returns `undefined`. The `?? false` gives us a sensible fallback, so a missing answer is treated as "not frozen" rather than allowing the Modifier to apply.

> `??` is a special operator in GM called the "nullish coalescing operator" ([read about it in the GM manual](https://manual.gamemaker.io/lts/en/GameMaker_Language/GML_Overview/Expressions_And_Operators.htm)). It means "use the value on the left unless that value is `undefined`; otherwise use the value on the right." For example, `var _value = my_variable ?? 0;` gives `_value` the contents of `my_variable` when it has a value, or `0` when `my_variable` is `undefined`. So the overall code in our `SetCondition()` function is exactly equivalent to:
> ```js
> var _frozen = _facts.GetFrom("target", "frozen"); // _frozen ends up holding either true, false or undefined
> if (_frozen == undefined) {
>    _frozen = false;
> }
> return _frozen;
> ```
{: .note}

The condition function must return a boolean answer. If it returns `true`, Catalyst continues evaluating the Modifier normally. If it returns `false`, Catalyst skips that Modifier for this calculation.

Nothing special happens when the Modifier is attached. It remains on `damage` just like the Modifiers from the Statistics & Modifiers guide. The only difference is that Catalyst now checks its condition before deciding whether the Modifier contributes anything.

---

## The Statistic follows the live facts automatically

Suppose the current target starts out unfrozen:

```js
var _damage = damage.GetValue(); // 10
```

When `GetValue()` calculates the Statistic, Frostbreaker's condition reads `"frozen"` from the `"target"` part of the view. The fact is `false`, so the condition fails and the Modifier is skipped.

Now something freezes that same enemy:

```js
target.frozen.AddModifier(
    new CatalystModifier(1, eCatMathOps.ADD, game_get_speed(gamespeed_fps) * 5)
);

var _damage = damage.GetValue(); // 12.5
```

This time the same Modifier applies and the 10 damage is multiplied by 1.25.

The important part is what we **didn't** have to do. The code that froze the enemy didn't call anything on `damage`, and it didn't add Frostbreaker again. It only changed the enemy's own fact.

Behind the scenes, the sequence is effectively:

```text
target.facts.Set("frozen", true)
    ↓
the target's OracleFacts records that it changed
    ↓
damage.GetValue() sees that its Fact View is no longer current
    ↓
Catalyst recalculates damage
    ↓
Frostbreaker's condition reads target.frozen = true
    ↓
Frostbreaker applies
    ↓
10 × 1.25 = 12.5
```

`GetValue()` still behaves like the normal way to read a Statistic. The automatic part is that Catalyst knows when the facts behind that value have changed and recalculates before returning it.

---

## Changing targets changes the situation too

The target doesn't have to change internally for the answer to become different. The player might simply select another enemy.

Wherever your targeting code changes `target`, update the `"target"` part of the view at the same time:

```js
// When we hit an enemy

if (target != _current_enemy_id) {
    target = _current_enemy_id;
    combat_fact_view
        .ClearFrom("target")
        .AddTo("target", target.facts);
}

// Now we continue with the rest of damage code
var _damage = damage.GetValue();
target.hp -= _damage;
```

When we hit an enemy that is different from the existing target all we do is run `ClearFrom("target")` on the `combat_fact_view` to clear out the old enemies facts, and add the new enemies facts with `AddTo("target", target.facts)`.

If the previous enemy was frozen and the new enemy isn't, the next call to:

```js
var _damage = damage.GetValue();
```

returns `10` again.

Catalyst notices both kinds of change:

- a fact inside one of the visible scopes changed, such as the current enemy becoming frozen;
- the Fact View itself changed, such as replacing one target scope with another.

If the player stops targeting anything, clear that part of the view and leave it empty:

```js
target = noone;
combat_fact_view.ClearFrom("target");
```

A later `GetFrom("target", ...)` then returns `undefined`, so the fallbacks in our conditions handle the missing target normally.

This is why we don't need to package up `target_frozen`, `target_is_boss`, and every other relevant value each time damage is requested. The targeting system changes which enemy is the target, the enemy owns its own facts, and the Statistic keeps reading the situation through the same Fact View.

You can also give the same `combat_fact_view` to other player Statistics that care about the same player and target. They each choose which facts matter through their own conditions, stack functions, or other fact-aware callbacks.

---

## Conditions can use facts from different parts of the view

Named parts become especially useful when one rule depends on more than one thing.

Suppose a Last Stand bonus increases damage by 50%, but only when the player is below 30% health **and** the current target is a boss.

The boss part already belongs to the target:

```js
// On a boss enemy
facts.Set("is_boss", true);
```

The health part belongs to the player. We could manually calculate a `health_fraction` fact every time HP changes, but the player already has a Catalyst Resource that owns that state, so Catalyst can publish the value for us.

---

## Publishing Resource state into the player's facts

Suppose the player has the HP Resource from the previous guide:

```js
hp = new CatalystResource(100);
```

The player's `facts` scope is already visible through the `"player"` part of `combat_fact_view`, so publish the HP fraction into that existing scope:

```js
health_fact_binding = hp.PublishToFact(
    facts,
    "health_fraction",
    function(_resource) {
        return _resource.GetFraction();
    }
);
```

`PublishToFact()` writes the fact immediately, then automatically keeps it updated when the Resource changes. Because our transform returns `GetFraction()`, the published value is the player's current HP as a fraction from `0` to `1` rather than the raw HP amount.

At full health, the player's facts now contain:

```text
player.health_fraction = 1
```

If the player takes 80 damage:

```js
hp.Decrease(80);
```

then the Resource republishes the fact as:

```text
player.health_fraction = 0.20
```

The code dealing damage only changes HP. It doesn't also need to know that some damage Modifier happens to care about low health.

`PublishToFact()` returns a `CatalystFactBinding`, which is Catalyst's handle for that ongoing connection. Most of the time you can leave it alone. If something changes outside the normal Resource notifications and you need to publish the current value again immediately, call:

```js
health_fact_binding.Sync();
```

When the connection itself should end, unbind it instead:

```js
health_fact_binding.Unbind();
```

`Sync()` republishes the current value and keeps the binding active. `Unbind()` stops future updates without deleting the fact already stored in Oracle. As you can see both Resources and Statistics have the same `PublishToFact()` helper when the ongoing fact you want to publish comes from a Catalyst Resource or Statistic.

---

## Asking one condition about both player and target

Now we can write Last Stand without either side needing to know about the other.

First create the Modifier:

```js
last_stand = new CatalystModifier(0.50, eCatMathOps.MULTIPLY)
    .SetCondition(function(_stat, _facts) {
        var _health_fraction = _facts.GetFrom("player", "health_fraction") ?? 1;
        var _target_is_boss = _facts.GetFrom("target", "is_boss") ?? false;

        return _health_fraction < 0.30 && _target_is_boss;
    });

damage.AddModifier(last_stand);
```

`SetCondition()` still gives Catalyst one function that must return `true` or `false`. The difference is that the answer now comes from two separately owned pieces of state.

This line:

```js
var _health_fraction = _facts.GetFrom("player", "health_fraction") ?? 1;
```

reads the player's current health. A missing value falls back to `1`, meaning full health.

This line:

```js
var _target_is_boss = _facts.GetFrom("target", "is_boss") ?? false;
```

reads the current target's boss flag. If there is no target, or the target doesn't provide that fact, it falls back to `false`.

The final line combines the two checks:

```js
return _health_fraction < 0.30 && _target_is_boss;
```

If the player is at 20% health but the target isn't a boss, Last Stand doesn't apply. If the target is a boss but the player is at full health, it still doesn't apply. Only when both parts of the current situation are true does the 50% Modifier contribute.

No system had to assemble a special "Last Stand situation" for this calculation. HP publishes the player's health because HP owns that state, the enemy stores whether it is a boss because the enemy owns that state, and the Fact View brings those two sources together for Statistics that need to ask questions about the fight.

---

## Letting a fact decide the number of stacks

Conditions answer an on/off question: does this Modifier apply or not?

Sometimes the situation should instead decide **how many times** a Modifier applies.

Suppose another attack gains `+2` damage for every Chill stack already on the current target, up to five stacks (let's call it "Shatter"). First we create a statistic on the enemy to hold how many chill stacks have been applied, and publish that fact to Oracle:

```js
// Enemy Create Event, after we have already set up their Oracle Facts
chill = new CatalystStatistic(0);
chill.PublishToFact(
	facts,
	"chill",
	function(_stat) {
		return _stat.GetValue();
	}
);
```

Earlier, we learned `SetStacks()` for a Modifier whose stack count belongs to the Modifier itself. We *could* respond to every Chill change by also calling `SetStacks()` on our damage Modifier, but then the same state would exist in two places: once on the enemy and again on the Modifier, and we would also have the enemies state effecting the players state in a somewhat backwards way.

Instead, let Catalyst calculate the stack count from the fact we already trust:

```js
// Whenever the player receives the Shatter upgrade
shatter_bonus = new CatalystModifier(2, eCatMathOps.ADD)
    .SetMaxStacks(5)
    .SetStackFunc(function(_stat, _facts) {
        return _facts.GetFrom("target", "chill") ?? 0;
    });

damage.AddModifier(shatter_bonus);
```

`SetStackFunc()` gives Catalyst a function for answering "how many stacks should this Modifier use right now?" Just like a condition function, it receives the Statistic as `_stat` and the resolved facts as `_facts`, but it returns a **number** instead of `true` or `false`.

Then, whenever appropriate, we add a modifier to the enemies `chill` Statistic, for instance, if we hit it with a chilling spell:

```js
// Collide Event in the chill spell instance colliding with obj_enemy

var _enemy_chill_stacks = other[$ "chill"];
if (_enemy_chill_stacks != undefined) {
    _enemy_chill_stacks.AddModifier(
        new CatalystModifier(1, eCatMathOps.ADD, game_get_speed(gamespeed_fps) * 8)
    );
}

// Other code that would happen when the chill spells hit the enemy goes here, maybe applying some damage or whatever
```

First we see if the enemy even *has* a chill Statistic, and if so, we add a Modifier that increases it by 1 and lasts for 8 seconds (assuming the default timer).

> Much like the nullish coalescing operator, we are using the `$` accessor here to read the `chill` variable from the enemy instance struct: `other[$ "chill"]`. Since this is in the Collision Event between the chill spell and the enemy, `other` refers to the enemies id here. If the enemy doesn't have a `chill` variable defined at all, the accessor will return `undefined` instead of crashing the game, so this is a safer way of trying to read the value instead of using dot notation: `other.chill` which would crash if `chill` didn't exist. A *better* way would be to standardise all your enemies through a parenting or composition to ensure that every one of them has a `chill` variable, but that's really swinging far into specific game architecture and so I won't touch on that here.
{: .note}

If we've applied three Chill stacks already (and assuming that Last Stand and Frozen aren't being applied as well):

```js
var _damage = damage.GetValue(); // 16
```

The stack function returns `3`, so Catalyst applies three stacks of `+2` to the base damage of `10`.

If one of the Chill stacks times out and the modifier gets automatically removed:

```js
var _damage = damage.GetValue(); // 14
```

there is no separate call to `shatter_bonus.SetStacks(1)`. The enemy changed the state it owns, and Catalyst asks the stack function again when the Statistic needs recalculating.

`SetMaxStacks(5)` still limits the result. If the target fact says `8`, Catalyst can only use five stacks because that is the Modifier's maximum.

> Use `SetStacks()` when the Modifier itself should remember how many stacks it has. Use `SetStackFunc()` when the stack count should be worked out from game state that already exists somewhere else.
{: .note}

---

## Conditions and stack functions can work together

A Modifier can have both a condition and a stack function when those answer different parts of the rule.

Suppose the Shatter bonus should only work once the target is actually frozen. We can add a condition to the same Modifier:

```js
shatter_bonus.SetCondition(function(_stat, _facts) {
    return _facts.GetFrom("target", "frozen") ?? false;
});
```

The stack function still answers **how strong is the bonus?** by returning the target's Chill stacks. The condition answers **is the bonus active at all?** by checking whether the target is frozen.

Catalyst checks the condition first. If it fails, the Modifier is skipped. If it passes, Catalyst uses the stack function, limits the result to the allowed stack range, and then applies the Modifier.

We could have written one more complicated stack function that returns `0` whenever the target isn't frozen, but separating the two rules keeps each callback responsible for one question.

And as you can start to see, you can build up quite complex game design rules pretty easily once you understand the system Catalyst uses.

---

## When the current situation isn't the question you want to ask

So far every example has been about the game state that is actually true right now. That is the normal path: facts live with the things that own them, the Statistic has a Fact View, and ordinary `GetValue()` calls use the current situation automatically.

Sometimes, however, you deliberately want to ask about a situation that **isn't** currently true.

Suppose the current target isn't frozen, so Frostbreaker currently gives:

```js
var _damage = damage.GetValue(); // 10
```

A targeting preview might still want to answer a different question: **what would the damage be if this target were frozen?**

We don't want to change the real enemy just to calculate that preview. Instead, create an `OracleFactQuery` that overrides the target's frozen fact for one evaluation:

```js
var _query = new OracleFactQuery()
    .SetFrom("target", "frozen", true);

var _preview_damage = damage.Evaluate(_query); // 12.5
```

`SetFrom()` mirrors the same named structure we've already been using. It says that, for this query, the `"frozen"` fact inside the `"target"` part of the view should be treated as `true`.

When `Evaluate()` runs, Catalyst starts from the Statistic's normal `combat_fact_view`, then applies the query to the resolved facts for this one calculation. Frostbreaker's condition receives the temporary value and applies the Modifier.

The real target hasn't changed:

```js
var _damage = damage.GetValue(); // still 10
```

`target.facts.Get("frozen")` is still `false`, the Fact View still points at the same enemy, and there is nothing to reset after the preview. The override existed only for that call to `Evaluate()`.

That makes `Evaluate()` useful for things such as equipment previews, AI considering possible actions, targeting interfaces, simulations, or any other "what would happen if...?" question where changing the real game state would be the wrong thing to do.

---

## `GetValue()` and `Evaluate()` answer different questions

The distinction is fairly simple.

`GetValue()` asks for the Statistic's value under the game state its Fact View can currently see:

```js
var _damage = damage.GetValue();
```

If the current target becomes frozen, changes to a different enemy, or some player fact used by the Statistic changes, Catalyst notices that the view is out of date and recalculates before returning the value.

`Evaluate()` asks for a temporary answer with one or more facts changed for that calculation:

```js
var _query = new OracleFactQuery()
    .SetFrom("target", "frozen", true);

var _preview_damage = damage.Evaluate(_query);
```

The query doesn't replace the Fact View. It starts from the same live situation and changes only the facts you explicitly override.

A query can override several named facts when a hypothetical needs them:

```js
var _query = new OracleFactQuery()
    .SetFrom("player", "health_fraction", 0.20)
    .SetFrom("target", "is_boss", true);

var _preview = damamge.Evaluate(_query);
```

Even if the player is currently healthy and the real target isn't a boss, this evaluation asks what Last Stand would do under that imagined combination.

> `GetValue()` asks "what is this Statistic worth in the current situation?" `Evaluate()` asks "what would it be if these particular facts were different?"
{: .note}

`Evaluate()` also accepts a plain struct as shorthand for simple overrides in Oracle's default fact chain. We haven't used that form here because named `"player"` and `"target"` chains make ownership much clearer for this kind of gameplay state. The Oracle documentation covers default chains and the shorthand form in more detail.

---

## Choosing where a fact belongs

When you're deciding how to represent a situational value, the useful question is usually **who owns this truth?**

If a value describes an enemy, that enemy's `OracleFacts` is a natural home for it. Some facts might be written directly by the enemy instance, like boss status, armour type, alertness, etc, while others can be Statistics or Resource that are automatically kept updated in Oracle via `PublishToFact()`, such as the Frozen state or accumulated status stacks.

If a value describes the player, keep it with the player. Again, some facts might be written directly by the player object, while Catalyst Statistics and Resources can publish values they already own through `PublishToFact()`.

Other systems can own their own scopes as well. A combat controller might expose facts about the current encounter, while a world controller could expose weather or time of day. A Fact View can bring whichever scopes are relevant together under separate names.

The important thing to keep in mind is that Oracle means that the Statistic doesn't become responsible for trying to maintain the correct values for those facts. The Statistics job is to read them when its rules need them, and Oracles job is to share those facts to whatever needs them.

Queries are different. A query doesn't describe a new source of truth. It describes a temporary assumption for one calculation. If the real game should now consider an enemy frozen, update the enemy's facts. If you only want to know what would happen **if** the enemy were frozen, use an `OracleFactQuery` with `Evaluate()`.

---

## Putting the whole setup together

We've built up three different situational rules on this page:

* **Frostbreaker** increases damage by 25% while the current target is frozen.
* **Last Stand** increases damage by 50% while the player is below 30% health and the current target is a boss.
* **Shatter** adds `+2` damage for every Chill stack on the current target, up to five stacks, but only while that target is frozen.

All three rules live on the same `damage` Statistic. Each one looks at the parts of the current situation it cares about, while the systems that own that state continue managing it normally.

Let's put the complete setup together in one place so we can view it holistically.

The enemy owns the Statistics that describe its changing status effects, along with the Oracle facts it exposes to the rest of the game:

```js
// obj_enemy Create event

facts = new OracleFacts({
    is_boss : false
});

frozen = new CatalystStatistic(0);

frozen.PublishToFact(
    facts,
    "frozen",
    function(_stat) {
        return _stat.GetValue() > 0;
    }
);

chill = new CatalystStatistic(0);

chill.PublishToFact(
    facts,
    "chill",
    function(_stat) {
        return _stat.GetValue();
    }
);
```

`frozen` and `chill` remain ordinary Catalyst Statistics. Oracle doesn't replace them or become a second place where we have to keep the same gameplay state.

Each Statistic publishes the part of its current value that other systems need to know.

For `frozen`, Oracle only cares whether the final value is above `0`, so the published fact is either `true` or `false`.

For `chill`, we want other systems to know the actual number of Chill stacks, so we publish its calculated value directly.

A freezing spell can now add its own timed Modifier:

```js
frozen.AddModifier(
    new CatalystModifier(
        1,
        eCatMathOps.ADD,
        game_get_speed(gamespeed_fps) * 5
    )
);
```

while a chilling spell can independently add a Chill stack:

```js
chill.AddModifier(
    new CatalystModifier(
        1,
        eCatMathOps.ADD,
        game_get_speed(gamespeed_fps) * 8
    )
);
```

Several spells can add their own Modifiers at the same time. As those Modifiers are added and expire, Catalyst recalculates the enemy's `frozen` and `chill` Statistics and their live fact bindings keep Oracle in sync automatically.

The player has its own facts, HP Resource, combat Fact View, and damage Statistic:

```js
// obj_player Create event

facts = new OracleFacts();

hp = new CatalystResource(100);

hp.PublishToFact(
    facts,
    "health_fraction",
    function(_resource) {
        return _resource.GetFraction();
    }
);

target = noone;

combat_fact_view = new OracleFactView()
    .AddTo("player", facts);

damage = new CatalystStatistic(10)
    .SetFactView(combat_fact_view);
```

The player's HP Resource publishes its current fraction into the player's facts, while the combat view makes those facts available through the `"player"` chain.

When the player chooses an enemy (perhaps a hitbox hits the enemy, or they are mousing over an enemy, or however you decide "the player is now about to/has hit someone"), the targeting code places that enemy's facts into the `"target"` chain:

```js
if (target != _enemy) {
    target = _enemy;

    combat_fact_view
        .ClearFrom("target")
        .AddTo("target", target.facts);
}
```

The same combat view can now see information owned by both sides of the fight:

```text
player
    health_fraction

target
    frozen
    chill
    is_boss
```

Now we can attach all three situational Modifiers to the player's existing `damage` Statistic.

Frostbreaker asks whether the current target is frozen:

```js
frozen_bonus = new CatalystModifier(0.25, eCatMathOps.MULTIPLY)
    .SetCondition(function(_stat, _facts) {
        return _facts.GetFrom("target", "frozen") ?? false;
    });

damage.AddModifier(frozen_bonus);
```

Last Stand asks about both the player and the target:

```js
last_stand = new CatalystModifier(0.50, eCatMathOps.MULTIPLY)
    .SetCondition(function(_stat, _facts) {
        var _health_fraction = _facts.GetFrom("player", "health_fraction") ?? 1;
        var _target_is_boss = _facts.GetFrom("target", "is_boss") ?? false;

        return _health_fraction < 0.30 && _target_is_boss;
    });

damage.AddModifier(last_stand);
```

And Shatter gets its stack count from the target's current Chill Statistic, while only becoming active once that target is frozen:

```js
shatter_bonus = new CatalystModifier(2, eCatMathOps.ADD)
    .SetMaxStacks(5)
    .SetStackFunc(function(_stat, _facts) {
        return _facts.GetFrom("target", "chill") ?? 0;
    })
    .SetCondition(function(_stat, _facts) {
        return _facts.GetFrom("target", "frozen") ?? false;
    });

damage.AddModifier(shatter_bonus);
```

All three Modifiers are now attached to the same Statistic at the same time. We don't have to choose which rule `damage` is currently using, or manually add and remove them as the fight changes. Each Modifier decides for itself whether, and how strongly, it should contribute whenever Catalyst calculates the Statistic.

Suppose the current target is a boss.

The player has fallen to 20 HP:

```js
hp.Decrease(80);
```

and several effects have left the target frozen with three active Chill stacks.

At that point, an ordinary damage read is:

```js
var _damage = damage.GetValue(); // 30
```

All three rules contribute to that one result.

Shatter sees three Chill stacks and adds three stacks of `+2` damage:

```text
10 + 6 = 16
```

Frostbreaker sees that the target is frozen and increases that by 25%:

```text
16 × 1.25 = 20
```

Last Stand sees that the player is below 30% health and that the target is a boss, so it increases the result by another 50%:

```text
20 × 1.50 = 30
```

There's no big:

```js
if (target.is_boss) {
    // Some code
}

if (target.frozen){
    // More code
}

// etc
```

Chains you have to write. No calculations you need to keep track of. Nothing asking for damage needed to know any of those details. It still only called:

```js
damage.GetValue();
```

If one of the Chill Modifiers expires, the enemy's `chill` Statistic automatically falls, Oracle automatically updates and Shatter automatically becomes weaker.

If the final freezing Modifier expires, `frozen` returns to `0`, its published fact becomes `false`, and both Frostbreaker and Shatter stop applying.

If the player heals above 30% health, Last Stand stops applying.

If the player switches to another enemy, the `"target"` chain points at that enemy's facts instead and all three Modifiers immediately start answering their questions about the new target.

None of those changes require us to touch the `damage` Statistic or manually synchronize its Modifiers.

That's the useful pattern behind situational Statistics: the player and enemy maintain the state they actually own, Oracle gives Catalyst a view of the current situation, and each Modifier reads whatever parts of that situation its own rule needs. Several completely different rules can then build on the same Statistic without the systems responsible for those rules needing to know about each other.

---

## Next: Resource Flows

We now have Resources that can publish the state they own, Statistics that can react to facts from different parts of the game, and queries for the cases where we deliberately want to calculate against a hypothetical situation.

The next useful combination is a rule that changes a Resource over time. Stamina regeneration needs a Resource to move, but the regeneration rate is itself a Statistic, so equipment, buffs, debuffs and situational rules can all change how quickly it moves.

Continue with **[Resource Flows](resource-flows)** for regeneration, drains, delays, pausing, and rates that use the same Statistic machinery you've already learned.
