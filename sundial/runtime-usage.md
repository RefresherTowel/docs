---
layout: default
title: Runtime Usage
parent: Sundial
nav_order: 2
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Runtime Usage

Once a Sundial preset has been authored, the runtime side is intentionally small.

You need a `Sundial`, you need to give it a time, and you need to draw the surface through it. Everything else is there for the games that need a little more control.

---

## Importing the default preset

If you're using the IDE plugin, the normal Create Event setup is:

```js
sundial = SundialImport();
```

`SundialImport()` looks up the preset marked as Default in the editor and creates a new `Sundial` configured from it.

That includes the preset's:

- six grading colours and strengths
- outdoor Day/Night brightness
- indoor grading settings
- cycle timing
- Morning clock origin
- Start Time
- Day Length
- Auto Time setting
- six authored period callbacks

It does **not** include a runtime mask. The editor's screenshot and preview mask are authoring resources, not game resources, so your game supplies its own mask if it needs one.

---

## Importing a named preset

Suppose the same game has an Overworld look and a much colder Winter look.

If Overworld is the default:

```js
sundial = SundialImport();
```

loads it automatically.

To load Winter instead:

```js
sundial = SundialImport("Winter");
```

Preset names are exact. If you request a preset that doesn't exist, Sundial throws an error instead of silently falling back to the default.

Each call creates a new `Sundial` instance, so the imported preset is the starting configuration for that Sundial rather than some shared mutable global grading object.

---

## Drawing the graded surface

Sundial grades a surface when you call `Draw()`:

```js
sundial.Draw(application_surface);
```

The one-argument form draws the source at `(0, 0)` using its own width and height.

If your game already has a final surface draw at a particular size, use the same destination there:

```js
sundial.Draw(application_surface, 64, 36, 1152, 648);
```

The arguments are:

```text
source surface
x
y
width
height
```

Sundial doesn't need to own your render pipeline. The useful way to think about `Draw()` is: wherever you would normally draw the final surface, Sundial can perform that draw through the current time-of-day grade instead.

The source must still exist when `Draw()` runs. If you're using a mask, that surface must also still exist and have exactly the same dimensions as the source surface.

---

## Setting the current time

If your game already has a clock, give Sundial the same time:

```js
sundial.SetTime(14.5);
```

That means 14:30.

Then later:

```js
sundial.SetTime(21);
```

moves the grade to 21:00.

`SetTime()` uses a decimal 24-hour clock, so `6.25` is 06:15 and `18.75` is 18:45.

You can also work directly in Sundial's normalized `0..1` cycle:

```js
sundial.SetTimeOfDay(0.5);
```

or use the equivalent alias:

```js
sundial.SetDayPercent(0.5);
```

The 24-hour clock is normally easier for game code to read. The normalized form is useful when another system already represents a day as a fraction.

---

## Letting Sundial keep time

For games that don't already have a clock, Sundial can advance itself:

```js
sundial
    .SetDayLength(600)
    .SetTime(8)
    .SetAutoTime(true);
```

This starts at 08:00 and makes one complete game day take 600 real seconds.

You don't need to add `time += something` in a Step Event. Sundial's automatic progression is based on elapsed real time and synchronizes when you draw it or ask a time-dependent question.

If gameplay code needs Sundial to advance at a particular point before any draw or query happens, you can explicitly synchronize it:

```js
sundial.Update();
```

Most projects won't need that call every Step. `Draw()` and the time queries already synchronize automatic time.

---

## Reading the current state

Sundial can answer the common clock questions directly:

```js
var _time = sundial.GetTime();
var _hour = sundial.GetHour();
var _minute = sundial.GetMinute();
var _period = sundial.GetPeriod();
```

You can also ask for the normalized day position:

```js
var _percent = sundial.GetDayPercent();
```

or the continuous sunlight amount Sundial is using for brightness:

```js
var _sunlight = sundial.GetSunlightAmount();
```

`GetSunlightAmount()` is useful when another visual system should roughly follow Sundial's daylight without trying to recreate Sundial's timing logic itself. For example, a separate shadow-opacity system could react to the same continuous daylight amount while still remaining its own system.

---

## The IDE plugin isn't a runtime dependency

`SundialImport()` doesn't open the authoring JSON while the game is running.

The plugin compiles the authored presets into an internal persistent GameMaker object in the project. `SundialImport()` creates that internal object lazily when it needs it, reads the compiled preset data, then configures an ordinary public `Sundial` through the same setter methods available to your own code.

That matters for two reasons.

First, the game doesn't need the IDE plugin installed to run.

Second, manual Sundial setup and imported Sundial setup aren't two separate runtime systems. Once the `Sundial` exists, you can use the same methods either way:

```js
sundial = SundialImport("Winter");
sundial.SetTime(18.5);
sundial.SetBrightness(1.0, 0.32);
```

The imported values are a starting configuration, not a cage around the object.

---

## Next: Time, Periods & Callbacks

Basic runtime use only needs an import, a time and a draw call. The next page goes into the part that becomes useful when gameplay itself cares whether it's Morning, Dusk or Night.

Continue with **[Time, Periods & Callbacks](time-periods-and-callbacks)** for Auto Time, period boundaries, clock queries and callbacks.
