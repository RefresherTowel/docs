---
layout: default
title: Echo Chamber Scripting Reference
nav_order: 2
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

## Echo Chamber Scripting Reference

Echo Chamber is the in-game debug UI builder. It is a set of constructors that output structs (Root, Window, Panel, Controls).

Important: you can use Echo Chamber without Echo, but they are designed to play nicely together.

### Enums
#### `eEchoChamberDock`
- `FILL`
- `TOP`
- `BOTTOM`
- `LEFT`
- `RIGHT`

#### `eEchoChamberCollapse`
- `NONE`
- `TO_LEFT`
- `TO_RIGHT`
- `TO_TOP`
- `TO_BOTTOM`

#### `eEchoChamberPanelSizeMode`
- `FIXED`
- `FIT_CONTENT`

#### `eEchoChamberPanelFlow`
- `ROW`
- `COLUMN`

#### `eEchoChamberInputCheck`
- `PRESSED`
- `DOWN`
- `RELEASED`

#### `eEchoChamberInputBindKind`
- `KEY`
- `FUNC`
- `BLOCK`

### Constructors
### `EchoChamberInputBinding()`
Base binding type for input actions.

**Returns**: `Struct.EchoChamberInputBinding`

---

### `EchoChamberInputBindingKey(_key, _check, _ctrl, _alt, _shift)`
Keyboard binding for an input action.

**Arguments**
- `_key` `Real` Keycode (vk_* or ord()).
- `_check` `eEchoChamberInputCheck` Optional, defaults to `PRESSED`.
- `_ctrl` `Bool` Optional, require Ctrl held.
- `_alt` `Bool` Optional, require Alt held.
- `_shift` `Bool` Optional, require Shift held.

**Returns**: `Struct.EchoChamberInputBinding`

---

### `EchoChamberInputBindingFunc(_fn)`
Function binding for an input action.

**Arguments**
- `_fn` `Function` Function that returns true when the action should fire (signature: `function() -> Bool`).

**Returns**: `Struct.EchoChamberInputBinding`

---

### `EchoChamberInputBindingBlock()`
Binding that blocks an action from inheriting from its parent context.

**Returns**: `Struct.EchoChamberInputBinding`

---

### `EchoChamberInputContext(_id)`
Input context for Echo Chamber actions, supports inheritance.

**Arguments**
- `_id` `String`

**Returns**: `Struct.EchoChamberInputContext`

**Public methods**
- `SetParent(_parent_id)`: Set the parent context id for inheritance.
  - **Arguments:**
    - `_parent_id` `String` Parent context id (use `undefined` to clear the parent).
  - **Returns:** `Struct.EchoChamberInputContext`
  - **Additional details:**
    - If `_parent_id` resolves to this context's own id, the call is ignored.
- `GetBinding(_action_id)`: Get the binding for an action id.
  - **Arguments:**
    - `_action_id` `String` Action id to look up.
  - **Returns:** `Struct.EchoChamberInputBinding,Undefined`
  - **Additional details:**
    - This only returns the local binding (it does not walk parent contexts).
- `BindAction(_action_id, _binding)`: Bind an action to a binding.
  - **Arguments:**
    - `_action_id` `String` Action id to bind.
    - `_binding` `Struct.EchoChamberInputBinding` Binding instance (built from `EchoChamberInputBinding*`).
  - **Returns:** `Struct.EchoChamberInputContext`
  - **Additional details:**
    - If `_binding` is not an `EchoChamberInputBinding`, the call is ignored.
- `BindKey(_action_id, _key, _check, _ctrl, _alt, _shift)`: Bind an action to a keyboard key.
  - **Arguments:**
    - `_action_id` `String` Action id to bind.
    - `_key` `Real` Keycode (vk_* or ord()).
    - `_check` `eEchoChamberInputCheck` Optional check type (pressed/down/released).
    - `_ctrl` `Bool` Optional, require Ctrl held.
    - `_alt` `Bool` Optional, require Alt held.
    - `_shift` `Bool` Optional, require Shift held.
  - **Returns:** `Struct.EchoChamberInputContext`
  - **Additional details:**
    - Creates a key binding and forwards to `BindAction`.
- `BindFunc(_action_id, _fn)`: Bind an action to a function.
  - **Arguments:**
    - `_action_id` `String` Action id to bind.
    - `_fn` `Function` Function that returns true when the action should fire (signature: `function() -> Bool`).
  - **Returns:** `Struct.EchoChamberInputContext`
  - **Additional details:**
    - The function is polled each frame while this context is active.
- `BindBlock(_action_id)`: Bind an action to a blocker (prevents inheritance).
  - **Arguments:**
    - `_action_id` `String` Action id to bind.
  - **Returns:** `Struct.EchoChamberInputContext`
  - **Additional details:**
    - Blocks inheritance from the parent context for this action id.
- `ClearAction(_action_id)`: Clear a local action binding so the parent can take over.
  - **Arguments:**
    - `_action_id` `String` Action id to clear.
  - **Returns:** `Struct.EchoChamberInputContext`
  - **Additional details:**
    - Clears only the local binding; parent bindings (if any) will be used again.

---

### `EchoChamberRoot(_theme)`
Root container for debug UI panels and controls.

**Arguments**
- `_theme` `Struct.EchoChamberTheme`

**Returns**: `Struct.EchoChamberRoot`

**Public methods**
- `ApplyTheme(_theme)`: Apply a new theme and reapply defaults across windows and panels.
  - **Arguments:**
    - `_theme` `Struct.EchoChamberTheme` Theme instance to apply.
  - **Returns:** `Struct.EchoChamberRoot`
  - **Additional details:**
    - If `_theme` is not an `EchoChamberTheme`, the call is ignored.
    - Reapplies theme defaults to all registered windows and panels.
- `BeginFrame()`: Snapshot mouse and wheel for this frame.
  - **Arguments:** None.
  - **Returns:** N/A
  - **Additional details:**
    - Resets per-frame state such as mouse/wheel consumption and overlay queue.
    - This is automatically called by `RunDesktop()`, so you do not need to manually call it unless you have a specific reason to do so.
- `GetDefaultInputContextId()`: Return the default input context id.
  - **Arguments:** None.
  - **Returns:** `String`
- `BindCoreInputAction(_action_id, _binding)`: Bind a core Echo Chamber action in the default context.
  - **Arguments:**
    - `_action_id` `String` Action id to bind.
    - `_binding` `Struct.EchoChamberInputBinding` Binding instance.
  - **Returns:** `Struct.EchoChamberRoot`
  - **Additional details:**
    - If the default context or binding is invalid, the call is ignored.
- `GetInputContext(_id)`: Get an input context by id.
  - **Arguments:**
    - `_id` `String` Context id to look up.
  - **Returns:** `Struct.EchoChamberInputContext,Undefined`
- `CreateInputContext(_id, _parent_id)`: Create or return an input context by id.
  - **Arguments:**
    - `_id` `String` Context id to create or fetch.
    - `_parent_id` `String` Optional parent context id (defaults to the root default context when created).
  - **Returns:** `Struct.EchoChamberInputContext,Undefined`
  - **Additional details:**
    - If a context already exists, it is returned and the parent is optionally updated.
- `RemoveInputContext(_id)`: Remove an input context by id.
  - **Arguments:**
    - `_id` `String` Context id to remove.
  - **Returns:** `Bool`
  - **Additional details:**
    - Returns false if the context is the default or is currently in use by any window.
- `InputPressed(_action_id, _window)`: Check whether an action is pressed in the active input context.
  - **Arguments:**
    - `_action_id` `String` Action id to check.
    - `_window` `Struct.EchoChamberWindow` Optional window whose input context should be used.
  - **Returns:** `Bool`
  - **Additional details:**
    - If `_window` is omitted, the focused window context is used.
- `InputDown(_action_id, _window)`: Check whether an action is held in the active input context.
  - **Arguments:**
    - `_action_id` `String` Action id to check.
    - `_window` `Struct.EchoChamberWindow` Optional window whose input context should be used.
  - **Returns:** `Bool`
  - **Additional details:**
    - If `_window` is omitted, the focused window context is used.
- `InputReleased(_action_id, _window)`: Check whether an action is released in the active input context.
  - **Arguments:**
    - `_action_id` `String` Action id to check.
    - `_window` `Struct.EchoChamberWindow` Optional window whose input context should be used.
  - **Returns:** `Bool`
  - **Additional details:**
    - If `_window` is omitted, the focused window context is used.
- `AddPanel(_panel)`: Add a top-level panel to the root.
  - **Arguments:**
    - `_panel` `Struct.EchoChamberPanel` Panel instance to attach.
  - **Returns:** `Struct.EchoChamberPanel,Undefined`
  - **Additional details:**
    - Assigns ownership to the root and its child panels/controls.
- `CreateWindow(_id)`: Create and register a floating debug window.
  - **Arguments:**
    - `_id` `Any` Window id.
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - Applies theme defaults and registers the window with this root.
- `RegisterWindow(_window)`: Register an externally created window instance.
  - **Arguments:**
    - `_window` `Struct.EchoChamberWindow` Window instance to register.
  - **Returns:** `Struct.EchoChamberWindow,Undefined`
  - **Additional details:**
    - Applies theme defaults, sets the window owner, and assigns ownership for all panels/controls.
- `FindWindow(_id)`: Find a registered window by id.
  - **Arguments:**
    - `_id` `Any` Window id.
  - **Returns:** `Struct.EchoChamberWindow,Undefined`
- `FindControl(_id)`: Find a control by id across all windows.
  - **Arguments:**
    - `_id` `Any` Control id.
  - **Returns:** `Struct.EchoChamberControlBase,Undefined`
- `DumpUI()`: Dump the current UI tree and focus/overlay state to the debug log.
  - **Arguments:** None.
  - **Returns:** `Struct.EchoChamberRoot`
  - **Additional details:**
    - Uses `EchoDebugInfo` to output the structure.
- `RemoveWindow(_window_or_id)`: Remove a registered window and detach its panels/controls.
  - **Arguments:**
    - `_window_or_id` `Struct.EchoChamberWindow,Any` Window instance or id.
  - **Returns:** `Bool`
  - **Additional details:**
    - Clears focus, modal, overlays, and mouse capture if they reference the removed window.
