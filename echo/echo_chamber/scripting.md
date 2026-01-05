---
layout: default
title: Echo Chamber Scripting Reference
nav_order: 2
parent: Echo Chamber
has_children: false
---

<!--
/// scripting.md - Changelog:
/// - 23-12-2025: Updated public API coverage for Echo Chamber scripting.
-->

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

### `EchoChamberInputBindingKey(_key, _check, _ctrl, _alt, _shift)`
Keyboard binding for an input action.
**Parameters**
- `_key` `Real` Keycode (vk_* or ord()).
- `_check` `eEchoChamberInputCheck` Optional, defaults to `PRESSED`.
- `_ctrl` `Bool` Optional, require Ctrl held.
- `_alt` `Bool` Optional, require Alt held.
- `_shift` `Bool` Optional, require Shift held.
**Returns**: `Struct.EchoChamberInputBinding`

### `EchoChamberInputBindingFunc(_fn)`
Function binding for an input action.
**Parameters**
- `_fn` `Function` Function that returns true when the action should fire.
**Returns**: `Struct.EchoChamberInputBinding`

### `EchoChamberInputBindingBlock()`
Binding that blocks an action from inheriting from its parent context.
**Returns**: `Struct.EchoChamberInputBinding`

### `EchoChamberInputContext(_id)`
Input context for Echo Chamber actions, supports inheritance.
**Parameters**
- `_id` `String`
**Returns**: `Struct.EchoChamberInputContext`

**Public methods**
- `SetParent(_parent_id)`: Set the parent context id for inheritance.
- `GetBinding(_action_id)`: Get the binding for an action id.
- `BindAction(_action_id, _binding)`: Bind an action to a binding. Requires an input binding struct built from `EchoChamberInputBinding`.
- `BindKey(_action_id, _key, _check, _ctrl, _alt, _shift)`: Bind an action to a keyboard key.
- `BindFunc(_action_id, _fn)`: Bind an action to a function.
- `BindBlock(_action_id)`: Bind an action to a blocker (prevents inheritance).
- `ClearAction(_action_id)`: Clear a local action binding so the parent can take over.

### `EchoChamberRoot(_theme)`
Root container for debug UI panels and controls.
**Parameters**
- `_theme` `Struct.EchoChamberTheme`
**Returns**: `Struct.EchoChamberRoot`

