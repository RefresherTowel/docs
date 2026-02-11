---
layout: default
title: Scripting Reference
parent: Quill
nav_order: 4
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# API Reference

This page documents Quill's public API surface in this repository.

Callback notes:
- Bind explicit scope with `method(scope, fn)` when you need instance or struct scope inside callbacks.

---

## Constants

### Core box kind

- `QUILL_SINGLE`
- `QUILL_MULTI`

### Input modes

- `QUILL_TEXTMODE_TEXT`
- `QUILL_TEXTMODE_INT`
- `QUILL_TEXTMODE_FLOAT`
- `QUILL_TEXTMODE_IDENTIFIER`
- `QUILL_TEXTMODE_PATH`
- `QUILL_TEXTMODE_CODE`
- `QUILL_TEXTMODE_PASSWORD`

`QUILL_TEXTMODE_CODE` uses `theme.fonts.code` by default when `SetFont(...)` is not set to a valid font.

### Render/debug macros

- `QUILL_VB_ENABLE`
- `QUILL_VB_FREEZE_FRAMES`
- `QUILL_VB_DEBUG`

---

## Macros and globals

### `QUILL`

Macro alias for the global manager instance.

- Definition: `#macro QUILL global.__QUILL_CORE`
- Notes:
	- `QUILL` is an alias of `global.__QUILL_CORE`.
	- Use `QuillSetTheme(new QuillTheme())` for a global style baseline.

---

## Enums

### Label enums

#### `eQuillLabelPlacement`

- `eQuillLabelPlacement.Above`
- `eQuillLabelPlacement.Leading`

#### `eQuillLabelAlign`

- `eQuillLabelAlign.Start`
- `eQuillLabelAlign.Center`

#### `eQuillLabelOverflow`

- `eQuillLabelOverflow.Wrap`
- `eQuillLabelOverflow.Ellipsis`

### Text align enum

#### `eQuillTextAlign`

- `eQuillTextAlign.Left`
- `eQuillTextAlign.Center`
- `eQuillTextAlign.Right`

---

## Constructors and drawing

### `Quill(kind = QUILL_SINGLE, label = "", placeholder = "")`

Creates a new Quill textbox.

**Arguments**
- `kind` `Real` Core box kind (use `QUILL_SINGLE` or `QUILL_MULTI`).
- `label` `String` Optional label text.
- `placeholder` `String` Optional placeholder text.

**Returns**: `Struct.__Quill`

---

### `QuillSingle(label = "", placeholder = "")`

Convenience wrapper for `Quill(QUILL_SINGLE, ...)`.

**Arguments**
- `label` `String` Optional label text.
- `placeholder` `String` Optional placeholder text.

**Returns**: `Struct.__Quill`

---

### `QuillMulti(label = "", placeholder = "")`

Convenience wrapper for `Quill(QUILL_MULTI, ...)`.

**Arguments**
- `label` `String` Optional label text.
- `placeholder` `String` Optional placeholder text.

**Returns**: `Struct.__Quill`

---

### `QuillDrawOverlays()`

Draws all overlay UI used by Quill (for example, overlay editors).

**Arguments**: None.

**Returns**: `Void`

---

### `QuillContextMenuItem(label = "", on_click = undefined, key = "")`

Creates a context menu action item.

**Arguments**
- `label` `String` Menu label.
- `on_click` `Function|Undefined` Click callback.
- `key` `String` Optional semantic key.

**Returns**: `Struct.__QuillContextMenuItem`

---

### `QuillContextMenuSeparator(key = "")`

Creates a context menu separator item.

**Arguments**
- `key` `String` Optional semantic key.

**Returns**: `Struct.__QuillContextMenuSeparator`

---

## Core ensure

### `QuillEnsure()`

Ensures that the global manager exists.

**Arguments**: None.

**Returns**: `Bool`

**Additional details**
- `QuillEnsure()` returns `true` if the manager already existed, `false` if it was recreated.

---

## Global theme helpers (top-level functions)

### `QuillSetTheme(theme)`

