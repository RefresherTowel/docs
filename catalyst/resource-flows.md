---
layout: default
title: Resource Flows
parent: Catalyst
nav_order: 4
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Resource Flows

The Resource methods you've used until now all respond to explicit gameplay calls: an attack calls `Decrease()`, a healing item calls `Increase()`, or a reset calls `SetCurrent()`.

Some values need to keep moving while a rule remains active. Stamina might regenerate every frame, heat might steadily cool down, hunger might drain once per turn, or a shield might begin recovering two seconds after it was broken.

You could update those values yourself every frame or turn, but then each system also needs to remember its rate, delay, pause state, and timing rules. Catalyst represents that ongoing movement with a `CatalystResourceFlow`.

---

## Your first Flow

Suppose the player has 40 stamina out of a possible 100, and we want it to regenerate while the game runs:

```js
stamina = new CatalystResource(100, 40);
stamina_regen = new CatalystResourceFlow(0.5);

stamina.AddFlow(stamina_regen);
```

There are two new actions here.

First, `new CatalystResourceFlow(0.5)` creates a Flow whose **rate** is positive `0.5`. A positive rate means the Resource moves upward, while a negative rate moves it downward.

Second, `stamina.AddFlow(stamina_regen)` tells the Flow which Resource it should move. Until a Flow is attached to a Resource, it has nothing to change. Once attached, its countdown tracker can advance it automatically.

Catalyst's global countdown tracker starts in **frame mode** by default, which means it advances by one countdown unit each frame. With the setup above, one frame of countdown produces:

```text
flow rate:        +0.5
countdown amount:  1
requested change: +0.5
```

Catalyst multiplies the Flow's rate by the amount of countdown that passed, then applies that signed amount through the Resource's normal `Change()` method. After one frame, stamina moves from `40` to `40.5`. After another, it moves to `41`, and so on.

The Resource still owns its bounds. If regeneration reaches 100, later positive Flow movement is simply clamped at the maximum in exactly the same way as an explicit `Increase()` call would be.

> A Flow describes a **rate**, not a one-off change. The rate only starts affecting a Resource after you attach the Flow with `AddFlow()`.
{: .note}

---

## Using seconds instead of frames

Frame-based rates are useful for some games, but a real-time stamina system will usually be easier to author in units per second. If you want “regenerate 12 stamina per second,” you don't want to calculate a per-frame rate yourself.

Tell the global Catalyst countdown tracker to use delta time instead:

```js
CATALYST_COUNTDOWN.StartAutomatic(eCatCountdownMode.DELTA_TIME);
```

You'd normally choose this once during game setup rather than whenever you create a Flow. The tracker still advances once per frame in delta-time mode, but each step uses the elapsed time for that frame in **seconds**.

Now the stamina Flow can be authored directly as 12 stamina per second:

```js
stamina = new CatalystResource(100, 40);
stamina_regen = new CatalystResourceFlow(12);

stamina.AddFlow(stamina_regen);
```

If one frame represents `0.016` seconds, Catalyst calculates approximately:

```text
flow rate:        +12 per second
countdown amount:  0.016 seconds
requested change: +0.192
```

A slower frame might contribute a larger amount and a faster frame a smaller amount, but the rate itself stays `12` per second.

Nothing about the Flow changed when we switched timing modes. The Flow still says “move at +12 per countdown unit.” We changed what one countdown unit means for the tracker advancing it.

The same Flow works in frame-based, real-time, and turn-based games. Only the meaning of one countdown unit changes.

---

## Draining a Resource

A negative Flow rate moves the Resource downward, so a drain uses the same class as regeneration:

```js
oxygen = new CatalystResource(100);
oxygen_drain = new CatalystResourceFlow(-4);

oxygen.AddFlow(oxygen_drain);
```

If the global tracker is using delta time, this removes four oxygen per second. Catalyst evaluates the rate, multiplies it by the elapsed countdown amount, then passes the resulting negative value to `oxygen.Change()`.

There's no separate “regeneration Flow” and “drain Flow” because the sign already expresses the direction:

```text
positive rate -> Resource rises
negative rate -> Resource falls
zero rate     -> Resource doesn't move
```

This is more similar to the `Change()` method on Resources, as compared to the `Increase()` and `Decrease()` methods. Those methods accept positive magnitudes because your gameplay code already knows whether it's healing or damaging the Resource. A Flow describes mathematical movement over time, so its rate stays signed.

---

## Delaying a Flow

Now suppose stamina shouldn't start regenerating immediately after the player spends it. We want a two-second wait, then regeneration should resume.

Assuming the countdown tracker is using delta time, you would call once this when the player running:

```js
stamina_regen.Delay(2);
```

`Delay()` doesn't create another timer beside the Flow. It stores an amount of countdown that the Flow must consume before any of that countdown is allowed to move the Resource.

Suppose `1.4` seconds of countdown have passed since we called `Delay(2)`. Catalyst has consumed `1.4` seconds of the delay, leaving:

```text
remaining delay: 0.6 seconds
eligible flow time: 0 seconds
```

The Resource hasn't regenerated yet.

Now suppose the next countdown step is `0.8` seconds. Only `0.6` seconds are needed to finish the delay, so the remaining `0.2` seconds are still eligible for regeneration during that same step:

```text
incoming countdown: 0.8 seconds
delay consumed:      0.6 seconds
flow time remaining: 0.2 seconds
```

With a regeneration rate of `12`, Catalyst requests:

```text
12 * 0.2 = +2.4 stamina
```

In other words, the Flow doesn't throw away time just because a delay ended partway through a frame.

### Restarting the delay

Calling `Delay()` replaces the Flow's remaining delay rather than adding more time onto whatever was already there.

For a stamina system, you can restart the recovery wait whenever stamina is spent:

```js
var _spent = stamina.Decrease(25);

if (_spent.DidChange()) {
    stamina_regen.Delay(2);
}
```

If one second remained from an earlier delay, `Delay(2)` puts it back at two seconds, matching rules such as “regeneration starts two seconds after the most recent stamina use.”

You can inspect or control that delay directly when needed:

```js
stamina_regen.IsDelayed();          // true while delay remains
stamina_regen.GetDelayRemaining();  // current remaining amount
stamina_regen.ClearDelay();         // begin flowing immediately
```

The units are always the units used by the Flow's countdown tracker. In delta-time mode, `Delay(2)` means two seconds. In frame mode it means two frames, and under manual timing it means two of whatever countdown units your game advances.

---

## Temporarily disabling a Flow

Sometimes a gameplay rule might say the Flow shouldn't advance right now. A stamina regeneration Flow might stop while sprinting, for example:

```js
stamina_regen.SetActive(false);
```

While the Flow is inactive, Catalyst leaves it attached but doesn't consume its delay or move the Resource. Turn it back on with:

```js
stamina_regen.SetActive(true);
```

and check its current state with:

```js
if (stamina_regen.IsActive()) {
    // The Flow is currently advancing.
}
```

### Why not just remove the Flow?

You could call `stamina.RemoveFlow(stamina_regen)`, but that expresses a different situation. Removing a Flow detaches it from the Resource and from active countdown tracking. `SetActive(false)` says the Flow is still part of this Resource's setup and is simply paused.

For a sprinting rule, the regeneration Flow still belongs to stamina, so keeping it attached and toggling its active state is usually clearer. You would instead remove the Flow when that Flow is no considered a part of that Resource, for instance, perhaps when a heal-over-time spell ends.

An inactive Flow also doesn't count down its remaining delay. If regeneration has `1.2` seconds left when you disable it, it'll still have `1.2` seconds left when you enable it again.

Use `SetActive(false)` when you want to freeze the Flow where it is. Use `Delay()` when time should continue passing but the Resource shouldn't start moving until that waiting period has finished.

---

## A Flow's rate is a Statistic

The Flows we created above all started with a plain number:

```js
stamina_regen = new CatalystResourceFlow(12);
```

Internally, Catalyst turns that number into a `CatalystStatistic`. When the Flow advances, it calls `GetValue()` on that rate Statistic before calculating how far the Resource should move.

