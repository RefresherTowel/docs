---
layout: default
title: Advanced Usage
parent: Echo Chamber
nav_order: 4
redirect_from:
  - /echo/echo_chamber/advanced.html
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Advanced Usage

The basic settings-window workflow gives you the things you need to build debug tools for the most common debug needs. This page is for the problems that show up once a debug tool starts requiring some more advanced machinery.

Nothing here is required for ordinary Echo Chamber use. Each section starts with the practical problem it solves, so you can quickly scan down and jump to the one that matches the tool you're building.

---

## Scrollable panels

If a panel contains more controls than fit in its visible area, the usual answer is to let the user scroll through them instead of making the whole window enormous.

Create a window, keep its vertical scroll position in a small state object, then make the panel scrollable:

```js
var _win = GetEchoChamberRoot()
	.CreateWindow("scroll_example")
	.SetTitle("Scrollable Settings")
	.SetRect(32, 32, 360, 260);

var _panel = new EchoChamberPanel("settings", eEchoChamberDock.FILL)
	.SetScrollable(true)

_win.AddPanel(_panel);
```

The first four lines are the same window setup used throughout the Getting Started guide. The panel itself is still an ordinary fill panel. `SetScrollable(true)` tells Echo Chamber that overflowing content should be viewed through a vertical scroll area.

`_win.AddPanel(_panel)` then attaches the configured panel to the window as usual.

Echo Chamber automatically creates a scroll state for you when you turn on scrollable, however, you *can* create an independent scroll state for yourself (via `new EchoChamberSCrollState()` and applying it to the panel with the `.SetScrollState()` method) if you need access to the scroll state for a particular reason. If you only want the panel to scroll and never need the scroll state elsewhere, just set scrollable to true as in the example. Create one yourself when the state is useful to the rest of your tool, such as when you want to inspect or reset the scroll position yourself.

Scrollable panels automatically skip most work for controls that are outside the visible area, so you don’t need to manually hide or recreate off-screen controls. You should still make dynamic getters reasonably cheap though because Echo Chamber may read them during layout or drawing even if they are offscreen.

---

## List views

A panel full of controls is useful when each row really *is* a separate control. It's a poor fit for something like 2,000 log lines, a list of enemy instances, inventory entries, path nodes, test results, or anything else that might be a big list of things.

For a large list like that, keep the actual data in your game and let one `EchoChamberListView` ask two questions as it draws: "how many rows exist?" and "what should this visible row look like?" That way you don't construct thousands of separate Echo Chamber controls just to represent thousands of entries.

The list below shows 2,000 strings through one list view:

```js
/// obj_debug_controller Create
ui_root = GetEchoChamberRoot();

debug_lines = [];
for (var i = 0; i < 2000; i++) {
	debug_lines[i] = "Line " + string(i);
}

var _win = ui_root
	.CreateWindow("debug_lines_example")
	.SetTitle("Debug Lines")
	.SetRect(32, 32, 420, 320);

var _panel = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_win.AddPanel(_panel);

var _list = new EchoChamberListView("debug_lines")
	.SetVisibleRows(12)
	.SetCountGetter(method(self, function() {
		return array_length(debug_lines);
	}))
	.SetRowDrawer(method(self, function(_index, _rect, _is_selected, _is_hover) {
		draw_text(_rect.x1 + 6, _rect.y1 + 2, debug_lines[_index]);
	}))
	.SetOnActivate(method(self, function(_index) {
		ui_root.ShowToast("Activated row " + string(_index), 900);
	}));

_list.Style().SetRowHeight(20);
_panel.AddControl(_list);
```

`debug_lines` is an instance variable because the list needs to access it after the Create event has finished running. `ui_root` is persistent for the same reason: the activation callback uses it later to show a toast. `_win`, `_panel`, and `_list` are only local handles used while the UI is being assembled.

After the ordinary window and panel setup, `new EchoChamberListView("debug_lines")` creates the list control.

`SetVisibleRows(12)` gives the list a preferred visible height based on 12 rows. It doesn't mean the list only contains 12 entries. The count getter below still reports all 2,000.

`SetCountGetter(...)` supplies a function that returns the current number of rows. Echo Chamber can ask it again later, so if `debug_lines` grows or shrinks, the list can follow that new count without being reconstructed.

`SetRowDrawer(...)` supplies the code that draws one row. Echo Chamber passes four useful pieces of information into that function:

