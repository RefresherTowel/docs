---
layout: default
title: Echo Chamber
nav_order: 9
has_children: true
library_id: echo-chamber
redirect_from:
  - /echo/echo_chamber/
  - /echo/echo_chamber/index.html
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Echo Chamber

Echo Chamber gives you in-game debug UI for GameMaker. Instead of awkwardly hand-writing mouse collision checks, dragging code, text input, scrolling, window movement, and all the other crappy little jobs around a debug tool, you can quickly build out the things you want: the windows, the controls inside them, and the game code those controls should read or run.

You can use the Echo Console, a comprehensive debugger that already ships with Echo Chamber, or build tools for your own game: a movement tuning window, enemy inspector, cheat panel, state viewer, live graph, profiler, or whatever else would make development easier.

---

## The four pieces of Echo Chamber

Before looking at the code, picture a small desktop drawn over your running game.

That desktop can contain movable debug windows, a window can be divided into layout areas, and those areas contain buttons, sliders, text fields, lists, and the other things you can interact with.

Echo Chamber gives those four levels these names throughout this documentation:

- The **root** is the debug desktop itself. It keeps the windows together and runs the shared UI behaviour they need.
- A **window** is one movable, resizable debug window on that desktop.
- A **panel** is an area inside a window. Panels decide where their controls go.
- A **control** is one visible or interactive item inside a panel, such as a button, slider, toggle, text input, dropdown, list, or text block.

Most Echo Chamber creation code is simply: get the root, create a window, put a panel in the window, then put controls in the panel.

With the standard bundled setup, the shared root already exists when you ask for it and Echo Chamber runs it for you. You don't need to build the scaffolding out before making your first tool.

---

## Make a small debug window

Put this in something that runs once, such as a debug controller's Create event:

```js
var _win = GetEchoChamberRoot()
	.CreateWindow("debug_tools")
	.SetTitle("Debug Tools")
	.SetRect(32, 32, 320, 180);

var _panel = new EchoChamberPanel("main", eEchoChamberDock.FILL);
_win.AddPanel(_panel);

_panel.AddControl(new EchoChamberButton("ping")
	.SetCaption("Ping")
	.OnClick(function() {
		EchoDebugInfo("Ping clicked", "UI");
	})
);
```

Echo Chambers window/panel/control setup is persistent, so make sure you're not setting it up somewhere which will repeat over (like a Step Event or a Draw Event).

The finished result is a movable window titled **Debug Tools** with one **Ping** button. Clicking that button sends an Echo info message tagged `"UI"`. You can click and drag the left/right/bottom/bottom corners of the window to resize it.

`GetEchoChamberRoot()` gets the shared debug desktop. `CreateWindow("debug_tools")` creates a window on that desktop and gives it the id `"debug_tools"`. The id isn't the title the user sees, instead it's just the stable name Echo Chamber can use later to find that same window or restore saved layout information for it.

The two chained calls configure the window:

- `SetTitle("Debug Tools")` sets the text shown in the window's title bar.
- `SetRect(32, 32, 320, 180)` sets the window rectangle using its left, top, right, and bottom coordinates in Echo Chamber's canvas.

`CreateWindow()` returns the window it just made, and these setters return the same window again. That's why the calls can be chained together with dots instead of being written as separate statements (otherwise known as a "fluent" interface).

The button needs a panel to live in:

`new EchoChamberPanel("main", eEchoChamberDock.FILL)` makes a panel with the id `"main"`. `FILL` means this panel takes the usable window space that hasn't been claimed by another docked panel. Because this tiny window only has one panel, it simply fills the inside of the window.

`_win.AddPanel(_panel)` is the step that puts that panel into the window. Creating a panel struct by itself doesn't attach it anywhere.

The last part builds the button and adds it to the panel. `"ping"` is the button's id, `SetCaption("Ping")` sets the words drawn on the button, and `OnClick(...)` gives Echo Chamber the function to run when the button is clicked. Inside that function, `EchoDebugInfo()` writes the test message.

`_win` and `_panel` are only convenient local variables while the UI is being built. Once the panel has been added to the window and the control has been added to the panel, Echo Chamber keeps those pieces as part of the root's UI regardless of whether you lose those variable references.

The [Getting Started](getting-started) page builds on this general shape. It shows how controls can read and edit your real game values, how to split a window into several panels, and how to save the layout between runs.

---

## Make use of the built-in Echo Console

You don't have to build a custom window before Echo Chamber is useful. If you haven't changed the default macros, press F1 and Echo Console opens over the running game.

The Console lets you search Echo logs, inspect a live instances variables in-game (and edit them!), keep important values visible, run debug commands, capture snapshots and crash reports, and use several other built-in debugging tools.

You can also open it from code if necessary:

```js
EchoChamberOpenConsole(GetEchoChamberRoot());
```

`GetEchoChamberRoot()` gets the shared desktop and `EchoChamberOpenConsole()` opens the Console on that desktop. Read [Echo Console](console) when you want to learn the built-in debugger itself.

---

## When Echo Chamber runs itself

In the normal bundled setup, you don't call an Echo Chamber update or draw function yourself. When both `ECHO_DEBUG_ENABLED` and `ECHO_CHAMBER_CONSOLE_ENABLED` are enabled, Echo Chamber creates the default root and a small controller object automatically. That controller runs the shared root once per frame and watches the Console hotkey.

`GetEchoChamberRoot()` also makes sure the default root exists before it returns it. That's why the earlier examples can simply ask for the root and start adding windows.

You only need to run a root yourself when you've deliberately opted out of the bundled controller, or when you've created a separate `EchoChamberRoot` of your own (which is unnecessary for most use cases). If you've disabled the bundled controller but still want to use the normal shared root, keep the root somewhere persistent and run it once per frame:

```js
/// Create
ui_root = GetEchoChamberRoot();

/// Draw GUI End
ui_root.RunDesktop();
```

The Create event stores the root so later events can use the same one. `RunDesktop()` is then called from Draw GUI End, where it handles that root's input, layout, drawing, windows, popups, and other shared UI work for the frame.

Don't also call `RunDesktop()` on the normal shared root while the bundled controller is already running it. You'd be running the same UI twice in one frame and this can lead to weird behaviour.

Echo Chamber's drawing coordinates are also separate from your game's GUI setup. Changing your GUI resolution, room camera, or application-surface size doesn't make the debug desktop automatically follow those coordinates. Theme `ui_scale` changes the size of Echo Chamber's own layout measurements instead.

---

## A useful reading order

1. [Getting Started](getting-started) - build an ordinary window and connect controls to game values.
2. [Echo Console](console) - learn how to use the debugger that already comes with Echo Chamber.
3. [Themes](themes) - change how your tools look.
4. [Advanced Usage](advanced) - handle long lists, custom drawing, popups, shortcuts, and live UI rebuilding.
5. [Echo Chamber API Reference](api-reference) - look up exact constructors, methods, enums, and macros.
6. [Style Reference](style-api-reference) - look up every style type and style setter.

The two reference pages are lookup material. You don't need to read them front to back before using the teaching pages. Use them as, interestingly enough, reference pages for when you have a specific command you want to look up (or want to see the full range of what's available to you).

---

{% include library-footer.html %}
