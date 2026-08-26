---
layout: default
title: Patterns and recipes
parent: Catalyst 2
nav_order: 9
redirect_from:
  - /catalyst/patterns.html
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Patterns and recipes

These examples put Catalyst's main pieces together into complete game systems.

They are simply some common shapes that you can get ideas from, and they're not meant to prescribe one way to structure every project. Each one starts with a gameplay problem, then combines the Statistics, Modifiers, Resources, Flows, Effects, facts and Sets you've already learned about throughout these docs in order to solve the gameplay problem.

The examples range across genres because Catalyst is **not** just an RPG stat system. It's a general purpose numeric state manager. The same pieces can be useful anywhere a numeric rule is affected by other game state.

Flow rates, delays, Effect durations and tick intervals below are expressed in whatever countdown units your project has chosen. A city simulation advancing Catalyst once per simulation step will interpret a rate differently from a real-time game using delta-time seconds, and the [Resource Flows](resource-flows) guide covers those timing models in detail.

One thing I want you to keep in mind is how we use the same basic Catalyst primitives to express complex and varied gameplay rules. That's the real power of Catalyst. Instead of thinking "Ah gosh, now I have to build a recharge system", or "Now I have to model population flow in my City Sim", the question becomes much simpler: "What parts of Catalyst do I combine to make this design happen?"

---

## City population driven by jobs and housing

Suppose a city has 4,200 residents. Population changes gradually as people move in and out, while available housing, jobs and happiness affect the direction of that migration.

Population itself is a good `CatalystResource`: it has a current amount that changes over time. Net migration is a good `CatalystResourceFlow`, because it's an ongoing signed change to that Resource.

Housing capacity and job capacity are calculated values rather than stored amounts, so they fit Statistics. We'll also keep happiness as a direct Oracle Fact for this example:

```js
population = new CatalystResource(1000000, 4200)
    .SetMaximumBoundMode(eCatResourceBoundMode.SOFT)
    .SetMinimumBoundMode(eCatResourceBoundMode.HARD);

housing_capacity = new CatalystStatistic(5000);
job_capacity = new CatalystStatistic(4700);

city_state_facts = new OracleFacts({
    happiness : 0.70
});

city_state_view = new OracleFactView()
    .Add(city_state_facts);
```

The maximum of `1000000` here is just a deliberately distant soft safety limit. We're **not** using housing capacity as the Resource maximum.

We're using a `SOFT` upper bound here, so if a city has 5,000 residents and you reduce a Resource's maximum to 4,000, Catalyst won't reconcile the current Resource value down to the new maximum. That behaviour fits something like a fuel tank whose physical capacity really has shrunk, but for population it would mean 1,000 citizens disappear immediately when an apartment block is demolished.

In this model, housing is instead something that affects migration pressure. A housing shortage causes people to leave over time.

The amount of free housing and the number of open jobs are both derived from other Catalyst values. Instead of recalculating them manually whenever something changes, publish the values they depend on to Oracle:

```js
housing_capacity.PublishToFact(city_state_facts, "housing_capacity");
job_capacity.PublishToFact(city_state_facts, "job_capacity");
population.PublishToFact(city_state_facts, "population");
```

Now `free_housing` and `open_jobs` can be Statistics whose base functions calculate their values from those facts:

```js
free_housing = new CatalystStatistic(0)
    .SetFactView(city_state_view)
    .SetBaseFunc(function(_statistic, _facts) {
        return _facts.Get("housing_capacity") - _facts.Get("population");
    });

open_jobs = new CatalystStatistic(0)
    .SetFactView(city_state_view)
    .SetBaseFunc(function(_statistic, _facts) {
        return _facts.Get("job_capacity") - _facts.Get("population");
    });
```

These are useful Statistics in their own right. For example, a housing policy could modify effective free housing without changing the city's physical housing capacity.

The migration rules need to see those calculated values too, so publish them into a second Oracle Fact scope:

```js
city_derived_facts = new OracleFacts();

free_housing.PublishToFact(city_derived_facts, "free_housing");
open_jobs.PublishToFact(city_derived_facts, "open_jobs");

city_fact_view = new OracleFactView()
    .Add(city_state_facts)
    .Add(city_derived_facts);
```

Keeping the derived facts in a separate scope means `free_housing` and `open_jobs` only listen to the facts they actually use to calculate themselves. The migration rule can combine both scopes in one Fact View.

Net migration is the ongoing change to the population Resource:

```js
migration = new CatalystResourceFlow(0, "Net migration");
population.AddFlow(migration);
```

