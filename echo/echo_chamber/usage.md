---
layout: default
title: Echo Chamber Usage & Examples
nav_order: 3
parent: Echo Chamber
has_children: false
---

<!--
/// usage.md - Changelog:
/// - 23-12-2025: Fixed Echo Chamber usage examples to match current API and callback behavior.
/// - 23-12-2025: Ensure example variables are created in Create before use.
-->

# Usage & Examples

> I'm writing these examples in a bit more of an informal way than the rest of my documentation, mostly because I want to get it out quickly and not be as structured. Let me know if you prefer this style or the "more professional" style of the other usage and examples pages I have for the other frameworks!
{: .note}

So, you've got Echo Chamber in your project, you've peeked at the scripting reference, and now you're thinking:

"Ok sure, I now know that it appears as though code might be involved...but how do I actually build a UI?"

Sweet. Let's do it.

Echo Chamber is a debug UI builder. Think of it like a tiny desktop inside your game: windows, panels, controls, tooltips, toasts, overlays, the whole deal.

And yes, it is debug-first. That doesn't mean you can't use it for a pause menu or an options screen, it just means it hasn't been tuned to be the fastest HUD framework on Earth yet. 

> If you're here because UI in GameMaker is a massive pain in the arse...
> same.
{: .note}

---

## The tiniest possible setup

Let's start with the absolute minimum:

1) Make a root.
2) Make a window.
3) Call `RunDesktop()` every frame in Draw GUI.

Why Draw GUI? Because Echo Chamber is GUI-space UI. You want it to behave like UI, not like a world-space object that accidentally scales with your camera or gets clipped by the room.

Create a controller object (I usually call it something like `obj_debug_controller`) and drop it into your room.

### Create event

```js
// obj_debug_controller: Create

// We'll bind controls to this struct, because binding is lovely and callbacks are optional.
ui_settings = {
	speed: 4,
	god_mode: false,
	player_name: "Drew",
	difficulty_index: 1,
};

// Theme -> Root
var _theme = new EchoChamberThemeMidnightNeon();
ui_root = new EchoChamberRoot(_theme);
// Note: if you have ECHO_DEBUG_ENABLED set to true in the scr_echo script file, you do not need to create a root. Echo automatically creates a root and saves it in global.__echo_chamber_root
// so you can just simply go: ui_root = global.__echo_chamber_root;

// Optional, but you'll thank yourself later.
ui_root.SetPersistenceFile("echo_chamber_demo.ini");
ui_root.SetPersistenceSection("demo");

// Root -> Window
ui_win = ui_root.CreateWindow("demo_main");
ui_win.SetTitle("Echo Chamber Demo");
ui_win.SetRect(40, 40, 560, 540);
```

### Draw GUI event

```js
// obj_debug_controller: Draw GUI
ui_root.RunDesktop();
```

Done and dusted. If you run the game now you won't see much (because we haven't added panels or controls yet), but the desktop runner is alive.

---

## Your first proper window

Right, now let's add some panels and controls.

Echo Chamber's panels are docked. That means you don't do manual pixel math for "left sidebar" and "top bar" every time. You say "LEFT" or "TOP" and the layout engine sorts it out.

We're going to build this layout:

- TOP toolbar panel (row flow)
- LEFT settings panel (column flow, collapsible)
- FILL main panel (column flow)

Add this after the `ui_win` creation in the Create event.

```js
// Panels
var _panel_top = new EchoChamberPanel("top_bar", eEchoChamberDock.TOP);
_panel_top.SetSizeMode(eEchoChamberPanelSizeMode.FIXED);
_panel_top.SetSize(32);
_panel_top.SetFlowMode(eEchoChamberPanelFlow.ROW);
_panel_top.SetGap(6);
ui_win.AddPanel(_panel_top);

var _panel_left = new EchoChamberPanel("left", eEchoChamberDock.LEFT);
_panel_left.SetSizeMode(eEchoChamberPanelSizeMode.FIXED);
_panel_left.SetSize(200);
_panel_left.SetFlowMode(eEchoChamberPanelFlow.COLUMN);
_panel_left.SetCollapseMode(eEchoChamberCollapse.TO_LEFT);
ui_win.AddPanel(_panel_left);

var _panel_main = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_panel_main.SetFlowMode(eEchoChamberPanelFlow.COLUMN);
ui_win.AddPanel(_panel_main);
```

Ok, so what's the big deal here?

The big deal is you just described a classic tool layout without touching a single `x += ...` line.

