---
layout: default
title: Time, Periods & Callbacks
parent: Sundial
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

# Time, Periods & Callbacks

The visual side of Sundial is continuous. Dusk doesn't suddenly snap on at 18:30 and replace Afternoon with a completely different colour. The grade is always moving smoothly through the cycle.

Gameplay often needs something more definite than that, though. For instance, street lights need a moment when they turn on, or shops might close at Night.

Sundial handles both ideas at once. The grading stays continuous, while the six time period nodes act as clear semantic **period** boundaries for your game logic.

---

## The six time periods

Sundial's public periods are:

```text
Morning
Day
Afternoon
Dusk
Night
Dawn
```

In code, those are referred to via the `eSundialPeriod` enum:

```js
eSundialPeriod.MORNING
eSundialPeriod.DAY
eSundialPeriod.AFTERNOON
eSundialPeriod.DUSK
eSundialPeriod.NIGHT
eSundialPeriod.DAWN
```

The timeline you create in the IDE is the same schedule `GetPeriod()` and the callback API use when your game is running.

In other words, if you put Dusk at 18:30 in the editor, then 18:30 is where Sundial starts reporting Dusk and where the Dusk callbacks fire.

---

## Reading the current period

Ask Sundial which period is active:

```js
switch (sundial.GetPeriod()) {
    case eSundialPeriod.DAY:
        // Day behaviour.
        break;

    case eSundialPeriod.NIGHT:
        // Night behaviour.
        break;
}
```

Use `GetPeriod()` for semantic game rules like this.

Sundial also exposes `GetPhase()` and `GetPhaseName()`, but phases are a different thing. Internally, Sundial uses a slightly more detailed resolver with phases such as Sunset, Twilight and Predawn to make the continuous visual transitions look good. You may find a use for them, but usually it's just easier to rely on the six basic periods.

If the question is "what part of the authored day is gameplay currently in?", use `GetPeriod()`.

If the question is "which part of Sundial's continuous visual resolver is currently dominant?", `GetPhase()` is the more specific answer.

---

## Running something when a period begins

Let's suppose, for examples sake, that the town's street lights should turn on when Dusk begins:

```js
sundial.OnDusk(function() {
    global.streetlights = true;
});
```

And then turn back off in the morning:

```js
sundial.OnMorning(function() {
    global.streetlights = false;
});
```

The convenience methods are:

```js
OnMorning()
OnDay()
OnAfternoon()
OnDusk()
OnNight()
OnDawn()
```

They're shorthand for the general form:

```js
sundial.OnPeriod(eSundialPeriod.DUSK, function() {
    global.streetlights = true;
});
```

Callbacks are additive, meaning that registering a second Dusk callback doesn't replace the first one:

```js
sundial.OnDusk(function() {
    global.streetlights = true;
});

sundial.OnDusk(function() {
    audio_play_sound(snd_evening_bells, 0, false);
});
```

Both of these will run, one after the other according to the order you added them, when Dusk begins.

If the preset was imported from the IDE, any callback authored in the Dusk Callback field is already registered as well. Adding extra callbacks through code will simply add more behaviour to the same period.

---

## Watching every period change

Sometimes you might want to have something that reacts any time *any* time period triggers.

In that case, use `OnPeriodChanged()`:

```js
sundial.OnPeriodChanged(function(_from, _to) {
    show_debug_message(
        "Sundial period changed from "
        + string(_from)
        + " to "
        + string(_to)
    );
});
```

The callback receives the old and new `eSundialPeriod` values.

This could be useful for systems like an ambient audio controller that reacts to the entire day schedule but still decides for itself what each transition should mean. It's really just there so you don't have to continuously fill out multiple `On*` methods for things that care about **all** the periods.

---

## Using Sundial's 24-hour clock

`SetTime()` and `GetTime()` use decimal hours:

```js
sundial.SetTime(6);      // 06:00
sundial.SetTime(13.5);   // 13:30
sundial.SetTime(23.75);  // 23:45
```

But you can read it back in whichever form is convenient:

```js
var _decimal_time = sundial.GetTime();
var _hour = sundial.GetHour();
var _minute = sundial.GetMinute();
```

The clock wraps around 24 hours, so values outside the normal range still land on a valid time.

Morning is Sundial's normalized `0/1` cycle seam. `SetMorningTime()` decides which 24-hour clock time that seam represents:

```js
sundial.SetMorningTime(6);
```

If you have set Morning to 06:00, then a normalized day position of `0.25` is 12:00, `0.5` is 18:00 and `0.75` is 00:00.

When you use the IDE, changing Morning's Time field configures this clock origin for you.

---

## Using normalized day time

If another system already works in a `0..1` day fraction, you don't have to convert it manually to hours, instead you can simply set Sundial to the percentage of your day:

```js
sundial.SetDayPercent(day_percent);
```

This is an alias for:

```js
sundial.SetTimeOfDay(day_percent);
```

Read the same value back with either:

```js
var _percent = sundial.GetDayPercent();
```

or:

```js
var _percent = sundial.GetTimeOfDay();
```

Values outside the range wrap around the cycle.

---

## Automatic time

Turn automatic time progression on with:

```js
sundial.SetAutoTime(true);
```

The easiest way to choose its speed is `SetDayLength()`:

```js
sundial.SetDayLength(900);
```

Now one complete game day takes 900 real seconds, or fifteen minutes.

You can read the setting back:

```js
var _seconds = sundial.GetDayLength();
```

If game-seconds-per-real-second is a more natural way to express your clock, use `SetSpeed()` instead:

```js
sundial.SetSpeed(120);
```

That advances the game clock by 120 seconds for every real second, so one real second is two game minutes.

Setting the speed to `0` pauses advancement without turning Auto Time off:

```js
sundial.SetSpeed(0);
```

`GetAutoTime()` still returns `true` in that case. All that happens is that the clock simply won't automatically move anymore until you give it a positive speed again.

---

## When to call Update

Automatic time is timestamp-driven, in other words, when `Draw()` runs, or when you ask Sundial a time-dependent question such as `GetTime()` or `GetPeriod()`, Sundial will synchronize the elapsed real time.

`sundial.Update()` is a way to manually force Sundial to synchronise its time (triggering callbacks that might need to be fired).

In general, you won't need to run this code. However, it exists for the cases where gameplay order matters. If some Step logic needs period callbacks to have fired *before* the rest of that logic runs, call `Update()` at the point where you want Sundial synchronized.

---

## Manual time skips vs automatic time

Suppose Sundial is currently in Morning and you do this:

```js
sundial.SetTime(23);
```

That's a direct jump. Sundial reports one transition from the old active period to the new one, triggering only the callback/s for that new time period. It won't act as though time naturally passed through Day, Afternoon and Dusk, so none of those intermediate callbacks will trigger.

Automatic progression behaves differently. If enough real time passes to cross several period boundaries (let's say you have sped up time significantly), Sundial walks those boundaries in chronological order and fires each one.

This lets you use manual time changes for things like loading a save, sleeping until night, debug controls, or a cutscene that deliberately jumps the clock. A jump is a jump. Normal time progression is what lets Sundial behave like time actually passed.

---

## Measuring sunlight

Sundials time periods are discrete but there might be cases when you want access to a continuous daylight value.

In those cases, `GetSunlightAmount()` returns Sundial's current daylight amount from `0..1`:

```js
var _sunlight = sundial.GetSunlightAmount();
```

Sundial uses this value internally to blend between Day and Night brightness, and your own visual systems can use it too. For example, a separate shadow renderer could make shadows stronger or weaker across the day without trying to mirror all of Sundial's Morning, Sunset, Twilight and Predawn maths.

Try to keep that distinction in mind: periods are good for **events**, while sunlight amount is good for **continuous reactions** that care about how much daylight is left.

---

## Next: Indoor & Outdoor Grading

The clock tells Sundial *when* the scene is. The next page deals with the case where different parts of the same scene should be colour graded differently.

Continue with **[Indoor & Outdoor Grading](indoor-and-outdoor)** to set up masks and give interiors their own grading behaviour.
