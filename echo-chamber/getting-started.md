---
layout: default
title: Getting Started
parent: Echo Chamber
nav_order: 1
redirect_from:
  - /echo/echo_chamber/usage.html
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Getting Started

This page builds a simple debug tool from the ground up. By the end, you should know what each piece is for, why the examples are structured this way, and which part to change when you build a tool for your own game.

The examples assume the normal bundled Echo Chamber setup. In that setup, Echo Chamber already has a shared debug desktop running once per frame, so our job will be mostly to create what windows and controls should exist on it.

---

## Put the debug UI somewhere that runs once

Build the *shape* of your debug UI once, such as in a debug controller's Create event. A window, its panels, and its controls are structs that stay around after the setup finishes. You don't recreate them every Step just because the values they show can change or anything like that.

Start by keeping a reference to Echo Chamber's shared desktop:

```js
/// obj_debug_controller Create
ui_root = GetEchoChamberRoot();
```

`GetEchoChamberRoot()` gives you that shared desktop. Echo Chamber calls it the **root** because the windows in this UI all belong underneath it.

The normal bundled controller is already running this root for you, so you can create windows on `ui_root` without also running your own `RunDesktop()` call. If you later choose to manage a separate root yourself, the [Echo Chamber](index) page explains that setup (though honestly, this is unnecessary for 99% of use cases).

---

## Building a window

Let's build out a small debug tool for tuning player movement. To begin with we'll just make a window with a button that proves the tool is alive. Build the window, give it one panel, then put one button in that panel:

```js
var _win = ui_root
	.CreateWindow("movement_debug")
	.SetTitle("Movement Debug")
	.SetRect(32, 32, 380, 240);

var _panel = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_win.AddPanel(_panel);

_panel.AddControl(new EchoChamberButton("ping")
	.SetCaption("Write test log")
	.SetTooltip("Send a test message through Echo.")
	.OnClick(function() {
		EchoDebugInfo("Movement debug window is alive", "UI");
	})
);
```

`ui_root.CreateWindow("movement_debug")` creates a new window on the shared desktop. `"movement_debug"` is the window's id: a stable name that code can use later with things such as `FindWindow()` and saved layout. It isn't the text shown to the user.

Two chained calls configure the window. `SetTitle("Movement Debug")` sets the visible title-bar text. `SetRect(32, 32, 380, 240)` sets the window's left, top, right, and bottom coordinates in Echo Chamber's canvas. `CreateWindow()` returns the new window, and the setters return that same window again, which is why the calls can be chained.

A window needs somewhere to lay out its controls, so the example creates a panel:

`new EchoChamberPanel("main", eEchoChamberDock.FILL)` makes a panel named `"main"`. `FILL` means the panel should use the window space left over after any edge-docked panels have taken theirs. There aren't any other panels yet, so this one fills the entire inside of the window.

`_win.AddPanel(_panel)` attaches the panel to the window. Constructing a panel doesn't place it anywhere by itself...Adding the panel to the window is what makes it part of this window's layout.

The last part creates the button. `new EchoChamberButton("ping")` gives it a stable id ("ping"), `SetCaption("Write test log")` sets the words drawn on it, `SetTooltip(...)` adds the hover help, and `OnClick(...)` supplies the function that writes the Echo info message when the button is clicked.

`_panel.AddControl(...)` puts that finished button into the panel. From then on, Echo Chamber handles drawing it and routes normal button interaction to the callback you supplied.

The local variables `_win` and `_panel` are only convenient handles while we are building the UI. The root keeps the window, the window keeps the panel, and the panel keeps the controls that were added to it. As I mentioned before, you can retrieve the handles again if necessary via `FindWindow()` and other methods like that.

> Windows are completely resizable, if you grab the left, right, bottom or bottom corners and drag them. Remember this because otherwise you'll likely end up with windows large enough to cover important gameplay elements, so resizing them is very useful.
{: .note}

---

## Let controls edit settings for you

A button is pretty simple because it only needs to run some code when clicked. Sliders, toggles, dropdowns, and text fields are slightly more complicated: they usually represent a value that already belongs to your game.

Imagine your debug controller already has this settings struct:

```js
debug_settings = {
	speed: 4,
	god_mode: false,
	player_name: "Drew"
};
```

You could copy `debug_settings.speed` into a slider every Step, then copy the slider back into `debug_settings.speed` whenever the player drags it. You could repeat that plumbing for the toggle and text field. But Echo Chamber can keep those controls connected to the real fields automatically instead.

The window and panel already exist, so find that panel and add three controls to it:

```js
var _panel = ui_root.FindWindow("movement_debug").FindPanel("main");

_panel.AddControl(new EchoChamberSlider("speed")
	.SetLabel("Speed")
	.SetRange(0, 12)
	.SetStep(1)
	.BindValue(debug_settings, "speed")
);

_panel.AddControl(new EchoChamberToggle("god_mode")
	.SetLabel("God mode")
	.BindValue(debug_settings, "god_mode")
);

_panel.AddControl(new EchoChamberTextInput("player_name")
	.SetLabel("Player name")
	.SetPlaceholder("Type a name...")
	.BindText(debug_settings, "player_name")
);
```

`FindWindow("movement_debug")` looks up the window by the id you gave it earlier, and `FindPanel("main")` finds the panel inside that window.

The first control is a slider:

- `SetLabel("Speed")` gives the slider a separate form label. This is text that is shown beside the control, so the user knows what it does. The panel can arrange that label beside or above the slider body.
- `SetRange(0, 12)` says the slider represents values from 0 through 12.
- `SetStep(1)` makes the slider move in steps of 1 instead of allowing every value between the minimum and maximum.
- `BindValue(debug_settings, "speed")` connects the slider's value to `debug_settings.speed`.

`BindValue(debug_settings, "speed")` is what keeps the two sides connected. Obviously, `debug_settings` is the struct we created, and then we supply the specific variable in that struct we want to target as a string: `"speed"`. Drag the slider and `debug_settings.speed` changes. Change `debug_settings.speed` somewhere else in the game and the slider reads the new value and automatically updates. In other words the struct remains the actual source of the setting.

The toggle does the same thing with `debug_settings.god_mode`, while the text input connects its text to `debug_settings.player_name`. `SetPlaceholder("Type a name...")` supplies the faint hint text shown when that text field is empty.

Echo Chamber calls this live connection between a control and game data a **binding**. The control shows and edits the value you already have instead of maintaining a second UI-only copy that your Step event has to keep synchronised.

Your game continues reading the field normally:

```js
var _current_speed = debug_settings.speed;
```

`SetCaption()` and `SetLabel()` are easy to confuse at first. A caption is text that belongs *inside* a control, such as the words on a button. A label is separate form text that the panel lays out next to a control, such as `Speed` beside a slider. `SetTooltip()` is different again: it's hover help that only appears when the user points at the control.

---

## Show values that keep changing

Not every debug value should be editable. Sometimes you simply want the UI to display some information from the game: FPS, a state name, the player's current room, an AI target, or whatever else.

For that job, a text block can ask a function for the current text whenever Echo Chamber needs it:

```js
var _panel = ui_root.FindWindow("movement_debug").FindPanel("main");

_panel.AddControl(new EchoChamberTextBlock("fps")
	.BindText(function() {
		return "FPS: " + string(fps_real);
	})
);
```

`EchoChamberTextBlock("fps")` creates a read-only piece of text. `BindText(function() { ... })` gives the text block a small getter function instead of binding it to a value in a struct. When Echo Chamber needs the text, that function returns the current value, so changes to `fps_real` appear without a Step event repeatedly calling `SetText()`.

The function should return the answer to a single question: "what text should this control show right now?" Keep it cheap and don't use it to rebuild UI or cause unrelated gameplay changes. Echo Chamber will ask for bound values at most once per frame (it caches it so sometimes it doesn't even need to ask).

If the getter needs to read instance variables from a particular instance, bind the function to that instance with `method()`:

```js
var _panel = ui_root.FindWindow("movement_debug").FindPanel("main");

_panel.AddControl(new EchoChamberTextBlock("speed_value")
	.BindText(method(self, function() {
		return "Speed setting: " + string(debug_settings.speed);
	}))
);
```