- `BringWindowToFront(_window_or_id)`: Bring a window (or id) to the front of the z-order.
  - **Arguments:**
    - `_window_or_id` `Struct.EchoChamberWindow,Any` Window instance or id.
  - **Returns:** N/A
  - **Additional details:**
    - Updates keyboard focus to the brought window.
- `BringWindowToFrontById(_id)`: Bring a window to the front by id.
  - **Arguments:**
    - `_id` `Any` Window id.
  - **Returns:** `Struct.EchoChamberWindow,Undefined`
- `SendWindowToBack(_window_or_id)`: Send a window (or id) to the back of the z-order.
  - **Arguments:**
    - `_window_or_id` `Struct.EchoChamberWindow,Any` Window instance or id.
  - **Returns:** `Bool`
  - **Additional details:**
    - Modal windows stay on top; sending a modal window to back just re-brings it to front.
- `BringWindowsBack()`: Bring all windows back into view so their title bars remain accessible.
  - **Arguments:** None.
  - **Returns:** `Struct.EchoChamberRoot`
- `SetWindowZIndex(_window_or_id, _index)`: Set a window z-order index (0 = back, last = front).
  - **Arguments:**
    - `_window_or_id` `Struct.EchoChamberWindow,Any` Window instance or id.
    - `_index` `Real` Target z-order index.
  - **Returns:** `Bool`
  - **Additional details:**
    - Modal windows are forced to the front index.
- `SetModalWindow(_window_or_id)`: Set the modal window (blocks input to other windows).
  - **Arguments:**
    - `_window_or_id` `Struct.EchoChamberWindow,Any` Window instance or id, or `undefined` to clear.
  - **Returns:** `Bool`
  - **Additional details:**
    - Clears overlays, context menus, and focus that are owned by other windows.
- `ClearModalWindow()`: Clear the current modal window.
  - **Arguments:** None.
  - **Returns:** `Bool`
- `GetModalWindow()`: Get the current modal window (if any).
  - **Arguments:** None.
  - **Returns:** `Struct.EchoChamberWindow,Undefined`
- `SetPersistenceFile(_filename)`: Set the INI filename used for saving and loading UI layout state.
  - **Arguments:**
    - `_filename` `String` INI filename (relative or absolute path).
  - **Returns:** `Struct.EchoChamberRoot`
- `SetPersistenceSection(_section)`: Set the INI section prefix used for saving and loading UI layout state.
  - **Arguments:**
    - `_section` `String` INI section prefix.
  - **Returns:** `Struct.EchoChamberRoot`
- `SaveLayout()`: Save window layout, z-order, and panel state to an INI file.
  - **Arguments:** None.
  - **Returns:** `Bool`
  - **Additional details:**
    - Returns false if the persistence file name is empty.
- `LoadLayout()`: Load window layout, z-order, and panel state from an INI file.
  - **Arguments:** None.
  - **Returns:** `Bool`
  - **Additional details:**
    - Windows and panels must already be created/registered before calling this.
    - Returns false if the file does not exist.
- `SetMouseCapture(_window)`: Capture the mouse for a window interaction (drag/resize).
  - **Arguments:**
    - `_window` `Struct.EchoChamberWindow` Window to own mouse capture.
  - **Returns:** N/A
  - **Additional details:**
    - Only used internally for drag/resize; you usually don't call this directly.
- `ClearMouseCapture(_window)`: Release mouse capture if owned by the given window.
  - **Arguments:**
    - `_window` `Struct.EchoChamberWindow` Window attempting to release capture.
  - **Returns:** N/A
  - **Additional details:**
    - Capture is only cleared if `_window` currently owns it.
- `RunDesktop()`: Run the managed desktop: capture input, process the active window, draw all windows, then draw overlays and tooltip.
  - **Arguments:** None.
  - **Returns:** N/A
  - **Additional details:**
    - Call this once per Draw GUI frame to run Echo Chamber.
- `ConsumeMouse()`: Consume mouse input for all remaining controls this frame.
  - **Arguments:** None.
  - **Returns:** N/A
- `ConsumeWheel()`: Consume mouse wheel for all remaining scroll regions.
  - **Arguments:** None.
  - **Returns:** N/A
- `DrawScrollArea(_scroll_state, _rect, _content_h, _draw_fn)`: Draw a scrollable clipped region and handle mouse wheel scrolling when hovered.
  - **Arguments:**
    - `_scroll_state` `Struct.EchoChamberScrollState` Scroll state that stores the current scroll offset.
    - `_rect` `Struct` `{x1,y1,x2,y2}` Visible clip rect in GUI space.
    - `_content_h` `Real` Total content height in pixels.
    - `_draw_fn` `Function` Draw callback (signature: `function(_root, _rect, _scroll_y)`).
  - **Returns:** N/A
  - **Additional details:**
    - The draw callback should offset its content by `_scroll_y` (positive values scroll down).
    - The scissor clip is already applied to `_rect` when `_draw_fn` runs.
- `PushClipRect(_x1, _y1, _x2, _y2)`: Push a clip rectangle.
  - **Arguments:**
    - `_x1` `Real` Left bound (GUI space).
    - `_y1` `Real` Top bound (GUI space).
    - `_x2` `Real` Right bound (GUI space).
    - `_y2` `Real` Bottom bound (GUI space).
  - **Returns:** N/A
  - **Additional details:**
    - Any existing clip is intersected with the new rect.
- `PopClipRect()`: Pop the most recently pushed clip rectangle.
  - **Arguments:** None.
  - **Returns:** N/A
- `HitTestRect(_x1, _y1, _x2, _y2)`: Simple hit test for a rect.
  - **Arguments:**
    - `_x1` `Real` Left bound (GUI space).
    - `_y1` `Real` Top bound (GUI space).
    - `_x2` `Real` Right bound (GUI space).
    - `_y2` `Real` Bottom bound (GUI space).
  - **Returns:** `Bool`
  - **Additional details:**
    - Respects `mouse_consumed` and the current clip region.
- `RequestTooltip(_control_id, _text, _anchor_x, _anchor_y)`: Request a tooltip for a given control id.
  - **Arguments:**
    - `_control_id` `String` Control id requesting the tooltip.
    - `_text` `String` Tooltip text.
    - `_anchor_x` `Real` Tooltip anchor X (GUI space).
    - `_anchor_y` `Real` Tooltip anchor Y (GUI space).
  - **Returns:** N/A
  - **Additional details:**
    - If a modal overlay is active, only its owner may request a tooltip.
- `SetActiveOverlayOwner(_control_id)`: Mark a control as owning a modal overlay (e.g. a dropdown).
  - **Arguments:**
    - `_control_id` `String,Undefined` Control id to own the overlay (use `undefined` to clear).
  - **Returns:** N/A
  - **Additional details:**
    - Overlay ownership is tied to the current window context.
- `ClearActiveOverlayOwner()`: Clear the active overlay (if any).
  - **Arguments:** None.
  - **Returns:** N/A
- `RequestCloseOverlay()`: Request the currently active overlay (if any) to close.
  - **Arguments:** None.
  - **Returns:** N/A
  - **Additional details:**
    - Overlay owners should honor this during `ProcessAndDraw`.
- `QueueOverlay(_owner_id, _draw_fn, _rect, _owner_window)`: Queue an overlay draw callback. Overlays are drawn after all windows.
  - **Arguments:**
    - `_owner_id` `Any` Control id that owns the overlay (used for overlay focus tracking).
    - `_draw_fn` `Function` Draw callback (signature: `function(_root)`).
    - `_rect` `Struct` Optional `{x1,y1,x2,y2}` overlay rect used for clipping and hit testing.
    - `_owner_window` `Struct.EchoChamberWindow` Optional owner window used for theme overrides.
  - **Returns:** N/A
- `OpenContextMenu(_items, _x, _y, _owner_window)`: Open a context menu overlay at a screen position.
  - **Arguments:**
    - `_items` `Array` Array of item structs: `{ label, on_click, enabled, shortcut }` or `{ is_separator:true }`.
    - `_x` `Real` Screen X position (GUI space).
    - `_y` `Real` Screen Y position (GUI space).
    - `_owner_window` `Struct.EchoChamberWindow` Optional owner window for theme overrides.
  - **Returns:** N/A
  - **Additional details:**
    - `on_click` is a callback with signature `function()`.
- `CloseContextMenu()`: Close the active context menu overlay (if open).
  - **Arguments:** None.
  - **Returns:** N/A
- `IsContextMenuOpen()`: Returns true if the context menu overlay is open.
  - **Arguments:** None.
  - **Returns:** `Bool`
- `DrawOverlays()`: Draw all queued overlays once per frame.
  - **Arguments:** None.
  - **Returns:** N/A
  - **Additional details:**
    - Overlays are drawn after all windows and are clipped to their queued rects.
- `LayoutPanels(_x1, _y1, _x2, _y2)`: Dock + collapse layout. Assigns rects to all top-level panels.
  - **Arguments:**
    - `_x1` `Real` Left bound (GUI space).
    - `_y1` `Real` Top bound (GUI space).
    - `_x2` `Real` Right bound (GUI space).
    - `_y2` `Real` Bottom bound (GUI space).
  - **Returns:** N/A
- `DrawTooltip()`: Draw simple tooltip for the current tooltip_control_id (if delay elapsed).
  - **Arguments:** None.
  - **Returns:** N/A
- `ShowToast(_text, _duration_ms)`: Show a short toast message (non-blocking).
  - **Arguments:**
    - `_text` `Any` Toast text (converted to string).
    - `_duration_ms` `Real` Optional duration in milliseconds.
  - **Returns:** N/A
  - **Additional details:**
    - Toasts appear in the bottom right of the game window.
- `CopyToClipboard(_text, _toast_text, _duration_ms)`: Copy text to clipboard and show a toast confirmation.
  - **Arguments:**
    - `_text` `Any` Text to copy.
    - `_toast_text` `Any` Optional toast text (defaults to a preview of `_text`).
    - `_duration_ms` `Real` Optional toast duration in milliseconds.
  - **Returns:** N/A