- `_index` tells you which item in your underlying data this row represents.
- `_rect` gives you the rectangle where that row should be drawn.
- `_is_selected` tells you whether this is the selected row.
- `_is_hover` tells you whether the pointer is currently over it.

Echo Chamber draws the list's normal row background and selection treatment before your row drawer runs. The custom row drawer only needs to draw `debug_lines[_index]` inside the supplied rectangle (Echo Chamber isn't opinionated about how you want your data drawn, so it leaves that up to you).

`SetOnActivate(...)` handles the moment the user activates the selected row with Echo Chamber's Accept action. Enter is the default Accept key. The callback receives the activated row index and uses it here to show a short toast naming that row. Clicking a row selects it, and you can make a callback run for that interaction with `SetOnSelect()`, while double-click behaviour can be handled separately with `SetOnDoubleClick()`.

`_list.Style().SetRowHeight(20)` changes the height used for rows in this particular list. Then `_panel.AddControl(_list)` places the finished list into the panel like any other control.

Unlike a giant panel full of separate controls, the list owns one reusable row-drawing process and asks it only for visible rows. Your actual array remains the data source.

If you later enable `SetAutoWidthFromContent(_max_rows)` (`_max_rows` being 0 disables it, any positive integer samples up to that many rows for the auto-width), Echo Chamber also needs a way to estimate how wide row contents are, so pair it with `SetRowMeasure()` (look these up in the API reference page for more info). Right-click callbacks (set via `SetOnRightClick()` and your callback should take the arguments `_index`, `_x` and `_y`) can receive `_index = -1` when the click is in empty list space rather than on a real row.

---

## Custom content drawing

Some debug views aren't naturally made from buttons and form controls at all. A graph, map, hitbox display, state diagram, timeline, or profiler chart needs drawing code that understands your game's data and visual meaning.

For that kind of tool, a panel can give you the rectangle it owns and let your own function draw inside it:

```js
/// obj_debug_controller Create
debug_settings = {
	speed: 4
};

var _win = GetEchoChamberRoot()
	.CreateWindow("custom_draw_example")
	.SetTitle("Custom Drawing")
	.SetRect(32, 32, 420, 220);

var _panel = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_win.AddPanel(_panel);

_panel.SetContentDrawer(method(self, function(_root, _rect) {
	var _pad = 8;
	var _x = _rect.x1 + _pad;
	var _y = _rect.y1 + _pad;
	var _w = (_rect.x2 - _rect.x1) - _pad * 2;

	draw_text(_x, _y, "Player speed: " + string(debug_settings.speed));
	draw_line(_x, _y + 28, _x + _w, _y + 28);
}));
```

The window and fill panel are ordinary, while `SetContentDrawer(...)` is what turns the panel into a custom-drawn view.

Instead of adding another control, this stores a draw callback on the panel. Echo Chamber calls it while drawing that panel and passes two arguments: the active `_root`, and `_rect`, the rectangle available for the panel's content.

`_rect` contains edge coordinates: `x1`, `y1`, `x2`, and `y2`. It isn't `{ x, y, width, height }`. That's why the example calculates the usable width with `_rect.x2 - _rect.x1` before drawing the horizontal line.

The callback then uses normal GameMaker drawing functions. Echo Chamber has already decided where the panel is, and it clips this custom content to the panel's content rectangle, so your drawing code won't spill outside of the provided space.

A panel can mix normal controls and custom drawing. Its ordinary controls are drawn first and the content drawer runs afterward. If the panel is purely a graph or map, simply don't add controls to it.

The `_root` argument is there when the custom view needs services owned by the same Echo Chamber desktop, such as a scroll area, popup, clipboard action, or toast. If the view itself has state that must last between frames, such as a selected graph node or zoom value, store that state somewhere persistent rather than as a local created inside the draw callback every frame.

---

## Root scroll areas

A custom drawing callback can have the same space problem as a panel full of controls. Imagine drawing a 900-pixel-tall report inside a panel that's only 200 pixels tall. You need to clip it to the panel, remember a scroll position, move the drawing by that amount, and draw a scrollbar.

`DrawScrollArea()` packages that behaviour for custom-drawn content:

```js
/// obj_debug_controller Create
custom_scroll = new EchoChamberScrollState("custom_log_scroll");

var _win = GetEchoChamberRoot()
	.CreateWindow("custom_scroll_example")
	.SetTitle("Custom Scroll Area")
	.SetRect(32, 32, 520, 300);

var _panel = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_win.AddPanel(_panel);

_panel.SetContentDrawer(method(self, function(_root, _rect) {
	_root.DrawScrollArea(
		custom_scroll,
		_rect,
		900,
		function(_draw_root, _draw_rect, _scroll_y) {
			var _draw_y = _draw_rect.y1 - _scroll_y;
			draw_text(_draw_rect.x1 + 8, _draw_y + 8, "Very tall custom content");
		}
	);
}));
```

`custom_scroll` is an `EchoChamberScrollState`, just like the one that Echo Chamber automatically creates when you set `SetScrollable(true)` at the very start of this page. It lives on the controller with an instance variable (not a local one) because the same scroll position has to survive between frames.

The panel's `SetContentDrawer()` gives you `_rect`, the visible rectangle available for the custom view. Inside that callback, `_root.DrawScrollArea(...)` receives:

1. `custom_scroll`, which remembers the vertical position.
2. `_rect`, which is the visible area to clip and interact with.
3. `900`, the full height of the custom content, including the part currently off screen.
4. a drawing function for the contents.

Echo Chamber handles the clipping, mouse wheel, scrollbar, and scroll position. The inner function receives `_scroll_y`, the current amount scrolled from the top. The example subtracts that from the content's starting Y position, so increasing the scroll amount moves the tall content upward through the fixed viewport.

The inner callback also receives `_draw_root` and `_draw_rect`. `_draw_rect` is the rectangle Echo Chamber tells your content to use for its drawing coordinates.

The full call also accepts an optional fifth rectangle. Supplying that changes the rectangle given to the draw callback, but it doesn't change the clipping rectangle or scrollbar geometry. Most custom views don't need that distinction, so leave the fifth argument out until you have a concrete reason to draw in a different coordinate rectangle.

---

## Dynamic dropdown options

A normal dropdown can be given a fixed array of options. Sometimes the available choices are themselves live game state: a list of connected players, loaded rooms, current quests, debug targets, or modes assembled elsewhere.

In that case, don't rebuild the dropdown every time the array changes. Give it a function that returns the options it should use now:

```js
/// obj_debug_controller Create
debug_settings = {
	mode_index: 0
};
mode_labels = ["Safe", "Fast"];

var _win = GetEchoChamberRoot()
	.CreateWindow("dynamic_dropdown_example")
	.SetTitle("Dynamic Dropdown")
	.SetRect(32, 32, 360, 180);

var _panel = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_win.AddPanel(_panel);

_panel.AddControl(new EchoChamberDropdownSelect("mode")
	.BindOptions(method(self, function() {
		return mode_labels;
	}))
	.BindIndex(debug_settings, "mode_index")
);
```

`mode_labels` is kept as an instance variable because the dropdown's getter will read it later. `debug_settings.mode_index` stores which option is currently selected.

`BindOptions(...)` gives the dropdown a function that returns the current options array. Echo Chamber asks that function when it needs the option count or labels, so changing `mode_labels` later changes what the existing dropdown sees.

`BindIndex(debug_settings, "mode_index")` connects the dropdown's selected index to the settings struct. Choosing a different option updates `mode_index`, and a change to `mode_index` from elsewhere is reflected when the control reads its bound value again.

Those two bindings solve different halves of the dropdown: `BindOptions()` answers "what choices exist?", while `BindIndex()` answers "which choice is selected?"

Keep the options getter cheap because Echo Chamber can ask it during UI work. Also avoid replacing the options underneath an open dropdown unless the tool genuinely needs live changes while the menu is open. A stable set of choices makes interaction easier to reason about.

---

## Customise the open part of a dropdown

When a dropdown is closed, it occupies one ordinary row in its panel. When it opens, the list of options needs to float over neighbouring controls rather than forcing the panel layout to make room for it.

Echo Chamber draws that floating list later, above the normal window contents. It calls later-drawn floating UI like this an **overlay**. The open menu sits visually on top of the normal layout.

Most dropdowns already draw and handle their overlays for you. Only customise this when the default rows can't show the information your tool needs.

The code below keeps all of the normal dropdown behaviour but replaces how each open option row is drawn:

```js
/// obj_debug_controller Create
debug_settings = {
	mode_index: 0
};
mode_labels = ["Safe", "Fast", "Testing"];

var _win = GetEchoChamberRoot()
	.CreateWindow("custom_dropdown_rows")
	.SetTitle("Custom Dropdown Rows")
	.SetRect(32, 32, 360, 180);

var _panel = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_win.AddPanel(_panel);

var _dropdown = new EchoChamberDropdownSelect("mode")
	.SetOptions(mode_labels)
	.BindIndex(debug_settings, "mode_index");

_dropdown.DrawOverlayRow = method(self, function(_root, _row_index, _rect, _hover, _selected) {
	var _old_colour = draw_get_color();
	draw_set_color(_selected ? c_yellow : c_white);
	draw_text(_rect.x1 + 8, _rect.y1 + 2, mode_labels[_row_index]);
	draw_set_color(_old_colour);
});

_panel.AddControl(_dropdown);
```

The setup should be starting to look familiar by now: a settings field stores the selected index, `mode_labels` stores the option text, and the dropdown uses `SetOptions(mode_labels)` plus `BindIndex(...)` to establish its choices and selection.

The unusual part is assigning a new function to `_dropdown.DrawOverlayRow`.

Echo Chamber calls that function once for each option row it needs to draw in the open dropdown. `_row_index` tells you which option is being drawn. `_rect` is the row rectangle. `_hover` tells you whether the pointer is over the row, and `_selected` tells you whether that row is the current selected value.

The example saves GameMaker's current draw colour, chooses yellow for the selected row and white for the others, draws the option text, then restores the previous draw colour so this custom drawing doesn't leak its colour into whatever Echo Chamber draws next.

Only the row visuals have been replaced. The dropdown still owns mouse selection, keyboard activation, updating its selected index, and closing the open list. There isn't a second public click callback you have to reimplement just because the rows look different.

The rectangle used here is in Echo Chamber's own screen/canvas coordinates, not room coordinates. At the default UI scale, one canvas unit corresponds to one game-window pixel. Keep the custom row drawing light because it runs every frame while those rows are visible.

---

## Colour controls

If a setting is a GameMaker colour, `EchoChamberColorButton` gives you a control that shows the current colour and opens a colour picker when edited.

Connect the control directly to `debug_settings.tint`:

```js
/// obj_debug_controller Create
debug_settings = {
	tint: c_white
};

var _win = GetEchoChamberRoot()
	.CreateWindow("colour_example")
	.SetTitle("Colour Setting")
	.SetRect(32, 32, 340, 180);

var _panel = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_win.AddPanel(_panel);

_panel.AddControl(new EchoChamberColorButton("tint")
	.SetLabel("Tint")
	.BindColor(debug_settings, "tint")
	.SetPopupTitle("Pick tint")
	.OnCommit(function(_colour) {
		EchoDebugInfo("Tint committed", "UI", _colour);
	})
);
```

`SetLabel("Tint")` gives the colour control its form label. `BindColor(debug_settings, "tint")` connects it to the existing colour field, so the control reads that field and writes the accepted colour back to it.

`SetPopupTitle("Pick tint")` sets the title used by the colour-picking popup.

`OnCommit(...)` supplies code to run when the edit is accepted. The callback receives the final `_colour` and logs a message using that colour here. A commit means the user has finished and accepted the edit.

For tools that need live preview while the user is still moving through the picker, `OnChange()` runs as the value changes. `OnCancel()` handles an edit that's abandoned instead of accepted. Choose the callback based on what your game needs to happen at each stage rather than treating every colour change as the same event.

---

## Text boxes

`EchoChamberTextInput` is for one line of text. When the value itself is naturally multi-line, use `EchoChamberTextBox` instead: notes, JSON, scripts, long debug descriptions, or any other text that needs room to grow vertically.

```js
/// obj_debug_controller Create
debug_settings = {
	notes: ""
};

var _win = GetEchoChamberRoot()
	.CreateWindow("notes_example")
	.SetTitle("Debug Notes")
	.SetRect(32, 32, 420, 300);

var _panel = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_win.AddPanel(_panel);

_panel.AddControl(new EchoChamberTextBox("notes")
	.SetLabel("Notes")
	.BindText(debug_settings, "notes")
	.SetVisibleRows(6)
	.SetWrap(true)
	.SetResizable(true, 80, 260)
);
```

`debug_settings.notes` is the real text value, and `BindText(debug_settings, "notes")` keeps the text box connected to it just like the single-line text binding from Getting Started.

`SetLabel("Notes")` gives the field its panel-managed label.