Here `method(self, ...)` keeps the stored getter attached to this debug controller. When Echo Chamber calls the getter later, `debug_settings.speed` is plainly accessible because the function is specifically bound to the instance you declared the struct in. You don't have to use `self`, any instance (or struct) reference will work.

This is the same underlying idea as the slider binding: Echo Chamber asks your game state for the value instead of requiring you to maintain a duplicate UI value. The difference is that this text block only needs a getter because the user isn't editing anything through it.

---

## Split a larger tool into panels

A single fill panel is enough for a small settings window but bigger tools often need recognisable areas instead: perhaps a toolbar across the top, settings down the left, and the main view in the remaining space.

For that layout, create a *separate* window rather than adding these panels to the earlier `movement_debug` window:

```js
var _layout_win = ui_root
	.CreateWindow("movement_layout_example")
	.SetTitle("Movement Layout Example")
	.SetRect(440, 32, 520, 320);

var _top = new EchoChamberPanel("toolbar", eEchoChamberDock.TOP)
	.SetSizeMode(eEchoChamberPanelSizeMode.FIXED)
	.SetSize(34)
	.SetFlowMode(eEchoChamberPanelFlow.ROW);
_top.Style().SetGap(6);
_layout_win.AddPanel(_top);

var _left = new EchoChamberPanel("settings", eEchoChamberDock.LEFT)
	.SetSizeMode(eEchoChamberPanelSizeMode.FIXED)
	.SetSize(220)
	.SetFlowMode(eEchoChamberPanelFlow.COLUMN)
	.SetCollapseMode(eEchoChamberCollapse.TO_LEFT);
_layout_win.AddPanel(_left);

var _main = new EchoChamberPanel("main", eEchoChamberDock.FILL)
	.SetFlowMode(eEchoChamberPanelFlow.COLUMN);
_layout_win.AddPanel(_main);
```

Several panel settings appear together here. Start with the toolbar:

`new EchoChamberPanel("toolbar", eEchoChamberDock.TOP)` creates a panel called `"toolbar"` and docks it to the top edge of the window. A `TOP` panel takes a horizontal strip from the available window area.

`SetSizeMode(eEchoChamberPanelSizeMode.FIXED)` says that strip should use an explicit thickness instead of sizing itself from its contents. For a top or bottom panel, that thickness is its height. `SetSize(34)` therefore makes the toolbar strip 34 canvas pixels tall (left or right panels will instead set their width to the thickness you provide). Canvas pixels are Echo Chamber's own UI coordinate units, and at the default theme scale they line up with pixels in the game window.

`SetFlowMode(eEchoChamberPanelFlow.ROW)` controls how direct controls inside the panel are arranged. `ROW` lays controls across rows and wraps them when needed, which suits a toolbar full of buttons. It doesn't change where the panel itself sits. Docking decides the panel's place in the window, while flow decides how the controls *inside* that panel are laid out.

`_top.Style()` changes only this panel's style, and `SetGap(6)` gives its horizontal and vertical control spacing a value of 6. The [Themes](themes) page explains local styles in more detail. Here, the visible effect is simply a little breathing room between toolbar controls.

`_layout_win.AddPanel(_top)` attaches the toolbar to the window. The panel now belongs to this window and participates in its layout.

The `settings` panel repeats the same pattern on a different edge. `eEchoChamberDock.LEFT` makes it take a vertical strip from the left side of the space that remains after the toolbar. With `FIXED` sizing, `SetSize(220)` means this left-docked panel is 220 canvas pixels wide.

Its flow is `COLUMN`, so direct controls stack vertically from top to bottom instead of packing across rows. That generally suits a settings form.

`SetCollapseMode(eEchoChamberCollapse.TO_LEFT)` gives this panel a collapse direction. When the panel is collapsed, it collapses toward the left edge (the handle remains so you can uncollapse it again). The setting won't start the panel collapsed, it simply defines how collapsing is allowed to work.

The `main` panel uses `eEchoChamberDock.FILL`. It doesn't take a new strip from an edge, but receives the space left after the edge-docked panels have claimed theirs. Echo Chamber processes dock directions in the order `TOP`, `BOTTOM`, `LEFT`, `RIGHT`, then `FILL`. The order you call `AddPanel()` only decides the order of panels that share the same dock direction.

