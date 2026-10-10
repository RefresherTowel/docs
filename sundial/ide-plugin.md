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

You *can* configure Sundial entirely in code, but colour grading is one of those jobs where staring at RGB values is a terrible substitute for being able to dynamically watch changes happen as you make them.

That's why I build the **Sundial IDE** plugin, which gives Sundial a native GameMaker editor to allow you to edit your day/night grading live. Simply import a screenshot from your game, scrub through the time of day and change the grading while looking at the actual scene as it would appear in-game.

This page will walk you through exactly how to use the GM pluging for Sundial, taking you from installing the plugin to an authored preset running in your game.

---

## Installing and opening Sundial

Sundial IDE is installed through GameMaker's Package Manager / GMPM flow. Please visit **INSERT URL HERE** to get the plugin after you've purchased Sundial, and for instructions on how to install it.

Quickly, the steps for a clean install are:

1. Install **Sundial IDE** from its GMPM source.
2. Make sure the installed plugin is enabled in Package Manager (the checkbox to the left of it needs to be **checked**).
3. Restart GameMaker after enabling the plugin.
4. Open the project you want to author.
5. Choose **Tools > Sundial**.

Installing the package and enabling the plugin are separate things in GameMaker. If Sundial is installed but **Tools > Sundial** doesn't appear, check that the plugin itself is enabled and has been loaded by the IDE.

The plugin only helps you author your scene. It isn't something your game loads at runtime so it doesn't add any extra load times or cpu cost or anything like that, it's purely GM IDE only.

---

## Importing a screenshot

Start by importing a screenshot from your game.

> Usually you can take a screenshot by pressing `Windows key + shift + S` and selecting an area of the screen on Windows, alternatively you can press the `printscrn` key. The exact method can differ depending on your setup, so try out a couple of different key combinations or do some research if these don't work for you (I don't own a mac so I can't offer advice on that platform).
{: .note}

Try to pick a screenshot that contains a good representation of any distinctive features your game might have, like particularly bright colours or interesting colour combinations. If your game has bright grass, dark stones, water and a bunch of other variations like that in the same kind of scene, then that's a good screenshot to use. You're looking for a representative screenshot that makes it easy to notice when one of the grades is pushing something too far.

**INSERT SCREENSHOT WITH IMPORT HIGHLIGHTED**

After you've imported the screenshot, it should show up in the preview section.

I've tried to make it so the preview window has all the normal navigation controls you'd expect from an image editor. You can pan, zoom, fit the image, return to 100%, or centre it and that kind of thing.

---

## Times of the day

The timeline contains Sundial's six authored periods:

```text
Morning -> Day -> Afternoon -> Dusk -> Night -> Dawn -> Morning
```

**INSERT SCREENSHOT WITH TIME SCRUBBER HIGHLIGHTED**

Click on one of the dots to select a specific time period. The **Colour Grading** panel then edits that period's:

```text
Time
Colour
Strength
Callback
```

You can also drag the dots around to adjust how long the time periods last relative to one another (Morning, specifically, is fixed in place, as it is the "start" of the day cycle, but you can change what time Sundial treats Morning as starting using the **Time** input).

**INSERT SCREENSHOT WITH COLOUR SETTINGS HIGHLIGHTED**

**Colour** chooses the hue Sundial biases the scene toward.

**Strength** controls how strongly that colour affects the scene. It isn't limited to `0..1`, instead it can push values above `1` to deliberately exaggerate the colour shift when you want a much stronger stylised look.

You can scrub the separate preview playhead anywhere across the timeline to see the continuous visuals between the six time periods as they flow into each other by dragging the arrow icon under the timeline.

**Play / Pause** starts or stops automatic play through of the preview timeline, and the playback-rate control lets you cycle through the day faster.

> **Play / Pause** and the speed scale **1x / 2x / etc** don't effect anything **in-game**, they are purely for the visualiser.
{: .important}

As mentioned earlier, Morning is the cycle "seam", so it stays fixed at the very start of the timeline. The other five nodes can be dragged horizontally to change what time they begin.

Typing a period's **Time** does the same job using a clock value instead. So, if you decided to enter `18:30` when Dusk is selected, that moves the Dusk node to 18:30, and Dusk will "arrive" at 18:30 in your game.

---

## Presets

The **Presets** list on the left holds different Sundial setups for the your game.

**INSERT SCREENSHOTS WITH PRESETS LIST HIGHLIGHTED**