The Flow's rate is a Statistic, so we can give that Statistic the combined city fact view and build the migration rules with ordinary Modifiers:

```js
var _migration_rate = migration.GetRateStatistic();
_migration_rate.SetFactView(city_fact_view);

_migration_rate.AddModifier(
    new CatalystModifier(8, eCatMathOps.ADD)
        .SetCondition(function(_stat, _facts) {
            return (_facts.Get("free_housing") ?? 0) > 0
                && (_facts.Get("open_jobs") ?? 0) > 0;
        })
        .SetSourceLabel("Attractive city")
);

_migration_rate.AddModifier(
    new CatalystModifier(-12, eCatMathOps.ADD)
        .SetCondition(function(_stat, _facts) {
            return (_facts.Get("free_housing") ?? 0) < 0;
        })
        .SetSourceLabel("Housing shortage")
);

_migration_rate.AddModifier(
    new CatalystModifier(-6, eCatMathOps.ADD)
        .SetCondition(function(_stat, _facts) {
            return (_facts.Get("happiness") ?? 0) < 0.40;
        })
        .SetSourceLabel("Low happiness")
);
```

The Flow starts from a rate of `0`. If the city has both free housing and open jobs, the first Modifier contributes `+8`. If housing is already over capacity, the second contributes `-12`, while severe unhappiness can push migration down another `6`.

Because the source Statistics and Resource publish themselves to Oracle, changes to housing capacity, job capacity or population automatically update the derived Statistics. Those Statistics then publish their new values for the migration rule to use. The city simulation doesn't need separate code to keep `free_housing` and `open_jobs` synchronized.

This same shape works for immigration, tourism, crime growth, disease spread, pollution, public approval or any other city value where **the current amount changes over time, but the rate of change depends on the city's current conditions**.

---

## A factory whose output depends on machines and power

A factory might produce 20 units of steel per simulation step with one active production line, then gain another 20 units for every additional line. If the factory has too little available power, however, production should fall sharply.

Steel is a stored quantity that should keep increasing over time, so the production itself is a Resource Flow. The number of effective production lines and the factory's available power are calculated values that other gameplay rules may affect, so they fit Statistics:

```js
production_lines = new CatalystStatistic(3);
power_supply = new CatalystStatistic(100);

factory_facts = new OracleFacts();
factory_fact_view = new OracleFactView()
    .Add(factory_facts);

production_lines.PublishToFact(factory_facts, "production_lines");
power_supply.PublishToFact(factory_facts, "power_supply");
```

Publishing those Statistics makes their current values available to other rules through Oracle. For example, damage could reduce the factory's effective production lines, while a grid failure or temporary generator could modify its available power. Anything reading these facts will then see the new calculated values.

Now create the steel stockpile and the Flow that fills it. The Flow already has a rate Statistic inside it, which is where we calculate how quickly the factory is currently producing steel:

```js
steel_stockpile = new CatalystResource(10000, 0);
steel_production = new CatalystResourceFlow(20, "Steel production");
steel_stockpile.AddFlow(steel_production);

var _production_rate = steel_production.GetRateStatistic();
_production_rate.SetFactView(factory_fact_view);
```

We can let one Modifier represent the contribution from additional production lines:

```js
_production_rate.AddModifier(
    new CatalystModifier(20, eCatMathOps.ADD)
        .SetStackFunc(function(_stat, _facts) {
            return max(0, (_facts.Get("production_lines") ?? 1) - 1);
        })
        .SetSourceLabel("Additional production lines")
);
```

The Flow's base rate already represents the first line, so the stack function subtracts one from the total line count. With three effective production lines, the Modifier uses two stacks and contributes another `40`, giving a production rate of `60` steel per step.

Now let available power affect that rate. Suppose the factory needs at least `50` power to operate normally:

```js
_production_rate.AddModifier(
    new CatalystModifier(-0.50, eCatMathOps.MULTIPLY)
        .SetCondition(function(_stat, _facts) {
            return (_facts.Get("power_supply") ?? 0) < 50;
        })
        .SetSourceLabel("Power shortage")
);
```

When `power_supply` falls below `50`, the factory's current production rate is cut by 50%. Every time the Flow advances, it uses the current value of its rate Statistic, so changes to production lines or available power automatically change future steel production.

This pattern works well whenever a simulation has a **calculated throughput feeding a stored quantity**: farms producing food, mines producing ore, generators producing stored energy, servers processing jobs, pumps filling reservoirs, or logistics hubs moving cargo.

---

## Stealth detection as a one-off situational calculation

Not every changing rule needs to become ongoing shared state. In a stealth game, a guard's detection strength might depend on the particular target being checked right now: whether that target is crouching, standing in light, moving quickly, or making noise.