- `DrawToast()`: Draw active toast notifications for this frame.
  - **Arguments:** None.
  - **Returns:** N/A
- `DrawPanelBackground(_panel)`: Convenience: draw a basic panel background.
  - **Arguments:**
    - `_panel` `Struct.EchoChamberPanel` Panel to draw.
  - **Returns:** N/A
- `DrawPanelCollapseHandle(_panel)`: Draw a collapse handle for a panel (if it supports collapsing).
  - **Arguments:**
    - `_panel` `Struct.EchoChamberPanel` Panel to draw.
  - **Returns:** N/A
- `SetTextInputSource(_fn)`: Set a function that returns the current active text input string. If not set, keyboard_string is used.
  - **Arguments:**
    - `_fn` `Function` Text source callback (signature: `function() -> String`).
  - **Returns:** N/A
  - **Additional details:**
    - When a source function is set, the active text input is treated as read-only and pulls its value from this function each frame.
- `SetTextInputSeed(_fn)`: Set a function that seeds the active text input string when focusing. If not set, keyboard_string is used.
  - **Arguments:**
    - `_fn` `Function` Seed callback (signature: `function(_text)`), where `_text` is the initial seed value.
  - **Returns:** N/A
  - **Additional details:**
    - Use this to sync the initial focus value into your own input storage when a text input gains focus.
- `FocusTextInput(_id, _initial_text, _placeholder, _commit_fn, _config)`: Focus a text input by id and seed its initial content.
  - **Arguments:**
    - `_id` `Any` Text input id to focus.
    - `_initial_text` `String` Initial text value.
    - `_placeholder` `String` Placeholder text shown when empty.
    - `_commit_fn` `Function` Optional commit callback (signature: `function(_final_text)`).
    - `_config` `Struct` Optional config struct for read-only, filters, and caret styling.
  - **Returns:** N/A
  - **Additional details:**
    - `_commit_fn` runs on blur after the final string is synced from the text source (if any).
- `BlurTextInput(_id)`: Blur a focused text input by id.
  - **Arguments:**
    - `_id` `Any` Text input id to blur.
  - **Returns:** `String`
  - **Additional details:**
    - Returns `""` if the id is not currently focused.
    - Commits the final value (after syncing from the text source) before returning.
- `IsActiveTextInput(_id)`: Returns true if the given id is the currently focused text input.
  - **Arguments:**
    - `_id` `Any` Text input id to check.
  - **Returns:** `Bool`
- `GetActiveText()`: Return the current active text string while a text input is focused.
  - **Arguments:** None.
  - **Returns:** `String`
  - **Additional details:**
    - If a text source is set, this returns the source value.
- `GetTextBuffer()`: Return the last committed text buffer for the active text input.
  - **Arguments:** None.
  - **Returns:** `String`
- `FocusControl(_id, _rect)`: Give keyboard focus to a non-text control by id.
  - **Arguments:**
    - `_id` `Any` Control id to focus.
    - `_rect` `Struct` `{x1,y1,x2,y2}` control rect in GUI space.
  - **Returns:** N/A
  - **Additional details:**
    - This focus is separate from text input focus.
- `IsControlFocused(_id)`: Returns true if the given control id currently owns keyboard focus (and no text input is active).
  - **Arguments:**
    - `_id` `Any` Control id to check.
  - **Returns:** `Bool`
  - **Additional details:**
    - Returns false when an overlay is active and owned by another control.
- `BlurControlFocus(_id)`: Blur (clear) keyboard focus from a control by id.
  - **Arguments:**
    - `_id` `Any` Optional id to validate before clearing (if provided, it must match the focused id).
  - **Returns:** `Bool`
- `RegisterFocusable(_id, _rect)`: Register a focusable control for Tab navigation.
  - **Arguments:**
    - `_id` `Any` Control id.
    - `_rect` `Struct` `{x1,y1,x2,y2}` control rect in GUI space.
  - **Returns:** N/A

---

### `EchoChamberWindow(_id)`
Floating debug window that owns a collection of docked panels.

**Arguments**
- `_id` `Any`

**Returns**: `Struct.EchoChamberWindow`

**Public methods**
- `SetTitle(_title)`: Set the window title text.
  - **Arguments:**
    - `_title` `Any` Title text (converted to string).
  - **Returns:** `Struct.EchoChamberWindow`
- `SetInputContext(_context_id, _parent_id)`: Set the input context id used for this window.
  - **Arguments:**
    - `_context_id` `String` Context id (use `undefined` to clear).
    - `_parent_id` `String` Optional parent context id.
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - When a root is assigned, the context is created if missing.
- `SwapInputContext(_context_id, _parent_id)`: Swap the input context and remove the old one if unused.
  - **Arguments:**
    - `_context_id` `String` New context id.
    - `_parent_id` `String` Optional parent context id.
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - Attempts to remove the previous context if it is unused by any window.
- `SetWindowStyleKey(_key)`: Set the window style key (for theme.window_styles).
  - **Arguments:**
    - `_key` `String` Style key.
  - **Returns:** `Struct.EchoChamberWindow`
- `SetHeaderStyleKey(_key)`: Set the header style key (for theme.header_styles).
  - **Arguments:**
    - `_key` `String` Style key.
  - **Returns:** `Struct.EchoChamberWindow`
- `SetChromeButtonStyleKey(_key)`: Set the chrome button style key (for theme.button_styles).
  - **Arguments:**
    - `_key` `String` Style key.
  - **Returns:** `Struct.EchoChamberWindow`
- `ApplyTheme(_theme)`: Apply a theme override to this window and its children.
  - **Arguments:**
    - `_theme` `Struct.EchoChamberTheme` Theme override (use `undefined` to clear).
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - Overrides only this window and its panels/controls.
- `ClearThemeOverride()`: Clear the window theme override (reverts to the root theme).
  - **Arguments:** None.
  - **Returns:** `Struct.EchoChamberWindow`
- `SetPadding(_value)`: Set the content padding for this window.
  - **Arguments:**
    - `_value` `Real` Padding in pixels.
  - **Returns:** `Struct.EchoChamberWindow`
- `SetMargin(_x, [_y])`: Set the outer margin for this window in GUI-space.
  - **Arguments:**
    - `_x` `Real` Horizontal margin.
    - `_y` `Real` Optional vertical margin (defaults to `_x`).
  - **Returns:** `Struct.EchoChamberWindow`
- `SetTitlebarHeight(_value)`: Set the titlebar height for this window.
  - **Arguments:**
    - `_value` `Real` Titlebar height in pixels.
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - Disables theme-driven titlebar sizing until `SetTitlebarAuto(true)` is used.
- `SetTitlebarAuto(_flag)`: Set whether the titlebar height is driven by the current theme.
  - **Arguments:**
    - `_flag` `Bool` Enable or disable auto sizing.
  - **Returns:** `Struct.EchoChamberWindow`
- `SetResizeGripSize(_value)`: Set the resize grip size for this window.
  - **Arguments:**
    - `_value` `Real` Grip size in pixels.
  - **Returns:** `Struct.EchoChamberWindow`
- `SetVisible(_flag)`: Show or hide this window.
  - **Arguments:**
    - `_flag` `Bool` Visible flag.
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - Hiding clears modal/capture/overlay ownership tied to this window.
- `SetShowChromeButtons(_show_close, _show_minimize, _show_pin)`: Configure which chrome buttons are shown in the window header.
  - **Arguments:**
    - `_show_close` `Bool` Show or hide the close button.
    - `_show_minimize` `Bool` Show or hide the minimize button.
    - `_show_pin` `Bool` Show or hide the pin button.
  - **Returns:** `Struct.EchoChamberWindow`
- `OnClose(_fn)`: Set a callback that runs when the window is closed via the close button.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function()`).
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - Also fired when `Close()` is called.
- `OnMove(_fn)`: Set a callback that runs when the window moves.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function()`).
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - Fired after the window rect changes position.
- `OnResize(_fn)`: Set a callback that runs when the window resizes.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function()`).
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - Fired after the window rect changes size.
- `OnShow(_fn)`: Set a callback that runs when the window becomes visible.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function()`).
  - **Returns:** `Struct.EchoChamberWindow`
- `OnHide(_fn)`: Set a callback that runs when the window is hidden.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function()`).
  - **Returns:** `Struct.EchoChamberWindow`
- `OnFocus(_fn)`: Set a callback that runs when the window gains focus.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function()`).
  - **Returns:** `Struct.EchoChamberWindow`
- `OnBlur(_fn)`: Set a callback that runs when the window loses focus.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function()`).
  - **Returns:** `Struct.EchoChamberWindow`
- `OnMinimize(_fn)`: Set a callback that runs when the window is minimized.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function()`).
  - **Returns:** `Struct.EchoChamberWindow`
