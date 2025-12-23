---
layout: default
title: Echo Chamber
nav_order: 1
parent: Echo
has_children: true
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

Echo Chamber is a debug UI builder I've designed to help me build debuggers for my frameworks. I'm releasing it publicly because it's become powerful enough to be useful for others building debug UIs too. It's intended for debug overlays first, but you can also use it for lightweight menus like options or pause screens (note: it's not optimised for full production HUDs right now, but that may be reworked in the future). I've tried to keep it powerful while still being as simple as possible to use. Let's start with a very simple example to get a feel for it:

```js
var _root = global.__echo_chamber_root
win = new EchoChamberWindow("test_window")
	.SetTitle("Test window")
	.FitToContent(_root);

toolbar_panel = new EchoChamberPanel("toolbar_panel", eEchoChamberDock.FILL)
	.SetSizeMode(eEchoChamberPanelSizeMode.FIT_CONTENT)
	.SetFlowMode(eEchoChamberPanelFlow.ROW);

ctrl_btn = new EchoChamberButton("toolbar_panel_btn")
	.SetLabel("My button")
	.SetTooltip("A button you can click")
	.OnClick(function() {
		EchoDebugSevere("You clicked the button!");
	});

_root.RegisterWindow(win);
toolbar_panel.AddControl(ctrl_btn);
win.AddPanel(toolbar_panel);
```

That is a simple setup that creates a window, adds a panel to that window and adds a button to that panel. As long as you have the `ECHO_DEBUG_ENABLED` macro in `scr_echo` set to true, then you will automatically get a window being drawn after adding this code (the code should be run in the Create Event of some singleton object). The window will be resizable by clicking and dragging the bottom right corner, you can move it around by clicking and dragging the title of the window, and you can minimize or close it by the corresponding buttons on the title.

When the macro is enabled, Echo will (behind the scenes) create an echo chamber root via this command: `global.__echo_chamber_root = new EchoChamberRoot(new EchoChamberTheme());` and spawn an instance to do the drawing: `global.__echo_controller = instance_create_depth(0, 0, 0, __obj_echo_controller);`, this instance is simply running the command: `global.__echo_chamber_root.RunDesktop();` to handle the drawing.

If you want to disable the Echo macro, feel free to do so, but be aware you'll have to create the root itself (obviously you don't need to name it `global.__echo_chamber_root` if you don't want to), and call `RunDesktop` on that root yourself if you want Echo Chamber to draw. It's not advisable to run multiple desktops at a time. Echo Chamber naturally handles multiple windows, so just set up new windows instead of new roots. Windows automatically respect focus and prevent click bleedthrough.