**Public methods**
- `ApplyTheme(_theme)`: Apply a new theme and reapply defaults across windows and panels.
- `BeginFrame()`: Snapshot mouse and wheel for this frame.
- `GetDefaultInputContextId()`: Return the default input context id.
- `BindCoreInputAction(_action_id, _binding)`: Bind a core Echo Chamber action in the default context. Requires an input binding struct built from `EchoChamberInputBinding`.
- `GetInputContext(_id)`: Get an input context by id.
- `CreateInputContext(_id, _parent_id)`: Create or return an input context by id. If parent is omitted, it inherits from the default context.
- `RemoveInputContext(_id)`: Remove an input context by id (only if unused by any window).
- `InputPressed(_action_id, _window)`: Check whether an action is pressed in the active input context.
- `InputDown(_action_id, _window)`: Check whether an action is held in the active input context.
- `InputReleased(_action_id, _window)`: Check whether an action is released in the active input context.
- `AddPanel(_panel)`: Add a top-level panel to the root. Requires a panel struct built from `EchoChamberPanel`.
- `CreateWindow(_id)`: Create and register a floating debug window.
- `RegisterWindow(_window)`: Register an externally created window instance. Requires a window struct built from `EchoChamberWindow`.
- `FindWindow(_id)`: Find a registered window by id.
- `FindControl(_id)`: Find a control by id across all windows.
- `DumpUI()`: Dump the current UI tree and focus/overlay state to the debug log.
- `RemoveWindow(_window_or_id)`: Remove a registered window and detach its panels/controls.
- `BringWindowToFront(_window_or_id)`: Bring a window (or id) to the front of the z-order.
- `BringWindowToFrontById(_id)`: Bring a window to the front by id.
- `SendWindowToBack(_window_or_id)`: Send a window (or id) to the back of the z-order.
- `BringWindowsBack()`: Bring all windows back into view so their title bars remain accessible.
- `SetWindowZIndex(_window_or_id, _index)`: Set a window z-order index (0 = back, last = front).
- `SetModalWindow(_window_or_id)`: Set the modal window (blocks input to other windows).
- `ClearModalWindow()`: Clear the current modal window.
- `GetModalWindow()`: Get the current modal window (if any).
- `SetPersistenceFile(_filename)`: Set the INI filename used for saving and loading UI layout state.
- `SetPersistenceSection(_section)`: Set the INI section prefix used for saving and loading UI layout state.
- `SaveLayout()`: Save window layout, z-order, and panel state to an INI file.
- `LoadLayout()`: Load window layout, z-order, and panel state from an INI file. Windows and panels must already be created/registered before calling this.
- `SetMouseCapture(_window)`: Capture the mouse for a window interaction (drag/resize). Requires a window struct built from `EchoChamberWindow`.
- `ClearMouseCapture(_window)`: Release mouse capture if owned by the given window. Requires a window struct built from `EchoChamberWindow`.
- `RunDesktop()`: Run the managed desktop: capture input, process the active window, draw all windows, then draw overlays and tooltip.
- `ConsumeMouse()`: Consume mouse input for all remaining controls this frame.
- `ConsumeWheel()`: Consume mouse wheel for all remaining scroll regions.
- `DrawScrollArea(_scroll_state, _rect, _content_h, _draw_fn)`: Draw a scrollable clipped region and handle mouse wheel scrolling when hovered. Requires a scroll state struct built from `EchoChamberScrollState`.
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
- `ShowToast(_text, _duration_ms)`: Show a short toast message (non-blocking). A toast is a brief popup in the bottom right hand corner of the game window.
- `CopyToClipboard(_text, _toast_text, _duration_ms)`: Copy text to clipboard and show a toast confirmation.
- `DrawToast()`: Draw active toast notifications for this frame.
- `DrawPanelBackground(_panel)`: Convenience: draw a basic panel background.
- `DrawPanelCollapseHandle(_panel)`: Draw a collapse handle for a panel (if it supports collapsing).
- `SetTextInputSource(_fn)`: Set a function that returns the current active text input string. If not set, keyboard_string is used.
- `SetTextInputSeed(_fn)`: Set a function that seeds the active text input string when focusing. If not set, keyboard_string is used.
- `FocusTextInput(_id, _initial_text, _placeholder, _commit_fn, _config)`: Focus a text input by id and seed its initial content. Optional _commit_fn is called with the final string on blur.
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
- `SetInputContext(_context_id, _parent_id)`: Set the input context id used for this window.
- `SwapInputContext(_context_id, _parent_id)`: Swap the input context and remove the old one if unused.
- `SetWindowStyleKey(_key)`: Set the window style key (for theme.window_styles).
- `SetHeaderStyleKey(_key)`: Set the header style key (for theme.header_styles).
- `SetChromeButtonStyleKey(_key)`: Set the chrome button style key (for theme.button_styles).
- `ApplyTheme(_theme)`: Apply a theme override to this window and its children.
- `ClearThemeOverride()`: Clear the window theme override (reverts to the root theme).
- `SetPadding(_value)`: Set the content padding for this window.
- `SetMargin(_x, [_y])`: Set the outer margin for this window in GUI-space.
- `SetTitlebarHeight(_value)`: Set the titlebar height for this window.
- `SetTitlebarAuto(_flag)`: Set whether the titlebar height is driven by the current theme.
- `SetResizeGripSize(_value)`: Set the resize grip size for this window.
- `SetVisible(_flag)`: Show or hide this window.
- `SetShowChromeButtons(_show_close, _show_minimize, _show_pin)`: Configure which chrome buttons are shown in the window header.
- `OnClose(_fn)`: Set a callback that runs when the window is closed via the close button.
- `OnMove(_fn)`: Set a callback that runs when the window moves.
- `OnResize(_fn)`: Set a callback that runs when the window resizes.
- `OnShow(_fn)`: Set a callback that runs when the window becomes visible.
- `OnHide(_fn)`: Set a callback that runs when the window is hidden.
- `OnFocus(_fn)`: Set a callback that runs when the window gains focus.
- `OnBlur(_fn)`: Set a callback that runs when the window loses focus.
- `OnMinimize(_fn)`: Set a callback that runs when the window is minimized.
- `OnRestore(_fn)`: Set a callback that runs when the window is restored.
- `Close()`: Close the window (sets visible to false). If an on_close callback exists, it is called.
- `SetPinned(_flag)`: Set whether the window is pinned (disables dragging and resizing).
- `TogglePinned()`: Toggle pinned state.
- `SetMinimized(_flag)`: Set whether the window is minimized (collapses content; only the title bar remains).
- `ToggleMinimized()`: Toggle minimized state.
- `SetRect(_x1, _y1, _x2, _y2)`: Set the window rectangle in GUI-space. Size is clamped to min_width/min_height.
- `SetPosition(_x, _y)`: Set the window position in GUI-space (size is unchanged).
- `GetWidth()`: Get the current window width (in GUI-space).
- `GetHeight()`: Get the current window height (in GUI-space).
- `SetMinSize(_w, _h)`: Set minimum width and height for this window.
- `SetMaxSize(_w, _h)`: Set maximum width and height for this window.
- `FitToContent([_root])`: Resize the window once to fit current content. Please note: If you have set a rectangle size (`SetRect()`) or a minimum / maximum window size (`SetMinSize()` / `SetMaxSize()`) those will override the autofit.
- `SetAutoFit(_flag)`: When enabled, future layout changes auto-fit the window (batches defer until EndLayoutBatch).
- `AddPanel(_panel)`: Add a top-level panel to this window. Requires a panel built from `EchoChamberPanel`.
- `RemovePanel(_panel_or_id)`: Remove a panel from this window (top-level or nested).
- `ClearPanels()`: Remove all panels from this window.
- `FindPanel(_id)`: Find a panel in this window by id (searches nested container panels too).
- `FindControl(_id)`: Find a control in this window by id (searches nested panels too).
- `MoveControlToPanel(_control_or_id, _panel_or_id, [_index])`: Move a control to another panel in this window.
- `ContainsPoint(_x, _y)`: Returns true if a point is inside this window's current rectangle (and the window is visible).
- `BeginLayoutBatch()`: Begin a layout batch (layout changes defer FitToContent until EndLayoutBatch).
- `EndLayoutBatch()`: End a layout batch and apply a single FitToContent if any layout changes occurred.
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
- `AddControl(_control)`: Add a control to this panel. Requires a control struct that inherits from `EchoChamberControlBase`.
- `InsertControl(_control, _index)`: Insert a control at a specific index (clamped).
- `MoveControl(_control_or_id, _index)`: Reorder a direct control to a specific index (clamped).
- `MoveControlToPanel(_control_or_id, _target_panel, [_index])`: Move a control to another panel.
- `SetControlOrder(_ids)`: Reorder direct controls using a list of ids (unlisted items keep order at the end).
- `RemoveControl(_control_or_id)`: Remove a control from this panel (direct or nested).
- `ClearControls()`: Remove all direct controls from this panel.
- `AddChildPanel(_panel)`: Add a child panel (for panel container usage). Requires a panel built from `EchoChamberPanel`.
- `RemoveChildPanel(_panel_or_id)`: Remove a child panel from this panel (direct or nested).
- `ClearChildPanels()`: Remove all child panels from this panel.
- `FindControl(_id)`: Find a direct or nested control within this panel by id.
- `SetSizeMode(_mode)`: Configure how this panel resolves its dock size.
- `SetSize(_value)`: Set dock thickness when using fixed sizing.
- `SetFlowMode(_flow_mode)`: Set how child controls flow within the panel.
- `SetScrollable(_flag)`: Enable or disable vertical scrolling for this panel.
- `SetScrollState(_state)`: Assign a scroll state for this panel (used when scrollable).
- `SetPadding(_value)`: Set panel content padding.
- `SetMargin(_x, [_y])`: Set panel outer margin in GUI-space.
- `SetGap(_value)`: Set panel control gap spacing.
- `SetRowHeight(_value)`: Set panel row height for controls.
- `SetCollapsedSize(_value)`: Set collapsed dock thickness for this panel.
- `SetCollapseMode(_mode)`: Set the panel collapse mode.
- `SetCollapsed(_value)`: Set whether this panel is collapsed.
- `SetPanelStyleKey(_key)`: Set the panel style key (for theme.panel_styles).
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
- `SetPadding(_x, [_y])`: Set inner padding for this control.
- `SetMargin(_x, [_y])`: Set outer margin for this control.
- `SetLabel(_text)`: Set the control's display label (used by controls that render a label).
- `SetTooltip(_text)`: Set the control tooltip (shown on hover where supported).
- `SetControlStyleKey(_style)`: Set the theme style key for this control (e.g. button/toggle/dropdown styles).
- `SetVisible(_flag)`: Show or hide this control.
- `SetEnabled(_flag)`: Enable or disable this control (disabled controls should not accept input).
- `ProcessAndDraw(_root, _panel, _rect)`: Override: process input and draw using the given rect.