Suppose a guard has a base detection strength of `10`:

```js
detection = new CatalystStatistic(10);
```

These conditions all describe the target being checked, so the Modifiers can read them from a named `target` Fact chain:

```js
detection.AddModifier(
    new CatalystModifier(0.60, eCatMathOps.MULTIPLY)
        .SetCondition(function(_stat, _facts) {
            return _facts.GetFrom("target", "in_bright_light") == true;
        })
        .SetSourceLabel("Bright light")
);

detection.AddModifier(
    new CatalystModifier(-0.35, eCatMathOps.MULTIPLY)
        .SetCondition(function(_stat, _facts) {
            return _facts.GetFrom("target", "crouching") == true;
        })
        .SetSourceLabel("Crouching target")
);

detection.AddModifier(
    new CatalystModifier(4, eCatMathOps.ADD)
        .SetCondition(function(_stat, _facts) {
            return (_facts.GetFrom("target", "noise") ?? 0) >= 0.75;
        })
        .SetSourceLabel("Loud target")
);
```

When this guard checks one target, create a one-off Oracle query containing that target's current situation and pass it into `Evaluate()`:

```js
var _query = new OracleFactQuery()
    .SetFrom("target", "in_bright_light", true)
    .SetFrom("target", "crouching", false)
    .SetFrom("target", "noise", 0.90);

var _strength = detection.Evaluate(_query);
```

Those values exist only for this evaluation. They don't become persistent facts attached to the guard, so the same guard can evaluate several different targets during one step without changing its normal Fact View. Using a named `target` chain also keeps target information separate from any world, player or guard facts the Statistic may use later.

The same pattern suits aim assistance, cover calculations, line-of-sight quality, dialogue attitude toward a particular listener, racing overtakes, tactical hit chances, or any other calculation whose answer depends on the current pairing or interaction. Ongoing state can live in the Statistic's normal `OracleFactView`, while an `OracleFactQuery` supplies the temporary facts that belong only to this particular calculation.

---

## Racing boost with a draining charge

A racing game might have a boost meter that drains while boost is held, then refills when boost isn't active. The amount in the meter is stored state, while the drain and refill are ongoing changes, so this maps naturally to a Resource with two Flows.

```js
boost_charge = new CatalystResource(100);
boost_active = false;

boost_drain = new CatalystResourceFlow(-30, "Boost drain")
    .SetActive(false);

boost_refill = new CatalystResourceFlow(12, "Boost recharge");

boost_charge.AddFlow(boost_drain);
boost_charge.AddFlow(boost_refill);
```

When boost begins, enable the drain and disable the refill:

```js
boost_drain.SetActive(true);
boost_refill.SetActive(false);
```

When the driver releases boost, reverse those states:

```js
boost_drain.SetActive(false);
boost_refill.SetActive(true);
```

If recharge shouldn't begin immediately, use the Flow delay you learned earlier:

```js
boost_refill.Delay(1.5);
```

Now the meter has a simple lifecycle without the car object manually subtracting and adding charge every update.

The boost's effect on the car can remain a completely separate Statistic rule:

```js
engine_force = new CatalystStatistic(8000);

boost_force = new CatalystModifier(0.25, eCatMathOps.MULTIPLY)
    .SetSourceLabel("Boost");
```

When boost actually starts, first make sure charge remains, then attach that Modifier along with changing the Flow states:

```js
if (!boost_charge.IsEmpty()) {
    boost_active = true;
    boost_drain.SetActive(true);
    boost_refill.SetActive(false);
    engine_force.AddModifier(boost_force);
}
```

When the driver releases boost, end the boost and detach the Modifier so the same authored rule can be reused the next time:

```js
boost_active = false;
boost_drain.SetActive(false);
boost_refill.SetActive(true);
boost_refill.Delay(1.5);
engine_force.DetachModifier(boost_force);
```

Running out of charge should take the same stop path rather than leaving the engine bonus active at an empty meter. In the car's normal update code, check the Resource while boost is active:

```js
if (boost_active && boost_charge.IsEmpty()) {
    boost_active = false;
    boost_drain.SetActive(false);
    boost_refill.SetActive(true);
    boost_refill.Delay(1.5);
    engine_force.DetachModifier(boost_force);
}
```

The Resource answers **whether there's charge left**, the Flows manage **how charge changes**, and the Modifier handles **what boosting does to engine force**. `DetachModifier()` is deliberate here: unlike `DestroyModifier()`, it keeps `boost_force` alive so a later boost can attach the same Modifier again.