- `OnRestore(_fn)`: Set a callback that runs when the window is restored.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function()`).
  - **Returns:** `Struct.EchoChamberWindow`
- `Close()`: Close the window (sets visible to false) and fires `OnClose`.
  - **Arguments:** None.
  - **Returns:** N/A
  - **Additional details:**
    - Calls `SetVisible(false)` first, then runs the close callback if assigned.
- `SetPinned(_flag)`: Set whether the window is pinned (disables dragging and resizing).
  - **Arguments:**
    - `_flag` `Bool` True to pin, false to unpin.
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - Cancels any active drag/resize and clears mouse capture.
- `TogglePinned()`: Toggle pinned state.
  - **Arguments:** None.
  - **Returns:** `Struct.EchoChamberWindow`
- `SetMinimized(_flag)`: Set whether the window is minimized (collapses content; only the title bar remains).
  - **Arguments:**
    - `_flag` `Bool` True to minimize, false to restore.
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - Restores to the previous height (clamped by min/max).
    - Clears any active overlay owned by this window.
    - Fires `OnMinimize` or `OnRestore` as appropriate.
- `ToggleMinimized()`: Toggle minimized state.
  - **Arguments:** None.
  - **Returns:** `Struct.EchoChamberWindow`
- `SetRect(_x1, _y1, _x2, _y2)`: Set the window rectangle in GUI-space.
  - **Arguments:**
    - `_x1` `Real` Left edge.
    - `_y1` `Real` Top edge.
    - `_x2` `Real` Right edge.
    - `_y2` `Real` Bottom edge.
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - Size is clamped to min/max.
    - Marks the rect as user-set and clears any pending fit-to-content on add.
- `SetPosition(_x, _y)`: Set the window position in GUI-space (size is unchanged).
  - **Arguments:**
    - `_x` `Real` New left edge.
    - `_y` `Real` New top edge.
  - **Returns:** `Struct.EchoChamberWindow`
- `GetWidth()`: Get the current window width (in GUI-space).
  - **Arguments:** None.
  - **Returns:** `Real`
- `GetHeight()`: Get the current window height (in GUI-space).
  - **Arguments:** None.
  - **Returns:** `Real`
- `SetMinSize(_w, _h)`: Set minimum width and height for this window.
  - **Arguments:**
    - `_w` `Real` Minimum width (clamped to at least 64).
    - `_h` `Real` Minimum height (clamped to at least 64).
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - If the current max size is smaller, it is raised to match.
- `SetMaxSize(_w, _h)`: Set maximum width and height for this window (0 means no max).
  - **Arguments:**
    - `_w` `Real` Maximum width (0 disables max width).
    - `_h` `Real` Maximum height (0 disables max height).
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - If the max size is smaller than the minimum, it is clamped up to the minimum.
- `FitToContent([_root])`: Resize the window once to fit current content.
  - **Arguments:**
    - `_root` `Struct.EchoChamberRoot` Optional root to use for measurement (defaults to owner root).
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - If no panels exist yet, the fit is deferred until the next panel is added.
    - The result is clamped to any min/max size settings.
- `SetAutoFit(_flag)`: Enable or disable auto-fit after layout changes.
  - **Arguments:**
    - `_flag` `Bool` True to auto-fit on future layout changes.
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - If a layout batch is active, the fit is deferred until `EndLayoutBatch`.
- `AddPanel(_panel)`: Add a top-level panel to this window.
  - **Arguments:**
    - `_panel` `Struct.EchoChamberPanel` Panel to add.
  - **Returns:** `Struct.EchoChamberPanel,Undefined`
  - **Additional details:**
    - Assigns ownership pointers on the panel and its children.
    - Triggers fit-to-content or auto-fit depending on window settings.
- `RemovePanel(_panel_or_id)`: Remove a panel from this window (top-level or nested).
  - **Arguments:**
    - `_panel_or_id` `Struct.EchoChamberPanel,Any` Panel struct or panel id.
  - **Returns:** `Bool`
  - **Additional details:**
    - Detaches ownership pointers for the removed panel tree.
    - Triggers auto-fit when enabled.
- `ClearPanels()`: Remove all panels from this window.
  - **Arguments:** None.
  - **Returns:** N/A
  - **Additional details:**
    - Detaches all panel trees and triggers auto-fit when enabled.
- `FindPanel(_id)`: Find a panel in this window by id (searches nested container panels too).
  - **Arguments:**
    - `_id` `Any` Panel id (converted to string).
  - **Returns:** `Struct.EchoChamberPanel,Undefined`
- `FindControl(_id)`: Find a control in this window by id (searches nested panels too).
  - **Arguments:**
    - `_id` `Any` Control id (converted to string).
  - **Returns:** `Struct.EchoChamberControlBase,Undefined`
- `MoveControlToPanel(_control_or_id, _panel_or_id, [_index])`: Move a control to another panel in this window.
  - **Arguments:**
    - `_control_or_id` `Struct.EchoChamberControlBase,Any` Control or control id.
    - `_panel_or_id` `Struct.EchoChamberPanel,Any` Target panel or panel id.
    - `_index` `Real` Optional target index (clamped).
  - **Returns:** `Bool`
- `ContainsPoint(_x, _y)`: Return true if a point is inside this window's current rectangle.
  - **Arguments:**
    - `_x` `Real` X position in GUI space.
    - `_y` `Real` Y position in GUI space.
  - **Returns:** `Bool`
  - **Additional details:**
    - Returns false when the window is not visible.
- `BeginLayoutBatch()`: Begin a layout batch (defers FitToContent until EndLayoutBatch).
  - **Arguments:** None.
  - **Returns:** `Struct.EchoChamberWindow`
- `EndLayoutBatch()`: End a layout batch and apply any deferred FitToContent.
  - **Arguments:** None.
  - **Returns:** `Struct.EchoChamberWindow`
  - **Additional details:**
    - Only triggers when the batch depth returns to zero.
- `LayoutPanels(_root)`: Layout this window's panels into the current content rect.
  - **Arguments:**
    - `_root` `Struct.EchoChamberRoot` Root for layout metrics.
  - **Returns:** N/A
- `ProcessWindowInteractions(_root)`: Handle mouse interactions for dragging/resizing and chrome button clicks.
  - **Arguments:**
    - `_root` `Struct.EchoChamberRoot` Root for input state and focus.
  - **Returns:** N/A
  - **Additional details:**
    - Does nothing if the window is not visible.
- `Draw(_root)`: Draw the window chrome and all owned panels.
  - **Arguments:**
    - `_root` `Struct.EchoChamberRoot` Root for theme and drawing helpers.
  - **Returns:** N/A

---

### `EchoChamberPanel(_id, _dock)`
Layout panel docked to an edge or fill.

**Arguments**
- `_id` `Any`
- `_dock` `eEchoChamberDock`

**Returns**: `Struct.EchoChamberPanel`

**Public methods**
- `AddControl(_control)`: Add a control to this panel.
  - **Arguments:**
    - `_control` `Struct.EchoChamberControlBase` Control to add.
  - **Returns:** `Struct.EchoChamberControlBase,Undefined`
  - **Additional details:**
    - Assigns ownership pointers to the control.
    - Triggers fit-to-content or auto-fit depending on window settings.
- `InsertControl(_control, _index)`: Insert a control at a specific index (clamped).
  - **Arguments:**
    - `_control` `Struct.EchoChamberControlBase` Control to insert.
    - `_index` `Real` Target index (clamped).
  - **Returns:** `Struct.EchoChamberControlBase,Undefined`
  - **Additional details:**
    - If the control already belongs to another panel, it is removed first.
- `MoveControl(_control_or_id, _index)`: Reorder a direct control to a specific index (clamped).
  - **Arguments:**
    - `_control_or_id` `Struct.EchoChamberControlBase,Any` Control or control id.
    - `_index` `Real` Target index (clamped).
  - **Returns:** `Bool`
  - **Additional details:**
    - Only reorders direct children of this panel.
- `MoveControlToPanel(_control_or_id, _target_panel, [_index])`: Move a control to another panel.
  - **Arguments:**
    - `_control_or_id` `Struct.EchoChamberControlBase,Any` Control or control id.
    - `_target_panel` `Struct.EchoChamberPanel` Target panel.
    - `_index` `Real` Optional target index (clamped).
  - **Returns:** `Bool`
- `SetControlOrder(_ids)`: Reorder direct controls using a list of ids.
  - **Arguments:**
    - `_ids` `Array<Any>` Control ids in desired order.
  - **Returns:** `Struct.EchoChamberPanel`
  - **Additional details:**
    - Any ids not listed keep their relative order at the end.
- `RemoveControl(_control_or_id)`: Remove a control from this panel (direct or nested).
  - **Arguments:**
    - `_control_or_id` `Struct.EchoChamberControlBase,Any` Control or control id.
  - **Returns:** `Bool`
  - **Additional details:**
    - If attached to a root, control focus/hover state is cleaned up.
- `ClearControls()`: Remove all direct controls from this panel.
  - **Arguments:** None.
  - **Returns:** `Struct.EchoChamberPanel`
  - **Additional details:**
    - Only direct controls are removed; nested panels are untouched.
- `AddChildPanel(_panel)`: Add a child panel (for container usage).
  - **Arguments:**
    - `_panel` `Struct.EchoChamberPanel` Child panel to add.
  - **Returns:** `Struct.EchoChamberPanel,Undefined`
  - **Additional details:**
    - Marks this panel as a container and assigns ownership pointers.
- `RemoveChildPanel(_panel_or_id)`: Remove a child panel from this panel (direct or nested).
  - **Arguments:**
    - `_panel_or_id` `Struct.EchoChamberPanel,Any` Panel or panel id.
  - **Returns:** `Bool`
- `ClearChildPanels()`: Remove all child panels from this panel.
  - **Arguments:** None.
  - **Returns:** `Struct.EchoChamberPanel`
  - **Additional details:**
    - Clears container state and triggers auto-fit when enabled.
- `FindControl(_id)`: Find a direct or nested control within this panel by id.
  - **Arguments:**
    - `_id` `Any` Control id (converted to string).
  - **Returns:** `Struct.EchoChamberControlBase,Undefined`
- `SetSizeMode(_mode)`: Configure how this panel resolves its dock size.
  - **Arguments:**
    - `_mode` `eEchoChamberPanelSizeMode` Fixed or fit-to-content.
  - **Returns:** `Struct.EchoChamberPanel`
- `SetSize(_value)`: Set dock thickness when using fixed sizing.
  - **Arguments:**
    - `_value` `Real` Dock thickness in pixels.
  - **Returns:** `Struct.EchoChamberPanel`
  - **Additional details:**
    - Raises max size if it is below the fixed size.
- `SetFlowMode(_flow_mode)`: Set how child controls flow within the panel.
  - **Arguments:**
    - `_flow_mode` `eEchoChamberPanelFlow` Row or column layout.
  - **Returns:** `Struct.EchoChamberPanel`
- `SetScrollable(_flag)`: Enable or disable vertical scrolling for this panel.
  - **Arguments:**
    - `_flag` `Bool` Scrollable flag.
  - **Returns:** `Struct.EchoChamberPanel`
  - **Additional details:**
    - When enabling, a scroll state is created if missing.
- `SetScrollState(_state)`: Assign a scroll state for this panel (used when scrollable).
  - **Arguments:**
    - `_state` `Struct.EchoChamberScrollState` Scroll state to use.
  - **Returns:** `Struct.EchoChamberPanel`
- `SetPadding(_value)`: Set panel content padding.
  - **Arguments:**
    - `_value` `Real` Padding in pixels.
  - **Returns:** `Struct.EchoChamberPanel`
- `SetMargin(_x, [_y])`: Set panel outer margin in GUI-space.
  - **Arguments:**
    - `_x` `Real` Horizontal margin.
    - `_y` `Real` Optional vertical margin (defaults to `_x`).
  - **Returns:** `Struct.EchoChamberPanel`
- `SetGap(_value)`: Set panel control gap spacing.
  - **Arguments:**
    - `_value` `Real` Gap in pixels.
  - **Returns:** `Struct.EchoChamberPanel`
- `SetRowHeight(_value)`: Set panel row height for controls.
  - **Arguments:**
    - `_value` `Real` Row height in pixels.
  - **Returns:** `Struct.EchoChamberPanel`
- `SetCollapsedSize(_value)`: Set collapsed dock thickness for this panel.
  - **Arguments:**
    - `_value` `Real` Collapsed thickness in pixels.
  - **Returns:** `Struct.EchoChamberPanel`
- `SetCollapseMode(_mode)`: Set the panel collapse mode.
  - **Arguments:**
    - `_mode` `eEchoChamberCollapse` Collapse direction (or `NONE`).
  - **Returns:** `Struct.EchoChamberPanel`
- `SetCollapsed(_value)`: Set whether this panel is collapsed.
  - **Arguments:**
    - `_value` `Bool` Collapsed flag.
  - **Returns:** `Struct.EchoChamberPanel`
- `SetPanelStyleKey(_key)`: Set the panel style key (for theme.panel_styles).
  - **Arguments:**
    - `_key` `String` Style key.
  - **Returns:** `Struct.EchoChamberPanel`
- `SetMinSize(_value)`: Set minimum dock thickness when using fit-to-content.
  - **Arguments:**
    - `_value` `Real` Minimum thickness in pixels.
  - **Returns:** `Struct.EchoChamberPanel`
  - **Additional details:**
    - Raises max size if it is below the minimum.
- `SetMaxSize(_value)`: Set maximum dock thickness when using fit-to-content.
  - **Arguments:**
    - `_value` `Real` Maximum thickness in pixels.
  - **Returns:** `Struct.EchoChamberPanel`
- `SetContentDrawer(_fn)`: Assign a custom content drawer for this panel.
  - **Arguments:**
    - `_fn` `Function` Draw callback (signature: `function(_root, _rect)`), where `_rect` is the panel content rect.
  - **Returns:** `Struct.EchoChamberPanel`
  - **Additional details:**
    - The callback runs after controls/child panels are drawn.
- `GetThickness()`: Get panel thickness based on collapsed state.
  - **Arguments:** None.
  - **Returns:** `Real`
  - **Additional details:**
    - Returns `collapsed_size` when collapsed and a collapse mode is active.
- `ResolveThickness(_root, _avail_width, _avail_height)`: Resolve actual thickness for layout considering size mode.
  - **Arguments:**
    - `_root` `Struct.EchoChamberRoot` Root for theme metrics.
    - `_avail_width` `Real` Available width.
    - `_avail_height` `Real` Available height.
  - **Returns:** `Real`
  - **Additional details:**
    - Includes margins and collapse handle sizing.
    - Uses fit-to-content sizing when size mode is `FIT_CONTENT`.
- `Draw(_root)`: Draw this panel and its contents (controls or child panels).
  - **Arguments:**
    - `_root` `Struct.EchoChamberRoot` Root for theme and drawing helpers.
  - **Returns:** N/A

---

### `EchoChamberScrollState(_id)`
Persistent scroll state for a scrollable region.

**Arguments**
- `_id` `Any`

**Returns**: `Struct.EchoChamberScrollState`

**Public methods**
- `SetScrollY(_y)`: Set the scroll offset in pixels.
  - **Arguments:**
    - `_y` `Real` Scroll offset in pixels.
  - **Returns:** `Struct.EchoChamberScrollState`
- `ScrollBy(_dy)`: Scroll by a delta in pixels (positive scrolls down).
  - **Arguments:**
    - `_dy` `Real` Delta in pixels.
  - **Returns:** `Struct.EchoChamberScrollState`
- `Reset()`: Reset scroll to the top.
  - **Arguments:** None.
  - **Returns:** `Struct.EchoChamberScrollState`

---

### `EchoChamberControlBase(_id)`
Base type for all debug UI controls.

**Arguments**
- `_id` `Any`

**Returns**: `Struct.EchoChamberControlBase`

**Public methods**
- `GetRoot()`: Get the owning root for this control (if attached).
  - **Arguments:** None.
  - **Returns:** `Struct.EchoChamberRoot,Undefined`
- `GetWindow()`: Get the owning window for this control (if attached).
  - **Arguments:** None.
  - **Returns:** `Struct.EchoChamberWindow,Undefined`
- `GetPanel()`: Get the owning panel for this control (if attached).
  - **Arguments:** None.
  - **Returns:** `Struct.EchoChamberPanel,Undefined`
- `SetPreferredWidth(_width)`: Set a preferred pixel width for this control when arranged in a row panel.
  - **Arguments:**
    - `_width` `Real` Preferred width in pixels.
  - **Returns:** `Struct.EchoChamberControlBase`
- `SetPreferredHeight(_height)`: Set a preferred pixel height for this control.
  - **Arguments:**
    - `_height` `Real` Preferred height in pixels.
  - **Returns:** `Struct.EchoChamberControlBase`
- `SetFillWidth(_flag)`: Set whether this control fills the available row width.
  - **Arguments:**
    - `_flag` `Bool` Fill width flag.
  - **Returns:** `Struct.EchoChamberControlBase`
- `SetPadding(_x, [_y])`: Set inner padding for this control.
  - **Arguments:**
    - `_x` `Real` Horizontal padding in pixels.
    - `_y` `Real` Optional vertical padding (defaults to `_x`).
  - **Returns:** `Struct.EchoChamberControlBase`
- `SetMargin(_x, [_y])`: Set outer margin for this control.
  - **Arguments:**
    - `_x` `Real` Horizontal margin in pixels.
    - `_y` `Real` Optional vertical margin (defaults to `_x`).
  - **Returns:** `Struct.EchoChamberControlBase`
- `SetLabel(_text)`: Set the control's display label (used by controls that render a label).
  - **Arguments:**
    - `_text` `Any` Label text (converted to string).
  - **Returns:** `Struct.EchoChamberControlBase`
- `SetTooltip(_text)`: Set the control tooltip (shown on hover where supported).
  - **Arguments:**
    - `_text` `Any` Tooltip text (converted to string).
  - **Returns:** `Struct.EchoChamberControlBase`
- `SetControlStyleKey(_style)`: Set the theme style key for this control (e.g. button/toggle/dropdown styles).
  - **Arguments:**
    - `_style` `Any` Style key (converted to string).
  - **Returns:** `Struct.EchoChamberControlBase`
- `SetVisible(_flag)`: Show or hide this control.
  - **Arguments:**
    - `_flag` `Bool` Visible flag.
  - **Returns:** `Struct.EchoChamberControlBase`
- `SetEnabled(_flag)`: Enable or disable this control (disabled controls should not accept input).
  - **Arguments:**
    - `_flag` `Bool` Enabled flag.
  - **Returns:** `Struct.EchoChamberControlBase`
- `ProcessAndDraw(_root, _panel, _rect)`: Override: process input and draw using the given rect.
  - **Arguments:**
    - `_root` `Struct.EchoChamberRoot` Root for input and theme.
    - `_panel` `Struct.EchoChamberPanel` Owning panel.
    - `_rect` `Struct` `{x1,y1,x2,y2}` draw rect in GUI space.
  - **Returns:** N/A

---

### `EchoChamberLabel(_id)`
Non-interactive text label.

**Arguments**
- `_id` `Any`

**Returns**: `Struct.EchoChamberLabel`

**Public methods**
- `SetText(_text)`: Set the label text.
  - **Arguments:**
    - `_text` `Any` Text to display (converted to string).
  - **Returns:** `Struct.EchoChamberLabel`
- `BindText(_source, [_key_or_fn])`: Bind the label text to a struct field or getter function.
  - **Arguments:**
    - `_source` `Struct,Function` Struct to read from, or a getter function (signature: `function() -> Any`).
    - `_key_or_fn` `String` Optional struct field key when `_source` is a struct.
  - **Returns:** `Struct.EchoChamberLabel`
  - **Additional details:**
    - If `_source` is callable, it becomes the getter, `_key_or_fn` is ignored, and any struct binding is cleared.
    - If `_source` is a struct, `_key_or_fn` is the field key and any function binding is cleared.
    - If the getter returns `undefined`, the label keeps its previous text.
- `SetAlign(_align)`: Set text alignment ("left", "center", "right").
  - **Arguments:**
    - `_align` `String` Alignment string.
  - **Returns:** `Struct.EchoChamberLabel`
- `UseSmallFont(_flag)`: Use the smaller theme font.
  - **Arguments:**
    - `_flag` `Bool` True to use `font_small`, false to use `font_body`.
  - **Returns:** `Struct.EchoChamberLabel`

---

### `EchoChamberTextBox(_id)`
Non-interactive text box that wraps text to its width.

**Arguments**
- `_id` `Any`

**Returns**: `Struct.EchoChamberTextBox`

**Public methods**
- `SetText(_text)`: Set the text content for this box.
  - **Arguments:**
    - `_text` `Any` Text to display (converted to string).
  - **Returns:** `Struct.EchoChamberTextBox`
- `BindText(_source, [_key_or_fn])`: Bind the text content to a struct field or getter function.
  - **Arguments:**
    - `_source` `Struct,Function` Struct to read from, or a getter function (signature: `function() -> Any`).
    - `_key_or_fn` `String` Optional struct field key when `_source` is a struct.
  - **Returns:** `Struct.EchoChamberTextBox`
  - **Additional details:**
    - If `_source` is callable, it becomes the getter, `_key_or_fn` is ignored, and any struct binding is cleared.
    - If `_source` is a struct, `_key_or_fn` is the field key and any function binding is cleared.
    - If the getter returns `undefined`, the text box keeps its previous text.
- `SetAlign(_align)`: Set text alignment ("left", "center", "right").
  - **Arguments:**
    - `_align` `String` Alignment string.
  - **Returns:** `Struct.EchoChamberTextBox`
- `UseSmallFont(_flag)`: Use the smaller theme font.
  - **Arguments:**
    - `_flag` `Bool` True to use `font_small`, false to use `font_body`.
  - **Returns:** `Struct.EchoChamberTextBox`
- `SetPadding(_x, [_y])`: Set inner padding for the text box.
  - **Arguments:**
    - `_x` `Real` Horizontal padding in pixels.
    - `_y` `Real` Optional vertical padding (defaults to `_x`).
  - **Returns:** `Struct.EchoChamberTextBox`
- `SetFillWidth(_flag)`: Set whether this box fills the available row width.
  - **Arguments:**
    - `_flag` `Bool` Fill width flag.
  - **Returns:** `Struct.EchoChamberTextBox`

---

### `EchoChamberButton(_id)`
Clickable button.

**Arguments**
- `_id` `Any`

**Returns**: `Struct.EchoChamberButton`

**Public methods**
- `OnClick(_fn)`: Set a callback to run when the button is activated.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function()`).
  - **Returns:** `Struct.EchoChamberButton`
  - **Additional details:**
    - Triggered by mouse click or Enter while the button is focused.
