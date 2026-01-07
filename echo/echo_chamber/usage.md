---
layout: default
title: Echo Chamber Usage & Examples
nav_order: 3
parent: Echo Chamber
has_children: false
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

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

## A small setup

Let's build up a little window that allows you to do some simple things:

Create a controller object (I usually call it something like `obj_debug_controller`) and drop it into your room.

### Create event

```js
// We'll bind controls to this struct, because binding is lovely and callbacks are optional.
ui_settings = {
	speed: 4,
	god_mode: false,
	player_name: "Drew",
	difficulty_index: 1,
};

ui_root = global.__echo_chamber_root;
// Note: if you have ECHO_DEBUG_ENABLED set to false in the scr_echo script file, you will need to create a root like this:
// ui_root = new EchoChamberRoot(_theme);
// And then manually draw it in the Draw GUI Event like this:
// ui_root.RunDesktop();

// First we create a window from the root
ui_win = ui_root.CreateWindow("demo_main")
	.SetTitle("Echo Chamber Demo")
	.SetAutoFit(true);
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
var _panel_top = new EchoChamberPanel("top_bar", eEchoChamberDock.TOP)
	.SetSizeMode(eEchoChamberPanelSizeMode.FIXED)
	.SetSize(32)
	.SetFlowMode(eEchoChamberPanelFlow.ROW)
	.SetGap(6);
// Each panel needs to be added to the window we created
ui_win.AddPanel(_panel_top);

var _panel_left = new EchoChamberPanel("left", eEchoChamberDock.LEFT)
	.SetSizeMode(eEchoChamberPanelSizeMode.FIXED)
	.SetSize(200)
	.SetFlowMode(eEchoChamberPanelFlow.COLUMN)
	.SetCollapseMode(eEchoChamberCollapse.TO_LEFT);
ui_win.AddPanel(_panel_left);

var _panel_main = new EchoChamberPanel("main", eEchoChamberDock.FILL)
	.SetFlowMode(eEchoChamberPanelFlow.COLUMN);
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
// We create a button, give it some text (the label) and then provide it with a function it will
// run when it is clicked
var _btn_console = new EchoChamberButton("btn_console")
	.SetLabel("Console")
	.OnClick(method(self, function() {
		EchoChamberOpenConsole(ui_root);
		// ShowToast is a nice little feature on the root, that creates a little popup in the bottom right corner briefly
		ui_root.ShowToast("Console opened", 1200);
	}));

// And like with adding the panels to the window, we need to add the button to a panel
_panel_top.AddControl(_btn_console);
```

### Some bound settings

This is where the real action happens.

Binding means the control writes straight into a struct field for you. No custom Step code, no "did I forget to sync the slider" nonsense.

```js
// A label is just a little bit of text
var _lbl_left = new EchoChamberLabel("lbl_left")
	.SetText("Quick settings")
	.UseSmallFont(false);
_panel_left.AddControl(_lbl_left);

// We'll add a separater after the label
var _sep = new EchoChamberSeparator("sep_left")
	.SetOrientation("horizontal");
_panel_left.AddControl(_sep);

// Now we get to something meaty, we want to create a slider, give it a range and how much each "tick" of
// slider movement is (an change of 1) in this case, and finally, we want to "bind" it to the struct we setup
// at the very start of this example. ui_settings is the name of the struct, and "speed" is the name of the
// variable inside the struct that we want the slider to change. The ui_settings.speed is now bound to this
// slider, and changing the value of the slider automatically changes the value of ui_settings.speed, so in-game
// we can just read ui_settings.speed when we move the player, and the players movement speed will change
// when we change the sliders value.
var _sld_speed = new EchoChamberSlider("sld_speed")
	.SetLabel("Speed")
	.SetRange(0, 12)
	.SetStep(1)
	.BindValue(ui_settings, "speed")
	.SetTooltip("Tweak movement speed without recompiling your brain");
_panel_left.AddControl(_sld_speed);

// Same goes for the rest of these settings, we bind them to one of the variables stored in ui_settings, and
// they become linked.
var _tgl_god = new EchoChamberToggle("tgl_god")
	.SetLabel("God mode")
	.BindBool(ui_settings, "god_mode");
_panel_left.AddControl(_tgl_god);

var _txt_name = new EchoChamberTextInput("txt_name")
	.SetLabel("Player name")
	.SetPlaceholder("Type a name...")
	.BindText(ui_settings, "player_name");
_panel_left.AddControl(_txt_name);

var _dd_diff = new EchoChamberDropdownSelect("dd_diff")
	.SetLabel("Difficulty")
	.SetOptions(["Easy", "Normal", "Hard", "Nightmare"])
	.BindIndex(ui_settings, "difficulty_index");
_panel_left.AddControl(_dd_diff);
```