Keeping those jobs separate makes it easier to add heat, upgrade recharge speed, reduce drain on certain track surfaces, or let damage weaken the boost without rewriting one monolithic boost system.

---

## Sports accuracy that falls with fatigue

Suppose a basketball player's shot accuracy is normally `0.75`, but tired players lose accuracy. Stamina is already represented as a Resource:

```js
stamina = new CatalystResource(100);
shot_accuracy = new CatalystStatistic(0.75, 0, 1)
    .SetClamped();
```

Add a conditional fatigue penalty:

```js
shot_accuracy.AddModifier(
    new CatalystModifier(-0.15, eCatMathOps.ADD)
        .SetCondition(function(_stat, _facts) {
            return (_facts.Get("stamina_fraction") ?? 1) < 0.25;
        })
        .SetSourceLabel("Severe fatigue")
);
```

When resolving a shot, ask for accuracy using the player's current stamina fraction:

```js
var _accuracy = shot_accuracy.Evaluate({
    stamina_fraction : stamina.GetFraction()
});
```

We could publish stamina into Oracle facts, but there isn't much reason to keep a shared fact updated if this value is only needed when a shot is attempted. `Evaluate()` lets the stamina Resource remain the one place that remembers current stamina while the accuracy Statistic receives exactly the temporary information needed for this shot.

If many systems start depending continuously on the same fatigue state, such as movement speed, defensive reactions, injury chance, AI decisions and animation selection, promote fatigue into a shared Fact instead.

---

## A storm that temporarily changes several city systems

Effects aren't limited to character buffs and debuffs. A city-wide storm is also a temporary state with several consequences that should begin and end together.

Suppose the city has a power-generation Statistic and an emergency-reserve Resource:

```js
power_generation = new CatalystStatistic(120);
emergency_power = new CatalystResource(500);
city_effects = new CatalystEffectManager(self);
```

A severe storm should reduce generation by 30% and drain emergency power at a rate of 15 units per countdown unit. Build those consequences as one Effect:

```js
storm_effect = new CatalystEffect("severe_storm", 12)
    .AddTag("weather")
    .AddTag("storm")
    .SetTickInterval(1);

storm_effect.AddModifier(
    power_generation,
    new CatalystModifier(-0.30, eCatMathOps.MULTIPLY)
        .SetSourceLabel("Storm damage")
);

storm_effect.AddFlow(
    emergency_power,
    new CatalystResourceFlow(-15, "Storm reserve usage")
);

city_effects.AddEffect(storm_effect);
```

`storm_effect` is kept as a persistent reference because the weather system will use that exact active Effect later. Once it's active, its Modifier reduces power generation for the whole Effect lifetime. Its owned Flow still represents a rate per countdown unit, but the Effect controls when that Flow is applied. With a tick interval of `1`, a rate of `-15` removes `15` emergency power on each tick. If the interval were `2`, each tick would represent two countdown units and remove `30` instead.

Using one Effect here means an early weather-clear event can remove the whole storm cleanly:

```js
city_effects.RemoveEffect(storm_effect, "weather_cleared");
```

The generation penalty and reserve drain belong to the same temporary event, so they disappear together rather than leaving city code responsible for synchronising several timers.

The same pattern fits blackouts, festivals, strikes, sieges, weather fronts, match-wide rules, global difficulty events or temporary environmental states.

---

## Comparing car upgrades before installing them

Sets and previews are useful anywhere players compare packages of changes, not just equipment screens in RPGs. A racing garage might let the player compare a new engine package against the one currently installed.

First, give the car Statistics identities that incoming parts can target, then put them in one Set:

```js
engine_force = new CatalystStatistic(8000)
    .SetName("Engine Force")
    .SetIdentity("engine_force");

fuel_efficiency = new CatalystStatistic(1.00)
    .SetName("Fuel Efficiency")
    .SetIdentity("fuel_efficiency");

car_stats = new CatalystSet("car_stats")
    .AddStatistic(engine_force)
    .AddStatistic(fuel_efficiency);
```

Describe the currently installed engine as a reusable Modifier package:

```js
current_force_mod = new CatalystModifier(1000, eCatMathOps.ADD)
    .SetTargetIdentity("engine_force");

current_efficiency_mod = new CatalystModifier(-0.08, eCatMathOps.ADD)
    .SetTargetIdentity("fuel_efficiency");

current_engine = new CatalystModifierSet("street_engine")
    .AddModifier(current_force_mod)
    .AddModifier(current_efficiency_mod);

car_stats.Apply(current_engine);
```

Now describe the racing engine the player is considering. Its Modifiers are still detached because the engine hasn't been installed:

```js
race_engine = new CatalystModifierSet("race_engine")
    .AddModifier(
        new CatalystModifier(2200, eCatMathOps.ADD)
            .SetTargetIdentity("engine_force")
    )
    .AddModifier(
        new CatalystModifier(-0.18, eCatMathOps.ADD)
            .SetTargetIdentity("fuel_efficiency")
    );
```

These Modifiers haven't been attached to the car. They only describe what this package would do.

Ask the car Set to preview the swap:

```js
var _preview = car_stats.PreviewSwap(
    current_engine,
    race_engine
);
```

Catalyst calculates the car as though the current engine's exact Modifiers were removed and the racing engine's Modifiers were attached to their named target Statistics, but it doesn't actually uninstall or install anything.

If the player accepts the comparison, the same two packages can perform the real all-or-nothing swap:

```js
var _result = car_stats.ApplySwap(
    current_engine,
    race_engine
);

if (_result.Succeeded()) {
    current_engine = race_engine;
}
```

That lets a garage UI show the tradeoff (more engine force, worse fuel efficiency) before the player commits, then apply exactly the package it previewed. The same approach works for ship modules, robot components, city policies, factory upgrade packages, deck-building relics, sports formations, vehicle tuning presets or any other system where one package changes several numeric rules at once.

---

## A reactor that gets harder to cool as it overheats

Catalyst can also describe feedback loops where one current value changes the rule governing another.

Suppose a reactor stores heat as a Resource. A standalone cooling Flow continuously removes heat:

```js
reactor_heat = new CatalystResource(100, 20);
reactor_cooling = new CatalystResourceFlow(-8, "Cooling system");

reactor_heat.AddFlow(reactor_cooling);
```

Now imagine the cooling system becomes less effective above 80% heat. We can evaluate the Flow's rate Statistic against the current heat fraction:

```js
var _cooling_rate = reactor_cooling.GetRateStatistic();

_cooling_rate.AddModifier(
    new CatalystModifier(-0.50, eCatMathOps.MULTIPLY)
        .SetCondition(function(_stat, _facts) {
            return (_facts.Get("heat_fraction") ?? 0) >= 0.80;
        })
        .SetSourceLabel("Cooling saturation")
);
```

A standalone Flow normally asks its rate Statistic for the current value without supplying one-off query facts. If heat should continuously affect cooling, its rate Statistic needs ongoing access to the current heat fraction:

```js
reactor_facts = new OracleFacts();

reactor_fact_view = new OracleFactView()
    .Add(reactor_facts);

_cooling_rate.SetFactView(reactor_fact_view);
```

Let the Resource publish its fraction directly instead of manually updating that fact every time heat changes:

```js
reactor_heat_binding = reactor_heat.PublishToFact(
    reactor_facts,
    "heat_fraction",
    function(_resource) {
        return _resource.GetFraction();
    }
);
```

`PublishToFact()` writes the fact immediately. The `CatalystFactBinding` it returns then keeps publishing the new fraction whenever the Resource changes.

Below 80% heat, cooling removes `8` units per countdown unit. At or above 80%, the `-50%` Modifier applies and the same Flow cools at only `4` units per countdown unit.

The same feedback shape can support machinery wear, ecological collapse, traffic congestion, network saturation, instability, combo meters, crowd excitement or any system where **the current state changes the rate at which that state can recover or worsen**.

---

## Choosing the primitive from the behaviour

These recipes use different Catalyst pieces because the underlying game behaviour is different. Choose according to what kind of thing the number represents:

- If the game needs to **calculate what a number should be**, start with a `CatalystStatistic`.
- If something should **change that calculation while it exists**, use a `CatalystModifier`.
- If the game needs to **remember how much of something currently exists**, use a `CatalystResource`.
- If that stored amount should **keep moving over time**, use a `CatalystResourceFlow`.
- If several temporary changes describe **one state that should begin and end together**, use a `CatalystEffect`.
- If a rule should normally see **ongoing world or character state**, give the relevant Statistic an Oracle Fact View.
- If the rule only needs information for **one particular calculation**, pass that information through `Evaluate()` instead.
- If several related Catalyst values form **one gameplay model**, coordinate them with a `CatalystSet`.
- If several Modifiers form **one reusable package** for previewing or applying, put them in a `CatalystModifierSet`.

Try not to think in rigid genre rules. A population count and an ammunition magazine can both be Resources, immigration and shield regeneration can both be Flows, and a city blackout and a poisoned character can both be Effects. Catalyst cares about the behaviour of the number, not what genre the game belongs to.

