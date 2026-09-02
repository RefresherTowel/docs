---
layout: default
title: Themes
parent: Echo Chamber
nav_order: 3
redirect_from:
  - /echo/echo_chamber/themes.html
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Themes

You can ignore styling completely while you're getting a debug tool working. Echo Chamber already has a usable default look. But sometimes you just wanna make stuff look slick or fit in with your game, because hey, why not?

There are three common styling decisions:

- "I want this whole debug desktop to use a different look."
- "I want every destructive button to share one special look."
- "I only want this one button or panel to be different."

Echo Chamber handles each of those jobs at a different styling level.

---

## Start with a built-in theme

If you want the whole debug desktop to change together, use a **theme**. A theme contains the fonts, colours, spacing, sizing, and control styles that give the windows on one Echo Chamber root a consistent appearance.

Echo Chamber includes these theme constructors:

- `EchoChamberTheme()`
- `EchoChamberThemeMidnightNeon()`
- `EchoChamberThemePhosphorTerminal()`
- `EchoChamberThemeBiohazardConsole()`
- `EchoChamberThemeEmeraldUltraviolet()`
- `EchoChamberThemeAmberForest()`
- `EchoChamberThemeSakuraPunch()`
- `EchoChamberThemeArcadeWave()`
- `EchoChamberThemeCircuitCandy()`
- `EchoChamberThemeToxicTerminal()`
- `EchoChamberThemeSunsetGlitch()`
- `EchoChamberThemeBubblegumTerminal()`
- `EchoChamberThemeMangoMint()`

To make the shared root use Mango Mint:

```js
GetEchoChamberRoot().ApplyTheme(new EchoChamberThemeMangoMint());
```

Read it from the inside out: `new EchoChamberThemeMangoMint()` constructs the theme, `GetEchoChamberRoot()` gets the shared debug desktop, and `ApplyTheme(...)` tells that root to use the new theme for its ordinary windows, panels, controls, popups, and other themed UI.

Applying another theme later switches the root again. You don't need to recreate all of your windows just to change their shared look.

### The built-in debugger keeps its own look

Echo Console and the other bundled debugger windows deliberately use a separate window-level theme instead of blindly following whatever theme your ordinary root currently uses. The macro that chooses that debugger theme is:

```js
#macro ECHO_CHAMBER_DEBUG_THEME eEchoChamberDebugTheme.EMERALD_ULTRAVIOLET
```

The available debugger choices are `PHOSPHOR_TERMINAL`, `BIOHAZARD_CONSOLE`, and `EMERALD_ULTRAVIOLET`. They correspond to the public theme constructors with the same names.

Your custom tuning tools can use a project-specific theme while the built-in debugger keeps a familiar, readable appearance. Changing the root theme doesn't unexpectedly recolour Echo Console, and changing the debugger macro doesn't restyle every custom window you made.

---

## Change a theme-wide font

Sometimes the overall theme is fine and only the fonts feel wrong for your project. Themes have shared body, header, and small-font roles so you can change those broad choices without editing every style object individually.

The `fnt_*` names in this example stand for GameMaker font assets from your own project. Replace them with fonts that actually exist in your game:

```js
var _theme = new EchoChamberThemeMidnightNeon();

_theme
	.SetBodyFont(fnt_debug_body)
	.SetHeaderFont(fnt_debug_header)
	.SetSmallFont(fnt_debug_small);

// Give buttons their own font before changing the shared small-font role again.
_theme.button_styles.Default().SetFont(fnt_button_special);
_theme.SetSmallFont(fnt_debug_small_alt);
```

`new EchoChamberThemeMidnightNeon()` gives `_theme` a complete starting theme.

`SetBodyFont()`, `SetHeaderFont()`, and `SetSmallFont()` replace the three shared font roles. Styles that are still following one of those roles update when the role changes.

The last two lines demonstrate the exception. `_theme.button_styles.Default()` gets the normal button style used by that theme. `SetFont(fnt_button_special)` gives that button style an explicit font of its own. After that explicit override, the later `SetSmallFont(fnt_debug_small_alt)` can update styles that still follow the shared small-font role, but it doesn't replace the button font you deliberately set to `fnt_button_special`.

So use the theme font setters when the intent is "change this font role everywhere that still follows it". Edit one style's font directly when that particular kind of UI should stop following the shared role.

---

## Reuse one special look

Suppose most buttons should use the normal theme, but every destructive action should have the same dark red appearance. Styling every Delete button separately would duplicate the same choices all over your debug UI.

