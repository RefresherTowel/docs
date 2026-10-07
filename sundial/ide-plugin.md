---
layout: default
title: Using the IDE Plugin
parent: Sundial
nav_order: 1
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Using the IDE Plugin

You *can* configure Sundial entirely in code, but colour grading is one of those jobs where staring at RGB values is a pretty miserable substitute for looking at the actual picture.

The **Sundial IDE** plugin gives Sundial a native GameMaker editor built around that idea. Import a screenshot from your game, scrub through the time of day, and change the grading while looking at the scene you're actually trying to make look good.

This page is currently the short version of the IDE guide. The editor itself is complete, but this page will eventually get the full screenshot-heavy walkthrough. For now, it covers the parts you need to get from installing the plugin to an authored preset that `SundialImport()` can use.

---

## Installing and opening Sundial

Sundial IDE is installed through GameMaker's Package Manager / GMPM flow.

On a clean install:

1. Install **Sundial IDE** from its GMPM source.
2. Make sure the installed plugin is enabled in Package Manager.
3. Restart GameMaker after enabling the plugin if GameMaker asks you to.
4. Open the project you want to author.
5. Choose **Tools > Sundial**.

Installing the package and enabling the plugin are separate things in GameMaker. If Sundial is installed but **Tools > Sundial** doesn't appear, check that the plugin itself is enabled and has been loaded by the IDE.

The plugin only needs to be present while you're authoring. It isn't something your finished game loads at runtime.

---

## Import a screenshot first

The easiest place to begin is **Import Screenshot**.

Pick a representative screenshot from your game and Sundial stores it as an editor-only preview image for this project. The screenshot isn't added to your game's Included Files and doesn't become part of the compiled game.

Try to use a screenshot that contains the kinds of colours you actually care about. If your game has bright grass, dark stone, skin tones, water and a bunch of UI all in the same kind of scene, a representative screenshot makes it much easier to notice when one of the grades is pushing something too far.

The preview has the normal navigation controls you'd expect from an image editor. You can pan, zoom, fit the image, return to 100%, or centre it without changing the authored Sundial data.

---

## Work through the six periods

The timeline contains Sundial's six authored periods:

```text
Morning -> Day -> Afternoon -> Dusk -> Night -> Dawn -> Morning
```

Click a period to select it. The **Colour Grading** panel then edits that period's:

```text
Time
Colour
Strength
Callback
```

**Colour** chooses the hue Sundial biases the scene toward.

**Strength** controls how strongly that colour affects the scene. It isn't limited to `0..1`; values above `1` deliberately exaggerate the colour shift when you want a much stronger look.

You can scrub the separate preview playhead anywhere across the timeline to see the continuous result between the six authored grades. **Play / Pause** runs the preview automatically, and the playback-rate control lets you cycle through the day faster.

Morning is the cycle seam and stays fixed at the start/end of the normalized day. The other five period nodes can be dragged horizontally to change when they begin.

Typing a period's **Time** does the same job using a clock value instead. If you type Dusk as `18:30`, that moves the Dusk node to 18:30. There isn't a second hidden gameplay schedule you also have to keep in sync.

---

## Presets let one project have several looks

The **Presets** list on the left holds named Sundial setups for the current project.

Use the `+` button to create a new preset from Sundial's defaults. Right-click an existing preset for the normal management actions:

- Rename
- Duplicate
- Set as Default
- Delete

Duplicate is useful when two areas should share the same basic day/night shape but have different colour character. You can build an Overworld preset, duplicate it into Winter, then push the new one colder without rebuilding every timing from scratch.

There is always one default preset. That is the preset returned by:

```js
sundial = SundialImport();
```

Named presets are loaded explicitly:

```js
sundial = SundialImport("Winter");
```

---

## Outdoor, indoor and time settings

The other foldouts apply to the whole selected preset rather than one grading anchor.

**Outdoor Settings** contains the Day and Night brightness values. These are deliberately separate from grading colour. Making Night blue and making Night dark are two different artistic decisions, so Sundial doesn't force one to imply the other.

**Indoor Settings** contains the indoor base colour, grading strength, daylight influence and separate Day/Night brightness values. These only become visible where a runtime mask marks pixels as indoor.

**Time** contains:

```text
Auto Time
Start Time
Day Length
```

Auto Time decides whether an imported Sundial should advance its own clock. Start Time is the clock time the imported preset begins at. Day Length is how many real-world minutes a complete game day should take.

The editor's **Play / Pause** button is only for previewing. It doesn't turn runtime Auto Time on or off.

---

## Previewing interiors

Use **Import Preview Mask** if the screenshot contains indoor and outdoor areas and you want to author both at once.

The preview mask uses the same meaning as the runtime mask:

```text
black = outdoor
white = indoor
grey  = proportional blend
```

Only the red channel matters.

The View palette can show the **Final**, **Original**, **Outdoor**, **Indoor** or **Mask** result, which is useful when you're trying to work out whether a weird pixel is coming from the outdoor grade, the indoor grade, or the mask itself.

The preview mask is editor-only just like the screenshot. Sundial doesn't turn it into a runtime mask for you.

---

## Callbacks can be authored with the period

Each period has a **Callback** field for a GML expression.

A function reference is fine:

```js
scr_on_dusk
```

So is a function expression:

```js
function() {
    global.streetlights = true;
}
```

Leave the field blank when that period doesn't need a callback.

The callback is compiled into the project's Sundial runtime data. When the period begins, Sundial checks whether the stored value is callable and invokes it if it is.

This is useful for small things that naturally belong to the schedule you're already authoring, such as turning street lights on at Dusk. You can still register callbacks from code as well; the IDE callback doesn't replace the runtime callback API.

---

## What the editor saves

The editor keeps its authoring data, preview screenshot, preview mask and editor state inside the project. Those editor files aren't runtime Included Files.

When you save Sundial settings, the plugin also generates the compiled data used by `SundialImport()` into Sundial's internal runtime object. That is why the game doesn't need to parse the editor JSON or load the IDE plugin at runtime.

For ordinary use, you don't need to touch any of those files by hand. Open **Tools > Sundial**, edit the preset, and let the plugin keep the authored and runtime forms in sync.

---

## Next: Runtime Usage

Once the preset looks right, the editor has done its job. The next step is getting that authored result onto the game's actual surface.

Continue with **[Runtime Usage](runtime-usage)** to import the preset, draw it, choose named presets, and understand what the IDE does and doesn't supply to the runtime.