For this particular window, that means the toolbar claims the top strip, the settings panel claims the left strip from what remains, and the main panel fills everything still unused. You can picture docking as progressively carving edge strips away from the window, then handing the remainder to `FILL`.

The `main` panel also uses `COLUMN`, so any controls added directly to the large centre area will stack vertically unless you change that flow or use child panels for a more specialised layout.

## Child panels

Child panels allow you to nest panels within each other.

```js
_main_panel.AddChildPanel(_child_panel);
```

You can add multiple child panels to a single panel, and you should imagine them being laid out the same as a window. So if you wanted a panel that had a "toolbar" at the top of it, and content below, you would add two child panels, with the first child panel being docked  as `TOP`, and the second being docked as `FILL`.

Each panel can host *either* child panels or controls, but not both. Trying to add controls to a panel that has been given a child panel will result in the controls being rejected, and vice versa for adding a child panel to a panel with existing controls. Use an extra child panel without any child panels attached to it to host the controls (in the "toolbar" example, we would have the main panel, which is the host for the child panels, and then the toolbar child panel would host the controls, with the content `FILL` panel either hosting more child panels for multiple sections, or hosting controls to display the content).

### Adjusting form labels layout

The settings panel will probably contain sliders, toggles, dropdowns, and other controls with labels. You can give the panel one label policy instead of configuring every control separately:

```js
var _left = ui_root.FindWindow("movement_layout_example").FindPanel("settings");

_left
	.SetLabelPlacement(eEchoChamberLabelPlacement.AUTO)
	.SetLabelGap(8)
	.SetLabelWidthClamp(90, 220);
```

`SetLabelPlacement(eEchoChamberLabelPlacement.AUTO)` tells this column panel to choose between putting a control's label beside it and putting the label above it. When there's enough room, the label can use a leading column. When that would leave too little space for the control itself, the label moves above instead.

`SetLabelGap(8)` leaves 8 canvas pixels between the label and the control body.

`SetLabelWidthClamp(90, 220)` constrains the automatically chosen width of the leading label column. Echo Chamber can size that column from the labels it sees, but these values won't let the result shrink below 90 or grow beyond 220.

These settings become the defaults for labelled controls in this panel. An individual control can still override its own label behaviour when it has a special reason to look different.

---

## Follow a target that can change

`BindValue(debug_settings, "speed")` works because `debug_settings` is the same struct for the life of the tool. An inspector often has a harder problem: the *owner* of the value can change.

Imagine your game keeps the currently inspected instance's debug data in a struct. Let's pretend you're making a game about bee's. When the player clicks one bee, the slider should show the `energy` variable stored in a struct on the bee called `stats`. Each time a new bee is selected, it should update so that it shows *that particular bees* data. You don't want to destroy and rebuild the control every time the selected data changes.

For that situation, give Echo Chamber a small function that answers "Give me the `stats` from the selected bee instance":

```js
// Create Event of your debug controller
selected_bee = noone;

var _panel = ui_root.FindWindow("movement_debug").FindPanel("main");
var _energy_binding = new EchoChamberFieldBinding(method(self, function() {
	if (instance_exists(selected_bee)) {
		return selected_bee.stats;
	}

	return undefined;
}), "energy", 0);

_panel.AddControl(new EchoChamberSlider("selected_energy")
	.SetLabel("Energy")
	.SetRange(0, 100)
	.BindValue(_energy_binding)
);
```

In your bee object, you would have a struct called `stats` with an `energy` variable initialised in it:

```js
// Create Event of your bee object
stats = {
	energy: 100,
}
```

Then, in the Step Event of your debug controller (where you declare `selected_bee = noone;`), you would have some code that lets you select a bee:
```js
// Step Event of your debug controller

if (mouse_check_button_pressed(mb_left)) {
	selected_bee = instance_position(mouse_x, mouse_y, obj_bee);
}
```

