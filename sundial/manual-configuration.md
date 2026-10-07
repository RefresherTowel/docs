---
layout: default
title: Configuring Sundial in Code
parent: Sundial
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

# Configuring Sundial in Code

The IDE plugin is the easiest way to author Sundial because you can see the result while you're changing it.

It isn't required, though.

`SundialImport()` ultimately creates an ordinary `Sundial` and configures it through the same public methods on this page. If your game wants to generate its own looks, load settings from somewhere else, or simply keep the whole setup in GML, you can start directly with:

```js
sundial = new Sundial();
```

The constructor already has a complete default day/night setup, so even that is a usable Sundial. From there, replace whichever parts your game wants to own.

---

## The six grading anchors

Sundial exposes six authored grading stages through `eSundial`:

```js
eSundial.MORNING
eSundial.DAY
eSundial.AFTERNOON
eSundial.DUSK
eSundial.NIGHT
eSundial.DAWN
```

Set a stage's colour with `SetGrading()`:

```js
sundial.SetGrading(
    eSundial.DUSK,
    make_color_rgb(161, 51, 71)
);
```

Then set how strongly that colour should bias the scene:

```js
sundial.SetGradingStrength(eSundial.DUSK, 1.48);
```

A strength of `0` leaves that stage neutral. `1` applies the full luminance-normalized colour bias, and values above `1` deliberately exaggerate it.

Sundial normalizes the grading colour around its luminance before applying the strength. In practical terms, the colour control is mainly answering "what colour should this part of the day feel like?" rather than secretly deciding how bright it should be as well.

Brightness is configured separately.

---

## Outdoor brightness

Set full-Day and full-Night brightness with:

```js
sundial.SetBrightness(1.09, 0.39);
```

The first value is Day brightness. The second is Night brightness.

Sundial blends continuously between them using its resolved sunlight amount, so you don't need to create a separate brightness value for all six grading anchors.

This separation is useful because two scenes can use the same Dusk colour but very different exposure. A bright stylised game might keep Night around `0.7`, while a horror game might deliberately push it much lower.

---

## A complete outdoor setup

You can chain the configuration calls:

```js
sundial = new Sundial()
    .SetGrading(eSundial.MORNING, make_color_rgb(194, 242, 229))
    .SetGradingStrength(eSundial.MORNING, 2.00)
    .SetGrading(eSundial.DAY, make_color_rgb(255, 237, 189))
    .SetGradingStrength(eSundial.DAY, 2.00)
    .SetGrading(eSundial.AFTERNOON, make_color_rgb(219, 121, 55))
    .SetGradingStrength(eSundial.AFTERNOON, 1.17)
    .SetGrading(eSundial.DUSK, make_color_rgb(161, 51, 71))
    .SetGradingStrength(eSundial.DUSK, 1.48)
    .SetGrading(eSundial.NIGHT, make_color_rgb(28, 28, 61))
    .SetGradingStrength(eSundial.NIGHT, 1.25)
    .SetGrading(eSundial.DAWN, make_color_rgb(246, 194, 222))
    .SetGradingStrength(eSundial.DAWN, 0.91)
    .SetBrightness(1.09, 0.39);
```

Those are Sundial's current built-in defaults. You don't need to repeat them when you like the defaults; the example is just showing what a full code-authored grading setup looks like.

Normally, start with the visual result you want rather than treating these numbers as rules. There isn't a mathematically correct Dusk strength. The useful value is the one that makes *your* scene look right.

---

## Configuring interiors in code

The indoor settings use the same public runtime API whether the Sundial came from `new Sundial()` or `SundialImport()`:

```js
sundial
    .SetIndoorGrading(make_color_rgb(230, 220, 205))
    .SetIndoorGradingStrength(0.8)
    .SetIndoorDaylightInfluence(0.25)
    .SetIndoorBrightness(0.85, 0.55);
```

These settings only affect pixels selected by a runtime mask.

