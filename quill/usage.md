---
layout: default
title: Usage
parent: Quill
nav_order: 2
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Usage Guide

This page shows practical patterns, from simple forms to editor-ish behavior. It's just a small library of patterns that show how you might want to use Quill.

## Basic Single-Line Input

```js
player_data = { display_name: "" };

name_box = QuillSingle("Display Name", "Enter name")
	.BindText(player_data, "display_name")
	.SetMaxLength(20)
	.SetAllowedChars("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-")
	.SetSelectAllOnFocus(true);
```

`BindText` keeps the textbox synced with a struct field. When the user types, your struct updates. If you set the struct field (or call `SetValue`), the box updates too (so manually setting `player_data.display_name = "My name is (Slim Shady)";` would also make the textbox display that).

## Basic Multiline Input

```js
player_data = { notes: "" };

notes_box = QuillMulti("Notes", "Write notes")
	.BindText(player_data, "notes")
	.SetWrap(true)
	.SetInputMode(QUILL_TEXTMODE_TEXT)
	.SetVisibleRows(10)
	.SetResizable(true)
	.SetShowResizeGrip(true);
```

Multiline is where Quill starts getting interesting. Wrap, resizing, a scrollbar, and the optional overlay editor all live here.

## Callback Patterns

Most of the time you want callbacks for two reasons: reacting to a change, and reacting to submission.

The easiest way to keep this sane is to create a small scope struct or grab an instance id, then bind it with `method(...)` so your callback has somewhere to write to that isn't the textbox struct itself.

```js
hook = {
	change_count: 0,
	last_submit: ""
};

__on_change = function(_tb, _new_value) {
	self.change_count += 1;
}

__on_submit = function(_tb, _value) {
	self.last_submit = _value;
}

textbox
	.OnChange(method(hook, __on_change))
	.OnSubmit(method(hook, __on_submit));
```

Quill's callback setters use these signatures:

```js
OnChange(fn) -> fn(tb, new_value)
OnFocus(fn) -> fn(tb)
OnBlur(fn) -> fn(tb)
OnSubmit(fn) -> fn(tb, value)
OnCancel(fn) -> fn(tb)
```

## Value Pipeline and Filtering

Typed input (and `SetValue(...)`) go through a few layers of filtering on it's journey to being displayed in the textbox. This allows you to build validation and formatting rules for exactly what you want textboxes to display.

In order, Quill applies:

First, auto transforms (`SetAutoTrim`, `SetAutoUpper`, `SetAutoLower`). Then any custom transforms from `AddTransform(fn)`. Then the filter function from `SetFilterFn(fn)`. Finally it runs the built-in checks (mode checks, allow/deny checks, numeric checks, max length).

If you're not sure where a character got removed or why a value changed, this pipeline is the place to look.

## Input Modes

Set via `SetInputMode(mode)`.

```js
QUILL_TEXTMODE_TEXT
QUILL_TEXTMODE_INT
QUILL_TEXTMODE_FLOAT
QUILL_TEXTMODE_IDENTIFIER
QUILL_TEXTMODE_PATH
QUILL_TEXTMODE_CODE
QUILL_TEXTMODE_PASSWORD
```

`INT` and `FLOAT` enable numeric restrictions. `CODE` enables tab insertion and auto-indent defaults (and makes the text use the `code` font that is supplied by the theme). `PASSWORD` enables masking defaults.

## Selection and Caret Control

Most of the time you won't touch this directly, but it's there if you need it.

```js
textbox.SetValue("abcdef");
textbox.SetCaret(3);
textbox.SetSelection(1, 4);

var _sel = textbox.GetSelection();
if (_sel.has_selection) {
	show_debug_message("Selection: " + string(_sel.start) + " to " + string(_sel._end));
}
```

Between `GetCaret`/`SetCaret`, `GetSelection`/`SetSelection`, and `SelectAll`, you can drive selection state from code.

## Focus and Tab Order

Tab order is just an integer. Lowest goes first.

```js
first_box.SetTabOrder(0);
second_box.SetTabOrder(1);
third_box.SetTabOrder(2);

second_box.Focus();
```

If necessary, you'll mostly use `Focus`, `Blur`, and `IsFocused` for manually changing focus, along with `SetTabEnabled` and `SetTabOrder` to help with how tab cycles through elements.

## Labels and Layout

Labels are part of the same component, so you configure them on the textbox.

The main helpers are `SetLabel`, `SetLabelVisible`, `SetLabelPlacement(...)`, `SetLabelAlign(...)`, `SetLabelOverflow(...)`, `SetLabelOffset(...)`, and `SetLabelWidth(...)`.

Quill starts with a default textbox width of 150 pixels. You can change this by the method `SetPreferredWidth()` (and get the preferred width via `GetPreferredWidth()`, and the same goes for height). You can also provide a width and height while actively drawing the textbox (`textbox.Draw(x, y, width, height)`).