Now let's sprinkle some controls.

---

## Controls without pain

Echo Chamber controls are little structs. You create them, configure them, then add them to a panel.

### A toolbar button

```js
var _owner = self;
var _btn_console = new EchoChamberButton("btn_console");
_btn_console.SetLabel("Console");
_btn_console.OnClick(method(_owner, function() {
	EchoChamberOpenConsole(ui_root);
	ui_root.ShowToast("Console opened", 1200);
}));
_panel_top.AddControl(_btn_console);
```

### Some bound settings

This is where the real action happens.

Binding means the control writes straight into a struct field for you. No custom Step code, no "did I forget to sync the slider" nonsense.

```js
var _lbl_left = new EchoChamberLabel("lbl_left");
_lbl_left.SetText("Quick settings");
_lbl_left.UseSmallFont(false);
_panel_left.AddControl(_lbl_left);

_panel_left.AddControl(new EchoChamberSeparator("sep_left").SetOrientation("horizontal"));

var _sld_speed = new EchoChamberSlider("sld_speed");
_sld_speed.SetLabel("Speed");
_sld_speed.SetRange(0, 12);
_sld_speed.SetStep(1);
_sld_speed.BindValue(ui_settings, "speed");
_sld_speed.SetTooltip("Tweak movement speed without recompiling your brain");
_panel_left.AddControl(_sld_speed);

var _tgl_god = new EchoChamberToggle("tgl_god");
_tgl_god.SetLabel("God mode");
_tgl_god.BindBool(ui_settings, "god_mode");
_panel_left.AddControl(_tgl_god);

var _txt_name = new EchoChamberTextInput("txt_name");
_txt_name.SetLabel("Player name");
_txt_name.SetPlaceholder("Type a name...");
_txt_name.BindText(ui_settings, "player_name");
_panel_left.AddControl(_txt_name);

var _dd_diff = new EchoChamberDropdownSelect("dd_diff");
_dd_diff.SetLabel("Difficulty");
_dd_diff.SetOptions(["Easy", "Normal", "Hard", "Nightmare"]);
_dd_diff.BindIndex(ui_settings, "difficulty_index");
_panel_left.AddControl(_dd_diff);
```

A small note on tooltips:

Echo Chamber's tooltip system is request based. Controls that support hovering will ask the root for a tooltip, and the root will handle the delay and drawing.

So you just set the tooltip text on the control and move on with your life.

> If you are using `FitToContent()` while adding lots of controls, wrap the adds in `BeginLayoutBatch()`/`EndLayoutBatch()` to avoid repeated size calculations. EndLayoutBatch will refit once if anything changed.
{: .note}

---

## Making the main panel do something useful

Ok, so we've got settings. Great.

But wait a minute. Debug UI isn't just knobs, it's visibility. You want to see what the game is doing.

Let's make a simple "stats" panel that reads from your own data.

For this example, we'll bind a few labels to live getters instead of pushing text in Step.

Add this in Create:

```js
var _lbl_main = new EchoChamberLabel("lbl_main");
_lbl_main.SetText("Live stats");
_panel_main.AddControl(_lbl_main);

_panel_main.AddControl(new EchoChamberSeparator("sep_main").SetOrientation("horizontal"));

_panel_main.AddControl(new EchoChamberLabel("lbl_fps").BindText(function() {
	return "FPS: " + string(fps_real);
}));

_panel_main.AddControl(new EchoChamberLabel("lbl_room").BindText(function() {
	return "Room: " + room_get_name(room);
}));

_panel_main.AddControl(new EchoChamberLabel("lbl_mouse").BindText(function() {
	return "Mouse: (" + string(mouse_x) + ", " + string(mouse_y) + ")";
}));

var _owner = self;
_panel_main.AddControl(new EchoChamberLabel("lbl_speed").BindText(method(_owner, function() {
	return "Speed setting: " + string(ui_settings.speed);
})));

_panel_main.AddControl(new EchoChamberLabel("lbl_god").BindText(method(_owner, function() {
	return "God mode: " + string(ui_settings.god_mode);
})));
```

Is this the fanciest inspector on the planet? Nah.

But it's honest. It's the exact pattern you'll use in a real tool:

- bind controls to your settings struct
- bind labels to live getters so you don't need a sync Step loop

---

## The "I don't want to rebuild my layout" section

Ah, here we go. Persistence.

Echo Chamber can save and load window layout, z-order, and panel state to an INI file. The only catch is important:

You must create/register your windows and panels first, then call `LoadLayout()`.

