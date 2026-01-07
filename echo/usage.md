---
layout: default
title: Usage and Examples
parent: Echo
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

# Usage and Examples

Echo is the logger. Echo Chamber is the thing you can *look at* while you are logging (plus a bunch of other UI goodies for your own tools).

You can use either one on its own, but together they turn "show_debug_message hell" into an actual workflow.

---

## Echo

### The 10 second setup

Add `scr_echo.gml` to your project and then log something:

```js
EchoDebugInfo("Hello from Echo!");
EchoDebugWarn("This smells suspicious...", "AI");
EchoDebugSevere("Something exploded.", ["Combat", "Damage"]);
```

- `EchoDebugInfo` and `EchoDebugWarn` are just convenience wrappers.
- `EchoDebugSevere` includes a stack trace (and stack traces can also be enabled for everything, see levels below).
- The third argument can be a single tag string or an array of tag strings.

### Picking a log level (so you are not drowning)

Echo logs have an urgency (INFO, WARNING, SEVERE), and Echo itself has a filter level.

```js
EchoDebugSetLevel(eEchoDebugLevel.COMPREHENSIVE);
```

The levels are:

- `eEchoDebugLevel.NONE` -> logs nothing
- `eEchoDebugLevel.SEVERE_ONLY` -> only `SEVERE`
- `eEchoDebugLevel.COMPREHENSIVE` -> `WARNING` + `SEVERE` (this is the default)
- `eEchoDebugLevel.COMPLETE` -> everything, and all logs include stack traces

So if you want "only the scary stuff", use `SEVERE_ONLY`.
If you want "I am hunting a heisenbug", use `COMPLETE`.

### Tag filtering (so you can mute the noisy subsystems)

You can whitelist tags. An empty allowed-tags array means "allow everything".

```js
EchoDebugSetTags(["UI", "Combat"]); // only these log
// ...
EchoDebugClearTags(); // back to allowing all
```

Tags are simple strings. Use whatever makes sense for your project:
`"UI"`, `"Net"`, `"AI"`, `"Loot"`, `"Save"`, `"Audio"`, etc.

### History and dumping

Echo keeps a history buffer so a UI can render it (Echo Chamber's console uses this).

Some handy calls:

```js
EchoDebugSetHistorySize(500); // 0 means "do not trim" (unbounded)
var _history = EchoDebugGetHistory();
var _structured = EchoDebugGetStructuredHistory();

EchoDebugDumpLog(); // writes a timestamped text file
```

If you are leaving Echo running for a long play session, set a history size.
Unbounded history is fine for short sessions, but it *will* grow forever if you let it.

---

## Echo Chamber

Echo Chamber is a debug UI builder. The point is not "a single built-in debugger".
The point is "make your own tools quickly, in-game, without writing a bespoke UI system".

### Minimal setup (run this in Draw GUI)

Create a root once, then run it every frame.

```js
// Create Event (or a controller object Create)
global.echo_ui = new EchoChamberRoot(new EchoChamberThemeMidnightNeon());

// Draw GUI Event
global.echo_ui.RunDesktop();
```

That is the whole "boot" sequence.

If you do nothing else, you have a desktop that can host windows. Now you add windows.

### Open the built-in Echo console (fastest payoff)

Echo Chamber ships with a console window for Echo.

```js
// Call this once when you want it (e.g. F1, a menu button, etc)
EchoChamberOpenConsole(global.echo_ui);
```

Now your `EchoDebug...()` calls are visible in a real in-game console.
No copy/pasting from the Output window. No scrolling through 800 lines of noise.

### Build a tiny custom window (labels, toggles, sliders, buttons)

A window contains panels. Panels contain controls.

Here is a "Debug Settings" window that binds controls to your own config struct:

```js
// Create Event
global.debug_cfg = {
	god_mode	: false,
	damage_mult	: 1.0,
	player_name	: "Drew"
};

var _win = global.echo_ui
	.CreateWindow("dbg_settings")
	.SetTitle("Debug Settings")
	.SetRect(32, 32, 420, 260);

var _panel = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_win.AddPanel(_panel);

_panel.AddControl(new EchoChamberLabel("lbl").SetText("Tweaks for testing:").UseSmallFont());

_panel.AddControl(new EchoChamberToggle("tog_god")
	.SetLabel("God mode")
	.BindBool(global.debug_cfg, "god_mode")
);

_panel.AddControl(new EchoChamberSlider("sld_dmg")
	.SetLabel("Damage multiplier")
	.SetRange(0.1, 5.0)
	.SetStep(0.1)
	.BindValue(global.debug_cfg, "damage_mult")
);

_panel.AddControl(new EchoChamberTextInput("txt_name")
	.SetLabel("Player name")
	.SetPlaceholder("type here...")
	.BindText(global.debug_cfg, "player_name")
);

_panel.AddControl(new EchoChamberButton("btn_ping")
	.SetLabel("Ping")
	.OnClick(function() {
		EchoDebugInfo($"Ping! dmg_mult={global.debug_cfg.damage_mult}", "UI");
	})
);
```

A couple of important notes:

- Binding can target a struct field, and some controls also accept getter/setter functions.
	- Sliders, toggles, and labels support method-bound getters/setters.
	- Text inputs and dropdowns still bind to struct fields.
	- If you want to affect instances, use method-bound callbacks or getters/setters with your own checks.
- Most setters return `self`, so you can chain them.

### Layout persistence (save window positions between runs)

Echo Chamber can save and load layout to an ini file. The typical flow is:

1) Create your windows/panels/controls
2) Call `LoadLayout()` once
3) Call `SaveLayout()` when you want (e.g. when the player exits, or when closing a tool window)