You can get that Statistic with `GetRateStatistic()`:

```js
var _regen_rate = stamina_regen.GetRateStatistic();
```

The Statistics and Modifiers you've already learned can control a Flow's rate too. Suppose a temporary buff should increase stamina regeneration by four per second:

```js
regen_boost = new CatalystModifier(4, eCatMathOps.ADD)
    .SetLayer(eCatStatLayer.TEMP);

stamina_regen.GetRateStatistic().AddModifier(regen_boost);
```

The Flow's base rate is 12, the Modifier adds 4, and the Flow now evaluates its rate as 16 whenever it advances. Remove the Modifier and the rate returns to 12:

```js
stamina_regen.GetRateStatistic().DestroyModifier(regen_boost);
```

There isn't a separate “modify regeneration” API because regeneration is already a number with the Catalyst Statistic rules attached to it.

If you need the rate to respond to the current situation, the same idea extends to the situational Statistics from the earlier guide. The rate Statistic can have conditions, stack functions and an Oracle fact view just like any other Statistic, and the Flow asks it for its current value when countdown advances.

### Using a rate Statistic the game already owns

Sometimes the regeneration rate already exists as a Statistic your game owns:

```js
stamina_regen_rate = new CatalystStatistic(12);
stamina_regen = new CatalystResourceFlow(stamina_regen_rate);

stamina.AddFlow(stamina_regen);
```

Because we supplied a `CatalystStatistic` instead of a number, the Flow uses that exact Statistic as its rate. If some other system modifies `stamina_regen_rate`, the Flow automatically uses the new calculated value the next time it advances.

You can also tell an existing Flow to use a different Statistic later. For example, if the game has a separate rested-regeneration stat:

```js
rested_regen_rate = new CatalystStatistic(20);
stamina_regen.BindRateStatistic(rested_regen_rate);
```

From then on, `stamina_regen` uses the current calculated value of `rested_regen_rate`.

### Why not just call `SetRate()`?

If the Flow owns its rate Statistic and the underlying rate changes from 12 to 15, `SetRate(15)` is appropriate:

```js
stamina_regen.SetRate(15);
```

If the Flow is currently using a Statistic supplied by your game, `SetRate()` is deliberately rejected. Otherwise the Flow could quietly stop using a Statistic that another system still expects to control. To give the Flow its own rate again, unbind first:

```js
stamina_regen.UnbindRateStatistic();
stamina_regen.SetRate(15);
```

`UnbindRateStatistic()` gives the Flow a new rate Statistic starting from the value the shared Statistic currently calculates. You should use an existing Statistic when other systems should keep controlling that same number, just as with Resource bounds. Use `SetRate()` when the rate belongs to the Flow itself.

---

## Knowing why a Flow changed a Resource

Resource changes can remember a reason, source, and extra metadata. A Flow can provide the same information for the changes it makes.

For a simple human-readable reason, start with the HP Resource the poison will change:

```js
hp = new CatalystResource(100);

poison_drain = new CatalystResourceFlow(-3)
    .SetSourceLabel("Poison");

hp.AddFlow(poison_drain);
```

Whenever that standalone Flow moves HP, Catalyst sends its source information through the Resource's normal change path. After a poison change, for example:

```js
var _change = hp.GetLastChange();

show_debug_message(_change.GetReason()); // "Poison"
```

You can also attach an arbitrary source handle and metadata when your game needs them. For example, a persistent trap object can be the source of this poison:

```js
poison_source = { name : "Swamp vent" };

poison_drain
    .SetSourceId(poison_source)
    .SetSourceMeta({damage_type : "poison"});
```

Those values don't change how the Flow behaves. They're copied into the Resource change result so other systems can identify where the movement came from. In a real project, `poison_source` could instead be the actual instance or struct that caused the poison.

As with explicit Resource mutations, there's no reason to add source metadata unless something in your game actually uses it. It's simply here so that you can package information your game wants about the Flow inside it.

---

## Removing and destroying Flows

If a standalone Flow should stop belonging to a Resource, remove it:

```js
var _removed = stamina.RemoveFlow(stamina_regen);
```

`RemoveFlow()` detaches the Flow and removes it from active tracking, but **doesn't destroy it**. The Flow keeps its assigned countdown tracker, rate, active state and remaining delay, so you can attach that same Flow again later:

```js
stamina.AddFlow(stamina_regen);
```

A standalone Flow can only be attached to one Resource at a time. If you want to move the exact Flow to another Resource, remove it from the first one before attaching it to the second.

If you're completely finished with the Flow, destroy it instead:

```js
stamina_regen.Destroy();
delete stamina_regen;
```

`Destroy()` detaches a standalone Flow from its Resource and countdown tracker.

Calling `delete` on `stamina_regen` releases the reference to the Flow stored in that variable. Once nothing else holds a reference to it, GameMaker's garbage collector can clean it up.

> `delete` is ordinary GameMaker struct lifetime behaviour rather than something Catalyst controls. In many cases references disappear naturally when locals go out of scope or instances are destroyed, so it is usually not necessary. See GameMaker’s delete documentation for the details [here](https://manual.gamemaker.io/lts/en/GameMaker_Language/GML_Overview/Language_Features/delete.htm).
{: .note}

The three common ways to stop a Flow have different meanings:

```text
SetActive(false)   keep it attached, but freeze it
RemoveFlow(flow)   detach it, but keep the Flow for later
flow.Destroy()     remove it completely
```

Choose the operation that matches whether the Flow is temporarily frozen, detached for possible reuse, or finished completely.

---

## A complete stamina regeneration setup

The complete stamina setup looks like this.

During game setup, we choose seconds as the global Catalyst time unit:

```js
CATALYST_COUNTDOWN.StartAutomatic(eCatCountdownMode.DELTA_TIME);
```

The player owns a stamina Resource and a regeneration Flow:

```js
stamina = new CatalystResource(100);
stamina_regen = new CatalystResourceFlow(15)
    .SetSourceLabel("Stamina regeneration");

stamina.AddFlow(stamina_regen);
```

The Flow regenerates 15 stamina per second. When the player spends stamina, the explicit gameplay action decreases the Resource and restarts a two-second regeneration delay:

```js
var _cost = stamina.Decrease(30, {
    reason : "sprint",
    source : self
});

if (_cost.DidChange()) {
    stamina_regen.Delay(2);
}
```

If sprinting should prevent even the delay from counting down, disable the Flow while sprinting:

```js
stamina_regen.SetActive(false);
```

and enable it when sprinting ends:

```js
stamina_regen.SetActive(true);
```

The remaining delay then continues from exactly where it was frozen. If sprinting should instead count toward the two-second wait, leave the Flow active and let `Delay()` handle the waiting period on its own.

A temporary regeneration buff can modify the Flow's rate without changing the stamina Resource itself:

```js
regen_boost = new CatalystModifier(5, eCatMathOps.ADD)
    .SetLayer(eCatStatLayer.TEMP);

stamina_regen.GetRateStatistic().AddModifier(regen_boost);
```

Now the same Flow regenerates 20 stamina per second until that Modifier is removed.

The Resource remembers how much stamina the player currently has, while the Flow says that stamina should keep moving over time. Its rate Statistic decides how fast, and the countdown tracker decides what passage of time Catalyst should count.

---

## When you need to control Catalyst's clock

The stamina setup above can use the global countdown tracker exactly as shown. The other timing controls come in when the game's clock itself needs special behaviour, such as pausing every timed Catalyst system together, applying slow motion, advancing time by turns, or separating two independent timing domains.

---

## Pausing all Catalyst countdown

`SetActive()` controls one Flow. Sometimes you want every timed Catalyst system on a tracker to stop together, such as when the game is paused.

The global tracker can be paused directly:

```js
CATALYST_COUNTDOWN.SetPaused(true);
```

While paused, calls that would advance that tracker do nothing, so standalone Flows assigned to it (or any other Catalyst features that might be attached to the countdown) don't consume delay or move their Resources. Resume with:

```js
CATALYST_COUNTDOWN.SetPaused(false);
```

Because the pause belongs to the tracker, every timed Catalyst system assigned to it stops advancing together.

You might be tempted to loop over every Resource Flow and call `SetActive(false)`, but that's usually the wrong level for a game pause. Individual Flow activity is gameplay state: “stamina regeneration is disabled while sprinting.” Tracker pause is time state: “Catalyst time isn't advancing while the game is paused.”

---

## Slowing or speeding up countdown

A tracker also has a time scale. Set it to `0.5` and each countdown step is halved before Catalyst advances its tracked systems:

```js
CATALYST_COUNTDOWN.SetTimeScale(0.5);
```

With the 15-stamina-per-second Flow from the complete example above, one real second now contributes only half a second of Catalyst countdown, so the Resource gains 7.5 stamina during that second.

Set it back to normal with:

```js
CATALYST_COUNTDOWN.SetTimeScale(1);
```

or inspect the current scale with:

```js
var _scale = CATALYST_COUNTDOWN.GetTimeScale();
```

A scale of `0` stops countdown movement, although `SetPaused(true)` is usually clearer when your intent is to explicitly pause the tracker.

---

## Manual timing

Not every game wants Catalyst to advance according to real time or frames. In a turn-based game, hunger might decrease once when the player ends a turn, regardless of how long they spent deciding what to do.

Stop the global tracker's automatic clock first:

```js
CATALYST_COUNTDOWN.StopAutomatic();
```

Now nothing on that tracker advances just because a frame passed. Your game decides when a countdown unit happens:

```js
hunger = new CatalystResource(100);
hunger_drain = new CatalystResourceFlow(-2);

hunger.AddFlow(hunger_drain);
```

At the end of each turn:

```js
CatalystCountdown(1);
```

`CatalystCountdown(1)` forwards one manual countdown unit to the global tracker. The Flow rate is `-2` per countdown unit, so hunger drops by 2 each time the game makes that call.

You can advance by other amounts if your rules need them:

```js
CatalystCountdown(0.5);
CatalystCountdown(3);
```

Catalyst doesn't decide what a manual unit means. It might represent one combat turn, one world tick, one hour of simulated travel, or any other unit your game uses consistently.

If you later call `StartAutomatic()` again, the global tracker returns to automatic frame or delta-time advancement depending on the mode you request.

---

## Separate timing with another tracker

Most games can use `CATALYST_COUNTDOWN` for everything, but sometimes two sets of timed rules genuinely need independent clocks. Perhaps combat continues in real time while a separate strategic simulation only advances when the player ends a turn.

A new `CatalystCountdownTracker` begins in manual mode:

```js
strategy_countdown = new CatalystCountdownTracker();
```

Create the Resource, then assign its Flow to that tracker before attaching it:

```js
food = new CatalystResource(100);

food_drain = new CatalystResourceFlow(-1)
    .SetCountdownTracker(strategy_countdown);

food.AddFlow(food_drain);
```

Now advancing the global tracker doesn't advance `food_drain`. The Flow belongs to `strategy_countdown`, so the strategic layer can move it independently:

```js
strategy_countdown.Countdown(1);
```

You can also start that custom tracker automatically if it represents a separate real-time domain:

```js
strategy_countdown.StartAutomatic(eCatCountdownMode.DELTA_TIME);
```

Use a custom tracker when two parts of the game are supposed to follow different clocks. Don't create one per Resource just for organisation. A tracker earns its place when several timed systems should pause, speed up, slow down, or advance together.

---

## Next: Effects

A Flow works well when one ongoing rule changes one Resource. Gameplay effects come in handy when you need to package several changes together: poison might drain HP, reduce movement speed, carry a `debuff` tag and disappear after five seconds, while a rage buff might raise damage and stamina regeneration for the same duration.

You could create and clean up each Modifier and Flow separately, but then your gameplay code has to keep their shared lifetime coordinated and you're balancing a bunch of different references that are really a part of one "thing". The next guide introduces **[Effects](effects)**, which let one gameplay effect own everything associated with that effect as one group and remove them together when the effect ends.