A small note on tooltips:

Echo Chamber's tooltip system is request based. Controls that support hovering will ask the root for a tooltip, and the root will handle the delay and drawing. So you just set the tooltip text on the control and move on with your life.

> If you are using `SetAutoFit(true)` while adding lots of controls, wrap the adds in `BeginLayoutBatch()`/`EndLayoutBatch()` to avoid repeated size calculations. EndLayoutBatch will refit once if anything changed.
{: .note}

---

## Making the main panel do something useful

Ok, so we've got settings. Great.

But wait a minute. Debug UI isn't just knobs, it's visibility. You want to see what the game is doing.

Let's make a simple "stats" panel that reads from your own data.

For this example, we'll bind a few labels to live getters instead of pushing text in Step (which might be what you naively want to do).

Add this in Create:

```js
// Again, just a label and a separator to begin with
var _lbl_main = new EchoChamberLabel("lbl_main")
	.SetText("Live stats");
_panel_main.AddControl(_lbl_main);

var _sep = new EchoChamberSeparator("sep_main")
	.SetOrientation("horizontal");
_panel_main.AddControl();

// Now we create a label, but this time, we "bind" its text to a function. Whatever that function
// returns is what the label will show. We return an fps string here.
var _lbl_fps = new EchoChamberLabel("lbl_fps")
	.BindText(function() {
		return "FPS: " + string(fps_real);
	});
_panel_main.AddControl(_lbl_fps);

// Here we return the name of the current room
var _lbl_rm = new EchoChamberLabel("lbl_room")
	.BindText(function() {
		return "Room: " + room_get_name(room);
	})
_panel_main.AddControl(_lbl_rm);

// Mouse position
var _lbl_mouse = new EchoChamberLabel("lbl_mouse")
	.BindText(function() {
		return "Mouse: (" + string(mouse_x) + ", " + string(mouse_y) + ")";
	});
_panel_main.AddControl(_lbl_mouse);

// And in this label, we read the speed vairable from the ui_settings struct we have.
var _lbl_spd = new EchoChamberLabel("lbl_speed")
	.BindText(method(self, function() {
		return "Speed setting: " + string(ui_settings.speed);
	}));
_panel_main.AddControl(_lbl_spd);

// And here we read god mode
var _lbl_god = new EchoChamberLabel("lbl_god")
	.BindText(method(self, function() {
		return "God mode: " + string(ui_settings.god_mode);
	}));
_panel_main.AddControl(_lbl_god);
```

Is this the fanciest inspector on the planet? Nah.

But it's useful and it's the exact pattern you'll use in a real tool:

- bind controls to your settings struct
- bind labels to live getters so you don't need a sync Step loop

---

## The "I don't want to rebuild my layout" section

Ah, here we go. Persistence.

Echo Chamber can save and load window layout, z-order, and panel state to an INI file. The only catch is important:

You must create/register all your windows and panels first, and only THEN call `LoadLayout()`.

So, at the start of the Create event, after you have set the `ui_root` variable, add this:

```js
ui_root.SetPersistenceFile("echo_chamber_demo.ini");
ui_root.SetPersistenceSection("demo");
```

And then at the very end of your Create event, after you've added all the windows, panels, buttons, labels, etc, add this:

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

Echo Chamber themes aren't magic. They are just structs. Essentially big bags of settings.

That means theme swapping is extremely straightforward: `ApplyTheme()`.

Here's a cheeky little way to do it with a dropdown.

Add this to our Create Event:

```js
// We need a variable to track what theme we are currently using
ui_settings.theme_index = 0;

// And we want a dropdown list that we can use to change the theme
var _dd_theme = new EchoChamberDropdownSelect("dd_theme")
	.SetLabel("Theme")
	// We give it an array of options to display
	.SetOptions([
		"Midnight Neon",
		"Amber Forest",
		"Mango Mint",
		"Sakura Punch",
		"Toxic Terminal",
		"Arcade Wave",
		"Circuit Candy",
		"Sunset Glitch",
		"Bubblegum Terminal",
		"Echo Chamber"
	])
	// Again, bind the dropdown to our ui_settings struct
	.BindIndex(ui_settings, "theme_index")
	// And when one of the options from the dropdown is selected, we want to apply the new theme to the root
	.OnChange(method(self, function(_index, _value) {
		// The function is always provided with _index and _value, so we'll always want to
		// base our functions around one of those.

		// If we look at the options array we gave before, we know that index 0 reads "MidnightNeon",
		// index 1 reads "MangoMint", and so on, so we just take the _index argument of the function
		// (which Echo Chamber automatically sets to the selected index from the dropdown)
		// and pick the appropriate theme for the index.
		var _new_theme;
		switch (_index) {
			case 0: _new_theme = new EchoChamberThemeMidnightNeon(); break;
			case 1: _new_theme = new EchoChamberThemeAmberForest(); break;
			case 2: _new_theme = new EchoChamberThemeMangoMint(); break;
			case 3: _new_theme = new EchoChamberThemeSakuraPunch(); break;
			case 4: _new_theme = new EchoChamberThemeToxicTerminal(); break;
			case 5: _new_theme = new EchoChamberThemeArcadeWave(); break;
			case 6: _new_theme = new EchoChamberThemeCircuitCandy(); break;
			case 7: _new_theme = new EchoChamberThemeSunsetGlitch(); break;
			case 8: _new_theme = new EchoChamberThemeBubblegumTerminal(); break;
			default: _new_theme = new EchoChamberTheme(); break;
		}

		// Then we apply the theme, and do a toast. We can even use _value here to display the value
		// of the options array that was picked (the theme name as a string, in this case)
		ui_root.ApplyTheme(_new_theme);
		ui_root.ShowToast($"{_value} theme applied", 1000);
	}))
_panel_top.AddControl(_dd_theme);
```

---

## Input: the simple way, and the "proper" way

Ok, so how do you toggle your debugger on and off?

### The simple way

This is totally fine for most projects:

### Create Event

```js
ui_visible = true;
```

### Step Event

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
// We create a new input binding, so we can toggle the debug window with F2
// The actual toggle happens in the step event
ui_root.BindCoreInputAction("toggle_debug", new EchoChamberInputBindingKey(vk_f1));
```

Then check it in the Step Event:

```js
if (ui_root.InputPressed("toggle_debug")) {
	ui_visible = !ui_visible;
	ui_win.SetVisible(ui_visible);
}
```

Nice. You can keep adding tool actions without turning your Step event into a keybinding spaghetti festival. If you need per-window overrides, create a context with `CreateInputContext` and assign it with `SetInputContext`, then call `InputPressed` with the window, instead of the root, to enforce focus.

---

## Batch layout updates (SetAutoFit without churn)

If you're adding or moving lots of controls, you can batch the layout work so that the autofitting that occurs for each addition when `SetAutoFit()` is true for a window gets deferred and only runs once at the end of the batch.

```js
// This is just reinforcing that we have SetAutoFit set to true
ui_win.SetAutoFit(true);

ui_win.BeginLayoutBatch();
// I'm just condensing the creation of the labels here, so we don't have to define a new local variable each time, mainly
// for speed of typing, lol
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

If you want a single window to temporarily own all input, set it as modal (this would live in some "action" like a keypress or whatever):

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

If you've ever built dropdown menus in GM by hand, you already know the pains:

- "how do I keep it on top of everything else?"
- "how do I close it properly"
- "why do clicks bleed through to stuff underneath"

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
// We want a lot of log lines to show in this list, so we'll generate some dummy data
ui_log = [];
for (var _i = 0; _i < 2000; _i++) {
	ui_log[_i] = "Log line " + string(_i);
}
```

Add a list view to the main panel:

```js
// Create a list view control, give it a default row height and a function that lets us count how many rows there are
var _list = new EchoChamberListView("list_log")
	.SetRowHeight(25)
	.SetVisibleRows(12)
	.SetFillWidth(true)
	.SetCountGetter(method(self, function() {
		return array_length(ui_log);
	}));