Sets the global theme used by textboxes that do not have a per-box theme.

**Arguments**
- `theme` `Struct.QuillTheme` Theme to apply globally.

**Returns**: `Struct.__QuillCore`

---

### `QuillGetTheme()`

Gets the current global Quill theme.

**Arguments**: None.

**Returns**: `Struct.QuillTheme`

---

## Global context menu registry (top-level functions)

### `QuillContextMenuAddItem(item)`

Registers a context menu item globally.

**Arguments**
- `item` `Struct` A plain item struct, or an item created by `QuillContextMenuItem(...)` / `QuillContextMenuSeparator(...)`.

**Returns**: `Struct`

---

### `QuillContextMenuRemoveItem(key_or_uid)`

Removes a globally registered context menu item.

**Arguments**
- `key_or_uid` `String|Real` A semantic key string or an auto-assigned uid.

**Returns**: `Bool`

---

### `QuillContextMenuGetItem(key_or_uid)`

Fetches a globally registered context menu item.

**Arguments**
- `key_or_uid` `String|Real` A semantic key string or an auto-assigned uid.

**Returns**: `Struct`

---

### `QuillContextMenuClearItems()`

Clears all globally registered context menu items.

**Arguments**: None.

**Returns**: `Void`

---

## `QUILL` manager methods

> In most cases, you shouldn't need to use these. Opening and closing Context menus are handled automatically by Quill, and adding or remove global context menu items should really be done via the `QuillContextMenu*()` global functions. These are simply provided for advanced use cases. Global themes can be handled via `QuillSetTheme()` and `QuillGetTheme()`
{: .note}

- #### `QUILL.OpenContextMenu(items, x, y, owner_id)`
	- **Arguments:**
		- `items` `Array<Struct>` Menu item array.
		- `x` `Real` Screen x position.
		- `y` `Real` Screen y position.
		- `owner_id` `Any` Owner identifier used to associate the menu with a textbox/owner.
	- **Returns:** `Void`

- #### `QUILL.CloseContextMenu()`
	- **Arguments:** None.
	- **Returns:** `Void`

- #### `QUILL.IsContextMenuOpen()`
	- **Arguments:** None.
	- **Returns:** `Bool`

- #### `QUILL.ContextMenuAddItem(item)`
	- **Arguments:**
		- `item` `Struct` Item struct.
	- **Returns:** `Struct`

- #### `QUILL.ContextMenuRemoveItem(key_or_uid)`
	- **Arguments:**
		- `key_or_uid` `String|Real`
	- **Returns:** `Bool`

- #### `QUILL.ContextMenuGetItem(key_or_uid)`
	- **Arguments:**
		- `key_or_uid` `String|Real`
	- **Returns:** `Struct`

- #### `QUILL.ContextMenuClearItems()`
	- **Arguments:** None.
	- **Returns:** `Struct.__QuillCore`

- #### `QUILL.SetTheme(theme)`
	- **Arguments:**
		- `theme` `Struct.QuillTheme`
	- **Returns:** `Struct.__QuillCore`

- #### `QUILL.GetTheme()`
	- **Arguments:** None.
	- **Returns:** `Struct.QuillTheme`

---

## Quill Textbox methods (`__Quill` struct returned via one of the `Quill()`, `QuillSingle()` and `QuillMulti()` functions) 

All setters return `Struct.__Quill` unless noted, and so can be fluidly chained (i.e. `tb.SetLabel("Notes").SetPlaceholder("A place for your notes").OnChange(_update_notes_func);`).

### Value and selection

- #### `GetValue()`
	- **Arguments:** None.
	- **Returns:** `String`

- #### `SetValue(v)`
	- **Arguments:**
		- `v` `String`
	- **Returns:** `Void`

- #### `GetCaret()`
	- **Arguments:** None.
	- **Returns:** `Real`

- #### `SetCaret(index, extend = false)`
	- **Arguments:**
		- `index` `Real`
		- `extend` `Bool` Optional, defaults to `false`.
	- **Returns:** `Struct.__Quill`

