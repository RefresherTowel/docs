---
layout: "default"
title: "API Reference"
parent: "Echo Chamber"
nav_order: 6
library_id: "echo_chamber"
doc_version: "current"
api_reference: true
---

<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. -->
<!-- Source: GML JSDoc + echo-chamber.yml -->

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>

1. TOC
{:toc}

</details>
</div>

# API Reference

Complete reference for Echo Chamber's roots, windows, panels, controls, input, themes, and Echo Console APIs. For explanations and worked examples, start with the teaching pages; this page is for looking up exact capabilities.

---

## Binding and input

### EchoChamberFieldBinding
{: #echo-chamber-field-binding .api-type-title }

Connects a control to a struct field whose target can change over time.

```gml
new EchoChamberFieldBinding(target_fn, key, fallback)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">target_fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function() -&gt; Struct</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">fallback <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-chamber-field-binding-set-fallback"><code>SetFallback()</code></a></td><td>Sets the value returned when the target or field is unavailable.</td></tr>
<tr><td><a href="#echo-chamber-field-binding-set-read-only"><code>SetReadOnly()</code></a></td><td>Enables or disables writes through this binding.</td></tr>
<tr><td><a href="#echo-chamber-field-binding-set-on-write"><code>SetOnWrite()</code></a></td><td>Sets a callback that runs after a successful write as function(_target, _key, _next, _prev). When a control writes through a root, Echo Chamber queues this callback until its UI callback pass rather than running it during control drawing.</td></tr>
<tr><td><a href="#echo-chamber-field-binding-get-target"><code>GetTarget()</code></a></td><td>Returns the current target. The target function should only return the target and must not rebuild UI or run other callbacks. The target callback must only resolve the current target. It must not rebuild UI, mutate panels, or fire callbacks.</td></tr>
<tr><td><a href="#echo-chamber-field-binding-get"><code>Get()</code></a></td><td>Returns the current field value, or the fallback when the target or field is unavailable.</td></tr>
<tr><td><a href="#echo-chamber-field-binding-set"><code>Set()</code></a></td><td>Writes the field on the current target and runs the optional write callback. Returns false when the binding is read-only or has no usable target or key.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-field-binding-set-fallback">
  <div class="api-method-name">SetFallback(value)</div>
  <p class="api-method-summary">Sets the value returned when the target or field is unavailable.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">value</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-field-binding">EchoChamberFieldBinding</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-field-binding-set-read-only">
  <div class="api-method-name">SetReadOnly([enabled])</div>
  <p class="api-method-summary">Enables or disables writes through this binding.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">enabled <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-field-binding">EchoChamberFieldBinding</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-field-binding-set-on-write">
  <div class="api-method-name">SetOnWrite(fn)</div>
  <p class="api-method-summary">Sets a callback that runs after a successful write as function(_target, _key, _next, _prev). When a control writes through a root, Echo Chamber queues this callback until its UI callback pass rather than running it during control drawing.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-field-binding">EchoChamberFieldBinding</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-field-binding-get-target">
  <div class="api-method-name">GetTarget()</div>
  <p class="api-method-summary">Returns the current target. The target function should only return the target and must not rebuild UI or run other callbacks. The target callback must only resolve the current target. It must not rebuild UI, mutate panels, or fire callbacks.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-field-binding-get">
  <div class="api-method-name">Get()</div>
  <p class="api-method-summary">Returns the current field value, or the fallback when the target or field is unavailable.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-field-binding-set">
  <div class="api-method-name">Set(value, [root])</div>
  <p class="api-method-summary">Writes the field on the current target and runs the optional write callback. Returns false when the binding is read-only or has no usable target or key.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">value</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">root <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a>|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

### EchoChamberInputBinding
{: #echo-chamber-input-binding .api-type-title }

Base type shared by Echo Chamber input bindings.

```gml
new EchoChamberInputBinding()
```

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-chamber-input-binding-get-key"><code>GetKey()</code></a></td><td>Returns the keyboard keycode for a key binding, or undefined for other binding types.</td></tr>
<tr><td><a href="#echo-chamber-input-binding-get-display-text"><code>GetDisplayText()</code></a></td><td>Returns this binding as display text for help text or menu shortcuts. Returns the same text as <a href="#echo-chamber-input-format-binding"><code>EchoChamberInputFormatBinding(self)</code></a>.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-input-binding-get-key">
  <div class="api-method-name">GetKey()</div>
  <p class="api-method-summary">Returns the keyboard keycode for a key binding, or undefined for other binding types.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-input-binding-get-display-text">
  <div class="api-method-name">GetDisplayText()</div>
  <p class="api-method-summary">Returns this binding as display text for help text or menu shortcuts. Returns the same text as <a href="#echo-chamber-input-format-binding"><code>EchoChamberInputFormatBinding(self)</code></a>.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

### EchoChamberInputBindingKey
{: #echo-chamber-input-binding-key .api-type-title }

Keyboard binding for an Echo Chamber input action.

Inherits from [`EchoChamberInputBinding`](#echo-chamber-input-binding).

```gml
new EchoChamberInputBindingKey(key, check, ctrl, alt, shift)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Keyboard keycode (vk_* or ord()).</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">check <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Input check type (pressed/down/released).</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">ctrl <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Require Ctrl to be held.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">alt <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Require Alt to be held.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">shift <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Require Shift to be held.</span>
    </div>
  </div>
</div>

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-chamber-input-binding-key-get-key"><code>GetKey()</code></a></td><td>Returns the keyboard keycode used by this binding.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-input-binding-key-get-key">
  <div class="api-method-name">GetKey()</div>
  <p class="api-method-summary">Returns the keyboard keycode used by this binding.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

### EchoChamberInputBindingFunc
{: #echo-chamber-input-binding-func .api-type-title }

Function binding for an Echo Chamber input action.

Inherits from [`EchoChamberInputBinding`](#echo-chamber-input-binding).

```gml
new EchoChamberInputBindingFunc(fn)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function that returns true when the action should fire.</span>
    </div>
  </div>
</div>

### EchoChamberInputBindingBlock
{: #echo-chamber-input-binding-block .api-type-title }

Blocks an input action from being inherited from a parent context.

Inherits from [`EchoChamberInputBinding`](#echo-chamber-input-binding).

```gml
new EchoChamberInputBindingBlock()
```

### EchoChamberInputContext
{: #echo-chamber-input-context .api-type-title }

Stores Echo Chamber input actions and can inherit bindings from a parent context.

```gml
new EchoChamberInputContext(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Context ID.</span>
    </div>
  </div>
</div>

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-chamber-input-context-set-parent"><code>SetParent()</code></a></td><td>Sets the parent context ID for inheritance.</td></tr>
<tr><td><a href="#echo-chamber-input-context-get-binding"><code>GetBinding()</code></a></td><td>Returns the binding for an action ID (or undefined if none).</td></tr>
<tr><td><a href="#echo-chamber-input-context-bind-action"><code>BindAction()</code></a></td><td>Binds an action to a binding instance.</td></tr>
<tr><td><a href="#echo-chamber-input-context-bind-key"><code>BindKey()</code></a></td><td>Binds an action to a keyboard key.</td></tr>
<tr><td><a href="#echo-chamber-input-context-bind-func"><code>BindFunc()</code></a></td><td>Binds an action to a custom function.</td></tr>
<tr><td><a href="#echo-chamber-input-context-bind-block"><code>BindBlock()</code></a></td><td>Binds an action to a blocker (prevents inheritance).</td></tr>
<tr><td><a href="#echo-chamber-input-context-clear-action"><code>ClearAction()</code></a></td><td>Clears a local action binding (falls back to parent context).</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-input-context-set-parent">
  <div class="api-method-name">SetParent(parent_id)</div>
  <p class="api-method-summary">Sets the parent context ID for inheritance.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">parent_id</span>
      <span class="api-argument-type">String|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-input-context">EchoChamberInputContext</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-input-context-get-binding">
  <div class="api-method-name">GetBinding(action_id)</div>
  <p class="api-method-summary">Returns the binding for an action ID (or undefined if none).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">action_id</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-input-binding">EchoChamberInputBinding</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-input-context-bind-action">
  <div class="api-method-name">BindAction(action_id, binding)</div>
  <p class="api-method-summary">Binds an action to a binding instance.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">action_id</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">binding</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-input-binding">EchoChamberInputBinding</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-input-context">EchoChamberInputContext</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-input-context-bind-key">
  <div class="api-method-name">BindKey(action_id, key, [check], [ctrl], [alt], [shift])</div>
  <p class="api-method-summary">Binds an action to a keyboard key.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">action_id</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Keyboard keycode (vk_* or ord()).</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">check <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Input check type (pressed/down/released).</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">ctrl <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Require Ctrl to be held.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">alt <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Require Alt to be held.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">shift <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Require Shift to be held.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-input-context">EchoChamberInputContext</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-input-context-bind-func">
  <div class="api-method-name">BindFunc(action_id, fn)</div>
  <p class="api-method-summary">Binds an action to a custom function.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">action_id</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function that returns true when the action should fire.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-input-context">EchoChamberInputContext</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-input-context-bind-block">
  <div class="api-method-name">BindBlock(action_id)</div>
  <p class="api-method-summary">Binds an action to a blocker (prevents inheritance).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">action_id</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-input-context">EchoChamberInputContext</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-input-context-clear-action">
  <div class="api-method-name">ClearAction(action_id)</div>
  <p class="api-method-summary">Clears a local action binding (falls back to parent context).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">action_id</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-input-context">EchoChamberInputContext</a></span>
    </div>
  </div>
</div>

## Desktop, windows, and panels

### EchoChamberRoot
{: #echo-chamber-root .api-type-title }

Owns the Echo Chamber windows, panels, controls, input, and shared UI state.

```gml
new EchoChamberRoot(theme)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">theme</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-theme">EchoChamberTheme</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Theme and input</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-root-refresh-theme"><code>RefreshTheme()</code></a></td><td>Reapplies the current theme and refreshes cached styles and layout defaults.</td></tr>
<tr><td><a href="#echo-chamber-root-mark-theme-dirty"><code>MarkThemeDirty()</code></a></td><td>Alias of RefreshTheme().</td></tr>
<tr><td><a href="#echo-chamber-root-apply-theme"><code>ApplyTheme()</code></a></td><td>Apply a new theme and reapply defaults across windows and panels.</td></tr>
<tr><td><a href="#echo-chamber-root-get-default-input-context-id"><code>GetDefaultInputContextId()</code></a></td><td>Returns the default input context ID used for global actions.</td></tr>
<tr><td><a href="#echo-chamber-root-bind-core-input-action"><code>BindCoreInputAction()</code></a></td><td>Binds a core Echo Chamber action in the default input context.</td></tr>
<tr><td><a href="#echo-chamber-root-get-input-context"><code>GetInputContext()</code></a></td><td>Returns an input context by ID.</td></tr>
<tr><td><a href="#echo-chamber-root-create-input-context"><code>CreateInputContext()</code></a></td><td>Returns an input context by ID, creating it if needed. New contexts inherit from the default context unless a parent is given.</td></tr>
<tr><td><a href="#echo-chamber-root-remove-input-context"><code>RemoveInputContext()</code></a></td><td>Removes an input context by ID (only if unused by any window). Returns false for the default context or contexts still used by a window.</td></tr>
<tr><td><a href="#echo-chamber-root-ec-input-pressed"><code>EC_InputPressed()</code></a></td><td>Checks whether an action is pressed in the active input context.</td></tr>
<tr><td><a href="#echo-chamber-root-ec-input-down"><code>EC_InputDown()</code></a></td><td>Checks whether an action is held down in the active input context.</td></tr>
<tr><td><a href="#echo-chamber-root-ec-input-released"><code>EC_InputReleased()</code></a></td><td>Checks whether an action was released in the active input context.</td></tr>
</tbody></table>

<div class="api-method-group-title">Panels and windows</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-root-add-panel"><code>AddPanel()</code></a></td><td>Adds a top-level panel to the root.</td></tr>
<tr><td><a href="#echo-chamber-root-create-window"><code>CreateWindow()</code></a></td><td>Creates and registers a floating debug window.</td></tr>
<tr><td><a href="#echo-chamber-root-get-debug-manager"><code>GetDebugManager()</code></a></td><td>Returns the shared Echo Chamber debug manager for this root.</td></tr>
<tr><td><a href="#echo-chamber-root-register-window"><code>RegisterWindow()</code></a></td><td>Registers an externally created window instance.</td></tr>
<tr><td><a href="#echo-chamber-root-find-window"><code>FindWindow()</code></a></td><td>Finds a registered window by ID.</td></tr>
<tr><td><a href="#echo-chamber-root-find-control"><code>FindControl()</code></a></td><td>Finds a control by ID across all registered windows.</td></tr>
<tr><td><a href="#echo-chamber-root-dump-ui"><code>DumpUI()</code></a></td><td>Dump the current UI tree and focus/overlay state to the debug log.</td></tr>
<tr><td><a href="#echo-chamber-root-remove-window"><code>RemoveWindow()</code></a></td><td>Removes a registered window and detach its panels/controls.</td></tr>
</tbody></table>

<div class="api-method-group-title">Window ordering and modality</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-root-bring-window-to-front"><code>BringWindowToFront()</code></a></td><td>Brings a window to the front of the z-order.</td></tr>
<tr><td><a href="#echo-chamber-root-bring-window-to-front-by-id"><code>BringWindowToFrontById()</code></a></td><td>Brings a window to the front by ID.</td></tr>
<tr><td><a href="#echo-chamber-root-send-window-to-back"><code>SendWindowToBack()</code></a></td><td>Send a window to the back of the z-order.</td></tr>
<tr><td><a href="#echo-chamber-root-set-window-zindex"><code>SetWindowZIndex()</code></a></td><td>Sets a window&#x27;s z-order index (0 = back, last = front).</td></tr>
<tr><td><a href="#echo-chamber-root-set-modal-window"><code>SetModalWindow()</code></a></td><td>Sets the modal window (blocks input to other windows).</td></tr>
<tr><td><a href="#echo-chamber-root-clear-modal-window"><code>ClearModalWindow()</code></a></td><td>Clears the modal window (if any).</td></tr>
<tr><td><a href="#echo-chamber-root-get-modal-window"><code>GetModalWindow()</code></a></td><td>Returns the current modal window (if any).</td></tr>
<tr><td><a href="#echo-chamber-root-is-window-frontmost-for-pointer-input"><code>IsWindowFrontmostForPointerInput()</code></a></td><td>Returns whether a window is treated as frontmost for pointer input after modal, overlay, and mouse-capture ownership are applied.</td></tr>
<tr><td><a href="#echo-chamber-root-bring-windows-back"><code>BringWindowsBack()</code></a></td><td>Brings all windows back into view so their title bars remain accessible.</td></tr>
<tr><td><a href="#echo-chamber-root-reset-window-layouts"><code>ResetWindowLayouts()</code></a></td><td>Resets registered window layouts to their stored default rectangles and sizing limits.</td></tr>
</tbody></table>

<div class="api-method-group-title">Persistence</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-root-set-persistence-file"><code>SetPersistenceFile()</code></a></td><td>Sets the INI filename used for saving and loading UI layout state.</td></tr>
<tr><td><a href="#echo-chamber-root-set-persistence-section"><code>SetPersistenceSection()</code></a></td><td>Sets the INI section prefix used for saving and loading UI layout state.</td></tr>
<tr><td><a href="#echo-chamber-root-save-layout"><code>SaveLayout()</code></a></td><td>Saves window layout, z-order, and panel state to an INI file.</td></tr>
<tr><td><a href="#echo-chamber-root-load-layout"><code>LoadLayout()</code></a></td><td>Loads window layout, z-order, and panel state from an INI file. Windows and panels must already be created/registered before calling this.</td></tr>
</tbody></table>

<div class="api-method-group-title">Pointer, scrolling, and clipping</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-root-set-mouse-capture"><code>SetMouseCapture()</code></a></td><td>Captures the mouse for a window interaction (drag/resize).</td></tr>
<tr><td><a href="#echo-chamber-root-clear-mouse-capture"><code>ClearMouseCapture()</code></a></td><td>Release mouse capture if owned by the given window.</td></tr>
<tr><td><a href="#echo-chamber-root-run-desktop"><code>RunDesktop()</code></a></td><td>Runs the managed desktop: capture input, process the active window, draw all windows, then draw overlays and tooltip. Call once per frame from Draw GUI End for the root you want to display. <code>RunDesktop()</code> establishes Echo Chamber&#x27;s independent window-backed canvas internally. One canvas unit corresponds to one game-window pixel at the default scale.</td></tr>
<tr><td><a href="#echo-chamber-root-consume-mouse"><code>ConsumeMouse()</code></a></td><td>Consume mouse input for all remaining controls this frame.</td></tr>
<tr><td><a href="#echo-chamber-root-consume-wheel"><code>ConsumeWheel()</code></a></td><td>Consume mouse wheel for all remaining scroll regions.</td></tr>
<tr><td><a href="#echo-chamber-root-draw-scroll-area"><code>DrawScrollArea()</code></a></td><td>Draws a scrollable clipped region and handle mouse wheel scrolling when hovered. Includes scrollbar thumb dragging and track page jumps.</td></tr>
<tr><td><a href="#echo-chamber-root-push-clip-rect"><code>PushClipRect()</code></a></td><td>Push a clip rectangle. Any existing clip will be intersected with this one.</td></tr>
<tr><td><a href="#echo-chamber-root-pop-clip-rect"><code>PopClipRect()</code></a></td><td>Pop the most recently pushed clip rectangle.</td></tr>
<tr><td><a href="#echo-chamber-root-hit-test-rect"><code>HitTestRect()</code></a></td><td>Simple hit test for a rectangle, respecting mouse_consumed and the current clip region.</td></tr>
</tbody></table>

<div class="api-method-group-title">Tooltips, popups, and overlays</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-root-request-tooltip"><code>RequestTooltip()</code></a></td><td>Request a tooltip for a given control ID.</td></tr>
<tr><td><a href="#echo-chamber-root-draw-tooltip-text-at"><code>DrawTooltipTextAt()</code></a></td><td>Draws tooltip text immediately at an Echo Chamber canvas anchor point.</td></tr>
<tr><td><a href="#echo-chamber-root-set-active-overlay-owner"><code>SetActiveOverlayOwner()</code></a></td><td>Mark a control as owning a modal overlay (e.g. a dropdown).</td></tr>
<tr><td><a href="#echo-chamber-root-clear-active-overlay-owner"><code>ClearActiveOverlayOwner()</code></a></td><td>Clears the active overlay (if any).</td></tr>
<tr><td><a href="#echo-chamber-root-consume-overlay-close-request"><code>ConsumeOverlayCloseRequest()</code></a></td><td>Returns true if a close request is pending for the current active overlay owner ID. Consumes the request.</td></tr>
<tr><td><a href="#echo-chamber-root-resolve-anchored-popup-rect"><code>ResolveAnchoredPopupRect()</code></a></td><td>Finds a popup rectangle beside a control while keeping it on screen. Returns <code>undefined</code> when <code>_anchor_rect</code> isn&#x27;t a rectangle struct. The return struct is <code>{ rect, direction, space_above, space_below }</code>. <code>rect</code> is <code>{ x1, y1, x2, y2 }</code>, <code>direction</code> is the actual popup direction used after fallback, and the space fields are available vertical pixels before clamping.</td></tr>
<tr><td><a href="#echo-chamber-root-resolve-point-popup-rect"><code>ResolvePointPopupRect()</code></a></td><td>Finds a popup rectangle beside a screen point while keeping it on screen. Returns <code>{ rect }</code>, where <code>rect</code> is <code>{ x1, y1, x2, y2 }</code> clamped to the popup viewport.</td></tr>
<tr><td><a href="#echo-chamber-root-should-close-popup-on-outside-click"><code>ShouldClosePopupOnOutsideClick()</code></a></td><td>Returns true when a popup should close because the user clicked outside both its base rectangle and popup rectangle.</td></tr>
<tr><td><a href="#echo-chamber-root-draw-popup-frame"><code>DrawPopupFrame()</code></a></td><td>Draws a generic popup frame using popup styles. Draws only the generic popup background, border, and optional header band. Popup contents are drawn by the caller.</td></tr>
<tr><td><a href="#echo-chamber-root-open-color-picker-popup"><code>OpenColorPickerPopup()</code></a></td><td>Opens the color picker popup. Use either <code>bind_struct</code> plus <code>bind_key</code>, or <code>get_color</code> plus <code>set_color</code>, for live color binding. <code>on_change</code> runs during edits, <code>on_commit</code> runs when closing with commit, and <code>on_cancel</code> runs when closing without commit.</td></tr>
<tr><td><a href="#echo-chamber-root-close-color-picker-popup"><code>CloseColorPickerPopup()</code></a></td><td>Closes the color picker popup.</td></tr>
<tr><td><a href="#echo-chamber-root-is-color-picker-popup-open"><code>IsColorPickerPopupOpen()</code></a></td><td>Returns whether the color picker popup is open.</td></tr>
<tr><td><a href="#echo-chamber-root-queue-overlay"><code>QueueOverlay()</code></a></td><td>Queue an overlay draw callback. Overlays are drawn after all windows. <code>_draw_fn</code> is called as <code>function(_root)</code>. When <code>_rect</code> is supplied, Echo Chamber clips the overlay to that rectangle and consumes unhandled clicks inside it.</td></tr>
<tr><td><a href="#echo-chamber-root-open-context-menu"><code>OpenContextMenu()</code></a></td><td>Opens a context menu overlay at a screen position.</td></tr>
<tr><td><a href="#echo-chamber-root-close-context-menu"><code>CloseContextMenu()</code></a></td><td>Closes the active context menu overlay (if open).</td></tr>
<tr><td><a href="#echo-chamber-root-is-context-menu-open"><code>IsContextMenuOpen()</code></a></td><td>Returns true if the context menu overlay is open.</td></tr>
<tr><td><a href="#echo-chamber-root-show-toast"><code>ShowToast()</code></a></td><td>Shows a short non-blocking toast message.</td></tr>
<tr><td><a href="#echo-chamber-root-copy-to-clipboard"><code>CopyToClipboard()</code></a></td><td>Copies text to clipboard and show a toast confirmation.</td></tr>
</tbody></table>

<div class="api-method-group-title">Text and control focus</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-root-focus-text-input"><code>FocusTextInput()</code></a></td><td>Focuses a text input by ID and sets its starting text. The optional _commit_fn runs with the final text when focus is lost. <code>_commit_fn</code> is called as <code>function(_final_text)</code> on blur unless the edit is cancelled.</td></tr>
<tr><td><a href="#echo-chamber-root-blur-text-input"><code>BlurTextInput()</code></a></td><td>Removes focus from a text input, commits its text, and returns the final string without submitting it.</td></tr>
<tr><td><a href="#echo-chamber-root-submit-text-input"><code>SubmitTextInput()</code></a></td><td>Submits a focused text input, commits its text, runs OnSubmit, and returns the final string.</td></tr>
<tr><td><a href="#echo-chamber-root-cancel-text-input"><code>CancelTextInput()</code></a></td><td>Cancels editing, discards the current changes, and removes focus without committing or submitting.</td></tr>
<tr><td><a href="#echo-chamber-root-is-active-text-input"><code>IsActiveTextInput()</code></a></td><td>Returns true if the given ID is the currently focused text input.</td></tr>
<tr><td><a href="#echo-chamber-root-get-active-text"><code>GetActiveText()</code></a></td><td>Returns the current text while a text input is focused.</td></tr>
<tr><td><a href="#echo-chamber-root-get-text-buffer"><code>GetTextBuffer()</code></a></td><td>Returns the last committed text for the active text input.</td></tr>
<tr><td><a href="#echo-chamber-root-focus-control"><code>FocusControl()</code></a></td><td>Give keyboard focus to a non-text control by ID. This focus is separate from text input focus.</td></tr>
<tr><td><a href="#echo-chamber-root-is-control-focused"><code>IsControlFocused()</code></a></td><td>Returns true if the given control ID currently owns keyboard focus (and no text input is active).</td></tr>
<tr><td><a href="#echo-chamber-root-blur-control-focus"><code>BlurControlFocus()</code></a></td><td>Clears keyboard focus from a control by ID.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-root-refresh-theme">
  <div class="api-method-name">RefreshTheme()</div>
  <p class="api-method-summary">Reapplies the current theme and refreshes cached styles and layout defaults.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-mark-theme-dirty">
  <div class="api-method-name">MarkThemeDirty()</div>
  <p class="api-method-summary">Alias of RefreshTheme().</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-apply-theme">
  <div class="api-method-name">ApplyTheme(theme)</div>
  <p class="api-method-summary">Apply a new theme and reapply defaults across windows and panels.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">theme</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-theme">EchoChamberTheme</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-get-default-input-context-id">
  <div class="api-method-name">GetDefaultInputContextId()</div>
  <p class="api-method-summary">Returns the default input context ID used for global actions.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-bind-core-input-action">
  <div class="api-method-name">BindCoreInputAction(action_id, binding)</div>
  <p class="api-method-summary">Binds a core Echo Chamber action in the default input context.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">action_id</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">binding</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-input-binding">EchoChamberInputBinding</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-get-input-context">
  <div class="api-method-name">GetInputContext(id)</div>
  <p class="api-method-summary">Returns an input context by ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-input-context">EchoChamberInputContext</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-create-input-context">
  <div class="api-method-name">CreateInputContext(id, [parent_id])</div>
  <p class="api-method-summary">Returns an input context by ID, creating it if needed. New contexts inherit from the default context unless a parent is given.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">parent_id <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-input-context">EchoChamberInputContext</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-remove-input-context">
  <div class="api-method-name">RemoveInputContext(id)</div>
  <p class="api-method-summary">Removes an input context by ID (only if unused by any window). Returns false for the default context or contexts still used by a window.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-ec-input-pressed">
  <div class="api-method-name">EC_InputPressed(action_id, [window])</div>
  <p class="api-method-summary">Checks whether an action is pressed in the active input context.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">action_id</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">window <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-ec-input-down">
  <div class="api-method-name">EC_InputDown(action_id, [window])</div>
  <p class="api-method-summary">Checks whether an action is held down in the active input context.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">action_id</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">window <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-ec-input-released">
  <div class="api-method-name">EC_InputReleased(action_id, [window])</div>
  <p class="api-method-summary">Checks whether an action was released in the active input context.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">action_id</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">window <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-add-panel">
  <div class="api-method-name">AddPanel(panel)</div>
  <p class="api-method-summary">Adds a top-level panel to the root.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">panel</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-create-window">
  <div class="api-method-name">CreateWindow(id)</div>
  <p class="api-method-summary">Creates and registers a floating debug window.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-get-debug-manager">
  <div class="api-method-name">GetDebugManager()</div>
  <p class="api-method-summary">Returns the shared Echo Chamber debug manager for this root.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-console-manager">EchoConsoleManager</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-register-window">
  <div class="api-method-name">RegisterWindow(window)</div>
  <p class="api-method-summary">Registers an externally created window instance.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">window</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-find-window">
  <div class="api-method-name">FindWindow(id)</div>
  <p class="api-method-summary">Finds a registered window by ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-find-control">
  <div class="api-method-name">FindControl(id)</div>
  <p class="api-method-summary">Finds a control by ID across all registered windows.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-dump-ui">
  <div class="api-method-name">DumpUI()</div>
  <p class="api-method-summary">Dump the current UI tree and focus/overlay state to the debug log.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-remove-window">
  <div class="api-method-name">RemoveWindow(window_or_id)</div>
  <p class="api-method-summary">Removes a registered window and detach its panels/controls.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">window_or_id</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-bring-window-to-front">
  <div class="api-method-name">BringWindowToFront(window_or_id)</div>
  <p class="api-method-summary">Brings a window to the front of the z-order.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">window_or_id</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-bring-window-to-front-by-id">
  <div class="api-method-name">BringWindowToFrontById(id)</div>
  <p class="api-method-summary">Brings a window to the front by ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-send-window-to-back">
  <div class="api-method-name">SendWindowToBack(window_or_id)</div>
  <p class="api-method-summary">Send a window to the back of the z-order.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">window_or_id</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-set-window-zindex">
  <div class="api-method-name">SetWindowZIndex(window_or_id, index)</div>
  <p class="api-method-summary">Sets a window&#x27;s z-order index (0 = back, last = front).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">window_or_id</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|String|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">index</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-set-modal-window">
  <div class="api-method-name">SetModalWindow(window_or_id)</div>
  <p class="api-method-summary">Sets the modal window (blocks input to other windows).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">window_or_id</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|String|Real|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-clear-modal-window">
  <div class="api-method-name">ClearModalWindow()</div>
  <p class="api-method-summary">Clears the modal window (if any).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-get-modal-window">
  <div class="api-method-name">GetModalWindow()</div>
  <p class="api-method-summary">Returns the current modal window (if any).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-is-window-frontmost-for-pointer-input">
  <div class="api-method-name">IsWindowFrontmostForPointerInput(window)</div>
  <p class="api-method-summary">Returns whether a window is treated as frontmost for pointer input after modal, overlay, and mouse-capture ownership are applied.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">window</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
      <span class="api-argument-description">The window to test.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Bool</span>
      <span class="api-return-description">True when the window is the frontmost pointer-input target.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-bring-windows-back">
  <div class="api-method-name">BringWindowsBack()</div>
  <p class="api-method-summary">Brings all windows back into view so their title bars remain accessible.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-reset-window-layouts">
  <div class="api-method-name">ResetWindowLayouts([visible_only])</div>
  <p class="api-method-summary">Resets registered window layouts to their stored default rectangles and sizing limits.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">visible_only <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-set-persistence-file">
  <div class="api-method-name">SetPersistenceFile(filename)</div>
  <p class="api-method-summary">Sets the INI filename used for saving and loading UI layout state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">filename</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-set-persistence-section">
  <div class="api-method-name">SetPersistenceSection(section)</div>
  <p class="api-method-summary">Sets the INI section prefix used for saving and loading UI layout state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">section</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-save-layout">
  <div class="api-method-name">SaveLayout()</div>
  <p class="api-method-summary">Saves window layout, z-order, and panel state to an INI file.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-load-layout">
  <div class="api-method-name">LoadLayout()</div>
  <p class="api-method-summary">Loads window layout, z-order, and panel state from an INI file. Windows and panels must already be created/registered before calling this.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-set-mouse-capture">
  <div class="api-method-name">SetMouseCapture(window)</div>
  <p class="api-method-summary">Captures the mouse for a window interaction (drag/resize).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">window</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-clear-mouse-capture">
  <div class="api-method-name">ClearMouseCapture(window)</div>
  <p class="api-method-summary">Release mouse capture if owned by the given window.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">window</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-run-desktop">
  <div class="api-method-name">RunDesktop()</div>
  <p class="api-method-summary">Runs the managed desktop: capture input, process the active window, draw all windows, then draw overlays and tooltip. Call once per frame from Draw GUI End for the root you want to display. <code>RunDesktop()</code> establishes Echo Chamber&#x27;s independent window-backed canvas internally. One canvas unit corresponds to one game-window pixel at the default scale.</p>
</div>

<div class="api-method-entry" id="echo-chamber-root-consume-mouse">
  <div class="api-method-name">ConsumeMouse()</div>
  <p class="api-method-summary">Consume mouse input for all remaining controls this frame.</p>
</div>

<div class="api-method-entry" id="echo-chamber-root-consume-wheel">
  <div class="api-method-name">ConsumeWheel()</div>
  <p class="api-method-summary">Consume mouse wheel for all remaining scroll regions.</p>
</div>

<div class="api-method-entry" id="echo-chamber-root-draw-scroll-area">
  <div class="api-method-name">DrawScrollArea(scroll_state, rect, content_h, draw_fn, [draw_rect])</div>
  <p class="api-method-summary">Draws a scrollable clipped region and handle mouse wheel scrolling when hovered. Includes scrollbar thumb dragging and track page jumps.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">scroll_state</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-scroll-state">EchoChamberScrollState</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">rect</span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">{x1,y1,x2,y2}</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">content_h</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Total content height in pixels.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">draw_fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_root, _rect, _scroll_y)</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">draw_rect <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">Optional callback rectangle. Scroll clipping and scrollbar geometry still use _rect.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-push-clip-rect">
  <div class="api-method-name">PushClipRect(x1, y1, x2, y2)</div>
  <p class="api-method-summary">Push a clip rectangle. Any existing clip will be intersected with this one.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">x1</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">y1</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">x2</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">y2</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-pop-clip-rect">
  <div class="api-method-name">PopClipRect()</div>
  <p class="api-method-summary">Pop the most recently pushed clip rectangle.</p>
</div>

<div class="api-method-entry" id="echo-chamber-root-hit-test-rect">
  <div class="api-method-name">HitTestRect(x1, y1, x2, y2)</div>
  <p class="api-method-summary">Simple hit test for a rectangle, respecting mouse_consumed and the current clip region.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">x1</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">y1</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">x2</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">y2</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-request-tooltip">
  <div class="api-method-name">RequestTooltip(control_id, text, anchor_x, anchor_y)</div>
  <p class="api-method-summary">Request a tooltip for a given control ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">control_id</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">text</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">anchor_x</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">anchor_y</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-draw-tooltip-text-at">
  <div class="api-method-name">DrawTooltipTextAt(text, anchor_x, anchor_y, [owner_window])</div>
  <p class="api-method-summary">Draws tooltip text immediately at an Echo Chamber canvas anchor point.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">text</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">anchor_x</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">anchor_y</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">owner_window <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-set-active-overlay-owner">
  <div class="api-method-name">SetActiveOverlayOwner(control_id)</div>
  <p class="api-method-summary">Mark a control as owning a modal overlay (e.g. a dropdown).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">control_id</span>
      <span class="api-argument-type">String|Real|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-clear-active-overlay-owner">
  <div class="api-method-name">ClearActiveOverlayOwner()</div>
  <p class="api-method-summary">Clears the active overlay (if any).</p>
</div>

<div class="api-method-entry" id="echo-chamber-root-consume-overlay-close-request">
  <div class="api-method-name">ConsumeOverlayCloseRequest(owner_id)</div>
  <p class="api-method-summary">Returns true if a close request is pending for the current active overlay owner ID. Consumes the request.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">owner_id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-resolve-anchored-popup-rect">
  <div class="api-method-name">ResolveAnchoredPopupRect(anchor_rect, popup_w, popup_h, [preferred_direction], [align], [gap], [viewport_margin], [style_key])</div>
  <p class="api-method-summary">Finds a popup rectangle beside a control while keeping it on screen. Returns <code>undefined</code> when <code>_anchor_rect</code> isn&#x27;t a rectangle struct. The return struct is <code>{ rect, direction, space_above, space_below }</code>. <code>rect</code> is <code>{ x1, y1, x2, y2 }</code>, <code>direction</code> is the actual popup direction used after fallback, and the space fields are available vertical pixels before clamping.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">anchor_rect</span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">popup_w</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">popup_h</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">preferred_direction <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-popup-direction"><code>eEchoChamberPopupDirection</code></a> enum.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">align <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-align-hor"><code>eEchoChamberAlignHor</code></a> enum.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">gap <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real|Undefined</span>
      <span class="api-argument-description">Optional explicit anchor gap override.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">viewport_margin <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real|Undefined</span>
      <span class="api-argument-description">Optional explicit symmetric viewport margin override.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">style_key <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Popup style key used for default gap and viewport margins.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-resolve-point-popup-rect">
  <div class="api-method-name">ResolvePointPopupRect(x, y, popup_w, popup_h, [viewport_margin], [style_key])</div>
  <p class="api-method-summary">Finds a popup rectangle beside a screen point while keeping it on screen. Returns <code>{ rect }</code>, where <code>rect</code> is <code>{ x1, y1, x2, y2 }</code> clamped to the popup viewport.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">x</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">y</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">popup_w</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">popup_h</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">viewport_margin <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real|Undefined</span>
      <span class="api-argument-description">Optional explicit symmetric viewport margin override.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">style_key <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Popup style key used for default viewport margins.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-should-close-popup-on-outside-click">
  <div class="api-method-name">ShouldClosePopupOnOutsideClick(base_rect, popup_rect, [consume_mouse], [allow_right_click])</div>
  <p class="api-method-summary">Returns true when a popup should close because the user clicked outside both its base rectangle and popup rectangle.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">base_rect</span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">popup_rect</span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">consume_mouse <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">allow_right_click <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-draw-popup-frame">
  <div class="api-method-name">DrawPopupFrame(rect, [style_key], [header_h])</div>
  <p class="api-method-summary">Draws a generic popup frame using popup styles. Draws only the generic popup background, border, and optional header band. Popup contents are drawn by the caller.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">rect</span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">style_key <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">header_h <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-open-color-picker-popup">
  <div class="api-method-name">OpenColorPickerPopup(owner_id, anchor_rect, [owner_window], [config])</div>
  <p class="api-method-summary">Opens the color picker popup. Use either <code>bind_struct</code> plus <code>bind_key</code>, or <code>get_color</code> plus <code>set_color</code>, for live color binding. <code>on_change</code> runs during edits, <code>on_commit</code> runs when closing with commit, and <code>on_cancel</code> runs when closing without commit.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">owner_id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">anchor_rect</span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">owner_window <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">config <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct|Undefined</span>
      <span class="api-argument-description">Optional config struct. Supported keys include: - title:String - style_key:String - preferred_direction:String - align:String - visual_space:String - initial_color - bind_struct:Struct - bind_key:String - get_color:Function - set_color:Function - on_change:Function - on_commit:Function - on_cancel:Function</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-close-color-picker-popup">
  <div class="api-method-name">CloseColorPickerPopup([commit])</div>
  <p class="api-method-summary">Closes the color picker popup.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">commit <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-is-color-picker-popup-open">
  <div class="api-method-name">IsColorPickerPopupOpen()</div>
  <p class="api-method-summary">Returns whether the color picker popup is open.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-queue-overlay">
  <div class="api-method-name">QueueOverlay(owner_id, draw_fn, [rect], [owner_window])</div>
  <p class="api-method-summary">Queue an overlay draw callback. Overlays are drawn after all windows. <code>_draw_fn</code> is called as <code>function(_root)</code>. When <code>_rect</code> is supplied, Echo Chamber clips the overlay to that rectangle and consumes unhandled clicks inside it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">owner_id</span>
      <span class="api-argument-type">String|Real|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">draw_fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">rect <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct|Undefined</span>
      <span class="api-argument-description">Optional rectangle struct {x1,y1,x2,y2} for hit testing.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">owner_window <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|Undefined</span>
      <span class="api-argument-description">Optional owner window reference.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-open-context-menu">
  <div class="api-method-name">OpenContextMenu(items, x, y, owner_window, [style_key])</div>
  <p class="api-method-summary">Opens a context menu overlay at a screen position.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">items</span>
      <span class="api-argument-type">Array&lt;Struct&gt;</span>
      <span class="api-argument-description">Array of item structs: - { label:String, on_click:Function, enabled:Bool (optional), shortcut:String (optional), icon_sprite:Asset.GMSprite (optional), icon_image_index:Real (optional), icon_hover_sprite:Asset.GMSprite (optional), icon_hover_image_index:Real (optional) } - { is_separator:true } for separators</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">x</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">y</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">owner_window</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
      <span class="api-argument-description">Optional owning window reference.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">style_key <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Optional context menu style key.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-close-context-menu">
  <div class="api-method-name">CloseContextMenu()</div>
  <p class="api-method-summary">Closes the active context menu overlay (if open).</p>
</div>

<div class="api-method-entry" id="echo-chamber-root-is-context-menu-open">
  <div class="api-method-name">IsContextMenuOpen()</div>
  <p class="api-method-summary">Returns true if the context menu overlay is open.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-show-toast">
  <div class="api-method-name">ShowToast(text, [duration_ms])</div>
  <p class="api-method-summary">Shows a short non-blocking toast message.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">text</span>
      <span class="api-argument-type">String|Real|Bool</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">duration_ms <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Optional duration in milliseconds.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-copy-to-clipboard">
  <div class="api-method-name">CopyToClipboard(text, [toast_text], [duration_ms])</div>
  <p class="api-method-summary">Copies text to clipboard and show a toast confirmation.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">text</span>
      <span class="api-argument-type">String|Real|Bool|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">toast_text <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String|Real|Bool|Undefined</span>
      <span class="api-argument-description">Optional toast text (otherwise uses &quot;Copied: &lt;preview&gt;&quot;).</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">duration_ms <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Optional duration in milliseconds.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-focus-text-input">
  <div class="api-method-name">FocusTextInput(id, initial_text, placeholder, [commit_fn], [config])</div>
  <p class="api-method-summary">Focuses a text input by ID and sets its starting text. The optional _commit_fn runs with the final text when focus is lost. <code>_commit_fn</code> is called as <code>function(_final_text)</code> on blur unless the edit is cancelled.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">initial_text</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">placeholder</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">commit_fn <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Function|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">config <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-blur-text-input">
  <div class="api-method-name">BlurTextInput(id)</div>
  <p class="api-method-summary">Removes focus from a text input, commits its text, and returns the final string without submitting it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-submit-text-input">
  <div class="api-method-name">SubmitTextInput(id)</div>
  <p class="api-method-summary">Submits a focused text input, commits its text, runs OnSubmit, and returns the final string.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-cancel-text-input">
  <div class="api-method-name">CancelTextInput(id)</div>
  <p class="api-method-summary">Cancels editing, discards the current changes, and removes focus without committing or submitting.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-is-active-text-input">
  <div class="api-method-name">IsActiveTextInput(id)</div>
  <p class="api-method-summary">Returns true if the given ID is the currently focused text input.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-get-active-text">
  <div class="api-method-name">GetActiveText()</div>
  <p class="api-method-summary">Returns the current text while a text input is focused.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-get-text-buffer">
  <div class="api-method-name">GetTextBuffer()</div>
  <p class="api-method-summary">Returns the last committed text for the active text input.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-focus-control">
  <div class="api-method-name">FocusControl(id, rect)</div>
  <p class="api-method-summary">Give keyboard focus to a non-text control by ID. This focus is separate from text input focus.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">rect</span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">{x1,y1,x2,y2}</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-is-control-focused">
  <div class="api-method-name">IsControlFocused(id)</div>
  <p class="api-method-summary">Returns true if the given control ID currently owns keyboard focus (and no text input is active).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-root-blur-control-focus">
  <div class="api-method-name">BlurControlFocus(id)</div>
  <p class="api-method-summary">Clears keyboard focus from a control by ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

### EchoChamberScrollState
{: #echo-chamber-scroll-state .api-type-title }

Stores scroll position and drag state for a scrollable region.

```gml
new EchoChamberScrollState(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-chamber-scroll-state-set-scroll-y"><code>SetScrollY()</code></a></td><td>Sets the scroll offset in pixels.</td></tr>
<tr><td><a href="#echo-chamber-scroll-state-scroll-by"><code>ScrollBy()</code></a></td><td>Scroll by a delta in pixels (positive scrolls down).</td></tr>
<tr><td><a href="#echo-chamber-scroll-state-reset"><code>Reset()</code></a></td><td>Resets scroll to the top.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-scroll-state-set-scroll-y">
  <div class="api-method-name">SetScrollY(y)</div>
  <p class="api-method-summary">Sets the scroll offset in pixels.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">y</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-scroll-state">EchoChamberScrollState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-scroll-state-scroll-by">
  <div class="api-method-name">ScrollBy(dy)</div>
  <p class="api-method-summary">Scroll by a delta in pixels (positive scrolls down).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">dy</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-scroll-state">EchoChamberScrollState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-scroll-state-reset">
  <div class="api-method-name">Reset()</div>
  <p class="api-method-summary">Resets scroll to the top.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-scroll-state">EchoChamberScrollState</a></span>
    </div>
  </div>
</div>

### EchoChamberWindow
{: #echo-chamber-window .api-type-title }

Floating debug window that owns a collection of docked panels.

```gml
new EchoChamberWindow(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Identity, input, and theme</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-window-set-title"><code>SetTitle()</code></a></td><td>Sets the window title text.</td></tr>
<tr><td><a href="#echo-chamber-window-set-input-context"><code>SetInputContext()</code></a></td><td>Sets the input context ID used for this window. Pass <code>undefined</code> for <code>_context_id</code> to clear the window input context.</td></tr>
<tr><td><a href="#echo-chamber-window-swap-input-context"><code>SwapInputContext()</code></a></td><td>Swap the window input context and remove the old context if it is unused.</td></tr>
<tr><td><a href="#echo-chamber-window-set-style-key"><code>SetStyleKey()</code></a></td><td>Sets the generic main style key for this window.</td></tr>
<tr><td><a href="#echo-chamber-window-style"><code>Style()</code></a></td><td>Returns the style controls for this window&#x27;s body, header, and window buttons.</td></tr>
<tr><td><a href="#echo-chamber-window-set-style-key-header"><code>SetStyleKeyHeader()</code></a></td><td>Sets the header style key.</td></tr>
<tr><td><a href="#echo-chamber-window-set-style-key-chrome-button"><code>SetStyleKeyChromeButton()</code></a></td><td>Sets the chrome button style key for a specific chrome part.</td></tr>
<tr><td><a href="#echo-chamber-window-refresh-theme-override"><code>RefreshThemeOverride()</code></a></td><td>Reapply this window&#x27;s effective theme and dirty this window subtree&#x27;s style caches.</td></tr>
<tr><td><a href="#echo-chamber-window-mark-theme-dirty"><code>MarkThemeDirty()</code></a></td><td>Alias of RefreshThemeOverride().</td></tr>
<tr><td><a href="#echo-chamber-window-apply-theme"><code>ApplyTheme()</code></a></td><td>Apply a theme override to this window and its children (does not affect other windows).</td></tr>
<tr><td><a href="#echo-chamber-window-clear-theme-override"><code>ClearThemeOverride()</code></a></td><td>Clears the theme override for this window and reapply root defaults.</td></tr>
</tbody></table>

<div class="api-method-group-title">Visibility and lifecycle</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-window-set-visible"><code>SetVisible()</code></a></td><td>Shows or hides this window.</td></tr>
<tr><td><a href="#echo-chamber-window-on-close"><code>OnClose()</code></a></td><td>Sets a callback that runs when the window is closed via the close button.</td></tr>
<tr><td><a href="#echo-chamber-window-on-move"><code>OnMove()</code></a></td><td>Sets a callback that runs when the window position changes.</td></tr>
<tr><td><a href="#echo-chamber-window-on-resize"><code>OnResize()</code></a></td><td>Sets a callback that runs when the window size changes.</td></tr>
<tr><td><a href="#echo-chamber-window-on-show"><code>OnShow()</code></a></td><td>Sets a callback that runs when the window becomes visible.</td></tr>
<tr><td><a href="#echo-chamber-window-on-hide"><code>OnHide()</code></a></td><td>Sets a callback that runs when the window is hidden.</td></tr>
<tr><td><a href="#echo-chamber-window-on-focus"><code>OnFocus()</code></a></td><td>Sets a callback that runs when the window receives keyboard focus.</td></tr>
<tr><td><a href="#echo-chamber-window-on-blur"><code>OnBlur()</code></a></td><td>Sets a callback that runs when the window loses keyboard focus.</td></tr>
<tr><td><a href="#echo-chamber-window-on-minimize"><code>OnMinimize()</code></a></td><td>Sets a callback that runs when the window is minimized.</td></tr>
<tr><td><a href="#echo-chamber-window-on-restore"><code>OnRestore()</code></a></td><td>Sets a callback that runs when the window is restored from minimized state.</td></tr>
<tr><td><a href="#echo-chamber-window-close"><code>Close()</code></a></td><td>Closes the window (sets visible to false). If an on_close callback exists, it is called.</td></tr>
<tr><td><a href="#echo-chamber-window-set-pinned"><code>SetPinned()</code></a></td><td>Sets whether the window is pinned (disables dragging and resizing).</td></tr>
<tr><td><a href="#echo-chamber-window-toggle-pinned"><code>TogglePinned()</code></a></td><td>Toggles pinned state.</td></tr>
<tr><td><a href="#echo-chamber-window-set-minimized"><code>SetMinimized()</code></a></td><td>Sets whether the window is minimized (collapses content. only the title bar remains).</td></tr>
<tr><td><a href="#echo-chamber-window-toggle-minimized"><code>ToggleMinimized()</code></a></td><td>Toggles minimized state.</td></tr>
</tbody></table>

<div class="api-method-group-title">Geometry and layout</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-window-set-rect"><code>SetRect()</code></a></td><td>Sets the window rectangle in Echo Chamber canvas space. Size is clamped to min_width/min_height.</td></tr>
<tr><td><a href="#echo-chamber-window-set-position"><code>SetPosition()</code></a></td><td>Sets the window position without changing its size.</td></tr>
<tr><td><a href="#echo-chamber-window-get-width"><code>GetWidth()</code></a></td><td>Returns the current window width.</td></tr>
<tr><td><a href="#echo-chamber-window-get-height"><code>GetHeight()</code></a></td><td>Returns the current window height.</td></tr>
<tr><td><a href="#echo-chamber-window-set-min-size"><code>SetMinSize()</code></a></td><td>Sets minimum width and height for this window.</td></tr>
<tr><td><a href="#echo-chamber-window-set-max-size"><code>SetMaxSize()</code></a></td><td>Sets maximum width and height for this window (0 means no max).</td></tr>
<tr><td><a href="#echo-chamber-window-set-default-layout"><code>SetDefaultLayout()</code></a></td><td>Store the default layout used when this window layout is reset. Optional min values default to <code>1</code>. Optional max values default to <code>0</code>, meaning no maximum.</td></tr>
<tr><td><a href="#echo-chamber-window-reset-layout"><code>ResetLayout()</code></a></td><td>Resets this window to its stored default rectangle and sizing limits.</td></tr>
<tr><td><a href="#echo-chamber-window-set-auto-fit"><code>SetAutoFit()</code></a></td><td>Sets whether this window auto-fits to content after layout changes.</td></tr>
<tr><td><a href="#echo-chamber-window-fit-to-content"><code>FitToContent()</code></a></td><td>Resize this window to fit its panels&#x27; content.</td></tr>
</tbody></table>

<div class="api-method-group-title">Panels and controls</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-window-add-panel"><code>AddPanel()</code></a></td><td>Adds a top-level panel to this window.</td></tr>
<tr><td><a href="#echo-chamber-window-add-scrollable-panel-body"><code>AddScrollablePanelBody()</code></a></td><td>Adds a scrollable fill panel that contains the supplied child panels.</td></tr>
<tr><td><a href="#echo-chamber-window-remove-panel"><code>RemovePanel()</code></a></td><td>Removes a panel from this window (top-level or nested).</td></tr>
<tr><td><a href="#echo-chamber-window-clear-panels"><code>ClearPanels()</code></a></td><td>Removes all panels from this window.</td></tr>
<tr><td><a href="#echo-chamber-window-find-panel"><code>FindPanel()</code></a></td><td>Finds a panel by ID, including panels nested inside containers.</td></tr>
<tr><td><a href="#echo-chamber-window-find-control"><code>FindControl()</code></a></td><td>Finds a control in this window by ID (searches nested panels too).</td></tr>
<tr><td><a href="#echo-chamber-window-move-control-to-panel"><code>MoveControlToPanel()</code></a></td><td>Move a control to another panel in this window.</td></tr>
</tbody></table>

<div class="api-method-group-title">Interaction and drawing</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-window-contains-point"><code>ContainsPoint()</code></a></td><td>Returns true if a point is inside this window&#x27;s current rectangle (and the window is visible).</td></tr>
<tr><td><a href="#echo-chamber-window-begin-layout-batch"><code>BeginLayoutBatch()</code></a></td><td>Begin a layout batch (defers FitToContent calls until EndLayoutBatch).</td></tr>
<tr><td><a href="#echo-chamber-window-end-layout-batch"><code>EndLayoutBatch()</code></a></td><td>End a layout batch and apply any deferred FitToContent.</td></tr>
<tr><td><a href="#echo-chamber-window-process-window-interactions"><code>ProcessWindowInteractions()</code></a></td><td>Handles mouse interactions for dragging/resizing and chrome button clicks. Usually called by <code>RunDesktop()</code>.</td></tr>
<tr><td><a href="#echo-chamber-window-draw"><code>Draw()</code></a></td><td>Draws the window chrome and all owned panels. Usually called by <code>RunDesktop()</code>.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-window-set-title">
  <div class="api-method-name">SetTitle(title)</div>
  <p class="api-method-summary">Sets the window title text.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">title</span>
      <span class="api-argument-type">String|Real|Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-set-input-context">
  <div class="api-method-name">SetInputContext(context_id, [parent_id])</div>
  <p class="api-method-summary">Sets the input context ID used for this window. Pass <code>undefined</code> for <code>_context_id</code> to clear the window input context.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">context_id</span>
      <span class="api-argument-type">String|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">parent_id <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-swap-input-context">
  <div class="api-method-name">SwapInputContext(context_id, [parent_id])</div>
  <p class="api-method-summary">Swap the window input context and remove the old context if it is unused.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">context_id</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">parent_id <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-set-style-key">
  <div class="api-method-name">SetStyleKey(key)</div>
  <p class="api-method-summary">Sets the generic main style key for this window.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-style">
  <div class="api-method-name">Style()</div>
  <p class="api-method-summary">Returns the style controls for this window&#x27;s body, header, and window buttons.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.EchoWindowStyleSurface</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-set-style-key-header">
  <div class="api-method-name">SetStyleKeyHeader(key)</div>
  <p class="api-method-summary">Sets the header style key.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-set-style-key-chrome-button">
  <div class="api-method-name">SetStyleKeyChromeButton(part, key)</div>
  <p class="api-method-summary">Sets the chrome button style key for a specific chrome part.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">part</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-echo-chamber-chrome-button-slot"><code>eEchoChamberChromeButtonSlot</code></a> enum.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-refresh-theme-override">
  <div class="api-method-name">RefreshThemeOverride()</div>
  <p class="api-method-summary">Reapply this window&#x27;s effective theme and dirty this window subtree&#x27;s style caches.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-mark-theme-dirty">
  <div class="api-method-name">MarkThemeDirty()</div>
  <p class="api-method-summary">Alias of RefreshThemeOverride().</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-apply-theme">
  <div class="api-method-name">ApplyTheme(theme)</div>
  <p class="api-method-summary">Apply a theme override to this window and its children (does not affect other windows).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">theme</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-theme">EchoChamberTheme</a>|Undefined</span>
      <span class="api-argument-description">Pass undefined to clear the override.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-clear-theme-override">
  <div class="api-method-name">ClearThemeOverride()</div>
  <p class="api-method-summary">Clears the theme override for this window and reapply root defaults.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-set-visible">
  <div class="api-method-name">SetVisible(flag)</div>
  <p class="api-method-summary">Shows or hides this window.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-on-close">
  <div class="api-method-name">OnClose(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when the window is closed via the close button.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-on-move">
  <div class="api-method-name">OnMove(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when the window position changes.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-on-resize">
  <div class="api-method-name">OnResize(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when the window size changes.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-on-show">
  <div class="api-method-name">OnShow(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when the window becomes visible.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-on-hide">
  <div class="api-method-name">OnHide(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when the window is hidden.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-on-focus">
  <div class="api-method-name">OnFocus(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when the window receives keyboard focus.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-on-blur">
  <div class="api-method-name">OnBlur(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when the window loses keyboard focus.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-on-minimize">
  <div class="api-method-name">OnMinimize(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when the window is minimized.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-on-restore">
  <div class="api-method-name">OnRestore(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when the window is restored from minimized state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-close">
  <div class="api-method-name">Close()</div>
  <p class="api-method-summary">Closes the window (sets visible to false). If an on_close callback exists, it is called.</p>
</div>

<div class="api-method-entry" id="echo-chamber-window-set-pinned">
  <div class="api-method-name">SetPinned(flag)</div>
  <p class="api-method-summary">Sets whether the window is pinned (disables dragging and resizing).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-toggle-pinned">
  <div class="api-method-name">TogglePinned()</div>
  <p class="api-method-summary">Toggles pinned state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-set-minimized">
  <div class="api-method-name">SetMinimized(flag)</div>
  <p class="api-method-summary">Sets whether the window is minimized (collapses content. only the title bar remains).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-toggle-minimized">
  <div class="api-method-name">ToggleMinimized()</div>
  <p class="api-method-summary">Toggles minimized state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-set-rect">
  <div class="api-method-name">SetRect(x1, y1, x2, y2)</div>
  <p class="api-method-summary">Sets the window rectangle in Echo Chamber canvas space. Size is clamped to min_width/min_height.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">x1</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">y1</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">x2</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">y2</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-set-position">
  <div class="api-method-name">SetPosition(x, y)</div>
  <p class="api-method-summary">Sets the window position without changing its size.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">x</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">y</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-get-width">
  <div class="api-method-name">GetWidth()</div>
  <p class="api-method-summary">Returns the current window width.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-get-height">
  <div class="api-method-name">GetHeight()</div>
  <p class="api-method-summary">Returns the current window height.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-set-min-size">
  <div class="api-method-name">SetMinSize(w, h)</div>
  <p class="api-method-summary">Sets minimum width and height for this window.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">w</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">h</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-set-max-size">
  <div class="api-method-name">SetMaxSize(w, h)</div>
  <p class="api-method-summary">Sets maximum width and height for this window (0 means no max).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">w</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">h</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-set-default-layout">
  <div class="api-method-name">SetDefaultLayout(x1, y1, x2, y2, [min_w], [min_h], [max_w], [max_h])</div>
  <p class="api-method-summary">Store the default layout used when this window layout is reset. Optional min values default to <code>1</code>. Optional max values default to <code>0</code>, meaning no maximum.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">x1</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">y1</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">x2</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">y2</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">min_w <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">min_h <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">max_w <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">max_h <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-reset-layout">
  <div class="api-method-name">ResetLayout()</div>
  <p class="api-method-summary">Resets this window to its stored default rectangle and sizing limits.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-add-panel">
  <div class="api-method-name">AddPanel(panel)</div>
  <p class="api-method-summary">Adds a top-level panel to this window.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">panel</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-add-scrollable-panel-body">
  <div class="api-method-name">AddScrollablePanelBody(id, panels)</div>
  <p class="api-method-summary">Adds a scrollable fill panel that contains the supplied child panels.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">panels</span>
      <span class="api-argument-type">Array&lt;Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a>&gt;</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-remove-panel">
  <div class="api-method-name">RemovePanel(panel_or_id)</div>
  <p class="api-method-summary">Removes a panel from this window (top-level or nested).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">panel_or_id</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a>|String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-clear-panels">
  <div class="api-method-name">ClearPanels()</div>
  <p class="api-method-summary">Removes all panels from this window.</p>
</div>

<div class="api-method-entry" id="echo-chamber-window-find-panel">
  <div class="api-method-name">FindPanel(id)</div>
  <p class="api-method-summary">Finds a panel by ID, including panels nested inside containers.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-find-control">
  <div class="api-method-name">FindControl(id)</div>
  <p class="api-method-summary">Finds a control in this window by ID (searches nested panels too).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-move-control-to-panel">
  <div class="api-method-name">MoveControlToPanel(control_or_id, panel_or_id, [index])</div>
  <p class="api-method-summary">Move a control to another panel in this window.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">control_or_id</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a>|String|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">panel_or_id</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a>|String|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">index <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-contains-point">
  <div class="api-method-name">ContainsPoint(x, y)</div>
  <p class="api-method-summary">Returns true if a point is inside this window&#x27;s current rectangle (and the window is visible).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">x</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">y</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-begin-layout-batch">
  <div class="api-method-name">BeginLayoutBatch()</div>
  <p class="api-method-summary">Begin a layout batch (defers FitToContent calls until EndLayoutBatch).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-end-layout-batch">
  <div class="api-method-name">EndLayoutBatch()</div>
  <p class="api-method-summary">End a layout batch and apply any deferred FitToContent.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-set-auto-fit">
  <div class="api-method-name">SetAutoFit(flag)</div>
  <p class="api-method-summary">Sets whether this window auto-fits to content after layout changes.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-fit-to-content">
  <div class="api-method-name">FitToContent([root])</div>
  <p class="api-method-summary">Resize this window to fit its panels&#x27; content.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">root <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a>|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-process-window-interactions">
  <div class="api-method-name">ProcessWindowInteractions(root)</div>
  <p class="api-method-summary">Handles mouse interactions for dragging/resizing and chrome button clicks. Usually called by <code>RunDesktop()</code>.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-window-draw">
  <div class="api-method-name">Draw(root)</div>
  <p class="api-method-summary">Draws the window chrome and all owned panels. Usually called by <code>RunDesktop()</code>.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

### EchoChamberPanel
{: #echo-chamber-panel .api-type-title }

Layout panel docked to an edge or fill.

```gml
new EchoChamberPanel(id, dock)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">dock</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-dock"><code>eEchoChamberDock</code></a> enum.</span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Style and content</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-panel-set-style-key"><code>SetStyleKey()</code></a></td><td>Sets the generic main style key for this panel.</td></tr>
<tr><td><a href="#echo-chamber-panel-style"><code>Style()</code></a></td><td>Returns this panel&#x27;s local override style object, creating it if needed. Returns a local panel style override. Use this for one panel only. Use theme style families for shared styling. Use a panel-local override for one panel; use the theme style family when the style should be shared.</td></tr>
<tr><td><a href="#echo-chamber-panel-label-style"><code>LabelStyle()</code></a></td><td>Returns this panel&#x27;s local label override style object, creating it if needed. Returns the default label style override used by controls inside this panel.</td></tr>
<tr><td><a href="#echo-chamber-panel-set-content-drawer"><code>SetContentDrawer()</code></a></td><td>Sets a custom content drawer for this panel. Echo Chamber calls the function after normal controls are drawn and clips it to the panel content rectangle. The callback is stored only when <code>_fn</code> is callable.</td></tr>
<tr><td><a href="#echo-chamber-panel-get-thickness"><code>GetThickness()</code></a></td><td>Returns panel thickness based on collapsed state.</td></tr>
</tbody></table>

<div class="api-method-group-title">Controls</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-panel-add-control"><code>AddControl()</code></a></td><td>Adds a direct control to this panel. Rejected while the panel contains child panels. Assigns owner pointers and appends the control when the argument is a valid Echo Chamber control. Panels use mutually exclusive content modes: if the panel already contains child panels, the add is rejected with an Echo Chamber warning and returns <code>undefined</code>.</td></tr>
<tr><td><a href="#echo-chamber-panel-insert-control"><code>InsertControl()</code></a></td><td>Insert a direct control at a specific index (clamped). Rejected while the panel contains child panels. Inserts a direct control at a clamped index. Index <code>0</code> means the first direct control. Like <code>AddControl()</code>, insertion is rejected while the panel contains child panels.</td></tr>
<tr><td><a href="#echo-chamber-panel-move-control"><code>MoveControl()</code></a></td><td>Reorder a direct control to a specific index (clamped). Reorders a direct child control only. Use <code>MoveControlToPanel()</code> for nested moves or cross-panel moves.</td></tr>
<tr><td><a href="#echo-chamber-panel-move-control-to-panel"><code>MoveControlToPanel()</code></a></td><td>Move a control to another panel (direct or nested in this panel). Searches direct and nested controls under this panel, then moves the found control into <code>_target_panel</code>. If the target contains child panels, the move is rejected before the source control is removed.</td></tr>
<tr><td><a href="#echo-chamber-panel-set-control-order"><code>SetControlOrder()</code></a></td><td>Reorder direct controls using a list of ids (unlisted items keep their relative order at the end).</td></tr>
<tr><td><a href="#echo-chamber-panel-remove-control"><code>RemoveControl()</code></a></td><td>Removes a control from this panel (direct or nested). Searches direct and nested controls. Removing a control clears ownership and related root state such as focus, tooltip, and overlay ownership.</td></tr>
<tr><td><a href="#echo-chamber-panel-clear-controls"><code>ClearControls()</code></a></td><td>Removes all direct controls from this panel. Removes only direct controls. Child panel contents are untouched.</td></tr>
<tr><td><a href="#echo-chamber-panel-find-control"><code>FindControl()</code></a></td><td>Finds a direct or nested control within this panel by ID. Searches direct controls first, then controls inside nested child panels.</td></tr>
</tbody></table>

<div class="api-method-group-title">Child panels</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-panel-add-child-panel"><code>AddChildPanel()</code></a></td><td>Adds a child panel. Rejected while the panel contains direct controls. A successful add marks the panel as a container. If direct controls are already present, Echo Chamber warns, rejects the add, and returns undefined.</td></tr>
<tr><td><a href="#echo-chamber-panel-remove-child-panel"><code>RemoveChildPanel()</code></a></td><td>Removes a child panel from this panel (direct or nested). Searches direct and nested child panels, then detaches the found panel tree.</td></tr>
<tr><td><a href="#echo-chamber-panel-clear-child-panels"><code>ClearChildPanels()</code></a></td><td>Removes all child panels from this panel. Removes direct child panels and clears their ownership pointers.</td></tr>
</tbody></table>

<div class="api-method-group-title">Layout and sizing</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-panel-set-active"><code>SetActive()</code></a></td><td>Enables or disables this panel&#x27;s participation in layout, drawing, and input.</td></tr>
<tr><td><a href="#echo-chamber-panel-set-size-mode"><code>SetSizeMode()</code></a></td><td>Configure how this panel resolves its dock size.</td></tr>
<tr><td><a href="#echo-chamber-panel-set-size"><code>SetSize()</code></a></td><td>Sets dock thickness when using fixed sizing.</td></tr>
<tr><td><a href="#echo-chamber-panel-set-flow-mode"><code>SetFlowMode()</code></a></td><td>Sets how child controls flow within the panel. <code>ROW</code> wraps controls across rows. <code>COLUMN</code> stacks controls vertically.</td></tr>
<tr><td><a href="#echo-chamber-panel-set-row-align"><code>SetRowAlign()</code></a></td><td>Sets how packed direct controls are aligned inside a ROW panel. Applies to packed rows only. It controls where a row sits when it doesn&#x27;t fill the available width.</td></tr>
<tr><td><a href="#echo-chamber-panel-set-row-vertical-align"><code>SetRowVerticalAlign()</code></a></td><td>Sets how direct controls are aligned vertically inside each ROW panel row.</td></tr>
<tr><td><a href="#echo-chamber-panel-set-row-distribution"><code>SetRowDistribution()</code></a></td><td>Sets how direct controls consume available width in a ROW panel. <code>PACK</code> keeps controls at desired widths. <code>FILL</code> distributes available row width to fill-width controls.</td></tr>
<tr><td><a href="#echo-chamber-panel-set-min-size"><code>SetMinSize()</code></a></td><td>Sets minimum dock thickness when using fit-to-content.</td></tr>
<tr><td><a href="#echo-chamber-panel-set-max-size"><code>SetMaxSize()</code></a></td><td>Sets maximum dock thickness when using fit-to-content.</td></tr>
</tbody></table>

<div class="api-method-group-title">Scrolling</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-panel-set-scrollable"><code>SetScrollable()</code></a></td><td>Sets whether this panel scrolls its contents vertically when content overflows. Scrollable panels require either an assigned <a href="#echo-chamber-scroll-state"><code>EchoChamberScrollState</code></a> or the internal state created by the panel.</td></tr>
<tr><td><a href="#echo-chamber-panel-set-scroll-state"><code>SetScrollState()</code></a></td><td>Sets a scroll state for this panel (used when scrollable). Assigns this panel&#x27;s scroll state. <code>SetScrollable(true)</code> creates an internal scroll state automatically when the panel doesn&#x27;t already have one.</td></tr>
</tbody></table>

<div class="api-method-group-title">Labels and collapse</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-panel-set-label-placement"><code>SetLabelPlacement()</code></a></td><td>Sets the default label placement for controls in this panel. This is the default label placement for child controls. Individual controls can override it.</td></tr>
<tr><td><a href="#echo-chamber-panel-set-label-gap"><code>SetLabelGap()</code></a></td><td>Sets the default label gap for this panel.</td></tr>
<tr><td><a href="#echo-chamber-panel-set-label-width"><code>SetLabelWidth()</code></a></td><td>Sets the default label column width for this panel (-1 uses auto width).</td></tr>
<tr><td><a href="#echo-chamber-panel-set-label-width-clamp"><code>SetLabelWidthClamp()</code></a></td><td>Sets min/max clamp values for the auto label column width. The clamp applies to auto label column width. If <code>_max_px</code> is omitted, Echo Chamber uses <code>_min_px</code> for both limits, so the automatic label width is fixed to that clamped value.</td></tr>
<tr><td><a href="#echo-chamber-panel-set-style-key-label"><code>SetStyleKeyLabel()</code></a></td><td>Sets the panel default label style key.</td></tr>
<tr><td><a href="#echo-chamber-panel-set-collapse-mode"><code>SetCollapseMode()</code></a></td><td>Sets the panel collapse mode. <code>NONE</code> disables the collapse handle. Directional modes decide which edge the panel collapses toward.</td></tr>
<tr><td><a href="#echo-chamber-panel-set-collapsed"><code>SetCollapsed()</code></a></td><td>Sets whether this panel is collapsed.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-panel-set-style-key">
  <div class="api-method-name">SetStyleKey(key)</div>
  <p class="api-method-summary">Sets the generic main style key for this panel.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-style">
  <div class="api-method-name">Style()</div>
  <p class="api-method-summary">Returns this panel&#x27;s local override style object, creating it if needed. Returns a local panel style override. Use this for one panel only. Use theme style families for shared styling. Use a panel-local override for one panel; use the theme style family when the style should be shared.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.EchoPanelStyle</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-label-style">
  <div class="api-method-name">LabelStyle()</div>
  <p class="api-method-summary">Returns this panel&#x27;s local label override style object, creating it if needed. Returns the default label style override used by controls inside this panel.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.EchoLabelStyle</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-add-control">
  <div class="api-method-name">AddControl(control)</div>
  <p class="api-method-summary">Adds a direct control to this panel. Rejected while the panel contains child panels. Assigns owner pointers and appends the control when the argument is a valid Echo Chamber control. Panels use mutually exclusive content modes: if the panel already contains child panels, the add is rejected with an Echo Chamber warning and returns <code>undefined</code>.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">control</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-insert-control">
  <div class="api-method-name">InsertControl(control, index)</div>
  <p class="api-method-summary">Insert a direct control at a specific index (clamped). Rejected while the panel contains child panels. Inserts a direct control at a clamped index. Index <code>0</code> means the first direct control. Like <code>AddControl()</code>, insertion is rejected while the panel contains child panels.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">control</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">index</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-move-control">
  <div class="api-method-name">MoveControl(control_or_id, index)</div>
  <p class="api-method-summary">Reorder a direct control to a specific index (clamped). Reorders a direct child control only. Use <code>MoveControlToPanel()</code> for nested moves or cross-panel moves.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">control_or_id</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a>|String|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">index</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-move-control-to-panel">
  <div class="api-method-name">MoveControlToPanel(control_or_id, target_panel, [index])</div>
  <p class="api-method-summary">Move a control to another panel (direct or nested in this panel). Searches direct and nested controls under this panel, then moves the found control into <code>_target_panel</code>. If the target contains child panels, the move is rejected before the source control is removed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">control_or_id</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a>|String|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">target_panel</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">index <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-control-order">
  <div class="api-method-name">SetControlOrder(ids)</div>
  <p class="api-method-summary">Reorder direct controls using a list of ids (unlisted items keep their relative order at the end).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ids</span>
      <span class="api-argument-type">Array&lt;Any&gt;</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-remove-control">
  <div class="api-method-name">RemoveControl(control_or_id)</div>
  <p class="api-method-summary">Removes a control from this panel (direct or nested). Searches direct and nested controls. Removing a control clears ownership and related root state such as focus, tooltip, and overlay ownership.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">control_or_id</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a>|String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-clear-controls">
  <div class="api-method-name">ClearControls()</div>
  <p class="api-method-summary">Removes all direct controls from this panel. Removes only direct controls. Child panel contents are untouched.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-add-child-panel">
  <div class="api-method-name">AddChildPanel(panel)</div>
  <p class="api-method-summary">Adds a child panel. Rejected while the panel contains direct controls. A successful add marks the panel as a container. If direct controls are already present, Echo Chamber warns, rejects the add, and returns undefined.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">panel</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-remove-child-panel">
  <div class="api-method-name">RemoveChildPanel(panel_or_id)</div>
  <p class="api-method-summary">Removes a child panel from this panel (direct or nested). Searches direct and nested child panels, then detaches the found panel tree.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">panel_or_id</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a>|String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-clear-child-panels">
  <div class="api-method-name">ClearChildPanels()</div>
  <p class="api-method-summary">Removes all child panels from this panel. Removes direct child panels and clears their ownership pointers.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-find-control">
  <div class="api-method-name">FindControl(id)</div>
  <p class="api-method-summary">Finds a direct or nested control within this panel by ID. Searches direct controls first, then controls inside nested child panels.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-active">
  <div class="api-method-name">SetActive(flag)</div>
  <p class="api-method-summary">Enables or disables this panel&#x27;s participation in layout, drawing, and input.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-size-mode">
  <div class="api-method-name">SetSizeMode(mode)</div>
  <p class="api-method-summary">Configure how this panel resolves its dock size.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">mode</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-panel-size-mode"><code>eEchoChamberPanelSizeMode</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-size">
  <div class="api-method-name">SetSize(value)</div>
  <p class="api-method-summary">Sets dock thickness when using fixed sizing.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">value</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-flow-mode">
  <div class="api-method-name">SetFlowMode(flow_mode)</div>
  <p class="api-method-summary">Sets how child controls flow within the panel. <code>ROW</code> wraps controls across rows. <code>COLUMN</code> stacks controls vertically.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flow_mode</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-panel-flow"><code>eEchoChamberPanelFlow</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-row-align">
  <div class="api-method-name">SetRowAlign(align)</div>
  <p class="api-method-summary">Sets how packed direct controls are aligned inside a ROW panel. Applies to packed rows only. It controls where a row sits when it doesn&#x27;t fill the available width.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">align</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-panel-row-align"><code>eEchoChamberPanelRowAlign</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-row-vertical-align">
  <div class="api-method-name">SetRowVerticalAlign(align)</div>
  <p class="api-method-summary">Sets how direct controls are aligned vertically inside each ROW panel row.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">align</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-align-ver"><code>eEchoChamberAlignVer</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-row-distribution">
  <div class="api-method-name">SetRowDistribution(distribution)</div>
  <p class="api-method-summary">Sets how direct controls consume available width in a ROW panel. <code>PACK</code> keeps controls at desired widths. <code>FILL</code> distributes available row width to fill-width controls.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">distribution</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-panel-row-distribution"><code>eEchoChamberPanelRowDistribution</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-scrollable">
  <div class="api-method-name">SetScrollable(flag)</div>
  <p class="api-method-summary">Sets whether this panel scrolls its contents vertically when content overflows. Scrollable panels require either an assigned <a href="#echo-chamber-scroll-state"><code>EchoChamberScrollState</code></a> or the internal state created by the panel.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-scroll-state">
  <div class="api-method-name">SetScrollState(state)</div>
  <p class="api-method-summary">Sets a scroll state for this panel (used when scrollable). Assigns this panel&#x27;s scroll state. <code>SetScrollable(true)</code> creates an internal scroll state automatically when the panel doesn&#x27;t already have one.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">state</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-scroll-state">EchoChamberScrollState</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-label-placement">
  <div class="api-method-name">SetLabelPlacement(placement)</div>
  <p class="api-method-summary">Sets the default label placement for controls in this panel. This is the default label placement for child controls. Individual controls can override it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">placement</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-label-placement"><code>eEchoChamberLabelPlacement</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-label-gap">
  <div class="api-method-name">SetLabelGap(px)</div>
  <p class="api-method-summary">Sets the default label gap for this panel.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">px</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-label-width">
  <div class="api-method-name">SetLabelWidth(px)</div>
  <p class="api-method-summary">Sets the default label column width for this panel (-1 uses auto width).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">px</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-label-width-clamp">
  <div class="api-method-name">SetLabelWidthClamp(min_px, [max_px])</div>
  <p class="api-method-summary">Sets min/max clamp values for the auto label column width. The clamp applies to auto label column width. If <code>_max_px</code> is omitted, Echo Chamber uses <code>_min_px</code> for both limits, so the automatic label width is fixed to that clamped value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">min_px</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">max_px <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-style-key-label">
  <div class="api-method-name">SetStyleKeyLabel(key)</div>
  <p class="api-method-summary">Sets the panel default label style key.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-collapse-mode">
  <div class="api-method-name">SetCollapseMode(mode)</div>
  <p class="api-method-summary">Sets the panel collapse mode. <code>NONE</code> disables the collapse handle. Directional modes decide which edge the panel collapses toward.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">mode</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-collapse"><code>eEchoChamberCollapse</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-collapsed">
  <div class="api-method-name">SetCollapsed(value)</div>
  <p class="api-method-summary">Sets whether this panel is collapsed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">value</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-min-size">
  <div class="api-method-name">SetMinSize(value)</div>
  <p class="api-method-summary">Sets minimum dock thickness when using fit-to-content.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">value</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-max-size">
  <div class="api-method-name">SetMaxSize(value)</div>
  <p class="api-method-summary">Sets maximum dock thickness when using fit-to-content.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">value</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-set-content-drawer">
  <div class="api-method-name">SetContentDrawer(fn)</div>
  <p class="api-method-summary">Sets a custom content drawer for this panel. Echo Chamber calls the function after normal controls are drawn and clips it to the panel content rectangle. The callback is stored only when <code>_fn</code> is callable.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-panel-get-thickness">
  <div class="api-method-name">GetThickness()</div>
  <p class="api-method-summary">Returns panel thickness based on collapsed state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

## Controls

### EchoChamberControlBase
{: #echo-chamber-control-base .api-type-title }

Base type shared by all Echo Chamber controls.

```gml
new EchoChamberControlBase(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Hierarchy and style</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-control-base-get-root"><code>GetRoot()</code></a></td><td>Returns the owning root for this control (if attached). Returns <code>undefined</code> until the control is attached to a root or window.</td></tr>
<tr><td><a href="#echo-chamber-control-base-get-window"><code>GetWindow()</code></a></td><td>Returns the owning window for this control (if attached).</td></tr>
<tr><td><a href="#echo-chamber-control-base-get-panel"><code>GetPanel()</code></a></td><td>Returns the owning panel for this control (if attached).</td></tr>
<tr><td><a href="#echo-chamber-control-base-set-style-key"><code>SetStyleKey()</code></a></td><td>Sets the generic style key for this control.</td></tr>
<tr><td><a href="#echo-chamber-control-base-style"><code>Style()</code></a></td><td>Returns this control&#x27;s local override style object, creating it if needed. The returned override is local to this control; use theme style families for shared styling.</td></tr>
</tbody></table>

<div class="api-method-group-title">Sizing</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-control-base-set-preferred-width"><code>SetPreferredWidth()</code></a></td><td>Sets a preferred pixel width for this control when arranged in a row panel.</td></tr>
<tr><td><a href="#echo-chamber-control-base-set-preferred-height"><code>SetPreferredHeight()</code></a></td><td>Sets a preferred pixel height for this control.</td></tr>
<tr><td><a href="#echo-chamber-control-base-set-fill-width"><code>SetFillWidth()</code></a></td><td>Sets whether this control fills the available row width.</td></tr>
</tbody></table>

<div class="api-method-group-title">Caption and labels</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-control-base-set-caption"><code>SetCaption()</code></a></td><td>Sets the control caption (drawn by controls that have built-in captions).</td></tr>
<tr><td><a href="#echo-chamber-control-base-set-label"><code>SetLabel()</code></a></td><td>Sets the panel-drawn label text for this control.</td></tr>
<tr><td><a href="#echo-chamber-control-base-set-label-placement"><code>SetLabelPlacement()</code></a></td><td>Sets where this control&#x27;s label is drawn.</td></tr>
<tr><td><a href="#echo-chamber-control-base-set-label-gap"><code>SetLabelGap()</code></a></td><td>Sets label spacing from the control body in pixels (-1 uses panel/theme defaults).</td></tr>
<tr><td><a href="#echo-chamber-control-base-set-label-width"><code>SetLabelWidth()</code></a></td><td>Sets label width in pixels for leading labels (-1 uses panel/theme defaults).</td></tr>
<tr><td><a href="#echo-chamber-control-base-set-label-auto-min-control-width"><code>SetLabelAutoMinControlWidth()</code></a></td><td>Sets the minimum body width required before AUTO labels stay leading (-1 uses panel/theme defaults).</td></tr>
<tr><td><a href="#echo-chamber-control-base-set-style-key-label"><code>SetStyleKeyLabel()</code></a></td><td>Sets the label style key (looked up in theme.label_styles).</td></tr>
<tr><td><a href="#echo-chamber-control-base-set-label-align"><code>SetLabelAlign()</code></a></td><td>Sets label alignment override.</td></tr>
<tr><td><a href="#echo-chamber-control-base-set-label-enabled"><code>SetLabelEnabled()</code></a></td><td>Enables or disables panel-drawn labels for this control.</td></tr>
</tbody></table>

<div class="api-method-group-title">State and drawing</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-control-base-set-tooltip"><code>SetTooltip()</code></a></td><td>Sets the control tooltip (shown on hover when supported).</td></tr>
<tr><td><a href="#echo-chamber-control-base-set-visible"><code>SetVisible()</code></a></td><td>Shows or hides this control.</td></tr>
<tr><td><a href="#echo-chamber-control-base-set-enabled"><code>SetEnabled()</code></a></td><td>Enables or disables this control (disabled controls should not accept input).</td></tr>
<tr><td><a href="#echo-chamber-control-base-draw-manual"><code>DrawManual()</code></a></td><td>Draws this control manually inside the given rectangle. Draws a control outside normal panel layout. Pass the root and panel context that should own input, theme, tooltip, and focus behavior for the manual draw.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-control-base-get-root">
  <div class="api-method-name">GetRoot()</div>
  <p class="api-method-summary">Returns the owning root for this control (if attached). Returns <code>undefined</code> until the control is attached to a root or window.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-get-window">
  <div class="api-method-name">GetWindow()</div>
  <p class="api-method-summary">Returns the owning window for this control (if attached).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-get-panel">
  <div class="api-method-name">GetPanel()</div>
  <p class="api-method-summary">Returns the owning panel for this control (if attached).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-set-style-key">
  <div class="api-method-name">SetStyleKey(key)</div>
  <p class="api-method-summary">Sets the generic style key for this control.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-style">
  <div class="api-method-name">Style()</div>
  <p class="api-method-summary">Returns this control&#x27;s local override style object, creating it if needed. The returned override is local to this control; use theme style families for shared styling.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.EchoTextBlockStyle|Struct.EchoButtonStyle|Struct.EchoSliderStyle|Struct.EchoToggleStyle|Struct.EchoTextInputStyle|Struct.EchoSeparatorStyle|Struct.EchoListRowStyle|Struct.EchoDropdownStyle|Struct.EchoColorButtonStyle</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-set-preferred-width">
  <div class="api-method-name">SetPreferredWidth(width)</div>
  <p class="api-method-summary">Sets a preferred pixel width for this control when arranged in a row panel.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">width</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-set-preferred-height">
  <div class="api-method-name">SetPreferredHeight(height)</div>
  <p class="api-method-summary">Sets a preferred pixel height for this control.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">height</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-set-fill-width">
  <div class="api-method-name">SetFillWidth(flag)</div>
  <p class="api-method-summary">Sets whether this control fills the available row width.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-set-caption">
  <div class="api-method-name">SetCaption(text)</div>
  <p class="api-method-summary">Sets the control caption (drawn by controls that have built-in captions).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">text</span>
      <span class="api-argument-type">String|Real|Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-set-label">
  <div class="api-method-name">SetLabel(text)</div>
  <p class="api-method-summary">Sets the panel-drawn label text for this control.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">text</span>
      <span class="api-argument-type">String|Real|Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-set-label-placement">
  <div class="api-method-name">SetLabelPlacement(placement)</div>
  <p class="api-method-summary">Sets where this control&#x27;s label is drawn.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">placement</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-label-placement"><code>eEchoChamberLabelPlacement</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-set-label-gap">
  <div class="api-method-name">SetLabelGap(px)</div>
  <p class="api-method-summary">Sets label spacing from the control body in pixels (-1 uses panel/theme defaults).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">px</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-set-label-width">
  <div class="api-method-name">SetLabelWidth(px)</div>
  <p class="api-method-summary">Sets label width in pixels for leading labels (-1 uses panel/theme defaults).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">px</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-set-label-auto-min-control-width">
  <div class="api-method-name">SetLabelAutoMinControlWidth(px)</div>
  <p class="api-method-summary">Sets the minimum body width required before AUTO labels stay leading (-1 uses panel/theme defaults).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">px</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-set-style-key-label">
  <div class="api-method-name">SetStyleKeyLabel(key)</div>
  <p class="api-method-summary">Sets the label style key (looked up in theme.label_styles).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-set-label-align">
  <div class="api-method-name">SetLabelAlign(align)</div>
  <p class="api-method-summary">Sets label alignment override.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">align</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-label-align"><code>eEchoChamberLabelAlign</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-set-label-enabled">
  <div class="api-method-name">SetLabelEnabled(flag)</div>
  <p class="api-method-summary">Enables or disables panel-drawn labels for this control.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-set-tooltip">
  <div class="api-method-name">SetTooltip(text)</div>
  <p class="api-method-summary">Sets the control tooltip (shown on hover when supported).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">text</span>
      <span class="api-argument-type">String|Real|Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-set-visible">
  <div class="api-method-name">SetVisible(flag)</div>
  <p class="api-method-summary">Shows or hides this control.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-set-enabled">
  <div class="api-method-name">SetEnabled(flag)</div>
  <p class="api-method-summary">Enables or disables this control (disabled controls should not accept input).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-control-base-draw-manual">
  <div class="api-method-name">DrawManual(root, panel, rect)</div>
  <p class="api-method-summary">Draws this control manually inside the given rectangle. Draws a control outside normal panel layout. Pass the root and panel context that should own input, theme, tooltip, and focus behavior for the manual draw.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">panel</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-panel">EchoChamberPanel</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">rect</span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">{x1,y1,x2,y2}</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-control-base">EchoChamberControlBase</a></span>
    </div>
  </div>
</div>

### EchoChamberTextBlock
{: #echo-chamber-text-block .api-type-title }

Non-interactive text block.

Inherits from [`EchoChamberControlBase`](#echo-chamber-control-base).

```gml
new EchoChamberTextBlock(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-chamber-text-block-set-text"><code>SetText()</code></a></td><td>Sets the text block text.</td></tr>
<tr><td><a href="#echo-chamber-text-block-bind-text"><code>BindText()</code></a></td><td>Binds the text block text to a field binding, struct field, or getter function. If <code>_source</code> is callable, it&#x27;s used as the getter. If <code>_source</code> is a struct, <code>_key_or_fn</code> is converted to the field key. A field binding resolves its target dynamically.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-text-block-set-text">
  <div class="api-method-name">SetText(text)</div>
  <p class="api-method-summary">Sets the text block text.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">text</span>
      <span class="api-argument-type">String|Real|Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-block">EchoChamberTextBlock</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-block-bind-text">
  <div class="api-method-name">BindText(source, [key_or_fn])</div>
  <p class="api-method-summary">Binds the text block text to a field binding, struct field, or getter function. If <code>_source</code> is callable, it&#x27;s used as the getter. If <code>_source</code> is a struct, <code>_key_or_fn</code> is converted to the field key. A field binding resolves its target dynamically.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-field-binding">EchoChamberFieldBinding</a>|Struct|Function</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key_or_fn <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String|Function|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-block">EchoChamberTextBlock</a></span>
    </div>
  </div>
</div>

### EchoChamberButton
{: #echo-chamber-button .api-type-title }

Clickable button.

Inherits from [`EchoChamberControlBase`](#echo-chamber-control-base).

```gml
new EchoChamberButton(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-chamber-button-on-click"><code>OnClick()</code></a></td><td>Sets a callback to run when the button is activated (click or Enter while focused).</td></tr>
<tr><td><a href="#echo-chamber-button-set-icon"><code>SetIcon()</code></a></td><td>Sets the button icon sprite.</td></tr>
<tr><td><a href="#echo-chamber-button-set-icon-subimg"><code>SetIconSubimg()</code></a></td><td>Sets the button icon subimage.</td></tr>
<tr><td><a href="#echo-chamber-button-clear-icon"><code>ClearIcon()</code></a></td><td>Clears the button icon.</td></tr>
<tr><td><a href="#echo-chamber-button-bind-caption"><code>BindCaption()</code></a></td><td>Binds the button caption to a field binding, struct field, or getter function.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-button-on-click">
  <div class="api-method-name">OnClick(fn)</div>
  <p class="api-method-summary">Sets a callback to run when the button is activated (click or Enter while focused).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-button">EchoChamberButton</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-button-set-icon">
  <div class="api-method-name">SetIcon(sprite)</div>
  <p class="api-method-summary">Sets the button icon sprite.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">sprite</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-button">EchoChamberButton</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-button-set-icon-subimg">
  <div class="api-method-name">SetIconSubimg(subimg)</div>
  <p class="api-method-summary">Sets the button icon subimage.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">subimg</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-button">EchoChamberButton</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-button-clear-icon">
  <div class="api-method-name">ClearIcon()</div>
  <p class="api-method-summary">Clears the button icon.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-button">EchoChamberButton</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-button-bind-caption">
  <div class="api-method-name">BindCaption(source, [key_or_fn])</div>
  <p class="api-method-summary">Binds the button caption to a field binding, struct field, or getter function.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-field-binding">EchoChamberFieldBinding</a>|Struct|Function</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key_or_fn <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String|Function|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-button">EchoChamberButton</a></span>
    </div>
  </div>
</div>

### EchoChamberSlider
{: #echo-chamber-slider .api-type-title }

Horizontal slider control.

Inherits from [`EchoChamberControlBase`](#echo-chamber-control-base).

```gml
new EchoChamberSlider(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-chamber-slider-set-range"><code>SetRange()</code></a></td><td>Sets the slider range.</td></tr>
<tr><td><a href="#echo-chamber-slider-set-step"><code>SetStep()</code></a></td><td>Sets step snapping size (0 disables snapping).</td></tr>
<tr><td><a href="#echo-chamber-slider-set-value-formatter"><code>SetValueFormatter()</code></a></td><td>Sets a formatter callback for built-in value text.</td></tr>
<tr><td><a href="#echo-chamber-slider-set-value-decimals"><code>SetValueDecimals()</code></a></td><td>Sets decimal precision for built-in value text (-1 uses default string conversion).</td></tr>
<tr><td><a href="#echo-chamber-slider-bind-value"><code>BindValue()</code></a></td><td>Binds the slider value to a field binding, struct field, or getter/setter function pair. Function binding uses <code>_source</code> as getter and <code>_key_or_fn</code> as setter when <code>_key_or_fn</code> is callable.</td></tr>
<tr><td><a href="#echo-chamber-slider-on-change"><code>OnChange()</code></a></td><td>Sets a callback that runs when the value changes.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-slider-set-range">
  <div class="api-method-name">SetRange(min, max)</div>
  <p class="api-method-summary">Sets the slider range.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">min</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">max</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-slider">EchoChamberSlider</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-slider-set-step">
  <div class="api-method-name">SetStep(step)</div>
  <p class="api-method-summary">Sets step snapping size (0 disables snapping).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">step</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-slider">EchoChamberSlider</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-slider-set-value-formatter">
  <div class="api-method-name">SetValueFormatter(fn)</div>
  <p class="api-method-summary">Sets a formatter callback for built-in value text.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_value) -&gt; string</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-slider">EchoChamberSlider</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-slider-set-value-decimals">
  <div class="api-method-name">SetValueDecimals(digits)</div>
  <p class="api-method-summary">Sets decimal precision for built-in value text (-1 uses default string conversion).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">digits</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-slider">EchoChamberSlider</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-slider-bind-value">
  <div class="api-method-name">BindValue(source, [key_or_fn])</div>
  <p class="api-method-summary">Binds the slider value to a field binding, struct field, or getter/setter function pair. Function binding uses <code>_source</code> as getter and <code>_key_or_fn</code> as setter when <code>_key_or_fn</code> is callable.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-field-binding">EchoChamberFieldBinding</a>|Struct|Function</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key_or_fn <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String|Function|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-slider">EchoChamberSlider</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-slider-on-change">
  <div class="api-method-name">OnChange(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when the value changes.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_value)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-slider">EchoChamberSlider</a></span>
    </div>
  </div>
</div>

### EchoChamberToggle
{: #echo-chamber-toggle .api-type-title }

Checkbox-style toggle.

Inherits from [`EchoChamberControlBase`](#echo-chamber-control-base).

```gml
new EchoChamberToggle(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-chamber-toggle-bind-value"><code>BindValue()</code></a></td><td>Binds the toggle state to a field binding, struct field, or getter/setter function pair.</td></tr>
<tr><td><a href="#echo-chamber-toggle-on-change"><code>OnChange()</code></a></td><td>Sets a callback that runs when the value changes.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-toggle-bind-value">
  <div class="api-method-name">BindValue(source, [key_or_fn])</div>
  <p class="api-method-summary">Binds the toggle state to a field binding, struct field, or getter/setter function pair.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-field-binding">EchoChamberFieldBinding</a>|Struct|Function</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key_or_fn <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String|Function|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-toggle">EchoChamberToggle</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-toggle-on-change">
  <div class="api-method-name">OnChange(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when the value changes.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_value)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-toggle">EchoChamberToggle</a></span>
    </div>
  </div>
</div>

### EchoChamberTextInput
{: #echo-chamber-text-input .api-type-title }

Single-line text input.

Inherits from [`EchoChamberControlBase`](#echo-chamber-control-base).

```gml
new EchoChamberTextInput(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Binding and callbacks</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-text-input-bind-text"><code>BindText()</code></a></td><td>Binds this text input to a field binding, struct field, or getter/setter function pair.</td></tr>
<tr><td><a href="#echo-chamber-text-input-on-change"><code>OnChange()</code></a></td><td>Sets a callback that runs when text is committed.</td></tr>
<tr><td><a href="#echo-chamber-text-input-on-submit"><code>OnSubmit()</code></a></td><td>Sets a callback that runs when text is submitted (committed edit).</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-submit-on-enter"><code>SetSubmitOnEnter()</code></a></td><td>Sets whether pressing Enter submits this text input.</td></tr>
<tr><td><a href="#echo-chamber-text-input-on-history-previous"><code>OnHistoryPrevious()</code></a></td><td>Sets a callback that returns the previous history text for this input.</td></tr>
<tr><td><a href="#echo-chamber-text-input-on-history-next"><code>OnHistoryNext()</code></a></td><td>Sets a callback that returns the next history text for this input.</td></tr>
<tr><td><a href="#echo-chamber-text-input-on-cancel"><code>OnCancel()</code></a></td><td>Sets a callback that runs when text editing is cancelled.</td></tr>
<tr><td><a href="#echo-chamber-text-input-on-focus"><code>OnFocus()</code></a></td><td>Sets a callback that runs when this text input gains editing focus.</td></tr>
<tr><td><a href="#echo-chamber-text-input-on-blur"><code>OnBlur()</code></a></td><td>Sets a callback that runs when this text input loses editing focus.</td></tr>
<tr><td><a href="#echo-chamber-text-input-on-live-change"><code>OnLiveChange()</code></a></td><td>Sets a callback that runs while the user edits text (typing, delete, paste, undo/redo).</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-live-change-rate-ms"><code>SetLiveChangeRateMs()</code></a></td><td>Sets a throttle rate for the live change callback (0 = no throttling).</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-on-live-change"><code>SetOnLiveChange()</code></a></td><td>Sets the live change callback and its rate in one call.</td></tr>
</tbody></table>

<div class="api-method-group-title">Input behaviour</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-text-input-set-placeholder"><code>SetPlaceholder()</code></a></td><td>Sets the placeholder text shown when empty and not active.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-context-menu-style-key"><code>SetContextMenuStyleKey()</code></a></td><td>Sets the context menu style key used by this input&#x27;s built-in context menus.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-read-only"><code>SetReadOnly()</code></a></td><td>Sets whether this text input is read-only.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-max-length"><code>SetMaxLength()</code></a></td><td>Sets the maximum number of characters allowed (0 = unlimited).</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-allowed-chars"><code>SetAllowedChars()</code></a></td><td>Restrict input to the characters in the given string (empty = allow all).</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-denied-chars"><code>SetDeniedChars()</code></a></td><td>Reject any characters contained in the given string.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-numeric-only"><code>SetNumericOnly()</code></a></td><td>Restrict input to numeric characters.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-select-all-on-focus"><code>SetSelectAllOnFocus()</code></a></td><td>Selects all text when the input gains focus.</td></tr>
</tbody></table>

<div class="api-method-group-title">Filtering and transforms</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-text-input-set-filter"><code>SetFilter()</code></a></td><td>Sets a filter function that can mutate inserted text. The filter can mutate inserted text after transforms and before built-in validators finish.</td></tr>
<tr><td><a href="#echo-chamber-text-input-add-transform"><code>AddTransform()</code></a></td><td>Adds a text transform function applied before SetFilter and built-in validators.</td></tr>
<tr><td><a href="#echo-chamber-text-input-clear-transforms"><code>ClearTransforms()</code></a></td><td>Clears all transform functions.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-auto-trim"><code>SetAutoTrim()</code></a></td><td>Enables or disables automatic trim of inserted text.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-auto-upper"><code>SetAutoUpper()</code></a></td><td>Enables or disables automatic uppercase transform.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-auto-lower"><code>SetAutoLower()</code></a></td><td>Enables or disables automatic lowercase transform.</td></tr>
</tbody></table>

<div class="api-method-group-title">Validation</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-text-input-set-invalid"><code>SetInvalid()</code></a></td><td>Mark this text input as invalid for styling.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-validation-message"><code>SetValidationMessage()</code></a></td><td>Sets a validation message and kind to show to the user.</td></tr>
<tr><td><a href="#echo-chamber-text-input-clear-validation-message"><code>ClearValidationMessage()</code></a></td><td>Clears any validation message.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-validation-visible"><code>SetValidationVisible()</code></a></td><td>Shows or hides validation messaging.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-validation-display"><code>SetValidationDisplay()</code></a></td><td>Sets how the validation message is displayed.</td></tr>
</tbody></table>

<div class="api-method-group-title">Input modes and editor</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-text-input-set-input-mode"><code>SetInputMode()</code></a></td><td>Sets the input mode (TEXT/INT/FLOAT/IDENTIFIER/PATH/CODE/PASSWORD). Integer and float modes enable numeric filtering. Code mode enables tab insertion and auto indent. Password mode masks display text.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-input-mode-int"><code>SetInputModeInt()</code></a></td><td>Sets the input mode to INT.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-input-mode-float"><code>SetInputModeFloat()</code></a></td><td>Sets the input mode to FLOAT.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-input-mode-code"><code>SetInputModeCode()</code></a></td><td>Sets the input mode to CODE.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-input-mode-password"><code>SetInputModePassword()</code></a></td><td>Sets the input mode to PASSWORD.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-tab-inserts"><code>SetTabInserts()</code></a></td><td>Enables or disables Tab insertion while editing (disables Tab focus cycling when active).</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-tab-uses-spaces"><code>SetTabUsesSpaces()</code></a></td><td>Sets whether Tab inserts spaces instead of a tab character.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-tab-spaces"><code>SetTabSpaces()</code></a></td><td>Sets how many spaces are inserted when Tab uses spaces.</td></tr>
</tbody></table>

<div class="api-method-group-title">Skin and forced sizing</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-text-input-set-background-sprite"><code>SetBackgroundSprite()</code></a></td><td>Sets the background sprite for this input (-1 to clear).</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-border-sprite"><code>SetBorderSprite()</code></a></td><td>Sets the border sprite for this input (-1 to clear).</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-caret-sprite"><code>SetCaretSprite()</code></a></td><td>Sets the caret sprite for this input (-1 to clear).</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-grip-sprite"><code>SetGripSprite()</code></a></td><td>Sets the TextBox resize grip sprite (-1 to clear).</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-expand-sprite"><code>SetExpandSprite()</code></a></td><td>Sets the TextBox expand button sprite (-1 to clear).</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-skin-tint"><code>SetSkinTint()</code></a></td><td>Enables or disables extra skin tint multiplication for sprites.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-force-size-from-background-sprite"><code>SetForceSizeFromBackgroundSprite()</code></a></td><td>Sets this control size to match the current background sprite.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-force-size-from-border-sprite"><code>SetForceSizeFromBorderSprite()</code></a></td><td>Sets this control size to match the current border sprite.</td></tr>
<tr><td><a href="#echo-chamber-text-input-set-force-size-from-sprite"><code>SetForceSizeFromSprite()</code></a></td><td>Sets this control size to match a sprite asset.</td></tr>
<tr><td><a href="#echo-chamber-text-input-clear-force-size"><code>ClearForceSize()</code></a></td><td>Clears forced sizing and restore previous layout sizing.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-text-input-bind-text">
  <div class="api-method-name">BindText(source, [key_or_fn])</div>
  <p class="api-method-summary">Binds this text input to a field binding, struct field, or getter/setter function pair.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-field-binding">EchoChamberFieldBinding</a>|Struct|Function</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key_or_fn <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String|Function|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-placeholder">
  <div class="api-method-name">SetPlaceholder(text)</div>
  <p class="api-method-summary">Sets the placeholder text shown when empty and not active.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">text</span>
      <span class="api-argument-type">String|Real|Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-context-menu-style-key">
  <div class="api-method-name">SetContextMenuStyleKey(key)</div>
  <p class="api-method-summary">Sets the context menu style key used by this input&#x27;s built-in context menus.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-on-change">
  <div class="api-method-name">OnChange(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when text is committed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_text)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-on-submit">
  <div class="api-method-name">OnSubmit(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when text is submitted (committed edit).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_text)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-submit-on-enter">
  <div class="api-method-name">SetSubmitOnEnter(flag)</div>
  <p class="api-method-summary">Sets whether pressing Enter submits this text input.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-on-history-previous">
  <div class="api-method-name">OnHistoryPrevious(fn)</div>
  <p class="api-method-summary">Sets a callback that returns the previous history text for this input.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_text) -&gt; String</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-on-history-next">
  <div class="api-method-name">OnHistoryNext(fn)</div>
  <p class="api-method-summary">Sets a callback that returns the next history text for this input.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_text) -&gt; String</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-on-cancel">
  <div class="api-method-name">OnCancel(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when text editing is cancelled.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_text, _initial_text)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-on-focus">
  <div class="api-method-name">OnFocus(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when this text input gains editing focus.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_text)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-on-blur">
  <div class="api-method-name">OnBlur(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when this text input loses editing focus.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_text, _was_cancelled)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-on-live-change">
  <div class="api-method-name">OnLiveChange(fn)</div>
  <p class="api-method-summary">Sets a callback that runs while the user edits text (typing, delete, paste, undo/redo).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_text)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-live-change-rate-ms">
  <div class="api-method-name">SetLiveChangeRateMs(ms)</div>
  <p class="api-method-summary">Sets a throttle rate for the live change callback (0 = no throttling).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ms</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-on-live-change">
  <div class="api-method-name">SetOnLiveChange(fn, [rate_ms])</div>
  <p class="api-method-summary">Sets the live change callback and its rate in one call.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_text)</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">rate_ms <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-read-only">
  <div class="api-method-name">SetReadOnly(flag)</div>
  <p class="api-method-summary">Sets whether this text input is read-only.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-max-length">
  <div class="api-method-name">SetMaxLength(len)</div>
  <p class="api-method-summary">Sets the maximum number of characters allowed (0 = unlimited).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">len</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-allowed-chars">
  <div class="api-method-name">SetAllowedChars(chars)</div>
  <p class="api-method-summary">Restrict input to the characters in the given string (empty = allow all).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">chars</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-denied-chars">
  <div class="api-method-name">SetDeniedChars(chars)</div>
  <p class="api-method-summary">Reject any characters contained in the given string.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">chars</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-numeric-only">
  <div class="api-method-name">SetNumericOnly(flag, [allow_decimal], [allow_negative])</div>
  <p class="api-method-summary">Restrict input to numeric characters.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">allow_decimal <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">allow_negative <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-select-all-on-focus">
  <div class="api-method-name">SetSelectAllOnFocus(flag)</div>
  <p class="api-method-summary">Selects all text when the input gains focus.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-filter">
  <div class="api-method-name">SetFilter(fn)</div>
  <p class="api-method-summary">Sets a filter function that can mutate inserted text. The filter can mutate inserted text after transforms and before built-in validators finish.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_insert_text)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-add-transform">
  <div class="api-method-name">AddTransform(fn)</div>
  <p class="api-method-summary">Adds a text transform function applied before SetFilter and built-in validators.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_insert_text)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-clear-transforms">
  <div class="api-method-name">ClearTransforms()</div>
  <p class="api-method-summary">Clears all transform functions.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-auto-trim">
  <div class="api-method-name">SetAutoTrim(flag)</div>
  <p class="api-method-summary">Enables or disables automatic trim of inserted text.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-auto-upper">
  <div class="api-method-name">SetAutoUpper(flag)</div>
  <p class="api-method-summary">Enables or disables automatic uppercase transform.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-auto-lower">
  <div class="api-method-name">SetAutoLower(flag)</div>
  <p class="api-method-summary">Enables or disables automatic lowercase transform.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-invalid">
  <div class="api-method-name">SetInvalid(flag)</div>
  <p class="api-method-summary">Mark this text input as invalid for styling.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-validation-message">
  <div class="api-method-name">SetValidationMessage(message, [kind])</div>
  <p class="api-method-summary">Sets a validation message and kind to show to the user.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">message</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">kind <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-validation-kind"><code>eEchoChamberValidationKind</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-clear-validation-message">
  <div class="api-method-name">ClearValidationMessage()</div>
  <p class="api-method-summary">Clears any validation message.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-validation-visible">
  <div class="api-method-name">SetValidationVisible(flag)</div>
  <p class="api-method-summary">Shows or hides validation messaging.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-validation-display">
  <div class="api-method-name">SetValidationDisplay(mode)</div>
  <p class="api-method-summary">Sets how the validation message is displayed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">mode</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-validation-display"><code>eEchoChamberValidationDisplay</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-input-mode">
  <div class="api-method-name">SetInputMode(mode)</div>
  <p class="api-method-summary">Sets the input mode (TEXT/INT/FLOAT/IDENTIFIER/PATH/CODE/PASSWORD). Integer and float modes enable numeric filtering. Code mode enables tab insertion and auto indent. Password mode masks display text.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">mode</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-input-mode-int">
  <div class="api-method-name">SetInputModeInt()</div>
  <p class="api-method-summary">Sets the input mode to INT.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-input-mode-float">
  <div class="api-method-name">SetInputModeFloat()</div>
  <p class="api-method-summary">Sets the input mode to FLOAT.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-input-mode-code">
  <div class="api-method-name">SetInputModeCode()</div>
  <p class="api-method-summary">Sets the input mode to CODE.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-input-mode-password">
  <div class="api-method-name">SetInputModePassword([allow_copy])</div>
  <p class="api-method-summary">Sets the input mode to PASSWORD.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">allow_copy <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-tab-inserts">
  <div class="api-method-name">SetTabInserts(flag)</div>
  <p class="api-method-summary">Enables or disables Tab insertion while editing (disables Tab focus cycling when active).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-tab-uses-spaces">
  <div class="api-method-name">SetTabUsesSpaces(flag)</div>
  <p class="api-method-summary">Sets whether Tab inserts spaces instead of a tab character.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-tab-spaces">
  <div class="api-method-name">SetTabSpaces(count)</div>
  <p class="api-method-summary">Sets how many spaces are inserted when Tab uses spaces.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">count</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-background-sprite">
  <div class="api-method-name">SetBackgroundSprite(spr, [subimg])</div>
  <p class="api-method-summary">Sets the background sprite for this input (-1 to clear).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">spr</span>
      <span class="api-argument-type">Asset.GMSprite|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">subimg <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-border-sprite">
  <div class="api-method-name">SetBorderSprite(spr, [subimg])</div>
  <p class="api-method-summary">Sets the border sprite for this input (-1 to clear).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">spr</span>
      <span class="api-argument-type">Asset.GMSprite|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">subimg <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-caret-sprite">
  <div class="api-method-name">SetCaretSprite(spr, [subimg])</div>
  <p class="api-method-summary">Sets the caret sprite for this input (-1 to clear).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">spr</span>
      <span class="api-argument-type">Asset.GMSprite|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">subimg <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-grip-sprite">
  <div class="api-method-name">SetGripSprite(spr, [subimg])</div>
  <p class="api-method-summary">Sets the TextBox resize grip sprite (-1 to clear).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">spr</span>
      <span class="api-argument-type">Asset.GMSprite|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">subimg <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-expand-sprite">
  <div class="api-method-name">SetExpandSprite(spr, [subimg])</div>
  <p class="api-method-summary">Sets the TextBox expand button sprite (-1 to clear).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">spr</span>
      <span class="api-argument-type">Asset.GMSprite|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">subimg <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-skin-tint">
  <div class="api-method-name">SetSkinTint(enabled, [col], [alpha_mul])</div>
  <p class="api-method-summary">Enables or disables extra skin tint multiplication for sprites.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">enabled</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">col <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">alpha_mul <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-force-size-from-background-sprite">
  <div class="api-method-name">SetForceSizeFromBackgroundSprite([scale], [lock_w], [lock_h])</div>
  <p class="api-method-summary">Sets this control size to match the current background sprite.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">scale <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">lock_w <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">lock_h <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-force-size-from-border-sprite">
  <div class="api-method-name">SetForceSizeFromBorderSprite([scale], [lock_w], [lock_h])</div>
  <p class="api-method-summary">Sets this control size to match the current border sprite.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">scale <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">lock_w <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">lock_h <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-set-force-size-from-sprite">
  <div class="api-method-name">SetForceSizeFromSprite(spr, [scale], [lock_w], [lock_h])</div>
  <p class="api-method-summary">Sets this control size to match a sprite asset.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">spr</span>
      <span class="api-argument-type">Asset.GMSprite|Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">scale <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">lock_w <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">lock_h <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-input-clear-force-size">
  <div class="api-method-name">ClearForceSize()</div>
  <p class="api-method-summary">Clears forced sizing and restore previous layout sizing.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-input">EchoChamberTextInput</a></span>
    </div>
  </div>
</div>

### EchoChamberTextBox
{: #echo-chamber-text-box .api-type-title }

Multi-line text box with vertical scrolling.

Inherits from [`EchoChamberTextInput`](#echo-chamber-text-input).

```gml
new EchoChamberTextBox(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-chamber-text-box-set-wrap"><code>SetWrap()</code></a></td><td>Enables or disables word wrapping.</td></tr>
<tr><td><a href="#echo-chamber-text-box-set-visible-rows"><code>SetVisibleRows()</code></a></td><td>Sets how many rows should be visible (uses font line height).</td></tr>
<tr><td><a href="#echo-chamber-text-box-set-min-height"><code>SetMinHeight()</code></a></td><td>Sets the minimum pixel height.</td></tr>
<tr><td><a href="#echo-chamber-text-box-set-max-height"><code>SetMaxHeight()</code></a></td><td>Sets the maximum pixel height (0 = unlimited).</td></tr>
<tr><td><a href="#echo-chamber-text-box-set-resizable"><code>SetResizable()</code></a></td><td>Enables or disables the resize grip.</td></tr>
<tr><td><a href="#echo-chamber-text-box-set-use-overlay-editor"><code>SetUseOverlayEditor()</code></a></td><td>Enables or disables the overlay editor affordance.</td></tr>
<tr><td><a href="#echo-chamber-text-box-set-editor-overlay-style-key"><code>SetEditorOverlayStyleKey()</code></a></td><td>Sets the editor overlay style key used by this text box&#x27;s modal editor.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-text-box-set-wrap">
  <div class="api-method-name">SetWrap(flag)</div>
  <p class="api-method-summary">Enables or disables word wrapping.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-box">EchoChamberTextBox</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-box-set-visible-rows">
  <div class="api-method-name">SetVisibleRows(rows)</div>
  <p class="api-method-summary">Sets how many rows should be visible (uses font line height).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">rows</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-box">EchoChamberTextBox</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-box-set-min-height">
  <div class="api-method-name">SetMinHeight(px)</div>
  <p class="api-method-summary">Sets the minimum pixel height.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">px</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-box">EchoChamberTextBox</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-box-set-max-height">
  <div class="api-method-name">SetMaxHeight(px)</div>
  <p class="api-method-summary">Sets the maximum pixel height (0 = unlimited).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">px</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-box">EchoChamberTextBox</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-box-set-resizable">
  <div class="api-method-name">SetResizable(flag, [min_h], [max_h])</div>
  <p class="api-method-summary">Enables or disables the resize grip.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">min_h <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">max_h <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-box">EchoChamberTextBox</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-box-set-use-overlay-editor">
  <div class="api-method-name">SetUseOverlayEditor(flag)</div>
  <p class="api-method-summary">Enables or disables the overlay editor affordance.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-box">EchoChamberTextBox</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-text-box-set-editor-overlay-style-key">
  <div class="api-method-name">SetEditorOverlayStyleKey(key)</div>
  <p class="api-method-summary">Sets the editor overlay style key used by this text box&#x27;s modal editor.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-text-box">EchoChamberTextBox</a></span>
    </div>
  </div>
</div>

### EchoChamberSeparator
{: #echo-chamber-separator .api-type-title }

Non-interactive separator line.

Inherits from [`EchoChamberControlBase`](#echo-chamber-control-base).

```gml
new EchoChamberSeparator(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-chamber-separator-set-orientation"><code>SetOrientation()</code></a></td><td>Sets separator orientation.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-separator-set-orientation">
  <div class="api-method-name">SetOrientation(ori)</div>
  <p class="api-method-summary">Sets separator orientation.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ori</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-separator-orientation"><code>eEchoChamberSeparatorOrientation</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-separator">EchoChamberSeparator</a></span>
    </div>
  </div>
</div>

### EchoChamberListView
{: #echo-chamber-list-view .api-type-title }

List control for very large lists. It only draws and checks input for rows that are on screen.

Inherits from [`EchoChamberControlBase`](#echo-chamber-control-base).

```gml
new EchoChamberListView(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Sizing and data</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-list-view-set-visible-rows"><code>SetVisibleRows()</code></a></td><td>Sets how many rows should be visible (uses row height).</td></tr>
<tr><td><a href="#echo-chamber-list-view-set-auto-height-from-count"><code>SetAutoHeightFromCount()</code></a></td><td>Auto-size to the current row count, clamped to a maximum number of rows.</td></tr>
<tr><td><a href="#echo-chamber-list-view-set-auto-width-from-content"><code>SetAutoWidthFromContent()</code></a></td><td>Auto-size width to row content, sampling up to the given number of rows (0 disables).</td></tr>
<tr><td><a href="#echo-chamber-list-view-set-fill-width"><code>SetFillWidth()</code></a></td><td>Sets whether this list view fills available row width.</td></tr>
<tr><td><a href="#echo-chamber-list-view-set-preferred-height"><code>SetPreferredHeight()</code></a></td><td>Sets the preferred pixel height for this list view (used by FitToContent).</td></tr>
<tr><td><a href="#echo-chamber-list-view-set-preferred-width"><code>SetPreferredWidth()</code></a></td><td>Sets a preferred pixel width for this list view.</td></tr>
<tr><td><a href="#echo-chamber-list-view-set-row-measure"><code>SetRowMeasure()</code></a></td><td>Sets a function that returns row text or pixel width (used for auto width).</td></tr>
<tr><td><a href="#echo-chamber-list-view-set-count-getter"><code>SetCountGetter()</code></a></td><td>Sets a function that returns the current number of rows.</td></tr>
<tr><td><a href="#echo-chamber-list-view-set-row-drawer"><code>SetRowDrawer()</code></a></td><td>Sets a function that draws a row&#x27;s content. Background is drawn by the control.</td></tr>
<tr><td><a href="#echo-chamber-list-view-set-row-tooltip-getter"><code>SetRowTooltipGetter()</code></a></td><td>Sets a function that returns complete tooltip text for the hovered row. Supplies complete tooltip text for the hovered row. Passing a non-callable value clears the getter.</td></tr>
</tbody></table>

<div class="api-method-group-title">Events</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-list-view-set-on-select"><code>SetOnSelect()</code></a></td><td>Sets a callback that runs when the selection changes.</td></tr>
<tr><td><a href="#echo-chamber-list-view-set-on-activate"><code>SetOnActivate()</code></a></td><td>Sets a callback that runs when the active row is activated with Enter.</td></tr>
<tr><td><a href="#echo-chamber-list-view-set-on-double-click"><code>SetOnDoubleClick()</code></a></td><td>Sets a callback that runs when a row is double clicked.</td></tr>
<tr><td><a href="#echo-chamber-list-view-set-on-right-click"><code>SetOnRightClick()</code></a></td><td>Sets a callback that runs when a row is right clicked. _index is -1 when empty space was clicked.</td></tr>
</tbody></table>

<div class="api-method-group-title">Selection and scrolling</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-chamber-list-view-set-auto-scroll"><code>SetAutoScroll()</code></a></td><td>Enables or disables auto-scroll-to-bottom behavior.</td></tr>
<tr><td><a href="#echo-chamber-list-view-jump-to-bottom"><code>JumpToBottom()</code></a></td><td>Scroll the list to the bottom and resume auto-follow (if enabled).</td></tr>
<tr><td><a href="#echo-chamber-list-view-is-near-bottom"><code>IsNearBottom()</code></a></td><td>Returns true if the list is currently near the bottom (based on the last draw).</td></tr>
<tr><td><a href="#echo-chamber-list-view-is-auto-follow-paused"><code>IsAutoFollowPaused()</code></a></td><td>Returns true if auto-follow is currently paused due to user scroll.</td></tr>
<tr><td><a href="#echo-chamber-list-view-get-selected-index"><code>GetSelectedIndex()</code></a></td><td>Returns the current selected row index (or -1).</td></tr>
<tr><td><a href="#echo-chamber-list-view-set-selected-index"><code>SetSelectedIndex()</code></a></td><td>Sets the selected row index (clamped to range). Use -1 to clear selection.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-list-view-set-visible-rows">
  <div class="api-method-name">SetVisibleRows(rows)</div>
  <p class="api-method-summary">Sets how many rows should be visible (uses row height).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">rows</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-set-auto-height-from-count">
  <div class="api-method-name">SetAutoHeightFromCount(max_rows)</div>
  <p class="api-method-summary">Auto-size to the current row count, clamped to a maximum number of rows.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">max_rows</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-set-auto-width-from-content">
  <div class="api-method-name">SetAutoWidthFromContent(max_rows)</div>
  <p class="api-method-summary">Auto-size width to row content, sampling up to the given number of rows (0 disables).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">max_rows</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-set-fill-width">
  <div class="api-method-name">SetFillWidth(flag)</div>
  <p class="api-method-summary">Sets whether this list view fills available row width.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-set-preferred-height">
  <div class="api-method-name">SetPreferredHeight(h)</div>
  <p class="api-method-summary">Sets the preferred pixel height for this list view (used by FitToContent).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">h</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-set-preferred-width">
  <div class="api-method-name">SetPreferredWidth(w)</div>
  <p class="api-method-summary">Sets a preferred pixel width for this list view.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">w</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-set-row-measure">
  <div class="api-method-name">SetRowMeasure(fn)</div>
  <p class="api-method-summary">Sets a function that returns row text or pixel width (used for auto width).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_index, _root, _panel) -&gt; String or Real</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-set-count-getter">
  <div class="api-method-name">SetCountGetter(fn)</div>
  <p class="api-method-summary">Sets a function that returns the current number of rows.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function() -&gt; Real</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-set-row-drawer">
  <div class="api-method-name">SetRowDrawer(fn)</div>
  <p class="api-method-summary">Sets a function that draws a row&#x27;s content. Background is drawn by the control.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Callback function(_index, _rect, _is_selected, _is_hover).</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-set-row-tooltip-getter">
  <div class="api-method-name">SetRowTooltipGetter(fn)</div>
  <p class="api-method-summary">Sets a function that returns complete tooltip text for the hovered row. Supplies complete tooltip text for the hovered row. Passing a non-callable value clears the getter.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Callback function(_index) -&gt; String or Undefined.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-set-on-select">
  <div class="api-method-name">SetOnSelect(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when the selection changes.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_index)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-set-on-activate">
  <div class="api-method-name">SetOnActivate(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when the active row is activated with Enter.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_index)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-set-on-double-click">
  <div class="api-method-name">SetOnDoubleClick(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when a row is double clicked.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_index)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-set-on-right-click">
  <div class="api-method-name">SetOnRightClick(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when a row is right clicked. _index is -1 when empty space was clicked.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_index, _x, _y)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-set-auto-scroll">
  <div class="api-method-name">SetAutoScroll(enabled)</div>
  <p class="api-method-summary">Enables or disables auto-scroll-to-bottom behavior.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">enabled</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-jump-to-bottom">
  <div class="api-method-name">JumpToBottom()</div>
  <p class="api-method-summary">Scroll the list to the bottom and resume auto-follow (if enabled).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-is-near-bottom">
  <div class="api-method-name">IsNearBottom()</div>
  <p class="api-method-summary">Returns true if the list is currently near the bottom (based on the last draw).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-is-auto-follow-paused">
  <div class="api-method-name">IsAutoFollowPaused()</div>
  <p class="api-method-summary">Returns true if auto-follow is currently paused due to user scroll.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-get-selected-index">
  <div class="api-method-name">GetSelectedIndex()</div>
  <p class="api-method-summary">Returns the current selected row index (or -1).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-list-view-set-selected-index">
  <div class="api-method-name">SetSelectedIndex(index)</div>
  <p class="api-method-summary">Sets the selected row index (clamped to range). Use -1 to clear selection.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">index</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

### EchoChamberDropdownBase
{: #echo-chamber-dropdown-base .api-type-title }

Base control used by the dropdown variants.

Inherits from [`EchoChamberControlBase`](#echo-chamber-control-base).

```gml
new EchoChamberDropdownBase(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-chamber-dropdown-base-get-selected-index"><code>GetSelectedIndex()</code></a></td><td>Returns the selected option index.</td></tr>
<tr><td><a href="#echo-chamber-dropdown-base-set-selected-index"><code>SetSelectedIndex()</code></a></td><td>Sets the selected option index (clamped to the available option range).</td></tr>
<tr><td><a href="#echo-chamber-dropdown-base-draw-overlay-row"><code>DrawOverlayRow()</code></a></td><td>Draws a single row inside the dropdown overlay.</td></tr>
<tr><td><a href="#echo-chamber-dropdown-base-set-options"><code>SetOptions()</code></a></td><td>Sets the dropdown option labels array.</td></tr>
<tr><td><a href="#echo-chamber-dropdown-base-bind-options"><code>BindOptions()</code></a></td><td>Binds this dropdown&#x27;s options to a field binding, struct field, or getter function. Replaces the direct <code>options</code> array with a dynamic source. The source should return an array and must be cheap and side-effect-free because the dropdown consults it while resolving option labels and layout.</td></tr>
<tr><td><a href="#echo-chamber-dropdown-base-set-unfold-direction"><code>SetUnfoldDirection()</code></a></td><td>Sets the preferred dropdown unfold direction.</td></tr>
<tr><td><a href="#echo-chamber-dropdown-base-set-use-selected-label-when-closed"><code>SetUseSelectedLabelWhenClosed()</code></a></td><td>Sets whether the base caption shows the selected option while closed.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-dropdown-base-get-selected-index">
  <div class="api-method-name">GetSelectedIndex()</div>
  <p class="api-method-summary">Returns the selected option index.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-dropdown-base-set-selected-index">
  <div class="api-method-name">SetSelectedIndex(idx)</div>
  <p class="api-method-summary">Sets the selected option index (clamped to the available option range).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">idx</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-dropdown-base-draw-overlay-row">
  <div class="api-method-name">DrawOverlayRow(root, row_index, row_rect, hover, selected)</div>
  <p class="api-method-summary">Draws a single row inside the dropdown overlay.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">row_index</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">row_rect</span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">{x1,y1,x2,y2}</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">hover</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">selected</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-dropdown-base-set-options">
  <div class="api-method-name">SetOptions(array)</div>
  <p class="api-method-summary">Sets the dropdown option labels array.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">array</span>
      <span class="api-argument-type">Array&lt;String&gt;</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-dropdown-base">EchoChamberDropdownBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-dropdown-base-bind-options">
  <div class="api-method-name">BindOptions(source, [key_or_fn])</div>
  <p class="api-method-summary">Binds this dropdown&#x27;s options to a field binding, struct field, or getter function. Replaces the direct <code>options</code> array with a dynamic source. The source should return an array and must be cheap and side-effect-free because the dropdown consults it while resolving option labels and layout.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-field-binding">EchoChamberFieldBinding</a>|Struct|Function</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key_or_fn <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String|Function|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-dropdown-base">EchoChamberDropdownBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-dropdown-base-set-unfold-direction">
  <div class="api-method-name">SetUnfoldDirection(dir)</div>
  <p class="api-method-summary">Sets the preferred dropdown unfold direction.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">dir</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-popup-direction"><code>eEchoChamberPopupDirection</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-dropdown-base">EchoChamberDropdownBase</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-dropdown-base-set-use-selected-label-when-closed">
  <div class="api-method-name">SetUseSelectedLabelWhenClosed(flag)</div>
  <p class="api-method-summary">Sets whether the base caption shows the selected option while closed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flag</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-dropdown-base">EchoChamberDropdownBase</a></span>
    </div>
  </div>
</div>

### EchoChamberDropdownSelect
{: #echo-chamber-dropdown-select .api-type-title }

Dropdown variant that binds a selected index to dynamic binding sources.

Inherits from [`EchoChamberDropdownBase`](#echo-chamber-dropdown-base).

```gml
new EchoChamberDropdownSelect(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-chamber-dropdown-select-bind-index"><code>BindIndex()</code></a></td><td>Binds the selected index to a field binding, struct field, or getter/setter function pair.</td></tr>
<tr><td><a href="#echo-chamber-dropdown-select-on-change"><code>OnChange()</code></a></td><td>Sets a callback that runs when selection changes.</td></tr>
<tr><td><a href="#echo-chamber-dropdown-select-get-selected-index"><code>GetSelectedIndex()</code></a></td><td>Returns the selected option index.</td></tr>
<tr><td><a href="#echo-chamber-dropdown-select-set-selected-index"><code>SetSelectedIndex()</code></a></td><td>Sets the selected option index and update the bound source (if configured).</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-dropdown-select-bind-index">
  <div class="api-method-name">BindIndex(source, [key_or_fn])</div>
  <p class="api-method-summary">Binds the selected index to a field binding, struct field, or getter/setter function pair.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-field-binding">EchoChamberFieldBinding</a>|Struct|Function</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key_or_fn <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String|Function|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-dropdown-select">EchoChamberDropdownSelect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-dropdown-select-on-change">
  <div class="api-method-name">OnChange(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when selection changes.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_index, _value)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-dropdown-select">EchoChamberDropdownSelect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-dropdown-select-get-selected-index">
  <div class="api-method-name">GetSelectedIndex()</div>
  <p class="api-method-summary">Returns the selected option index.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-dropdown-select-set-selected-index">
  <div class="api-method-name">SetSelectedIndex(idx, [root])</div>
  <p class="api-method-summary">Sets the selected option index and update the bound source (if configured).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">idx</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">root <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a>|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

### EchoChamberDropdownToggleMenu
{: #echo-chamber-dropdown-toggle-menu .api-type-title }

Dropdown variant that shows a checklist menu that stays open.

Inherits from [`EchoChamberDropdownBase`](#echo-chamber-dropdown-base).

```gml
new EchoChamberDropdownToggleMenu(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-chamber-dropdown-toggle-menu-set-items"><code>SetItems()</code></a></td><td>Sets the toggle menu items and rebuild the overlay option count.</td></tr>
<tr><td><a href="#echo-chamber-dropdown-toggle-menu-on-any-change"><code>OnAnyChange()</code></a></td><td>Sets a callback that runs after any item is toggled.</td></tr>
<tr><td><a href="#echo-chamber-dropdown-toggle-menu-get-selected-index"><code>GetSelectedIndex()</code></a></td><td>Returns a selected index placeholder (toggle menus do not have a single selected row).</td></tr>
<tr><td><a href="#echo-chamber-dropdown-toggle-menu-set-selected-index"><code>SetSelectedIndex()</code></a></td><td>No-op for toggle menus (kept for base compatibility).</td></tr>
<tr><td><a href="#echo-chamber-dropdown-toggle-menu-draw-overlay-row"><code>DrawOverlayRow()</code></a></td><td>Draws a checklist row in the overlay.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-dropdown-toggle-menu-set-items">
  <div class="api-method-name">SetItems(items)</div>
  <p class="api-method-summary">Sets the toggle menu items and rebuild the overlay option count.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">items</span>
      <span class="api-argument-type">Array&lt;Struct&gt;</span>
      <span class="api-argument-description">Each item: {label, bind_struct, bind_key}</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-dropdown-toggle-menu">EchoChamberDropdownToggleMenu</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-dropdown-toggle-menu-on-any-change">
  <div class="api-method-name">OnAnyChange(fn)</div>
  <p class="api-method-summary">Sets a callback that runs after any item is toggled.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-dropdown-toggle-menu">EchoChamberDropdownToggleMenu</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-dropdown-toggle-menu-get-selected-index">
  <div class="api-method-name">GetSelectedIndex()</div>
  <p class="api-method-summary">Returns a selected index placeholder (toggle menus do not have a single selected row).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-dropdown-toggle-menu-set-selected-index">
  <div class="api-method-name">SetSelectedIndex(idx)</div>
  <p class="api-method-summary">No-op for toggle menus (kept for base compatibility).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">idx</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-list-view">EchoChamberListView</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-dropdown-toggle-menu-draw-overlay-row">
  <div class="api-method-name">DrawOverlayRow(root, row_index, rect, hover, is_selected)</div>
  <p class="api-method-summary">Draws a checklist row in the overlay.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">row_index</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">rect</span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">{x1,y1,x2,y2}</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">hover</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">is_selected</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

### EchoChamberColorButton
{: #echo-chamber-color-button .api-type-title }

Clickable color swatch button that opens the root-managed color picker popup.

Inherits from [`EchoChamberControlBase`](#echo-chamber-control-base).

```gml
new EchoChamberColorButton(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">String|Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-chamber-color-button-bind-color"><code>BindColor()</code></a></td><td>Binds this color button to a field binding, struct field, or getter/setter function pair.</td></tr>
<tr><td><a href="#echo-chamber-color-button-on-change"><code>OnChange()</code></a></td><td>Sets a callback that runs while the popup changes color live.</td></tr>
<tr><td><a href="#echo-chamber-color-button-on-commit"><code>OnCommit()</code></a></td><td>Sets a callback that runs when the popup commits.</td></tr>
<tr><td><a href="#echo-chamber-color-button-on-cancel"><code>OnCancel()</code></a></td><td>Sets a callback that runs when the popup cancels.</td></tr>
<tr><td><a href="#echo-chamber-color-button-set-popup-style-key"><code>SetPopupStyleKey()</code></a></td><td>Sets the popup style key used by this color button&#x27;s color picker.</td></tr>
<tr><td><a href="#echo-chamber-color-button-set-popup-direction"><code>SetPopupDirection()</code></a></td><td>Sets the preferred popup direction.</td></tr>
<tr><td><a href="#echo-chamber-color-button-set-popup-visual-space"><code>SetPopupVisualSpace()</code></a></td><td>Sets the popup visual space.</td></tr>
<tr><td><a href="#echo-chamber-color-button-set-popup-title"><code>SetPopupTitle()</code></a></td><td>Sets the popup title text.</td></tr>
<tr><td><a href="#echo-chamber-color-button-set-value-text-mode"><code>SetValueTextMode()</code></a></td><td>Sets the value text display mode.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-color-button-bind-color">
  <div class="api-method-name">BindColor(source, [key_or_fn])</div>
  <p class="api-method-summary">Binds this color button to a field binding, struct field, or getter/setter function pair.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-field-binding">EchoChamberFieldBinding</a>|Struct|Function</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key_or_fn <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String|Function|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-color-button">EchoChamberColorButton</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-color-button-on-change">
  <div class="api-method-name">OnChange(fn)</div>
  <p class="api-method-summary">Sets a callback that runs while the popup changes color live.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_color)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-color-button">EchoChamberColorButton</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-color-button-on-commit">
  <div class="api-method-name">OnCommit(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when the popup commits.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_color)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-color-button">EchoChamberColorButton</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-color-button-on-cancel">
  <div class="api-method-name">OnCancel(fn)</div>
  <p class="api-method-summary">Sets a callback that runs when the popup cancels.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_color)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-color-button">EchoChamberColorButton</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-color-button-set-popup-style-key">
  <div class="api-method-name">SetPopupStyleKey(key)</div>
  <p class="api-method-summary">Sets the popup style key used by this color button&#x27;s color picker.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-color-button">EchoChamberColorButton</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-color-button-set-popup-direction">
  <div class="api-method-name">SetPopupDirection(direction)</div>
  <p class="api-method-summary">Sets the preferred popup direction.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">direction</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-popup-direction"><code>eEchoChamberPopupDirection</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-color-button">EchoChamberColorButton</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-color-button-set-popup-visual-space">
  <div class="api-method-name">SetPopupVisualSpace(space)</div>
  <p class="api-method-summary">Sets the popup visual space.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">space</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-color-popup-visual-space"><code>eEchoChamberColorPopupVisualSpace</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-color-button">EchoChamberColorButton</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-color-button-set-popup-title">
  <div class="api-method-name">SetPopupTitle(text)</div>
  <p class="api-method-summary">Sets the popup title text.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">text</span>
      <span class="api-argument-type">String|Real|Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-color-button">EchoChamberColorButton</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-color-button-set-value-text-mode">
  <div class="api-method-name">SetValueTextMode(mode)</div>
  <p class="api-method-summary">Sets the value text display mode.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">mode</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Takes <a href="#enum-e-echo-chamber-color-button-value-text-mode"><code>eEchoChamberColorButtonValueTextMode</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-color-button">EchoChamberColorButton</a></span>
    </div>
  </div>
</div>

## Echo Console

### EchoConsoleCommandArg
{: #echo-console-command-arg .api-type-title }

Argument metadata for a custom Echo Console command. Required arguments can&#x27;t appear after optional arguments. <code>TEXT</code> consumes the rest of the command line and must be the final argument definition. Command lines are split on whitespace. Use <code>TEXT</code> when an argument needs to include spaces. The custom command callback receives <code>_args</code> as a plain struct. Each member name matches one argument <code>name</code>. The callback context struct contains <code>root</code>, <code>debug_manager</code>, <code>command_key</code>, <code>command_name</code>, <code>raw_text</code>, <code>raw_args</code>, <code>target</code>, <code>target_kind</code>, <code>target_value</code>, and <code>target_summary</code>. Callback returns: <code>undefined</code> means success, <code>Bool</code> controls success or failure, a struct <code>{ ok, message }</code> controls both status and output text, and any other value is converted to successful output text.

```gml
new EchoConsoleCommandArg(name, type, required, description, default_value)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Parsed argument field name.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">type <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-echo-console-command-arg-type"><code>eEchoConsoleCommandArgType</code></a> enum.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">required <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">description <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">default_value <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

### EchoConsoleTarget
{: #echo-console-target .api-type-title }

Value object describing the current Echo Chamber debug target.

```gml
new EchoConsoleTarget(kind, value, label)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">kind <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">value <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any|Undefined</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">label <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-console-target-is-none"><code>IsNone()</code></a></td><td>Returns whether this target represents no active target.</td></tr>
<tr><td><a href="#echo-console-target-is-instance"><code>IsInstance()</code></a></td><td>Returns whether this target represents an instance.</td></tr>
<tr><td><a href="#echo-console-target-is-valid"><code>IsValid()</code></a></td><td>Returns whether this target still points at a valid runtime value. Instance targets are valid only while the instance still exists. <code>NONE</code> is considered valid.</td></tr>
<tr><td><a href="#echo-console-target-get-value"><code>GetValue()</code></a></td><td>Returns the runtime value held by this target.</td></tr>
<tr><td><a href="#echo-console-target-get-label"><code>GetLabel()</code></a></td><td>Returns the display label for this target.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-console-target-is-none">
  <div class="api-method-name">IsNone()</div>
  <p class="api-method-summary">Returns whether this target represents no active target.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-target-is-instance">
  <div class="api-method-name">IsInstance()</div>
  <p class="api-method-summary">Returns whether this target represents an instance.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-target-is-valid">
  <div class="api-method-name">IsValid()</div>
  <p class="api-method-summary">Returns whether this target still points at a valid runtime value. Instance targets are valid only while the instance still exists. <code>NONE</code> is considered valid.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-target-get-value">
  <div class="api-method-name">GetValue()</div>
  <p class="api-method-summary">Returns the runtime value held by this target.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-target-get-label">
  <div class="api-method-name">GetLabel()</div>
  <p class="api-method-summary">Returns the display label for this target.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

### EchoConsoleManager
{: #echo-console-manager .api-type-title }

Shared state used by Echo Console and the other debug windows.

```gml
new EchoConsoleManager(root)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Target and picking</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-console-manager-set-target"><code>SetTarget()</code></a></td><td>Sets the active debug target.</td></tr>
<tr><td><a href="#echo-console-manager-set-instance-target"><code>SetInstanceTarget()</code></a></td><td>Sets the active debug target to an instance.</td></tr>
<tr><td><a href="#echo-console-manager-clear-target"><code>ClearTarget()</code></a></td><td>Clears the active debug target.</td></tr>
<tr><td><a href="#echo-console-manager-get-target"><code>GetTarget()</code></a></td><td>Returns the active debug target.</td></tr>
<tr><td><a href="#echo-console-manager-get-target-kind"><code>GetTargetKind()</code></a></td><td>Returns the active debug target kind.</td></tr>
<tr><td><a href="#echo-console-manager-get-target-value"><code>GetTargetValue()</code></a></td><td>Returns the active debug target value.</td></tr>
<tr><td><a href="#echo-console-manager-get-target-revision"><code>GetTargetRevision()</code></a></td><td>Returns the active debug target revision.</td></tr>
<tr><td><a href="#echo-console-manager-get-target-summary"><code>GetTargetSummary()</code></a></td><td>Returns a display string for the active debug target.</td></tr>
<tr><td><a href="#echo-console-manager-get-console-summary"><code>GetConsoleSummary()</code></a></td><td>Returns a display string for the main Echo Console hub status.</td></tr>
<tr><td><a href="#echo-console-manager-start-instance-pick"><code>StartInstancePick()</code></a></td><td>Starts instance pick mode.</td></tr>
<tr><td><a href="#echo-console-manager-cancel-pick"><code>CancelPick()</code></a></td><td>Cancels active debug pick mode.</td></tr>
<tr><td><a href="#echo-console-manager-is-picking"><code>IsPicking()</code></a></td><td>Returns whether any debug pick mode is active.</td></tr>
<tr><td><a href="#echo-console-manager-is-picking-instance"><code>IsPickingInstance()</code></a></td><td>Returns whether instance pick mode is active.</td></tr>
<tr><td><a href="#echo-console-manager-get-pick-mode"><code>GetPickMode()</code></a></td><td>Returns the active debug pick mode.</td></tr>
<tr><td><a href="#echo-console-manager-get-pick-hover-instance"><code>GetPickHoverInstance()</code></a></td><td>Returns the currently hovered instance while picking.</td></tr>
<tr><td><a href="#echo-console-manager-get-pick-hover-count"><code>GetPickHoverCount()</code></a></td><td>Returns the number of valid instances currently under the picker.</td></tr>
</tbody></table>

<div class="api-method-group-title">Watches</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-console-manager-add-instance-variable-watch"><code>AddInstanceVariableWatch()</code></a></td><td>Adds an instance-variable watch.</td></tr>
<tr><td><a href="#echo-console-manager-add-global-watch"><code>AddGlobalWatch()</code></a></td><td>Adds a global-variable watch.</td></tr>
<tr><td><a href="#echo-console-manager-add-callback-watch"><code>AddCallbackWatch()</code></a></td><td>Adds a callback watch.</td></tr>
<tr><td><a href="#echo-console-manager-remove-watch"><code>RemoveWatch()</code></a></td><td>Removes a watch.</td></tr>
<tr><td><a href="#echo-console-manager-clear-watches"><code>ClearWatches()</code></a></td><td>Clears all watches.</td></tr>
<tr><td><a href="#echo-console-manager-build-watches-snapshot-text"><code>BuildWatchesSnapshotText()</code></a></td><td>Builds a text report of current Echo Watches.</td></tr>
</tbody></table>

<div class="api-method-group-title">Input recording</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-console-manager-start-input-recording"><code>StartInputRecording()</code></a></td><td>Starts GameMaker debug input recording.</td></tr>
<tr><td><a href="#echo-console-manager-stop-input-recording"><code>StopInputRecording()</code></a></td><td>Stops and save the current GameMaker debug input recording.</td></tr>
<tr><td><a href="#echo-console-manager-play-input-recording"><code>PlayInputRecording()</code></a></td><td>Plays a saved GameMaker debug input recording.</td></tr>
<tr><td><a href="#echo-console-manager-handle-async-system"><code>HandleAsyncSystem()</code></a></td><td>Routes an Async System event to the debug manager.</td></tr>
</tbody></table>

<div class="api-method-group-title">Snapshots and crash reports</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-console-manager-capture-snapshot"><code>CaptureSnapshot()</code></a></td><td>Captures an Echo Snapshot report.</td></tr>
<tr><td><a href="#echo-console-manager-copy-snapshot"><code>CopySnapshot()</code></a></td><td>Copies the latest Echo Snapshot report to the clipboard.</td></tr>
<tr><td><a href="#echo-console-manager-save-snapshot"><code>SaveSnapshot()</code></a></td><td>Saves the latest Echo Snapshot report to a text file.</td></tr>
<tr><td><a href="#echo-console-manager-clear-saved-snapshots"><code>ClearSavedSnapshots()</code></a></td><td>Clears saved Echo Snapshot reports from the current window session.</td></tr>
<tr><td><a href="#echo-console-manager-enable-crash-capture"><code>EnableCrashCapture()</code></a></td><td>Enables Echo Crash Reports capture.</td></tr>
<tr><td><a href="#echo-console-manager-disable-crash-capture"><code>DisableCrashCapture()</code></a></td><td>Disables Echo Crash Reports capture.</td></tr>
<tr><td><a href="#echo-console-manager-has-crash-report"><code>HasCrashReport()</code></a></td><td>Returns whether a saved Echo Crash Report exists.</td></tr>
<tr><td><a href="#echo-console-manager-copy-crash-report"><code>CopyCrashReport()</code></a></td><td>Copies the saved Echo Crash Report to the clipboard.</td></tr>
<tr><td><a href="#echo-console-manager-clear-crash-report"><code>ClearCrashReport()</code></a></td><td>Clears the saved Echo Crash Report.</td></tr>
<tr><td><a href="#echo-console-manager-get-crash-report-text"><code>GetCrashReportText()</code></a></td><td>Returns the saved Echo Crash Report text.</td></tr>
</tbody></table>

<div class="api-method-group-title">Commands</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-console-manager-add-command"><code>AddCommand()</code></a></td><td>Adds a custom Echo Console command. Keys are normalized by Echo Console. Duplicate keys, invalid argument definitions, and non-callable callbacks return false.</td></tr>
<tr><td><a href="#echo-console-manager-unregister-command"><code>UnregisterCommand()</code></a></td><td>Unregister a custom Echo Console command.</td></tr>
<tr><td><a href="#echo-console-manager-run-command"><code>RunCommand()</code></a></td><td>Runs an Echo Console command line.</td></tr>
<tr><td><a href="#echo-console-manager-get-command-output"><code>GetCommandOutput()</code></a></td><td>Returns the latest command output text.</td></tr>
<tr><td><a href="#echo-console-manager-get-command-output-is-error"><code>GetCommandOutputIsError()</code></a></td><td>Returns whether the latest command output is an error.</td></tr>
<tr><td><a href="#echo-console-manager-get-previous-command"><code>GetPreviousCommand()</code></a></td><td>Returns the previous command history entry.</td></tr>
<tr><td><a href="#echo-console-manager-get-next-command"><code>GetNextCommand()</code></a></td><td>Returns the next command history entry.</td></tr>
</tbody></table>

<div class="api-method-group-title">Integration and windows</div>
<table class="api-methods"><tbody>
<tr><td><a href="#echo-console-manager-register-target-listener"><code>RegisterTargetListener()</code></a></td><td>Registers a callback fired when the active debug target changes. Reusing a key replaces the existing listener callback.</td></tr>
<tr><td><a href="#echo-console-manager-unregister-target-listener"><code>UnregisterTargetListener()</code></a></td><td>Removes a target-change listener by key.</td></tr>
<tr><td><a href="#echo-console-manager-register-window-opener"><code>RegisterWindowOpener()</code></a></td><td>Registers a debug window opener.</td></tr>
<tr><td><a href="#echo-console-manager-unregister-window-opener"><code>UnregisterWindowOpener()</code></a></td><td>Removes a debug window opener by key.</td></tr>
<tr><td><a href="#echo-console-manager-open-window"><code>OpenWindow()</code></a></td><td>Opens a registered debug window.</td></tr>
<tr><td><a href="#echo-console-manager-open-command-help"><code>OpenCommandHelp()</code></a></td><td>Opens the Echo Command Help window.</td></tr>
<tr><td><a href="#echo-console-manager-reset-built-in-window-layouts"><code>ResetBuiltInWindowLayouts()</code></a></td><td>Resets Echo Console and built-in debug window layouts.</td></tr>
<tr><td><a href="#echo-console-manager-register-overlay-drawer"><code>RegisterOverlayDrawer()</code></a></td><td>Registers a debug GUI overlay drawer. Overlay drawers run behind Echo Chamber windows during debug overlay drawing.</td></tr>
<tr><td><a href="#echo-console-manager-unregister-overlay-drawer"><code>UnregisterOverlayDrawer()</code></a></td><td>Removes a debug GUI overlay drawer by key.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-console-manager-set-target">
  <div class="api-method-name">SetTarget(target)</div>
  <p class="api-method-summary">Sets the active debug target.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">target</span>
      <span class="api-argument-type">Struct.<a href="#echo-console-target">EchoConsoleTarget</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-set-instance-target">
  <div class="api-method-name">SetInstanceTarget(instance)</div>
  <p class="api-method-summary">Sets the active debug target to an instance.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">instance</span>
      <span class="api-argument-type">Id.Instance</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-clear-target">
  <div class="api-method-name">ClearTarget()</div>
  <p class="api-method-summary">Clears the active debug target.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-console-manager">EchoConsoleManager</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-get-target">
  <div class="api-method-name">GetTarget()</div>
  <p class="api-method-summary">Returns the active debug target.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-console-target">EchoConsoleTarget</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-get-target-kind">
  <div class="api-method-name">GetTargetKind()</div>
  <p class="api-method-summary">Returns the active debug target kind.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-get-target-value">
  <div class="api-method-name">GetTargetValue()</div>
  <p class="api-method-summary">Returns the active debug target value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-get-target-revision">
  <div class="api-method-name">GetTargetRevision()</div>
  <p class="api-method-summary">Returns the active debug target revision.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-get-target-summary">
  <div class="api-method-name">GetTargetSummary()</div>
  <p class="api-method-summary">Returns a display string for the active debug target.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-get-console-summary">
  <div class="api-method-name">GetConsoleSummary()</div>
  <p class="api-method-summary">Returns a display string for the main Echo Console hub status.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-start-instance-pick">
  <div class="api-method-name">StartInstancePick()</div>
  <p class="api-method-summary">Starts instance pick mode.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-console-manager">EchoConsoleManager</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-cancel-pick">
  <div class="api-method-name">CancelPick()</div>
  <p class="api-method-summary">Cancels active debug pick mode.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-console-manager">EchoConsoleManager</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-is-picking">
  <div class="api-method-name">IsPicking()</div>
  <p class="api-method-summary">Returns whether any debug pick mode is active.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-is-picking-instance">
  <div class="api-method-name">IsPickingInstance()</div>
  <p class="api-method-summary">Returns whether instance pick mode is active.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-get-pick-mode">
  <div class="api-method-name">GetPickMode()</div>
  <p class="api-method-summary">Returns the active debug pick mode.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Real</span>
      <span class="api-return-description">Uses the <a href="#enum-e-echo-chamber-debug-pick-mode"><code>eEchoChamberDebugPickMode</code></a> enum.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-get-pick-hover-instance">
  <div class="api-method-name">GetPickHoverInstance()</div>
  <p class="api-method-summary">Returns the currently hovered instance while picking.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Id.Instance|Constant.Noone</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-add-instance-variable-watch">
  <div class="api-method-name">AddInstanceVariableWatch(instance, variable_name)</div>
  <p class="api-method-summary">Adds an instance-variable watch.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">instance</span>
      <span class="api-argument-type">Id.Instance</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">variable_name</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Real</span>
      <span class="api-return-description">Watch ID, or -1 when the watch could not be added.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-add-global-watch">
  <div class="api-method-name">AddGlobalWatch(key)</div>
  <p class="api-method-summary">Adds a global-variable watch.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Real</span>
      <span class="api-return-description">Watch ID, or -1 when the watch could not be added.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-add-callback-watch">
  <div class="api-method-name">AddCallbackWatch(label, callback)</div>
  <p class="api-method-summary">Adds a callback watch.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">label</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Real</span>
      <span class="api-return-description">Watch ID, or -1 when the watch could not be added.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-remove-watch">
  <div class="api-method-name">RemoveWatch(watch_id)</div>
  <p class="api-method-summary">Removes a watch.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">watch_id</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-clear-watches">
  <div class="api-method-name">ClearWatches()</div>
  <p class="api-method-summary">Clears all watches.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-console-manager">EchoConsoleManager</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-start-input-recording">
  <div class="api-method-name">StartInputRecording(filter)</div>
  <p class="api-method-summary">Starts GameMaker debug input recording.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">filter</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses debug_input_filter_* constants.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-stop-input-recording">
  <div class="api-method-name">StopInputRecording(filename)</div>
  <p class="api-method-summary">Stops and save the current GameMaker debug input recording.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">filename</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-play-input-recording">
  <div class="api-method-name">PlayInputRecording(filename)</div>
  <p class="api-method-summary">Plays a saved GameMaker debug input recording.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">filename</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-handle-async-system">
  <div class="api-method-name">HandleAsyncSystem(async_load)</div>
  <p class="api-method-summary">Routes an Async System event to the debug manager.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">async_load</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Async System event DS map ID.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-build-watches-snapshot-text">
  <div class="api-method-name">BuildWatchesSnapshotText()</div>
  <p class="api-method-summary">Builds a text report of current Echo Watches.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-capture-snapshot">
  <div class="api-method-name">CaptureSnapshot()</div>
  <p class="api-method-summary">Captures an Echo Snapshot report.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-copy-snapshot">
  <div class="api-method-name">CopySnapshot()</div>
  <p class="api-method-summary">Copies the latest Echo Snapshot report to the clipboard.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-save-snapshot">
  <div class="api-method-name">SaveSnapshot()</div>
  <p class="api-method-summary">Saves the latest Echo Snapshot report to a text file.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-clear-saved-snapshots">
  <div class="api-method-name">ClearSavedSnapshots()</div>
  <p class="api-method-summary">Clears saved Echo Snapshot reports from the current window session.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-console-manager">EchoConsoleManager</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-enable-crash-capture">
  <div class="api-method-name">EnableCrashCapture([chain_previous])</div>
  <p class="api-method-summary">Enables Echo Crash Reports capture.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">chain_previous <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-disable-crash-capture">
  <div class="api-method-name">DisableCrashCapture()</div>
  <p class="api-method-summary">Disables Echo Crash Reports capture.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-has-crash-report">
  <div class="api-method-name">HasCrashReport()</div>
  <p class="api-method-summary">Returns whether a saved Echo Crash Report exists.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-copy-crash-report">
  <div class="api-method-name">CopyCrashReport()</div>
  <p class="api-method-summary">Copies the saved Echo Crash Report to the clipboard.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-clear-crash-report">
  <div class="api-method-name">ClearCrashReport()</div>
  <p class="api-method-summary">Clears the saved Echo Crash Report.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-get-crash-report-text">
  <div class="api-method-name">GetCrashReportText()</div>
  <p class="api-method-summary">Returns the saved Echo Crash Report text.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-add-command">
  <div class="api-method-name">AddCommand(key, description, args, callback)</div>
  <p class="api-method-summary">Adds a custom Echo Console command. Keys are normalized by Echo Console. Duplicate keys, invalid argument definitions, and non-callable callbacks return false.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">description</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">args</span>
      <span class="api-argument-type">Array&lt;Struct.<a href="#echo-console-command-arg">EchoConsoleCommandArg</a>&gt;</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_args, _context)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-unregister-command">
  <div class="api-method-name">UnregisterCommand(key)</div>
  <p class="api-method-summary">Unregister a custom Echo Console command.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-run-command">
  <div class="api-method-name">RunCommand(text)</div>
  <p class="api-method-summary">Runs an Echo Console command line.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">text</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-get-command-output">
  <div class="api-method-name">GetCommandOutput()</div>
  <p class="api-method-summary">Returns the latest command output text.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-get-command-output-is-error">
  <div class="api-method-name">GetCommandOutputIsError()</div>
  <p class="api-method-summary">Returns whether the latest command output is an error.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-get-previous-command">
  <div class="api-method-name">GetPreviousCommand(current_text)</div>
  <p class="api-method-summary">Returns the previous command history entry.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">current_text</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-get-next-command">
  <div class="api-method-name">GetNextCommand(current_text)</div>
  <p class="api-method-summary">Returns the next command history entry.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">current_text</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-get-pick-hover-count">
  <div class="api-method-name">GetPickHoverCount()</div>
  <p class="api-method-summary">Returns the number of valid instances currently under the picker.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-register-target-listener">
  <div class="api-method-name">RegisterTargetListener(key, fn)</div>
  <p class="api-method-summary">Registers a callback fired when the active debug target changes. Reusing a key replaces the existing listener callback.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-unregister-target-listener">
  <div class="api-method-name">UnregisterTargetListener(key)</div>
  <p class="api-method-summary">Removes a target-change listener by key.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-register-window-opener">
  <div class="api-method-name">RegisterWindowOpener(key, fn)</div>
  <p class="api-method-summary">Registers a debug window opener.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-unregister-window-opener">
  <div class="api-method-name">UnregisterWindowOpener(key)</div>
  <p class="api-method-summary">Removes a debug window opener by key.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-open-window">
  <div class="api-method-name">OpenWindow(key)</div>
  <p class="api-method-summary">Opens a registered debug window.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-open-command-help">
  <div class="api-method-name">OpenCommandHelp([key])</div>
  <p class="api-method-summary">Opens the Echo Command Help window.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-reset-built-in-window-layouts">
  <div class="api-method-name">ResetBuiltInWindowLayouts()</div>
  <p class="api-method-summary">Resets Echo Console and built-in debug window layouts.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-register-overlay-drawer">
  <div class="api-method-name">RegisterOverlayDrawer(key, fn)</div>
  <p class="api-method-summary">Registers a debug GUI overlay drawer. Overlay drawers run behind Echo Chamber windows during debug overlay drawing.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-manager-unregister-overlay-drawer">
  <div class="api-method-name">UnregisterOverlayDrawer(key)</div>
  <p class="api-method-summary">Removes a debug GUI overlay drawer by key.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

## Themes

### EchoChamberTheme
{: #echo-chamber-theme .api-type-title }

Creates the shared Echo Chamber theme used by Statement Lens.

```gml
new EchoChamberTheme()
```

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#echo-chamber-theme-get-generation"><code>GetGeneration()</code></a></td><td>Returns the generation. The generation increments when theme metrics or style defaults are refreshed. Echo Chamber uses it to invalidate cached resolved styles.</td></tr>
<tr><td><a href="#echo-chamber-theme-get-header-font"><code>GetHeaderFont()</code></a></td><td>Returns the theme font used for headers and window chrome.</td></tr>
<tr><td><a href="#echo-chamber-theme-set-header-font"><code>SetHeaderFont()</code></a></td><td>Sets the theme header font and propagate it to styles still following the header role.</td></tr>
<tr><td><a href="#echo-chamber-theme-get-body-font"><code>GetBodyFont()</code></a></td><td>Returns the theme font used for normal control and body text.</td></tr>
<tr><td><a href="#echo-chamber-theme-set-body-font"><code>SetBodyFont()</code></a></td><td>Sets the theme body font and propagate it to styles still following the body role.</td></tr>
<tr><td><a href="#echo-chamber-theme-get-small-font"><code>GetSmallFont()</code></a></td><td>Returns the theme font used for compact and informational text.</td></tr>
<tr><td><a href="#echo-chamber-theme-set-small-font"><code>SetSmallFont()</code></a></td><td>Sets the theme small font and propagate it to styles still following the small role.</td></tr>
<tr><td><a href="#echo-chamber-theme-refresh-metrics"><code>RefreshMetrics()</code></a></td><td>Recompute row heights based on current fonts and padding. Recomputes row heights from the current fonts and padding, then refreshes theme-owned style metrics. Call this after changing theme fonts, scale, or base spacing fields directly.</td></tr>
</tbody></table>

<div class="api-method-entry" id="echo-chamber-theme-get-generation">
  <div class="api-method-name">GetGeneration()</div>
  <p class="api-method-summary">Returns the generation. The generation increments when theme metrics or style defaults are refreshed. Echo Chamber uses it to invalidate cached resolved styles.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-theme-get-header-font">
  <div class="api-method-name">GetHeaderFont()</div>
  <p class="api-method-summary">Returns the theme font used for headers and window chrome.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Asset.GMFont</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-theme-set-header-font">
  <div class="api-method-name">SetHeaderFont(font)</div>
  <p class="api-method-summary">Sets the theme header font and propagate it to styles still following the header role.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">font</span>
      <span class="api-argument-type">String|Asset.GMFont</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-theme">EchoChamberTheme</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-theme-get-body-font">
  <div class="api-method-name">GetBodyFont()</div>
  <p class="api-method-summary">Returns the theme font used for normal control and body text.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Asset.GMFont</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-theme-set-body-font">
  <div class="api-method-name">SetBodyFont(font)</div>
  <p class="api-method-summary">Sets the theme body font and propagate it to styles still following the body role.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">font</span>
      <span class="api-argument-type">String|Asset.GMFont</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-theme">EchoChamberTheme</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-theme-get-small-font">
  <div class="api-method-name">GetSmallFont()</div>
  <p class="api-method-summary">Returns the theme font used for compact and informational text.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Asset.GMFont</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-theme-set-small-font">
  <div class="api-method-name">SetSmallFont(font)</div>
  <p class="api-method-summary">Sets the theme small font and propagate it to styles still following the small role.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">font</span>
      <span class="api-argument-type">String|Asset.GMFont</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-theme">EchoChamberTheme</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-theme-refresh-metrics">
  <div class="api-method-name">RefreshMetrics()</div>
  <p class="api-method-summary">Recompute row heights based on current fonts and padding. Recomputes row heights from the current fonts and padding, then refreshes theme-owned style metrics. Call this after changing theme fonts, scale, or base spacing fields directly.</p>
</div>

### EchoChamberThemeMidnightNeon
{: #echo-chamber-theme-midnight-neon .api-type-title }

Dark midnight blues with neon purple accent.

Inherits from [`EchoChamberTheme`](#echo-chamber-theme).

```gml
new EchoChamberThemeMidnightNeon()
```

### EchoChamberThemePhosphorTerminal
{: #echo-chamber-theme-phosphor-terminal .api-type-title }

Creates a warm phosphor-green terminal theme with ivory text and restrained brass diagnostics.

Inherits from [`EchoChamberThemeMidnightNeon`](#echo-chamber-theme-midnight-neon).

```gml
new EchoChamberThemePhosphorTerminal()
```

### EchoChamberThemeBiohazardConsole
{: #echo-chamber-theme-biohazard-console .api-type-title }

Creates an industrial charcoal-and-olive theme with acid green controls and hazard-yellow accents.

Inherits from [`EchoChamberThemeMidnightNeon`](#echo-chamber-theme-midnight-neon).

```gml
new EchoChamberThemeBiohazardConsole()
```

### EchoChamberThemeEmeraldUltraviolet
{: #echo-chamber-theme-emerald-ultraviolet .api-type-title }

Creates a blackened aubergine theme with saturated emerald controls and ultraviolet counter-accents.

Inherits from [`EchoChamberThemeMidnightNeon`](#echo-chamber-theme-midnight-neon).

```gml
new EchoChamberThemeEmeraldUltraviolet()
```

### EchoChamberThemeAmberForest
{: #echo-chamber-theme-amber-forest .api-type-title }

Forest greens with warm amber highlights.

Inherits from [`EchoChamberTheme`](#echo-chamber-theme).

```gml
new EchoChamberThemeAmberForest()
```

### EchoChamberThemeSakuraPunch
{: #echo-chamber-theme-sakura-punch .api-type-title }

Inky plum with candy pink accents.

Inherits from [`EchoChamberTheme`](#echo-chamber-theme).

```gml
new EchoChamberThemeSakuraPunch()
```

### EchoChamberThemeArcadeWave
{: #echo-chamber-theme-arcade-wave .api-type-title }

Retro arcade navy with bright cyan accents.

Inherits from [`EchoChamberTheme`](#echo-chamber-theme).

```gml
new EchoChamberThemeArcadeWave()
```

### EchoChamberThemeCircuitCandy
{: #echo-chamber-theme-circuit-candy .api-type-title }

Playful teal and orange on a soft dark background.

Inherits from [`EchoChamberTheme`](#echo-chamber-theme).

```gml
new EchoChamberThemeCircuitCandy()
```

### EchoChamberThemeToxicTerminal
{: #echo-chamber-theme-toxic-terminal .api-type-title }

Acid terminal green with rogue magenta highlights.

Inherits from [`EchoChamberTheme`](#echo-chamber-theme).

```gml
new EchoChamberThemeToxicTerminal()
```

### EchoChamberThemeSunsetGlitch
{: #echo-chamber-theme-sunset-glitch .api-type-title }

Sunset oranges colliding with cyan and grape.

Inherits from [`EchoChamberTheme`](#echo-chamber-theme).

```gml
new EchoChamberThemeSunsetGlitch()
```

### EchoChamberThemeBubblegumTerminal
{: #echo-chamber-theme-bubblegum-terminal .api-type-title }

Bubblegum pink UI with teal statement nodes.

Inherits from [`EchoChamberTheme`](#echo-chamber-theme).

```gml
new EchoChamberThemeBubblegumTerminal()
```

### EchoChamberThemeMangoMint
{: #echo-chamber-theme-mango-mint .api-type-title }

Warm mango chrome with mint green graph.

Inherits from [`EchoChamberTheme`](#echo-chamber-theme).

```gml
new EchoChamberThemeMangoMint()
```

## Top-level functions

### Root and lifecycle
{: .api-function-subsection-title .api-function-subsection-title-first }

<div class="api-method-entry" id="get-echo-chamber-root">
  <div class="api-method-name">GetEchoChamberRoot()</div>
  <p class="api-method-summary">Returns the default Echo Chamber root. This returns the default global root used by the bundled setup, creating it first if needed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-return-description">Default Echo Chamber root.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#ensure-echo-chamber-root"><code>EnsureEchoChamberRoot</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-root"><code>EchoChamberRoot</code></a></div>
  </div>
</div>

<div class="api-method-entry" id="ensure-echo-chamber-root">
  <div class="api-method-name">EnsureEchoChamberRoot()</div>
  <p class="api-method-summary">Ensures the existence of the default Echo Chamber root. Creates <code>global.__echo_chamber_root</code> when it doesn&#x27;t exist or isn&#x27;t an <a href="#echo-chamber-root"><code>EchoChamberRoot</code></a>.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Undefined</span>
      <span class="api-return-description">No return value.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#get-echo-chamber-root"><code>GetEchoChamberRoot</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-root"><code>EchoChamberRoot</code></a></div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-release-gpu-resources">
  <div class="api-method-name">EchoChamberReleaseGpuResources()</div>
  <p class="api-method-summary">Releases cached GPU resources owned by Echo Chamber. Call this when you need Echo Chamber to discard GPU-backed caches, such as during resource/device lifecycle handling. Currently releases the built-in window chrome icon buffer cache.</p>
</div>

### Input
{: .api-function-subsection-title }

<div class="api-method-entry" id="echo-chamber-input-format-key">
  <div class="api-method-name">EchoChamberInputFormatKey(key)</div>
  <p class="api-method-summary">Formats a keyboard key code for display.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Keyboard keycode (vk_* or ord()).</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-input-format-binding">
  <div class="api-method-name">EchoChamberInputFormatBinding(binding)</div>
  <p class="api-method-summary">Formats an input binding for display in help text or menu shortcuts.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">binding</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-input-binding">EchoChamberInputBinding</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

### Echo Console
{: .api-function-subsection-title }

<div class="api-method-entry" id="echo-chamber-open-console">
  <div class="api-method-name">EchoChamberOpenConsole(ui_root)</div>
  <p class="api-method-summary">Opens the built-in Echo Console window, creating it if needed. Pass the root you&#x27;re actually drawing with <code>RunDesktop()</code>.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|Undefined</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-console-get-manager"><code>EchoConsoleGetManager</code></a> <span aria-hidden="true">·</span> <a href="#echo-console-manager"><code>EchoConsoleManager</code></a></div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-get-manager">
  <div class="api-method-name">EchoConsoleGetManager(ui_root)</div>
  <p class="api-method-summary">Returns the shared Echo Chamber debug manager for a root. Returns <code>undefined</code> when <code>_ui_root</code> isn&#x27;t an <a href="#echo-chamber-root"><code>EchoChamberRoot</code></a>.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-console-manager">EchoConsoleManager</a>|Undefined</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-console-manager"><code>EchoConsoleManager</code></a> <span aria-hidden="true">·</span> <a href="#get-echo-chamber-root"><code>GetEchoChamberRoot</code></a></div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-set-instance-target">
  <div class="api-method-name">EchoConsoleSetInstanceTarget(ui_root, instance)</div>
  <p class="api-method-summary">Sets the active Echo Chamber debug target to an instance. Returns false when the root is invalid, the instance is <code>noone</code>, or the instance no longer exists.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">instance</span>
      <span class="api-argument-type">Id.Instance</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-clear-target">
  <div class="api-method-name">EchoConsoleClearTarget(ui_root)</div>
  <p class="api-method-summary">Clears the active Echo Chamber debug target.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-get-target">
  <div class="api-method-name">EchoConsoleGetTarget(ui_root)</div>
  <p class="api-method-summary">Returns the active Echo Chamber debug target.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-console-target">EchoConsoleTarget</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-open-window">
  <div class="api-method-name">EchoConsoleOpenWindow(ui_root, key)</div>
  <p class="api-method-summary">Opens a registered Echo Chamber debug window. Built-in keys use the <code>ECHO_DEBUG_WINDOW_*</code> macros. Custom keys must be registered with <code>RegisterWindowOpener()</code>.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-start-instance-pick">
  <div class="api-method-name">EchoConsoleStartInstancePick(ui_root)</div>
  <p class="api-method-summary">Starts Echo Chamber instance pick mode. Starts instance-pick mode. Left click selects an instance, while right click or Cancel exits pick mode.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-cancel-pick">
  <div class="api-method-name">EchoConsoleCancelPick(ui_root)</div>
  <p class="api-method-summary">Cancels the active Echo Chamber debug pick mode.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-is-picking">
  <div class="api-method-name">EchoConsoleIsPicking(ui_root)</div>
  <p class="api-method-summary">Returns whether Echo Chamber debug pick mode is active.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-add-instance-watch">
  <div class="api-method-name">EchoConsoleAddInstanceWatch(ui_root, instance, variable_name)</div>
  <p class="api-method-summary">Adds an instance-variable watch to the Echo Watches window.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">instance</span>
      <span class="api-argument-type">Id.Instance</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">variable_name</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Real</span>
      <span class="api-return-description">Watch ID, or -1 when the watch could not be added.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-add-global-watch">
  <div class="api-method-name">EchoConsoleAddGlobalWatch(ui_root, key)</div>
  <p class="api-method-summary">Adds a global-variable watch to the Echo Watches window.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Real</span>
      <span class="api-return-description">Watch ID, or -1 when the watch could not be added.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-add-callback-watch">
  <div class="api-method-name">EchoConsoleAddCallbackWatch(ui_root, label, callback)</div>
  <p class="api-method-summary">Adds a callback watch to the Echo Watches window. The callback is evaluated by Echo Watches and its return value is displayed as the watched value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">label</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Real</span>
      <span class="api-return-description">Watch ID, or -1 when the watch could not be added.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-remove-watch">
  <div class="api-method-name">EchoConsoleRemoveWatch(ui_root, watch_id)</div>
  <p class="api-method-summary">Removes a watch from the Echo Watches window.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">watch_id</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-clear-watches">
  <div class="api-method-name">EchoConsoleClearWatches(ui_root)</div>
  <p class="api-method-summary">Removes all watches from the Echo Watches window.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-add-command">
  <div class="api-method-name">EchoConsoleAddCommand(ui_root, key, description, args, callback)</div>
  <p class="api-method-summary">Adds a custom Echo Console command. <code>_callback</code> is called as <code>function(_args, _context)</code>. See <a href="#echo-console-command-arg"><code>EchoConsoleCommandArg()</code></a> for parsed argument and context details.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">description</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">args</span>
      <span class="api-argument-type">Array&lt;Struct.<a href="#echo-console-command-arg">EchoConsoleCommandArg</a>&gt;</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">function(_args, _context)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-unregister-command">
  <div class="api-method-name">EchoConsoleUnregisterCommand(ui_root, key)</div>
  <p class="api-method-summary">Unregister a custom Echo Console command. Built-in commands can&#x27;t be unregistered.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-run-command">
  <div class="api-method-name">EchoConsoleRunCommand(ui_root, text)</div>
  <p class="api-method-summary">Runs an Echo Console command. Runs the command through the same parser used by Echo Console and updates the latest command output text.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">text</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-capture-snapshot">
  <div class="api-method-name">EchoConsoleCaptureSnapshot(ui_root)</div>
  <p class="api-method-summary">Captures an Echo Snapshot report from the current runtime state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-copy-snapshot">
  <div class="api-method-name">EchoConsoleCopySnapshot(ui_root)</div>
  <p class="api-method-summary">Captures an Echo Snapshot report and copies it to the clipboard.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-save-snapshot">
  <div class="api-method-name">EchoConsoleSaveSnapshot(ui_root)</div>
  <p class="api-method-summary">Captures an Echo Snapshot report and saves it to a text file.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-clear-saved-snapshots">
  <div class="api-method-name">EchoConsoleClearSavedSnapshots(ui_root)</div>
  <p class="api-method-summary">Clears saved Echo Snapshot reports from the current window session.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-enable-crash-capture">
  <div class="api-method-name">EchoConsoleEnableCrashCapture(ui_root, [chain_previous])</div>
  <p class="api-method-summary">Enables Echo Crash Reports capture for unhandled exceptions. <code>_chain_previous</code> defaults to true and lets the previous unhandled-exception handler run after Echo captures the report.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">chain_previous <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-disable-crash-capture">
  <div class="api-method-name">EchoConsoleDisableCrashCapture(ui_root)</div>
  <p class="api-method-summary">Disables Echo Crash Reports capture and restore the previous unhandled-exception handler.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-has-crash-report">
  <div class="api-method-name">EchoConsoleHasCrashReport(ui_root)</div>
  <p class="api-method-summary">Returns whether Echo has a saved last-crash report.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-copy-crash-report">
  <div class="api-method-name">EchoConsoleCopyCrashReport(ui_root)</div>
  <p class="api-method-summary">Copies the saved Echo Crash Report to the clipboard.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-clear-crash-report">
  <div class="api-method-name">EchoConsoleClearCrashReport(ui_root)</div>
  <p class="api-method-summary">Delete the saved Echo Crash Report.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-start-input-recording">
  <div class="api-method-name">EchoConsoleStartInputRecording(ui_root, filter)</div>
  <p class="api-method-summary">Starts GameMaker debug input recording.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">filter</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses debug_input_filter_* constants.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-stop-input-recording">
  <div class="api-method-name">EchoConsoleStopInputRecording(ui_root, filename)</div>
  <p class="api-method-summary">Stops and save the current GameMaker debug input recording.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">filename</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-play-input-recording">
  <div class="api-method-name">EchoConsolePlayInputRecording(ui_root, filename)</div>
  <p class="api-method-summary">Plays a saved GameMaker debug input recording.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">filename</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-open-data-structure-scanner">
  <div class="api-method-name">EchoConsoleOpenDataStructureScanner(ui_root)</div>
  <p class="api-method-summary">Opens the Echo Data Structure Scanner window.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#echo-chamber-window">EchoChamberWindow</a>|Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-console-handle-async-system">
  <div class="api-method-name">EchoConsoleHandleAsyncSystem(ui_root, async_load)</div>
  <p class="api-method-summary">Routes an Async System event to Echo Console debug systems. Call this from an Async System event when using the input recording playback helpers.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.<a href="#echo-chamber-root">EchoChamberRoot</a></span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">async_load</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Async System event DS map ID.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

### Library integration
{: .api-function-subsection-title }

<div class="api-method-entry" id="echo-console-library-registration">
  <div class="api-method-name">EchoConsoleLibraryRegistration(name, launcher, debug_enabled)</div>
  <p class="api-method-summary">Echo Console supports up to thirty library registrations. The Console reads them when its hub is built, so register a library before opening the Console if you want it to appear immediately.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">The name of the library</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">launcher</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">The function that launches the libraries debug panel/interactive elements</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">debug_enabled</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether the library should show up in Echo Console or not</span>
    </div>
  </div>
</div>

### Theme assets
{: .api-function-subsection-title }

<div class="api-method-entry" id="echo-chamber-theme-try-get-font">
  <div class="api-method-name">EchoChamberThemeTryGetFont(font_name)</div>
  <p class="api-method-summary">Returns a font asset by name. If missing, returns the current draw font. Passing a valid font asset returns that asset. Passing a string resolves the asset name with <code>asset_get_index()</code>.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">font_name</span>
      <span class="api-argument-type">String|Asset.GMFont</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Asset.GMFont</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-theme-try-get-sprite"><code>EchoChamberThemeTryGetSprite</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-theme"><code>EchoChamberTheme</code></a></div>
  </div>
</div>

<div class="api-method-entry" id="echo-chamber-theme-try-get-sprite">
  <div class="api-method-name">EchoChamberThemeTryGetSprite(sprite_name)</div>
  <p class="api-method-summary">Returns a sprite asset by name. If missing, returns -1. Passing a valid sprite asset returns that asset. Passing a string resolves the asset name with <code>asset_get_index()</code>.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">sprite_name</span>
      <span class="api-argument-type">String|Asset.GMSprite</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Asset.GMSprite|Real</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-theme-try-get-font"><code>EchoChamberThemeTryGetFont</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-theme"><code>EchoChamberTheme</code></a></div>
  </div>
</div>

## Enums

### Layout and drawing

<div class="api-enum-entry" id="enum-e-echo-chamber-dock">
  <div class="api-enum-name">eEchoChamberDock</div>
  <p>Chooses how a panel claims space from its parent. Echo Chamber lays out <code>TOP</code>, <code>BOTTOM</code>, <code>LEFT</code>, and <code>RIGHT</code> edge strips first, then gives <code>FILL</code> whatever space remains. Panels that use the same dock direction are handled in their added order.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">FILL</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">TOP</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">BOTTOM</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">LEFT</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">RIGHT</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-chrome-button-slot">
  <div class="api-enum-name">eEchoChamberChromeButtonSlot</div>
  <p>Identifies which title-bar button on a window you want to style or address.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">CLOSE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">MINIMISE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">PIN</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-chrome-icon">
  <div class="api-enum-name">eEchoChamberChromeIcon</div>
  <p>Names the built-in icon meaning used by window title-bar buttons.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">CLOSE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">MINIMISE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">MAXIMISE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">RESTORE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">PIN</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">UNPIN</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-chrome-icon-state">
  <div class="api-enum-name">eEchoChamberChromeIconState</div>
  <p>Describes the current visual state of a title-bar icon so a style can provide different visuals for normal, hovered, pressed, or disabled states.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">NORMAL</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">HOVER</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">DOWN</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">DISABLED</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-chrome-icon-visual-kind">
  <div class="api-enum-name">eEchoChamberChromeIconVisualKind</div>
  <p>Chooses how a title-bar icon is represented: not drawn, drawn from a sprite, drawn from Echo Chamber&#x27;s built-in buffer, or drawn as text.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">NONE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">SPRITE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">BUILTIN_BUFFER</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">TEXT</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-collapse">
  <div class="api-enum-name">eEchoChamberCollapse</div>
  <p>Controls whether a panel can collapse and, when it can, which edge it collapses toward.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">NONE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">TO_LEFT</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">TO_RIGHT</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">TO_TOP</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">TO_BOTTOM</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-panel-size-mode">
  <div class="api-enum-name">eEchoChamberPanelSizeMode</div>
  <p>Chooses whether a docked panel uses an explicit thickness (<code>FIXED</code>) or sizes that thickness from its contents (<code>FIT_CONTENT</code>). For top/bottom panels the thickness is height, while for left/right panels it&#x27;s width.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">FIXED</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">FIT_CONTENT</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-panel-flow">
  <div class="api-enum-name">eEchoChamberPanelFlow</div>
  <p>Chooses how a panel arranges its direct controls. <code>ROW</code> packs controls across rows and can wrap, while <code>COLUMN</code> stacks them vertically.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">ROW</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">COLUMN</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-panel-row-align">
  <div class="api-enum-name">eEchoChamberPanelRowAlign</div>
  <p>When a packed row doesn&#x27;t use the full available width, chooses whether that row sits at the start, centre, or end.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">START</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">CENTER</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">END</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-panel-row-distribution">
  <div class="api-enum-name">eEchoChamberPanelRowDistribution</div>
  <p>Controls horizontal space inside packed rows. <code>PACK</code> keeps controls at their desired widths, while <code>FILL</code> distributes available row width to controls that are allowed to fill.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">PACK</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">FILL</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-align-hor">
  <div class="api-enum-name">eEchoChamberAlignHor</div>
  <p>General left/centre/right alignment used by layouts, popups, and styles.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">LEFT</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">CENTER</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">RIGHT</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-align-ver">
  <div class="api-enum-name">eEchoChamberAlignVer</div>
  <p>General top/middle/bottom alignment used by layouts and styles.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">TOP</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">MIDDLE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">BOTTOM</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-box-shape">
  <div class="api-enum-name">eEchoChamberBoxShape</div>
  <p>Chooses the shape drawn by style surfaces that support rectangular or rounded boxes.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">RECTANGLE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">ROUNDRECT</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">NUM</span>
      <span class="api-enum-description">Enum sentinel. Use RECTANGLE or ROUNDRECT for style SetShape() calls.</span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-label-placement">
  <div class="api-enum-name">eEchoChamberLabelPlacement</div>
  <p>Chooses where a control&#x27;s separate form label is drawn. <code>LEADING</code> places it beside the control, <code>ABOVE</code> puts it above, <code>NONE</code> hides it, and <code>AUTO</code> lets the panel/style choose based on available room.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">AUTO</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">LEADING</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">ABOVE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">NONE</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-label-align">
  <div class="api-enum-name">eEchoChamberLabelAlign</div>
  <p>Chooses the horizontal alignment of label text. <code>AUTO</code> leaves the choice to the active label style and placement rules.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">AUTO</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">LEFT</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">CENTER</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">RIGHT</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

### Popup and controls

<div class="api-enum-entry" id="enum-e-echo-chamber-popup-direction">
  <div class="api-enum-name">eEchoChamberPopupDirection</div>
  <p>Chooses whether an anchored popup prefers to open below or above its anchor, or lets Echo Chamber choose from the available space.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">DOWN</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">UP</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">AUTO</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-color-popup-visual-space">
  <div class="api-enum-name">eEchoChamberColorPopupVisualSpace</div>
  <p>Chooses whether the colour picker presents its colour controls in HSV or HSL space.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">HSV</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">HSL</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-color-button-value-text-mode">
  <div class="api-enum-name">eEchoChamberColorButtonValueTextMode</div>
  <p>Chooses whether a colour button also prints the current RGB value as text.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">NONE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">RGB</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-slider-value-position">
  <div class="api-enum-name">eEchoChamberSliderValuePosition</div>
  <p>Chooses whether a slider&#x27;s displayed value text appears above or below the slider body.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">ABOVE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">BELOW</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-validation-kind">
  <div class="api-enum-name">eEchoChamberValidationKind</div>
  <p>Describes how serious a validation message is when a text control reports a problem or informational note.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">ERROR</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">WARN</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">INFO</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-validation-display">
  <div class="api-enum-name">eEchoChamberValidationDisplay</div>
  <p>Chooses whether validation feedback is shown inline, as a tooltip, or chosen automatically.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">AUTO</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">INLINE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">TOOLTIP</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-separator-orientation">
  <div class="api-enum-name">eEchoChamberSeparatorOrientation</div>
  <p>Chooses whether a separator control draws horizontally or vertically.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">HORIZONTAL</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">VERTICAL</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-binding-kind">
  <div class="api-enum-name">eEchoChamberBindingKind</div>
  <p>Internal storage mode used by dynamic control bindings. Configure bindings with the relevant Bind*() method instead of assigning this enum directly.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">NONE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">STRUCT_FIELD</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">FUNCTION_PAIR</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">FIELD_BINDING</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">NUM</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

### Input

<div class="api-enum-entry" id="enum-e-echo-chamber-input-check">
  <div class="api-enum-name">eEchoChamberInputCheck</div>
  <p>Chooses which moment of a key/input action counts: the first press, every frame it&#x27;s held, or the release.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">PRESSED</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">DOWN</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">RELEASED</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-input-bind-kind">
  <div class="api-enum-name">eEchoChamberInputBindKind</div>
  <p>Describes whether a named Echo Chamber action is connected to a keyboard key, a custom function, or deliberately blocked from parent-context fallback.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">KEY</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">FUNC</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">BLOCK</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

### Echo Console

<div class="api-enum-entry" id="enum-e-echo-chamber-debug-theme">
  <div class="api-enum-name">eEchoChamberDebugTheme</div>
  <p>Chooses the dedicated visual theme used by Echo Console and the other built-in debugger windows.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">PHOSPHOR_TERMINAL</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">BIOHAZARD_CONSOLE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">EMERALD_ULTRAVIOLET</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-debug-target-kind">
  <div class="api-enum-name">eEchoChamberDebugTargetKind</div>
  <p>Tells the debugger what kind of value is currently selected as its shared target, such as a live instance, struct, global scope, asset, or log entry.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">NONE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">INSTANCE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">STRUCT</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">GLOBAL</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">ASSET</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">LOG_ENTRY</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-console-ds-kind">
  <div class="api-enum-name">eEchoConsoleDsKind</div>
  <p>Lists the GameMaker DS types the Data Structure Scanner knows how to inspect.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">LIST</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">MAP</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">GRID</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">QUEUE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">STACK</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">PRIORITY</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-console-command-arg-type">
  <div class="api-enum-name">eEchoConsoleCommandArgType</div>
  <p>Tells the Console command parser how to turn one typed argument into a GML value. <code>TEXT</code> consumes the rest of the command line and is useful for values containing spaces.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">STRING</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">TEXT</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">REAL</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">INT</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">BOOL</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">ANY</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-console-command-callback-kind">
  <div class="api-enum-name">eEchoConsoleCommandCallbackKind</div>
  <p>Describes whether a registered command callback receives raw command text or arguments that Echo Console has already parsed.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">RAW</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">PARSED</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-debug-pick-mode">
  <div class="api-enum-name">eEchoChamberDebugPickMode</div>
  <p>Describes whether the debugger is currently waiting for the user to click a live instance in the game.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">NONE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">INSTANCE</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-chamber-watch-kind">
  <div class="api-enum-name">eEchoChamberWatchKind</div>
  <p>Describes where a watch gets the value it keeps visible: one instance field, one global field, or a callback that calculates the value.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">INSTANCE_VARIABLE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">GLOBAL_VARIABLE</span>
      <span class="api-enum-description"></span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">CALLBACK</span>
      <span class="api-enum-description"></span>
    </div>
  </div>
</div>

## Macros

### Version

<div class="api-method-entry api-macro-entry api-macro-metadata" id="macro-echo-chamber-version">
  <div class="api-method-name">ECHO_CHAMBER_VERSION</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Value</div>
    <pre class="api-example"><code>&quot;1.0.0&quot;</code></pre>
  </div>
</div>

### Console setup

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-chamber-console-enabled">
  <div class="api-method-name">ECHO_CHAMBER_CONSOLE_ENABLED</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>1</code></pre>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-chamber-console-key">
  <div class="api-method-name">ECHO_CHAMBER_CONSOLE_KEY</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>vk_f1</code></pre>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-chamber-launch-on-startup">
  <div class="api-method-name">ECHO_CHAMBER_LAUNCH_ON_STARTUP</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>false</code></pre>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-chamber-debug-theme">
  <div class="api-method-name">ECHO_CHAMBER_DEBUG_THEME</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>eEchoChamberDebugTheme.EMERALD_ULTRAVIOLET</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#enum-e-echo-chamber-debug-theme"><code>eEchoChamberDebugTheme</code></a></div>
  </div>
</div>

### Core input action ids

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-ui-action-cancel">
  <div class="api-method-name">ECHO_UI_ACTION_CANCEL</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-input-context-bind-action"><code>EchoChamberInputContext.BindAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-ui-action-accept">
  <div class="api-method-name">ECHO_UI_ACTION_ACCEPT</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-input-context-bind-action"><code>EchoChamberInputContext.BindAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-ui-action-tab-next">
  <div class="api-method-name">ECHO_UI_ACTION_TAB_NEXT</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-input-context-bind-action"><code>EchoChamberInputContext.BindAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-ui-action-tab-prev">
  <div class="api-method-name">ECHO_UI_ACTION_TAB_PREV</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-input-context-bind-action"><code>EchoChamberInputContext.BindAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-ui-action-nav-up">
  <div class="api-method-name">ECHO_UI_ACTION_NAV_UP</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-input-context-bind-action"><code>EchoChamberInputContext.BindAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-ui-action-nav-down">
  <div class="api-method-name">ECHO_UI_ACTION_NAV_DOWN</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-input-context-bind-action"><code>EchoChamberInputContext.BindAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-ui-action-page-up">
  <div class="api-method-name">ECHO_UI_ACTION_PAGE_UP</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-input-context-bind-action"><code>EchoChamberInputContext.BindAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-ui-action-page-down">
  <div class="api-method-name">ECHO_UI_ACTION_PAGE_DOWN</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-input-context-bind-action"><code>EchoChamberInputContext.BindAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-ui-action-home">
  <div class="api-method-name">ECHO_UI_ACTION_HOME</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-input-context-bind-action"><code>EchoChamberInputContext.BindAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-ui-action-end">
  <div class="api-method-name">ECHO_UI_ACTION_END</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-input-context-bind-action"><code>EchoChamberInputContext.BindAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-ui-action-restore-windows">
  <div class="api-method-name">ECHO_UI_ACTION_RESTORE_WINDOWS</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-input-context-bind-action"><code>EchoChamberInputContext.BindAction</code></a></div>
  </div>
</div>

### Default core bindings

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-ui-bind-cancel">
  <div class="api-method-name">ECHO_UI_BIND_CANCEL</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(vk_escape)</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#macro-echo-ui-action-cancel"><code>ECHO_UI_ACTION_CANCEL</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-ui-bind-accept">
  <div class="api-method-name">ECHO_UI_BIND_ACCEPT</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(vk_enter)</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#macro-echo-ui-action-accept"><code>ECHO_UI_ACTION_ACCEPT</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-ui-bind-tab-next">
  <div class="api-method-name">ECHO_UI_BIND_TAB_NEXT</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingFunc(function() { return keyboard_check_pressed(vk_tab) &amp;&amp; !keyboard_check(vk_shift); })</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#macro-echo-ui-action-tab-next"><code>ECHO_UI_ACTION_TAB_NEXT</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-ui-bind-tab-prev">
  <div class="api-method-name">ECHO_UI_BIND_TAB_PREV</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingFunc(function() { return keyboard_check_pressed(vk_tab) &amp;&amp; keyboard_check(vk_shift); })</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#macro-echo-ui-action-tab-prev"><code>ECHO_UI_ACTION_TAB_PREV</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-ui-bind-nav-up">
  <div class="api-method-name">ECHO_UI_BIND_NAV_UP</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(vk_up)</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#macro-echo-ui-action-nav-up"><code>ECHO_UI_ACTION_NAV_UP</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-ui-bind-nav-down">
  <div class="api-method-name">ECHO_UI_BIND_NAV_DOWN</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(vk_down)</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#macro-echo-ui-action-nav-down"><code>ECHO_UI_ACTION_NAV_DOWN</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-ui-bind-page-up">
  <div class="api-method-name">ECHO_UI_BIND_PAGE_UP</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(vk_pageup)</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#macro-echo-ui-action-page-up"><code>ECHO_UI_ACTION_PAGE_UP</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-ui-bind-page-down">
  <div class="api-method-name">ECHO_UI_BIND_PAGE_DOWN</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(vk_pagedown)</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#macro-echo-ui-action-page-down"><code>ECHO_UI_ACTION_PAGE_DOWN</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-ui-bind-home">
  <div class="api-method-name">ECHO_UI_BIND_HOME</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(vk_home)</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#macro-echo-ui-action-home"><code>ECHO_UI_ACTION_HOME</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-ui-bind-end">
  <div class="api-method-name">ECHO_UI_BIND_END</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(vk_end)</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#macro-echo-ui-action-end"><code>ECHO_UI_ACTION_END</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-ui-bind-restore-windows">
  <div class="api-method-name">ECHO_UI_BIND_RESTORE_WINDOWS</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(vk_f12)</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#macro-echo-ui-action-restore-windows"><code>ECHO_UI_ACTION_RESTORE_WINDOWS</code></a> <span aria-hidden="true">·</span> <a href="#echo-chamber-root-bind-core-input-action"><code>EchoChamberRoot.BindCoreInputAction</code></a></div>
  </div>
</div>

### Built-in debug window ids

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-debug-window-inspector">
  <div class="api-method-name">ECHO_DEBUG_WINDOW_INSPECTOR</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-console-open-window"><code>EchoConsoleOpenWindow</code></a> <span aria-hidden="true">·</span> <a href="#echo-console-manager-open-window"><code>EchoConsoleManager.OpenWindow</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-debug-window-watches">
  <div class="api-method-name">ECHO_DEBUG_WINDOW_WATCHES</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-console-open-window"><code>EchoConsoleOpenWindow</code></a> <span aria-hidden="true">·</span> <a href="#echo-console-manager-open-window"><code>EchoConsoleManager.OpenWindow</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-debug-window-game">
  <div class="api-method-name">ECHO_DEBUG_WINDOW_GAME</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-console-open-window"><code>EchoConsoleOpenWindow</code></a> <span aria-hidden="true">·</span> <a href="#echo-console-manager-open-window"><code>EchoConsoleManager.OpenWindow</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-debug-window-runtime">
  <div class="api-method-name">ECHO_DEBUG_WINDOW_RUNTIME</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-console-open-window"><code>EchoConsoleOpenWindow</code></a> <span aria-hidden="true">·</span> <a href="#echo-console-manager-open-window"><code>EchoConsoleManager.OpenWindow</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-debug-window-data-structures">
  <div class="api-method-name">ECHO_DEBUG_WINDOW_DATA_STRUCTURES</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-console-open-window"><code>EchoConsoleOpenWindow</code></a> <span aria-hidden="true">·</span> <a href="#echo-console-manager-open-window"><code>EchoConsoleManager.OpenWindow</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-debug-window-command-help">
  <div class="api-method-name">ECHO_DEBUG_WINDOW_COMMAND_HELP</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-console-open-window"><code>EchoConsoleOpenWindow</code></a> <span aria-hidden="true">·</span> <a href="#echo-console-manager-open-window"><code>EchoConsoleManager.OpenWindow</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-debug-window-input">
  <div class="api-method-name">ECHO_DEBUG_WINDOW_INPUT</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-console-open-window"><code>EchoConsoleOpenWindow</code></a> <span aria-hidden="true">·</span> <a href="#echo-console-manager-open-window"><code>EchoConsoleManager.OpenWindow</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-debug-window-crash">
  <div class="api-method-name">ECHO_DEBUG_WINDOW_CRASH</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-console-open-window"><code>EchoConsoleOpenWindow</code></a> <span aria-hidden="true">·</span> <a href="#echo-console-manager-open-window"><code>EchoConsoleManager.OpenWindow</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-debug-window-snapshot">
  <div class="api-method-name">ECHO_DEBUG_WINDOW_SNAPSHOT</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-console-open-window"><code>EchoConsoleOpenWindow</code></a> <span aria-hidden="true">·</span> <a href="#echo-console-manager-open-window"><code>EchoConsoleManager.OpenWindow</code></a></div>
  </div>
</div>

### Console limits

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-console-room-scan-limit">
  <div class="api-method-name">ECHO_CONSOLE_ROOM_SCAN_LIMIT</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>100</code></pre>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-console-ds-scan-limit">
  <div class="api-method-name">ECHO_CONSOLE_DS_SCAN_LIMIT</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>10000</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-console-open-data-structure-scanner"><code>EchoConsoleOpenDataStructureScanner</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-console-ds-inspect-limit">
  <div class="api-method-name">ECHO_CONSOLE_DS_INSPECT_LIMIT</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>200</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-console-open-data-structure-scanner"><code>EchoConsoleOpenDataStructureScanner</code></a></div>
  </div>
</div>

### Text input modes

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-textmode-text">
  <div class="api-method-name">ECHO_TEXTMODE_TEXT</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-text-input-set-input-mode"><code>EchoChamberTextInput.SetInputMode</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-textmode-int">
  <div class="api-method-name">ECHO_TEXTMODE_INT</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-text-input-set-input-mode"><code>EchoChamberTextInput.SetInputMode</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-textmode-float">
  <div class="api-method-name">ECHO_TEXTMODE_FLOAT</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-text-input-set-input-mode"><code>EchoChamberTextInput.SetInputMode</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-textmode-identifier">
  <div class="api-method-name">ECHO_TEXTMODE_IDENTIFIER</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-text-input-set-input-mode"><code>EchoChamberTextInput.SetInputMode</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-textmode-path">
  <div class="api-method-name">ECHO_TEXTMODE_PATH</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-text-input-set-input-mode"><code>EchoChamberTextInput.SetInputMode</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-textmode-code">
  <div class="api-method-name">ECHO_TEXTMODE_CODE</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-text-input-set-input-mode"><code>EchoChamberTextInput.SetInputMode</code></a></div>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-symbol" id="macro-echo-textmode-password">
  <div class="api-method-name">ECHO_TEXTMODE_PASSWORD</div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-chamber-text-input-set-input-mode"><code>EchoChamberTextInput.SetInputMode</code></a></div>
  </div>
</div>

## Symbol index

<div class="api-symbol-index">
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">A</div>
    <div class="api-symbol-row"><a href="#echo-console-manager-add-callback-watch"><code>AddCallbackWatch()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-add-child-panel"><code>AddChildPanel()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-add-command"><code>AddCommand()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-add-control"><code>AddControl()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-add-global-watch"><code>AddGlobalWatch()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-add-instance-variable-watch"><code>AddInstanceVariableWatch()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-add-panel"><code>AddPanel()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-add-panel"><code>AddPanel()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-add-scrollable-panel-body"><code>AddScrollablePanelBody()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-add-transform"><code>AddTransform()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-apply-theme"><code>ApplyTheme()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-apply-theme"><code>ApplyTheme()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">B</div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-begin-layout-batch"><code>BeginLayoutBatch()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-context-bind-action"><code>BindAction()</code></a><span class="api-symbol-owner">EchoChamberInputContext</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-context-bind-block"><code>BindBlock()</code></a><span class="api-symbol-owner">EchoChamberInputContext</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-button-bind-caption"><code>BindCaption()</code></a><span class="api-symbol-owner">EchoChamberButton</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-color-button-bind-color"><code>BindColor()</code></a><span class="api-symbol-owner">EchoChamberColorButton</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-bind-core-input-action"><code>BindCoreInputAction()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-context-bind-func"><code>BindFunc()</code></a><span class="api-symbol-owner">EchoChamberInputContext</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-select-bind-index"><code>BindIndex()</code></a><span class="api-symbol-owner">EchoChamberDropdownSelect</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-context-bind-key"><code>BindKey()</code></a><span class="api-symbol-owner">EchoChamberInputContext</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-base-bind-options"><code>BindOptions()</code></a><span class="api-symbol-owner">EchoChamberDropdownBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-block-bind-text"><code>BindText()</code></a><span class="api-symbol-owner">EchoChamberTextBlock</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-bind-text"><code>BindText()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-slider-bind-value"><code>BindValue()</code></a><span class="api-symbol-owner">EchoChamberSlider</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-toggle-bind-value"><code>BindValue()</code></a><span class="api-symbol-owner">EchoChamberToggle</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-blur-control-focus"><code>BlurControlFocus()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-blur-text-input"><code>BlurTextInput()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-bring-windows-back"><code>BringWindowsBack()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-bring-window-to-front"><code>BringWindowToFront()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-bring-window-to-front-by-id"><code>BringWindowToFrontById()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-build-watches-snapshot-text"><code>BuildWatchesSnapshotText()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">C</div>
    <div class="api-symbol-row"><a href="#echo-console-manager-cancel-pick"><code>CancelPick()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-cancel-text-input"><code>CancelTextInput()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-capture-snapshot"><code>CaptureSnapshot()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-context-clear-action"><code>ClearAction()</code></a><span class="api-symbol-owner">EchoChamberInputContext</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-clear-active-overlay-owner"><code>ClearActiveOverlayOwner()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-clear-child-panels"><code>ClearChildPanels()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-clear-controls"><code>ClearControls()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-clear-crash-report"><code>ClearCrashReport()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-clear-force-size"><code>ClearForceSize()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-button-clear-icon"><code>ClearIcon()</code></a><span class="api-symbol-owner">EchoChamberButton</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-clear-modal-window"><code>ClearModalWindow()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-clear-mouse-capture"><code>ClearMouseCapture()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-clear-panels"><code>ClearPanels()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-clear-saved-snapshots"><code>ClearSavedSnapshots()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-clear-target"><code>ClearTarget()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-clear-theme-override"><code>ClearThemeOverride()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-clear-transforms"><code>ClearTransforms()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-clear-validation-message"><code>ClearValidationMessage()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-clear-watches"><code>ClearWatches()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-close"><code>Close()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-close-color-picker-popup"><code>CloseColorPickerPopup()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-close-context-menu"><code>CloseContextMenu()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-consume-mouse"><code>ConsumeMouse()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-consume-overlay-close-request"><code>ConsumeOverlayCloseRequest()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-consume-wheel"><code>ConsumeWheel()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-contains-point"><code>ContainsPoint()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-copy-crash-report"><code>CopyCrashReport()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-copy-snapshot"><code>CopySnapshot()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-copy-to-clipboard"><code>CopyToClipboard()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-create-input-context"><code>CreateInputContext()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-create-window"><code>CreateWindow()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">D</div>
    <div class="api-symbol-row"><a href="#echo-console-manager-disable-crash-capture"><code>DisableCrashCapture()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-draw"><code>Draw()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-draw-manual"><code>DrawManual()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-base-draw-overlay-row"><code>DrawOverlayRow()</code></a><span class="api-symbol-owner">EchoChamberDropdownBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-toggle-menu-draw-overlay-row"><code>DrawOverlayRow()</code></a><span class="api-symbol-owner">EchoChamberDropdownToggleMenu</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-draw-popup-frame"><code>DrawPopupFrame()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-draw-scroll-area"><code>DrawScrollArea()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-draw-tooltip-text-at"><code>DrawTooltipTextAt()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-dump-ui"><code>DumpUI()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">E</div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-ec-input-down"><code>EC_InputDown()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-ec-input-pressed"><code>EC_InputPressed()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-ec-input-released"><code>EC_InputReleased()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-button"><code>EchoChamberButton</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-color-button"><code>EchoChamberColorButton</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base"><code>EchoChamberControlBase</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-base"><code>EchoChamberDropdownBase</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-select"><code>EchoChamberDropdownSelect</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-toggle-menu"><code>EchoChamberDropdownToggleMenu</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-field-binding"><code>EchoChamberFieldBinding</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-binding"><code>EchoChamberInputBinding</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-binding-block"><code>EchoChamberInputBindingBlock</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-binding-func"><code>EchoChamberInputBindingFunc</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-binding-key"><code>EchoChamberInputBindingKey</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-context"><code>EchoChamberInputContext</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-format-binding"><code>EchoChamberInputFormatBinding()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-format-key"><code>EchoChamberInputFormatKey()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view"><code>EchoChamberListView</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-open-console"><code>EchoChamberOpenConsole()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel"><code>EchoChamberPanel</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-release-gpu-resources"><code>EchoChamberReleaseGpuResources()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root"><code>EchoChamberRoot</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-scroll-state"><code>EchoChamberScrollState</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-separator"><code>EchoChamberSeparator</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-slider"><code>EchoChamberSlider</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-block"><code>EchoChamberTextBlock</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-box"><code>EchoChamberTextBox</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input"><code>EchoChamberTextInput</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme"><code>EchoChamberTheme</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-amber-forest"><code>EchoChamberThemeAmberForest</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-arcade-wave"><code>EchoChamberThemeArcadeWave</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-biohazard-console"><code>EchoChamberThemeBiohazardConsole</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-bubblegum-terminal"><code>EchoChamberThemeBubblegumTerminal</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-circuit-candy"><code>EchoChamberThemeCircuitCandy</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-emerald-ultraviolet"><code>EchoChamberThemeEmeraldUltraviolet</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-mango-mint"><code>EchoChamberThemeMangoMint</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-midnight-neon"><code>EchoChamberThemeMidnightNeon</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-phosphor-terminal"><code>EchoChamberThemePhosphorTerminal</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-sakura-punch"><code>EchoChamberThemeSakuraPunch</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-sunset-glitch"><code>EchoChamberThemeSunsetGlitch</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-toxic-terminal"><code>EchoChamberThemeToxicTerminal</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-try-get-font"><code>EchoChamberThemeTryGetFont()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-try-get-sprite"><code>EchoChamberThemeTryGetSprite()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-toggle"><code>EchoChamberToggle</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window"><code>EchoChamberWindow</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-add-callback-watch"><code>EchoConsoleAddCallbackWatch()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-add-command"><code>EchoConsoleAddCommand()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-add-global-watch"><code>EchoConsoleAddGlobalWatch()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-add-instance-watch"><code>EchoConsoleAddInstanceWatch()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-cancel-pick"><code>EchoConsoleCancelPick()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-capture-snapshot"><code>EchoConsoleCaptureSnapshot()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-clear-crash-report"><code>EchoConsoleClearCrashReport()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-clear-saved-snapshots"><code>EchoConsoleClearSavedSnapshots()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-clear-target"><code>EchoConsoleClearTarget()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-clear-watches"><code>EchoConsoleClearWatches()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-command-arg"><code>EchoConsoleCommandArg</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-copy-crash-report"><code>EchoConsoleCopyCrashReport()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-copy-snapshot"><code>EchoConsoleCopySnapshot()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-disable-crash-capture"><code>EchoConsoleDisableCrashCapture()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-enable-crash-capture"><code>EchoConsoleEnableCrashCapture()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-get-manager"><code>EchoConsoleGetManager()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-get-target"><code>EchoConsoleGetTarget()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-handle-async-system"><code>EchoConsoleHandleAsyncSystem()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-has-crash-report"><code>EchoConsoleHasCrashReport()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-is-picking"><code>EchoConsoleIsPicking()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-library-registration"><code>EchoConsoleLibraryRegistration()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-manager"><code>EchoConsoleManager</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-open-data-structure-scanner"><code>EchoConsoleOpenDataStructureScanner()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-open-window"><code>EchoConsoleOpenWindow()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-play-input-recording"><code>EchoConsolePlayInputRecording()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-remove-watch"><code>EchoConsoleRemoveWatch()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-run-command"><code>EchoConsoleRunCommand()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-save-snapshot"><code>EchoConsoleSaveSnapshot()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-set-instance-target"><code>EchoConsoleSetInstanceTarget()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-start-input-recording"><code>EchoConsoleStartInputRecording()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-start-instance-pick"><code>EchoConsoleStartInstancePick()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-stop-input-recording"><code>EchoConsoleStopInputRecording()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-target"><code>EchoConsoleTarget</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-unregister-command"><code>EchoConsoleUnregisterCommand()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-enable-crash-capture"><code>EnableCrashCapture()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-end-layout-batch"><code>EndLayoutBatch()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#ensure-echo-chamber-root"><code>EnsureEchoChamberRoot()</code></a></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">F</div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-find-control"><code>FindControl()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-find-control"><code>FindControl()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-find-control"><code>FindControl()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-find-panel"><code>FindPanel()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-find-window"><code>FindWindow()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-fit-to-content"><code>FitToContent()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-focus-control"><code>FocusControl()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-focus-text-input"><code>FocusTextInput()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">G</div>
    <div class="api-symbol-row"><a href="#echo-chamber-field-binding-get"><code>Get()</code></a><span class="api-symbol-owner">EchoChamberFieldBinding</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-get-active-text"><code>GetActiveText()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-context-get-binding"><code>GetBinding()</code></a><span class="api-symbol-owner">EchoChamberInputContext</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-get-body-font"><code>GetBodyFont()</code></a><span class="api-symbol-owner">EchoChamberTheme</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-get-command-output"><code>GetCommandOutput()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-get-command-output-is-error"><code>GetCommandOutputIsError()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-get-console-summary"><code>GetConsoleSummary()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-get-crash-report-text"><code>GetCrashReportText()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-get-debug-manager"><code>GetDebugManager()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-get-default-input-context-id"><code>GetDefaultInputContextId()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-binding-get-display-text"><code>GetDisplayText()</code></a><span class="api-symbol-owner">EchoChamberInputBinding</span></div>
    <div class="api-symbol-row"><a href="#get-echo-chamber-root"><code>GetEchoChamberRoot()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-get-generation"><code>GetGeneration()</code></a><span class="api-symbol-owner">EchoChamberTheme</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-get-header-font"><code>GetHeaderFont()</code></a><span class="api-symbol-owner">EchoChamberTheme</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-get-height"><code>GetHeight()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-get-input-context"><code>GetInputContext()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-binding-get-key"><code>GetKey()</code></a><span class="api-symbol-owner">EchoChamberInputBinding</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-binding-key-get-key"><code>GetKey()</code></a><span class="api-symbol-owner">EchoChamberInputBindingKey</span></div>
    <div class="api-symbol-row"><a href="#echo-console-target-get-label"><code>GetLabel()</code></a><span class="api-symbol-owner">EchoConsoleTarget</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-get-modal-window"><code>GetModalWindow()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-get-next-command"><code>GetNextCommand()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-get-panel"><code>GetPanel()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-get-pick-hover-count"><code>GetPickHoverCount()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-get-pick-hover-instance"><code>GetPickHoverInstance()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-get-pick-mode"><code>GetPickMode()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-get-previous-command"><code>GetPreviousCommand()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-get-root"><code>GetRoot()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-base-get-selected-index"><code>GetSelectedIndex()</code></a><span class="api-symbol-owner">EchoChamberDropdownBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-select-get-selected-index"><code>GetSelectedIndex()</code></a><span class="api-symbol-owner">EchoChamberDropdownSelect</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-toggle-menu-get-selected-index"><code>GetSelectedIndex()</code></a><span class="api-symbol-owner">EchoChamberDropdownToggleMenu</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-get-selected-index"><code>GetSelectedIndex()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-get-small-font"><code>GetSmallFont()</code></a><span class="api-symbol-owner">EchoChamberTheme</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-field-binding-get-target"><code>GetTarget()</code></a><span class="api-symbol-owner">EchoChamberFieldBinding</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-get-target"><code>GetTarget()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-get-target-kind"><code>GetTargetKind()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-get-target-revision"><code>GetTargetRevision()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-get-target-summary"><code>GetTargetSummary()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-get-target-value"><code>GetTargetValue()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-get-text-buffer"><code>GetTextBuffer()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-get-thickness"><code>GetThickness()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-console-target-get-value"><code>GetValue()</code></a><span class="api-symbol-owner">EchoConsoleTarget</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-get-width"><code>GetWidth()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-get-window"><code>GetWindow()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">H</div>
    <div class="api-symbol-row"><a href="#echo-console-manager-handle-async-system"><code>HandleAsyncSystem()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-has-crash-report"><code>HasCrashReport()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-hit-test-rect"><code>HitTestRect()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">I</div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-insert-control"><code>InsertControl()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-is-active-text-input"><code>IsActiveTextInput()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-is-auto-follow-paused"><code>IsAutoFollowPaused()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-is-color-picker-popup-open"><code>IsColorPickerPopupOpen()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-is-context-menu-open"><code>IsContextMenuOpen()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-is-control-focused"><code>IsControlFocused()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-console-target-is-instance"><code>IsInstance()</code></a><span class="api-symbol-owner">EchoConsoleTarget</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-is-near-bottom"><code>IsNearBottom()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-console-target-is-none"><code>IsNone()</code></a><span class="api-symbol-owner">EchoConsoleTarget</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-is-picking"><code>IsPicking()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-is-picking-instance"><code>IsPickingInstance()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-target-is-valid"><code>IsValid()</code></a><span class="api-symbol-owner">EchoConsoleTarget</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-is-window-frontmost-for-pointer-input"><code>IsWindowFrontmostForPointerInput()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">J</div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-jump-to-bottom"><code>JumpToBottom()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">L</div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-label-style"><code>LabelStyle()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-load-layout"><code>LoadLayout()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">M</div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-mark-theme-dirty"><code>MarkThemeDirty()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-mark-theme-dirty"><code>MarkThemeDirty()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-move-control"><code>MoveControl()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-move-control-to-panel"><code>MoveControlToPanel()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-move-control-to-panel"><code>MoveControlToPanel()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">O</div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-toggle-menu-on-any-change"><code>OnAnyChange()</code></a><span class="api-symbol-owner">EchoChamberDropdownToggleMenu</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-on-blur"><code>OnBlur()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-on-blur"><code>OnBlur()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-color-button-on-cancel"><code>OnCancel()</code></a><span class="api-symbol-owner">EchoChamberColorButton</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-on-cancel"><code>OnCancel()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-color-button-on-change"><code>OnChange()</code></a><span class="api-symbol-owner">EchoChamberColorButton</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-select-on-change"><code>OnChange()</code></a><span class="api-symbol-owner">EchoChamberDropdownSelect</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-slider-on-change"><code>OnChange()</code></a><span class="api-symbol-owner">EchoChamberSlider</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-on-change"><code>OnChange()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-toggle-on-change"><code>OnChange()</code></a><span class="api-symbol-owner">EchoChamberToggle</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-button-on-click"><code>OnClick()</code></a><span class="api-symbol-owner">EchoChamberButton</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-on-close"><code>OnClose()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-color-button-on-commit"><code>OnCommit()</code></a><span class="api-symbol-owner">EchoChamberColorButton</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-on-focus"><code>OnFocus()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-on-focus"><code>OnFocus()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-on-hide"><code>OnHide()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-on-history-next"><code>OnHistoryNext()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-on-history-previous"><code>OnHistoryPrevious()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-on-live-change"><code>OnLiveChange()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-on-minimize"><code>OnMinimize()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-on-move"><code>OnMove()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-on-resize"><code>OnResize()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-on-restore"><code>OnRestore()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-on-show"><code>OnShow()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-on-submit"><code>OnSubmit()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-open-color-picker-popup"><code>OpenColorPickerPopup()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-open-command-help"><code>OpenCommandHelp()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-open-context-menu"><code>OpenContextMenu()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-open-window"><code>OpenWindow()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">P</div>
    <div class="api-symbol-row"><a href="#echo-console-manager-play-input-recording"><code>PlayInputRecording()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-pop-clip-rect"><code>PopClipRect()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-process-window-interactions"><code>ProcessWindowInteractions()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-push-clip-rect"><code>PushClipRect()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">Q</div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-queue-overlay"><code>QueueOverlay()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">R</div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-refresh-metrics"><code>RefreshMetrics()</code></a><span class="api-symbol-owner">EchoChamberTheme</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-refresh-theme"><code>RefreshTheme()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-refresh-theme-override"><code>RefreshThemeOverride()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-register-overlay-drawer"><code>RegisterOverlayDrawer()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-register-target-listener"><code>RegisterTargetListener()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-register-window"><code>RegisterWindow()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-register-window-opener"><code>RegisterWindowOpener()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-remove-child-panel"><code>RemoveChildPanel()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-remove-control"><code>RemoveControl()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-remove-input-context"><code>RemoveInputContext()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-remove-panel"><code>RemovePanel()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-remove-watch"><code>RemoveWatch()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-remove-window"><code>RemoveWindow()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-request-tooltip"><code>RequestTooltip()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-scroll-state-reset"><code>Reset()</code></a><span class="api-symbol-owner">EchoChamberScrollState</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-reset-built-in-window-layouts"><code>ResetBuiltInWindowLayouts()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-reset-layout"><code>ResetLayout()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-reset-window-layouts"><code>ResetWindowLayouts()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-resolve-anchored-popup-rect"><code>ResolveAnchoredPopupRect()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-resolve-point-popup-rect"><code>ResolvePointPopupRect()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-run-command"><code>RunCommand()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-run-desktop"><code>RunDesktop()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">S</div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-save-layout"><code>SaveLayout()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-save-snapshot"><code>SaveSnapshot()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-scroll-state-scroll-by"><code>ScrollBy()</code></a><span class="api-symbol-owner">EchoChamberScrollState</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-send-window-to-back"><code>SendWindowToBack()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-field-binding-set"><code>Set()</code></a><span class="api-symbol-owner">EchoChamberFieldBinding</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-active"><code>SetActive()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-set-active-overlay-owner"><code>SetActiveOverlayOwner()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-allowed-chars"><code>SetAllowedChars()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-set-auto-fit"><code>SetAutoFit()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-set-auto-height-from-count"><code>SetAutoHeightFromCount()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-auto-lower"><code>SetAutoLower()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-set-auto-scroll"><code>SetAutoScroll()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-auto-trim"><code>SetAutoTrim()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-auto-upper"><code>SetAutoUpper()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-set-auto-width-from-content"><code>SetAutoWidthFromContent()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-background-sprite"><code>SetBackgroundSprite()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-set-body-font"><code>SetBodyFont()</code></a><span class="api-symbol-owner">EchoChamberTheme</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-border-sprite"><code>SetBorderSprite()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-set-caption"><code>SetCaption()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-caret-sprite"><code>SetCaretSprite()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-collapsed"><code>SetCollapsed()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-collapse-mode"><code>SetCollapseMode()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-content-drawer"><code>SetContentDrawer()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-context-menu-style-key"><code>SetContextMenuStyleKey()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-control-order"><code>SetControlOrder()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-set-count-getter"><code>SetCountGetter()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-set-default-layout"><code>SetDefaultLayout()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-denied-chars"><code>SetDeniedChars()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-box-set-editor-overlay-style-key"><code>SetEditorOverlayStyleKey()</code></a><span class="api-symbol-owner">EchoChamberTextBox</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-set-enabled"><code>SetEnabled()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-expand-sprite"><code>SetExpandSprite()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-field-binding-set-fallback"><code>SetFallback()</code></a><span class="api-symbol-owner">EchoChamberFieldBinding</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-set-fill-width"><code>SetFillWidth()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-set-fill-width"><code>SetFillWidth()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-filter"><code>SetFilter()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-flow-mode"><code>SetFlowMode()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-force-size-from-background-sprite"><code>SetForceSizeFromBackgroundSprite()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-force-size-from-border-sprite"><code>SetForceSizeFromBorderSprite()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-force-size-from-sprite"><code>SetForceSizeFromSprite()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-grip-sprite"><code>SetGripSprite()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-set-header-font"><code>SetHeaderFont()</code></a><span class="api-symbol-owner">EchoChamberTheme</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-button-set-icon"><code>SetIcon()</code></a><span class="api-symbol-owner">EchoChamberButton</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-button-set-icon-subimg"><code>SetIconSubimg()</code></a><span class="api-symbol-owner">EchoChamberButton</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-set-input-context"><code>SetInputContext()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-input-mode"><code>SetInputMode()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-input-mode-code"><code>SetInputModeCode()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-input-mode-float"><code>SetInputModeFloat()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-input-mode-int"><code>SetInputModeInt()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-input-mode-password"><code>SetInputModePassword()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-set-instance-target"><code>SetInstanceTarget()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-invalid"><code>SetInvalid()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-toggle-menu-set-items"><code>SetItems()</code></a><span class="api-symbol-owner">EchoChamberDropdownToggleMenu</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-set-label"><code>SetLabel()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-set-label-align"><code>SetLabelAlign()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-set-label-auto-min-control-width"><code>SetLabelAutoMinControlWidth()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-set-label-enabled"><code>SetLabelEnabled()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-set-label-gap"><code>SetLabelGap()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-label-gap"><code>SetLabelGap()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-set-label-placement"><code>SetLabelPlacement()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-label-placement"><code>SetLabelPlacement()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-set-label-width"><code>SetLabelWidth()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-label-width"><code>SetLabelWidth()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-label-width-clamp"><code>SetLabelWidthClamp()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-live-change-rate-ms"><code>SetLiveChangeRateMs()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-box-set-max-height"><code>SetMaxHeight()</code></a><span class="api-symbol-owner">EchoChamberTextBox</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-max-length"><code>SetMaxLength()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-max-size"><code>SetMaxSize()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-set-max-size"><code>SetMaxSize()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-box-set-min-height"><code>SetMinHeight()</code></a><span class="api-symbol-owner">EchoChamberTextBox</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-set-minimized"><code>SetMinimized()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-min-size"><code>SetMinSize()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-set-min-size"><code>SetMinSize()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-set-modal-window"><code>SetModalWindow()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-set-mouse-capture"><code>SetMouseCapture()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-numeric-only"><code>SetNumericOnly()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-set-on-activate"><code>SetOnActivate()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-set-on-double-click"><code>SetOnDoubleClick()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-on-live-change"><code>SetOnLiveChange()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-set-on-right-click"><code>SetOnRightClick()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-set-on-select"><code>SetOnSelect()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-field-binding-set-on-write"><code>SetOnWrite()</code></a><span class="api-symbol-owner">EchoChamberFieldBinding</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-base-set-options"><code>SetOptions()</code></a><span class="api-symbol-owner">EchoChamberDropdownBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-separator-set-orientation"><code>SetOrientation()</code></a><span class="api-symbol-owner">EchoChamberSeparator</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-input-context-set-parent"><code>SetParent()</code></a><span class="api-symbol-owner">EchoChamberInputContext</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-set-persistence-file"><code>SetPersistenceFile()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-set-persistence-section"><code>SetPersistenceSection()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-set-pinned"><code>SetPinned()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-placeholder"><code>SetPlaceholder()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-color-button-set-popup-direction"><code>SetPopupDirection()</code></a><span class="api-symbol-owner">EchoChamberColorButton</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-color-button-set-popup-style-key"><code>SetPopupStyleKey()</code></a><span class="api-symbol-owner">EchoChamberColorButton</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-color-button-set-popup-title"><code>SetPopupTitle()</code></a><span class="api-symbol-owner">EchoChamberColorButton</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-color-button-set-popup-visual-space"><code>SetPopupVisualSpace()</code></a><span class="api-symbol-owner">EchoChamberColorButton</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-set-position"><code>SetPosition()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-set-preferred-height"><code>SetPreferredHeight()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-set-preferred-height"><code>SetPreferredHeight()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-set-preferred-width"><code>SetPreferredWidth()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-set-preferred-width"><code>SetPreferredWidth()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-slider-set-range"><code>SetRange()</code></a><span class="api-symbol-owner">EchoChamberSlider</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-field-binding-set-read-only"><code>SetReadOnly()</code></a><span class="api-symbol-owner">EchoChamberFieldBinding</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-read-only"><code>SetReadOnly()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-set-rect"><code>SetRect()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-box-set-resizable"><code>SetResizable()</code></a><span class="api-symbol-owner">EchoChamberTextBox</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-row-align"><code>SetRowAlign()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-row-distribution"><code>SetRowDistribution()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-set-row-drawer"><code>SetRowDrawer()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-set-row-measure"><code>SetRowMeasure()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-set-row-tooltip-getter"><code>SetRowTooltipGetter()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-row-vertical-align"><code>SetRowVerticalAlign()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-scrollable"><code>SetScrollable()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-scroll-state"><code>SetScrollState()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-scroll-state-set-scroll-y"><code>SetScrollY()</code></a><span class="api-symbol-owner">EchoChamberScrollState</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-select-all-on-focus"><code>SetSelectAllOnFocus()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-base-set-selected-index"><code>SetSelectedIndex()</code></a><span class="api-symbol-owner">EchoChamberDropdownBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-select-set-selected-index"><code>SetSelectedIndex()</code></a><span class="api-symbol-owner">EchoChamberDropdownSelect</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-toggle-menu-set-selected-index"><code>SetSelectedIndex()</code></a><span class="api-symbol-owner">EchoChamberDropdownToggleMenu</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-set-selected-index"><code>SetSelectedIndex()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-size"><code>SetSize()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-size-mode"><code>SetSizeMode()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-skin-tint"><code>SetSkinTint()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-theme-set-small-font"><code>SetSmallFont()</code></a><span class="api-symbol-owner">EchoChamberTheme</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-slider-set-step"><code>SetStep()</code></a><span class="api-symbol-owner">EchoChamberSlider</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-set-style-key"><code>SetStyleKey()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-style-key"><code>SetStyleKey()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-set-style-key"><code>SetStyleKey()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-set-style-key-chrome-button"><code>SetStyleKeyChromeButton()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-set-style-key-header"><code>SetStyleKeyHeader()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-set-style-key-label"><code>SetStyleKeyLabel()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-set-style-key-label"><code>SetStyleKeyLabel()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-submit-on-enter"><code>SetSubmitOnEnter()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-tab-inserts"><code>SetTabInserts()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-tab-spaces"><code>SetTabSpaces()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-tab-uses-spaces"><code>SetTabUsesSpaces()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-set-target"><code>SetTarget()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-block-set-text"><code>SetText()</code></a><span class="api-symbol-owner">EchoChamberTextBlock</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-set-title"><code>SetTitle()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-set-tooltip"><code>SetTooltip()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-base-set-unfold-direction"><code>SetUnfoldDirection()</code></a><span class="api-symbol-owner">EchoChamberDropdownBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-box-set-use-overlay-editor"><code>SetUseOverlayEditor()</code></a><span class="api-symbol-owner">EchoChamberTextBox</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-dropdown-base-set-use-selected-label-when-closed"><code>SetUseSelectedLabelWhenClosed()</code></a><span class="api-symbol-owner">EchoChamberDropdownBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-validation-display"><code>SetValidationDisplay()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-validation-message"><code>SetValidationMessage()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-input-set-validation-visible"><code>SetValidationVisible()</code></a><span class="api-symbol-owner">EchoChamberTextInput</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-slider-set-value-decimals"><code>SetValueDecimals()</code></a><span class="api-symbol-owner">EchoChamberSlider</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-slider-set-value-formatter"><code>SetValueFormatter()</code></a><span class="api-symbol-owner">EchoChamberSlider</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-color-button-set-value-text-mode"><code>SetValueTextMode()</code></a><span class="api-symbol-owner">EchoChamberColorButton</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-set-visible"><code>SetVisible()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-set-visible"><code>SetVisible()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-list-view-set-visible-rows"><code>SetVisibleRows()</code></a><span class="api-symbol-owner">EchoChamberListView</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-box-set-visible-rows"><code>SetVisibleRows()</code></a><span class="api-symbol-owner">EchoChamberTextBox</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-set-window-zindex"><code>SetWindowZIndex()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-text-box-set-wrap"><code>SetWrap()</code></a><span class="api-symbol-owner">EchoChamberTextBox</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-should-close-popup-on-outside-click"><code>ShouldClosePopupOnOutsideClick()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-show-toast"><code>ShowToast()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-start-input-recording"><code>StartInputRecording()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-start-instance-pick"><code>StartInstancePick()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-stop-input-recording"><code>StopInputRecording()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-control-base-style"><code>Style()</code></a><span class="api-symbol-owner">EchoChamberControlBase</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-panel-style"><code>Style()</code></a><span class="api-symbol-owner">EchoChamberPanel</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-style"><code>Style()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-root-submit-text-input"><code>SubmitTextInput()</code></a><span class="api-symbol-owner">EchoChamberRoot</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-swap-input-context"><code>SwapInputContext()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">T</div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-toggle-minimized"><code>ToggleMinimized()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
    <div class="api-symbol-row"><a href="#echo-chamber-window-toggle-pinned"><code>TogglePinned()</code></a><span class="api-symbol-owner">EchoChamberWindow</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">U</div>
    <div class="api-symbol-row"><a href="#echo-console-manager-unregister-command"><code>UnregisterCommand()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-unregister-overlay-drawer"><code>UnregisterOverlayDrawer()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-unregister-target-listener"><code>UnregisterTargetListener()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
    <div class="api-symbol-row"><a href="#echo-console-manager-unregister-window-opener"><code>UnregisterWindowOpener()</code></a><span class="api-symbol-owner">EchoConsoleManager</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">Enums</div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-align-hor"><code>eEchoChamberAlignHor</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-align-ver"><code>eEchoChamberAlignVer</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-binding-kind"><code>eEchoChamberBindingKind</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-box-shape"><code>eEchoChamberBoxShape</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-chrome-button-slot"><code>eEchoChamberChromeButtonSlot</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-chrome-icon"><code>eEchoChamberChromeIcon</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-chrome-icon-state"><code>eEchoChamberChromeIconState</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-chrome-icon-visual-kind"><code>eEchoChamberChromeIconVisualKind</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-collapse"><code>eEchoChamberCollapse</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-color-button-value-text-mode"><code>eEchoChamberColorButtonValueTextMode</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-color-popup-visual-space"><code>eEchoChamberColorPopupVisualSpace</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-debug-pick-mode"><code>eEchoChamberDebugPickMode</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-debug-target-kind"><code>eEchoChamberDebugTargetKind</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-debug-theme"><code>eEchoChamberDebugTheme</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-dock"><code>eEchoChamberDock</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-input-bind-kind"><code>eEchoChamberInputBindKind</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-input-check"><code>eEchoChamberInputCheck</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-label-align"><code>eEchoChamberLabelAlign</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-label-placement"><code>eEchoChamberLabelPlacement</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-panel-flow"><code>eEchoChamberPanelFlow</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-panel-row-align"><code>eEchoChamberPanelRowAlign</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-panel-row-distribution"><code>eEchoChamberPanelRowDistribution</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-panel-size-mode"><code>eEchoChamberPanelSizeMode</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-popup-direction"><code>eEchoChamberPopupDirection</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-separator-orientation"><code>eEchoChamberSeparatorOrientation</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-slider-value-position"><code>eEchoChamberSliderValuePosition</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-validation-display"><code>eEchoChamberValidationDisplay</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-validation-kind"><code>eEchoChamberValidationKind</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-chamber-watch-kind"><code>eEchoChamberWatchKind</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-console-command-arg-type"><code>eEchoConsoleCommandArgType</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-console-command-callback-kind"><code>eEchoConsoleCommandCallbackKind</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-console-ds-kind"><code>eEchoConsoleDsKind</code></a><span class="api-symbol-owner">enum</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">Macros</div>
    <div class="api-symbol-row"><a href="#macro-echo-chamber-console-enabled"><code>ECHO_CHAMBER_CONSOLE_ENABLED</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-chamber-console-key"><code>ECHO_CHAMBER_CONSOLE_KEY</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-chamber-debug-theme"><code>ECHO_CHAMBER_DEBUG_THEME</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-chamber-launch-on-startup"><code>ECHO_CHAMBER_LAUNCH_ON_STARTUP</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-chamber-version"><code>ECHO_CHAMBER_VERSION</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-console-ds-inspect-limit"><code>ECHO_CONSOLE_DS_INSPECT_LIMIT</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-console-ds-scan-limit"><code>ECHO_CONSOLE_DS_SCAN_LIMIT</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-console-room-scan-limit"><code>ECHO_CONSOLE_ROOM_SCAN_LIMIT</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-debug-window-command-help"><code>ECHO_DEBUG_WINDOW_COMMAND_HELP</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-debug-window-crash"><code>ECHO_DEBUG_WINDOW_CRASH</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-debug-window-data-structures"><code>ECHO_DEBUG_WINDOW_DATA_STRUCTURES</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-debug-window-game"><code>ECHO_DEBUG_WINDOW_GAME</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-debug-window-input"><code>ECHO_DEBUG_WINDOW_INPUT</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-debug-window-inspector"><code>ECHO_DEBUG_WINDOW_INSPECTOR</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-debug-window-runtime"><code>ECHO_DEBUG_WINDOW_RUNTIME</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-debug-window-snapshot"><code>ECHO_DEBUG_WINDOW_SNAPSHOT</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-debug-window-watches"><code>ECHO_DEBUG_WINDOW_WATCHES</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-textmode-code"><code>ECHO_TEXTMODE_CODE</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-textmode-float"><code>ECHO_TEXTMODE_FLOAT</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-textmode-identifier"><code>ECHO_TEXTMODE_IDENTIFIER</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-textmode-int"><code>ECHO_TEXTMODE_INT</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-textmode-password"><code>ECHO_TEXTMODE_PASSWORD</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-textmode-path"><code>ECHO_TEXTMODE_PATH</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-textmode-text"><code>ECHO_TEXTMODE_TEXT</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-action-accept"><code>ECHO_UI_ACTION_ACCEPT</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-action-cancel"><code>ECHO_UI_ACTION_CANCEL</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-action-end"><code>ECHO_UI_ACTION_END</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-action-home"><code>ECHO_UI_ACTION_HOME</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-action-nav-down"><code>ECHO_UI_ACTION_NAV_DOWN</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-action-nav-up"><code>ECHO_UI_ACTION_NAV_UP</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-action-page-down"><code>ECHO_UI_ACTION_PAGE_DOWN</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-action-page-up"><code>ECHO_UI_ACTION_PAGE_UP</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-action-restore-windows"><code>ECHO_UI_ACTION_RESTORE_WINDOWS</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-action-tab-next"><code>ECHO_UI_ACTION_TAB_NEXT</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-action-tab-prev"><code>ECHO_UI_ACTION_TAB_PREV</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-bind-accept"><code>ECHO_UI_BIND_ACCEPT</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-bind-cancel"><code>ECHO_UI_BIND_CANCEL</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-bind-end"><code>ECHO_UI_BIND_END</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-bind-home"><code>ECHO_UI_BIND_HOME</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-bind-nav-down"><code>ECHO_UI_BIND_NAV_DOWN</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-bind-nav-up"><code>ECHO_UI_BIND_NAV_UP</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-bind-page-down"><code>ECHO_UI_BIND_PAGE_DOWN</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-bind-page-up"><code>ECHO_UI_BIND_PAGE_UP</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-bind-restore-windows"><code>ECHO_UI_BIND_RESTORE_WINDOWS</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-bind-tab-next"><code>ECHO_UI_BIND_TAB_NEXT</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-ui-bind-tab-prev"><code>ECHO_UI_BIND_TAB_PREV</code></a><span class="api-symbol-owner">macro</span></div>
  </div>
</div>
