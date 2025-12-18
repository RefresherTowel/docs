---
layout: default
title: Reference
parent: Echo
nav_order: 20
---

# Reference

This is the full public API for Echo + Echo Chamber.

Private rule: anything starting with `__` and/or marked with `/// @ignore` is considered internal and is intentionally not documented here.

## Echo

Echo is the logger: it decides what to print, what to store, and how to filter it.

### Enums
#### `eEchoDebugLevel`
- `NONE`
- `SEVERE_ONLY`
- `COMPREHENSIVE`
- `COMPLETE`

#### `eEchoDebugUrgency`
- `INFO`
- `WARNING`
- `SEVERE`

### Functions
### `EchoDebug(_message, _urgency = eEchoDebugUrgency.WARNING, _tag = "")`
Send a message to the debug logger with a specific urgency level. Returns true if the message meets current debug level critera, false if not.
**Parameters**
- `_message` `String`: The message to send to the debug logger
- `[_urgency]` `Real`: The level of urgency of the debug message (pick an entry from the eEchoDebugUrgency enum)
- `[_tag]` `String,Array<String>`: Optional tag or tags to filter on (e.g., "UI", ["Physics","Jump"]). Empty or empty array allows all.
**Returns**: `Boolean`

### `EchoDebugInfo(_message, _tag = "")`
Logs a debug message with an INFO urgency level
**Parameters**
- `_message` `String`
- `[_tag]` `String,Array<String>`

### `EchoDebugWarn(_message, _tag = "")`
Logs a debug message with a WARNING urgency level
**Parameters**
- `_message` `String`
- `[_tag]` `String,Array<String>`

### `EchoDebugSevere(_message, _tag = "")`
Logs a debug message with a SEVERE urgency level (includes stack trace)
**Parameters**
- `_message` `String`
- `[_tag]` `String,Array<String>`

### `EchoDebugSetLevel(_level)`
Sets the debug logging level, which determines what urgency criteria messages must meet in order to be logged.
**Parameters**
- `_level` `Real`: The level of logging (pick an entry from the eEchoDebugLevel enum)
**Returns**: `Boolean`

### `EchoDebugGetLevel(_stringify = false)`
Returns the current debug logging level (will be equivalent to one of the entries from the eEchoDebugLevel enum).
**Parameters**
- `_stringify` `Boolean`: Whether to return the debug level as a string, or as the plain real value.
**Returns**: `Real,String,Bool` - False if debug is disabled.