`selected_bee` is the changing game-side selection. The `EchoChamberFieldBinding` stores a function that finds the `stats` struct from the selected bee, and grabs the field name `"energy"` from that struct, and also provides a fallback value of `0` if the function returns `undefined` instead (for instance, if you haven't clicked a bee).

Whenever the binding needs the field, it first runs the target function. If `selected_bee` is a valid instance, the function returns the correct struct from it and the binding reads or writes its `energy` field. If there isn't a usable selected instance, the function returns `undefined`, so the binding has no target and reads the fallback value instead.

The slider itself doesn't need to know which bee is selected. `BindValue(_energy_binding)` tells it to use that reusable field binding, and the binding handles the moving target.

`EchoChamberFieldBinding` binds the field on whichever owner its getter says is current at the time.

The same field binding can be used by controls that call `BindText`, `BindCaption`, `BindValue`, `BindIndex`, `BindColor`, or `BindOptions`, depending on what the field represents.

If a dynamic field should only be inspected, `SetReadOnly()` prevents writes through the field binding. `SetOnWrite()` lets you attach extra code that runs after the UI successfully writes a new value. Those are useful when a debug edit needs a side effect beyond assigning the field itself.

---

## Keep window positions between runs

Once you have several debug windows, dragging them back into place every time the game starts gets old. Echo Chamber can save the current arrangement to an INI file and restore it on the next run.

The saved layout includes window position and size, visibility, minimised and pinned state, window order, and panel collapse or fixed-size state.

First tell the root which INI file and which section of that file this debug layout should use:

```js
ui_root
	.SetPersistenceFile("echo_chamber_layout.ini")
	.SetPersistenceSection("debug_tools");
```

`SetPersistenceFile("echo_chamber_layout.ini")` chooses the file. `SetPersistenceSection("debug_tools")` chooses the section prefix used for this layout inside that file. The word **persistence** here just means "remember this arrangement between runs".

Create the windows and panels *before* loading the layout. Echo Chamber restores saved values onto pieces that already exist, using the ids you gave those windows and panels to match them up:

```js
ui_root.LoadLayout();
```

`LoadLayout()` returns after applying any saved layout data it can match to the current UI.

When you have arranged the windows the way they want, save the current state:

```js
ui_root.SaveLayout();
```

For a simple debug controller, its Clean Up event is one reasonable place to save when that controller goes away:

```js
/// obj_debug_controller Clean Up
ui_root.SaveLayout();
```

If you have two different debug setups that should remember independent arrangements, give them different persistence sections so one doesn't overwrite the other's saved values.

---

## Open the built-in Console from your own tool

Your custom windows and Echo Console can live on the same root, so a button in your own toolbar can open the built-in debugger beside the tools you've made yourself:

```js
var _top = ui_root.FindWindow("movement_layout_example").FindPanel("toolbar");

_top.AddControl(new EchoChamberButton("open_console")
	.SetCaption("Console")
	.OnClick(method(self, function() {
		EchoChamberOpenConsole(ui_root);
	}))
);
```

The first line finds the `"toolbar"` panel created in the split-layout example. The button is then added to that panel just like the earlier Ping button.

Its `OnClick()` callback calls `EchoChamberOpenConsole(ui_root)`, passing the same root that owns the custom window. The Console therefore opens on the same debug desktop rather than creating some unrelated UI surface.

With the default bundled setup you can also press F1, so this button is mostly useful when you want the Console discoverable inside your own debug toolbar.

The [Echo Console](console) guide explains the log search, instance inspector, watches, commands, snapshots, crash reports, input recordings, and the other built-in tools.

---

## Where the other controls fit

You don't need to memorise every control constructor before making useful tools. The controls on this page cover the common settings-window jobs: run an action, edit a number, edit a boolean, edit one line of text, and show a changing value.

Here are some other controls Echo Chamber supports when the game-facing problem calls for them:

- A dropdown when the user should choose one option from a set.
- A colour button when the tool edits a GameMaker colour.
- A text box when one line of text isn't enough.
- A list view when you may have hundreds or thousands of rows and only want to process the visible part efficiently.
- A separator when a visual divider makes groups of controls easier to scan.

[Advanced Usage](advanced) teaches those less common situations in context, including scrolling, large lists, custom drawing, popups, modal windows, input contexts, and rebuilding live tools. The [Scripting Reference](api-reference) is the exact API lookup once you already know what kind of thing you're trying to do.