Use the `+` button to create a new preset from Sundial's defaults. Right-click an existing preset to see the available actions for it:

- Rename
- Duplicate
- Set as Default
- Delete

Duplicate is useful when two areas should share the same rough day/night shape but have different colour character. You can build an Overworld preset, duplicate it into Winter, then push the new one colder without rebuilding every timing from scratch.

There's always one default preset. That's the preset returned by:

```js
sundial = SundialImport();
```

You need to load named presets explicitly:

```js
sundial = SundialImport("Winter");
```

---

## Outdoor, indoor and time settings

The other foldouts apply to the whole selected preset rather than one grading anchor.

**Outdoor Settings** contains the Day and Night brightness values. Brightness is kept separate from grading colour, as ,aking Night **blue** and making Night *dark* are two different artistic decisions, and therefore Sundial doesn't treat them as a single setting.

**INSERT SCREENSHOT WITH OUTDOOR SETTINGS HIGHLIGHTED**

**Indoor Settings** contains the indoor base colour, grading strength, daylight influence and separate Day/Night brightness values. These only become visible when you supply a runtime mask that marks pixels as indoor.

**INSERT SCREENSHOT WITH INDOOR SETTINGS HIGHLIGHTED**

**Time** contains:

```text
Auto Time
Start Time
Day Length
```

**INSERT SCREENSHOT WITH TIME SETTINGS HIGHLIGHTED**

Auto Time decides whether an imported Sundial should advance its own clock. You should only turn this off if you already have a time system in your game and want to manually sync Sundial with that time. Start Time is the clock time that Sundial starts at when it begins running in your game. Day Length is how many real-world minutes a complete game day should take.

> These time settings are different to the editor's **Play / Pause** and **1x / 2x / etc** buttons. Those buttons are only for previewing. These settings are the live settings for how time works when Sundial is running in your game.
{: .note}

---

## Previewing interiors

Use **Import Preview Mask** if the screenshot contains indoor and outdoor areas and you want to change the indoor colour grading.

The preview mask uses the same meaning as the runtime mask:

```text
black = outdoor
white = indoor
grey  = proportional blend
```

> Only the red channel actually matters, but black and white is easier to understand.
{: .note}

To show you an example of what you might want to mask, here's a screenshot from a top-down bee sim game.

**INSERT SCREENSHOT OF BEE SIM**

And here's the mask, where you can see I've essentially replaced the hive with a fuzzy white colour.

**INSERT SCREENSHOT OF A MASK**

The View palette that sits in the preview window gives you the option to inspect the **Final**, **Original**, **Outdoor**, **Indoor** or **Mask** result, so you can inspect each part individually to track down any weird spots doing bizarre things.

> The preview mask is editor-only just like the screenshot of your game. Sundial won't use it during runtime in your game. Instead, you should either dynamically create the mask based on what's on screen (maybe have the inside of houses draw themselves as pure white to a surface you are using as a mask), or if your game is suitable, you can just create a mask sprite in an image editor and give it to Sundial when your game starts.
{: .important}

---

## Callbacks

Each period has a **Callback** field that allows you to supply a function that will be executed when Sundial hits the particular time of day when the game is running.

A function reference is perfectly fine (and probably the easiest to work with):

```js
MyDuskFunction
```

> Make sure you **don't** provide the rounded brackets when supplying a function here, as that will *execute* the function, not store it. So `MyDuskFunction()` is incorrect. It should be `MyDuskFunction`.
{: .warning}

But you can also supply a function expression if you wish:

```js
function() {
    global.streetlights = true;
}
```

You don't have to provide anything here if you don't need Sundial to run code for a particular time of day.

You can use this for small things that belong to the schedule you're creating, such as turning street lights on at Dusk. You can still register callbacks from code as well...the IDE callback doesn't replace callbacks that you add via code, instead, all callbacks are added to an array and will all be executed when the time of day is hit.

---

## The editor internals

Sundial keeps its files stored in the `/rtg/sundial/` folder in your project folder. When you uninstall it, it should delete these files, but just in case it doesn't, that's where you would need to look.

---

## Next: How to set up Sundial in your actual game

Once the preset looks right, the editor has done its job. The next step is getting Sundial set up and working in your game.

Continue with **[Using Sundial in your game](using-sundial)** to see how to import the preset, draw Sundial, and get an idea of what the IDE *does* and *doesn't* supply to the runtime.
