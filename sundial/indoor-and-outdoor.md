---
layout: default
title: Indoor & Outdoor Grading
parent: Sundial
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

# Indoor & Outdoor Grading

A full-screen colour grade works nicely until both indoors and outdoors are visible at the same time, at which point you start to need a little more control.

Let's say it's deep night, the sky is dark purple, the grass is cool and tinged blue, but there are people walking around a room inside a house. That house should *probably* have some light in it. Sundial handles this split with a mask.

---

## The indoor mask

Masking is relatively simple.

Build out a black and white image, either programmatically on a surface or as a presupplied sprite, and then hand Sundial that image:

```js
sundial.SetMask(indoor_mask_surface);

// Or if you're using a prebuilt sprite:
sundial.SetSpriteMask(spr_indoor_mask);
```

Sundial reads that surface/sprite like this:

```text
black      = outdoor
white      = indoor
50% grey   = halfway between outdoor and indoor
```

> Technically, Sundial only cares about the red channel internally, but it's easier to just author everything in greyscale which gives the exact same result.
{: .note}

As you might've noticed, the mask doesn't have to be only pure black and white, you can blend and soften edges to transition between the outdoor and indoor colour grading cleanly.

> A nice effect that you can make with a white to black gradient is to mask out the windows of a house in white, so that the windows are lit up at night, and then have a blended blur to black move outwards from the sharp white of actual window, creating a "indoor light leaking out into the dark" kind of effect.
{: .tip}

---

## Dealing with surfaces

`SetMask()` stores the surface handle, and as we know, surfaces are volatile and can be destroyed at any point in time. If the surface is lost or destroyed, you'll need to recreate it and give Sundial the new handle:

```js
if (!surface_exists(indoor_mask_surface)) {
    indoor_mask_surface = surface_create(
        surface_get_width(application_surface),
        surface_get_height(application_surface)
    );

    
    surface_set_target(indoor_mask_surface);
    // Rebuild the mask here.
    surface_reset_target();

    sundial.SetMask(indoor_mask_surface);
}
```

You don't need to keep track of the surface handle you hand to Sundial if you don't want to as Sundial will hold it for you (although, as I've said above, you still need to make sure the surface hasn't been destroyed or lost). You can ask whether Sundial's current mask still exists:

```js
if (sundial.HasMask()) {
    // A valid mask is currently configured.
}
```

and retrieve the handle with:

```js
var _mask = sundial.GetMask();
```

To return to whole-screen outdoor grading:

```js
sundial.ClearMask();
```

---

## Indoor colour grading

The outdoor scene moves through the six Morning, Day, Afternoon, Dusk, Night and Dawn grades.

Indoors don't deal with an additional six more authored colours. Instead, Sundial starts indoor pixels from one base indoor grade:

```js
sundial.SetIndoorGrading(make_color_rgb(230, 220, 205));
```

And you can choose how strongly that colour should affect the interior:

```js
sundial.SetIndoorGradingStrength(0.8);
```

Just like outdoor grading strength, this value can go above `1` when you deliberately want to exaggerate the colour bias.

If there is no mask, these indoor settings don't change the output because every source pixel is treated as outdoor.

---

## Daylight influence keeps interiors visually connected to outside

A completely fixed indoor grade can look strange when the outside world becomes very dramatic.

A tavern doesn't need to turn fully purple because Dawn is purple, but letting it pick up *some* of that colour can make the window light and the room around it feel like they still belong to the same time of day.

Use `SetIndoorDaylightInfluence()` for that:

```js
sundial.SetIndoorDaylightInfluence(0.25);
```

The value is in the range `0..1`:

```text
0 = use only the indoor base grade
1 = inherit the full resolved outdoor grade
```

Values between those two blend the outdoor colour into the indoor grade.

This setting changes colour influence, not brightness. Indoor brightness has its own controls.

---

## Indoor brightness

Set the indoor Day and Night brightness together:

```js
sundial.SetIndoorBrightness(0.85, 0.55);
```

Sundial continuously blends between those two values using the same sunlight amount that drives outdoor brightness.

This lets an interior stay lighter than outdoors during the night without becoming unbearably bright during the day (or do the opposite if that's the kind of thing you're going for).

For example:

```js
sundial
    .SetBrightness(1.1, 0.35)
    .SetIndoorBrightness(0.8, 0.6);
```

makes the outdoor world change much more strongly between Day and Night while keeping the interior in a narrower brightness range.

---

## Preview masks vs in-game masks

As I stated during the IDE Plugin page, the IDE's **Import Preview Mask** button exists so you can test out the indoor/outdoor behaviour on the screenshot while you're creating a preset, it does NOT use that mask in the actual game.

So ensure you provide the mask via code in-game when you need to mask out some indoor space.

---

## A basic masked setup

A complete mask setup might look roughly like this:

```js
sundial = SundialImport();
sundial.SetMask(indoor_mask_surface);
```

Easy, wholesome, rustic.

---

## Next: Configuring Sundial in Code

If you're using the IDE plugin, you already have all the grading configuration you need at your fingertips. The next page is mainly for people who want to build or alter the complete setup programmatically without touching the IDE plugin.

Continue with **[Configuring Sundial in Code](manual-configuration)** for grading anchors, strengths, brightness and cycle timing without relying on an authored preset.