- #### `GetSelection()`
	- **Arguments:** None.
	- **Returns:** `Struct` (`{ has_selection, start, _end }`)

- #### `SetSelection(start, end)`
	- **Arguments:**
		- `start` `Real`
		- `end` `Real`
	- **Returns:** `Struct.__Quill`

- #### `SelectAll()`
	- **Arguments:** None.
	- **Returns:** `Struct.__Quill`

### Size and drawing state

These return measured values before first draw, and continue to update from textbox configuration changes.

- #### `GetWidth()`
	- **Arguments:** None.
	- **Returns:** `Real`

- #### `GetHeight()`
	- **Arguments:** None.
	- **Returns:** `Real`

- #### `GetBoxWidth()`
	- **Arguments:** None.
	- **Returns:** `Real`

- #### `GetBoxHeight()`
	- **Arguments:** None.
	- **Returns:** `Real`

### Binding and text metadata

- #### `BindText(struct_ref, key)`
	- **Arguments:**
		- `struct_ref` `Struct`
		- `key` `String`
	- **Returns:** `Struct.__Quill`

- #### `SetPlaceholder(text)`
	- **Arguments:**
		- `text` `String`
	- **Returns:** `Struct.__Quill`

- #### `SetLabel(text)`
	- **Arguments:**
		- `text` `String`
	- **Returns:** `Struct.__Quill`

- #### `SetLabelVisible(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`

- #### `SetLabelPlacement(placement)`
	- **Arguments:**
		- `placement` `Any` Use `eQuillLabelPlacement.*`.
	- **Returns:** `Struct.__Quill`

- #### `SetLabelAlign(align)`
	- **Arguments:**
		- `align` `Any` Use `eQuillLabelAlign.*`.
	- **Returns:** `Struct.__Quill`

- #### `SetLabelOverflow(overflow)`
	- **Arguments:**
		- `overflow` `Any` Use `eQuillLabelOverflow.*`.
	- **Returns:** `Struct.__Quill`

- #### `SetLabelOffset(pixels)`
	- **Arguments:**
		- `pixels` `Real`
	- **Returns:** `Struct.__Quill`

- #### `SetLabelWidth(width)`
	- **Arguments:**
		- `width` `Real`
	- **Returns:** `Struct.__Quill`

### Callbacks

- #### `OnChange(fn)`
	- **Arguments:**
		- `fn` `Function`
	- **Returns:** `Struct.__Quill`

- #### `OnFocus(fn)`
	- **Arguments:**
		- `fn` `Function`
	- **Returns:** `Struct.__Quill`

- #### `OnBlur(fn)`
	- **Arguments:**
		- `fn` `Function`
	- **Returns:** `Struct.__Quill`

- #### `OnSubmit(fn)`
	- **Arguments:**
		- `fn` `Function`
	- **Returns:** `Struct.__Quill`

- #### `OnCancel(fn)`
	- **Arguments:**
		- `fn` `Function`
	- **Returns:** `Struct.__Quill`

### Focus, tab, and enabled state

- #### `Focus()`
	- **Arguments:** None.
	- **Returns:** `Struct.__Quill`

- #### `Blur()`
	- **Arguments:** None.
	- **Returns:** `Struct.__Quill`

- #### `IsFocused()`
	- **Arguments:** None.
	- **Returns:** `Bool`

- #### `SetTabEnabled(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`

- #### `SetTabOrder(order)`
	- **Arguments:**
		- `order` `Real`
	- **Returns:** `Struct.__Quill`

- #### `SetMultilineSubmitOnCtrlEnter(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`

- #### `SetEnabled(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`

- #### `IsEnabled()`
	- **Arguments:** None.
	- **Returns:** `Bool`

### Per-textbox context menu registry

- #### `ContextMenuAddItem(item)`
	- **Arguments:**
		- `item` `Struct`
	- **Returns:** `Struct.__Quill`

- #### `ContextMenuRemoveItem(key_or_uid)`
	- **Arguments:**
		- `key_or_uid` `String|Real`
	- **Returns:** `Struct.__Quill`