- `BindLabel(_source, [_key_or_fn])`: Bind the button label to a struct field or getter function.
  - **Arguments:**
    - `_source` `Struct,Function` Struct to read from, or a getter function (signature: `function() -> Any`).
    - `_key_or_fn` `String` Optional struct field key when `_source` is a struct.
  - **Returns:** `Struct.EchoChamberButton`
  - **Additional details:**
    - If `_source` is callable, it becomes the getter, `_key_or_fn` is ignored, and any struct binding is cleared.
    - If `_source` is a struct, `_key_or_fn` is the field key and any function binding is cleared.
    - If the getter returns `undefined`, the button keeps its previous label.

---

### `EchoChamberSlider(_id)`
Horizontal slider control.

**Arguments**
- `_id` `Any`

**Returns**: `Struct.EchoChamberSlider`

**Public methods**
- `SetRange(_min, _max)`: Set the slider value range.
  - **Arguments:**
    - `_min` `Real` Minimum value.
    - `_max` `Real` Maximum value.
  - **Returns:** `Struct.EchoChamberSlider`
- `SetStep(_step)`: Set snap step size (0 for no snapping).
  - **Arguments:**
    - `_step` `Real` Step size (0 disables snapping).
  - **Returns:** `Struct.EchoChamberSlider`
