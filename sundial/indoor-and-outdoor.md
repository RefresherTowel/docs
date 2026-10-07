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

A full-screen colour grade works nicely until the camera can see both a sunset and the inside of a house at the same time.

The sky should be turning orange. The grass can pick up that warmth too. The room inside the house probably shouldn't suddenly look like somebody filled it with orange fog.

Sundial handles that split with a mask.

---

## The mask chooses indoor and outdoor pixels

Give Sundial a surface the same size as the source surface you're grading:

```js
sundial.SetMask(indoor_mask_surface);
```

Sundial reads the **red channel** of that surface:

```text
black      = outdoor
white      = indoor
50% grey   = halfway between outdoor and indoor
```

The blend is proportional, so the mask doesn't have to be only pure black and white. Soft edges or partially covered pixels can transition between the two treatments cleanly.

The green, blue and alpha channels don't affect the indoor amount. If you're generating the mask yourself, treating it as a simple greyscale surface is normally the least confusing option.

---

## The mask must match the source surface

If you're grading `application_surface`, the mask needs the same width and height as `application_surface` when `Draw()` runs.

Sundial checks this because a differently sized mask would no longer describe the same pixels:

```text
source pixel (500, 300)
        needs to match
mask pixel   (500, 300)
```

If the dimensions don't match, `Draw()` reports an error rather than stretching the mask and producing something that looks vaguely plausible but is spatially wrong.

How you create the mask is up to your renderer. A room system might draw visible interiors into it, a tilemap-driven game might build it from indoor tiles, or a simpler game might only need a few solid shapes.

Sundial only cares about receiving the finished same-sized surface.

---

## The game owns the mask surface

`SetMask()` stores the surface handle. It doesn't copy the surface or take over its lifetime.

That means the usual GameMaker surface rules still apply. If the surface is lost or destroyed, recreate it and give Sundial the new handle:

```js
if (!surface_exists(indoor_mask_surface)) {
    indoor_mask_surface = surface_create(
        surface_get_width(application_surface),
        surface_get_height(application_surface)
    );

    // Rebuild the mask here.
    sundial.SetMask(indoor_mask_surface);
}
```

You can ask whether Sundial's current mask still exists:

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

## Indoor colour is its own base grade

The outdoor scene moves through the six Morning, Day, Afternoon, Dusk, Night and Dawn grades.

Indoors don't need six more authored colours. Instead, Sundial starts indoor pixels from one base indoor grade:

```js
sundial.SetIndoorGrading(make_color_rgb(230, 220, 205));
```

Then choose how strongly that colour should affect the interior:

```js
sundial.SetIndoorGradingStrength(0.8);
```

Just like outdoor grading strength, this value can go above `1` when you deliberately want to exaggerate the colour bias.

If there is no mask, these indoor settings don't change the output because every source pixel is treated as outdoor.

---

## Daylight influence keeps interiors connected to outside

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

## Indoor brightness has separate Day and Night values

Set the indoor Day and Night brightness together:

```js
sundial.SetIndoorBrightness(0.85, 0.55);
```

Sundial continuously blends between those two values using the same sunlight amount that drives outdoor brightness.

This lets an interior stay darker than outdoors during the day without becoming unreadably dark at night, or do the opposite if that's what the scene needs.

For example:

```js
sundial
    .SetBrightness(1.1, 0.35)
    .SetIndoorBrightness(0.8, 0.6);
```

makes the outdoor world change much more strongly between Day and Night while keeping the interior in a narrower brightness range.

---

## Preview masks and runtime masks are separate

The IDE's **Import Preview Mask** button exists so you can see indoor/outdoor behaviour on the screenshot while you're authoring a preset.

That mask is not automatically used by the game.

The screenshot and preview mask are editor-only files. Runtime masks usually need to follow the current room, camera and visible interiors anyway, so the game supplies the real surface with `SetMask()`.

The semantics are the same in both places:

```text
black = outdoor
white = indoor
red channel = blend amount
```

So the preview is still showing the same grading maths the runtime will use once your game provides the corresponding mask.

---

## A simple masked setup

A complete setup might look roughly like this:

```js
sundial = SundialImport();
sundial.SetMask(indoor_mask_surface);
```

Then the normal draw call doesn't change:

```js
sundial.Draw(application_surface);
```

Sundial sees that a valid mask exists and blends the outdoor and indoor multipliers per pixel while drawing the source.

You don't need a separate outdoor draw pass and indoor draw pass. The mask is what tells the one Sundial draw which treatment each pixel should receive.

---

## Next: Configuring Sundial in Code

If you're using the IDE, you may already have all the grading configuration you need. The next page is mainly for people who want to build or alter the complete setup programmatically.

Continue with **[Configuring Sundial in Code](manual-configuration)** for grading anchors, strengths, brightness and cycle timing without relying on an authored preset.