- #### `ContextMenuGetItem(key_or_uid)`
	- **Arguments:**
		- `key_or_uid` `String|Real`
	- **Returns:** `Struct`

- #### `ContextMenuClearItems()`
	- **Arguments:** None.
	- **Returns:** `Struct.__Quill`

### Text transforms and filtering

- #### `SetTextAlign(align)`
	- **Arguments:**
		- `align` `Any` Use `eQuillTextAlign.*`.
	- **Returns:** `Struct.__Quill`

- #### `AddTransform(fn)`
	- **Arguments:**
		- `fn` `Function`
	- **Returns:** `Struct.__Quill`

- #### `ClearTransforms()`
	- **Arguments:** None.
	- **Returns:** `Struct.__Quill`

- #### `SetAutoTrim(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`

- #### `SetAutoUpper(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`

- #### `SetAutoLower(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`

- #### `SetReadOnly(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`

- #### `SetMaxLength(len)`
	- **Arguments:**
		- `len` `Real`
	- **Returns:** `Struct.__Quill`

- #### `SetAllowedChars(chars)`
	- **Arguments:**
		- `chars` `String`
	- **Returns:** `Struct.__Quill`

- #### `SetDeniedChars(chars)`
	- **Arguments:**
		- `chars` `String`
	- **Returns:** `Struct.__Quill`

- #### `SetNumericOnly(flag, allow_decimal = false, allow_negative = false)`
	- **Arguments:**
		- `flag` `Bool`
		- `allow_decimal` `Bool` Optional, defaults to `false`.
		- `allow_negative` `Bool` Optional, defaults to `false`.
	- **Returns:** `Struct.__Quill`

- #### `SetSelectAllOnFocus(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`

- #### `SetFilterFn(fn)`
	- **Arguments:**
		- `fn` `Function`
	- **Returns:** `Struct.__Quill`

- #### `SetOnLiveChange(fn, rate_ms = 0)`
	- **Arguments:**
		- `fn` `Function`
		- `rate_ms` `Real` Optional, defaults to `0`.
	- **Returns:** `Struct.__Quill`

- #### `SetInputMode(mode)`
	- **Arguments:**
		- `mode` `Any` Use `QUILL_TEXTMODE_*`.
	- **Returns:** `Struct.__Quill`

### Multiline/code/password controls

- #### `SetTabInserts(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`

- #### `SetTabUsesSpaces(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`

- #### `SetTabSpaces(count)`
	- **Arguments:**
		- `count` `Real`
	- **Returns:** `Struct.__Quill`

- #### `SetAutoIndent(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`

- #### `SetPasswordMask(flag, mask_char = "*", allow_copy = false)`
	- **Arguments:**
		- `flag` `Bool`
		- `mask_char` `String` Optional, defaults to `"*"`.
		- `allow_copy` `Bool` Optional, defaults to `false`.
	- **Returns:** `Struct.__Quill`

- #### `SetWrap(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`
	- **Notes:** On multiline textboxes, setting `false` enables horizontal overflow scrolling (horizontal scrollbar when needed, and `Shift + mouse wheel` scrolls horizontally).

- #### `SetFont(font_asset)`
	- **Arguments:**
		- `font_asset` `Asset.Font`
	- **Returns:** `Struct.__Quill`

- #### `SetPreferredWidth(pixels)`
	- **Arguments:**
		- `pixels` `Real`
	- **Returns:** `Struct.__Quill`

- #### `GetPreferredWidth()`
	- **Arguments:** None.
	- **Returns:** `Real`

- #### `SetVisibleRows(rows)`
	- **Arguments:**
		- `rows` `Real`
	- **Returns:** `Struct.__Quill`

- #### `GetVisibleRows()`
	- **Arguments:** None.
	- **Returns:** `Real`

- #### `SetPreferredHeight(pixels)`
	- **Arguments:**
		- `pixels` `Real`
	- **Returns:** `Struct.__Quill`

