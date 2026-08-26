---
layout: default
title: Effects
parent: Catalyst
nav_order: 5
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Effects

A Modifier can change one Statistic, while a Resource Flow can keep moving one Resource until you disable or remove it. Each of those pieces can have its own lifetime.

Gameplay rules often arrive as a bundle, though. Being **burning** might drain HP, reduce defence, count as a `fire` debuff, last for five seconds, and disappear completely if the player uses a cleanse. Those pieces all describe one gameplay state, so managing each one separately would leave your own code responsible for keeping their lifetimes in sync.

A `CatalystEffect` lets those changes belong to the same thing. You build the Effect first, give it the Modifiers and Flows that make up the state, then submit it to a `CatalystEffectManager`. If the Effect becomes active, those changes become active with it. When the Effect is removed or expires, Catalyst removes and destroys the changes it owns.

---

## Your first Effect

Suppose a five-second rage state should increase the character's damage and stamina regeneration together.

Because this is a real-time example, first tell the shared Catalyst countdown tracker to use delta time. In that mode, durations and Flow rates are authored in seconds:

```js
CATALYST_COUNTDOWN.StartAutomatic(eCatCountdownMode.DELTA_TIME);
```

The character already has the pieces those rules affect:

```js
damage = new CatalystStatistic(20);

stamina = new CatalystResource(100);
stamina_regen = new CatalystResourceFlow(12);
stamina.AddFlow(stamina_regen);

effects = new CatalystEffectManager(self);
```

An Effect Manager keeps track of the Effects currently active on one game object or other owner. This one belongs to the character, so we pass `self` when we create it.

Now build the rage Effect while it's still detached:

```js
rage_effect = new CatalystEffect("rage", 5);

rage_effect.AddModifier(
    damage,
    new CatalystModifier(8, eCatMathOps.ADD)
        .SetLayer(eCatStatLayer.TEMP)
);

rage_effect.AddModifier(
    stamina_regen.GetRateStatistic(),
    new CatalystModifier(6, eCatMathOps.ADD)
        .SetLayer(eCatStatLayer.TEMP)
);
```

`new CatalystEffect("rage", 5)` creates a five-second rage Effect because the shared tracker is using delta time. The string `"rage"` is its **identity**: a stable name Catalyst can later use for rules such as “refresh the existing rage instead of adding another copy.” The Effect isn't active yet. Right now we're only describing what rage will do if it's applied.

We're keeping this Effect in the persistent `rage_effect` variable because a later example will remove this exact active Effect. If you only build and submit an Effect once and never need its exact reference again, a temporary local is fine.

Each `AddModifier()` gives the Effect one Modifier and tells it which Statistic that Modifier should affect. Calling `AddModifier()` on the Effect **doesn't change the Statistic yet**. The Modifier waits with the Effect until we submit the finished Effect to its manager.

Finally, apply it:

```js
var _application = effects.AddEffect(rage_effect);
```

If the application succeeds, Catalyst attaches both staged Modifiers and starts tracking the Effect's five-second lifetime. Damage rises from 20 to 28, while the regeneration Flow's rate rises from 12 to 18:

```js
show_debug_message(damage.GetValue()); // 28
show_debug_message(stamina_regen.GetRateStatistic().GetValue()); // 18
```

When rage expires, Catalyst removes the Effect and destroys both Modifiers it owns automatically. Both values return to normal together without the gameplay code having to find and clean up two separate temporary changes.

> Build the Effect first, then apply it. `AddModifier()` and `AddFlow()` describe the changes that belong to the Effect, while `EffectManager.AddEffect()` is what makes the Effect and those changes active.
{: .note}

---

## Why the shared owner matters

Without an Effect, your game would have to attach both rage Modifiers itself, track when the rage effect should end, and remember to remove both Modifiers at the right time.

The Effect gives **rage itself** ownership of those related consequences and their shared lifetime. As the design grows, the same Effect can also own a Resource Flow, carry tags other systems can recognise, run setup or cleanup logic, be refreshed, or be removed early by a cleanse.

The individual Modifiers and Flows still work exactly as they do normally. The Effect is the gameplay struct that says those changes belong to the same state and should appear and disappear together.

---

## Once a Modifier or Flow belongs to an Effect

Passing a detached Modifier to `effect.AddModifier()` makes that Modifier part of the Effect. The same is true for a Flow passed to `effect.AddFlow()`.

From that point on, don't try to run a second lifetime for that Modifier or Flow. The Effect is already the thing deciding when the change starts and ends.

An Effect-owned Modifier or Flow follows the Effect's countdown tracker too. Calls such as `SetCountdownTracker()` on the owned Modifier or Flow are ignored, because giving one part of the Effect a different clock would break the shared lifetime we're using the Effect to create.