- `BindValue(_source, [_key_or_fn])`: Bind the slider value to a struct field or getter/setter functions.
  - **Arguments:**
    - `_source` `Struct,Function` Struct to bind, or a getter function (signature: `function() -> Real`).
    - `_key_or_fn` `String,Function` Optional struct field key, or a setter function (signature: `function(_value)`).
  - **Returns:** `Struct.EchoChamberSlider`
  - **Additional details:**
    - If `_source` is callable, it becomes the getter and `_key_or_fn` is used as the optional setter (if callable); struct binding is cleared.
    - If `_source` is a struct, `_key_or_fn` is treated as the field key and getter/setter functions are cleared.
    - If no setter is provided, the slider still changes visually and `OnChange` still fires.
- `OnChange(_fn)`: Set a callback that runs when the value changes.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function(_value)`).
  - **Returns:** `Struct.EchoChamberSlider`
  - **Additional details:**
    - Fires when the slider changes via user input.

---

### `EchoChamberToggle(_id)`
Checkbox-style toggle.

**Arguments**
- `_id` `Any`

**Returns**: `Struct.EchoChamberToggle`

**Public methods**
- `BindBool(_source, [_key_or_fn])`: Bind the toggle value to a struct field or getter/setter functions.
  - **Arguments:**
    - `_source` `Struct,Function` Struct to bind, or a getter function (signature: `function() -> Bool`).
    - `_key_or_fn` `String,Function` Optional struct field key, or a setter function (signature: `function(_value)`).
  - **Returns:** `Struct.EchoChamberToggle`
  - **Additional details:**
    - If `_source` is callable, it becomes the getter and `_key_or_fn` is used as the optional setter (if callable); struct binding is cleared.
    - If `_source` is a struct, `_key_or_fn` is treated as the field key and getter/setter functions are cleared.
    - If no setter is provided, the toggle still updates visually and `OnChange` still fires.
- `BindValue(_source, [_key_or_fn])`: Bind the toggle value (alias of BindBool).
  - **Arguments:**
    - `_source` `Struct,Function` Struct to bind, or a getter function (signature: `function() -> Bool`).
    - `_key_or_fn` `String,Function` Optional struct field key, or a setter function (signature: `function(_value)`).
  - **Returns:** `Struct.EchoChamberToggle`
  - **Additional details:**
    - Same behavior as `BindBool`.
- `OnChange(_fn)`: Set a callback that runs when the value changes.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function(_value)`).
  - **Returns:** `Struct.EchoChamberToggle`
  - **Additional details:**
    - Fires when the toggle changes via click or keyboard.

---

### `EchoChamberTextInput(_id)`
Single-line text input.

**Arguments**
- `_id` `Any`

**Returns**: `Struct.EchoChamberTextInput`

**Public methods**
- `BindText(_struct, _key)`: Bind the text input to a struct field.
  - **Arguments:**
    - `_struct` `Struct` Struct holding the field to update.
    - `_key` `String` Field key to read/write.
  - **Returns:** `Struct.EchoChamberTextInput`
  - **Additional details:**
    - If `_struct` is not a struct, the binding is not changed.
- `SetPlaceholder(_text)`: Set placeholder text shown when empty.
  - **Arguments:**
    - `_text` `Any` Placeholder text (converted to string).
  - **Returns:** `Struct.EchoChamberTextInput`
- `OnChange(_fn)`: Set a callback that runs when text is committed.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function(_text)`).
  - **Returns:** `Struct.EchoChamberTextInput`
  - **Additional details:**
    - Fired when the input is committed (blur or Enter).
- `SetReadOnly(_flag)`: Toggle read-only mode.
  - **Arguments:**
    - `_flag` `Bool` Read-only flag.
  - **Returns:** `Struct.EchoChamberTextInput`
- `SetMaxLength(_len)`: Set the maximum number of characters (0 for unlimited).
  - **Arguments:**
    - `_len` `Real` Maximum length (0 disables the limit).
  - **Returns:** `Struct.EchoChamberTextInput`
- `SetAllowedChars(_chars)`: Restrict input to a specific set of characters.
  - **Arguments:**
    - `_chars` `String` Allowed characters (empty string allows all).
  - **Returns:** `Struct.EchoChamberTextInput`
- `SetDeniedChars(_chars)`: Reject characters in the given set.
  - **Arguments:**
    - `_chars` `String` Denied characters.
  - **Returns:** `Struct.EchoChamberTextInput`
- `SetNumericOnly(_flag, [_allow_decimal], [_allow_negative])`: Restrict input to numeric characters.
  - **Arguments:**
    - `_flag` `Bool` Enable numeric-only mode.
    - `_allow_decimal` `Bool` Optional, allow decimal points (defaults to false).
    - `_allow_negative` `Bool` Optional, allow a leading negative sign (defaults to false).
  - **Returns:** `Struct.EchoChamberTextInput`
- `SetSelectAllOnFocus(_flag)`: Select all text when the input gains focus.
  - **Arguments:**
    - `_flag` `Bool` Select-all flag.
  - **Returns:** `Struct.EchoChamberTextInput`
- `SetFilter(_fn)`: Provide a filter function for inserted text.
  - **Arguments:**
    - `_fn` `Function` Filter callback (signature: `function(_insert_text) -> String`).
  - **Returns:** `Struct.EchoChamberTextInput`
  - **Additional details:**
    - The filter runs before allow/deny/numeric constraints.
    - Return an empty string to reject the insert.
- `SetInvalid(_flag)`: Toggle invalid styling.
  - **Arguments:**
    - `_flag` `Bool` Invalid flag.
  - **Returns:** `Struct.EchoChamberTextInput`

---

### `EchoChamberSeparator(_id)`
Non-interactive separator line.

**Arguments**
- `_id` `Any`

**Returns**: `Struct.EchoChamberSeparator`

**Public methods**
- `SetOrientation(_ori)`: Set orientation ("horizontal" or "vertical").
  - **Arguments:**
    - `_ori` `String` Orientation string.
  - **Returns:** `Struct.EchoChamberSeparator`

---

### `EchoChamberListView(_id)`
Virtualized list view control for very large row counts. Draws and hit-tests only visible rows.

**Arguments**
- `_id` `Any`

**Returns**: `Struct.EchoChamberListView`

**Public methods**
- `SetRowHeight(_h)`: Set row height in pixels.
  - **Arguments:**
    - `_h` `Real` Row height in pixels.
  - **Returns:** `Struct.EchoChamberListView`
- `SetVisibleRows(_rows)`: Set a visible row count (auto height from row height).
  - **Arguments:**
    - `_rows` `Real` Visible row count (<= 0 clears).
  - **Returns:** `Struct.EchoChamberListView`
  - **Additional details:**
    - Setting this disables auto-height-from-count.
- `SetAutoHeightFromCount(_max_rows)`: Auto-size to row count up to a maximum.
  - **Arguments:**
    - `_max_rows` `Real` Maximum row count to use for auto height (0 disables).
  - **Returns:** `Struct.EchoChamberListView`
  - **Additional details:**
    - Setting this clears any explicit visible row count.
- `SetAutoWidthFromContent(_max_rows)`: Auto-size width from row content (sample limit).
  - **Arguments:**
    - `_max_rows` `Real` Maximum rows to sample (0 disables).
  - **Returns:** `Struct.EchoChamberListView`
  - **Additional details:**
    - Requires `SetRowMeasure` to be provided.
- `SetFillWidth(_flag)`: Toggle fill width for row layouts.
  - **Arguments:**
    - `_flag` `Bool` Fill width flag.
  - **Returns:** `Struct.EchoChamberListView`
- `SetPreferredHeight(_h)`: Set the preferred height for FitToContent.
  - **Arguments:**
    - `_h` `Real` Preferred height in pixels.
  - **Returns:** `Struct.EchoChamberListView`
- `SetPreferredWidth(_w)`: Set the preferred width for FitToContent.
  - **Arguments:**
    - `_w` `Real` Preferred width in pixels.
  - **Returns:** `Struct.EchoChamberListView`
- `SetCountGetter(_fn)`: Set a function that returns the row count.
  - **Arguments:**
    - `_fn` `Function` Row count callback (signature: `function() -> Real`).
  - **Returns:** `Struct.EchoChamberListView`
  - **Additional details:**
    - Called whenever the list view needs to know its row count.
- `SetRowDrawer(_fn)`: Set a function that draws a row.
  - **Arguments:**
    - `_fn` `Function` Row draw callback (signature: `function(_index, _rect, _is_selected, _is_hover)`).
  - **Returns:** `Struct.EchoChamberListView`
  - **Additional details:**
    - `_rect` is `{x1,y1,x2,y2}` in GUI space and already excludes padding/scrollbar.
    - Background is already drawn; this function should only draw row content.
- `SetRowMeasure(_fn)`: Set a function that returns row text/width for auto width.
  - **Arguments:**
    - `_fn` `Function` Measure callback (signature: `function(_index, _root, _panel) -> String,Real`).
  - **Returns:** `Struct.EchoChamberListView`
  - **Additional details:**
    - Returning a string uses the theme body font to measure width.
    - Returning a real value treats it as a pixel width.
    - Only used when `SetAutoWidthFromContent` is enabled.
- `SetOnSelect(_fn)`: Set a callback that runs when selection changes.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function(_index)`).
  - **Returns:** `Struct.EchoChamberListView`
  - **Additional details:**
    - Fired when the selected index changes via mouse or keyboard.