So, at the end of your Create event, do this:

```js
ui_root.LoadLayout();
```

And if you want a manual save key (highly recommended while you're tweaking your layout), add this to Step:

```js
if (keyboard_check_pressed(vk_f5)) {
	ui_root.SaveLayout();
	ui_root.ShowToast("Layout saved", 1200);
}

if (keyboard_check_pressed(vk_f9)) {
	ui_root.LoadLayout();
	ui_root.ShowToast("Layout loaded", 1200);
}
```

> Why F5 and F9?
> No reason. I'm just a creature of habit.
{: .note}

---

## Theme swapping (because why ugly when can pretty?)

Echo Chamber themes are just structs. They aren't magic. They are a big bag of settings.

That means theme swapping is extremely straightforward: `ApplyTheme()`.

Here's a cheeky little way to do it with a dropdown.

Add a field:

```js
ui_settings.theme_index = 0;
```

Add this control to the top bar (after the console button):

```js
var _owner = self;
var _dd_theme = new EchoChamberDropdownSelect("dd_theme");
_dd_theme.SetLabel("Theme");
_dd_theme.SetOptions([
	"MidnightNeon",
	"MangoMint",
	"SakuraPunch",
	"ToxicTerminal",
]);
_dd_theme.BindIndex(ui_settings, "theme_index");
_dd_theme.OnChange(method(_owner, function(_index, _value) {
	var _new_theme;
	switch (_index) {
		case 0: _new_theme = new EchoChamberThemeMidnightNeon(); break;
		case 1: _new_theme = new EchoChamberThemeMangoMint(); break;
		case 2: _new_theme = new EchoChamberThemeSakuraPunch(); break;
		case 3: _new_theme = new EchoChamberThemeToxicTerminal(); break;
		default: _new_theme = new EchoChamberThemeMidnightNeon(); break;
	}

	ui_root.ApplyTheme(_new_theme);
	ui_root.ShowToast("Theme applied", 1000);
}));
_panel_top.AddControl(_dd_theme);
```

---

## Input: the simple way, and the "proper" way

Ok, so how do you toggle your debugger on and off?

### The simple way

This is totally fine for most projects:

```js
// obj_debug_controller: Create
ui_visible = true;
```

```js
if (keyboard_check_pressed(vk_f1)) {
	ui_visible = !ui_visible;
	ui_win.SetVisible(ui_visible);
}
```

### The Echo Chamber way (input contexts)

Echo Chamber has input contexts with inheritance. This is a fancy way of saying:

- you can have defaults
- a window can override or block specific actions
- you can keep your bindings sane as tools grow

Bind a default action in Create:

```js
ui_root.BindCoreInputAction("toggle_debug", new EchoChamberInputBindingKey(vk_f1));
```

Then check it somewhere you run every frame (Step is fine):

```js
if (ui_root.InputPressed("toggle_debug")) {
	ui_visible = !ui_visible;
	ui_win.SetVisible(ui_visible);
}
```

Nice. You can keep adding tool actions without turning your Step event into a keybinding spaghetti festival. If you need per-window overrides, create a context with `CreateInputContext` and assign it with `SetInputContext`, then call `InputPressed` with the window to enforce focus.

---

## Batch layout updates (FitToContent without churn)

If you're adding or moving lots of controls, you can batch the layout work so `FitToContent()` only runs once at the end.

```js
ui_win.FitToContent(); // size to the current content
ui_win.BeginLayoutBatch();

_panel_main.ClearControls();
_panel_main.AddControl(new EchoChamberLabel("lbl_a").SetText("A"));
_panel_main.AddControl(new EchoChamberLabel("lbl_b").SetText("B"));
_panel_main.AddControl(new EchoChamberLabel("lbl_c").SetText("C"));

ui_win.EndLayoutBatch(); // fits once after the batch
```

This keeps large UI rebuilds snappy while still giving you the convenience of auto-sizing.

---

## Reordering and moving controls

You can insert, reorder, and move controls between panels without rebuilding the whole UI.

```js
// Insert at a specific index
_panel_top.InsertControl(new EchoChamberButton("btn_new").SetLabel("New"), 0);

// Reorder a direct child
_panel_top.MoveControl("btn_console", 2);

// Set explicit order (unlisted items keep their order at the end)
_panel_top.SetControlOrder(["btn_console", "dd_theme"]);

// Move a control between panels
_panel_left.MoveControlToPanel("sld_speed", _panel_main);
ui_win.MoveControlToPanel("tgl_god", "main", 1);
```

These work on direct controls unless otherwise noted (nested panels are handled where supported).

---

## Modal windows

If you want a single window to temporarily own all input, set it as modal:

```js
ui_root.SetModalWindow(ui_win); // all other windows ignore input
```

When you're done:

```js
ui_root.ClearModalWindow();
```

Modal windows always stay on top and block input to other windows.

---

## A quick word on overlays, dropdowns, and context menus

If you've ever built dropdown menus in GM by hand, you already know the vibe:

- "where do I draw it"
- "how do I close it"
- "why is it appearing behind other things"
- "why does it eat input even after I click away"

Echo Chamber handles all that with the root overlay system.

You don't need to call it directly to use dropdown controls, but it's there if you want to build your own popups or context menus.

> If you do want to build a custom overlay or context menu, check the scripting reference for `QueueOverlay()`, `OpenContextMenu()`, and the overlay owner helpers.
{: .note}

---

## Advanced recipe: a virtualized list view

Echo Chamber has a `ListView` control that only draws and hit-tests the visible rows.

That is a big deal when you're showing logs, entity lists, save slots, whatever. You can have 50,000 rows and it won't try to draw 50,000 rows.

This control uses callbacks, so bind them with `method` and carry any instance data you need through the scope struct.

Add a little fake log to your object:

```js
ui_log = [];
for (var _i = 0; _i < 2000; _i++) {
	ui_log[_i] = "Log line " + string(_i);
}
```

Add a list view to the main panel:

```js
var _owner = self;
var _list = new EchoChamberListView("list_log");
_list.SetRowHeight(18);
_list.SetCountGetter(method(_owner, function() {
	return array_length(ui_log);
}));

_list.SetRowDrawer(method(_owner, function(_row_index, _row_rect, _is_selected, _is_hover) {
	var _x = _row_rect.x1;
	var _y = _row_rect.y1;
	draw_text(_x + 6, _y + 2, ui_log[_row_index]);
}));

_list.SetOnSelect(method(_owner, function(_index) {
	ui_root.ShowToast("Selected row " + string(_index), 800);
}));

_panel_main.AddControl(_list);
```

Even if you don't use this directly, it's worth knowing it exists because it powers "real tool" UIs.

---

## The whole thing (one object, three events)

If you just want the complete demo lump so you can paste it, here's a compact version.

> This is demo code. Rename ids, split things up, and make it nice for your actual project.
{: .note}

```js
// obj_debug_controller: Create
ui_settings = {
	speed: 4,
	god_mode: false,
	player_name: "Drew",
	difficulty_index: 1,
	theme_index: 0,
};

var _theme = new EchoChamberThemeMidnightNeon();
ui_root = new EchoChamberRoot(_theme);
ui_root.SetPersistenceFile("echo_chamber_demo.ini");
ui_root.SetPersistenceSection("demo");

ui_win = ui_root.CreateWindow("demo_main");
ui_win.SetTitle("Echo Chamber Demo");
ui_win.SetRect(40, 40, 560, 540);

var _panel_top = new EchoChamberPanel("top_bar", eEchoChamberDock.TOP);
_panel_top.SetSizeMode(eEchoChamberPanelSizeMode.FIXED);
_panel_top.SetSize(32);
_panel_top.SetFlowMode(eEchoChamberPanelFlow.ROW);
_panel_top.SetGap(6);
ui_win.AddPanel(_panel_top);

var _panel_left = new EchoChamberPanel("left", eEchoChamberDock.LEFT);
_panel_left.SetSizeMode(eEchoChamberPanelSizeMode.FIXED);
_panel_left.SetSize(200);
_panel_left.SetFlowMode(eEchoChamberPanelFlow.COLUMN);
_panel_left.SetCollapseMode(eEchoChamberCollapse.TO_LEFT);
ui_win.AddPanel(_panel_left);

var _panel_main = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_panel_main.SetFlowMode(eEchoChamberPanelFlow.COLUMN);
ui_win.AddPanel(_panel_main);

var _owner = self;
var _btn_console = new EchoChamberButton("btn_console");
_btn_console.SetLabel("Console");
_btn_console.OnClick(method(_owner, function() {
	EchoChamberOpenConsole(ui_root);
	ui_root.ShowToast("Console opened", 1200);
}));
_panel_top.AddControl(_btn_console);

var _dd_theme = new EchoChamberDropdownSelect("dd_theme");
_dd_theme.SetLabel("Theme");
_dd_theme.SetOptions(["MidnightNeon", "MangoMint", "SakuraPunch", "ToxicTerminal"]);
_dd_theme.BindIndex(ui_settings, "theme_index");
_dd_theme.OnChange(method(_owner, function(_index, _value) {
	var _new_theme;
	switch (_index) {
		case 0: _new_theme = new EchoChamberThemeMidnightNeon(); break;
		case 1: _new_theme = new EchoChamberThemeMangoMint(); break;
		case 2: _new_theme = new EchoChamberThemeSakuraPunch(); break;
		case 3: _new_theme = new EchoChamberThemeToxicTerminal(); break;
		default: _new_theme = new EchoChamberThemeMidnightNeon(); break;
	}
	ui_root.ApplyTheme(_new_theme);
	ui_root.ShowToast("Theme applied", 1000);
}));
_panel_top.AddControl(_dd_theme);

_panel_left.AddControl(new EchoChamberLabel("lbl_left").SetText("Quick settings"));
_panel_left.AddControl(new EchoChamberSeparator("sep_left").SetOrientation("horizontal"));

var _sld_speed = new EchoChamberSlider("sld_speed");
_sld_speed.SetLabel("Speed");
_sld_speed.SetRange(0, 12);
_sld_speed.SetStep(1);
_sld_speed.BindValue(ui_settings, "speed");
_panel_left.AddControl(_sld_speed);

var _tgl_god = new EchoChamberToggle("tgl_god");
_tgl_god.SetLabel("God mode");
_tgl_god.BindBool(ui_settings, "god_mode");
_panel_left.AddControl(_tgl_god);

var _txt_name = new EchoChamberTextInput("txt_name");
_txt_name.SetLabel("Player name");
_txt_name.SetPlaceholder("Type a name...");
_txt_name.BindText(ui_settings, "player_name");
_panel_left.AddControl(_txt_name);

var _dd_diff = new EchoChamberDropdownSelect("dd_diff");
_dd_diff.SetLabel("Difficulty");
_dd_diff.SetOptions(["Easy", "Normal", "Hard", "Nightmare"]);
_dd_diff.BindIndex(ui_settings, "difficulty_index");
_panel_left.AddControl(_dd_diff);

_panel_main.AddControl(new EchoChamberLabel("lbl_main").SetText("Live stats"));
_panel_main.AddControl(new EchoChamberSeparator("sep_main").SetOrientation("horizontal"));

_panel_main.AddControl(new EchoChamberLabel("lbl_fps").BindText(function() {
	return "FPS: " + string(fps_real);
}));

_panel_main.AddControl(new EchoChamberLabel("lbl_room").BindText(function() {
	return "Room: " + room_get_name(room);
}));

_panel_main.AddControl(new EchoChamberLabel("lbl_mouse").BindText(function() {
	return "Mouse: (" + string(mouse_x) + ", " + string(mouse_y) + ")";
}));

_panel_main.AddControl(new EchoChamberLabel("lbl_speed").BindText(method(_owner, function() {
	return "Speed setting: " + string(ui_settings.speed);
})));

_panel_main.AddControl(new EchoChamberLabel("lbl_god").BindText(method(_owner, function() {
	return "God mode: " + string(ui_settings.god_mode);
})));

ui_root.LoadLayout();
ui_visible = true;

// Optional input binding toggle
ui_root.BindCoreInputAction("toggle_debug", new EchoChamberInputBindingKey(vk_f1));


// obj_debug_controller: Step
if (ui_root.InputPressed("toggle_debug")) {
	ui_visible = !ui_visible;
	ui_win.SetVisible(ui_visible);
}

if (keyboard_check_pressed(vk_f5)) {
	ui_root.SaveLayout();
	ui_root.ShowToast("Layout saved", 1200);
}

if (keyboard_check_pressed(vk_f9)) {
	ui_root.LoadLayout();
	ui_root.ShowToast("Layout loaded", 1200);
}


// obj_debug_controller: Draw GUI
ui_root.RunDesktop();
```

---

## Where to go next

At this point you've got:

- a root running a desktop every frame
- a window with docked panels
- a pile of controls bound to a struct
- persistence for your layout
- theme swapping

From here, the world is your oyster.

If you want to build something more custom (graphs, inspectors, weird visualizers), start looking at:

- `SetContentDrawer()` on panels
- `DrawScrollArea()` on the root
- the overlay helpers (dropdowns, popups, context menus)

And, very importantly, make sure you look over the API reference page to see all the possible options you have available to you.
