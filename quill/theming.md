---
layout: default
title: Theming
parent: Quill
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

# Theming Guide

Quill has a variety of ways to theme your textboxes. You can set a global theme, and also set an theme and override individual theme settings per textbox. The global theme is set via `QuillSetTheme(...)` (and you can retrieve the currently set theme with `QuillGetTheme()`), and per-textbox themes are set via the method `box.SetTheme(...)`, and each textbox also has a variety of methods to let you set a single setting, such as `box.SetLabelFont()`.
## Theme Resolution Order

For each textbox, style values resolve in this order:

First, per-textbox override values (`box.overrides.<subtheme>.<field>`). If you set any of these, they will always take precedence.
Next, the per-textbox theme (`box.theme`, if set with `SetTheme(new QuillTheme())`) is checked.
Finally, it falls back to the global theme (`QuillGetTheme()` or `QUILL.GetTheme()`) if any necessary settings haven't been touched by either of the two former.

First, let's go through the quickest and dirtiest way to apply unique theming elements to your textboxes. This will let you get a textbox up and running fast, by simply changing a few settings from the default Quill theme.

## Quick Global Theme Example

This is a quick and dirty way of creating a unique global theme. First create a "default" Quill theme, then simply override some of the settings manually. This is quick and easy, but can be kind of tricky to work with as you will usually have to look up what the fields are every time you want to do this (ain't nobody got time to remember exact theme settings, lol).

```js
var _theme = new QuillTheme();
_theme.textbox.text_col = c_white;
_theme.textbox.placeholder_col = c_gray;
_theme.skins.prim_bg_idle_col = make_colour_rgb(24, 24, 24);
_theme.skins.prim_border_idle_col = make_colour_rgb(96, 96, 96);
_theme.menu.item_hover_col = make_colour_rgb(64, 64, 64);

QuillSetTheme(_theme);
```

## Per-Box Theme Example

Again, a quick and dirty way of applying a unique theme to a specific textbox.

```js
var _danger_theme = new QuillTheme();
_danger_theme.skins.prim_border_idle_col = make_colour_rgb(200, 70, 70);
_danger_theme.textbox.validation_error_col = make_colour_rgb(255, 90, 90);

error_box.SetTheme(_danger_theme);
```

Pass `-1` to `SetTheme` to return to the global theme fallback:

```js
error_box.SetTheme(-1);
```

## Per-Box Style Override Methods

If you've got a theme set that you already like, but want to make a change or two for a specific textbox, use the override setters instead of making a new theme: `tb.SetLabelFont(font)`. There's a full listing of the overrides you have access to in the Scripting Reference page.

## Theme Constructors

Quill exposes a root theme plus a set of subthemes. These are the constructors you'll use:

The default Quill Theme constructor:

```js
QuillTheme()
```
This builds a full theme struct, and if you make any custom themes, you should *always* inherit from this default theme, like this:

```js
function MyCustomTheme() : QuillTheme() {
	// Theming code
}
```
This is because Quill runs a check to see if a theme you provide is valid, and that check compares the theme against the `QuillTheme` constructor (which returns true if it inherits from it).

Each "category" of settings in a Quill theme is its own struct, and these structs are made via the Subtheme constructors, listed here:

```js
QuillFontSubtheme()
QuillTextboxSubtheme()
QuillLabelSubtheme()
QuillSkinSubtheme()
QuillSelectionSubtheme()
QuillCaretSubtheme()
QuillScrollbarSubtheme()
QuillMenuSubtheme()
QuillEditorSubtheme()
```
Again, if you make any subthemes for yourself, you should *always* inherit from the appropriate subtheme constructor, just like with the default theme.

Lets make a custom font subtheme, and a custom theme that uses that font subtheme.

```js
// First, we'll make the font subtheme, making sure that we inherit from QuillFontSubtheme.
// We'll only change the body and label fonts for this custom theme, the others will be automatically set
// to the defaults in QuillFontSubtheme via the inheritance
function CustomFontSubtheme() : QuillFontSubtheme() {
	body = fnt_text_body; // We need to use the name of font assets we have created in the GM editor
	label = fnt_label_body;
}

// Now that we have our custom font theme, we can create a custom theme, inheriting from QuillTheme.
function CustomTheme() : QuillTheme() {
	// And we simply call the SetFonts() method, building a custom font struct from our CustomFontSubtheme
	// constructor and supplying it as the argument.
	SetFonts(new CustomFontSubtheme());
}
```
That's it, we've now got a `CustomTheme` that inherits all the defaults from the `QuillTheme`, but changes the body and label fonts. Obviously, if that's all you wanted to change, it's a bit easier to just use the quick and dirty method I outlined above, but this gets very useful once you start, for instance, having different skins while still wanting the same fonts to be applied across a variety of custom themes.

You'd create the custom font subtheme once, and then create a bunch of custom skin subthemes, and then you can build out a number of custom themes, mixing and matching with the different subthemes you've created.

It makes it simpler to port between projects as well. Think of it as building up a library of thematic styles that you like, which you can carry from game to game, making small tweaks here and there via the override settings.

I've also included a few preset themes in the repo:

```js
QuillTheme_VoidMango()
QuillTheme_ChunkyCandy()
```

## Theme Subtheme Setters

We've already used a subtheme setter in the example above. The full list of subtheme setters is `SetFonts(...)`, `SetTextbox(...)`, `SetLabel(...)`, `SetSkins(...)`, `SetSelection(...)`, `SetCaret(...)`, `SetScrollbar(...)`, `SetMenu(...)`, and `SetEditor(...)`.

If you're happy mostly happy with the defaults, another way of setting up themes is this:

```js
var _fonts = new QuillFontSubtheme();
_fonts.body = fnt_ui_body;
_fonts.label = fnt_ui_label;

var _theme = new QuillTheme()
	.SetFonts(_fonts);

QuillSetTheme(_theme);
```

Here we're kind of merging the "quick and dirty" method with the full "build out proper subthemes and custom themes" method. Instead of creating a completely new custom font subtheme and custom theme, we instead build out a font subtheme struct from the default constructor, apply the few changes that we want, and then build out a default theme and apply that edited fonts subtheme to it (we also use fluid chaining). Then we can just apply the new theme globally.

## High-Value Fields By Subtheme

If you're not sure where to start, these are the fields people touch most often.

For `fonts`, you'll usually set `body`, `code`, `label`, `menu`, `editor_title`, `editor_body`, and `validation`.

`fonts.code` is the default text font for any textbox in `QUILL_TEXTMODE_CODE` (single-line, multiline, and overlay editor textbox content).

For `textbox`, focus on padding (`pad_l`, `pad_t`, `pad_r`, `pad_b`), text colors (`text_col`, `placeholder_col`, `disabled_text_col`), and validation colors (`validation_error_col`, `validation_warn_col`, `validation_info_col`).

For `label`, common knobs are padding/margins, text color/alpha, and optional sprite slots (`bg_spr`, `border_spr`) including `border_spr_outside_draw` when using Nine Slice borders. When `border_spr_outside_draw` is `false`, the label reserves the border Nine Slice edges inside the panel before placing text.

For `skins`, you'll often set sprite slots (`bg_spr`, `border_spr`, `caret_spr`, `resize_spr`), border sprite behavior (`border_spr_outside_draw`), fallback primitive colors for idle/hover/active/disabled/invalid, and border thickness. When `border_spr_outside_draw` is `false`, textbox content is inset by the border Nine Slice edges so text/caret/selection stay clear of border art.

For `selection` and `caret`, you're mostly configuring selection background (and optional text tint) plus caret color, alpha, width, and blink timing.

For `scrollbar`, the common knobs are width, padding, thumb minimum, track/thumb/border colors, and `border_spr_outside_draw` when using a Nine Slice border sprite. The same scrollbar theme drives both vertical and horizontal multiline bars.

For `menu`, you'll likely touch item size, paddings, min/max width, viewport margin, panel colors, hover colors, text colors, separator style, and `border_spr_outside_draw` for Nine Slice border sprites. With inside-draw borders, menu row layout reserves those inside border edges automatically.

For `editor`, you'll usually set the dim background style, panel min/max sizes and paddings, button colors and dimensions, and `panel_border_spr_outside_draw` for Nine Slice panel border sprites. With inside-draw borders, title/buttons/editor lane are inset away from the panel border edges.

## Professional Notes

Set a global baseline once, then use per-box overrides for targeted UI variation. Try not to mutate theme every frame; configure it the UI setup time, such as your Create Event. Also, keep color and alpha decisions centralized in theme structs so it's easy to restyle later.