- `SetOnActivate(_fn)`: Set a callback that runs when a row is activated.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function(_index)`).
  - **Returns:** `Struct.EchoChamberListView`
  - **Additional details:**
    - Triggered by Enter while a row is selected.
- `SetOnDoubleClick(_fn)`: Set a callback for double click on a row.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function(_index)`).
  - **Returns:** `Struct.EchoChamberListView`
  - **Additional details:**
    - Triggered by a fast double-click on the same row.
- `SetOnRightClick(_fn)`: Set a callback for right click on a row.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function(_index, _x, _y)`).
  - **Returns:** `Struct.EchoChamberListView`
  - **Additional details:**
    - `_x`/`_y` are GUI-space mouse coordinates.
    - `_index` is -1 when right-clicking empty space.
- `SetAutoScroll(_enabled)`: Enable or disable auto scroll to bottom.
  - **Arguments:**
    - `_enabled` `Bool` Auto-scroll flag.
  - **Returns:** `Struct.EchoChamberListView`
  - **Additional details:**
    - Enabling does not force a snap unless the list is already near bottom.
- `JumpToBottom()`: Jump scroll to the bottom.
  - **Arguments:** None.
  - **Returns:** `Struct.EchoChamberListView`
  - **Additional details:**
    - Also resumes auto-follow if it was paused.
- `IsNearBottom()`: Return true if the scroll is near the bottom.
  - **Arguments:** None.
  - **Returns:** `Bool`
  - **Additional details:**
    - Based on the last draw frame.
- `IsAutoFollowPaused()`: Return true if auto follow is paused.
  - **Arguments:** None.
  - **Returns:** `Bool`
- `GetSelectedIndex()`: Get the selected index.
  - **Arguments:** None.
  - **Returns:** `Real`
- `SetSelectedIndex(_index)`: Set the selected index.
  - **Arguments:**
    - `_index` `Real` Selected row index (use -1 to clear selection).
  - **Returns:** `Struct.EchoChamberListView`

---

### `EchoChamberDropdownBase(_id)`
Base dropdown control. Variants override selection and row behavior.

**Arguments**
- `_id` `Any`

**Returns**: `Struct.EchoChamberDropdownBase`

**Public methods**
- `GetSelectedIndex()`: Get the selected index.
  - **Arguments:** None.
  - **Returns:** `Real`
- `SetSelectedIndex(_idx)`: Set the selected index.
  - **Arguments:**
    - `_idx` `Real` Selected index (clamped to available options).
  - **Returns:** N/A
- `DrawOverlayRow(_root, _row_index, _row_rect, _hover, _selected)`: Draw an overlay row (override to customize).
  - **Arguments:**
    - `_root` `Struct.EchoChamberRoot` Root for theme access and metrics.
    - `_row_index` `Real` Row index being drawn.
    - `_row_rect` `Struct` `{x1,y1,x2,y2}` row rect in GUI space.
    - `_hover` `Bool` True if the row is hovered.
    - `_selected` `Bool` True if the row is selected.
  - **Returns:** N/A
- `OnOverlayRowClick(_root, _row_index, _rect, _mx, _my)`: Handle overlay row click (override to customize).
  - **Arguments:**
    - `_root` `Struct.EchoChamberRoot` Root for focus/overlay management.
    - `_row_index` `Real` Row index that was clicked.
    - `_rect` `Struct` `{x1,y1,x2,y2}` row rect in GUI space.
    - `_mx` `Real` Mouse X (GUI space).
    - `_my` `Real` Mouse Y (GUI space).
  - **Returns:** N/A
- `SetOptions(_array)`: Set the dropdown options array.
  - **Arguments:**
    - `_array` `Array<String>` Option labels.
  - **Returns:** `Struct.EchoChamberDropdownBase`
  - **Additional details:**
    - The array is stored directly; pass a new array to replace options.
- `SetUnfoldDirection(_dir)`: Set the overlay unfold direction ("up" or "down").
  - **Arguments:**
    - `_dir` `String` Direction string.
  - **Returns:** `Struct.EchoChamberDropdownBase`
- `SetUseSelectedLabelWhenClosed(_flag)`: Use the selected label when closed.
  - **Arguments:**
    - `_flag` `Bool` True to show the selected option label in the base control.
  - **Returns:** `Struct.EchoChamberDropdownBase`
- `SetOverlayMaxHeight(_height)`: Set the max overlay height.
  - **Arguments:**
    - `_height` `Real` Max height in pixels (0 disables the cap).
  - **Returns:** `Struct.EchoChamberDropdownBase`

---

### `EchoChamberDropdownSelect(_id)`
Dropdown variant that binds a selected index to a struct field.

**Arguments**
- `_id` `Any`

**Returns**: `Struct.EchoChamberDropdownSelect`

**Public methods**
- `BindIndex(_struct, _key)`: Bind the selected index to a struct field.
  - **Arguments:**
    - `_struct` `Struct` Struct holding the selected index field.
    - `_key` `String` Field key to read/write.
  - **Returns:** `Struct.EchoChamberDropdownSelect`
- `OnChange(_fn)`: Set a callback that runs when the selected index changes.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function(_index, _value)`).
  - **Returns:** `Struct.EchoChamberDropdownSelect`
  - **Additional details:**
    - Only fires when the selected index actually changes.
- `GetSelectedIndex()`: Get the selected index.
  - **Arguments:** None.
  - **Returns:** `Real`
- `SetSelectedIndex(_idx)`: Set the selected index.
  - **Arguments:**
    - `_idx` `Real` Selected index (clamped to available options).
  - **Returns:** N/A
  - **Additional details:**
    - Updates the bound struct field when one is configured.
- `OnOverlayRowClick(_root, _row_index, _rect, _mx, _my)`: Handle overlay row click.
  - **Arguments:**
    - `_root` `Struct.EchoChamberRoot` Root for overlay management.
    - `_row_index` `Real` Row index that was clicked.
    - `_rect` `Struct` `{x1,y1,x2,y2}` row rect in GUI space.
    - `_mx` `Real` Mouse X (GUI space).
    - `_my` `Real` Mouse Y (GUI space).
  - **Returns:** N/A

---

### `EchoChamberDropdownToggleMenu(_id)`
Dropdown variant that shows a checklist menu that stays open.

**Arguments**
- `_id` `Any`

**Returns**: `Struct.EchoChamberDropdownToggleMenu`

**Public methods**
- `SetItems(_items)`: Set the item list for the menu.
  - **Arguments:**
    - `_items` `Array<Struct>` Array of item structs (`{ label, bind_struct, bind_key }`).
  - **Returns:** `Struct.EchoChamberDropdownToggleMenu`
  - **Additional details:**
    - Each item reads/writes `bind_struct[bind_key]` as a Bool toggle.