- #### `GetPreferredHeight()`
	- **Arguments:** None.
	- **Returns:** `Real`

- #### `SetMinHeight(pixels)`
	- **Arguments:**
		- `pixels` `Real`
	- **Returns:** `Struct.__Quill`

- #### `GetMinHeight()`
	- **Arguments:** None.
	- **Returns:** `Real`

- #### `SetMaxHeight(pixels)`
	- **Arguments:**
		- `pixels` `Real`
	- **Returns:** `Struct.__Quill`

- #### `GetMaxHeight()`
	- **Arguments:** None.
	- **Returns:** `Real`

- #### `SetResizable(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`

- #### `IsResizable()`
	- **Arguments:** None.
	- **Returns:** `Bool`

- #### `SetShowResizeGrip(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`

- #### `IsResizeGripVisible()`
	- **Arguments:** None.
	- **Returns:** `Bool`

- #### `SetUseOverlayEditor(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`

- #### `IsUsingOverlayEditor()`
	- **Arguments:** None.
	- **Returns:** `Bool`

- #### `SetOverlayEditorTitle(title)`
	- **Arguments:**
		- `title` `String`
	- **Returns:** `Struct.__Quill`

- #### `GetOverlayEditorTitle()`
	- **Arguments:** None.
	- **Returns:** `String`

### Validation

- #### `SetValidationMessage(text, kind = "error")`
	- **Arguments:**
		- `text` `String`
		- `kind` `String` Optional, defaults to `"error"`.
	- **Returns:** `Struct.__Quill`

- #### `ClearValidationMessage()`
	- **Arguments:** None.
	- **Returns:** `Struct.__Quill`

- #### `SetValidationVisible(flag)`
	- **Arguments:**
		- `flag` `Bool`
	- **Returns:** `Struct.__Quill`

### Theme and style overrides

- #### `SetTheme(theme_or_minus_one)`
	- **Arguments:**
		- `theme_or_minus_one` `Struct.QuillTheme|Real`
	- **Returns:** `Struct.__Quill`

- #### `SetLabelFont(font)`
	- **Arguments:**
		- `font` `Asset.Font`
	- **Returns:** `Struct.__Quill`

- #### `SetLabelPadding(l, t, r, b)`
	- **Arguments:**
		- `l` `Real`
		- `t` `Real`
		- `r` `Real`
		- `b` `Real`
	- **Returns:** `Struct.__Quill`

- #### `SetLabelMargin(l, t, r, b)`
	- **Arguments:**
		- `l` `Real`
		- `t` `Real`
		- `r` `Real`
		- `b` `Real`
	- **Returns:** `Struct.__Quill`

- #### `SetLabelTextStyle(col, alpha = 1)`
	- **Arguments:**
		- `col` `Real`
		- `alpha` `Real` Optional, defaults to `1`.
	- **Returns:** `Struct.__Quill`

- #### `SetLabelBackgroundSprite(spr, subimg = 0)`
	- **Arguments:**
		- `spr` `Asset.Sprite`
		- `subimg` `Real` Optional, defaults to `0`.
	- **Returns:** `Struct.__Quill`

- #### `SetLabelBorderSprite(spr, subimg = 0)`
	- **Arguments:**
		- `spr` `Asset.Sprite`
		- `subimg` `Real` Optional, defaults to `0`.
	- **Returns:** `Struct.__Quill`

- #### `SetLabelPrimitiveBackground(col, alpha = 1)`
	- **Arguments:**
		- `col` `Real`
		- `alpha` `Real` Optional, defaults to `1`.
	- **Returns:** `Struct.__Quill`

- #### `SetLabelPrimitiveBorder(col, alpha = 1, thickness = 1)`
	- **Arguments:**
		- `col` `Real`
		- `alpha` `Real` Optional, defaults to `1`.
		- `thickness` `Real` Optional, defaults to `1`.
	- **Returns:** `Struct.__Quill`

