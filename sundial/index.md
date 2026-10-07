---
layout: default
title: Sundial
nav_order: 5
has_children: true
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

![Sundial icon](../assets/sundial_icon.png)
{: .text-center}

*A visual time-of-day colour grader for GameMaker*
{: .text-center}

A day/night effect often starts with something very simple. Make the screen a bit blue at night, maybe a bit orange around sunset, and call it done.

Then you want dawn to feel different from morning. Night needs to actually be darker, not just bluer. The sunset transition looks good but the interior of a house suddenly turns bright orange with everything outside it. You add a few more colours, a few more timings, and now you've got a surprisingly fiddly little lighting system sitting in the middle of your game.

**Sundial** is built to handle that particular problem without turning into a full lighting engine.

It takes an existing 2D scene and grades it continuously through six authored parts of the day:

- **Morning**
- **Day**
- **Afternoon**
- **Dusk**
- **Night**
- **Dawn**

You choose the colour and strength of those looks, Sundial blends between them, and separate day/night brightness controls handle how light the scene should actually be.

The easiest way to author Sundial is through its GameMaker IDE plugin. Import a screenshot from your game, scrub through the day, drag the period timings around, and tune the result while looking at the actual scene you're trying to grade.

The runtime itself stays small. Once you've authored a preset, using it in-game can be as simple as:

```js
sundial = SundialImport();
```

and then, wherever your game draws the surface you want to grade:

```js
sundial.Draw(application_surface);
```

That's enough to load the default IDE-authored preset and draw the current Sundial grade.

> Sundial is part of the **RefresherTowel Games** suite of libraries for GameMaker.
{: .note}

---

## Your first Sundial setup

Suppose you've opened the Sundial IDE editor, imported a screenshot, and adjusted the preset until you like how the day looks.

In your controller's Create Event:

```js
sundial = SundialImport();
```

`SundialImport()` creates a new `Sundial` using the preset marked as **Default** in the editor. The colours, strengths, brightness, timings, start time, Auto Time setting and authored callbacks all come with it.

If you made several presets, ask for one by name instead:

```js
sundial = SundialImport("Winter");
```

The name must exactly match one of the presets you authored. If it doesn't, Sundial throws a clear error instead of quietly loading something else and leaving you wondering why the game looks wrong.

Now draw the surface through Sundial:

```js
sundial.Draw(application_surface);
```

Sundial doesn't take ownership of the surface or decide how your game should render everything else. It simply takes the source surface you give it, applies the current grade, and draws the result to the active render target.

If your final surface normally needs to be drawn somewhere other than its original size, provide the destination too:

```js
sundial.Draw(application_surface, 0, 0, 1280, 720);
```

The rest of your rendering setup can stay exactly where it already belongs.

---

## Time can be manual or automatic

For a game that already owns its own clock, you can simply tell Sundial what time it is:

```js
sundial.SetTime(18.5);
```

`18.5` means 18:30 on Sundial's 24-hour clock.

Or let Sundial advance the clock itself:

```js
sundial
    .SetDayLength(600)
    .SetAutoTime(true);
```

Now a complete in-game day takes 600 real-world seconds, or ten minutes.

You don't have to manually lerp between six colours or work out which side of midnight you're on. Sundial resolves the continuous grade, brightness and current period for you.

---

## Indoor and outdoor areas can react differently

Without a mask, Sundial grades the entire source surface as outdoor scenery.

If your scene contains interiors, you can provide a same-sized mask surface:

```text
black = outdoor
white = indoor
grey  = a blend between the two
```

Sundial only reads the mask's red channel.

Indoor pixels can have their own base colour, grading strength and day/night brightness. They can also inherit some of the outdoor colour through **Indoor Daylight Influence**, which lets a room stay recognisably indoors while still picking up some of the warmth of dusk or the coolness of night.

The editor can use a preview mask while you're authoring, but that image is only for the editor. Your game still supplies the real runtime mask with `SetMask()`.

---

## You don't need the IDE to use Sundial

The IDE plugin is there because colour grading is much easier to author when you can actually see it.

It isn't a runtime dependency.

You can build a Sundial entirely in code:

```js
sundial = new Sundial()
    .SetGrading(eSundial.MORNING, make_color_rgb(194, 242, 229))
    .SetGradingStrength(eSundial.MORNING, 2)
    .SetBrightness(1.09, 0.39)
    .SetTime(6);
```

Every setting the importer applies goes through the same public `Sundial` API available to your own code. The editor is simply a visual authoring layer over that runtime.

That also means disabling or uninstalling the IDE plugin doesn't suddenly make a built project depend on it. The GML runtime and the compiled preset data live in the project itself.

---

## Where to go next

Start with **[Using the IDE Plugin](ide-plugin)**. That's the intended authoring path and the quickest way to understand what Sundial is doing visually.

Then move to **[Runtime Usage](runtime-usage)** for importing presets and drawing them in-game. **[Time, Periods & Callbacks](time-periods-and-callbacks)** covers the clock, automatic time progression and gameplay reactions to Morning, Dusk, Night and the other authored periods.

If your game needs interiors, **[Indoor & Outdoor Grading](indoor-and-outdoor)** explains the mask and the separate indoor controls.

Finally, **[Configuring Sundial in Code](manual-configuration)** covers the full code-only setup for projects that don't want to use the IDE plugin at all.

{% include library-footer.html %}
