---
layout: default
title: Using Sundial in Your Game
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

# Using Sundial in Your Game

Let's look at how you might use Sundial in your game, without running it through the automated `SundialStart()` and `SundialStop()` functions, giving you more control over how Sundial works.

In your Create Event (preferably in a singleton controller object):

```js
sundial = SundialImport();
```

Then in Post Draw:

```js
sundial.Draw();
```

> Sundial takes over the application surface by default. This includes turning off automatic drawing of the application surface. This is something you should be aware of. You can tell sundial **not** to do this by providing `false` as the second argument to `SundialImport()` or as the first argument when creating a Sundial constructor yourself. However, this will mean that the app surface ends up drawing over Sundial during a naive post-draw cycle, so you'll then have to manage either separate surfaces, or handle turning off the app surface drawing yourself.
{: .warning}

---

## Loading your preset

`SundialImport()` loads whichever preset you marked as **Default** in the Visual Editor:

```js
sundial = SundialImport();
```

The Sundial struct you get back already has the settings you made in the editor, including its colours, brightness, timings and time settings.

If you've made several presets, you can choose which on to load by supplying its name as a string:

```js
sundial = SundialImport("Winter");
```

> If Sundial can't find the name of the preset you asked for, it will error, so make sure you type your strings correctly!
{: .warning}

---

## Drawing Sundial

Most games can simply call `Draw()` from a **Post Draw Event**:

```js
sundial.Draw();
```

Sundial then colour grades what GameMaker has drawn to the app surface, then draws the graded result on screen at the correct position and size.

You don't need to pass `application_surface` yourself, and you don't need to work out how GameMaker has scaled it to the window, as Sundial will handle that for you.

Anything you draw later in **Draw GUI** will not be graded.

The no-argument `Draw()` is intended for Post Draw. If you call it from another event and you don't supply a custom surface, Sundial will throw (this is because Sundial cannot draw the app surface while the app surface is the active draw target).

You can also supply the x and y and width and height arguments if you so wish.

---

## Auto Time

Unless your game already has its own clock, the easiest option is to simply leave **Auto Time** turned on in the Visual Editor and set the **Start Time** and **Day Length** there.

That way, Sundial itself will manage the flow of time in your game.

If your game already keeps track of time, leave Auto Time off and use `SetTime()` to pass that time to Sundial instead.

For manual time control, period callbacks, reading the current time, or using `GetSunlightAmount()`, see **[Time, Periods & Callbacks](time-periods-and-callbacks)**.

---

## Drawing your own surface

Most games can just use the Post Draw setup above.

If your game already draws everything to its own surface (perhaps you have a lighting system, or something else like that where you're taking control of the drawing process), you can give that surface to Sundial instead:

```js
sundial.Draw(game_surface);
```

Or choose exactly where and how large it should be drawn:

```js
sundial.Draw(game_surface, x, y, width, height);
```

This is mainly for games that already have their own surface setup. You don't need to create a surface just to use Sundial.

---

## Where to go next

If your game needs something slightly more complex than this basic setup, then check out one of these pages.

See **[Time, Periods & Callbacks](time-periods-and-callbacks)** if your game needs to control or react to the time of day.

See **[Indoor & Outdoor Grading](indoor-and-outdoor)** if different parts of the scene need different grading.

See **[Configuring Sundial in Code](manual-configuration)** if you want to set Sundial up without using the IDE plugin.
