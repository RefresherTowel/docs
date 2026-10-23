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

// Or if you're using a sprite as a mask:
sundial.SetMaskSprite(spr_indoor_mask);
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

`SetMask()` stores the surface handle, and as we GameMakers know, surfaces are volatile and can be destroyed at any point in time. If the surface is lost or destroyed, you'll need to recreate it and give Sundial the new handle:

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

## Making a surface for the indoor mask

I'm not going to go super indepth here, but just as a bit of a primer for what you might want to do:

Create a surface (you want to do this in the Draw Event, as per the GM manual). It's a good idea to make it the same size as your target draw surface (usually the app surface, unless you're manually handling a surface you also want Sundial to draw to).

If you have houses, you might want to create a sprite for their indoor mask according to their shape. Remember, in mask terms, white is **indoors** and black is **outdoors**. So if you have a window in the front of your house that you wanted to light up at night, you'd have the house mask sprite with it's windows coloured white, and the entire rest of the house coloured black.

Then you'd simply draw this house mask sprite to the mask surface at roughly the same time you are drawing your actual houses. The timing doesn't matter too much, as long as all the masks are drawn to the mask surface before the Post Draw Event runs.

`camera_apply()` can be a useful function here, if you are having trouble getting the coordinates of your mask drawing lining up with the actual sprites you want to be masking. Run it immediately after you switch your surface target:

```js
surface_set_target(my_mask_surface);
draw_clear_alpha(c_black, 0); // Clear the mask surface to black with opacity 0
camera_apply(camera_get_active());
// Rest of mask drawing here
surface_reset_target();
```

That's usually enough to get everything lined up so what you are drawing to the mask corresponds exactly to what is being shown on your camera.

You don't need to continuously tell Sundial to use the the masking surface just because you are drawing to it. Just make sure that it exists, and if it doesn't, create it again and **then** hand Sundial the reference for that new mask.

This should be enough to get you started with surfaces and how the mask works. There's lots of educational material out there on exactly how surfaces work, so if this is completely new to you, it'll be a good idea to get comfortable with surfaces before trying to add indoor masking to Sundial.

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

## Using daylight influence to keep interiors visually connected to the outside

A completely fixed indoor grade can look strange when the outside world becomes very dramatically coloured.

For instance, you probably don't want a tavern to turn fully purple because Dawn is purple, but letting it pick up *some* of that colour can make the window light and the room around it feel like they still belong to the same time of day.

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

As I stated during the Visual Editor Plugin page, the Visual Editor's **Import Preview Mask** button exists so you can test out the indoor/outdoor behaviour on the screenshot while you're creating a preset, it does NOT use that mask in the actual game.

So ensure you provide the mask via code in-game when you need to mask out some indoor space.

---

## A basic masked setup

A complete mask setup might look roughly like this:

**Create Event**
```js
sundial = SundialImport();
global.indoor_mask_surface = undefined;
```

**Draw Event**
```js
if (!surface_exists(global.indoor_mask_surface)) {
    global.indoor_mask_surface = surface_create(
        surface_get_width(application_surface),
        surface_get_height(application_surface)
    );
    sundial.SetMask(global.indoor_mask_surface);
}
```

Then you would simply draw to `global.indoor_mask_surface` whenever you want to draw some masking (making sure to run an existence check beforehand).

Easy, wholesome, rustic.

---

## Next: Configuring Sundial in Code

If you're using the Visual Editor plugin, you already have all the grading configuration you need at your fingertips. The next page is mainly for people who want to build or alter the complete setup programmatically without touching the Visual Editor plugin.

Continue with **[Configuring Sundial in Code](manual-configuration)** for grading anchors, strengths, brightness and cycle timing without relying on an authored preset.