// We need to draw the rows manually (this is so that the list can virtualise rows that are offscreen)
_list.SetRowDrawer(method(self, function(_row_index, _row_rect, _is_selected, _is_hover) {
	var _x = _row_rect.x1;
	var _y = _row_rect.y1;
	draw_text(_x + 6, _y + 2, ui_log[_row_index]);
}));

// And we can also provide a function that is called when a row is selected
_list.SetOnSelect(method(self, function(_index) {
	ui_root.ShowToast("Selected row " + string(_index), 800);
}));

_panel_main.AddControl(_list);
```

Even if you don't use this directly, it's worth knowing it exists because it powers "real tool" UIs.

---

## The whole thing (one object, two events)

If you just want the complete demo lump so you can paste it, here's a compact version.

> This is demo code. Rename ids, split things up, and make it nice for your actual project.
{: .note}

### Create Event

```js
// We'll bind controls to this struct, because binding is lovely and callbacks are optional.
ui_settings = {
	speed: 4,
	god_mode: false,
	player_name: "Drew",
	difficulty_index: 1,
};

ui_root = global.__echo_chamber_root;
// Note: if you have ECHO_DEBUG_ENABLED set to false in the scr_echo script file, you will need to create a root like this:
// ui_root = new EchoChamberRoot(_theme);

// Setup persistence (saving/loading layout)
ui_root.SetPersistenceFile("echo_chamber_demo.ini");
ui_root.SetPersistenceSection("demo");

// First we create a window from the root
ui_win = ui_root.CreateWindow("demo_main")
	.SetTitle("Echo Chamber Demo")
	.SetAutoFit(true);

// Panels
var _panel_top = new EchoChamberPanel("top_bar", eEchoChamberDock.TOP)
	.SetSizeMode(eEchoChamberPanelSizeMode.FIXED)
	.SetSize(32)
	.SetFlowMode(eEchoChamberPanelFlow.ROW)
	.SetGap(6);
// Each panel needs to be added to the window we created
ui_win.AddPanel(_panel_top);

var _panel_left = new EchoChamberPanel("left", eEchoChamberDock.LEFT)
	.SetSizeMode(eEchoChamberPanelSizeMode.FIXED)
	.SetSize(200)
	.SetFlowMode(eEchoChamberPanelFlow.COLUMN)
	.SetCollapseMode(eEchoChamberCollapse.TO_LEFT);
ui_win.AddPanel(_panel_left);

var _panel_main = new EchoChamberPanel("main", eEchoChamberDock.FILL)
	.SetFlowMode(eEchoChamberPanelFlow.COLUMN);
ui_win.AddPanel(_panel_main);

// We create a button, give it some text (the label) and then provide it with a function it will
// run when it is clicked
var _btn_console = new EchoChamberButton("btn_console")
	.SetLabel("Console")
	.OnClick(method(self, function() {
		EchoChamberOpenConsole(ui_root);
		// ShowToast is a nice little feature on the root, that creates a little popup in the bottom right corner briefly
		ui_root.ShowToast("Console opened", 1200);
	}));

// And like with adding the panels to the window, we need to add the button to a panel
_panel_top.AddControl(_btn_console);

// A label is just a little bit of text
var _lbl_left = new EchoChamberLabel("lbl_left")
	.SetText("Quick settings")
	.UseSmallFont(false);
_panel_left.AddControl(_lbl_left);

// We'll add a separater after the label
var _sep = new EchoChamberSeparator("sep_left")
	.SetOrientation("horizontal");
_panel_left.AddControl(_sep);

// Now we get to something meaty, we want to create a slider, give it a range and how much each "tick" of
// slider movement is (an change of 1) in this case, and finally, we want to "bind" it to the struct we setup
// at the very start of this example. ui_settings is the name of the struct, and "speed" is the name of the
// variable inside the struct that we want the slider to change. The ui_settings.speed is now bound to this
// slider, and changing the value of the slider automatically changes the value of ui_settings.speed, so in-game
// we can just read ui_settings.speed when we move the player, and the players movement speed will change
// when we change the sliders value.
var _sld_speed = new EchoChamberSlider("sld_speed")
	.SetLabel("Speed")
	.SetRange(0, 12)
	.SetStep(1)
	.BindValue(ui_settings, "speed")
	.SetTooltip("Tweak movement speed without recompiling your brain");