### Functions
### `EchoChamberLabel(_id)`
Non-interactive text label.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberLabel`

**Public methods**
- `SetText(_text)`: Set the label text.
- `BindText(_source, [_key_or_fn])`: Bind the label text to a struct field or getter function.
- `SetAlign(_align)`: Set text alignment ("left", "center", "right").
- `UseSmallFont(_flag)`: Use the smaller theme font.

### `EchoChamberTextBox(_id)`
Non-interactive text box that wraps text to its width.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberTextBox`

**Public methods**
- `SetText(_text)`: Set the text content for this box.
- `BindText(_source, [_key_or_fn])`: Bind the text content to a struct field or getter function.
- `SetAlign(_align)`: Set text alignment ("left", "center", "right").
- `UseSmallFont(_flag)`: Use the smaller theme font.
- `SetPadding(_x, [_y])`: Set inner padding for the text box.
- `SetFillWidth(_flag)`: Set whether this box fills the available row width.

### `EchoChamberButton(_id)`
Clickable button.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberButton`

**Public methods**
- `OnClick(_fn)`: Set a callback to run when the button is activated.
- `BindLabel(_source, [_key_or_fn])`: Bind the button label to a struct field or getter function.

### `EchoChamberSlider(_id)`
Horizontal slider control.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberSlider`