- #### `SetSkinBackgroundSprite(spr, subimg = 0)`
	- **Arguments:**
		- `spr` `Asset.Sprite`
		- `subimg` `Real` Optional, defaults to `0`.
	- **Returns:** `Struct.__Quill`

- #### `SetSkinBorderSprite(spr, subimg = 0)`
	- **Arguments:**
		- `spr` `Asset.Sprite`
		- `subimg` `Real` Optional, defaults to `0`.
	- **Returns:** `Struct.__Quill`

### Rendering

- #### `Draw(x, y, w = undefined, h = undefined)`
	- **Arguments:**
		- `x` `Real`
		- `y` `Real`
		- `w` `Real|Undefined` Optional. Uses `preferred_width` when omitted.
		- `h` `Real|Undefined` Optional.
	- **Returns:** `Void`

- #### `DrawOverlay()`
	- **Arguments:** None.
	- **Returns:** `Void`

---

## Theme API

### `new QuillTheme()`

Creates a root theme object.

**Returns**: `Struct.QuillTheme`

**Members**
- `fonts`
- `textbox`
- `label`
- `skins`
- `selection`
- `caret`
- `scrollbar`
- `menu`
- `editor`

**Setters**
- `SetFonts(font_theme)`
- `SetTextbox(tb_theme)`
- `SetLabel(label_theme)`
- `SetSkins(skin_theme)`
- `SetSelection(sel_theme)`
- `SetCaret(caret_theme)`
- `SetScrollbar(scroll_theme)`
- `SetMenu(menu_theme)`
- `SetEditor(editor_theme)`

---

### Subtheme constructors

- `new QuillFontSubtheme()`
- `new QuillTextboxSubtheme()`
- `new QuillLabelSubtheme()`
- `new QuillSkinSubtheme()`
- `new QuillSelectionSubtheme()`
- `new QuillCaretSubtheme()`
- `new QuillScrollbarSubtheme()`
- `new QuillMenuSubtheme()`
- `new QuillEditorSubtheme()`

`QuillFontSubtheme` exposes `body`, `code`, `label`, `menu`, `editor_title`, `editor_body`, and `validation`.
`QuillScrollbarSubtheme` includes `border_spr_outside_draw` for Nine Slice outside-border rendering.
`QuillMenuSubtheme` includes `border_spr_outside_draw` for Nine Slice outside-border rendering.
`QuillEditorSubtheme` includes `panel_border_spr_outside_draw` for Nine Slice outside-border rendering.

---

### Built-in presets

- `new QuillTheme_VoidMango()`
- `new QuillTheme_ChunkyCandy()`

---

## Callback signatures

- `OnChange(fn)` -> `fn(tb, new_value)`
- `OnFocus(fn)` -> `fn(tb)`
- `OnBlur(fn)` -> `fn(tb)`
- `OnSubmit(fn)` -> `fn(tb, value)`
- `OnCancel(fn)` -> `fn(tb)`
- `SetFilterFn(fn)` -> `fn(insert_text) -> string`
- `SetOnLiveChange(fn)` -> `fn(text)`
- `AddTransform(fn)` -> `fn(text) -> text`

Use `method(scope, fn)` for callback scope binding.

---

## Custom context menu item schema

For `QUILL.OpenContextMenu(items, x, y, owner_id)`, each item can be either:
- a plain struct using the fields below
- or an item created by `QuillContextMenuItem(...)` / `QuillContextMenuSeparator(...)`

### Common fields

- `__uid` (auto-assigned unique numeric ID)
- `key` (string, optional semantic key)

### Action item fields

- `label` (string)
- `shortcut` (string, optional)
- `enabled` (bool, optional, default true)
- `visible` (bool, optional, default true)
- `on_click` (callable)

### Separator item fields

- `is_separator: true`

### Item instance methods

- `SetKey(key)`
- `SetLabel(label)`
- `SetShortcut(shortcut)`
- `SetEnabled(flag)`
- `SetVisible(flag)`
- `SetOnClick(on_click)`

---

## Notes on internal API

Methods prefixed with `__` are internal implementation details and aren't stable API.