_panel_left.AddControl(_sld_speed);

// Same goes for the rest of these settings, we bind them to one of the variables stored in ui_settings, and
// they become linked.
var _tgl_god = new EchoChamberToggle("tgl_god")
	.SetLabel("God mode")
	.BindBool(ui_settings, "god_mode");
_panel_left.AddControl(_tgl_god);

var _txt_name = new EchoChamberTextInput("txt_name")
	.SetLabel("Player name")
	.SetPlaceholder("Type a name...")
	.BindText(ui_settings, "player_name");
_panel_left.AddControl(_txt_name);

var _dd_diff = new EchoChamberDropdownSelect("dd_diff")
	.SetLabel("Difficulty")
	.SetOptions(["Easy", "Normal", "Hard", "Nightmare"])
	.BindIndex(ui_settings, "difficulty_index");
_panel_left.AddControl(_dd_diff);

// Again, just a label and a separator to begin with
var _lbl_main = new EchoChamberLabel("lbl_main")
	.SetText("Live stats");
_panel_main.AddControl(_lbl_main);

var _sep = new EchoChamberSeparator("sep_main")
	.SetOrientation("horizontal");
_panel_main.AddControl();

// Now we create a label, but this time, we "bind" its text to a function. Whatever that function
// returns is what the label will show. We return an fps string here.
var _lbl_fps = new EchoChamberLabel("lbl_fps")
	.BindText(function() {
		return "FPS: " + string(fps_real);
	});
_panel_main.AddControl(_lbl_fps);

// Here we return the name of the current room
var _lbl_rm = new EchoChamberLabel("lbl_room")
	.BindText(function() {
		return "Room: " + room_get_name(room);
	})
_panel_main.AddControl(_lbl_rm);

// Mouse position
var _lbl_mouse = new EchoChamberLabel("lbl_mouse")
	.BindText(function() {
		return "Mouse: (" + string(mouse_x) + ", " + string(mouse_y) + ")";
	});
_panel_main.AddControl(_lbl_mouse);

// And in this label, we read the speed vairable from the ui_settings struct we have.
var _lbl_spd = new EchoChamberLabel("lbl_speed")
	.BindText(method(self, function() {
		return "Speed setting: " + string(ui_settings.speed);
	}));
_panel_main.AddControl(_lbl_spd);

// And here we read god mode
var _lbl_god = new EchoChamberLabel("lbl_god")
	.BindText(method(self, function() {
		return "God mode: " + string(ui_settings.god_mode);
	}));
_panel_main.AddControl(_lbl_god);

// We need a variable to track what theme we are currently using
ui_settings.theme_index = 0;

// And we want a dropdown list that we can use to change the theme
var _dd_theme = new EchoChamberDropdownSelect("dd_theme")
	.SetLabel("Theme")
	// We give it an array of options to display
	.SetOptions([
		"Midnight Neon",
		"Amber Forest",
		"Mango Mint",
		"Sakura Punch",
		"Toxic Terminal",
		"Arcade Wave",
		"Circuit Candy",
		"Sunset Glitch",
		"Bubblegum Terminal",
		"Echo Chamber"
	])
	// Again, bind the dropdown to our ui_settings struct
	.BindIndex(ui_settings, "theme_index")
	// And when one of the options from the dropdown is selected, we want to apply the new theme to the root
	.OnChange(method(self, function(_index, _value) {
		// The function is always provided with _index and _value, so we'll always want to
		// base our functions around one of those.

		// If we look at the options array we gave before, we know that index 0 reads "MidnightNeon",
		// index 1 reads "MangoMint", and so on, so we just take the _index argument of the function
		// (which Echo Chamber automatically sets to the selected index from the dropdown)
		// and pick the appropriate theme for the index.
		var _new_theme;
		switch (_index) {
			case 0: _new_theme = new EchoChamberThemeMidnightNeon(); break;
			case 1: _new_theme = new EchoChamberThemeAmberForest(); break;
			case 2: _new_theme = new EchoChamberThemeMangoMint(); break;
			case 3: _new_theme = new EchoChamberThemeSakuraPunch(); break;
			case 4: _new_theme = new EchoChamberThemeToxicTerminal(); break;
			case 5: _new_theme = new EchoChamberThemeArcadeWave(); break;
			case 6: _new_theme = new EchoChamberThemeCircuitCandy(); break;
			case 7: _new_theme = new EchoChamberThemeSunsetGlitch(); break;
			case 8: _new_theme = new EchoChamberThemeBubblegumTerminal(); break;
			default: _new_theme = new EchoChamberTheme(); break;
		}

		// Then we apply the theme, and do a toast. We can even use _value here to display the value
		// of the options array that was picked (the theme name as a string, in this case)
		ui_root.ApplyTheme(_new_theme);
		ui_root.ShowToast($"{_value} theme applied", 1000);
	}))