`SetVisibleRows(6)` chooses a useful starting height based on six visible lines of text. It doesn't limit the stored text to six lines. Longer content can be scrolled.

`SetWrap(true)` enables wrapping, so long lines can continue onto additional displayed lines instead of requiring all text to stay on one horizontal line.

`SetResizable(true, 80, 260)` enables the text box's resize grip and sets its minimum height to 80 canvas pixels and maximum height to 260. The user can therefore give the editor more or less vertical room without letting it shrink or grow beyond those heights.

Text boxes also support `SetUseOverlayEditor(true)`, which lets the user open the value in a larger temporary editor when the normal control is too cramped. They also share the text-input features for validation, transforms, and edit callbacks. Use those when the text represents structured data rather than just some arbitrary notes or something.

---

## Context menus

Sometimes an action belongs to the thing the user clicked rather than to a permanent button in the window. A context menu solves that by opening a temporary list of actions at the pointer position.

The menu isn't part of the panel's normal layout. It floats over the UI while open, so the root needs three things: a description of the menu rows, the Echo Chamber screen position where it should appear, and the window that owns it.

Here the context menu opens from a button so all of the setup can live in one Create event:

```js
/// obj_debug_controller Create
ui_root = GetEchoChamberRoot();

var _win = ui_root
	.CreateWindow("context_menu_example")
	.SetTitle("Context Menu")
	.SetRect(32, 32, 340, 180);

var _panel = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_win.AddPanel(_panel);

_panel.AddControl(new EchoChamberButton("open_menu")
	.SetCaption("Open menu")
	.OnClick(method(self, function() {
		var _owner = ui_root.FindWindow("context_menu_example");

		ui_root.OpenContextMenu([
			{
				label: "Inspect",
				on_click: method(self, function() {
					EchoConsoleOpenWindow(ui_root, ECHO_DEBUG_WINDOW_INSPECTOR);
				})
			},
			{ is_separator: true },
			{
				label: "Copy label",
				on_click: method(self, function() {
					ui_root.CopyToClipboard("Example label");
				})
			}
		], ui_root.mx, ui_root.my, _owner);
	}))
);
```

The first half is ordinary window, panel, and button setup. The menu is created inside the button's `OnClick()` callback because that's when there is actually a current pointer position to open beside (and we want the menu to appear next to the mouse).

`ui_root.FindWindow("context_menu_example")` gets the window that owns the button. The result is stored in `_owner` so it can be passed to `OpenContextMenu()`.

The first argument to `OpenContextMenu()` is an array of row description structs. Here:

- the `Inspect` row has a `label` and an `on_click` function that opens Echo Chamber's built-in Inspector window.
- `{ is_separator: true }` inserts a visual divider rather than a clickable command.
- the `Copy label` row has its own callback.

You can add a `shortcut` field to the structs describing a potential shortcut you might want for an action, but it's only a text display in the context menu itself. You would then have to manually bind the shortcut to Echo Chamber (we'll see how to bind inputs pretty soon).

After you've finished setting up the array of options for the context menu, the next two arguments are `ui_root.mx` and `ui_root.my`. Those are the pointer coordinates captured by Echo Chamber in the same screen/canvas coordinate system its windows use. Room-space `mouse_x` and `mouse_y` can point somewhere different when cameras or the game window transform room coordinates, so don't rely on `mouse_x` or even `device_mouse_x_to_gui(0)`, instead always use the `ui_root.mx` and `ui_root.my` for mouse interactions.

Passing `_owner` associates the floating menu with the window that opened it. Echo Chamber can then apply the correct popup ownership and interaction behaviour, and it keeps the final menu rectangle inside the game window for you.

A normal context-menu row can use these fields:

`label` - text shown for the row.
`on_click` - function run when the row is activated.
`enabled` - whether the row can currently be activated.
`shortcut` - optional shortcut text shown beside the label. This is display text only and does not create an input binding.
`icon_sprite` - optional sprite drawn for the row.
`icon_image_index` - subimage used from icon_sprite.
`icon_hover_sprite` - optional sprite used while the row is hovered.
`icon_hover_image_index` - subimage used from icon_hover_sprite.

A separator row uses `{ is_separator: true }`.

---

## Modal windows

A normal Echo Chamber window can sit beside the others and let the user move between them freely. Some workflows shouldn't allow that. A delete confirmation, for example, should make the user finish or cancel the confirmation before interacting with the debug window underneath it.

The first step is to create the confirmation window like any other window, then leave it hidden until it's needed:

```js
/// obj_debug_controller Create
ui_root = GetEchoChamberRoot();

var _confirm_window = ui_root
	.CreateWindow("delete_confirmation")
	.SetTitle("Confirm Delete")
	.SetRect(140, 100, 320, 160);

var _confirm_panel = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_confirm_window.AddPanel(_confirm_panel);

_confirm_panel.AddControl(new EchoChamberButton("cancel")
	.SetCaption("Cancel")
	.OnClick(method(self, function() {
		ui_root.ClearModalWindow();
		ui_root.FindWindow("delete_confirmation").SetVisible(false);
	}))
);

_confirm_window.SetVisible(false);
```

The window and fill panel are ordinary. The Cancel button's callback performs *two* separate jobs: `ClearModalWindow()` removes the input restriction, and `SetVisible(false)` hides the confirmation window again.

Those are separate operations because "this window is the one that currently owns modal interaction" and "this window is visible" aren't the same state. Clearing the modal restriction doesn't automatically decide what your workflow should do with the window afterward.

`_confirm_window.SetVisible(false)` at the end keeps the confirmation window out of the way when the game first starts.

When some later action actually needs confirmation, show the existing window and then make it the modal window:

```js
var _confirm_window = ui_root.FindWindow("delete_confirmation");
_confirm_window.SetVisible(true);
ui_root.SetModalWindow(_confirm_window);
```

`FindWindow()` retrieves the window by its stable id. `SetVisible(true)` makes it appear. `SetModalWindow(_confirm_window)` tells the root that this is now the window the user must interact with before ordinary pointer or keyboard focus can move back to other windows.

While modal, the confirmation stays above the other windows and normal input is restricted accordingly. When the workflow ends, clear the modal state and then hide, close, or otherwise update the window in whatever way makes sense for that workflow.

---

## Input contexts

A tiny debug panel can check F2 directly and move on. A larger tool eventually gets harder to manage that way. The same physical key may mean Refresh in one window, Rotate in another, and nothing at all while a popup owns keyboard focus.

Echo Chamber lets your code ask for a *named action* instead of hard-coding the key at the place where the action is used. You first say which input should trigger an action name, then later ask whether that action happened.

The following setup says that the action called `"toggle_debug"` should use F2:

```js
/// obj_debug_controller Create
ui_root = GetEchoChamberRoot();

debug_window = ui_root
	.CreateWindow("input_example")
	.SetTitle("Input Example")
	.SetRect(32, 32, 340, 180);

ui_root.BindCoreInputAction("toggle_debug", new EchoChamberInputBindingKey(vk_f2));
```

`BindCoreInputAction("toggle_debug", new EchoChamberInputBindingKey(vk_f2))` connects the action name your tool cares about (`"toggle_debug"`) to the actual key that triggers it (`EchoChamberInputBindingKey(vk_f2)`).

The Step event can then ask for the action rather than asking for F2 directly:

```js
/// obj_debug_controller Step
if (ui_root.EC_InputPressed("toggle_debug")) {
	debug_window.SetVisible(!debug_window.visible);
}
```

`EC_InputPressed("toggle_debug")` is true on the press of whatever input is currently bound to that action. The code then flips the stored window's `visible` value through `SetVisible()`.

`debug_window` is kept as an instance variable because the Step event needs the same window reference after Create has finished.

For one global set of shortcuts, core actions may be enough. If one window needs its own meanings, give that window a named set of action bindings:

```js
/// obj_debug_controller Create
ui_root.CreateInputContext("inventory_debug");
debug_window.SetInputContext("inventory_debug");

ui_root.GetInputContext("inventory_debug")
	.BindKey("refresh", ord("R"));
```

`CreateInputContext("inventory_debug")` creates the named set, `debug_window.SetInputContext("inventory_debug")` makes the window use it, and `GetInputContext("inventory_debug").BindKey("refresh", ord("R"))` defines R as this context's `"refresh"` action.

That named set is an **input context**. Input contexts can inherit from a parent context, which lets a specialised window override a few shortcuts while keeping the shared bindings for everything else.

Sometimes inheritance is exactly what you *don't* want. `BindBlock()` marks an action as deliberately unavailable in the child context instead of letting the parent supply it.

Use contexts when naming and grouping shortcuts makes the behaviour easier to reason about than scattering `keyboard_check_*()` calls through several windows. For one isolated key check, ordinary GameMaker input can still be the simpler choice.