Instead, give that reusable button look a name once, then let any button ask for it:

```js
var _root = GetEchoChamberRoot();
var _theme = new EchoChamberThemeMidnightNeon();

_theme.button_styles.Set("danger", new EchoButtonStyle()
	.SetBgColour(make_color_rgb(70, 20, 20))
	.SetBorderColour(make_color_rgb(255, 80, 80))
	.SetTextColour(c_white)
);

_root.ApplyTheme(_theme);

var _win = _root
	.CreateWindow("theme_variant_example")
	.SetTitle("Theme Variant")
	.SetRect(32, 32, 320, 180);

var _panel = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_win.AddPanel(_panel);

_panel.AddControl(new EchoChamberButton("delete")
	.SetCaption("Delete")
	.SetStyleKey("danger")
);
```

The first two lines get the shared root and create a Midnight Neon theme to customise before applying it.

`_theme.button_styles` is the theme's collection of button looks. `Set("danger", ...)` adds a reusable look under the name `"danger"`.

The value being stored is a new `EchoButtonStyle`. Its three setters change the background, border, and text colours for that named look. The style doesn't have to repeat every other button setting such as padding, font, or sizing. Anything you don't override will still come from the normal/default button style.

`_root.ApplyTheme(_theme)` makes the root use the theme that now contains the named `"danger"` button style.

The rest of the example creates a normal window and fill panel. The Delete button uses `SetStyleKey("danger")`, which asks the active theme for its named danger button style. The button still behaves like an ordinary `EchoChamberButton`. The style key changes its appearance, not its click semantics.

Other styled UI types work the same way. Each type has a collection with one normal/default style plus any named alternatives you add. Echo Chamber calls that collection a **style family**. Define a reusable special look once, then refer to it by name from several controls of the same kind.

Because named styles only need to contain the fields they actually change, the style reference describes them as **sparse** styles. In ordinary terms, your `"danger"` style can say "only change these three colours" and let the normal button style supply the rest.

Style families provide `Default()`, `Set()`, `Get()`, `Has()`, `Remove()`, and `ClearVariants()` when you need to manage those named looks directly.

---

## Change just one control

A named look is useful when several controls should share it. If only one button, panel, or window needs an exception, changing that one object directly is simpler than inventing a style key that nothing else will use.

This example makes local changes at three different levels:

```js
var _window = GetEchoChamberRoot()
	.CreateWindow("local_style_example")
	.SetTitle("Local Styles")
	.SetRect(32, 32, 340, 200);

var _panel = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_window.AddPanel(_panel);

var _button = new EchoChamberButton("launch")
	.SetCaption("Launch");

_button.Style()
	.SetBgColour(make_color_rgb(30, 60, 90))
	.SetTextColour(c_white);

_panel.AddControl(_button);

_panel.Style()
	.SetGap(8)
	.SetRowHeight(28);

_window.Style()
	.Body()
	.SetClampMargin(12);
```

The first part creates an ordinary window and fill panel, then constructs a Launch button.

`_button.Style()` gets the local style override belonging to this particular button. `SetBgColour()` and `SetTextColour()` therefore affect the Launch button without changing other buttons in the theme.

`_panel.Style()` does the same thing at the panel level. `SetGap(8)` changes the spacing between controls in this panel and `SetRowHeight(28)` changes this panel's row height. Another panel on the same root keeps its own normal style.

Windows have more than one styled piece: the body, header, and chrome buttons can differ. `_window.Style()` returns the window's style surface, and `.Body()` selects the body part of that surface. `SetClampMargin(12)` changes the margin Echo Chamber uses when clamping this window so a usable part of its title bar stays within the debug desktop. Other windows keep the theme's normal clamp margin.

Match the styling level to the scope of the change:

- Change the root theme when a whole debug desktop should change together.
- Add a named style when several things of the same kind should reuse one special look.
- Call `.Style()` when one particular object needs an exception.

Those levels can be combined. A button can use the theme's defaults, select a named theme style, and still have a local override for one final field.

---

## Give one window a different theme

Sometimes the exception is bigger than one control. A specialist profiler or visual editor may need its own complete theme while the rest of the debug desktop keeps using the normal root theme.

Keep the window reference if you plan to change or remove that special theme later:

```js
/// obj_debug_controller Create
specialist_window = GetEchoChamberRoot()
	.CreateWindow("specialist_tool")
	.SetTitle("Specialist Tool")
	.SetRect(32, 32, 420, 260);

specialist_window.ApplyTheme(new EchoChamberThemeAmberForest());
```

