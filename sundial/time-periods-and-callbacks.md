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

Gameplay often needs something more definite, though.

Street lights need a moment when they turn on. Shops might close at Night. Morning birds shouldn't ask whether the screen is currently 63% dawn-coloured before deciding whether to chirp.

Sundial handles both ideas at once. The grading stays continuous, while the six authored timeline nodes also act as clear semantic **period** boundaries for game logic.

---

## The six authored periods are the schedule

Sundial's public periods are:

```text
Morning
Day
Afternoon
Dusk
Night
Dawn
```

In code, those are the `eSundialPeriod` values:

```js
eSundialPeriod.MORNING
eSundialPeriod.DAY
eSundialPeriod.AFTERNOON
eSundialPeriod.DUSK
eSundialPeriod.NIGHT
eSundialPeriod.DAWN
```

The timeline you author in the IDE is the same schedule `GetPeriod()` and the callback API use at runtime.

If you put Dusk at 18:30 in the editor, then 18:30 is where Sundial starts reporting Dusk and where the Dusk callbacks fire. You don't need to author the visual timeline and then separately reproduce those times in game code.

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

Sundial also exposes `GetPhase()` and `GetPhaseName()`, but phases are a different thing. Internally, Sundial uses a slightly more detailed resolver with phases such as Sunset, Twilight and Predawn to make the continuous visual transitions look good.

Those internal phases don't add extra authored schedule boundaries.

If the question is "what part of the authored day is gameplay currently in?", use `GetPeriod()`.

If the question is "which part of Sundial's continuous visual resolver is currently dominant?", `GetPhase()` is the more specific diagnostic answer.

---

## Running something when a period begins

Suppose the town's street lights should turn on when Dusk begins:

```js
sundial.OnDusk(function() {
    global.streetlights = true;
});
```

Then turn them back off in the morning:

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

Callbacks are additive. Registering a second Dusk callback doesn't replace the first one:

```js
sundial.OnDusk(function() {
    global.streetlights = true;
});

sundial.OnDusk(function() {
    audio_play_sound(snd_evening_bells, 0, false);
});
```

Both run when Dusk begins.

If the preset was imported from the IDE, any callback authored in the Dusk Callback field is already registered as well. Programmatic callbacks simply add more behaviour to the same period.

---

## Watching every period change

Sometimes one system wants to know about every period instead of registering six separate callbacks.

Use `OnPeriodChanged()`:

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

This is useful for systems such as an ambient audio controller that reacts to the entire day schedule but still decides for itself what each transition should mean.

---

## Using Sundial's 24-hour clock

`SetTime()` and `GetTime()` use decimal hours:

```js
sundial.SetTime(6);      // 06:00
sundial.SetTime(13.5);   // 13:30
sundial.SetTime(23.75);  // 23:45
```

Read it back in whichever form is convenient:

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

With Morning at 06:00, a normalized day position of `0.25` is 12:00, `0.5` is 18:00 and `0.75` is 00:00.

When you use the IDE, changing Morning's Time field configures this clock origin for you.

---

## Using normalized day time

If another system already works in a `0..1` day fraction, you don't have to convert it to hours:

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

Values outside the range wrap around the cycle. The explicit endpoint `1` is preserved as the end of the current cycle, which meets Morning again at the seam.

---

## Automatic time

Turn automatic progression on with:

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

`GetAutoTime()` still returns `true` in that case. The clock simply isn't moving until you give it a positive speed again.

---

## You normally don't need to call Update every Step

Automatic time is timestamp-driven.

When `Draw()` runs, or when you ask Sundial a time-dependent question such as `GetTime()` or `GetPeriod()`, Sundial first synchronizes the elapsed real time.

That means this is normally enough:

```js
sundial.SetAutoTime(true);
```

You don't also need:

```js
// Usually unnecessary.
sundial.Update();
```

in every Step Event.

`Update()` exists for the cases where gameplay order matters. If some Step logic needs period callbacks to have fired *before* the rest of that logic runs, call `Update()` at the point where you want Sundial synchronized.

---

## Manual jumps and automatic crossings are deliberately different

Suppose Sundial is currently in Morning and you do this:

```js
sundial.SetTime(23);
```

That's a direct jump. Sundial reports one transition from the old active period to the new one. It doesn't pretend time naturally passed through Day, Afternoon and Dusk on the way there.

Automatic progression behaves differently. If enough real time passes to cross several period boundaries, Sundial walks those boundaries in chronological order and fires each one.

That distinction keeps manual time changes useful for things such as loading a save, sleeping until night, debug controls, or a cutscene that deliberately jumps the clock. A jump is a jump. Normal time progression still behaves like time actually passed.

---

## Sunlight amount is continuous

Periods are discrete, but some systems want a continuous daylight value.

`GetSunlightAmount()` returns Sundial's current daylight amount from `0..1`:

```js
var _sunlight = sundial.GetSunlightAmount();
```

Sundial already uses this value internally to blend between Day and Night brightness.

Your own visual systems can use it too. For example, a separate shadow renderer could make shadows stronger or weaker across the day without trying to mirror all of Sundial's Morning, Sunset, Twilight and Predawn maths.

Try to keep that distinction in mind: periods are good for **events**, while sunlight amount is good for **continuous reactions**.

---

## Next: Indoor & Outdoor Grading

The clock tells Sundial *when* the scene is. The next page deals with the case where different parts of the same scene shouldn't receive the same treatment.

Continue with **[Indoor & Outdoor Grading](indoor-and-outdoor)** to set up masks and give interiors their own grading behaviour.