The rule is:

```text
standalone Modifier / Flow -> can use its own timing
part of an Effect          -> follows the Effect's timing and lifetime
```

If a Modifier or Flow needs to keep existing after the Effect ends, it shouldn't be added to that Effect in the first place.

---

## Removing an Effect early

Effects don't have to wait for their duration to expire. If rage should end because the character was dispelled, you can check that the exact Effect is still active and remove it through its manager:

```js
if (effects.HasEffect(rage_effect)) {
    effects.RemoveEffect(rage_effect, "dispelled");
}
```

The second argument is an open-ended removal reason. Catalyst doesn't assign gameplay meaning to strings such as `"dispelled"`. It passes the reason along to the Effect's removal callback if one exists.

Removing the Effect performs the same cleanup as natural expiry: Catalyst removes the Effect from active state, destroys the Modifiers and Flows it owns, and destroys the Effect itself. Keep the reference only for as long as you need to target that active Effect, and don't keep using it after removal.

You can get the manager's current active Effects with:

```js
var _active_effects = effects.GetEffects();
```

`GetEffects()` returns a new shallow array containing the active Effect references, so changing the returned array itself doesn't rewrite the manager's internal Effect list.

---

## Tags describe what an active Effect represents

Often you don't care about one exact Effect reference. A cleanse spell might need to remove every poison (or even all debuffs), or an animation system might only need to know whether the character currently has any stun Effect.

Tags give active Effects those broader labels:

```js
var _burn = new CatalystEffect("burn", 5)
    .AddTag("debuff")
    .AddTag("fire");

effects.AddEffect(_burn);
```

`AddTag()` adds the tag to the Effect. `AddEffect()` makes this burn active in `effects`, so the manager can now answer questions about the tags supplied by its active Effects:

```js
if (effects.HasTag("fire")) {
    // At least one active Effect is tagged as fire.
}
```

If you need the matching Effect references themselves:

```js
var _fire_effects = effects.GetEffectsTagged("fire");
```

or, if a cleanse should remove every matching Effect:

```js
effects.RemoveEffectsTagged("fire", "cleansed");
```

That call finds every active Effect carrying the `"fire"` tag and removes each one. The Modifiers and Flows owned by those Effects are removed with them. `"cleansed"` is simply a user-provided reason for the removal.

### Why use a tag instead of the Effect identity?

The Effect's identity is its stable name for **which Effect this is**:

```js
"burn"
"poison_cloud"
"flame_aura"
```

A tag can describe something several different Effects have in common:

```js
"fire"
"debuff"
"poison"
```

If your antidote should remove several different poison Effects, asking for the `"poison"` tag is much more useful than writing special-case checks for every Effect identity your game might contain.

### Finding Effects by identity

You don't have to keep the exact Effect reference just to find an active Effect later. If gameplay only knows the authored identity, the manager can search by that identity:

```js
if (effects.HasEffectIdentity("burn")) {
    var _burns = effects.GetEffectsByIdentity("burn");
}
```

`GetEffectsByIdentity()` returns an array because Catalyst allows several active Effects to share the same identity by default. The reapplication section later on this page shows how to change that behaviour.

You can remove every active copy with that identity as well:

```js
effects.RemoveEffectsByIdentity("burn", "cleansed");
```

Use the exact Effect reference when you mean one particular active object. Use identity lookup when the game means “the active Effect or Effects called `burn`.”

### Grouping related Effects with a family

An Effect can also carry one **family** value:

```js
var _burn = new CatalystEffect("burn", 5)
    .SetFamily("damage_over_time");

var _bleed = new CatalystEffect("bleed", 8)
    .SetFamily("damage_over_time");

effects.AddEffect(_burn);
effects.AddEffect(_bleed);

var _damage_over_time = effects.GetEffectsByFamily("damage_over_time");
```

An Effect family is just a stable grouping value for lookup. It doesn't decide what happens when the same Effect is applied again, and it doesn't make Effects compete with one another. Those rules use the Effect's **identity**.

This is also separate from the Modifier families covered later in the advanced Statistics guide. Modifier families choose which related numerical contribution wins during a Statistic calculation. Effect families simply let you find related active Effects.

Tags and families overlap a little, but they suit different shapes. An Effect can carry several tags such as `"debuff"`, `"fire"`, and `"damage_over_time"`, while it has at most one family value. Use whichever matches how your game wants to classify its Effects.

---

## Damage over time with an Effect-owned Flow

Now we can build the burning example that motivated our discussion on Effects in the first place.