### `EchoDebugDumpLog()`
Dumps the entire debug log history to a file (file naming convention is "echo_debug_dump-[current_date]-([time_since_game_started]).txt). Returns true if dump succeeded, false if not
**Returns**: `Boolean`

### `EchoDebugGetHistorySize()`
Returns the current maximum number of entries allowed in the debug log history
**Returns**: `Real,Bool` - False if debug is disabled.

### `EchoDebugSetHistorySize(_max)`
Sets the maximum number of entries allowed in the debug log history. Setting it to 0 means there is no limit.
**Parameters**
- `_max` `Real`
**Returns**: `Boolean`

### `EchoDebugClearHistory()`
Clears all entries from the debug log history
**Returns**: `Boolean` - False if debug is disabled, otherwise true after clearing.

### `EchoDebugGetHistory()`
Returns a new array filled with the entries from debug log history
**Returns**: `Array<String>,Boolean` - False if debug is disabled.

### `EchoDebugGetRevision()`
Returns the current log revision number. This increments whenever history changes.
**Returns**: `Real,Boolean` - False if debug is disabled.

### `EchoDebugGetStructuredHistory()`
Returns a new array of structured history entries for UI rendering.
**Returns**: `Array<Struct>,Boolean` - False if debug is disabled.

### `EchoDebugSetTags(_tags)`
Sets which tags are allowed to log. An empty array means "allow all".
**Parameters**
- `_tags` `Array<String>`
**Returns**: `Boolean`

### `EchoDebugClearTags()`
Clears any tag filter so all tags are allowed.
**Returns**: `Boolean`

### `EchoDebugGetTags()`
Gets the current allowed tags array (empty means "allow all").
**Returns**: `Array<String>,Boolean`

## Echo Chamber

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

### Constructors
### `EchoChamberRoot(_theme)`
Root container for debug UI panels and controls.
**Parameters**
- `_theme` `Struct.EchoChamberTheme`
**Returns**: `Struct.EchoChamberRoot`

**Public methods**
- `BeginFrame()`: Snapshot mouse and wheel for this frame.
- `AddPanel(_panel)`: Add a top-level panel to the root.
- `CreateWindow(_id)`: Create and register a floating debug window.
- `RegisterWindow(_window)`: Register an externally created window instance.
- `FindWindow(_id)`: Find a registered window by id.
- `BringWindowToFront(_window)`: Bring a window to the front of the z-order.
- `SetPersistenceFile(_filename)`: Set the INI filename used for saving and loading UI layout state.
- `SetPersistenceSection(_section)`: Set the INI section prefix used for saving and loading UI layout state.
- `SaveLayout()`: Save window layout, z-order, and panel state to an INI file.
- `LoadLayout()`: Load window layout, z-order, and panel state from an INI file. Windows and panels must already be created/registered before calling this.
- `SetMouseCapture(_window)`: Capture the mouse for a window interaction (drag/resize).
- `ClearMouseCapture(_window)`: Release mouse capture if owned by the given window.
- `RunDesktop()`: Run the managed desktop: capture input, process the active window, draw all windows, then draw overlays and tooltip.
- `ConsumeMouse()`: Consume mouse input for all remaining controls this frame.
- `ConsumeWheel()`: Consume mouse wheel for all remaining scroll regions.
- `DrawScrollArea(_scroll_state, _rect, _content_h, _draw_fn)`: Draw a scrollable clipped region and handle mouse wheel scrolling when hovered. Includes scrollbar thumb dragging and track page jumps.
- `PushClipRect(_x1, _y1, _x2, _y2)`: Push a clip rectangle. Any existing clip will be intersected with this one.
- `PopClipRect()`: Pop the most recently pushed clip rectangle.
- `HitTestRect(_x1, _y1, _x2, _y2)`: Simple hit test for a rect, respecting mouse_consumed and the current clip region.
- `RequestTooltip(_control_id, _text, _anchor_x, _anchor_y)`: Request a tooltip for a given control id.
- `SetActiveOverlayOwner(_control_id)`: Mark a control as owning a modal overlay (e.g. a dropdown).
- `ClearActiveOverlayOwner()`: Clear the active overlay (if any).
- `RequestCloseOverlay()`: Request the currently active overlay (if any) to close.
- `QueueOverlay(_owner_id, _draw_fn, _rect, _owner_window)`: Queue an overlay draw callback. Overlays are drawn after all windows.
- `OpenContextMenu(_items, _x, _y, _owner_window)`: Open a context menu overlay at a screen position.
- `CloseContextMenu()`: Close the active context menu overlay (if open).
- `IsContextMenuOpen()`: Returns true if the context menu overlay is open.
- `DrawOverlays()`: Draw all queued overlays once per frame.
- `LayoutPanels(_x1, _y1, _x2, _y2)`: Dock + collapse layout. Assigns rects to all top-level panels.
- `DrawTooltip()`: Draw simple tooltip for the current tooltip_control_id (if delay elapsed).
- `ShowToast(_text, _duration_ms)`: Show a short toast message (non-blocking).
- `CopyToClipboard(_text, _toast_text, _duration_ms)`: Copy text to clipboard and show a toast confirmation.
- `DrawPanelBackground(_panel)`: Convenience: draw a basic panel background.
- `DrawPanelCollapseHandle(_panel)`: Draw a collapse handle for a panel (if it supports collapsing).
- `SetTextInputSource(_fn)`: Set a function that returns the current active text input string. If not set, keyboard_string is used.
- `SetTextInputSeed(_fn)`: Set a function that seeds the active text input string when focusing. If not set, keyboard_string is used.
- `FocusTextInput(_id, _initial_text, _placeholder, _commit_fn)`: Focus a text input by id and seed its initial content. Optional _commit_fn is called with the final string on blur.
- `BlurTextInput(_id)`: Blur a focused text input by id. Returns the final string (after syncing from the text source).
- `IsActiveTextInput(_id)`: Returns true if the given id is the currently focused text input.
- `GetActiveText()`: Return the current active text string while a text input is focused.
- `GetTextBuffer()`: Return the last committed text buffer for the active text input.
- `FocusControl(_id, _rect)`: Give keyboard focus to a non-text control by id. This focus is separate from text input focus.
- `IsControlFocused(_id)`: Returns true if the given control id currently owns keyboard focus (and no text input is active).
- `BlurControlFocus(_id)`: Blur (clear) keyboard focus from a control by id.
- `RegisterFocusable(_id, _rect)`: Register a focusable control for Tab navigation.

### `EchoChamberWindow(_id)`
Floating debug window that owns a collection of docked panels.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberWindow`

**Public methods**
- `SetTitle(_title)`: Set the window title text.
- `SetWindowStyleKey(_key)`: Set the window style key (for theme.window_styles).
- `SetHeaderStyleKey(_key)`: Set the header style key (for theme.header_styles).
- `SetVisible(_flag)`: Show or hide this window.
- `SetShowChromeButtons(_show_close, _show_minimize, _show_pin)`: Configure which chrome buttons are shown in the window header.
- `OnClose(_fn)`: Set a callback that runs when the window is closed via the close button.
- `Close()`: Close the window (sets visible to false). If an on_close callback exists, it is called.
- `SetPinned(_flag)`: Set whether the window is pinned (disables dragging and resizing).
- `TogglePinned()`: Toggle pinned state.
- `SetMinimized(_flag)`: Set whether the window is minimized (collapses content; only the title bar remains).
- `ToggleMinimized()`: Toggle minimized state.
- `SetRect(_x1, _y1, _x2, _y2)`: Set the window rectangle in GUI-space. Size is clamped to min_width/min_height.
- `SetMinSize(_w, _h)`: Set minimum width and height for this window.
- `AddPanel(_panel)`: Add a top-level panel to this window.
- `ClearPanels()`: Remove all panels from this window.
- `FindPanel(_id)`: Find a panel in this window by id (searches nested container panels too).
- `ContainsPoint(_x, _y)`: Returns true if a point is inside this window's current rectangle (and the window is visible).
- `LayoutPanels(_root)`: Layout this window's panels into the current content rect.
- `ProcessWindowInteractions(_root)`: Handle mouse interactions for dragging/resizing and chrome button clicks.
- `Draw(_root)`: Draw the window chrome and all owned panels.

### `EchoChamberPanel(_id, _dock)`
Layout panel docked to an edge or fill.
**Parameters**
- `_id` `Any`
- `_dock` `eEchoChamberDock`
**Returns**: `Struct.EchoChamberPanel`

**Public methods**
- `AddControl(_control)`: Add a control to this panel.
- `AddChildPanel(_panel)`: Add a child panel (for panel container usage).
- `FindControl(_id)`: Find a direct or nested control within this panel by id.
- `SetSizeMode(_mode)`: Configure how this panel resolves its dock size.
- `SetStyleKey(_key)`: Set the panel style key (for theme.panel_styles).
- `SetMinSize(_value)`: Set minimum dock thickness when using fit-to-content.
- `SetMaxSize(_value)`: Set maximum dock thickness when using fit-to-content.
- `SetContentDrawer(_fn)`: Assign a custom content drawer for this panel.
- `GetThickness()`: Get panel thickness based on collapsed state.
- `ResolveThickness(_root, _avail_width, _avail_height)`: Resolve actual thickness for layout considering size mode.
- `Draw(_root)`: Draw this panel and its contents (controls or child panels).

### `EchoChamberScrollState(_id)`
Persistent scroll state for a scrollable region.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberScrollState`

**Public methods**
- `SetScrollY(_y)`: Set the scroll offset in pixels.
- `ScrollBy(_dy)`: Scroll by a delta in pixels (positive scrolls down).
- `Reset()`: Reset scroll to the top.

### `EchoChamberControlBase(_id)`
Base type for all debug UI controls.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberControlBase`

**Public methods**
- `GetRoot()`: Get the owning root for this control (if attached).
- `GetWindow()`: Get the owning window for this control (if attached).
- `GetPanel()`: Get the owning panel for this control (if attached).
- `SetPreferredWidth(_width)`: Set a preferred pixel width for this control when arranged in a row panel.
- `SetLabel(_text)`: Set the control's display label (used by controls that render a label).
- `SetTooltip(_text)`: Set the control tooltip (shown on hover where supported).
- `SetStyle(_style)`: Set the theme style key for this control (e.g. button/toggle/dropdown styles).
- `SetVisible(_flag)`: Show or hide this control.
- `SetEnabled(_flag)`: Enable or disable this control (disabled controls should not accept input).
- `ProcessAndDraw(_root, _panel, _rect)`: Override: process input and draw using the given rect.

### Functions
### `EchoChamberLabel(_id)`
Non-interactive text label.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberLabel`

### `EchoChamberButton(_id)`
Clickable button.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberButton`

### `EchoChamberSlider(_id)`
Horizontal slider control.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberSlider`

### `EchoChamberToggle(_id)`
Checkbox-style toggle.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberToggle`

### `EchoChamberTextInput(_id)`
Single-line text input.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberTextInput`

### `EchoChamberSeparator(_id)`
Non-interactive separator line.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberSeparator`

### `EchoChamberListView(_id)`
Virtualized list view control for very large row counts. Draws and hit-tests only visible rows.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberListView`

### `EchoChamberDropdownBase(_id)`
Base dropdown control. Variants override selection and row behavior.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberDropdownBase`

### `EchoChamberDropdownSelect(_id)`
Dropdown variant that binds a selected index to a struct field.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberDropdownSelect`

### `EchoChamberDropdownToggleMenu(_id)`
Dropdown variant that shows a checklist menu that stays open.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberDropdownToggleMenu`

### `EchoChamberMachinePicker(_id)`
Dropdown-style machine picker with search field at top.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberMachinePicker`

### `EchoChamberOpenConsole(_ui_root)`
Open or create the built-in Echo Console window (log history viewer + filters).
**Parameters**
- `_ui_root` `Struct.EchoChamberRoot`
**Returns**: `Struct.EchoChamberWindow`

## Echo Chamber Themes

Themes are just structs that hold fonts, sprites, colors, spacing, and sizing rules.
They are not magic. They are a big bag of settings that Echo Chamber reads when drawing.

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

#### DEFAULT
- `default_control_width`
- `default_padding`

#### DROPDOWN
- `dropdown_styles`

#### FONT
- `font_header`
- `font_body`
- `font_small`

#### HEADER
- `header_styles`

#### LIST
- `list_row_styles`

#### MIN
- `min_hit_h`

#### PAD
- `pad_x`
- `pad_y`

#### PANEL
- `panel_styles`
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

> Note: Statement stores its own themes inside its own debug UI constructors.
> You can do the same for your own tools (keep themes close to the UI they belong to).
{: .note}

### Theme constructors
### `EchoChamberTheme()`
Creates the shared default UI theme container for Echo Chamber visuals.
**Returns**: `Struct.EchoChamberTheme`

**Public methods**
- `RefreshMetrics()`: Recompute row heights based on current fonts and padding.

### Functions
### `EchoChamberThemeTryGetFont(_font_name)`
Resolve a font asset by name. If missing, returns the current draw font.
**Parameters**
- `_font_name` `String, Asset.GMFont`
**Returns**: `Asset.GMFont`

### `EchoChamberThemeTryGetSprite(_sprite_name)`
Resolve a sprite asset by name. If missing, returns -1.
**Parameters**
- `_sprite_name` `String, Asset.GMSprite`
**Returns**: `Asset.GMSprite,Real`

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