`GetWidth`/`GetHeight` report label plus textbox union size, while `GetBoxWidth`/`GetBoxHeight` report the textbox only. You can use this for accurately positioning other textboxes or gui elements around each textbox. Bear in mind that if you want a stable layout before the first draw, set the preferred width/height and then don't provide width and height arguments while drawing (or provide the same arguments as preferred). This doesn't matter if you are doing a "pop-in" animation by sizing the textbox though, only if you expect it to be stable from the get go.

## Validation Messaging

Validation messaging is meant to show your user why a specific input was disallowed. You set it when something's wrong, and clear it when it's fine.

```js
if (string_length(model.username) < 3) {
	name_box.SetValidationMessage("At least 3 characters", "warn");
}
else {
	name_box.ClearValidationMessage();
}
```

`SetValidationMessage(text, kind)` supports `"error"`, `"warn"`, and `"info"`.

## Context Menu and Overlay Editor

By default, right clicking a textbox opens the context menu. Multiline boxes can also show an `Edit...` overlay action.

Per-box overlay controls are methods: `SetUseOverlayEditor(flag)` (which enables the "Edit" overlay) and `SetOverlayEditorTitle(title)` (which sets the title for the "Edit" overlay).

For drawing, `QuillDrawOverlays()` draws all open overlays, while `textbox.DrawOverlay()` draws overlays for one owner box.

### Custom context menu

Create new entries for your right context menu via the helpers `QuillContextMenuItem()` and `QuillContextMenuSeparator()`. These can be added globally or per textbox, and will change what options the user has when they right click the textbox:

```js
__menu_clear = function() {
	SetValue("");
}

tb_name = QuillSingle("Name", "Enter your name");

var _clear_item = QuillContextMenuItem("Clear", method(tb_name, __menu_clear), "clear_name")
	.SetShortcut("Ctrl+K")
	.SetEnabled(true);
```

Add items globally (all textboxes):

```js
QuillContextMenuAddItem(_clear_item);
```

Add items for one textbox only:

```js
tb_name.ContextMenuAddItem(
	QuillContextMenuItem("Clear", method(tb_name, __menu_clear), "clear_name")
);
```

You can still open a context menu manually, but this isn't necessary for Quill to function, it will happily handle the context menus for you automatically:

```js
var _items = [
	QuillContextMenuItem("Clear", method(self, __menu_clear)),
	QuillContextMenuSeparator(),
	QuillContextMenuItem("Paste", method(self, __menu_paste)).SetShortcut("Ctrl+V")
];

QUILL.OpenContextMenu(
	_items,
	device_mouse_x_to_gui(0),
	device_mouse_y_to_gui(0),
	box.id
);
```

## Advanced Multiline Fields

When you really need to tweak multiline textboxes to feel perfect, these are the knobs you'll reach for most often:

```js
SetVisibleRows(rows) / GetVisibleRows()

SetPreferredHeight(px) / GetPreferredHeight()
SetMinHeight(px) / GetMinHeight()
SetMaxHeight(px) / GetMaxHeight()

SetResizable(flag) / IsResizable()
SetShowResizeGrip(flag) / IsResizeGripVisible()

SetUseOverlayEditor(flag) / IsUsingOverlayEditor()
SetOverlayEditorTitle(title) / GetOverlayEditorTitle()
```

## Integration Tips

Create boxes in Create, and draw them in Draw GUI. Set your setters during setup so you aren't doing configuration work in hot paths every frame, as this can cause vertex buffer freeze churn (Quill is optimised to try to intelligently swap between hot buffers and frozen buffers, if you are doing something like a "pop in" animation for the textbox via it's width and height, but it's always best to keep churn to a minimum).

Use binding for form state, then validate at boundaries (submit, save, confirm) instead of trying to do heavy validation logic every keypress.

For styling, treat the global theme as your project baseline, then use per-box themes and overrides when you want a component to look different without having to create a bunch of custom themes (although custom themes are great for sharing between projects).

## Two Final Things That Often Trip People Up

These have been touched on already, but I want to explicitly outline them again because they're points that I often see missed.

1. Quill draws "on command", so the exact point in your code where you call `textbox.Draw()` is the where it will be drawn, so you can draw it under OR over other things. This also applies to the overlays (right click context menu and popup text editor). Wherever you call `textbox.DrawOverlay()` is where that will be drawn, so usually, you'd want to layer those two together, drawing the textbox first and then the overlay immediately afterwards (as an aside, you can draw ALL the overlays at once with the `QuillDrawOverlays()` function if you don't want to manually handle each one).

2. All callbacks are "unscoped" by nature. That means, 90% of the time if you just provide a function, that function will run from the scope of the textbox itself. So you'd usually want to scope the function provided to a callback with a method: `textbox.OnChange(method(scope, function));`. Think of a method like a `with()` statement, it shifts the scope of execution to whatever instance/struct you provide for the `scope` argument. So if you want something to be altered on an instance (let's say you want to name a character), you'd provide the id of the instance as the scope:
```js
textbox.OnChange(method(inst_id, function(_tb, _textbox_value) {
	name = _textbox_value;
}));
```