Suppose burning should last five seconds and deal 4 HP per second. The shared tracker is already using delta-time timing from the first example. We obviously need an HP Resource this Effect will change (this is almost certainly already setup on your target if you're taking advantage of Catalyst properly):

```js
hp = new CatalystResource(100);
```

Then build and submit the burn:

```js
var _burn = new CatalystEffect("burn", 5)
    .AddTag("debuff")
    .AddTag("fire")
    .SetTickInterval(1);

_burn.AddFlow(
    hp,
    new CatalystResourceFlow(-4, "Burn")
);

effects.AddEffect(_burn);
```

An Effect-owned Flow is attached differently from the standalone Flows in the previous guide.

With a standalone Flow, you create the Flow and attach it directly to its Resource:

```js
var _drain = new CatalystResourceFlow(-4, "Burn");
hp.AddFlow(_drain);
```

and the Flow's own countdown tracker advances it directly.

With an Effect-owned Flow, the detached Effect receives the target Resource and the Flow together. In the burn setup above, `_burn.AddFlow(hp, new CatalystResourceFlow(-4, "Burn"))` does that before `effects.AddEffect(_burn)` is called.

The first argument tells the Effect which Resource the Flow should affect, while the second supplies the Flow itself. Just like `AddModifier()`, adding the Flow doesn't change the live game yet. If the Effect is successfully applied, Catalyst attaches the Flow to `hp`, and from then on the burn Effect decides when that Flow is allowed to move the Resource.

You **shouldn't also call `hp.AddFlow()`** on that Flow. It's no longer a standalone Flow because it belongs to `_burn`. You also can't add new Flow or Modifier payloads after an Effect has become active, so finish building its owned changes before calling `AddEffect()`.

### Why the tick interval is necessary

The `.SetTickInterval(1)` in the burn constructor is necessary because a standalone Flow already knows how to move over time, while a Flow inside an Effect only moves when one of the Effect's ticks completes. The Effect therefore needs a positive tick interval.

`SetTickInterval(1)` means one Effect tick completes for every `1` countdown unit that passes. With delta-time timing, that's one tick per second.

During that interval, the burn Flow accumulates the amount of time for which it's eligible to move. When the one-second interval completes, Catalyst evaluates the Flow's rate and applies:

```text
rate:              -4 HP per second
eligible time:      1 second
requested movement: -4 HP
```

so HP drops by 4.

After another complete second, another tick finishes and another 4 HP is requested. Because the Effect lasts five seconds, the ordinary case gives us five one-second burn ticks before the Effect expires.

If you changed the tick interval to `0.5`, the same Flow rate would request `-2` HP on each half-second tick:

```text
-4 * 0.5 = -2 HP
```

The Flow's rate still means “HP per countdown unit,” while the Effect's tick interval decides how often that accumulated movement is actually applied.

> Effect-owned Flows only move through completed Effect ticks. If an Effect owns a Flow but has no positive tick interval, that Flow won't move the Resource.

{: .warning}

### Incomplete final ticks aren't applied

Suppose an Effect has one second of duration remaining but a two-second tick interval. One second passes, the Effect expires, but a full two-second interval never completed.

Catalyst doesn't invent a partial final tick just because the Effect is ending. The Effect expires without applying that unfinished interval.

That behaviour fits discrete rules such as “poison deals damage every two seconds”: a one-second poison shouldn't deal half of a two-second tick on expiry unless you explicitly model that behaviour yourself.

---

## Flow delays still work inside Effects

Effect-owned Flows keep their ordinary active and delay behaviour. Suppose burn lasts five seconds, but its damage should wait one second before becoming eligible:

```js
var _burn_flow = new CatalystResourceFlow(-4, "Burn")
    .Delay(1);

var _burn = new CatalystEffect("burn", 5)
    .SetTickInterval(1)
    .AddFlow(hp, _burn_flow);

effects.AddEffect(_burn);
```

During each Effect interval, Catalyst offers elapsed time to the Flow. The Flow consumes its delay first, exactly as it did when standalone, and only the time left over becomes eligible movement for that tick.

If an interval contains `0.75` seconds of remaining delay and then `0.25` seconds of eligible time, a `-4` Flow contributes:

```text
-4 * 0.25 = -1 HP
```

when that Effect tick resolves.

You don't need a second timer for “Effect tick timing” and “Flow delay timing” because the Flow's delay is consumed within the Effect's timeline.

---

## A complete burn Effect

A complete burn setup can now use all of those pieces together. The character owns an HP Resource, a defence Statistic and an Effect manager:

```js
hp = new CatalystResource(100);
defence = new CatalystStatistic(10);
effects = new CatalystEffectManager(self);
```

The global Catalyst tracker is using delta-time timing, so our Effect durations and rates are authored in seconds:

```js
CATALYST_COUNTDOWN.StartAutomatic(eCatCountdownMode.DELTA_TIME);
```

When the character is set on fire, we construct the Effect:

```js
var _burn = new CatalystEffect("burn", 5)
    .AddTag("debuff")
    .AddTag("fire")
    .SetTickInterval(1);

```

This creates a five-second Effect, labels it so other gameplay systems can recognise it as both a debuff and fire, and gives it one-second ticks.

Next we give the Effect its damage Flow:

```js
_burn.AddFlow(
    hp,
    new CatalystResourceFlow(-4, "Burn")
);
```

The Flow isn't attached to `hp` yet. `_burn` remembers that this Flow should affect `hp`, but if the Effect never becomes active, the Flow never starts changing HP.

We can also give the Effect a defence penalty if burning should make the character easier to hurt:

```js
_burn.AddModifier(
    defence,
    new CatalystModifier(-3, eCatMathOps.ADD)
        .SetLayer(eCatStatLayer.TEMP)
);
```

Finally, submit the finished Effect:

```js
var _application = effects.AddEffect(_burn);
```

If application succeeds, the defence penalty attaches immediately and the Effect begins counting down. Each completed one-second tick lets the burn Flow request `-4` HP, and when the fifth second completes, Catalyst resolves that final complete tick before expiring the Effect. Expiry then removes the Effect and destroys both the HP Flow and defence Modifier it owned.

A cleanse doesn't need to know about either individual change:

```js
effects.RemoveEffectsTagged("fire", "cleansed");
```

The cleanse removes the Effect, and the Effect removes its own consequences.

Gameplay code can now reason about **burning** as one thing instead of separately coordinating every numeric consequence burning happens to create.

---

## Running code when an Effect starts

Sometimes applying an Effect needs to do something that isn't naturally a Modifier or Flow. You might want to start an animation, spawn a visual effect, or tell another gameplay system that rage has begun.

Use `SetOnApply()` for that:

```js
var _rage = new CatalystEffect("rage", 5)
    .SetOnApply(function() {
        show_debug_message("Rage started on " + string(owner));
    });

effects.AddEffect(_rage);
```

`SetOnApply()` stores the function on the Effect. Catalyst doesn't call it while you're building the Effect. `effects.AddEffect(_rage)` submits it, and the callback runs only after the Effect has successfully become active and its Modifiers and Flows have been attached.

Catalyst runs the function as part of the Effect, so fields such as `owner`, `manager`, `identity` and `duration` inside the callback refer to the active Effect's own data. In this example, `owner` is the value that was originally passed to `new CatalystEffectManager(...)`.

The callback's return value is ignored. Its job is to perform whatever side effect your game needs after successful application.

### Why not put everything in `OnApply()`?

You could manually add Modifiers and Flows from an `OnApply()` callback, but then Catalyst wouldn't automatically know that those pieces belong to the Effect. You'd also have to remove them yourself later.

Use `AddModifier()` and `AddFlow()` for changes whose lifetime belongs to the Effect, then reserve `OnApply()` for work that doesn't already have a built-in Catalyst representation.

---

## Running code when an Effect ends

`SetOnRemove()` gives you the other side of the lifecycle. If your game plans to remove this exact Effect later, keep its active reference somewhere persistent:

```js
removable_rage = new CatalystEffect("removable_rage", 5)
    .SetOnRemove(function(_reason) {
        show_debug_message("Rage ended: " + string(_reason));
    });

effects.AddEffect(removable_rage);
```

The callback receives the reason used to remove the Effect. Natural expiry uses `"expired"`, while an explicit call can supply whatever reason is useful to your game:

```js
effects.RemoveEffect(removable_rage, "dispelled");
```

By the time `OnRemove()` runs, the Effect has already left the manager's active list and Catalyst has destroyed the Modifiers and Flows it owned. The Effect's `owner` and `manager` are still available during the callback. Afterward, those links are cleared and the Effect itself is destroyed.

So `OnRemove()` is a good place to react to the Effect ending, but its numerical changes have already been removed.

---

## Changing and refreshing duration

For a duration example, start with an Effect that's still active:

```js
duration_rage = new CatalystEffect("duration_rage", 5);
effects.AddEffect(duration_rage);
```

You can then change its duration with `SetDuration()`:

```js
duration_rage.SetDuration(8);
```

For an active timed Effect, Catalyst updates both its remaining duration and the duration it considers the Effect's current maximum. If the Effect is on a valid countdown tracker, it remains registered for countdown using the new value.

Calling:

```js
duration_rage.ResetDuration();
```

restores the remaining duration to that most recently assigned maximum. Code that already owns the exact active Effect can use this to restart its timer directly. The next section covers manager-level reapplication, where a new incoming Effect can refresh an existing one by identity.

The sign of the duration has the same meaning as it did in the constructor:

```text
positive duration -> timed Effect
zero              -> already expired / remove an active Effect
negative duration -> permanent Effect
```

If you call `SetDuration(0)` on an active Effect, the Effect asks its manager to remove it with the reason `"expired"` rather than leaving a zero-duration Effect active.

A permanent Effect doesn't expire, but it can still be removed explicitly through its manager. If it has a positive tick interval, it can also keep resolving ticks while it remains active. That makes permanent Effects useful when a persistent status owns periodic behaviour as well as tags or Modifiers.

---

## What happens when the same Effect is applied again

By default, Effects use `eCatEffectReapplyPolicy.STACK`. Two active Effects can therefore share an identity and exist at the same time.

Sometimes that isn't the rule you want. A poison might refresh its timer when applied again, or a stance might ignore another copy while it's already active. Give each incoming Effect the same stable identity and reapplication policy. For a refreshing poison:

```js
var _first_poison = new CatalystEffect("poison", 6)
    .SetReapplyPolicy(eCatEffectReapplyPolicy.REFRESH);

effects.AddEffect(_first_poison);

// Reapplying poison means submitting a new incoming Effect with the same identity.
var _incoming_poison = new CatalystEffect("poison", 6)
    .SetReapplyPolicy(eCatEffectReapplyPolicy.REFRESH);

var _reapplication = effects.AddEffect(_incoming_poison);
```

Catalyst reads the policy from the **incoming** Effect. Here it finds the already-active `"poison"`, resets that existing Effect to the incoming six-second duration, and leaves `_incoming_poison` detached. `_reapplication.Succeeded()` is true because the refresh succeeded, while `_reapplication.Applied()` is false because the incoming Effect itself did not become active.

Don't submit `_first_poison` again while it's active. An Effect already owned by a manager isn't a valid incoming Effect, so reapplication is represented by constructing another Effect that describes the new application attempt.

The available policies are:

```js
eCatEffectReapplyPolicy.STACK
eCatEffectReapplyPolicy.IGNORE
eCatEffectReapplyPolicy.REPLACE
eCatEffectReapplyPolicy.REFRESH
eCatEffectReapplyPolicy.EXTEND
```

`STACK` adds the incoming Effect as another active copy.

`IGNORE` leaves the existing Effect alone.

`REPLACE` removes the existing Effect and applies the incoming one.

`REFRESH` keeps the existing Effect but resets its duration.

`EXTEND` keeps the existing Effect and adds the incoming duration to it.

Every non-`STACK` policy needs a stable Effect identity because Catalyst needs a name it can use to find the already-active Effect that the new one should refresh, ignore, replace, or extend.

Application chance (which we will touch on in a bit) is resolved before the reapplication rule. An incoming Effect that fails its chance doesn't refresh, replace, extend, or otherwise alter the existing Effect.

With `IGNORE`, `REFRESH`, or `EXTEND`, the incoming Effect doesn't become the active Effect. The existing one stays active, and the application result tells you which Effect ended up active after the attempt.

---

## Using a different countdown tracker

Timed Effects use `CATALYST_COUNTDOWN` by default, so they follow the same frame, delta-time, pause and time-scale settings you learned about with Resource Flows. If an Effect belongs to a different timing domain, create or reuse a tracker for that domain and assign it to the Effect itself:

```js
combat_countdown = new CatalystCountdownTracker();

var _poison = new CatalystEffect("poison", 4)
    .SetCountdownTracker(combat_countdown)
    .SetTickInterval(1);

effects.AddEffect(_poison);
```

A new custom tracker starts in manual mode. Once the Effect is active, it follows `combat_countdown`. Any Modifiers or Flows it owns follow the Effect's timing too, so you don't assign a tracker to each owned change separately.

If `combat_countdown` is manual, the Effect advances whenever your game calls:

```js
combat_countdown.Countdown(1);
```

Passing `noone` to `SetCountdownTracker()` disables automatic countdown for that Effect. A positive duration then stays where it is until you assign another tracker or remove the Effect, which can be useful when some other game rule deliberately controls whether its timer is allowed to advance.

---

## Application chance

Every Effect begins with an application chance of `1`, meaning 100%, so the Effects above all applied successfully.

Suppose a stun should have only a 35% chance to take hold:

```js
var _stun = new CatalystEffect("stun", 2)
    .AddTag("debuff")
    .AddTag("stun")
    .SetChanceToApply(0.35);

var _application = effects.AddEffect(_stun);
```

`SetChanceToApply(0.35)` changes the Statistic Catalyst uses when the manager evaluates whether the Effect should apply. The value is interpreted between `0` and `1`, so `0.35` represents a 35% chance.

When `AddEffect()` is called, the manager checks that chance before changing any Statistics or Resources. If the chance succeeds, the Effect becomes active and its Modifiers and Flows are attached. If it fails, the Effect stays inactive and none of those changes happen.

The returned application result tells you what happened:

```js
if (_application.Applied()) {
    // The incoming Effect became active.
}
else {
    show_debug_message(_application.GetOutcome());
}
```

`Applied()` answers the simple question “did this incoming Effect itself become active?” `Succeeded()` is slightly broader: a `REFRESH`, `EXTEND`, or `IGNORE` reapplication can succeed by doing the requested thing to an Effect that was already active, even though the incoming Effect was never added.

The result also exposes `GetEffect()` for whichever Effect is active after the attempt, `GetChance()` for the chance Catalyst used, and `GetRoll()` when a random roll was required.

### The application chance is itself a Statistic

Application chance follows the same pattern as Resource bounds and Flow rates: Catalyst uses a Statistic when a number might need the rest of the Statistic system later.

Before an Effect is submitted, you can retrieve its chance Statistic with:

```js
var _stun = new CatalystEffect("stun", 2)
    .SetChanceToApply(0.35);

var _chance = _stun.GetChanceToApplyStatistic();
```

Modifiers, conditions and facts can affect application chance too.

If your game already has a Statistic that should decide the chance, let the Effect use that same Statistic before you submit it. For example, suppose stun chance is a character stat that other systems can also modify:

```js
stun_chance = new CatalystStatistic(0.35);

var _stun = new CatalystEffect("stun", 2)
    .BindChanceToApplyStatistic(stun_chance);

var _application = effects.AddEffect(_stun);
```

The application attempt evaluates that exact `stun_chance` Statistic. Because it's your external Statistic, Catalyst doesn't replace its own configuration with the Effect's usual zero-to-one clamping. If your shared chance stat must stay inside that range, configure the Statistic itself accordingly.

> This can get absurd when you start really thinking about things in terms of Statistics. You could have a `dexterity` Statistic, which is itself based on a function that combines existing `speed` and `agility` Statistics, with post-processing applied to shape result of the `dexterity` output, with your `stun_chance` being built from that shaped `dexterity` output, with it's own modifiers, shaping, effects, etc applied to it. This is a somewhat arbitrary example, but I want to encourage you to start thinking about how all these things can layer together to build highly complex game design rules from very simple Catalyst primitives. Now back to your scheduled documentation
{: .note}

While an Effect is using a shared chance Statistic, `SetChanceToApply()` is rejected rather than silently replacing it. If a detached Effect should go back to owning its own chance before you submit it, make that change explicitly:

```js
var _stun = new CatalystEffect("stun", 2)
    .BindChanceToApplyStatistic(stun_chance);

_stun.UnbindChanceToApplyStatistic();
_stun.SetChanceToApply(0.5);
```

`UnbindChanceToApplyStatistic()` stops sharing the external Statistic and gives the Effect a new chance Statistic starting from the value the shared one currently calculates.

### Reusing one-off situational evaluation

Earlier we used `Evaluate(_query)` when a Statistic needed a one-off answer such as “what would this be against a frozen target?” Effect application can use the same idea.

If the application-chance Statistic contains situational rules, pass a query to `AddEffect()`. Here frozen targets add another 25 percentage points to a 35% base chance:

```js
var _frost_stun = new CatalystEffect("frost_stun", 2)
    .SetChanceToApply(0.35);

_frost_stun.GetChanceToApplyStatistic()
    .SetFactView(combat_fact_view)
    .AddModifier(
        new CatalystModifier(0.25, eCatMathOps.ADD)
            .SetCondition(function(_stat, _facts) {
                return _facts.GetFrom("target", "frozen") ?? false;
            })
    );

var _query = new OracleFactQuery()
    .SetFrom("target", "frozen", true);

var _application = effects.AddEffect(_frost_stun, _query);
```

For this attempt, the query temporarily treats the `"frozen"` fact in the `"target"` part of the combat Fact View as `true`, so the application chance evaluates to `0.60`. The query is only used for this application calculation and isn't stored on the Effect or its Statistic.

When a query is supplied, the manager evaluates application chance with `Evaluate(_query)`. Without one, it uses the chance Statistic's ordinary `GetValue()`. Just like the prior encounter we had with Oracle Facts, `GetValue()` already takes into account the Fact View you have given the Statistic. Adding a query just overlays the query Facts on top of the existing Fact View. You could calculate the chance yourself before calling `AddEffect()`, but that would remove a lot of the usefulness of Oracle.

---

## Chance on each Effect tick

Application chance answers one question:

> Does this Effect become active at all?

Sometimes the Effect should definitely become active, but each completed tick should have its own chance to do anything. A poison might last for ten seconds while having a 50% chance to deal damage on each one-second tick.

Use `SetChancePerTick()` for that:

```js
poison_effect = new CatalystEffect("poison", 10)
    .AddTag("debuff")
    .AddTag("poison")
    .SetTickInterval(1)
    .SetChancePerTick(0.5);
    .AddFlow(
        hp,
        new CatalystResourceFlow(-6, "Poison")

    );

effects.AddEffect(poison_effect);
```

`poison_effect` is kept as a persistent reference because the next examples continue configuring and observing this active Effect.

The Effect itself applies normally because we haven't changed its application chance. Once active, each completed one-second tick checks the per-tick chance.

If a tick succeeds, Catalyst applies the Effect-owned Flow movement for that tick. If it fails, the Flow doesn't move HP during that tick, but the Effect remains active and its duration continues counting down.

An Effect's own per-tick chance is a Statistic that starts at `1` and is clamped from `0` to `1`. You can modify that Statistic directly, or let the Effect use a chance Statistic your game already owns. A bound external Statistic keeps its own configuration rather than inheriting the Effect's clamping. For example:

```js
poison_tick_chance = new CatalystStatistic(0.5);
poison_effect.BindChancePerTickStatistic(poison_tick_chance);

var _chance_stat = poison_effect.GetChancePerTickStatistic();
```

As with application chance, `SetChancePerTick()` won't silently stop using a shared Statistic. Call `UnbindChancePerTickStatistic()` first if you want the Effect to go back to owning its own per-tick chance.

Use application chance when the uncertainty is **whether the Effect takes hold**. Use per-tick chance when the Effect is already active and the uncertainty is **whether this particular tick succeeds**.

---

## Controlling Effect randomness

By default, an Effect Manager uses GameMaker's normal `random(1)` behaviour for application and per-tick chance rolls.

For tests, deterministic replays, or a game-wide RNG system, you can supply the manager's random source yourself:

```js
effects.SetRandomFunction(function() {
    return 0.25;
});
```

The function above makes every test roll `0.25`. In a real project, it can call whatever seeded or replayable RNG your game already uses. Catalyst calls the zero-argument function whenever this manager needs an Effect chance roll, and compares the returned value with the Effect's zero-to-one chance.

The random source belongs to the manager so every Effect on the same gameplay owner can use the same one.

Return to GameMaker's default random source with:

```js
effects.ClearRandomFunction();
```

You don't need to replace the random source just to use Effect chances. This exists for when your project already has a reason to control randomness, or to allow you to set arbitrary values for testing purposes.

---

## Running code after each Effect tick

If you need code to run after each completed Effect tick, use `SetOnTick()`:

```js
poison_effect.SetOnTick(function(_tick_duration, _result) {
    show_debug_message(
        "Poison tick success: "
        + string(_result.Succeeded())
    );
});
```

Catalyst runs this callback as a method of the Effect. The first argument tells you how much countdown that completed tick represented, while the second is a `CatalystEffectTickResult` describing what happened.

The result struct gives you:

```text
Succeeded()       whether the tick ultimately succeeded
GetChance()       evaluated per-tick chance
GetRoll()         random roll, when one was needed
ChanceSucceeded() whether the ordinary chance roll succeeded
GetMultiplier()   multiplier used for owned Flow movement
GetFlowResults()  concrete results from Flow movements
```

`OnTick()` runs after Flow movement for successful ticks, and it also runs for ticks that failed their per-tick chance, so it can observe the outcome either way.

If you only want “do something when poison successfully damages the target,” check `_result.Succeeded()` rather than assuming every `OnTick()` call represents successful movement.

---

## Changing a tick before its Flows move

Most Effects won't need to customise what happens inside a tick. A tick interval, per-tick chance, and one or more Flows already cover a large number of periodic gameplay rules.

When you genuinely need to change the tick after its normal chance roll but before its Flows move, `SetResolveTick()` gives you that hook. Suppose the object that owns the Effect manager has a `poison_immunity` flag:

```js
poison_effect.SetResolveTick(function(_tick_duration, _result) {
    if (owner.poison_immunity) {
        _result.SetSucceeded(false);
    }
});

```

Catalyst calls `ResolveTick` after it has performed the ordinary per-tick chance roll but **before** any eligible Effect-owned Flows move their Resources. The callback receives the same result struct that will later be passed to `OnTick()`.

Changing:

```js
_result.SetSucceeded(false);
```

prevents the owned Flow movement for that tick, even if the ordinary chance roll succeeded.

You can also scale every owned Flow's movement for the tick:

```js
poison_effect.SetResolveTick(function(_tick_duration, _result) {
    _result.SetMultiplier(0.5);
});
```

A Flow that would normally request `-6` HP for the completed interval now requests `-3` instead.

If the rule can already be expressed with a Flow rate Statistic, a condition, Oracle facts, or the Effect's per-tick chance, prefer those pieces: they make the rule visible in the same Catalyst model as everything else. `ResolveTick()` is for the cases where the tick really does need custom code before its Flows move.

---

## Watching Effects enter and leave a manager

A manager can also notify code that cares about its overall active-Effect list, like the UI, debugging, audio-visual systems, etc, that should react to any Effect rather than one specific Effect's own callbacks (or even something like "a buff that makes any removal of a dispell tagged effect heal the player").

```js
effect_applied_subscription = effects.OnEffectApplied(
    function(_manager, _effect, _application) {
        // Update status UI, play a generic cue, and so on.
    }
);

effect_removed_subscription = effects.OnEffectRemoved(
    function(_manager, _effect, _reason) {
        // Respond to any Effect leaving this manager.
    }
);
```

`OnEffectApplied()` only runs when an Effect actually becomes active. A successful `REFRESH`, `EXTEND`, or `IGNORE` reapplication doesn't pretend the incoming Effect was newly applied.

Combining this with [Pulse]({{ '/pulse/' | relative_url }}) can be a powerful driver of game-wide reactions to things.

Both calls return `CatalystSubscription` handles, so the observer can be removed later:

```js
effect_applied_subscription.Unsubscribe();
effect_removed_subscription.Unsubscribe();
```

Use an Effect's own `SetOnApply()` / `SetOnRemove()` when the behaviour belongs to that Effect. Use manager subscriptions when another system wants to observe the manager as a whole.

### Adding or removing another Effect from a callback

An Effect callback can cause another Effect to be added or removed. If the manager is already partway through an Effect change, Catalyst accepts the nested request and finishes it after the current change is complete rather than modifying the active list halfway through the callback.

For `AddEffect()`, the returned result tells you when that happened. Here one Effect applies another from its `OnApply()` callback:

```js
var _trigger = new CatalystEffect("trigger", 1)
    .SetOnApply(function() {
        var _aftershock = new CatalystEffect("aftershock", 2);
        var _result = manager.AddEffect(_aftershock);

        if (_result.Queued()) {
            // Accepted, but it won't become active until this application finishes.
        }
    });

effects.AddEffect(_trigger);
```

Inside an Effect callback, `manager` is the Effect's own manager, as shown earlier on this page. The aftershock request is queued because the manager is still finishing `_trigger`'s application.

A queued application isn't reported as `Succeeded()` yet because the actual chance and reapplication rules haven't run. Code inside the callback shouldn't assume the new Effect is already active just because the request was accepted.

`RemoveEffect()` similarly returns `true` when an exact removal happened immediately **or** was accepted to run after the current Effect change. In ordinary gameplay code this distinction rarely matters, but it matters inside lifecycle callbacks if you were about to inspect the manager again and expected the active list to have changed already.

---

## Cleaning up an Effect manager

When the object that owns an Effect manager is being torn down, destroy the manager:

```js
effects.Destroy();
delete effects;
```

The manager removes all of its active Effects and destroys the Modifiers and Flows those Effects own. Effects removed this way receive the removal reason `"manager_destroyed"` in `OnRemove()`.

> See the note under [Removing and destroying Flows](resource-flows#removing-and-destroying-flows) for more info on the `delete` keyword.
{: .note}

---

## Effect ownership at a glance

A `CatalystEffectManager` keeps track of the Effects currently active on one owner. A `CatalystEffect` represents one gameplay state with a shared lifetime. You give it its Modifiers and Flows while building it, and those changes only become live if `AddEffect()` succeeds.

Once a Modifier or Flow belongs to an Effect, it follows that Effect's lifetime and timing. Removing or expiring the Effect destroys those changes together, while tags let other systems work with broad categories such as `"fire"`, `"poison"`, or `"debuff"` without knowing every exact Effect name.

For periodic Effects, a positive tick interval is what makes Effect-owned Flows eligible to move. Application chance decides whether the Effect becomes active, while per-tick chance decides whether an individual completed tick succeeds. Callbacks are there when your game needs work that the existing Catalyst pieces don't already express.

---

## Next: Sets and previews

Effects solve the problem of several changes sharing one gameplay lifetime. The next guide moves to a different problem: several Catalyst objects belonging to one gameplay model (like a character), plus reusable packages of Modifiers that need to be previewed or swapped together.

Continue with **[Sets & Previews](sets-and-previews)** to build a character Set and answer questions such as “what would these stats look like if I equipped this item?” without changing the live build.