**Public methods**
- `SetRange(_min, _max)`: Set the slider value range.
- `SetStep(_step)`: Set snap step size (0 for no snapping).
- `BindValue(_source, [_key_or_fn])`: Bind the slider value to a struct field or getter/setter functions.
- `OnChange(_fn)`: Set a callback that runs when the value changes.

### `EchoChamberToggle(_id)`
Checkbox-style toggle.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberToggle`

**Public methods**
- `BindBool(_source, [_key_or_fn])`: Bind the toggle value to a struct field or getter/setter functions.
- `BindValue(_source, [_key_or_fn])`: Bind the toggle value (alias of BindBool).
- `OnChange(_fn)`: Set a callback that runs when the value changes.

### `EchoChamberTextInput(_id)`
Single-line text input.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberTextInput`

**Public methods**
- `BindText(_struct, _key)`: Bind the text input to a struct field.
- `SetPlaceholder(_text)`: Set placeholder text shown when empty.
- `OnChange(_fn)`: Set a callback that runs when text is committed.
- `SetReadOnly(_flag)`: Toggle read-only mode.
- `SetMaxLength(_len)`: Set the maximum number of characters (0 for unlimited).
- `SetAllowedChars(_chars)`: Restrict input to a specific set of characters.
- `SetDeniedChars(_chars)`: Reject characters in the given set.
- `SetNumericOnly(_flag, [_allow_decimal], [_allow_negative])`: Restrict input to numeric characters.
- `SetSelectAllOnFocus(_flag)`: Select all text when the input gains focus.
- `SetFilter(_fn)`: Provide a filter function for inserted text.
- `SetInvalid(_flag)`: Toggle invalid styling.

### `EchoChamberSeparator(_id)`
Non-interactive separator line.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberSeparator`

**Public methods**
- `SetOrientation(_ori)`: Set orientation ("horizontal" or "vertical").

### `EchoChamberListView(_id)`
Virtualized list view control for very large row counts. Draws and hit-tests only visible rows.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberListView`