---

## Reordering and moving controls

Debug tools often start with one specific layout and then change while the game is running: a new option appears, a section changes mode, or a control belongs in a different panel after the user chooses something.

You don't have to destroy those controls and recreate replacements. Echo Chamber can move the existing structs and keep the bindings and state already attached to them.

The code deliberately performs several movement operations one after another so you can see the differences:

```js
/// obj_debug_controller Create
var _win = GetEchoChamberRoot()
	.CreateWindow("moving_controls_example")
	.SetTitle("Moving Controls")
	.SetRect(32, 32, 520, 260);

var _main = new EchoChamberPanel("main", eEchoChamberDock.LEFT)
	.SetSizeMode(eEchoChamberPanelSizeMode.FIXED)
	.SetSize(250);
var _other_panel = new EchoChamberPanel("other", eEchoChamberDock.FILL);

_win.AddPanel(_main);
_win.AddPanel(_other_panel);

_main.AddControl(new EchoChamberSlider("speed").SetLabel("Speed"));
_main.AddControl(new EchoChamberToggle("god_mode").SetLabel("God mode"));

_main.InsertControl(new EchoChamberButton("new").SetCaption("New"), 0);
_main.MoveControl("new", 2);
_main.SetControlOrder(["new", "speed", "god_mode"]);

_main.MoveControlToPanel("speed", _other_panel);
_win.MoveControlToPanel("god_mode", "other", 1);
```

The window has two panels. `main` is a fixed 250-pixel left strip and `other` fills the remaining area. The slider and toggle are first added to `main` in the normal way.

`InsertControl(new EchoChamberButton("new")..., 0)` creates the button and inserts it at direct-child index 0 instead of appending it to the end. At that moment it becomes the first direct control in `main`.

`MoveControl("new", 2)` then moves that *existing* button to index 2 within the same panel. No replacement button is made. Only its position in the panel changes.

`SetControlOrder(["new", "speed", "god_mode"])` gives an ordered list of ids that should come first in the panel. If the panel had other direct controls whose ids weren't listed, those unlisted controls would keep their existing relative order after the listed ones.

The final two calls move controls across panels. `_main.MoveControlToPanel("speed", _other_panel)` starts the search from `_main` and moves the existing `speed` slider into the supplied panel struct. `_win.MoveControlToPanel("god_mode", "other", 1)` performs the move through the window and identifies the destination panel by its id, inserting the toggle at index 1 there.

Because the control structs themselves move, their bindings and current control state move with them. Use these functions when the UI's arrangement changes, and rebuild a control only when you actually need one with different behaviour.

---

## Group several layout changes together

An auto-fitting window can resize itself to match its contents. That's convenient when a single control changes. It can be wasteful when you're about to add or remove a whole batch of controls, because each intermediate change can ask for a fit even though the very next line changes the layout again.

A layout batch tells the window not to finish that repeated fitting work until the group of changes is complete:

```js
/// obj_debug_controller Create
var _win = GetEchoChamberRoot()
	.CreateWindow("layout_batch_example")
	.SetTitle("Layout Batch")
	.SetRect(32, 32, 320, 180);

var _panel = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_win.AddPanel(_panel);

_win.BeginLayoutBatch();
_win.SetAutoFit(true);
_panel.AddControl(new EchoChamberTextBlock("a").SetText("A"));
_panel.AddControl(new EchoChamberTextBlock("b").SetText("B"));
_panel.AddControl(new EchoChamberTextBlock("c").SetText("C"));
_win.EndLayoutBatch();
```

The initial window and panel setup are ordinary.

`BeginLayoutBatch()` marks the start of a group of layout changes. `SetAutoFit(true)` turns on automatic fitting for the window, and the next three calls add text blocks that all change the content the window may need to fit around.

If fitting is requested while the batch is open, Echo Chamber defers that fitting work rather than repeatedly settling on an intermediate size. `EndLayoutBatch()` closes the group and lets the deferred fit happen once against the final contents.

Layout batches are mainly useful when a live tool rebuilds a sizeable chunk of itself at once. For the normal one-time setup in a Create event, you generally don't need to wrap every group of `AddControl()` calls in one.

---

## Styling specialised tools

Once one of these tools works, [Themes](themes) explains styling through the decisions you actually make: changing the whole debug desktop, giving several controls a reusable special look, changing one particular control, or giving one specialist window a theme of its own.