The first four calls create the window normally. `specialist_window` is an instance variable here because the later code needs the same window reference after Create has finished.

`specialist_window.ApplyTheme(new EchoChamberThemeAmberForest())` gives *that window* a theme override. Its panels and controls use the window's theme while other windows on the root continue following the root theme.

When the specialist window should go back to following the root again:

```js
specialist_window.ClearThemeOverride();
```

`ClearThemeOverride()` removes the window-specific theme. It doesn't delete the window or change the root's theme. The window simply goes back to following the root theme.

Echo Console uses the same general window-level idea for the debugger theme described earlier.

---

## Build a reusable custom theme

If your changes add up to a complete look that you'll reuse across several tools or projects, put them in your own theme constructor rather than repeating setup code every time.

A convenient starting point is to inherit from a built-in theme and then change the parts that belong to your project:

```js
function EchoChamberThemeMyGame() : EchoChamberThemeMidnightNeon() constructor {
	SetBodyFont(fnt_debug_body);
	SetHeaderFont(fnt_debug_header);

	button_styles.Set("danger", new EchoButtonStyle()
		.SetBgColour(make_color_rgb(70, 20, 20))
		.SetBorderColour(make_color_rgb(255, 80, 80))
		.SetTextColour(c_white)
	);
}
```

`EchoChamberThemeMyGame()` is your new constructor. The `: EchoChamberThemeMidnightNeon()` part runs the Midnight Neon theme constructor first, so your theme begins with a complete set of working styles and metrics instead of starting from nothing.

Inside the constructor, `SetBodyFont()` and `SetHeaderFont()` replace shared font roles just like they did earlier on a theme instance. The `button_styles.Set("danger", ...)` call adds the same kind of reusable named button look, but now it's built into every `EchoChamberThemeMyGame` you create.

Use the constructor like any built-in theme:

```js
GetEchoChamberRoot().ApplyTheme(new EchoChamberThemeMyGame());
```

Constructing `EchoChamberThemeMyGame()` builds the base Midnight Neon theme and then applies your changes. `ApplyTheme()` makes the root use that finished result.

### Lower-level theme fields

The built-in theme constructors also use lower-level fields such as `col_window_bg`, `col_panel_bg`, `col_text`, `col_accent`, `ui_scale`, `default_control_width`, and `tooltip_delay_ms` while they build the finished styles.

Those values are ingredients used during construction, not a permanent CSS-like layer that keeps rewriting every completed style afterward.

For example, changing `col_window_bg` *after* the constructor has already built `window_styles` doesn't automatically search through those finished styles and recolour them. If a lower-level colour should affect the theme's finished styles, change it in your theme constructor directly, or edit the relevant style object directly.

`RefreshMetrics()` recalculates sizing values derived from fonts and other theme measurements. The public font setters already perform the refresh they need. You mainly need `RefreshMetrics()` inside custom theme construction when you directly change lower-level metrics yourself.

`ui_scale` multiplies Echo Chamber's layout measurements, making the debug UI larger or smaller. It doesn't change your game's GUI resolution and it doesn't replace Echo Chamber's underlying screen/canvas coordinate system.

---

## Statement Lens colours

The base theme also contains a `statement` group of colours used by Statement Lens when Statement is installed. Those colours describe things Lens itself draws, such as state cards, connections, activity, selection, and badges.

If your project uses Statement Lens and your custom theme should include Lens colours, set those fields while building the theme. They're theme data that Statement Lens reads, not a separate live styling API that automatically edits Lens after the fact.

---

## Look up fonts and sprites by name

A one-project theme can usually refer directly to the GameMaker font and sprite assets it uses. A reusable theme may instead be given an asset name and need to find the asset in whichever project imported the theme.

`EchoChamberThemeTryGetFont(_font_name)` accepts either a font asset or a font asset name. If a supplied name can't be resolved, the helper falls back to the current draw font.

`EchoChamberThemeTryGetSprite(_sprite_name)` performs the same kind of name lookup for sprites and returns `-1` when no sprite can be found.

These helpers are mainly useful inside reusable theme constructors. For ordinary styling inside one known project, direct asset references are usually simpler.

For the complete list of style constructors, style families, and setters, use the [Style Reference](style-api-reference). The [Scripting Reference](api-reference) contains the exact theme and helper signatures.