**Public methods**
- `SetRowHeight(_h)`: Set row height in pixels.
- `SetVisibleRows(_rows)`: Set a visible row count (auto height from row height).
- `SetAutoHeightFromCount(_max_rows)`: Auto-size to row count up to a maximum.
- `SetAutoWidthFromContent(_max_rows)`: Auto-size width from row content (sample limit).
- `SetFillWidth(_flag)`: Toggle fill width for row layouts.
- `SetPreferredHeight(_h)`: Set the preferred height for FitToContent.
- `SetPreferredWidth(_w)`: Set the preferred width for FitToContent.
- `SetCountGetter(_fn)`: Set a function that returns the row count.
- `SetRowDrawer(_fn)`: Set a function that draws a row.
- `SetRowMeasure(_fn)`: Set a function that returns row text/width for auto width.
- `SetOnSelect(_fn)`: Set a callback that runs when selection changes.
- `SetOnActivate(_fn)`: Set a callback that runs when a row is activated.
- `SetOnDoubleClick(_fn)`: Set a callback for double click on a row.
- `SetOnRightClick(_fn)`: Set a callback for right click on a row.
- `SetAutoScroll(_enabled)`: Enable or disable auto scroll to bottom.
- `JumpToBottom()`: Jump scroll to the bottom.
- `IsNearBottom()`: Return true if the scroll is near the bottom.
- `IsAutoFollowPaused()`: Return true if auto follow is paused.
- `GetSelectedIndex()`: Get the selected index.
- `SetSelectedIndex(_index)`: Set the selected index.

### `EchoChamberDropdownBase(_id)`
Base dropdown control. Variants override selection and row behavior.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberDropdownBase`

**Public methods**
- `GetSelectedIndex()`: Get the selected index.
- `SetSelectedIndex(_idx)`: Set the selected index.
- `DrawOverlayRow(_root, _row_index, _row_rect, _hover, _selected)`: Draw an overlay row (override to customize).
- `OnOverlayRowClick(_root, _row_index, _rect, _mx, _my)`: Handle overlay row click (override to customize).
- `SetOptions(_array)`: Set the dropdown options array.
- `SetUnfoldDirection(_dir)`: Set the overlay unfold direction ("up" or "down").
- `SetUseSelectedLabelWhenClosed(_flag)`: Use the selected label when closed.
- `SetOverlayMaxHeight(_height)`: Set the max overlay height.

### `EchoChamberDropdownSelect(_id)`
Dropdown variant that binds a selected index to a struct field.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberDropdownSelect`

**Public methods**
- `BindIndex(_struct, _key)`: Bind the selected index to a struct field.
- `OnChange(_fn)`: Set a callback that runs when the selected index changes.
- `GetSelectedIndex()`: Get the selected index.
- `SetSelectedIndex(_idx)`: Set the selected index.
- `OnOverlayRowClick(_root, _row_index, _rect, _mx, _my)`: Handle overlay row click.

### `EchoChamberDropdownToggleMenu(_id)`
Dropdown variant that shows a checklist menu that stays open.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberDropdownToggleMenu`

**Public methods**
- `SetItems(_items)`: Set the item list for the menu.
- `OnAnyChange(_fn)`: Set a callback that runs when any item changes.
- `GetSelectedIndex()`: Get the selected index.
- `SetSelectedIndex(_idx)`: Set the selected index.
- `DrawOverlayRow(_root, _row_index, _rect, _hover, _is_selected)`: Draw an overlay row.
- `OnOverlayRowClick(_root, _row_index, _rect, _mx, _my)`: Handle overlay row click.

### `EchoChamberMachinePicker(_id)`
Dropdown-style machine picker with search field at top.
**Parameters**
- `_id` `Any`
**Returns**: `Struct.EchoChamberMachinePicker`

**Public methods**
- `SetListBuilder(_fn)`: Set a function that provides the list of machines based on the current filter text.
- `OnSelect(_fn)`: Set a callback that runs when the user selects a machine.
- `SetUnfoldDirection(_dir)`: Set the overlay unfold direction ("up" or "down").

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

> Statement stores its own themes inside its own debug UI constructors.
> You can do the same for your own tools (keep themes close to the UI they belong to).
{: .note}

### Theme constructors
### `EchoChamberTheme()`
Creates the shared default UI theme container for Echo Chamber visuals.
**Returns**: `Struct.EchoChamberTheme`

> If you wish to create your own themes, the simplest way is to create a constructor that inherits from the EchoChamberTheme and then just override the specific values you wish to change.
{: .note}

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