```js
// After building your UI
global.echo_ui
	.SetPersistenceFile("echo_chamber_layout.ini")
	.SetPersistenceSection("my_game_debug")
	.LoadLayout();

// Later, when you want to save
global.echo_ui.SaveLayout();
```

Important: load happens after the windows exist.
Echo Chamber is not a UI "serializer"; it is a layout restorer.

### Themes (and making your own)

Echo Chamber uses a theme struct for colors, fonts, spacing, and style variants.

You have a few built-in themes:

- `new EchoChamberTheme()` (base theme)
- `new EchoChamberThemeMidnightNeon()`
- `new EchoChamberThemeAmberForest()`
- `new EchoChamberThemeSakuraPunch()`
- `new EchoChamberThemeArcadeWave()`
- `new EchoChamberThemeCircuitCandy()`
- `new EchoChamberThemeToxicTerminal()`
- `new EchoChamberThemeSunsetGlitch()`
- `new EchoChamberThemeBubblegumTerminal()`
- `new EchoChamberThemeMangoMint()`

#### Option A: tweak an existing theme

This is the lowest-effort way to get your own flavor:

```js
var _theme = new EchoChamberThemeMidnightNeon();

// Swap fonts if you want
_theme.font_body = fnt_my_body;
_theme.font_header = fnt_my_header;

// Make accents louder
_theme.col_accent = make_color_rgb(255, 100, 180);

// Recompute derived metrics after changing fonts
_theme.RefreshMetrics();

global.echo_ui = new EchoChamberRoot(_theme);
```

#### Option B: make a full custom theme function

This is basically "theme as a constructor".

```js
function EchoChamberThemeMyTheme() : EchoChamberTheme() constructor {
	col_window_bg = make_color_rgb(18, 18, 22);
	col_panel_bg  = make_color_rgb(24, 24, 30);
	col_accent    = make_color_rgb(120, 200, 255);

	// Add a custom button style variant
	button_styles[$ "danger"] = {
		bg			: make_color_rgb(60, 20, 20),
		border		: make_color_rgb(255, 80, 80),
		bg_alpha	: 1,
		hover		: make_color_rgb(90, 30, 30),
		align		: "center"
	};

	RefreshMetrics();
}
```

Then use it like:

```js
global.echo_ui = new EchoChamberRoot(new EchoChamberThemeMyTheme());
```

And apply the style on a button:

```js
_panel.AddControl(new EchoChamberButton("btn_delete")
	.SetLabel("Delete Everything")
	.SetControlStyleKey("danger")
	.OnClick(function() {
		EchoDebugWarn("You almost clicked it.", "UI");
	})
);
```

#### About theme storage for other tools

The theme includes a `statement` field used by Statement Lens.
You do not need it unless you are using Statement.

The idea is simple though: a theme is just a big organized settings struct.
If you build your own debug interfaces on top of Echo Chamber, you can store your own tool-specific theme settings in the same way (exactly like Statement does).

---

## Custom drawing (SetContentDrawer)

Ok, so controls are great for 90% of debug UI. But sometimes you want to draw something that is not a button, not a slider, not a text input. You want a tiny inspector, a graph, a list, a timeline, a minimap, a heatmap, whatever.

That is what panel content drawers are for. You give a panel a function, and that function draws the inside of the panel every frame.

Here is a small example: a custom panel that draws a scrollable list of your last Echo lines.

```js
// Create Event
var _win = global.echo_ui
	.CreateWindow("dbg_echo_mini")
	.SetTitle("Echo Mini")
	.SetRect(480, 32, 520, 320);

var _panel = new EchoChamberPanel("mini", eEchoChamberDock.FILL);
_win.AddPanel(_panel);

// This value lives in a struct so Echo Chamber can bind to it safely
global.echo_mini_state = {
	scroll_y	: 0
};

_panel.SetContentDrawer(function(_ctx) {
	// Grab the log lines (plain history strings)
	var _lines = EchoDebugGetHistory();

	// Padding inside the panel
	var _pad = 8;
	var _x = _ctx.x + _pad;
	var _y = _ctx.y + _pad;
	var _w = _ctx.w - _pad * 2;
	var _h = _ctx.h - _pad * 2;

	// Basic line layout
	var _line_h = 16;
	var _total_h = array_length(_lines) * _line_h;

	// Clamp scroll so it does not drift into the void
	global.echo_mini_state.scroll_y = clamp(
		global.echo_mini_state.scroll_y,
		0,
		max(0, _total_h - _h)
	);

	// Apply scroll offset
	var _draw_y = _y - global.echo_mini_state.scroll_y;

	// Draw the visible lines only
	for (var _i = 0; _i < array_length(_lines); _i++) {
		var _ly = _draw_y + _i * _line_h;

		// Quick cull
		if (_ly < _y - _line_h) continue;
		if (_ly > _y + _h) break;

		draw_text(_x, _ly, _lines[_i]);
	}

	// Scroll wheel support (only when hovered)
	// NOTE: This uses a generic "mouse wheel delta" idea. If your project stores wheel input differently,
	// just replace _wheel with your own value.
	var _wheel = mouse_wheel_up() - mouse_wheel_down();
	if (_ctx.is_hovered && _wheel != 0) {
		global.echo_mini_state.scroll_y -= _wheel * _line_h * 3;
	}
});
```

A couple of notes:

- The `_ctx` argument is the panel draw context: x/y/w/h, hover state, theme, and whatever other helpers Echo Chamber provides.
- This example uses the plain string history for simplicity. If you want colors, severity icons, tags, and stack trace expand/collapse, use the structured history.
- The scroll is just a number. Keep it in a struct (like `global.echo_mini_state`) so you can bind it, clamp it, and not lose it between frames.

Once you have this pattern, you can build basically any tool UI you want.

---

## Where to go next

- If you have not already: open the built-in Echo console window and get a feel for what "real" debug output looks like in-game.
- Make sure to look over the API reference page to see all the possible options you have available to you.
- If you are building a bigger tool: start experimenting with panels that mix controls + a custom drawer (controls on the left, live visual on the right is a classic combo).
- Finally: try making a custom theme. Even tiny changes (fonts + accent color) make your tools feel like part of your game instead of a bolted-on dev menu.