_panel_top.AddControl(_dd_theme);

ui_visible = true;

// We create a new input binding, so we can toggle the debug window with F2
// The actual toggle happens in the step event
ui_root.BindCoreInputAction("toggle_debug", new EchoChamberInputBindingKey(vk_f2));

// A batch add, which skips autofitting until the batch is ended
ui_win.BeginLayoutBatch();
// I'm just condensing the creation of the labels here, so we don't have to define a new local variable each time, mainly
// for speed of typing, lol
_panel_main.AddControl(new EchoChamberLabel("lbl_a").SetText("A"));
_panel_main.AddControl(new EchoChamberLabel("lbl_b").SetText("B"));
_panel_main.AddControl(new EchoChamberLabel("lbl_c").SetText("C"));

ui_win.EndLayoutBatch(); // fits once after the batch

// Insert at a specific index
_panel_top.InsertControl(new EchoChamberButton("btn_new").SetLabel("New"), 0);

// Reorder a direct child
_panel_top.MoveControl("btn_console", 2);

// Set explicit order (unlisted items keep their order at the end)
_panel_top.SetControlOrder(["btn_console", "dd_theme"]);

// Move a control between panels
_panel_left.MoveControlToPanel("sld_speed", _panel_main);
ui_win.MoveControlToPanel("tgl_god", "main", 1);

// We want a lot of log lines to show in this list, so we'll generate some dummy data
ui_log = [];
for (var _i = 0; _i < 2000; _i++) {
	ui_log[_i] = "Log line " + string(_i);
}

// Create a list view control, give it a default row height and a function that lets us count how many rows there are
var _list = new EchoChamberListView("list_log")
	.SetRowHeight(25)
	.SetVisibleRows(12)
	.SetFillWidth(true)
	.SetCountGetter(method(self, function() {
		return array_length(ui_log);
	}));

// We need to draw the rows manually (this is so that the list can virtualise rows that are offscreen)
_list.SetRowDrawer(method(self, function(_row_index, _row_rect, _is_selected, _is_hover) {
	var _x = _row_rect.x1;
	var _y = _row_rect.y1;
	draw_text(_x + 6, _y + 2, ui_log[_row_index]);
}));

// And we can also provide a function that is called when a row is selected
_list.SetOnSelect(method(self, function(_index) {
	ui_root.ShowToast("Selected row " + string(_index), 800);
}));

_panel_main.AddControl(_list);

ui_root.LoadLayout();
```

### Step Event
```js
if (keyboard_check_pressed(vk_f5)) {
	ui_root.SaveLayout();
	ui_root.ShowToast("Layout saved", 1200);
}

if (keyboard_check_pressed(vk_f9)) {
	ui_root.LoadLayout();
	ui_root.ShowToast("Layout loaded", 1200);
}

if (ui_root.InputPressed("toggle_debug")) {
	ui_visible = !ui_visible;
	ui_win.SetVisible(ui_visible);
}
```

---

## Where to go next

At this point you've got:

- a root "desktop"
- a window with docked panels
- a pile of controls bound to a settings struct
- persistence for your layout
- theme swapping

From here, the world is your oyster.

If you want to build something more custom (graphs, inspectors, weird visualizers), start looking at:

- `SetContentDrawer()` on panels
- `DrawScrollArea()` on the root
- the overlay helpers (dropdowns, popups, context menus)

And, very importantly, make sure you look over the API reference page to see all the possible options you have available to you.