- `OnAnyChange(_fn)`: Set a callback that runs when any item changes.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function()`).
  - **Returns:** `Struct.EchoChamberDropdownToggleMenu`
- `GetSelectedIndex()`: Get the selected index.
  - **Arguments:** None.
  - **Returns:** `Real`
  - **Additional details:**
    - Toggle menus do not track a single selection; this is a placeholder.
- `SetSelectedIndex(_idx)`: Set the selected index.
  - **Arguments:**
    - `_idx` `Real` Ignored for toggle menus.
  - **Returns:** N/A
- `DrawOverlayRow(_root, _row_index, _rect, _hover, _is_selected)`: Draw an overlay row.
  - **Arguments:**
    - `_root` `Struct.EchoChamberRoot` Root for theme access and metrics.
    - `_row_index` `Real` Row index being drawn.
    - `_rect` `Struct` `{x1,y1,x2,y2}` row rect in GUI space.
    - `_hover` `Bool` True if the row is hovered.
    - `_is_selected` `Bool` True if the row is selected (unused for toggle menus).
  - **Returns:** N/A
- `OnOverlayRowClick(_root, _row_index, _rect, _mx, _my)`: Handle overlay row click.
  - **Arguments:**
    - `_root` `Struct.EchoChamberRoot` Root for overlay management.
    - `_row_index` `Real` Row index that was clicked.
    - `_rect` `Struct` `{x1,y1,x2,y2}` row rect in GUI space.
    - `_mx` `Real` Mouse X (GUI space).
    - `_my` `Real` Mouse Y (GUI space).
  - **Returns:** N/A

---

### `EchoChamberMachinePicker(_id)`
Dropdown-style machine picker with search field at top.

**Arguments**
- `_id` `Any`

**Returns**: `Struct.EchoChamberMachinePicker`

**Public methods**
- `SetListBuilder(_fn)`: Set a function that provides the list of machines based on the current filter text.
  - **Arguments:**
    - `_fn` `Function` List builder (signature: `function(_filter_string) -> Struct` with `labels`, `index_map`, and `selected_index`).
  - **Returns:** `Struct.EchoChamberMachinePicker`
  - **Additional details:**
    - `labels` is the filtered display list.
    - `index_map` maps filtered indices to real indices in your source list.
    - `selected_index` is the initially selected filtered index.
- `OnSelect(_fn)`: Set a callback that runs when the user selects a machine.
  - **Arguments:**
    - `_fn` `Function` Callback (signature: `function(_real_index)`).
  - **Returns:** `Struct.EchoChamberMachinePicker`
  - **Additional details:**
    - `_real_index` comes from `index_map` for the selected filtered row.
- `SetUnfoldDirection(_dir)`: Set the overlay unfold direction ("up" or "down").
  - **Arguments:**
    - `_dir` `String` Direction string.
  - **Returns:** `Struct.EchoChamberMachinePicker`

---

### `EchoChamberOpenConsole(_ui_root)`
Open or create the built-in Echo Console window (log history viewer + filters).

**Arguments**
- `_ui_root` `Struct.EchoChamberRoot`

**Returns**: `Struct.EchoChamberWindow`

---

## Echo Chamber Themes

Themes are just structs that hold fonts, sprites, colors, spacing, and sizing rules. They're essentially a big bag of settings that Echo Chamber reads when drawing.

### Default theme structure
The base theme constructor is: `EchoChamberTheme()`.

It outputs a struct with fields in roughly these buckets (names below are from the actual theme struct):

#### CORE
- `statement`
- `gap`

#### BUTTON
- `button_styles`

#### COL
- `col_window_bg`
- `col_panel_bg`
- `col_text`
- `col_text_dim`
- `col_accent`
- `col_accent_dim`
- `col_muted`
- `col_muted_strong`
- `col_error`
- `col_hover_row`
- `col_hover_row_alt`
- `col_menu_bg`
- `col_menu_hover`
- `col_label_hover_bg`
- `col_checkbox_off`
- `col_checkbox_on`

#### DEFAULT
- `default_control_width`
- `default_control_max_width`
- `default_padding`
- `default_row_height`

#### DROPDOWN
- `dropdown_styles`

#### FONT
- `font_header`
- `font_body`
- `font_small`

#### HEADER
- `header_styles`

#### LABEL
- `label_styles` (style keys include `font`, `text`, `text_alpha`, `text_disabled`, `text_disabled_alpha`)

#### LIST
- `list_row_styles` (style keys include `bg_*`, `text_*`, and `*_alpha` variants)

#### SEPARATOR
- `separator_styles` (style keys include `line`, `line_alpha`, `line_disabled`, `line_disabled_alpha`)

#### MIN
- `min_hit_h`

#### PAD
- `pad_x`
- `pad_y`

#### PANEL
- `panel_styles` (style keys include `bg`, `border`, `bg_alpha`, `border_alpha`)
- `panel_padding`
- `panel_gap`
- `panel_row_height`
- `panel_collapsed_size`
- `panel_collapse_handle_size`

#### POPUP
- `popup_styles`

#### ROW
- `row_header_h`
- `row_toolbar_h`
- `row_small_h`

#### SCROLLBAR
- `scrollbar_styles`
- `scrollbar_w`

#### TEXTINPUT
- `textinput_styles`

#### TOGGLE
- `toggle_styles`

#### TOOLTIP
- `tooltip_styles`
- `tooltip_delay_ms`
- `tooltip_padding`

#### UI
- `ui_scale`

#### WINDOW
- `window_styles`
- `window_padding`
- `window_titlebar_h`
- `window_resize_grip_size`
- `window_minimized_h`
- `window_button_gap`
- `window_button_size`
- `window_button_close_label`
- `window_button_minimize_label`
- `window_button_restore_label`
- `window_button_pin_label`
- `window_button_unpin_label`

### Style map conventions
Most control styles are stored in a map of named styles (including `_default`). A control reads its `style_id` key and falls back to `_default`.

**Common interaction keys** (buttons, toggles, dropdowns, text inputs):
- `bg`, `bg_alpha`
- `border`, `border_alpha`
- `text`, `text_alpha`
- `bg_hover`, `bg_hover_alpha`, `border_hover`, `border_hover_alpha`, `text_hover`, `text_hover_alpha`
- `bg_pressed`, `bg_pressed_alpha`, `border_pressed`, `border_pressed_alpha`, `text_pressed`, `text_pressed_alpha`
- `bg_disabled`, `bg_disabled_alpha`, `border_disabled`, `border_disabled_alpha`, `text_disabled`, `text_disabled_alpha`

**Control-specific keys**
- `label_styles`: `font`, `text`, `text_alpha`, `text_disabled`, `text_disabled_alpha`.
- `separator_styles`: `line`, `line_alpha`, `line_disabled`, `line_disabled_alpha`.
- `list_row_styles`: `bg_normal`, `bg_hover`, `bg_selected`, `bg_pressed`, `bg_disabled`, `text_normal`, `text_hover`, `text_selected`, `text_pressed`, `text_disabled`, and matching `*_alpha` keys.
- `toggle_styles`: `box_on`, `box_off`, `box_border`, plus `box_*_hover`, `box_*_pressed`, `box_*_disabled`, and matching `*_alpha` keys.
- `slider_styles`: `track_bg`, `track_fill`, `knob`, plus hover/pressed/disabled variants and matching `*_alpha` keys.
- `dropdown_styles`: `bg_open`, `border_open`, `text_open` with `*_alpha` keys, plus overlay keys:
  - `overlay_bg`, `overlay_bg_alpha`, `overlay_border`, `overlay_border_alpha`
  - `overlay_row_*` and `overlay_text_*` keys, each with `*_alpha`
  - `overlay_search_bg`, `overlay_search_hover_bg`, `overlay_search_border`, `overlay_search_text`, `overlay_search_placeholder`, each with `*_alpha`
- `textinput_styles`: `bg_active`, `border_active`, `text_active`, `bg_readonly`, `border_readonly`, `text_readonly`, `bg_invalid`, `border_invalid`, `text_invalid` with `*_alpha` keys, plus:
  - `selection_bg`, `selection_text`, `selection_bg_inactive`, `selection_text_inactive` with `*_alpha`
  - `caret_color`, `caret_alpha`, `caret_char`, `caret_blink_ms`, `caret_width`, `caret_height`, `caret_inset_x`, `caret_inset_y`
  - `placeholder`, `placeholder_alpha`, `align`
- `scrollbar_styles`: `track_bg`, `track_bg_hover`, `track_border`, `handle_bg`, `handle_bg_hover`, `handle_bg_pressed`, `handle_border`, each with `*_alpha`.

---

### Theme constructors
### `EchoChamberTheme()`
Creates the shared default UI theme container for Echo Chamber visuals.

**Returns**: `Struct.EchoChamberTheme`

> If you wish to create your own themes, the simplest way is to create a constructor that inherits from the EchoChamberTheme and then just override the specific values you wish to change.
{: .note}

**Public methods**
- `RefreshMetrics()`: Recompute row heights based on current fonts and padding.
  - **Arguments:** None.
  - **Returns:** N/A
  - **Additional details:**
    - Updates derived layout metrics such as row heights, padding, and window sizing.

### Pre-built Custom Themes

### `EchoChamberThemeMidnightNeon()`
Dark midnight blues with neon purple accent.

**Returns**: `Struct.EchoChamberThemeMidnightNeon`

### `EchoChamberThemeAmberForest()`
Forest greens with warm amber highlights.

**Returns**: `Struct.EchoChamberThemeAmberForest`

### `EchoChamberThemeSakuraPunch()`
Inky plum with candy pink accents.

**Returns**: `Struct.EchoChamberThemeSakuraPunch`

### `EchoChamberThemeArcadeWave()`
Retro arcade navy with bright cyan accents.

**Returns**: `Struct.EchoChamberThemeArcadeWave`

### `EchoChamberThemeCircuitCandy()`
Playful teal and orange on a soft dark background.

**Returns**: `Struct.EchoChamberThemeCircuitCandy`

### `EchoChamberThemeToxicTerminal()`
Acid terminal green with rogue magenta highlights.

**Returns**: `Struct.EchoChamberThemeToxicTerminal`

### `EchoChamberThemeSunsetGlitch()`
Sunset oranges colliding with cyan and grape.

**Returns**: `Struct.EchoChamberThemeSunsetGlitch`

### `EchoChamberThemeBubblegumTerminal()`
Bubblegum pink UI with teal statement nodes.

**Returns**: `Struct.EchoChamberThemeBubblegumTerminal`

### `EchoChamberThemeMangoMint()`
Warm mango chrome with mint green graph.

**Returns**: `Struct.EchoChamberThemeMangoMint`

---

### Functions
### `EchoChamberThemeTryGetFont(_font_name)`
Resolve a font asset by name. If missing, returns the current draw font.

**Arguments**
- `_font_name` `String, Asset.GMFont`

**Returns**: `Asset.GMFont`

### `EchoChamberThemeTryGetSprite(_sprite_name)`
Resolve a sprite asset by name. If missing, returns -1.

**Arguments**
- `_sprite_name` `String, Asset.GMSprite`

**Returns**: `Asset.GMSprite,Real`