See **[Indoor & Outdoor Grading](indoor-and-outdoor)** for the mask itself and the exact meaning of each indoor control.

---

## Configuring cycle timing

`SetCycleTiming()` controls the normalized shape of Sundial's continuous resolver:

```js
sundial.SetCycleTiming(
    0.60,      // day fraction
    0.10,      // morning duration
    0.27,      // afternoon blend start
    65 / 600,  // sunset duration
    45 / 600,  // twilight duration
    75 / 600   // predawn duration
);
```

All six values live in Sundial's normalized `0..1` cycle.

They mean:

```text
day_fraction       where daytime ends and Dusk begins
morning_duration   how long Morning takes to fade into Day
afternoon_start    where the Afternoon colour begins blending in
sunset_duration    how long before day end the sunset blend occupies
twilight_duration  how long after day end Twilight occupies
predawn_duration   how much of the end of night is used for Predawn
```

There is a little more going on here than six simple clock timestamps because Sundial's internal visual resolver uses extra Sunset, Twilight and Predawn phases to make the grade move naturally.

The public semantic period boundaries resolve to:

```text
Morning   = 0
Day       = morning_duration
Afternoon = day_fraction - sunset_duration
Dusk      = day_fraction
Night     = day_fraction + twilight_duration
Dawn      = 1 - predawn_duration * 0.5
```

`afternoon_start` is deliberately separate from the public Afternoon boundary. It controls when the Afternoon colour begins blending in before the authored Afternoon period is considered active.

This is the one part of Sundial I would normally recommend authoring in the IDE unless you have a specific reason not to. Dragging the visible period nodes around a timeline is simply easier to reason about than editing six normalized timing values by hand.

---

## Giving the normalized cycle a clock

The visual cycle itself only needs `0..1`. If game code wants a 24-hour clock as well, tell Sundial what time Morning represents:

```js
sundial.SetMorningTime(6);
```

Now normalized `0` is 06:00.

Set the current clock time with:

```js
sundial.SetTime(17.5);
```

which means 17:30.

The clock origin doesn't change the visual timing shape. It gives the existing normalized cycle a human-readable 24-hour interpretation.

---

## Configuring automatic time

For a ten-minute day:

```js
sundial
    .SetDayLength(600)
    .SetTime(8)
    .SetAutoTime(true);
```

Or configure the speed directly in game seconds per real second:

```js
sundial
    .SetSpeed(144)
    .SetAutoTime(true);
```

The two controls describe the same progression rate in different ways. Setting one updates the value represented by the other.

See **[Time, Periods & Callbacks](time-periods-and-callbacks)** for the exact synchronization and callback behaviour.

---

## Adding period callbacks in code

The general form is:

```js
sundial.OnPeriod(eSundialPeriod.NIGHT, function() {
    global.is_night = true;
});
```

but the convenience calls are usually nicer to read:

```js
sundial
    .OnDusk(function() {
        global.streetlights = true;
    })
    .OnMorning(function() {
        global.streetlights = false;
    });
```

`OnPeriodChanged()` is available when one callback wants every change instead:

```js
sundial.OnPeriodChanged(function(_from, _to) {
    global.current_period = _to;
});
```

---

## Code-authored and IDE-authored Sundials can mix

You don't have to make a project-wide choice between the IDE and manual configuration.

For example, you can author the expensive visual part in the IDE:

```js
sundial = SundialImport("Overworld");
```

then let a difficulty mode alter Night brightness in code:

```js
if (hard_mode) {
    sundial.SetBrightness(1.09, 0.25);
}
```

Or use the IDE for the Overworld and create a tiny special-purpose Sundial in code for a dream sequence.

Once imported, a `Sundial` is just a normal Sundial. Use whichever authoring path keeps the thing you're trying to express easiest to understand.

---

## API Reference

The teaching pages focus on how the pieces fit together. For exact signatures, argument types, return values and enum members, continue to the **[API Reference](api-reference)**.
