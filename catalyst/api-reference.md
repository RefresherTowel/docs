---
layout: "default"
title: "API Reference"
parent: "Catalyst 2"
nav_order: 10
library_id: "catalyst"
doc_version: "current"
api_reference: true
---

<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. -->
<!-- Source: GML JSDoc + catalyst.yml -->

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>

1. TOC
{:toc}

</details>
</div>

# API Reference

Complete reference for Catalyst's public API. For explanations and worked examples, start with the teaching pages; this page is for looking up exact constructors, methods, return values, enums, and package-level helpers.

---

## Statistics and modifiers

### CatalystStatistic
{: #catalyst-statistic .api-type-title }

Creates a Statistic: a number with a base value that Modifiers can change. You can also give it optional minimum and maximum values, then use SetClamped(true) to keep the final value inside those limits.

```gml
new CatalystStatistic(value, min_value, max_value)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">value</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Starting base value. ResetToStarting() returns the Statistic to this value.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">min_value <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Lowest final value allowed when SetClamped(true) is enabled. Defaults to no lower limit.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">max_value <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Highest final value allowed when SetClamped(true) is enabled. Defaults to no upper limit.</span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Identity and tags</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-statistic-set-identity"><code>SetIdentity()</code></a></td><td>Sets this Statistic&#x27;s ID. <a href="#catalyst-set"><code>CatalystSet</code></a> uses it to find the Statistic when a Modifier targets that ID, and your own code can also use it for lookup.</td></tr>
<tr><td><a href="#catalyst-statistic-get-identity"><code>GetIdentity()</code></a></td><td>Returns the statistic&#x27;s ID.</td></tr>
<tr><td><a href="#catalyst-statistic-set-name"><code>SetName()</code></a></td><td>Sets the statistic name.</td></tr>
<tr><td><a href="#catalyst-statistic-get-name"><code>GetName()</code></a></td><td>Returns the statistic name.</td></tr>
<tr><td><a href="#catalyst-statistic-add-tag"><code>AddTag()</code></a></td><td>Adds a tag if absent.</td></tr>
<tr><td><a href="#catalyst-statistic-remove-tag"><code>RemoveTag()</code></a></td><td>Removes every matching tag.</td></tr>
<tr><td><a href="#catalyst-statistic-has-tag"><code>HasTag()</code></a></td><td>Returns whether this statistic has a tag.</td></tr>
<tr><td><a href="#catalyst-statistic-clear-tags"><code>ClearTags()</code></a></td><td>Removes every tag.</td></tr>
</tbody></table>

<div class="api-method-group-title">Layers and modifier order</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-statistic-set-layer-order"><code>SetLayerOrder()</code></a></td><td>Sets the exact order in which this Statistic processes Modifier layers. A Modifier whose layer is not in this array will be skipped, so include every layer you intend this Statistic to use.</td></tr>
<tr><td><a href="#catalyst-statistic-get-layer-order"><code>GetLayerOrder()</code></a></td><td>Returns a new array containing the configured evaluation-layer order.</td></tr>
<tr><td><a href="#catalyst-statistic-set-modifier-order"><code>SetModifierOrder()</code></a></td><td>Chooses whether ADD Modifiers run before MULTIPLY Modifiers, MULTIPLY runs first, or all Modifiers follow attachment order inside each layer.</td></tr>
<tr><td><a href="#catalyst-statistic-get-modifier-order"><code>GetModifierOrder()</code></a></td><td>Returns how ADD and MULTIPLY Modifiers are ordered inside each configured layer.</td></tr>
<tr><td><a href="#catalyst-statistic-has-layer"><code>HasLayer()</code></a></td><td>Returns whether this Statistic uses the given layer.</td></tr>
</tbody></table>

<div class="api-method-group-title">Modifier management</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-statistic-add-modifier"><code>AddModifier()</code></a></td><td>Attaches a standalone Modifier so it can affect this Statistic. A Modifier already owned by an Effect must be added through that Effect instead. If the Modifier has a different target ID, Catalyst warns but still allows this direct attachment.</td></tr>
<tr><td><a href="#catalyst-statistic-detach-modifier"><code>DetachModifier()</code></a></td><td>Removes a standalone Modifier from this Statistic without destroying it, so you can attach it again later. Effect-owned Modifiers must be removed through their Effect instead.</td></tr>
<tr><td><a href="#catalyst-statistic-destroy-modifier"><code>DestroyModifier()</code></a></td><td>Removes this exact standalone Modifier from the Statistic and destroys it so it cannot be reused.</td></tr>
<tr><td><a href="#catalyst-statistic-destroy-all-modifiers"><code>DestroyAllModifiers()</code></a></td><td>Removes and destroys every standalone Modifier attached directly to this Statistic. Modifiers owned by active Effects are left alone.</td></tr>
<tr><td><a href="#catalyst-statistic-destroy-modifiers-by-source-label"><code>DestroyModifiersBySourceLabel()</code></a></td><td>Destroys all modifiers with one source label.</td></tr>
<tr><td><a href="#catalyst-statistic-destroy-modifiers-by-source-id"><code>DestroyModifiersBySourceId()</code></a></td><td>Destroys every attached Modifier whose source ID exactly matches the value you provide.</td></tr>
<tr><td><a href="#catalyst-statistic-destroy-modifiers-by-source-meta"><code>DestroyModifiersBySourceMeta()</code></a></td><td>Destroys every attached Modifier for which your callback returns true after receiving the extra source data stored with SetSourceMeta().</td></tr>
<tr><td><a href="#catalyst-statistic-destroy-modifiers-by-tag"><code>DestroyModifiersByTag()</code></a></td><td>Destroys every attached modifier carrying one tag.</td></tr>
<tr><td><a href="#catalyst-statistic-get-modifiers"><code>GetModifiers()</code></a></td><td>Returns a new array containing every Modifier currently attached to this Statistic.</td></tr>
<tr><td><a href="#catalyst-statistic-find-modifiers-by-source-id"><code>FindModifiersBySourceId()</code></a></td><td>Returns attached Modifiers whose source ID exactly matches the value you provide.</td></tr>
<tr><td><a href="#catalyst-statistic-find-modifiers-by-source-label"><code>FindModifiersBySourceLabel()</code></a></td><td>Finds attached modifiers with one source label.</td></tr>
<tr><td><a href="#catalyst-statistic-find-modifiers-by-source-meta"><code>FindModifiersBySourceMeta()</code></a></td><td>Returns attached Modifiers for which your callback returns true after receiving the extra source data stored with SetSourceMeta().</td></tr>
<tr><td><a href="#catalyst-statistic-has-modifier-from-source-id"><code>HasModifierFromSourceId()</code></a></td><td>Returns true when at least one attached Modifier has a source ID exactly matching the value you provide.</td></tr>
<tr><td><a href="#catalyst-statistic-has-modifier-from-source-label"><code>HasModifierFromSourceLabel()</code></a></td><td>Returns whether any attached modifier has one source label.</td></tr>
<tr><td><a href="#catalyst-statistic-has-modifier-from-source-meta"><code>HasModifierFromSourceMeta()</code></a></td><td>Returns true when your callback returns true for the extra source data stored on at least one attached Modifier with SetSourceMeta().</td></tr>
<tr><td><a href="#catalyst-statistic-has-modifier"><code>HasModifier()</code></a></td><td>Returns whether this exact Modifier is attached to the Statistic.</td></tr>
</tbody></table>

<div class="api-method-group-title">Evaluation and observation</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-statistic-refresh"><code>Refresh()</code></a></td><td>Recalculates the Statistic now and runs OnChange callbacks if its value changed.</td></tr>
<tr><td><a href="#catalyst-statistic-get-value"><code>GetValue()</code></a></td><td>Returns the current Statistic value, recalculating it first when needed.</td></tr>
<tr><td><a href="#catalyst-statistic-evaluate"><code>Evaluate()</code></a></td><td>Calculates what this Statistic would be for the supplied Oracle Fact query. The result is temporary: it does not replace the stored current value and does not run OnChange callbacks.</td></tr>
<tr><td><a href="#catalyst-statistic-explain"><code>Explain()</code></a></td><td>Calculates the Statistic and returns a breakdown showing the base value, each layer, and what every Modifier did. This does not change the stored current value.</td></tr>
<tr><td><a href="#catalyst-statistic-preview"><code>Preview()</code></a></td><td>Shows what the value would be with one extra Modifier, without attaching it.</td></tr>
<tr><td><a href="#catalyst-statistic-preview-modifiers"><code>PreviewModifiers()</code></a></td><td>Shows what the value would be with extra Modifiers, without attaching them.</td></tr>
<tr><td><a href="#catalyst-statistic-on-change"><code>OnChange()</code></a></td><td>Adds a callback that runs whenever the Statistic&#x27;s stored current value changes. Catalyst calls it as fn(statistic, previous, current). Keep the returned <a href="#catalyst-subscription"><code>CatalystSubscription</code></a> if you may want to stop listening later.</td></tr>
</tbody></table>

<div class="api-method-group-title">Facts and post-processing</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-statistic-set-fact-view"><code>SetFactView()</code></a></td><td>Gives this Statistic an OracleFactView to read whenever a base function, condition, stack function, or post-process function needs Facts.</td></tr>
<tr><td><a href="#catalyst-statistic-clear-fact-view"><code>ClearFactView()</code></a></td><td>Stops using the current FactView and marks the Statistic for recalculation.</td></tr>
<tr><td><a href="#catalyst-statistic-get-fact-view"><code>GetFactView()</code></a></td><td>Returns the currently bound FactView.</td></tr>
<tr><td><a href="#catalyst-statistic-set-post-process"><code>SetPostProcess()</code></a></td><td>Sets a final adjustment function that runs after all Modifiers, but before the minimum/maximum limit and rounding step are applied.</td></tr>
<tr><td><a href="#catalyst-statistic-clear-post-process"><code>ClearPostProcess()</code></a></td><td>Removes the post-process callback.</td></tr>
<tr><td><a href="#catalyst-statistic-set-clamped"><code>SetClamped()</code></a></td><td>Chooses whether the final value is kept between this Statistic&#x27;s minimum and maximum. When disabled, those limits are stored but do not restrict the value.</td></tr>
<tr><td><a href="#catalyst-statistic-set-rounding-step"><code>SetRoundingStep()</code></a></td><td>Rounds the final value to the nearest multiple of a positive step. For example, 1 rounds to whole numbers and 0.25 rounds to quarter steps.</td></tr>
<tr><td><a href="#catalyst-statistic-clear-rounding"><code>ClearRounding()</code></a></td><td>Disables final rounding without changing other evaluation configuration.</td></tr>
<tr><td><a href="#catalyst-statistic-publish-to-fact"><code>PublishToFact()</code></a></td><td>Publishes this Statistic into an Oracle Facts scope under the key you provide, then keeps that Fact updated whenever the Statistic changes.</td></tr>
</tbody></table>

<div class="api-method-group-title">Base value and bounds</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-statistic-set-base-value"><code>SetBaseValue()</code></a></td><td>Sets the base value before modifiers.</td></tr>
<tr><td><a href="#catalyst-statistic-set-base-func"><code>SetBaseFunc()</code></a></td><td>Replaces the stored base value with a function. Each time Catalyst calculates the Statistic, it calls this function with the Statistic and the same captured set of current Facts used for the rest of that calculation.</td></tr>
<tr><td><a href="#catalyst-statistic-clear-base-func"><code>ClearBaseFunc()</code></a></td><td>Returns base evaluation to the stored base value.</td></tr>
<tr><td><a href="#catalyst-statistic-set-max-value"><code>SetMaxValue()</code></a></td><td>Sets the maximum used when clamping is enabled.</td></tr>
<tr><td><a href="#catalyst-statistic-set-min-value"><code>SetMinValue()</code></a></td><td>Sets the minimum used when clamping is enabled.</td></tr>
<tr><td><a href="#catalyst-statistic-change-base-value"><code>ChangeBaseValue()</code></a></td><td>Changes the stored base value by the amount supplied. Positive values increase it and negative values decrease it.</td></tr>
<tr><td><a href="#catalyst-statistic-change-max-value"><code>ChangeMaxValue()</code></a></td><td>Changes the clamp maximum by the amount supplied. Positive values increase it and negative values decrease it.</td></tr>
<tr><td><a href="#catalyst-statistic-change-min-value"><code>ChangeMinValue()</code></a></td><td>Changes the clamp minimum by the amount supplied. Positive values increase it and negative values decrease it.</td></tr>
<tr><td><a href="#catalyst-statistic-reset-to-starting"><code>ResetToStarting()</code></a></td><td>Restores the base value captured when this statistic was constructed.</td></tr>
<tr><td><a href="#catalyst-statistic-reset-all"><code>ResetAll()</code></a></td><td>Resets the Statistic settings and destroys its Modifiers while keeping the starting value, name, ID, layer order, and Modifier order.</td></tr>
<tr><td><a href="#catalyst-statistic-get-starting-value"><code>GetStartingValue()</code></a></td><td>Returns the original constructor value.</td></tr>
<tr><td><a href="#catalyst-statistic-get-base-value"><code>GetBaseValue()</code></a></td><td>Returns the stored base value before modifiers.</td></tr>
<tr><td><a href="#catalyst-statistic-get-max-value"><code>GetMaxValue()</code></a></td><td>Returns the maximum used when SetClamped(true) is enabled.</td></tr>
<tr><td><a href="#catalyst-statistic-get-min-value"><code>GetMinValue()</code></a></td><td>Returns the minimum used when SetClamped(true) is enabled.</td></tr>
</tbody></table>

<div class="api-method-group-title">Debugging</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-statistic-debug-describe"><code>DebugDescribe()</code></a></td><td>Writes the Statistic and its Explain() details to Echo debug output.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-statistic-set-layer-order">
  <div class="api-method-name">SetLayerOrder(layers)</div>
  <p class="api-method-summary">Sets the exact order in which this Statistic processes Modifier layers. A Modifier whose layer is not in this array will be skipped, so include every layer you intend this Statistic to use.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">layers</span>
      <span class="api-argument-type">Array&lt;Any&gt;</span>
      <span class="api-argument-description">Layer IDs in the order they should be calculated. Each ID must be unique; strings and finite numbers are supported.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-get-layer-order">
  <div class="api-method-name">GetLayerOrder()</div>
  <p class="api-method-summary">Returns a new array containing the configured evaluation-layer order.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Any&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-set-modifier-order">
  <div class="api-method-name">SetModifierOrder(order)</div>
  <p class="api-method-summary">Chooses whether ADD Modifiers run before MULTIPLY Modifiers, MULTIPLY runs first, or all Modifiers follow attachment order inside each layer.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">order</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Ordering rule from <a href="#enum-e-cat-modifier-order"><code>eCatModifierOrder</code></a>: ADD_FIRST, MULTIPLY_FIRST, or ATTACHMENT_ORDER.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-get-modifier-order">
  <div class="api-method-name">GetModifierOrder()</div>
  <p class="api-method-summary">Returns how ADD and MULTIPLY Modifiers are ordered inside each configured layer.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-has-layer">
  <div class="api-method-name">HasLayer(layer)</div>
  <p class="api-method-summary">Returns whether this Statistic uses the given layer.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">layer</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">Layer ID to check.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-add-modifier">
  <div class="api-method-name">AddModifier(modifier)</div>
  <p class="api-method-summary">Attaches a standalone Modifier so it can affect this Statistic. A Modifier already owned by an Effect must be added through that Effect instead. If the Modifier has a different target ID, Catalyst warns but still allows this direct attachment.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Detached standalone Modifier to attach.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#catalyst-modifier"><code>CatalystModifier</code></a> <span aria-hidden="true">·</span> <a href="#catalyst-statistic-preview"><code>CatalystStatistic.Preview</code></a> <span aria-hidden="true">·</span> <a href="{{ '/catalyst/statistics-and-modifiers' | relative_url }}">Statistics &amp; Modifiers</a></div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-detach-modifier">
  <div class="api-method-name">DetachModifier(modifier)</div>
  <p class="api-method-summary">Removes a standalone Modifier from this Statistic without destroying it, so you can attach it again later. Effect-owned Modifiers must be removed through their Effect instead.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Exact standalone Modifier to detach.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-destroy-modifier">
  <div class="api-method-name">DestroyModifier(modifier)</div>
  <p class="api-method-summary">Removes this exact standalone Modifier from the Statistic and destroys it so it cannot be reused.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Exact Modifier to destroy.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-destroy-all-modifiers">
  <div class="api-method-name">DestroyAllModifiers()</div>
  <p class="api-method-summary">Removes and destroys every standalone Modifier attached directly to this Statistic. Modifiers owned by active Effects are left alone.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-destroy-modifiers-by-source-label">
  <div class="api-method-name">DestroyModifiersBySourceLabel(source_label)</div>
  <p class="api-method-summary">Destroys all modifiers with one source label.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source_label</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Source label to match.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-destroy-modifiers-by-source-id">
  <div class="api-method-name">DestroyModifiersBySourceId(source_id)</div>
  <p class="api-method-summary">Destroys every attached Modifier whose source ID exactly matches the value you provide.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source_id</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Source ID value to match exactly.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-destroy-modifiers-by-source-meta">
  <div class="api-method-name">DestroyModifiersBySourceMeta(predicate_func)</div>
  <p class="api-method-summary">Destroys every attached Modifier for which your callback returns true after receiving the extra source data stored with SetSourceMeta().</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">predicate_func</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function called as fn(source_meta), where source_meta is the extra data stored with SetSourceMeta(). Return true for Modifiers you want to match.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-destroy-modifiers-by-tag">
  <div class="api-method-name">DestroyModifiersByTag(tag)</div>
  <p class="api-method-summary">Destroys every attached modifier carrying one tag.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tag</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Tag to match.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-get-modifiers">
  <div class="api-method-name">GetModifiers()</div>
  <p class="api-method-summary">Returns a new array containing every Modifier currently attached to this Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-modifier">CatalystModifier</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-find-modifiers-by-source-id">
  <div class="api-method-name">FindModifiersBySourceId(source_id)</div>
  <p class="api-method-summary">Returns attached Modifiers whose source ID exactly matches the value you provide.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source_id</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Source ID value to match exactly.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-modifier">CatalystModifier</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-find-modifiers-by-source-label">
  <div class="api-method-name">FindModifiersBySourceLabel(source_label)</div>
  <p class="api-method-summary">Finds attached modifiers with one source label.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source_label</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Source label to match.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-modifier">CatalystModifier</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-find-modifiers-by-source-meta">
  <div class="api-method-name">FindModifiersBySourceMeta(predicate_func)</div>
  <p class="api-method-summary">Returns attached Modifiers for which your callback returns true after receiving the extra source data stored with SetSourceMeta().</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">predicate_func</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function called as fn(source_meta), where source_meta is the extra data stored with SetSourceMeta(). Return true for Modifiers you want to match.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-modifier">CatalystModifier</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-has-modifier-from-source-id">
  <div class="api-method-name">HasModifierFromSourceId(source_id)</div>
  <p class="api-method-summary">Returns true when at least one attached Modifier has a source ID exactly matching the value you provide.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source_id</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Source ID value to match exactly.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-has-modifier-from-source-label">
  <div class="api-method-name">HasModifierFromSourceLabel(source_label)</div>
  <p class="api-method-summary">Returns whether any attached modifier has one source label.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source_label</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Source label to match.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-has-modifier-from-source-meta">
  <div class="api-method-name">HasModifierFromSourceMeta(predicate_func)</div>
  <p class="api-method-summary">Returns true when your callback returns true for the extra source data stored on at least one attached Modifier with SetSourceMeta().</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">predicate_func</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function called as fn(source_meta), where source_meta is the extra data stored with SetSourceMeta(). Return true for Modifiers you want to match.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-has-modifier">
  <div class="api-method-name">HasModifier(modifier)</div>
  <p class="api-method-summary">Returns whether this exact Modifier is attached to the Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Modifier to check.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-refresh">
  <div class="api-method-name">Refresh()</div>
  <p class="api-method-summary">Recalculates the Statistic now and runs OnChange callbacks if its value changed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic-refresh-result">CatalystStatisticRefreshResult</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-get-value">
  <div class="api-method-name">GetValue()</div>
  <p class="api-method-summary">Returns the current Statistic value, recalculating it first when needed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-evaluate">
  <div class="api-method-name">Evaluate([query])</div>
  <p class="api-method-summary">Calculates what this Statistic would be for the supplied Oracle Fact query. The result is temporary: it does not replace the stored current value and does not run OnChange callbacks.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">query <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.OracleFactQuery,Struct</span>
      <span class="api-argument-description">Optional Oracle Fact query to use for this one calculation instead of the Statistic&#x27;s normal FactView state.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-explain">
  <div class="api-method-name">Explain([query])</div>
  <p class="api-method-summary">Calculates the Statistic and returns a breakdown showing the base value, each layer, and what every Modifier did. This does not change the stored current value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">query <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.OracleFactQuery,Struct</span>
      <span class="api-argument-description">Optional Oracle Fact query to use for this one calculation instead of the Statistic&#x27;s normal FactView state.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic-evaluation">CatalystStatisticEvaluation</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-preview">
  <div class="api-method-name">Preview(modifier, [query])</div>
  <p class="api-method-summary">Shows what the value would be with one extra Modifier, without attaching it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Modifier to include temporarily.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">query <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.OracleFactQuery,Struct</span>
      <span class="api-argument-description">Optional Oracle Fact query to use for this one calculation instead of the Statistic&#x27;s normal FactView state.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-preview-modifiers">
  <div class="api-method-name">PreviewModifiers(modifiers, [query])</div>
  <p class="api-method-summary">Shows what the value would be with extra Modifiers, without attaching them.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifiers</span>
      <span class="api-argument-type">Array&lt;Struct.<a href="#catalyst-modifier">CatalystModifier</a>&gt;</span>
      <span class="api-argument-description">Modifiers to include temporarily.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">query <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.OracleFactQuery,Struct</span>
      <span class="api-argument-description">Optional Oracle Fact query to use for this one calculation instead of the Statistic&#x27;s normal FactView state.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-on-change">
  <div class="api-method-name">OnChange(callback)</div>
  <p class="api-method-summary">Adds a callback that runs whenever the Statistic&#x27;s stored current value changes. Catalyst calls it as fn(statistic, previous, current). Keep the returned <a href="#catalyst-subscription"><code>CatalystSubscription</code></a> if you may want to stop listening later.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function called as fn(statistic, previous, current) after the stored value changes.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-subscription">CatalystSubscription</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-set-fact-view">
  <div class="api-method-name">SetFactView(fact_view)</div>
  <p class="api-method-summary">Gives this Statistic an OracleFactView to read whenever a base function, condition, stack function, or post-process function needs Facts.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fact_view</span>
      <span class="api-argument-type">Struct.OracleFactView</span>
      <span class="api-argument-description">Oracle FactView the Statistic should read from.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-clear-fact-view">
  <div class="api-method-name">ClearFactView()</div>
  <p class="api-method-summary">Stops using the current FactView and marks the Statistic for recalculation.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-get-fact-view">
  <div class="api-method-name">GetFactView()</div>
  <p class="api-method-summary">Returns the currently bound FactView.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.OracleFactView,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-set-post-process">
  <div class="api-method-name">SetPostProcess(fn)</div>
  <p class="api-method-summary">Sets a final adjustment function that runs after all Modifiers, but before the minimum/maximum limit and rounding step are applied.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function called as fn(statistic, value, facts). Return the final number you want Catalyst to continue with.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-clear-post-process">
  <div class="api-method-name">ClearPostProcess()</div>
  <p class="api-method-summary">Removes the post-process callback.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-set-clamped">
  <div class="api-method-name">SetClamped([enabled])</div>
  <p class="api-method-summary">Chooses whether the final value is kept between this Statistic&#x27;s minimum and maximum. When disabled, those limits are stored but do not restrict the value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">enabled <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">true to keep the final value between the minimum and maximum; false to allow values outside them.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-set-rounding-step">
  <div class="api-method-name">SetRoundingStep(step)</div>
  <p class="api-method-summary">Rounds the final value to the nearest multiple of a positive step. For example, 1 rounds to whole numbers and 0.25 rounds to quarter steps.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">step</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Positive rounding step, such as 1 or 0.01.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-clear-rounding">
  <div class="api-method-name">ClearRounding()</div>
  <p class="api-method-summary">Disables final rounding without changing other evaluation configuration.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-set-name">
  <div class="api-method-name">SetName(name)</div>
  <p class="api-method-summary">Sets the statistic name.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">New name.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-get-name">
  <div class="api-method-name">GetName()</div>
  <p class="api-method-summary">Returns the statistic name.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-set-identity">
  <div class="api-method-name">SetIdentity(identity)</div>
  <p class="api-method-summary">Sets this Statistic&#x27;s ID. <a href="#catalyst-set"><code>CatalystSet</code></a> uses it to find the Statistic when a Modifier targets that ID, and your own code can also use it for lookup.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real,Undefined</span>
      <span class="api-argument-description">ID to use. Give a non-empty string or finite number, or undefined to remove the current ID.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-get-identity">
  <div class="api-method-name">GetIdentity()</div>
  <p class="api-method-summary">Returns the statistic&#x27;s ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-set-base-value">
  <div class="api-method-name">SetBaseValue(amount)</div>
  <p class="api-method-summary">Sets the base value before modifiers.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">amount</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">New base value.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-set-base-func">
  <div class="api-method-name">SetBaseFunc(fn)</div>
  <p class="api-method-summary">Replaces the stored base value with a function. Each time Catalyst calculates the Statistic, it calls this function with the Statistic and the same captured set of current Facts used for the rest of that calculation.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function called as fn(statistic, facts). Return the base number Catalyst should use before Modifiers.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-clear-base-func">
  <div class="api-method-name">ClearBaseFunc()</div>
  <p class="api-method-summary">Returns base evaluation to the stored base value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-set-max-value">
  <div class="api-method-name">SetMaxValue(amount)</div>
  <p class="api-method-summary">Sets the maximum used when clamping is enabled.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">amount</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">New maximum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-set-min-value">
  <div class="api-method-name">SetMinValue(amount)</div>
  <p class="api-method-summary">Sets the minimum used when clamping is enabled.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">amount</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">New minimum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-change-base-value">
  <div class="api-method-name">ChangeBaseValue(amount)</div>
  <p class="api-method-summary">Changes the stored base value by the amount supplied. Positive values increase it and negative values decrease it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">amount</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Amount to change by. Use a positive number to increase or a negative number to decrease.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-change-max-value">
  <div class="api-method-name">ChangeMaxValue(amount)</div>
  <p class="api-method-summary">Changes the clamp maximum by the amount supplied. Positive values increase it and negative values decrease it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">amount</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Amount to change by. Use a positive number to increase or a negative number to decrease.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-change-min-value">
  <div class="api-method-name">ChangeMinValue(amount)</div>
  <p class="api-method-summary">Changes the clamp minimum by the amount supplied. Positive values increase it and negative values decrease it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">amount</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Amount to change by. Use a positive number to increase or a negative number to decrease.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-reset-to-starting">
  <div class="api-method-name">ResetToStarting()</div>
  <p class="api-method-summary">Restores the base value captured when this statistic was constructed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-reset-all">
  <div class="api-method-name">ResetAll()</div>
  <p class="api-method-summary">Resets the Statistic settings and destroys its Modifiers while keeping the starting value, name, ID, layer order, and Modifier order.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-get-starting-value">
  <div class="api-method-name">GetStartingValue()</div>
  <p class="api-method-summary">Returns the original constructor value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-get-base-value">
  <div class="api-method-name">GetBaseValue()</div>
  <p class="api-method-summary">Returns the stored base value before modifiers.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-get-max-value">
  <div class="api-method-name">GetMaxValue()</div>
  <p class="api-method-summary">Returns the maximum used when SetClamped(true) is enabled.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-get-min-value">
  <div class="api-method-name">GetMinValue()</div>
  <p class="api-method-summary">Returns the minimum used when SetClamped(true) is enabled.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-add-tag">
  <div class="api-method-name">AddTag(tag)</div>
  <p class="api-method-summary">Adds a tag if absent.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tag</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Tag to add.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-remove-tag">
  <div class="api-method-name">RemoveTag(tag)</div>
  <p class="api-method-summary">Removes every matching tag.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tag</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Tag to remove.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-has-tag">
  <div class="api-method-name">HasTag(tag)</div>
  <p class="api-method-summary">Returns whether this statistic has a tag.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tag</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Tag to query.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-clear-tags">
  <div class="api-method-name">ClearTags()</div>
  <p class="api-method-summary">Removes every tag.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-publish-to-fact">
  <div class="api-method-name">PublishToFact(facts, key, [transform])</div>
  <p class="api-method-summary">Publishes this Statistic into an Oracle Facts scope under the key you provide, then keeps that Fact updated whenever the Statistic changes.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">facts</span>
      <span class="api-argument-type">Struct.OracleFacts</span>
      <span class="api-argument-description">Oracle Facts scope that should receive the published value.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Name of the Fact to write, such as &quot;health_fraction&quot;.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">transform <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Optional function called as fn(statistic). Return the value you want stored in Oracle instead of the raw Statistic value.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-fact-binding">CatalystFactBinding</a>,Undefined</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#catalyst-fact-binding"><code>CatalystFactBinding</code></a> <span aria-hidden="true">·</span> <a href="{{ '/catalyst/situational-statistics' | relative_url }}">Situational Statistics</a></div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-debug-describe">
  <div class="api-method-name">DebugDescribe()</div>
  <p class="api-method-summary">Writes the Statistic and its Explain() details to Echo debug output.</p>
</div>

### CatalystModifier
{: #catalyst-modifier .api-type-title }

Creates a Modifier that can change a <a href="#catalyst-statistic"><code>CatalystStatistic</code></a> when attached. Choose whether it adds to the value, multiplies it, or forces a minimum/maximum using <a href="#enum-e-cat-math-ops"><code>eCatMathOps</code></a>.

```gml
new CatalystModifier(value, math_operation, duration, source_label, source_id, source_meta)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">value</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Amount used by the Modifier. Its meaning depends on _math_operation; for example ADD 5 adds 5, while MULTIPLY 0.5 increases the value by 50%.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">math_operation</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">How this Modifier changes the Statistic. Use <a href="#enum-e-cat-math-ops"><code>eCatMathOps</code></a>.ADD, MULTIPLY, FORCE_MIN, or FORCE_MAX.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">duration <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">How long the Modifier lasts once attached. Negative means permanent, positive counts down, and zero expires immediately when attached.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">source_label <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Optional human-readable label for what created the Modifier, such as &quot;poison&quot; or &quot;iron_sword&quot;.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">source_id <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional value your game can use to identify the exact source that created this Modifier.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">source_meta <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional extra project data to store with the Modifier. Catalyst does not interpret it.</span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Identity and routing</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-modifier-set-identity"><code>SetIdentity()</code></a></td><td>Sets an optional ID for this Modifier so your own code or Catalyst&#x27;s save/restore tools can identify it.</td></tr>
<tr><td><a href="#catalyst-modifier-get-identity"><code>GetIdentity()</code></a></td><td>Returns the modifier&#x27;s optional ID.</td></tr>
<tr><td><a href="#catalyst-modifier-set-target-identity"><code>SetTargetIdentity()</code></a></td><td>Sets the ID of the Statistic this Modifier should affect when passed through a <a href="#catalyst-set"><code>CatalystSet</code></a>. <a href="#catalyst-set"><code>CatalystSet</code></a> uses this ID to find the matching Statistic automatically.</td></tr>
<tr><td><a href="#catalyst-modifier-get-target-identity"><code>GetTargetIdentity()</code></a></td><td>Returns the Statistic ID <a href="#catalyst-set"><code>CatalystSet</code></a> uses to decide which Statistic this Modifier should attach to.</td></tr>
<tr><td><a href="#catalyst-modifier-set-layer"><code>SetLayer()</code></a></td><td>Chooses which Statistic layer contains this ADD or MULTIPLY Modifier. The target Statistic must include this layer in its layer order or the Modifier will be skipped.</td></tr>
</tbody></table>

<div class="api-method-group-title">Value and stacks</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-modifier-set-value"><code>SetValue()</code></a></td><td>Changes the modifier&#x27;s base value.</td></tr>
<tr><td><a href="#catalyst-modifier-set-maths-op"><code>SetMathsOp()</code></a></td><td>Changes the math this Modifier uses when applied to a Statistic.</td></tr>
<tr><td><a href="#catalyst-modifier-set-stacks"><code>SetStacks()</code></a></td><td>Sets how many copies, or stacks, of this Modifier are active. Catalyst limits the result to max_stacks.</td></tr>
<tr><td><a href="#catalyst-modifier-add-stacks"><code>AddStacks()</code></a></td><td>Adds or removes stacks from the Modifier.</td></tr>
<tr><td><a href="#catalyst-modifier-set-max-stacks"><code>SetMaxStacks()</code></a></td><td>Sets the maximum number of stacks this Modifier can use.</td></tr>
<tr><td><a href="#catalyst-modifier-set-stack-mode"><code>SetStackMode()</code></a></td><td>Chooses how multiple stacks work for MULTIPLY. COMPOUND applies the multiplier once per stack; ADDITIVE combines the percentage change before multiplying.</td></tr>
<tr><td><a href="#catalyst-modifier-get-stack-mode"><code>GetStackMode()</code></a></td><td>Returns the multiplicative stack mode.</td></tr>
<tr><td><a href="#catalyst-modifier-set-stack-func"><code>SetStackFunc()</code></a></td><td>Lets a function decide the Modifier&#x27;s stack count each time the Statistic is calculated, instead of using the stored stacks value.</td></tr>
<tr><td><a href="#catalyst-modifier-clear-stack-func"><code>ClearStackFunc()</code></a></td><td>Stops calculating stacks from a function and uses the stored stack count again.</td></tr>
</tbody></table>

<div class="api-method-group-title">Conditions and families</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-modifier-set-condition"><code>SetCondition()</code></a></td><td>Sets a function that can turn this Modifier on or off for each Statistic calculation by returning true or false.</td></tr>
<tr><td><a href="#catalyst-modifier-clear-condition"><code>ClearCondition()</code></a></td><td>Removes the condition so this Modifier can always apply.</td></tr>
<tr><td><a href="#catalyst-modifier-set-family"><code>SetFamily()</code></a></td><td>Groups this Modifier with other Modifiers using the same family ID. The family mode decides whether all members apply or Catalyst chooses only the strongest/weakest.</td></tr>
<tr><td><a href="#catalyst-modifier-clear-family"><code>ClearFamily()</code></a></td><td>Removes this Modifier from its family.</td></tr>
<tr><td><a href="#catalyst-modifier-set-family-mode"><code>SetFamilyMode()</code></a></td><td>Changes the rule used when this Modifier is compared with other members of the same family.</td></tr>
<tr><td><a href="#catalyst-modifier-set-family-scope"><code>SetFamilyScope()</code></a></td><td>Chooses whether this Modifier competes with same-family Modifiers only in its own layer or anywhere in the Statistic.</td></tr>
</tbody></table>

<div class="api-method-group-title">Source metadata and tags</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-modifier-set-source-label"><code>SetSourceLabel()</code></a></td><td>Sets a human-readable label describing what created this Modifier. Source labels are useful for finding or removing groups of Modifiers later.</td></tr>
<tr><td><a href="#catalyst-modifier-set-source-id"><code>SetSourceId()</code></a></td><td>Stores a source ID for this Modifier. Catalyst does not interpret the value; you can use it to match the exact gameplay source later.</td></tr>
<tr><td><a href="#catalyst-modifier-set-source-meta"><code>SetSourceMeta()</code></a></td><td>Stores extra project data about the Modifier&#x27;s source. Catalyst keeps the value but does not interpret it.</td></tr>
<tr><td><a href="#catalyst-modifier-add-tag"><code>AddTag()</code></a></td><td>Adds a tag if it is not already present.</td></tr>
<tr><td><a href="#catalyst-modifier-remove-tag"><code>RemoveTag()</code></a></td><td>Removes every matching tag.</td></tr>
<tr><td><a href="#catalyst-modifier-has-tag"><code>HasTag()</code></a></td><td>Returns whether this modifier has one tag.</td></tr>
<tr><td><a href="#catalyst-modifier-clear-tags"><code>ClearTags()</code></a></td><td>Removes every tag.</td></tr>
</tbody></table>

<div class="api-method-group-title">Timing</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-modifier-set-countdown-tracker"><code>SetCountdownTracker()</code></a></td><td>Chooses which <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> counts down this Modifier while it is attached directly to a Statistic. A Modifier owned by an Effect uses the Effect&#x27;s tracker instead.</td></tr>
<tr><td><a href="#catalyst-modifier-get-countdown-tracker"><code>GetCountdownTracker()</code></a></td><td>Returns the standalone countdown tracker assigned to this modifier.</td></tr>
<tr><td><a href="#catalyst-modifier-set-duration"><code>SetDuration()</code></a></td><td>Replaces both the remaining time and the reset duration for this standalone Modifier. If it is already attached and you set zero, it expires immediately.</td></tr>
<tr><td><a href="#catalyst-modifier-reset-duration"><code>ResetDuration()</code></a></td><td>Resets the remaining time to this Modifier&#x27;s configured maximum duration. If that maximum is zero and the Modifier is attached, it expires immediately.</td></tr>
</tbody></table>

<div class="api-method-group-title">Lifecycle</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-modifier-destroy"><code>Destroy()</code></a></td><td>Destroys this Modifier. By default Catalyst first removes it from the Statistic it is attached to; pass false only when the caller has already handled that removal.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-modifier-set-identity">
  <div class="api-method-name">SetIdentity(identity)</div>
  <p class="api-method-summary">Sets an optional ID for this Modifier so your own code or Catalyst&#x27;s save/restore tools can identify it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real,Undefined</span>
      <span class="api-argument-description">Non-empty string or finite number used as an ID to store, or undefined to clear.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-get-identity">
  <div class="api-method-name">GetIdentity()</div>
  <p class="api-method-summary">Returns the modifier&#x27;s optional ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-target-identity">
  <div class="api-method-name">SetTargetIdentity(identity)</div>
  <p class="api-method-summary">Sets the ID of the Statistic this Modifier should affect when passed through a <a href="#catalyst-set"><code>CatalystSet</code></a>. <a href="#catalyst-set"><code>CatalystSet</code></a> uses this ID to find the matching Statistic automatically.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real,Undefined</span>
      <span class="api-argument-description">ID of the target Statistic, or undefined to remove the target.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-get-target-identity">
  <div class="api-method-name">GetTargetIdentity()</div>
  <p class="api-method-summary">Returns the Statistic ID <a href="#catalyst-set"><code>CatalystSet</code></a> uses to decide which Statistic this Modifier should attach to.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-value">
  <div class="api-method-name">SetValue(value)</div>
  <p class="api-method-summary">Changes the modifier&#x27;s base value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">value</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">New modifier value.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-maths-op">
  <div class="api-method-name">SetMathsOp(maths_op)</div>
  <p class="api-method-summary">Changes the math this Modifier uses when applied to a Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">maths_op</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">New operation from <a href="#enum-e-cat-math-ops"><code>eCatMathOps</code></a>: ADD, MULTIPLY, FORCE_MIN, or FORCE_MAX.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-layer">
  <div class="api-method-name">SetLayer(layer)</div>
  <p class="api-method-summary">Chooses which Statistic layer contains this ADD or MULTIPLY Modifier. The target Statistic must include this layer in its layer order or the Modifier will be skipped.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">layer</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">Layer ID used by the target Statistic.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-stacks">
  <div class="api-method-name">SetStacks(stacks)</div>
  <p class="api-method-summary">Sets how many copies, or stacks, of this Modifier are active. Catalyst limits the result to max_stacks.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">stacks</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Desired stack count.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-add-stacks">
  <div class="api-method-name">AddStacks([delta])</div>
  <p class="api-method-summary">Adds or removes stacks from the Modifier.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">delta <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Amount to add, defaults to one stack.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-max-stacks">
  <div class="api-method-name">SetMaxStacks(max)</div>
  <p class="api-method-summary">Sets the maximum number of stacks this Modifier can use.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">max</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Maximum stacks, use infinity for unlimited.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-stack-mode">
  <div class="api-method-name">SetStackMode(mode)</div>
  <p class="api-method-summary">Chooses how multiple stacks work for MULTIPLY. COMPOUND applies the multiplier once per stack; ADDITIVE combines the percentage change before multiplying.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">mode</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Use <a href="#enum-e-cat-stack-mode"><code>eCatStackMode</code></a>.COMPOUND or <a href="#enum-e-cat-stack-mode"><code>eCatStackMode</code></a>.ADDITIVE.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-get-stack-mode">
  <div class="api-method-name">GetStackMode()</div>
  <p class="api-method-summary">Returns the multiplicative stack mode.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-condition">
  <div class="api-method-name">SetCondition(fn)</div>
  <p class="api-method-summary">Sets a function that can turn this Modifier on or off for each Statistic calculation by returning true or false.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function called as fn(statistic, facts). Return true to let the Modifier apply or false to skip it.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-clear-condition">
  <div class="api-method-name">ClearCondition()</div>
  <p class="api-method-summary">Removes the condition so this Modifier can always apply.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-stack-func">
  <div class="api-method-name">SetStackFunc(fn)</div>
  <p class="api-method-summary">Lets a function decide the Modifier&#x27;s stack count each time the Statistic is calculated, instead of using the stored stacks value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function called as fn(statistic, facts). Return the number of stacks Catalyst should use.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-clear-stack-func">
  <div class="api-method-name">ClearStackFunc()</div>
  <p class="api-method-summary">Stops calculating stacks from a function and uses the stored stack count again.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-family">
  <div class="api-method-name">SetFamily(family, [mode])</div>
  <p class="api-method-summary">Groups this Modifier with other Modifiers using the same family ID. The family mode decides whether all members apply or Catalyst chooses only the strongest/weakest.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">family</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">Shared string or number ID used to group related Modifiers into the same family.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">mode <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Family rule from <a href="#enum-e-cat-family-mode"><code>eCatFamilyMode</code></a>. Defaults to STRONGEST; STACK_ALL and WEAKEST are also available.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-clear-family">
  <div class="api-method-name">ClearFamily()</div>
  <p class="api-method-summary">Removes this Modifier from its family.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-family-mode">
  <div class="api-method-name">SetFamilyMode(mode)</div>
  <p class="api-method-summary">Changes the rule used when this Modifier is compared with other members of the same family.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">mode</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Use <a href="#enum-e-cat-family-mode"><code>eCatFamilyMode</code></a>.STACK_ALL, STRONGEST, or WEAKEST.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-family-scope">
  <div class="api-method-name">SetFamilyScope(scope)</div>
  <p class="api-method-summary">Chooses whether this Modifier competes with same-family Modifiers only in its own layer or anywhere in the Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">scope</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Use <a href="#enum-e-cat-family-scope"><code>eCatFamilyScope</code></a>.LAYER or <a href="#enum-e-cat-family-scope"><code>eCatFamilyScope</code></a>.STATISTIC.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-source-label">
  <div class="api-method-name">SetSourceLabel(source_label)</div>
  <p class="api-method-summary">Sets a human-readable label describing what created this Modifier. Source labels are useful for finding or removing groups of Modifiers later.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source_label</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">New label.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-source-id">
  <div class="api-method-name">SetSourceId(source_id)</div>
  <p class="api-method-summary">Stores a source ID for this Modifier. Catalyst does not interpret the value; you can use it to match the exact gameplay source later.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source_id</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">New source ID.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-source-meta">
  <div class="api-method-name">SetSourceMeta(source_meta)</div>
  <p class="api-method-summary">Stores extra project data about the Modifier&#x27;s source. Catalyst keeps the value but does not interpret it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source_meta</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Extra project data to store with this Modifier.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-countdown-tracker">
  <div class="api-method-name">SetCountdownTracker(tracker)</div>
  <p class="api-method-summary">Chooses which <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> counts down this Modifier while it is attached directly to a Statistic. A Modifier owned by an Effect uses the Effect&#x27;s tracker instead.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tracker</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-countdown-tracker">CatalystCountdownTracker</a>,Noone</span>
      <span class="api-argument-description">Tracker to assign, or noone to disable tracking.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-get-countdown-tracker">
  <div class="api-method-name">GetCountdownTracker()</div>
  <p class="api-method-summary">Returns the standalone countdown tracker assigned to this modifier.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-countdown-tracker">CatalystCountdownTracker</a>,Noone</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-duration">
  <div class="api-method-name">SetDuration(duration)</div>
  <p class="api-method-summary">Replaces both the remaining time and the reset duration for this standalone Modifier. If it is already attached and you set zero, it expires immediately.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">duration</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">New duration. Negative means permanent, positive counts down, and zero expires immediately while attached.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-reset-duration">
  <div class="api-method-name">ResetDuration()</div>
  <p class="api-method-summary">Resets the remaining time to this Modifier&#x27;s configured maximum duration. If that maximum is zero and the Modifier is attached, it expires immediately.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-add-tag">
  <div class="api-method-name">AddTag(tag)</div>
  <p class="api-method-summary">Adds a tag if it is not already present.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tag</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Tag to add.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-remove-tag">
  <div class="api-method-name">RemoveTag(tag)</div>
  <p class="api-method-summary">Removes every matching tag.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tag</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Tag to remove.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-has-tag">
  <div class="api-method-name">HasTag(tag)</div>
  <p class="api-method-summary">Returns whether this modifier has one tag.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tag</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Tag to test.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-clear-tags">
  <div class="api-method-name">ClearTags()</div>
  <p class="api-method-summary">Removes every tag.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-destroy">
  <div class="api-method-name">Destroy([remove_from_stat])</div>
  <p class="api-method-summary">Destroys this Modifier. By default Catalyst first removes it from the Statistic it is attached to; pass false only when the caller has already handled that removal.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">remove_from_stat <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">true to remove the Modifier from its Statistic before destroying it. Defaults to true.</span>
    </div>
  </div>
</div>

### CatalystStatisticRefreshResult
{: #catalyst-statistic-refresh-result .api-type-title }

Stores the before-and-after values from Statistic.Refresh(), along with whether the value actually changed.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-statistic-refresh-result-did-change"><code>DidChange()</code></a></td><td>Returns whether the value changed.</td></tr>
<tr><td><a href="#catalyst-statistic-refresh-result-get-previous"><code>GetPrevious()</code></a></td><td>Returns the value before the refresh.</td></tr>
<tr><td><a href="#catalyst-statistic-refresh-result-get-current"><code>GetCurrent()</code></a></td><td>Returns the value after the refresh.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-statistic-refresh-result-did-change">
  <div class="api-method-name">DidChange()</div>
  <p class="api-method-summary">Returns whether the value changed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-refresh-result-get-previous">
  <div class="api-method-name">GetPrevious()</div>
  <p class="api-method-summary">Returns the value before the refresh.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-refresh-result-get-current">
  <div class="api-method-name">GetCurrent()</div>
  <p class="api-method-summary">Returns the value after the refresh.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

### CatalystModifierEvaluation
{: #catalyst-modifier-evaluation .api-type-title }

Describes what happened to one Modifier while Catalyst calculated a Statistic, including whether it applied, how many stacks were used, and the value before and after it.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-modifier-evaluation-get-modifier"><code>GetModifier()</code></a></td><td>Returns the Modifier these calculation details belong to.</td></tr>
<tr><td><a href="#catalyst-modifier-evaluation-applied"><code>Applied()</code></a></td><td>Returns whether the Modifier affected the calculation.</td></tr>
<tr><td><a href="#catalyst-modifier-evaluation-get-skip-reason"><code>GetSkipReason()</code></a></td><td>Returns why this Modifier did not affect the Statistic. Returns <a href="#enum-e-cat-modifier-skip-reason"><code>eCatModifierSkipReason</code></a>.NONE when it was not skipped.</td></tr>
<tr><td><a href="#catalyst-modifier-evaluation-get-effective-stacks"><code>GetEffectiveStacks()</code></a></td><td>Returns the number of Modifier stacks Catalyst actually used for this calculation.</td></tr>
<tr><td><a href="#catalyst-modifier-evaluation-won-family"><code>WonFamily()</code></a></td><td>Returns whether the family rules allowed this Modifier to apply.</td></tr>
<tr><td><a href="#catalyst-modifier-evaluation-get-contribution"><code>GetContribution()</code></a></td><td>Returns how much this Modifier changed the value at its point in the calculation.</td></tr>
<tr><td><a href="#catalyst-modifier-evaluation-get-value-before"><code>GetValueBefore()</code></a></td><td>Returns the value immediately before this Modifier was applied.</td></tr>
<tr><td><a href="#catalyst-modifier-evaluation-get-value-after"><code>GetValueAfter()</code></a></td><td>Returns the value immediately after this Modifier was applied.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-modifier-evaluation-get-modifier">
  <div class="api-method-name">GetModifier()</div>
  <p class="api-method-summary">Returns the Modifier these calculation details belong to.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-evaluation-applied">
  <div class="api-method-name">Applied()</div>
  <p class="api-method-summary">Returns whether the Modifier affected the calculation.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-evaluation-get-skip-reason">
  <div class="api-method-name">GetSkipReason()</div>
  <p class="api-method-summary">Returns why this Modifier did not affect the Statistic. Returns <a href="#enum-e-cat-modifier-skip-reason"><code>eCatModifierSkipReason</code></a>.NONE when it was not skipped.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-evaluation-get-effective-stacks">
  <div class="api-method-name">GetEffectiveStacks()</div>
  <p class="api-method-summary">Returns the number of Modifier stacks Catalyst actually used for this calculation.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-evaluation-won-family">
  <div class="api-method-name">WonFamily()</div>
  <p class="api-method-summary">Returns whether the family rules allowed this Modifier to apply.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-evaluation-get-contribution">
  <div class="api-method-name">GetContribution()</div>
  <p class="api-method-summary">Returns how much this Modifier changed the value at its point in the calculation.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-evaluation-get-value-before">
  <div class="api-method-name">GetValueBefore()</div>
  <p class="api-method-summary">Returns the value immediately before this Modifier was applied.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-evaluation-get-value-after">
  <div class="api-method-name">GetValueAfter()</div>
  <p class="api-method-summary">Returns the value immediately after this Modifier was applied.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

### CatalystStatisticLayerEvaluation
{: #catalyst-statistic-layer-evaluation .api-type-title }

Groups the calculation details for all Modifiers that were processed in one Statistic layer.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-statistic-layer-evaluation-get-layer"><code>GetLayer()</code></a></td><td>Returns this Layer ID.</td></tr>
<tr><td><a href="#catalyst-statistic-layer-evaluation-get-modifier-results"><code>GetModifierResults()</code></a></td><td>Returns the Modifier details for this layer.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-statistic-layer-evaluation-get-layer">
  <div class="api-method-name">GetLayer()</div>
  <p class="api-method-summary">Returns this Layer ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-layer-evaluation-get-modifier-results">
  <div class="api-method-name">GetModifierResults()</div>
  <p class="api-method-summary">Returns the Modifier details for this layer.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-modifier-evaluation">CatalystModifierEvaluation</a>&gt;</span>
    </div>
  </div>
</div>

### CatalystStatisticEvaluation
{: #catalyst-statistic-evaluation .api-type-title }

Contains the final Statistic value plus a breakdown of the base value, layers, and Modifiers that produced it. This is the result returned by Explain().

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-statistic-evaluation-get-value"><code>GetValue()</code></a></td><td>Returns the final evaluated value.</td></tr>
<tr><td><a href="#catalyst-statistic-evaluation-get-base-value"><code>GetBaseValue()</code></a></td><td>Returns the base number Catalyst started with for this calculation, after SetBaseFunc() was used if one is configured.</td></tr>
<tr><td><a href="#catalyst-statistic-evaluation-get-modifier-results"><code>GetModifierResults()</code></a></td><td>Returns the details for every Modifier in this calculation.</td></tr>
<tr><td><a href="#catalyst-statistic-evaluation-get-layers"><code>GetLayers()</code></a></td><td>Returns the layer details in evaluation order.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-statistic-evaluation-get-value">
  <div class="api-method-name">GetValue()</div>
  <p class="api-method-summary">Returns the final evaluated value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-evaluation-get-base-value">
  <div class="api-method-name">GetBaseValue()</div>
  <p class="api-method-summary">Returns the base number Catalyst started with for this calculation, after SetBaseFunc() was used if one is configured.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-evaluation-get-modifier-results">
  <div class="api-method-name">GetModifierResults()</div>
  <p class="api-method-summary">Returns the details for every Modifier in this calculation.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-modifier-evaluation">CatalystModifierEvaluation</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-statistic-evaluation-get-layers">
  <div class="api-method-name">GetLayers()</div>
  <p class="api-method-summary">Returns the layer details in evaluation order.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-statistic-layer-evaluation">CatalystStatisticLayerEvaluation</a>&gt;</span>
    </div>
  </div>
</div>

## Resources and flows

### CatalystResource
{: #catalyst-resource .api-type-title }

Creates a Resource: a current amount with a minimum and maximum, useful for values such as health, stamina, fuel, stock, or capacity. Number bounds create private Statistics; passing existing Statistics makes the Resource share those live bounds.

```gml
new CatalystResource(maximum, current, minimum)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">maximum</span>
      <span class="api-argument-type">Real,Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
      <span class="api-argument-description">Maximum amount, or an existing Statistic whose current value should act as the maximum.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">current <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Starting current amount. If omitted, the Resource starts at its maximum.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">minimum <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real,Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
      <span class="api-argument-description">Minimum amount, or an existing Statistic whose current value should act as the minimum. Defaults to 0.</span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Identity</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-resource-set-identity"><code>SetIdentity()</code></a></td><td>Sets this Resource&#x27;s ID so a <a href="#catalyst-set"><code>CatalystSet</code></a> and your own code can find it later.</td></tr>
<tr><td><a href="#catalyst-resource-get-identity"><code>GetIdentity()</code></a></td><td>Returns the Resource ID.</td></tr>
<tr><td><a href="#catalyst-resource-set-name"><code>SetName()</code></a></td><td>Sets the resource name.</td></tr>
<tr><td><a href="#catalyst-resource-get-name"><code>GetName()</code></a></td><td>Returns the resource name.</td></tr>
</tbody></table>

<div class="api-method-group-title">Values and bounds</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-resource-get-current"><code>GetCurrent()</code></a></td><td>Returns the current amount. If a HARD minimum or maximum Statistic changed since the last check, Catalyst first moves current back inside those absolute bounds.</td></tr>
<tr><td><a href="#catalyst-resource-get-minimum"><code>GetMinimum()</code></a></td><td>Returns the Resource&#x27;s current minimum after its minimum Statistic has been calculated.</td></tr>
<tr><td><a href="#catalyst-resource-get-maximum"><code>GetMaximum()</code></a></td><td>Returns the current maximum. If the minimum rises above it, the minimum wins.</td></tr>
<tr><td><a href="#catalyst-resource-set-minimum-bound-mode"><code>SetMinimumBoundMode()</code></a></td><td>Chooses how the minimum affects current. HARD never allows current below it. SOFT stops ordinary decreases at the minimum but explicit past-bound methods can go below it. OPEN does not restrict current at all.</td></tr>
<tr><td><a href="#catalyst-resource-get-minimum-bound-mode"><code>GetMinimumBoundMode()</code></a></td><td>Returns how the minimum constrains current.</td></tr>
<tr><td><a href="#catalyst-resource-set-maximum-bound-mode"><code>SetMaximumBoundMode()</code></a></td><td>Chooses how the maximum affects current. HARD never allows current above it. SOFT stops ordinary increases at the maximum but explicit past-bound methods can go above it. OPEN does not restrict current at all.</td></tr>
<tr><td><a href="#catalyst-resource-get-maximum-bound-mode"><code>GetMaximumBoundMode()</code></a></td><td>Returns how the maximum constrains current.</td></tr>
<tr><td><a href="#catalyst-resource-get-fraction"><code>GetFraction()</code></a></td><td>Returns the Resource&#x27;s position between its minimum and maximum as a number from 0 to 1. Values below the minimum return 0, values above the maximum return 1, and a Resource whose minimum equals its maximum returns 1.</td></tr>
<tr><td><a href="#catalyst-resource-get-missing"><code>GetMissing()</code></a></td><td>Returns how much could be added before current reaches the Resource&#x27;s current maximum. Returns zero if current is already at or above the maximum.</td></tr>
<tr><td><a href="#catalyst-resource-get-overflow"><code>GetOverflow()</code></a></td><td>Returns how far current is above the Resource&#x27;s current maximum.</td></tr>
<tr><td><a href="#catalyst-resource-get-underflow"><code>GetUnderflow()</code></a></td><td>Returns how far current is below the Resource&#x27;s current minimum.</td></tr>
<tr><td><a href="#catalyst-resource-is-empty"><code>IsEmpty()</code></a></td><td>Returns whether current is at or below the Resource&#x27;s current minimum.</td></tr>
<tr><td><a href="#catalyst-resource-is-full"><code>IsFull()</code></a></td><td>Returns whether current is at or above the Resource&#x27;s current maximum.</td></tr>
<tr><td><a href="#catalyst-resource-set-current"><code>SetCurrent()</code></a></td><td>Sets current to a specific value. HARD bounds still cannot be crossed, but SOFT and OPEN bounds allow you to place current outside the usual minimum/maximum range.</td></tr>
<tr><td><a href="#catalyst-resource-change"><code>Change()</code></a></td><td>Changes the current amount. Positive values increase it and negative values decrease it. HARD bounds cannot be crossed, and ordinary movement stops at SOFT bounds.</td></tr>
<tr><td><a href="#catalyst-resource-change-past-bounds"><code>ChangePastBounds()</code></a></td><td>Changes the current amount while allowing it to pass SOFT bounds. Positive values increase it and negative values decrease it. HARD bounds still cannot be crossed.</td></tr>
<tr><td><a href="#catalyst-resource-increase"><code>Increase()</code></a></td><td>Adds a positive amount to current. The value stops at a SOFT maximum and can never pass a HARD maximum.</td></tr>
<tr><td><a href="#catalyst-resource-increase-past-maximum"><code>IncreasePastMaximum()</code></a></td><td>Adds a positive amount to current and allows it to pass a SOFT maximum. A HARD maximum still cannot be crossed.</td></tr>
<tr><td><a href="#catalyst-resource-decrease"><code>Decrease()</code></a></td><td>Subtracts a positive amount from current. The value stops at a SOFT minimum and can never pass a HARD minimum.</td></tr>
<tr><td><a href="#catalyst-resource-decrease-past-minimum"><code>DecreasePastMinimum()</code></a></td><td>Subtracts a positive amount from current and allows it to pass a SOFT minimum. A HARD minimum still cannot be crossed.</td></tr>
<tr><td><a href="#catalyst-resource-fill"><code>Fill()</code></a></td><td>Raises current to the Resource&#x27;s current maximum when it is below maximum. If current is already above maximum, that overflow is left unchanged.</td></tr>
<tr><td><a href="#catalyst-resource-empty"><code>Empty()</code></a></td><td>Lowers current to the Resource&#x27;s current minimum when it is above minimum. If current is already below minimum, that underflow is left unchanged.</td></tr>
<tr><td><a href="#catalyst-resource-refresh"><code>Refresh()</code></a></td><td>Recalculates the minimum and maximum Statistics, then checks current against the latest HARD bounds. Use this when bound Statistics may have changed and you want the Resource updated immediately.</td></tr>
<tr><td><a href="#catalyst-resource-set-minimum"><code>SetMinimum()</code></a></td><td>Changes the minimum&#x27;s base value when this Resource owns its minimum Statistic. If the minimum is sharing an external Statistic, call UnbindMinimumStatistic() first.</td></tr>
<tr><td><a href="#catalyst-resource-set-maximum"><code>SetMaximum()</code></a></td><td>Changes the maximum&#x27;s base value when this Resource owns its maximum Statistic. If the maximum is sharing an external Statistic, call UnbindMaximumStatistic() first.</td></tr>
</tbody></table>

<div class="api-method-group-title">Dynamic bounds</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-resource-bind-minimum-statistic"><code>BindMinimumStatistic()</code></a></td><td>Makes this Resource use an existing <a href="#catalyst-statistic"><code>CatalystStatistic</code></a> as its minimum. Because the Statistic is shared, changes to it change the Resource&#x27;s minimum.</td></tr>
<tr><td><a href="#catalyst-resource-bind-maximum-statistic"><code>BindMaximumStatistic()</code></a></td><td>Makes this Resource use an existing <a href="#catalyst-statistic"><code>CatalystStatistic</code></a> as its maximum. Because the Statistic is shared, changes to it change the Resource&#x27;s maximum.</td></tr>
<tr><td><a href="#catalyst-resource-unbind-minimum-statistic"><code>UnbindMinimumStatistic()</code></a></td><td>Stops sharing the external minimum Statistic. Catalyst creates a new internal Statistic starting at the external minimum&#x27;s current value.</td></tr>
<tr><td><a href="#catalyst-resource-unbind-maximum-statistic"><code>UnbindMaximumStatistic()</code></a></td><td>Stops sharing the external maximum Statistic. Catalyst creates a new internal Statistic starting at the external maximum&#x27;s current value.</td></tr>
<tr><td><a href="#catalyst-resource-is-minimum-bound"><code>IsMinimumBound()</code></a></td><td>Returns whether the minimum Statistic is using an external Statistic.</td></tr>
<tr><td><a href="#catalyst-resource-is-maximum-bound"><code>IsMaximumBound()</code></a></td><td>Returns whether the maximum Statistic is using an external Statistic.</td></tr>
<tr><td><a href="#catalyst-resource-get-minimum-statistic"><code>GetMinimumStatistic()</code></a></td><td>Returns the Statistic currently supplying this Resource&#x27;s minimum.</td></tr>
<tr><td><a href="#catalyst-resource-get-maximum-statistic"><code>GetMaximumStatistic()</code></a></td><td>Returns the Statistic currently supplying this Resource&#x27;s maximum.</td></tr>
<tr><td><a href="#catalyst-resource-add-minimum-modifier"><code>AddMinimumModifier()</code></a></td><td>Attaches one modifier to the active minimum Statistic.</td></tr>
<tr><td><a href="#catalyst-resource-destroy-minimum-modifier"><code>DestroyMinimumModifier()</code></a></td><td>Destroys one exact modifier on the active minimum Statistic.</td></tr>
<tr><td><a href="#catalyst-resource-add-maximum-modifier"><code>AddMaximumModifier()</code></a></td><td>Attaches one modifier to the active maximum Statistic.</td></tr>
<tr><td><a href="#catalyst-resource-destroy-maximum-modifier"><code>DestroyMaximumModifier()</code></a></td><td>Destroys one exact modifier on the active maximum Statistic.</td></tr>
</tbody></table>

<div class="api-method-group-title">Observation and facts</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-resource-get-last-change"><code>GetLastChange()</code></a></td><td>Returns the most recent Resource change, including changes caused by its bounds.</td></tr>
<tr><td><a href="#catalyst-resource-on-change"><code>OnChange()</code></a></td><td>Adds a callback that runs when current, minimum, or maximum changes. Catalyst calls it as fn(resource, change), where change is a <a href="#catalyst-resource-change"><code>CatalystResourceChange</code></a> describing what happened.</td></tr>
<tr><td><a href="#catalyst-resource-publish-to-fact"><code>PublishToFact()</code></a></td><td>Publishes this Resource into an Oracle Facts scope under the key you provide, then keeps that Fact updated when current, minimum, or maximum changes.</td></tr>
</tbody></table>

<div class="api-method-group-title">Flows</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-resource-add-flow"><code>AddFlow()</code></a></td><td>Attaches a standalone ResourceFlow to this Resource. Its assigned <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> then begins advancing it automatically if that tracker is running.</td></tr>
<tr><td><a href="#catalyst-resource-remove-flow"><code>RemoveFlow()</code></a></td><td>Removes a standalone Flow without destroying it, so it can be reused later.</td></tr>
<tr><td><a href="#catalyst-resource-destroy-flow"><code>DestroyFlow()</code></a></td><td>Destroys one exact standalone flow attached to this resource.</td></tr>
<tr><td><a href="#catalyst-resource-has-flow"><code>HasFlow()</code></a></td><td>Returns whether this exact standalone Flow is attached to the Resource.</td></tr>
<tr><td><a href="#catalyst-resource-get-flows"><code>GetFlows()</code></a></td><td>Returns every Flow currently changing this Resource, including standalone Flows attached directly and Flows owned by active Effects.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-resource-set-identity">
  <div class="api-method-name">SetIdentity(identity)</div>
  <p class="api-method-summary">Sets this Resource&#x27;s ID so a <a href="#catalyst-set"><code>CatalystSet</code></a> and your own code can find it later.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real,Undefined</span>
      <span class="api-argument-description">Non-empty string or finite number used as an ID to assign, or undefined to clear.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-get-identity">
  <div class="api-method-name">GetIdentity()</div>
  <p class="api-method-summary">Returns the Resource ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-set-name">
  <div class="api-method-name">SetName(name)</div>
  <p class="api-method-summary">Sets the resource name.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">New name.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-get-name">
  <div class="api-method-name">GetName()</div>
  <p class="api-method-summary">Returns the resource name.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-get-current">
  <div class="api-method-name">GetCurrent()</div>
  <p class="api-method-summary">Returns the current amount. If a HARD minimum or maximum Statistic changed since the last check, Catalyst first moves current back inside those absolute bounds.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-get-minimum">
  <div class="api-method-name">GetMinimum()</div>
  <p class="api-method-summary">Returns the Resource&#x27;s current minimum after its minimum Statistic has been calculated.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-get-maximum">
  <div class="api-method-name">GetMaximum()</div>
  <p class="api-method-summary">Returns the current maximum. If the minimum rises above it, the minimum wins.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-set-minimum-bound-mode">
  <div class="api-method-name">SetMinimumBoundMode(mode)</div>
  <p class="api-method-summary">Chooses how the minimum affects current. HARD never allows current below it. SOFT stops ordinary decreases at the minimum but explicit past-bound methods can go below it. OPEN does not restrict current at all.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">mode</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Use <a href="#enum-e-cat-resource-bound-mode"><code>eCatResourceBoundMode</code></a>.HARD, SOFT, or OPEN.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-get-minimum-bound-mode">
  <div class="api-method-name">GetMinimumBoundMode()</div>
  <p class="api-method-summary">Returns how the minimum constrains current.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-set-maximum-bound-mode">
  <div class="api-method-name">SetMaximumBoundMode(mode)</div>
  <p class="api-method-summary">Chooses how the maximum affects current. HARD never allows current above it. SOFT stops ordinary increases at the maximum but explicit past-bound methods can go above it. OPEN does not restrict current at all.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">mode</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Use <a href="#enum-e-cat-resource-bound-mode"><code>eCatResourceBoundMode</code></a>.HARD, SOFT, or OPEN.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-get-maximum-bound-mode">
  <div class="api-method-name">GetMaximumBoundMode()</div>
  <p class="api-method-summary">Returns how the maximum constrains current.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-get-fraction">
  <div class="api-method-name">GetFraction()</div>
  <p class="api-method-summary">Returns the Resource&#x27;s position between its minimum and maximum as a number from 0 to 1. Values below the minimum return 0, values above the maximum return 1, and a Resource whose minimum equals its maximum returns 1.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-get-missing">
  <div class="api-method-name">GetMissing()</div>
  <p class="api-method-summary">Returns how much could be added before current reaches the Resource&#x27;s current maximum. Returns zero if current is already at or above the maximum.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-get-overflow">
  <div class="api-method-name">GetOverflow()</div>
  <p class="api-method-summary">Returns how far current is above the Resource&#x27;s current maximum.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-get-underflow">
  <div class="api-method-name">GetUnderflow()</div>
  <p class="api-method-summary">Returns how far current is below the Resource&#x27;s current minimum.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-is-empty">
  <div class="api-method-name">IsEmpty()</div>
  <p class="api-method-summary">Returns whether current is at or below the Resource&#x27;s current minimum.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-is-full">
  <div class="api-method-name">IsFull()</div>
  <p class="api-method-summary">Returns whether current is at or above the Resource&#x27;s current maximum.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-set-current">
  <div class="api-method-name">SetCurrent(amount, [change_info])</div>
  <p class="api-method-summary">Sets current to a specific value. HARD bounds still cannot be crossed, but SOFT and OPEN bounds allow you to place current outside the usual minimum/maximum range.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">amount</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Desired current value.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">change_info <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">Optional struct describing the change: reason can say why it happened, source can say what caused it, and meta can hold any extra project data you want returned with the <a href="#catalyst-resource-change"><code>CatalystResourceChange</code></a>.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-change">CatalystResourceChange</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-change">
  <div class="api-method-name">Change(amount, [change_info])</div>
  <p class="api-method-summary">Changes the current amount. Positive values increase it and negative values decrease it. HARD bounds cannot be crossed, and ordinary movement stops at SOFT bounds.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">amount</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Amount to add to current. Use a positive number to increase or a negative number to decrease.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">change_info <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">Optional struct describing the change: reason can say why it happened, source can say what caused it, and meta can hold any extra project data you want returned with the <a href="#catalyst-resource-change"><code>CatalystResourceChange</code></a>.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-change">CatalystResourceChange</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-change-past-bounds">
  <div class="api-method-name">ChangePastBounds(amount, [change_info])</div>
  <p class="api-method-summary">Changes the current amount while allowing it to pass SOFT bounds. Positive values increase it and negative values decrease it. HARD bounds still cannot be crossed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">amount</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Amount to add to current. Use a positive number to increase or a negative number to decrease.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">change_info <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">Optional struct describing the change: reason can say why it happened, source can say what caused it, and meta can hold any extra project data you want returned with the <a href="#catalyst-resource-change"><code>CatalystResourceChange</code></a>.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-change">CatalystResourceChange</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-increase">
  <div class="api-method-name">Increase(amount, [change_info])</div>
  <p class="api-method-summary">Adds a positive amount to current. The value stops at a SOFT maximum and can never pass a HARD maximum.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">amount</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Positive amount to add. Negative inputs are treated as their positive magnitude.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">change_info <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">Optional struct describing the change: reason can say why it happened, source can say what caused it, and meta can hold any extra project data you want returned with the <a href="#catalyst-resource-change"><code>CatalystResourceChange</code></a>.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-change">CatalystResourceChange</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-increase-past-maximum">
  <div class="api-method-name">IncreasePastMaximum(amount, [change_info])</div>
  <p class="api-method-summary">Adds a positive amount to current and allows it to pass a SOFT maximum. A HARD maximum still cannot be crossed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">amount</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Positive amount to add. Negative inputs are treated as their positive magnitude.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">change_info <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">Optional struct describing the change: reason can say why it happened, source can say what caused it, and meta can hold any extra project data you want returned with the <a href="#catalyst-resource-change"><code>CatalystResourceChange</code></a>.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-change">CatalystResourceChange</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-decrease">
  <div class="api-method-name">Decrease(amount, [change_info])</div>
  <p class="api-method-summary">Subtracts a positive amount from current. The value stops at a SOFT minimum and can never pass a HARD minimum.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">amount</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Positive amount to subtract. Negative inputs are treated as their positive magnitude.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">change_info <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">Optional struct describing the change: reason can say why it happened, source can say what caused it, and meta can hold any extra project data you want returned with the <a href="#catalyst-resource-change"><code>CatalystResourceChange</code></a>.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-change">CatalystResourceChange</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-decrease-past-minimum">
  <div class="api-method-name">DecreasePastMinimum(amount, [change_info])</div>
  <p class="api-method-summary">Subtracts a positive amount from current and allows it to pass a SOFT minimum. A HARD minimum still cannot be crossed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">amount</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Positive amount to subtract. Negative inputs are treated as their positive magnitude.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">change_info <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">Optional struct describing the change: reason can say why it happened, source can say what caused it, and meta can hold any extra project data you want returned with the <a href="#catalyst-resource-change"><code>CatalystResourceChange</code></a>.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-change">CatalystResourceChange</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-fill">
  <div class="api-method-name">Fill([change_info])</div>
  <p class="api-method-summary">Raises current to the Resource&#x27;s current maximum when it is below maximum. If current is already above maximum, that overflow is left unchanged.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">change_info <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">Optional struct describing the change: reason can say why it happened, source can say what caused it, and meta can hold any extra project data you want returned with the <a href="#catalyst-resource-change"><code>CatalystResourceChange</code></a>.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-change">CatalystResourceChange</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-empty">
  <div class="api-method-name">Empty([change_info])</div>
  <p class="api-method-summary">Lowers current to the Resource&#x27;s current minimum when it is above minimum. If current is already below minimum, that underflow is left unchanged.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">change_info <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">Optional struct describing the change: reason can say why it happened, source can say what caused it, and meta can hold any extra project data you want returned with the <a href="#catalyst-resource-change"><code>CatalystResourceChange</code></a>.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-change">CatalystResourceChange</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-refresh">
  <div class="api-method-name">Refresh()</div>
  <p class="api-method-summary">Recalculates the minimum and maximum Statistics, then checks current against the latest HARD bounds. Use this when bound Statistics may have changed and you want the Resource updated immediately.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-change">CatalystResourceChange</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-set-minimum">
  <div class="api-method-name">SetMinimum(value)</div>
  <p class="api-method-summary">Changes the minimum&#x27;s base value when this Resource owns its minimum Statistic. If the minimum is sharing an external Statistic, call UnbindMinimumStatistic() first.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">value</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">New owned minimum base value.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-set-maximum">
  <div class="api-method-name">SetMaximum(value)</div>
  <p class="api-method-summary">Changes the maximum&#x27;s base value when this Resource owns its maximum Statistic. If the maximum is sharing an external Statistic, call UnbindMaximumStatistic() first.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">value</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">New owned maximum base value.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-bind-minimum-statistic">
  <div class="api-method-name">BindMinimumStatistic(statistic)</div>
  <p class="api-method-summary">Makes this Resource use an existing <a href="#catalyst-statistic"><code>CatalystStatistic</code></a> as its minimum. Because the Statistic is shared, changes to it change the Resource&#x27;s minimum.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">statistic</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
      <span class="api-argument-description">Statistic to bind.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-bind-maximum-statistic">
  <div class="api-method-name">BindMaximumStatistic(statistic)</div>
  <p class="api-method-summary">Makes this Resource use an existing <a href="#catalyst-statistic"><code>CatalystStatistic</code></a> as its maximum. Because the Statistic is shared, changes to it change the Resource&#x27;s maximum.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">statistic</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
      <span class="api-argument-description">Statistic to bind.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-unbind-minimum-statistic">
  <div class="api-method-name">UnbindMinimumStatistic()</div>
  <p class="api-method-summary">Stops sharing the external minimum Statistic. Catalyst creates a new internal Statistic starting at the external minimum&#x27;s current value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-unbind-maximum-statistic">
  <div class="api-method-name">UnbindMaximumStatistic()</div>
  <p class="api-method-summary">Stops sharing the external maximum Statistic. Catalyst creates a new internal Statistic starting at the external maximum&#x27;s current value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-is-minimum-bound">
  <div class="api-method-name">IsMinimumBound()</div>
  <p class="api-method-summary">Returns whether the minimum Statistic is using an external Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-is-maximum-bound">
  <div class="api-method-name">IsMaximumBound()</div>
  <p class="api-method-summary">Returns whether the maximum Statistic is using an external Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-get-minimum-statistic">
  <div class="api-method-name">GetMinimumStatistic()</div>
  <p class="api-method-summary">Returns the Statistic currently supplying this Resource&#x27;s minimum.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-get-maximum-statistic">
  <div class="api-method-name">GetMaximumStatistic()</div>
  <p class="api-method-summary">Returns the Statistic currently supplying this Resource&#x27;s maximum.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-add-minimum-modifier">
  <div class="api-method-name">AddMinimumModifier(modifier)</div>
  <p class="api-method-summary">Attaches one modifier to the active minimum Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Modifier to attach.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-destroy-minimum-modifier">
  <div class="api-method-name">DestroyMinimumModifier(modifier)</div>
  <p class="api-method-summary">Destroys one exact modifier on the active minimum Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Modifier to destroy.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-add-maximum-modifier">
  <div class="api-method-name">AddMaximumModifier(modifier)</div>
  <p class="api-method-summary">Attaches one modifier to the active maximum Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Modifier to attach.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-destroy-maximum-modifier">
  <div class="api-method-name">DestroyMaximumModifier(modifier)</div>
  <p class="api-method-summary">Destroys one exact modifier on the active maximum Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Modifier to destroy.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-get-last-change">
  <div class="api-method-name">GetLastChange()</div>
  <p class="api-method-summary">Returns the most recent Resource change, including changes caused by its bounds.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-change">CatalystResourceChange</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-on-change">
  <div class="api-method-name">OnChange(callback)</div>
  <p class="api-method-summary">Adds a callback that runs when current, minimum, or maximum changes. Catalyst calls it as fn(resource, change), where change is a <a href="#catalyst-resource-change"><code>CatalystResourceChange</code></a> describing what happened.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function called as fn(resource, change) whenever the Resource state changes.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-subscription">CatalystSubscription</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-add-flow">
  <div class="api-method-name">AddFlow(flow)</div>
  <p class="api-method-summary">Attaches a standalone ResourceFlow to this Resource. Its assigned <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> then begins advancing it automatically if that tracker is running.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flow</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
      <span class="api-argument-description">Detached flow to attach.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#catalyst-resource-flow"><code>CatalystResourceFlow</code></a> <span aria-hidden="true">·</span> <a href="{{ '/catalyst/resource-flows' | relative_url }}">Resource Flows</a></div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-remove-flow">
  <div class="api-method-name">RemoveFlow(flow)</div>
  <p class="api-method-summary">Removes a standalone Flow without destroying it, so it can be reused later.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flow</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
      <span class="api-argument-description">Flow to detach.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-destroy-flow">
  <div class="api-method-name">DestroyFlow(flow)</div>
  <p class="api-method-summary">Destroys one exact standalone flow attached to this resource.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flow</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
      <span class="api-argument-description">Flow to destroy.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-has-flow">
  <div class="api-method-name">HasFlow(flow)</div>
  <p class="api-method-summary">Returns whether this exact standalone Flow is attached to the Resource.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flow</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
      <span class="api-argument-description">Flow to check.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-get-flows">
  <div class="api-method-name">GetFlows()</div>
  <p class="api-method-summary">Returns every Flow currently changing this Resource, including standalone Flows attached directly and Flows owned by active Effects.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-publish-to-fact">
  <div class="api-method-name">PublishToFact(facts, key, [transform])</div>
  <p class="api-method-summary">Publishes this Resource into an Oracle Facts scope under the key you provide, then keeps that Fact updated when current, minimum, or maximum changes.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">facts</span>
      <span class="api-argument-type">Struct.OracleFacts</span>
      <span class="api-argument-description">Oracle fact scope to update.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">key</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Fact key to publish.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">transform <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Optional function called as fn(resource). Return the value you want stored in Oracle instead of the Resource&#x27;s current amount.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-fact-binding">CatalystFactBinding</a>,Undefined</span>
    </div>
  </div>
</div>

### CatalystResourceChange
{: #catalyst-resource-change .api-type-title }

Describes one Resource update. It records the value before and after, what was requested, what was actually applied after minimum/maximum rules, and any optional reason/source information.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-resource-change-did-change"><code>DidChange()</code></a></td><td>Returns true if the Resource value, minimum, or maximum changed.</td></tr>
<tr><td><a href="#catalyst-resource-change-succeeded"><code>Succeeded()</code></a></td><td>Returns whether the resource operation was accepted.</td></tr>
<tr><td><a href="#catalyst-resource-change-get-operation"><code>GetOperation()</code></a></td><td>Returns the recorded <a href="#enum-e-cat-resource-operation"><code>eCatResourceOperation</code></a>.</td></tr>
<tr><td><a href="#catalyst-resource-change-get-previous"><code>GetPrevious()</code></a></td><td>Returns the Resource value before the change.</td></tr>
<tr><td><a href="#catalyst-resource-change-get-requested"><code>GetRequested()</code></a></td><td>Returns the caller-requested amount when the operation has one.</td></tr>
<tr><td><a href="#catalyst-resource-change-get-target"><code>GetTarget()</code></a></td><td>Returns the value the operation tried to reach before Resource bound rules changed or limited it.</td></tr>
<tr><td><a href="#catalyst-resource-change-get-applied"><code>GetApplied()</code></a></td><td>Returns how much current actually changed after Resource bounds were applied. Positive means an increase and negative means a decrease.</td></tr>
<tr><td><a href="#catalyst-resource-change-get-current"><code>GetCurrent()</code></a></td><td>Returns the Resource value after the change.</td></tr>
<tr><td><a href="#catalyst-resource-change-get-previous-minimum"><code>GetPreviousMinimum()</code></a></td><td>Returns the minimum value Catalyst was using before the change.</td></tr>
<tr><td><a href="#catalyst-resource-change-get-previous-maximum"><code>GetPreviousMaximum()</code></a></td><td>Returns the maximum value Catalyst was using before the change.</td></tr>
<tr><td><a href="#catalyst-resource-change-get-minimum"><code>GetMinimum()</code></a></td><td>Returns the minimum value Catalyst used for this operation.</td></tr>
<tr><td><a href="#catalyst-resource-change-get-maximum"><code>GetMaximum()</code></a></td><td>Returns the maximum value Catalyst used for this operation.</td></tr>
<tr><td><a href="#catalyst-resource-change-get-reason"><code>GetReason()</code></a></td><td>Returns optional reason supplied by your project.</td></tr>
<tr><td><a href="#catalyst-resource-change-get-source"><code>GetSource()</code></a></td><td>Returns the optional source responsible for the operation.</td></tr>
<tr><td><a href="#catalyst-resource-change-get-meta"><code>GetMeta()</code></a></td><td>Returns any extra project data supplied with this Resource change.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-resource-change-did-change">
  <div class="api-method-name">DidChange()</div>
  <p class="api-method-summary">Returns true if the Resource value, minimum, or maximum changed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-change-succeeded">
  <div class="api-method-name">Succeeded()</div>
  <p class="api-method-summary">Returns whether the resource operation was accepted.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-change-get-operation">
  <div class="api-method-name">GetOperation()</div>
  <p class="api-method-summary">Returns the recorded <a href="#enum-e-cat-resource-operation"><code>eCatResourceOperation</code></a>.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-change-get-previous">
  <div class="api-method-name">GetPrevious()</div>
  <p class="api-method-summary">Returns the Resource value before the change.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-change-get-requested">
  <div class="api-method-name">GetRequested()</div>
  <p class="api-method-summary">Returns the caller-requested amount when the operation has one.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-change-get-target">
  <div class="api-method-name">GetTarget()</div>
  <p class="api-method-summary">Returns the value the operation tried to reach before Resource bound rules changed or limited it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-change-get-applied">
  <div class="api-method-name">GetApplied()</div>
  <p class="api-method-summary">Returns how much current actually changed after Resource bounds were applied. Positive means an increase and negative means a decrease.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-change-get-current">
  <div class="api-method-name">GetCurrent()</div>
  <p class="api-method-summary">Returns the Resource value after the change.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-change-get-previous-minimum">
  <div class="api-method-name">GetPreviousMinimum()</div>
  <p class="api-method-summary">Returns the minimum value Catalyst was using before the change.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-change-get-previous-maximum">
  <div class="api-method-name">GetPreviousMaximum()</div>
  <p class="api-method-summary">Returns the maximum value Catalyst was using before the change.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-change-get-minimum">
  <div class="api-method-name">GetMinimum()</div>
  <p class="api-method-summary">Returns the minimum value Catalyst used for this operation.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-change-get-maximum">
  <div class="api-method-name">GetMaximum()</div>
  <p class="api-method-summary">Returns the maximum value Catalyst used for this operation.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-change-get-reason">
  <div class="api-method-name">GetReason()</div>
  <p class="api-method-summary">Returns optional reason supplied by your project.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-change-get-source">
  <div class="api-method-name">GetSource()</div>
  <p class="api-method-summary">Returns the optional source responsible for the operation.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-change-get-meta">
  <div class="api-method-name">GetMeta()</div>
  <p class="api-method-summary">Returns any extra project data supplied with this Resource change.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any</span>
    </div>
  </div>
</div>

### CatalystResourceFlow
{: #catalyst-resource-flow .api-type-title }

Creates a ResourceFlow that changes a Resource as countdown time passes. Positive rates add to the Resource and negative rates remove from it. Passing a number creates a private rate Statistic; passing an existing Statistic makes the Flow share that Statistic as its rate.

```gml
new CatalystResourceFlow(rate, source_label, source_id, source_meta)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">rate</span>
      <span class="api-argument-type">Real,Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
      <span class="api-argument-description">Resource change per countdown unit, or an existing Statistic that supplies that rate. Positive increases the Resource; negative decreases it.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">source_label <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Optional human-readable label copied into ResourceChange results so you can tell what caused the movement.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">source_id <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional source ID copied into ResourceChange results.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">source_meta <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional extra project data copied into ResourceChange results. Catalyst does not interpret it.</span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Identity and source</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-resource-flow-set-identity"><code>SetIdentity()</code></a></td><td>Sets an optional ID for this Flow so Catalyst save/restore or your own code can identify it.</td></tr>
<tr><td><a href="#catalyst-resource-flow-get-identity"><code>GetIdentity()</code></a></td><td>Returns the flow&#x27;s optional ID.</td></tr>
<tr><td><a href="#catalyst-resource-flow-set-name"><code>SetName()</code></a></td><td>Sets the flow name.</td></tr>
<tr><td><a href="#catalyst-resource-flow-get-name"><code>GetName()</code></a></td><td>Returns the flow name.</td></tr>
<tr><td><a href="#catalyst-resource-flow-set-source-label"><code>SetSourceLabel()</code></a></td><td>Sets the source label copied into Resource changes.</td></tr>
<tr><td><a href="#catalyst-resource-flow-set-source-id"><code>SetSourceId()</code></a></td><td>Sets the source ID copied into ResourceChange results.</td></tr>
<tr><td><a href="#catalyst-resource-flow-set-source-meta"><code>SetSourceMeta()</code></a></td><td>Stores extra project data to copy into ResourceChange results caused by this Flow. Catalyst does not interpret it.</td></tr>
</tbody></table>

<div class="api-method-group-title">Rate</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-resource-flow-set-rate"><code>SetRate()</code></a></td><td>Changes the Flow&#x27;s rate when it is using its own internal rate Statistic. If the Flow is sharing an external Statistic, call UnbindRateStatistic() before setting a direct value.</td></tr>
<tr><td><a href="#catalyst-resource-flow-bind-rate-statistic"><code>BindRateStatistic()</code></a></td><td>Makes this Flow use an existing <a href="#catalyst-statistic"><code>CatalystStatistic</code></a> as its rate. Because the Statistic is shared, later changes to it immediately change the Flow&#x27;s rate.</td></tr>
<tr><td><a href="#catalyst-resource-flow-unbind-rate-statistic"><code>UnbindRateStatistic()</code></a></td><td>Stops sharing the external rate Statistic. Catalyst creates a new internal Statistic starting at the external Statistic&#x27;s current value.</td></tr>
<tr><td><a href="#catalyst-resource-flow-is-rate-bound"><code>IsRateBound()</code></a></td><td>Returns whether the active rate Statistic is using an external Statistic.</td></tr>
<tr><td><a href="#catalyst-resource-flow-get-rate-statistic"><code>GetRateStatistic()</code></a></td><td>Returns the Statistic currently supplying this Flow&#x27;s rate.</td></tr>
</tbody></table>

<div class="api-method-group-title">State and timing</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-resource-flow-set-active"><code>SetActive()</code></a></td><td>Turns Resource movement on or off without changing the Flow&#x27;s rate or remaining delay.</td></tr>
<tr><td><a href="#catalyst-resource-flow-is-active"><code>IsActive()</code></a></td><td>Returns whether this Flow is currently allowed to move its Resource when countdown time passes.</td></tr>
<tr><td><a href="#catalyst-resource-flow-delay"><code>Delay()</code></a></td><td>Sets how much countdown time must pass before this Flow can start moving its Resource. Calling Delay() again replaces the remaining delay rather than adding to it.</td></tr>
<tr><td><a href="#catalyst-resource-flow-is-delayed"><code>IsDelayed()</code></a></td><td>Returns whether delay remains.</td></tr>
<tr><td><a href="#catalyst-resource-flow-get-delay-remaining"><code>GetDelayRemaining()</code></a></td><td>Returns remaining delay.</td></tr>
<tr><td><a href="#catalyst-resource-flow-clear-delay"><code>ClearDelay()</code></a></td><td>Removes the current delay so the Flow can move the next time countdown advances. It also clears any partial progress this Flow had made toward an Effect tick.</td></tr>
<tr><td><a href="#catalyst-resource-flow-set-countdown-tracker"><code>SetCountdownTracker()</code></a></td><td>Chooses which <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> advances this Flow when it is attached directly to a Resource. A Flow owned by an Effect uses the Effect&#x27;s timing instead.</td></tr>
<tr><td><a href="#catalyst-resource-flow-get-countdown-tracker"><code>GetCountdownTracker()</code></a></td><td>Returns the tracker assigned to this flow.</td></tr>
</tbody></table>

<div class="api-method-group-title">Lifecycle</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-resource-flow-destroy"><code>Destroy()</code></a></td><td>Destroys this Flow. If it is attached directly to a Resource, Catalyst detaches it first. If an Effect owns it, the Effect handles the removal so its ownership stays consistent.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-resource-flow-set-identity">
  <div class="api-method-name">SetIdentity(identity)</div>
  <p class="api-method-summary">Sets an optional ID for this Flow so Catalyst save/restore or your own code can identify it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real,Undefined</span>
      <span class="api-argument-description">Non-empty string or finite number used as an ID to assign, or undefined to clear.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-get-identity">
  <div class="api-method-name">GetIdentity()</div>
  <p class="api-method-summary">Returns the flow&#x27;s optional ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-set-name">
  <div class="api-method-name">SetName(name)</div>
  <p class="api-method-summary">Sets the flow name.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">New name.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-get-name">
  <div class="api-method-name">GetName()</div>
  <p class="api-method-summary">Returns the flow name.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-set-rate">
  <div class="api-method-name">SetRate(value)</div>
  <p class="api-method-summary">Changes the Flow&#x27;s rate when it is using its own internal rate Statistic. If the Flow is sharing an external Statistic, call UnbindRateStatistic() before setting a direct value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">value</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">New Resource change per countdown unit. Positive increases the Resource; negative decreases it.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-bind-rate-statistic">
  <div class="api-method-name">BindRateStatistic(statistic)</div>
  <p class="api-method-summary">Makes this Flow use an existing <a href="#catalyst-statistic"><code>CatalystStatistic</code></a> as its rate. Because the Statistic is shared, later changes to it immediately change the Flow&#x27;s rate.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">statistic</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
      <span class="api-argument-description">Statistic to bind.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-unbind-rate-statistic">
  <div class="api-method-name">UnbindRateStatistic()</div>
  <p class="api-method-summary">Stops sharing the external rate Statistic. Catalyst creates a new internal Statistic starting at the external Statistic&#x27;s current value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-is-rate-bound">
  <div class="api-method-name">IsRateBound()</div>
  <p class="api-method-summary">Returns whether the active rate Statistic is using an external Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-get-rate-statistic">
  <div class="api-method-name">GetRateStatistic()</div>
  <p class="api-method-summary">Returns the Statistic currently supplying this Flow&#x27;s rate.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-set-active">
  <div class="api-method-name">SetActive(active)</div>
  <p class="api-method-summary">Turns Resource movement on or off without changing the Flow&#x27;s rate or remaining delay.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">active</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether the flow should advance.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-is-active">
  <div class="api-method-name">IsActive()</div>
  <p class="api-method-summary">Returns whether this Flow is currently allowed to move its Resource when countdown time passes.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-delay">
  <div class="api-method-name">Delay(amount)</div>
  <p class="api-method-summary">Sets how much countdown time must pass before this Flow can start moving its Resource. Calling Delay() again replaces the remaining delay rather than adding to it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">amount</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Non-negative delay amount.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-is-delayed">
  <div class="api-method-name">IsDelayed()</div>
  <p class="api-method-summary">Returns whether delay remains.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-get-delay-remaining">
  <div class="api-method-name">GetDelayRemaining()</div>
  <p class="api-method-summary">Returns remaining delay.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-clear-delay">
  <div class="api-method-name">ClearDelay()</div>
  <p class="api-method-summary">Removes the current delay so the Flow can move the next time countdown advances. It also clears any partial progress this Flow had made toward an Effect tick.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-set-countdown-tracker">
  <div class="api-method-name">SetCountdownTracker(tracker)</div>
  <p class="api-method-summary">Chooses which <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> advances this Flow when it is attached directly to a Resource. A Flow owned by an Effect uses the Effect&#x27;s timing instead.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tracker</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-countdown-tracker">CatalystCountdownTracker</a>,Noone</span>
      <span class="api-argument-description">Tracker to assign, or noone.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-get-countdown-tracker">
  <div class="api-method-name">GetCountdownTracker()</div>
  <p class="api-method-summary">Returns the tracker assigned to this flow.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-countdown-tracker">CatalystCountdownTracker</a>,Noone</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-set-source-label">
  <div class="api-method-name">SetSourceLabel(source_label)</div>
  <p class="api-method-summary">Sets the source label copied into Resource changes.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source_label</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">New label.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-set-source-id">
  <div class="api-method-name">SetSourceId(source_id)</div>
  <p class="api-method-summary">Sets the source ID copied into ResourceChange results.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source_id</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Source ID to copy into future ResourceChange results.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-set-source-meta">
  <div class="api-method-name">SetSourceMeta(source_meta)</div>
  <p class="api-method-summary">Stores extra project data to copy into ResourceChange results caused by this Flow. Catalyst does not interpret it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source_meta</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Extra project data to copy into future ResourceChange results.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-destroy">
  <div class="api-method-name">Destroy()</div>
  <p class="api-method-summary">Destroys this Flow. If it is attached directly to a Resource, Catalyst detaches it first. If an Effect owns it, the Effect handles the removal so its ownership stays consistent.</p>
</div>

### CatalystResourceFlowResult
{: #catalyst-resource-flow-result .api-type-title }

Describes one Resource movement produced by an Effect-owned Flow during a successful Effect tick, including the rate, time amount, multiplier, requested movement, and exact Resource change.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-resource-flow-result-succeeded"><code>Succeeded()</code></a></td><td>Returns whether the Resource change succeeded.</td></tr>
<tr><td><a href="#catalyst-resource-flow-result-get-flow"><code>GetFlow()</code></a></td><td>Returns the flow that requested movement.</td></tr>
<tr><td><a href="#catalyst-resource-flow-result-get-resource"><code>GetResource()</code></a></td><td>Returns the moved Resource.</td></tr>
<tr><td><a href="#catalyst-resource-flow-result-get-countdown-amount"><code>GetCountdownAmount()</code></a></td><td>Returns the amount of Flow time used for this movement after any delay.</td></tr>
<tr><td><a href="#catalyst-resource-flow-result-get-rate"><code>GetRate()</code></a></td><td>Returns the rate used for this movement. Positive means the Resource increases; negative means it decreases.</td></tr>
<tr><td><a href="#catalyst-resource-flow-result-get-multiplier"><code>GetMultiplier()</code></a></td><td>Returns the applied effect-tick multiplier.</td></tr>
<tr><td><a href="#catalyst-resource-flow-result-get-requested"><code>GetRequested()</code></a></td><td>Returns the movement requested from the Resource before its bounds were applied. Positive means increase; negative means decrease.</td></tr>
<tr><td><a href="#catalyst-resource-flow-result-get-change"><code>GetChange()</code></a></td><td>Returns the exact Resource change result.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-resource-flow-result-succeeded">
  <div class="api-method-name">Succeeded()</div>
  <p class="api-method-summary">Returns whether the Resource change succeeded.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-result-get-flow">
  <div class="api-method-name">GetFlow()</div>
  <p class="api-method-summary">Returns the flow that requested movement.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-result-get-resource">
  <div class="api-method-name">GetResource()</div>
  <p class="api-method-summary">Returns the moved Resource.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-result-get-countdown-amount">
  <div class="api-method-name">GetCountdownAmount()</div>
  <p class="api-method-summary">Returns the amount of Flow time used for this movement after any delay.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-result-get-rate">
  <div class="api-method-name">GetRate()</div>
  <p class="api-method-summary">Returns the rate used for this movement. Positive means the Resource increases; negative means it decreases.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-result-get-multiplier">
  <div class="api-method-name">GetMultiplier()</div>
  <p class="api-method-summary">Returns the applied effect-tick multiplier.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-result-get-requested">
  <div class="api-method-name">GetRequested()</div>
  <p class="api-method-summary">Returns the movement requested from the Resource before its bounds were applied. Positive means increase; negative means decrease.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-resource-flow-result-get-change">
  <div class="api-method-name">GetChange()</div>
  <p class="api-method-summary">Returns the exact Resource change result.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-change">CatalystResourceChange</a></span>
    </div>
  </div>
</div>

## Effects

### CatalystEffect
{: #catalyst-effect .api-type-title }

Creates an Effect: a reusable bundle that can attach Modifiers and ResourceFlows when applied through an EffectManager. Effects can be permanent or timed, can run apply/tick/remove callbacks, and can control what happens when the same Effect ID is applied again.

```gml
new CatalystEffect(identity, duration, source_label, source_id, source_meta)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">Optional Effect ID. EffectManager uses matching IDs for reapplication rules such as REPLACE, REFRESH, and EXTEND.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">duration <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">How long the Effect lasts after applying. Positive values count down, negative means permanent, and zero is already expired.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">source_label <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Optional human-readable label describing where this Effect came from.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">source_id <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional value your game can use to identify the exact source that created this Effect.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">source_meta <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional extra project data to store with the Effect. Catalyst does not interpret it.</span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Identity and reapplication</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-effect-set-identity"><code>SetIdentity()</code></a></td><td>Sets this Effect&#x27;s ID. When the Effect is applied, its EffectManager compares this ID with active Effects to decide whether the reapplication policy should run.</td></tr>
<tr><td><a href="#catalyst-effect-get-identity"><code>GetIdentity()</code></a></td><td>Returns the Effect ID.</td></tr>
<tr><td><a href="#catalyst-effect-set-family"><code>SetFamily()</code></a></td><td>Gives this Effect a family ID so you can find a group of related active Effects even when they have different individual IDs.</td></tr>
<tr><td><a href="#catalyst-effect-get-family"><code>GetFamily()</code></a></td><td>Returns the Effect family value.</td></tr>
<tr><td><a href="#catalyst-effect-set-reapply-policy"><code>SetReapplyPolicy()</code></a></td><td>Chooses what the EffectManager should do if this Effect is applied while another active Effect has the same ID.</td></tr>
<tr><td><a href="#catalyst-effect-get-reapply-policy"><code>GetReapplyPolicy()</code></a></td><td>Returns the current reapplication policy.</td></tr>
</tbody></table>

<div class="api-method-group-title">Duration and timing source</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-effect-set-duration"><code>SetDuration()</code></a></td><td>Replaces both this Effect&#x27;s remaining time and the duration ResetDuration() returns to. If an active Effect is set to zero duration, it is removed immediately.</td></tr>
<tr><td><a href="#catalyst-effect-reset-duration"><code>ResetDuration()</code></a></td><td>Resets the Effect&#x27;s remaining time to its configured maximum duration.</td></tr>
<tr><td><a href="#catalyst-effect-set-countdown-tracker"><code>SetCountdownTracker()</code></a></td><td>Chooses which <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> advances this Effect&#x27;s duration and tick timer while the Effect is active.</td></tr>
<tr><td><a href="#catalyst-effect-get-countdown-tracker"><code>GetCountdownTracker()</code></a></td><td>Returns the countdown tracker assigned to this Effect.</td></tr>
</tbody></table>

<div class="api-method-group-title">Application chance</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-effect-set-chance-to-apply"><code>SetChanceToApply()</code></a></td><td>Sets the Effect&#x27;s chance of applying when it uses its own internal chance Statistic. If you bound an external Statistic with BindChanceToApplyStatistic(), unbind it first.</td></tr>
<tr><td><a href="#catalyst-effect-bind-chance-to-apply-statistic"><code>BindChanceToApplyStatistic()</code></a></td><td>Makes this Effect use an existing <a href="#catalyst-statistic"><code>CatalystStatistic</code></a> for its application chance. Because the Statistic is shared, changes to it immediately affect future applications.</td></tr>
<tr><td><a href="#catalyst-effect-unbind-chance-to-apply-statistic"><code>UnbindChanceToApplyStatistic()</code></a></td><td>Stops sharing the external application-chance Statistic. Catalyst creates a new internal Statistic starting at the external Statistic&#x27;s current value.</td></tr>
<tr><td><a href="#catalyst-effect-is-chance-to-apply-bound"><code>IsChanceToApplyBound()</code></a></td><td>Returns whether application chance is using an external Statistic.</td></tr>
<tr><td><a href="#catalyst-effect-get-chance-to-apply-statistic"><code>GetChanceToApplyStatistic()</code></a></td><td>Returns the active application-chance Statistic.</td></tr>
</tbody></table>

<div class="api-method-group-title">Ticking</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-effect-set-tick-interval"><code>SetTickInterval()</code></a></td><td>Chooses how much Effect time must pass between ticks. Positive values enable ticking; zero or a negative value disables it.</td></tr>
<tr><td><a href="#catalyst-effect-clear-tick-interval"><code>ClearTickInterval()</code></a></td><td>Turns ticking off and discards any partial progress toward the next tick.</td></tr>
<tr><td><a href="#catalyst-effect-get-tick-interval"><code>GetTickInterval()</code></a></td><td>Returns the positive interval, or a negative value when ticking is disabled.</td></tr>
<tr><td><a href="#catalyst-effect-set-chance-per-tick"><code>SetChancePerTick()</code></a></td><td>Sets the chance that each completed tick succeeds when the Effect uses its own internal chance Statistic. If an external Statistic is bound, unbind it first.</td></tr>
<tr><td><a href="#catalyst-effect-bind-chance-per-tick-statistic"><code>BindChancePerTickStatistic()</code></a></td><td>Makes this Effect use an existing <a href="#catalyst-statistic"><code>CatalystStatistic</code></a> for its per-tick chance. Because the Statistic is shared, changes to it affect later ticks.</td></tr>
<tr><td><a href="#catalyst-effect-unbind-chance-per-tick-statistic"><code>UnbindChancePerTickStatistic()</code></a></td><td>Stops using the external per-tick chance and replaces it with a new internal Statistic at the same current value.</td></tr>
<tr><td><a href="#catalyst-effect-is-chance-per-tick-bound"><code>IsChancePerTickBound()</code></a></td><td>Returns whether per-tick chance is using an external Statistic.</td></tr>
<tr><td><a href="#catalyst-effect-get-chance-per-tick-statistic"><code>GetChancePerTickStatistic()</code></a></td><td>Returns the active per-tick chance Statistic.</td></tr>
</tbody></table>

<div class="api-method-group-title">Callbacks</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-effect-set-on-apply"><code>SetOnApply()</code></a></td><td>Sets a callback that runs after the Effect has successfully become active and its Modifiers and Flows have been attached.</td></tr>
<tr><td><a href="#catalyst-effect-clear-on-apply"><code>ClearOnApply()</code></a></td><td>Clears the application callback.</td></tr>
<tr><td><a href="#catalyst-effect-set-resolve-tick"><code>SetResolveTick()</code></a></td><td>Sets a callback that runs after the normal tick chance is checked but before owned Flows move Resources. Use the <a href="#catalyst-effect-tick-result"><code>CatalystEffectTickResult</code></a> to cancel the tick or change its movement multiplier.</td></tr>
<tr><td><a href="#catalyst-effect-clear-resolve-tick"><code>ClearResolveTick()</code></a></td><td>Removes the ResolveTick callback, so Catalyst uses the normal tick result and movement multiplier without a custom adjustment.</td></tr>
<tr><td><a href="#catalyst-effect-set-on-tick"><code>SetOnTick()</code></a></td><td>Sets a callback that runs after every completed tick, after any Flow movement. It runs whether the tick succeeded or failed its chance check.</td></tr>
<tr><td><a href="#catalyst-effect-clear-on-tick"><code>ClearOnTick()</code></a></td><td>Clears the post-movement tick callback.</td></tr>
<tr><td><a href="#catalyst-effect-set-on-remove"><code>SetOnRemove()</code></a></td><td>Sets a callback that runs when an active Effect is removed. Its Modifiers and Flows have already been removed. During the callback, effect.manager and effect.owner still point to the EffectManager and owner it was removed from.</td></tr>
<tr><td><a href="#catalyst-effect-clear-on-remove"><code>ClearOnRemove()</code></a></td><td>Clears the removal callback.</td></tr>
</tbody></table>

<div class="api-method-group-title">Flows and modifiers</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-effect-add-flow"><code>AddFlow()</code></a></td><td>Adds a detached ResourceFlow to this Effect. The Flow is not attached to the Resource yet; it is attached only if the Effect successfully applies, and the Effect owns it afterward.</td></tr>
<tr><td><a href="#catalyst-effect-remove-flow"><code>RemoveFlow()</code></a></td><td>Removes and destroys one exact Flow owned by this Effect.</td></tr>
<tr><td><a href="#catalyst-effect-add-modifier"><code>AddModifier()</code></a></td><td>Adds a detached Modifier to this Effect. The Modifier is not attached to the Statistic yet; it is attached only if the Effect successfully applies, and the Effect owns it afterward.</td></tr>
<tr><td><a href="#catalyst-effect-remove-modifier"><code>RemoveModifier()</code></a></td><td>Removes and destroys one exact Modifier owned by this Effect.</td></tr>
</tbody></table>

<div class="api-method-group-title">Tags</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-effect-add-tag"><code>AddTag()</code></a></td><td>Adds a tag if absent.</td></tr>
<tr><td><a href="#catalyst-effect-remove-tag"><code>RemoveTag()</code></a></td><td>Removes every matching tag.</td></tr>
<tr><td><a href="#catalyst-effect-has-tag"><code>HasTag()</code></a></td><td>Returns whether this Effect contains a tag.</td></tr>
<tr><td><a href="#catalyst-effect-clear-tags"><code>ClearTags()</code></a></td><td>Removes every tag.</td></tr>
</tbody></table>

<div class="api-method-group-title">Lifecycle</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-effect-destroy"><code>Destroy()</code></a></td><td>Destroys this Effect. If it is active, its EffectManager removes it normally so callbacks and owned Modifiers/Flows are cleaned up. If it has not been applied, its stored Modifiers and Flows are destroyed directly.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-effect-set-identity">
  <div class="api-method-name">SetIdentity(identity)</div>
  <p class="api-method-summary">Sets this Effect&#x27;s ID. When the Effect is applied, its EffectManager compares this ID with active Effects to decide whether the reapplication policy should run.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real,Undefined</span>
      <span class="api-argument-description">Non-empty string or finite number used as an ID to assign, or undefined to clear.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-get-identity">
  <div class="api-method-name">GetIdentity()</div>
  <p class="api-method-summary">Returns the Effect ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-set-family">
  <div class="api-method-name">SetFamily(family)</div>
  <p class="api-method-summary">Gives this Effect a family ID so you can find a group of related active Effects even when they have different individual IDs.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">family</span>
      <span class="api-argument-type">String,Real,Undefined</span>
      <span class="api-argument-description">Shared string or finite number used to group related Effects, or undefined to clear the family.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-get-family">
  <div class="api-method-name">GetFamily()</div>
  <p class="api-method-summary">Returns the Effect family value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-set-reapply-policy">
  <div class="api-method-name">SetReapplyPolicy(policy)</div>
  <p class="api-method-summary">Chooses what the EffectManager should do if this Effect is applied while another active Effect has the same ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">policy</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Reapplication rule from <a href="#enum-e-cat-effect-reapply-policy"><code>eCatEffectReapplyPolicy</code></a>: STACK, IGNORE, REPLACE, REFRESH, or EXTEND.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-get-reapply-policy">
  <div class="api-method-name">GetReapplyPolicy()</div>
  <p class="api-method-summary">Returns the current reapplication policy.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-set-duration">
  <div class="api-method-name">SetDuration(duration)</div>
  <p class="api-method-summary">Replaces both this Effect&#x27;s remaining time and the duration ResetDuration() returns to. If an active Effect is set to zero duration, it is removed immediately.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">duration</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Positive timed duration, zero expired, or negative permanent duration.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-reset-duration">
  <div class="api-method-name">ResetDuration()</div>
  <p class="api-method-summary">Resets the Effect&#x27;s remaining time to its configured maximum duration.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-set-countdown-tracker">
  <div class="api-method-name">SetCountdownTracker(tracker)</div>
  <p class="api-method-summary">Chooses which <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> advances this Effect&#x27;s duration and tick timer while the Effect is active.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tracker</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-countdown-tracker">CatalystCountdownTracker</a>,Noone</span>
      <span class="api-argument-description">Tracker to assign, or noone.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-get-countdown-tracker">
  <div class="api-method-name">GetCountdownTracker()</div>
  <p class="api-method-summary">Returns the countdown tracker assigned to this Effect.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-countdown-tracker">CatalystCountdownTracker</a>,Noone</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-set-chance-to-apply">
  <div class="api-method-name">SetChanceToApply(value)</div>
  <p class="api-method-summary">Sets the Effect&#x27;s chance of applying when it uses its own internal chance Statistic. If you bound an external Statistic with BindChanceToApplyStatistic(), unbind it first.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">value</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">New chance value, where 0 never applies and 1 always applies. Values below 0 are treated as 0 and values above 1 as 1 when Catalyst checks the chance.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-bind-chance-to-apply-statistic">
  <div class="api-method-name">BindChanceToApplyStatistic(statistic)</div>
  <p class="api-method-summary">Makes this Effect use an existing <a href="#catalyst-statistic"><code>CatalystStatistic</code></a> for its application chance. Because the Statistic is shared, changes to it immediately affect future applications.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">statistic</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
      <span class="api-argument-description">Statistic to bind.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-unbind-chance-to-apply-statistic">
  <div class="api-method-name">UnbindChanceToApplyStatistic()</div>
  <p class="api-method-summary">Stops sharing the external application-chance Statistic. Catalyst creates a new internal Statistic starting at the external Statistic&#x27;s current value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-is-chance-to-apply-bound">
  <div class="api-method-name">IsChanceToApplyBound()</div>
  <p class="api-method-summary">Returns whether application chance is using an external Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-get-chance-to-apply-statistic">
  <div class="api-method-name">GetChanceToApplyStatistic()</div>
  <p class="api-method-summary">Returns the active application-chance Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-set-tick-interval">
  <div class="api-method-name">SetTickInterval(interval)</div>
  <p class="api-method-summary">Chooses how much Effect time must pass between ticks. Positive values enable ticking; zero or a negative value disables it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">interval</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Tick interval, or non-positive to disable.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-clear-tick-interval">
  <div class="api-method-name">ClearTickInterval()</div>
  <p class="api-method-summary">Turns ticking off and discards any partial progress toward the next tick.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-get-tick-interval">
  <div class="api-method-name">GetTickInterval()</div>
  <p class="api-method-summary">Returns the positive interval, or a negative value when ticking is disabled.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-set-chance-per-tick">
  <div class="api-method-name">SetChancePerTick(value)</div>
  <p class="api-method-summary">Sets the chance that each completed tick succeeds when the Effect uses its own internal chance Statistic. If an external Statistic is bound, unbind it first.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">value</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">New chance value, where 0 never succeeds and 1 always succeeds. Values below 0 are treated as 0 and values above 1 as 1 when Catalyst checks the chance.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-bind-chance-per-tick-statistic">
  <div class="api-method-name">BindChancePerTickStatistic(statistic)</div>
  <p class="api-method-summary">Makes this Effect use an existing <a href="#catalyst-statistic"><code>CatalystStatistic</code></a> for its per-tick chance. Because the Statistic is shared, changes to it affect later ticks.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">statistic</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
      <span class="api-argument-description">Statistic to bind.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-unbind-chance-per-tick-statistic">
  <div class="api-method-name">UnbindChancePerTickStatistic()</div>
  <p class="api-method-summary">Stops using the external per-tick chance and replaces it with a new internal Statistic at the same current value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-is-chance-per-tick-bound">
  <div class="api-method-name">IsChancePerTickBound()</div>
  <p class="api-method-summary">Returns whether per-tick chance is using an external Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-get-chance-per-tick-statistic">
  <div class="api-method-name">GetChancePerTickStatistic()</div>
  <p class="api-method-summary">Returns the active per-tick chance Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-set-on-apply">
  <div class="api-method-name">SetOnApply(callback)</div>
  <p class="api-method-summary">Sets a callback that runs after the Effect has successfully become active and its Modifiers and Flows have been attached.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function to run after application. Catalyst calls it with this Effect as self.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-clear-on-apply">
  <div class="api-method-name">ClearOnApply()</div>
  <p class="api-method-summary">Clears the application callback.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-set-resolve-tick">
  <div class="api-method-name">SetResolveTick(callback)</div>
  <p class="api-method-summary">Sets a callback that runs after the normal tick chance is checked but before owned Flows move Resources. Use the <a href="#catalyst-effect-tick-result"><code>CatalystEffectTickResult</code></a> to cancel the tick or change its movement multiplier.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function called as fn(tick_duration, result) with this Effect as self.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-clear-resolve-tick">
  <div class="api-method-name">ClearResolveTick()</div>
  <p class="api-method-summary">Removes the ResolveTick callback, so Catalyst uses the normal tick result and movement multiplier without a custom adjustment.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-set-on-tick">
  <div class="api-method-name">SetOnTick(callback)</div>
  <p class="api-method-summary">Sets a callback that runs after every completed tick, after any Flow movement. It runs whether the tick succeeded or failed its chance check.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function called as fn(tick_duration, result) with this Effect as self.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-clear-on-tick">
  <div class="api-method-name">ClearOnTick()</div>
  <p class="api-method-summary">Clears the post-movement tick callback.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-set-on-remove">
  <div class="api-method-name">SetOnRemove(callback)</div>
  <p class="api-method-summary">Sets a callback that runs when an active Effect is removed. Its Modifiers and Flows have already been removed. During the callback, effect.manager and effect.owner still point to the EffectManager and owner it was removed from.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function called as fn(reason) with this Effect as self. reason is the value supplied when the Effect was removed.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-clear-on-remove">
  <div class="api-method-name">ClearOnRemove()</div>
  <p class="api-method-summary">Clears the removal callback.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-add-flow">
  <div class="api-method-name">AddFlow(resource, flow)</div>
  <p class="api-method-summary">Adds a detached ResourceFlow to this Effect. The Flow is not attached to the Resource yet; it is attached only if the Effect successfully applies, and the Effect owns it afterward.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">resource</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
      <span class="api-argument-description">Resource this Flow should change while the Effect is active.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">flow</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
      <span class="api-argument-description">Detached Flow to add. Do not attach it separately; this Effect will manage its lifetime.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-remove-flow">
  <div class="api-method-name">RemoveFlow(flow)</div>
  <p class="api-method-summary">Removes and destroys one exact Flow owned by this Effect.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flow</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
      <span class="api-argument-description">Owned flow to remove.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-add-modifier">
  <div class="api-method-name">AddModifier(statistic, modifier)</div>
  <p class="api-method-summary">Adds a detached Modifier to this Effect. The Modifier is not attached to the Statistic yet; it is attached only if the Effect successfully applies, and the Effect owns it afterward.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">statistic</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
      <span class="api-argument-description">Statistic this Modifier should affect while the Effect is active.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Detached Modifier to add. Do not attach it separately; this Effect will manage its lifetime.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-remove-modifier">
  <div class="api-method-name">RemoveModifier(modifier)</div>
  <p class="api-method-summary">Removes and destroys one exact Modifier owned by this Effect.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Owned modifier to remove.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-add-tag">
  <div class="api-method-name">AddTag(tag)</div>
  <p class="api-method-summary">Adds a tag if absent.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tag</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Tag to add.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-remove-tag">
  <div class="api-method-name">RemoveTag(tag)</div>
  <p class="api-method-summary">Removes every matching tag.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tag</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Tag to remove.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-has-tag">
  <div class="api-method-name">HasTag(tag)</div>
  <p class="api-method-summary">Returns whether this Effect contains a tag.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tag</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Tag to query.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-clear-tags">
  <div class="api-method-name">ClearTags()</div>
  <p class="api-method-summary">Removes every tag.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-destroy">
  <div class="api-method-name">Destroy([reason])</div>
  <p class="api-method-summary">Destroys this Effect. If it is active, its EffectManager removes it normally so callbacks and owned Modifiers/Flows are cleaned up. If it has not been applied, its stored Modifiers and Flows are destroyed directly.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">reason <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional value describing why the Effect was removed. Catalyst passes it to OnRemove callbacks but otherwise leaves it untouched.</span>
    </div>
  </div>
</div>

### CatalystEffectManager
{: #catalyst-effect-manager .api-type-title }

Creates an EffectManager for one owner. The owner can be a GameMaker instance, a struct, or any other value your game uses to represent the thing receiving Effects. The manager applies, removes, searches, and updates that owner&#x27;s active Effects.

```gml
new CatalystEffectManager(owner)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">owner</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Value that these Effects belong to, such as a player instance, enemy instance, or gameplay struct.</span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Identity and owner</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-effect-manager-set-identity"><code>SetIdentity()</code></a></td><td>Sets this EffectManager&#x27;s ID so a <a href="#catalyst-set"><code>CatalystSet</code></a> and your own code can find it later.</td></tr>
<tr><td><a href="#catalyst-effect-manager-get-identity"><code>GetIdentity()</code></a></td><td>Returns the manager ID.</td></tr>
<tr><td><a href="#catalyst-effect-manager-set-name"><code>SetName()</code></a></td><td>Sets the manager name.</td></tr>
<tr><td><a href="#catalyst-effect-manager-get-name"><code>GetName()</code></a></td><td>Returns the manager name.</td></tr>
<tr><td><a href="#catalyst-effect-manager-get-owner"><code>GetOwner()</code></a></td><td>Returns the owner value that was given to this EffectManager when it was created.</td></tr>
</tbody></table>

<div class="api-method-group-title">Randomness and observation</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-effect-manager-set-random-function"><code>SetRandomFunction()</code></a></td><td>Replaces the random-number function used for Effect application and per-tick chance checks. This is useful when your game needs seeded or otherwise controlled randomness.</td></tr>
<tr><td><a href="#catalyst-effect-manager-clear-random-function"><code>ClearRandomFunction()</code></a></td><td>Restores GameMaker random(1) as the manager&#x27;s random source.</td></tr>
<tr><td><a href="#catalyst-effect-manager-on-effect-applied"><code>OnEffectApplied()</code></a></td><td>Adds a callback that runs whenever an Effect successfully becomes active. Catalyst calls it as fn(manager, effect, application_result). Keep the returned subscription if you may want to stop listening later.</td></tr>
<tr><td><a href="#catalyst-effect-manager-on-effect-removed"><code>OnEffectRemoved()</code></a></td><td>Adds a callback that runs whenever an active Effect is removed. Catalyst calls it as fn(manager, effect, reason), where reason is the value supplied by the removal call.</td></tr>
</tbody></table>

<div class="api-method-group-title">Effect management</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-effect-manager-add-effect"><code>AddEffect()</code></a></td><td>Tries to make a detached Effect active on this manager. Catalyst checks its application chance and same-ID reapplication policy, then attaches its Modifiers and Flows and starts its timer if the Effect applies.</td></tr>
<tr><td><a href="#catalyst-effect-manager-remove-effect"><code>RemoveEffect()</code></a></td><td>Removes one active Effect from this manager. Its owned Modifiers and Flows are removed and destroyed and its removal callbacks run. If the manager is currently applying/removing another Effect, this exact request is saved until that operation finishes.</td></tr>
<tr><td><a href="#catalyst-effect-manager-has-effect"><code>HasEffect()</code></a></td><td>Returns whether this exact Effect is currently active on the manager.</td></tr>
<tr><td><a href="#catalyst-effect-manager-get-effects"><code>GetEffects()</code></a></td><td>Returns the currently active Effects in the order they were applied.</td></tr>
</tbody></table>

<div class="api-method-group-title">Lookup and removal</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-effect-manager-get-effects-by-identity"><code>GetEffectsByIdentity()</code></a></td><td>Returns active Effects with the given ID.</td></tr>
<tr><td><a href="#catalyst-effect-manager-has-effect-identity"><code>HasEffectIdentity()</code></a></td><td>Returns whether any active Effect has the given ID.</td></tr>
<tr><td><a href="#catalyst-effect-manager-remove-effects-by-identity"><code>RemoveEffectsByIdentity()</code></a></td><td>Removes every active Effect with the given ID.</td></tr>
<tr><td><a href="#catalyst-effect-manager-get-effects-by-family"><code>GetEffectsByFamily()</code></a></td><td>Returns active Effects whose family ID exactly matches the value you provide.</td></tr>
<tr><td><a href="#catalyst-effect-manager-has-tag"><code>HasTag()</code></a></td><td>Returns whether any active Effect provides a tag.</td></tr>
<tr><td><a href="#catalyst-effect-manager-get-effects-tagged"><code>GetEffectsTagged()</code></a></td><td>Returns active Effects providing one tag.</td></tr>
<tr><td><a href="#catalyst-effect-manager-remove-effects-tagged"><code>RemoveEffectsTagged()</code></a></td><td>Removes every active Effect providing one tag.</td></tr>
</tbody></table>

<div class="api-method-group-title">Lifecycle</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-effect-manager-destroy"><code>Destroy()</code></a></td><td>Destroys the EffectManager after removing all active Effects and stopping its event subscriptions. If Destroy() is called while the manager is already applying or removing an Effect, cleanup completes as soon as that current operation finishes.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-effect-manager-set-identity">
  <div class="api-method-name">SetIdentity(identity)</div>
  <p class="api-method-summary">Sets this EffectManager&#x27;s ID so a <a href="#catalyst-set"><code>CatalystSet</code></a> and your own code can find it later.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real,Undefined</span>
      <span class="api-argument-description">Non-empty string or finite number used as an ID to assign, or undefined to clear.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect-manager">CatalystEffectManager</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-get-identity">
  <div class="api-method-name">GetIdentity()</div>
  <p class="api-method-summary">Returns the manager ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-set-name">
  <div class="api-method-name">SetName(name)</div>
  <p class="api-method-summary">Sets the manager name.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">New name.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect-manager">CatalystEffectManager</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-get-name">
  <div class="api-method-name">GetName()</div>
  <p class="api-method-summary">Returns the manager name.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-get-owner">
  <div class="api-method-name">GetOwner()</div>
  <p class="api-method-summary">Returns the owner value that was given to this EffectManager when it was created.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-set-random-function">
  <div class="api-method-name">SetRandomFunction(fn)</div>
  <p class="api-method-summary">Replaces the random-number function used for Effect application and per-tick chance checks. This is useful when your game needs seeded or otherwise controlled randomness.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function called with no arguments. Return a number on the same 0-to-1 scale as your Effect chance values.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect-manager">CatalystEffectManager</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-clear-random-function">
  <div class="api-method-name">ClearRandomFunction()</div>
  <p class="api-method-summary">Restores GameMaker random(1) as the manager&#x27;s random source.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect-manager">CatalystEffectManager</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-on-effect-applied">
  <div class="api-method-name">OnEffectApplied(callback)</div>
  <p class="api-method-summary">Adds a callback that runs whenever an Effect successfully becomes active. Catalyst calls it as fn(manager, effect, application_result). Keep the returned subscription if you may want to stop listening later.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function called as fn(manager, effect, application_result).</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-subscription">CatalystSubscription</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-on-effect-removed">
  <div class="api-method-name">OnEffectRemoved(callback)</div>
  <p class="api-method-summary">Adds a callback that runs whenever an active Effect is removed. Catalyst calls it as fn(manager, effect, reason), where reason is the value supplied by the removal call.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function called as fn(manager, effect, reason).</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-subscription">CatalystSubscription</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-add-effect">
  <div class="api-method-name">AddEffect(effect, [query])</div>
  <p class="api-method-summary">Tries to make a detached Effect active on this manager. Catalyst checks its application chance and same-ID reapplication policy, then attaches its Modifiers and Flows and starts its timer if the Effect applies.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">effect</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
      <span class="api-argument-description">Detached Effect to apply. It must not already belong to an EffectManager.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">query <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.OracleFactQuery,Struct</span>
      <span class="api-argument-description">Optional Oracle Fact query used only while calculating this Effect&#x27;s application chance.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect-application-result">CatalystEffectApplicationResult</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#catalyst-effect"><code>CatalystEffect</code></a> <span aria-hidden="true">·</span> <a href="#catalyst-effect-application-result"><code>CatalystEffectApplicationResult</code></a> <span aria-hidden="true">·</span> <a href="{{ '/catalyst/effects' | relative_url }}">Effects</a></div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-remove-effect">
  <div class="api-method-name">RemoveEffect(effect, [reason])</div>
  <p class="api-method-summary">Removes one active Effect from this manager. Its owned Modifiers and Flows are removed and destroyed and its removal callbacks run. If the manager is currently applying/removing another Effect, this exact request is saved until that operation finishes.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">effect</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
      <span class="api-argument-description">Active Effect to remove.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">reason <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional value describing why the Effect is being removed. Catalyst passes it to removal callbacks but otherwise leaves it untouched.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-has-effect">
  <div class="api-method-name">HasEffect(effect)</div>
  <p class="api-method-summary">Returns whether this exact Effect is currently active on the manager.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">effect</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
      <span class="api-argument-description">Effect to check.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-get-effects">
  <div class="api-method-name">GetEffects()</div>
  <p class="api-method-summary">Returns the currently active Effects in the order they were applied.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-effect">CatalystEffect</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-get-effects-by-identity">
  <div class="api-method-name">GetEffectsByIdentity(identity)</div>
  <p class="api-method-summary">Returns active Effects with the given ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">ID to match.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-effect">CatalystEffect</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-has-effect-identity">
  <div class="api-method-name">HasEffectIdentity(identity)</div>
  <p class="api-method-summary">Returns whether any active Effect has the given ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">ID to match.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-remove-effects-by-identity">
  <div class="api-method-name">RemoveEffectsByIdentity(identity, [reason])</div>
  <p class="api-method-summary">Removes every active Effect with the given ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">ID to match.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">reason <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Removal reason.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-get-effects-by-family">
  <div class="api-method-name">GetEffectsByFamily(family)</div>
  <p class="api-method-summary">Returns active Effects whose family ID exactly matches the value you provide.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">family</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">Effect family ID to match.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-effect">CatalystEffect</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-has-tag">
  <div class="api-method-name">HasTag(tag)</div>
  <p class="api-method-summary">Returns whether any active Effect provides a tag.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tag</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Tag to query.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-get-effects-tagged">
  <div class="api-method-name">GetEffectsTagged(tag)</div>
  <p class="api-method-summary">Returns active Effects providing one tag.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tag</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Tag to query.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-effect">CatalystEffect</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-remove-effects-tagged">
  <div class="api-method-name">RemoveEffectsTagged(tag, [reason])</div>
  <p class="api-method-summary">Removes every active Effect providing one tag.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tag</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Tag to match.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">reason <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Removal reason.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-manager-destroy">
  <div class="api-method-name">Destroy()</div>
  <p class="api-method-summary">Destroys the EffectManager after removing all active Effects and stopping its event subscriptions. If Destroy() is called while the manager is already applying or removing an Effect, cleanup completes as soon as that current operation finishes.</p>
</div>

### CatalystEffectTickResult
{: #catalyst-effect-tick-result .api-type-title }

Stores everything Catalyst decided for one completed Effect tick. ResolveTick can use this result to cancel the tick or change the multiplier before owned ResourceFlows move Resources.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-effect-tick-result-succeeded"><code>Succeeded()</code></a></td><td>Returns whether this tick will currently succeed. ResolveTick can change this value with SetSucceeded().</td></tr>
<tr><td><a href="#catalyst-effect-tick-result-set-succeeded"><code>SetSucceeded()</code></a></td><td>Changes whether this tick succeeds. Call this from ResolveTick when your own rules should override the normal chance result.</td></tr>
<tr><td><a href="#catalyst-effect-tick-result-get-multiplier"><code>GetMultiplier()</code></a></td><td>Returns the multiplier that will be applied to Resource movement from this Effect&#x27;s owned Flows when the tick succeeds.</td></tr>
<tr><td><a href="#catalyst-effect-tick-result-set-multiplier"><code>SetMultiplier()</code></a></td><td>Changes how much this Effect&#x27;s owned Flows move Resources for this tick. For example, 0.5 gives half movement and 2 gives double movement.</td></tr>
<tr><td><a href="#catalyst-effect-tick-result-get-effect"><code>GetEffect()</code></a></td><td>Returns the Effect this tick belongs to.</td></tr>
<tr><td><a href="#catalyst-effect-tick-result-get-tick-duration"><code>GetTickDuration()</code></a></td><td>Returns the completed interval duration.</td></tr>
<tr><td><a href="#catalyst-effect-tick-result-get-chance"><code>GetChance()</code></a></td><td>Returns the evaluated per-tick chance.</td></tr>
<tr><td><a href="#catalyst-effect-tick-result-get-roll"><code>GetRoll()</code></a></td><td>Returns the random number Catalyst used for the normal per-tick chance check, or undefined when the chance did not require a random roll.</td></tr>
<tr><td><a href="#catalyst-effect-tick-result-chance-succeeded"><code>ChanceSucceeded()</code></a></td><td>Returns the chance result from before ResolveTick changed anything.</td></tr>
<tr><td><a href="#catalyst-effect-tick-result-get-flow-results"><code>GetFlowResults()</code></a></td><td>Returns a new array containing concrete flow movement results produced by this tick.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-effect-tick-result-succeeded">
  <div class="api-method-name">Succeeded()</div>
  <p class="api-method-summary">Returns whether this tick will currently succeed. ResolveTick can change this value with SetSucceeded().</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-tick-result-set-succeeded">
  <div class="api-method-name">SetSucceeded(success)</div>
  <p class="api-method-summary">Changes whether this tick succeeds. Call this from ResolveTick when your own rules should override the normal chance result.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">success</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">New success state.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect-tick-result">CatalystEffectTickResult</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-tick-result-get-multiplier">
  <div class="api-method-name">GetMultiplier()</div>
  <p class="api-method-summary">Returns the multiplier that will be applied to Resource movement from this Effect&#x27;s owned Flows when the tick succeeds.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-tick-result-set-multiplier">
  <div class="api-method-name">SetMultiplier(multiplier)</div>
  <p class="api-method-summary">Changes how much this Effect&#x27;s owned Flows move Resources for this tick. For example, 0.5 gives half movement and 2 gives double movement.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">multiplier</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">New multiplier.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect-tick-result">CatalystEffectTickResult</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-tick-result-get-effect">
  <div class="api-method-name">GetEffect()</div>
  <p class="api-method-summary">Returns the Effect this tick belongs to.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-tick-result-get-tick-duration">
  <div class="api-method-name">GetTickDuration()</div>
  <p class="api-method-summary">Returns the completed interval duration.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-tick-result-get-chance">
  <div class="api-method-name">GetChance()</div>
  <p class="api-method-summary">Returns the evaluated per-tick chance.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-tick-result-get-roll">
  <div class="api-method-name">GetRoll()</div>
  <p class="api-method-summary">Returns the random number Catalyst used for the normal per-tick chance check, or undefined when the chance did not require a random roll.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-tick-result-chance-succeeded">
  <div class="api-method-name">ChanceSucceeded()</div>
  <p class="api-method-summary">Returns the chance result from before ResolveTick changed anything.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-tick-result-get-flow-results">
  <div class="api-method-name">GetFlowResults()</div>
  <p class="api-method-summary">Returns a new array containing concrete flow movement results produced by this tick.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-resource-flow-result">CatalystResourceFlowResult</a>&gt;</span>
    </div>
  </div>
</div>

### CatalystEffectApplicationResult
{: #catalyst-effect-application-result .api-type-title }

Describes the result of EffectManager.AddEffect(), including whether the Effect became active, whether the request was queued, what reapplication rule ran, and any chance roll that was used.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-effect-application-result-succeeded"><code>Succeeded()</code></a></td><td>Returns true when AddEffect() handled the request successfully. This includes cases where the incoming Effect did not become active because the current Effect was ignored, refreshed, or extended instead.</td></tr>
<tr><td><a href="#catalyst-effect-application-result-applied"><code>Applied()</code></a></td><td>Returns whether the exact Effect passed to AddEffect() became active.</td></tr>
<tr><td><a href="#catalyst-effect-application-result-queued"><code>Queued()</code></a></td><td>Returns true when the manager was already changing its active Effects and saved this request to process immediately afterward.</td></tr>
<tr><td><a href="#catalyst-effect-application-result-get-outcome"><code>GetOutcome()</code></a></td><td>Returns the specific <a href="#enum-e-cat-effect-application-outcome"><code>eCatEffectApplicationOutcome</code></a> explaining what AddEffect() did.</td></tr>
<tr><td><a href="#catalyst-effect-application-result-get-incoming-effect"><code>GetIncomingEffect()</code></a></td><td>Returns the Effect supplied by the caller.</td></tr>
<tr><td><a href="#catalyst-effect-application-result-get-effect"><code>GetEffect()</code></a></td><td>Returns the active Effect produced or affected by this request.</td></tr>
<tr><td><a href="#catalyst-effect-application-result-get-chance"><code>GetChance()</code></a></td><td>Returns the evaluated application chance when chance resolution was reached.</td></tr>
<tr><td><a href="#catalyst-effect-application-result-get-roll"><code>GetRoll()</code></a></td><td>Returns the random roll when a non-guaranteed chance required one.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-effect-application-result-succeeded">
  <div class="api-method-name">Succeeded()</div>
  <p class="api-method-summary">Returns true when AddEffect() handled the request successfully. This includes cases where the incoming Effect did not become active because the current Effect was ignored, refreshed, or extended instead.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-application-result-applied">
  <div class="api-method-name">Applied()</div>
  <p class="api-method-summary">Returns whether the exact Effect passed to AddEffect() became active.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-application-result-queued">
  <div class="api-method-name">Queued()</div>
  <p class="api-method-summary">Returns true when the manager was already changing its active Effects and saved this request to process immediately afterward.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-application-result-get-outcome">
  <div class="api-method-name">GetOutcome()</div>
  <p class="api-method-summary">Returns the specific <a href="#enum-e-cat-effect-application-outcome"><code>eCatEffectApplicationOutcome</code></a> explaining what AddEffect() did.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-application-result-get-incoming-effect">
  <div class="api-method-name">GetIncomingEffect()</div>
  <p class="api-method-summary">Returns the Effect supplied by the caller.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-application-result-get-effect">
  <div class="api-method-name">GetEffect()</div>
  <p class="api-method-summary">Returns the active Effect produced or affected by this request.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect">CatalystEffect</a>,Noone</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-application-result-get-chance">
  <div class="api-method-name">GetChance()</div>
  <p class="api-method-summary">Returns the evaluated application chance when chance resolution was reached.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-effect-application-result-get-roll">
  <div class="api-method-name">GetRoll()</div>
  <p class="api-method-summary">Returns the random roll when a non-guaranteed chance required one.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real,Undefined</span>
    </div>
  </div>
</div>

## Sets and previews

### CatalystSet
{: #catalyst-set .api-type-title }

Creates a <a href="#catalyst-set"><code>CatalystSet</code></a>: a container that lets related Statistics, Resources, and EffectManagers share a FactView/layer order and lets ModifierSets target Statistics by ID. Adding something to a Set does not transfer ownership; destroying the Set leaves those Catalyst values alive. A Statistic, Resource, or EffectManager can be a direct member of only one Set at a time.

```gml
new CatalystSet(identity)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">Optional Set ID, used by save/restore and available for your own lookup.</span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Identity and metadata</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-set-set-identity"><code>SetIdentity()</code></a></td><td>Sets this Set&#x27;s ID. Save/restore uses it to make sure captured state is being loaded into the intended Set.</td></tr>
<tr><td><a href="#catalyst-set-get-identity"><code>GetIdentity()</code></a></td><td>Returns the Set ID.</td></tr>
<tr><td><a href="#catalyst-set-set-name"><code>SetName()</code></a></td><td>Sets the Set name.</td></tr>
<tr><td><a href="#catalyst-set-get-name"><code>GetName()</code></a></td><td>Returns the Set name.</td></tr>
<tr><td><a href="#catalyst-set-set-meta"><code>SetMeta()</code></a></td><td>Stores any extra project data you want to keep with this value. Catalyst does not interpret or change it.</td></tr>
<tr><td><a href="#catalyst-set-get-meta"><code>GetMeta()</code></a></td><td>Returns the extra project data previously stored with SetMeta().</td></tr>
</tbody></table>

<div class="api-method-group-title">Saving and loading</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-set-capture-state"><code>CaptureState()</code></a></td><td>Collects the Catalyst data in this Set into a save-friendly struct. Call Succeeded() on the result before using GetState(); functions and other runtime-only values may require repair when the state is restored.</td></tr>
<tr><td><a href="#catalyst-set-restore-state"><code>RestoreState()</code></a></td><td>Prepares previously captured state to load into this already-created Set. RestoreState() does not immediately change gameplay data. First supply any callbacks or custom countdown trackers the save file could not contain with Repair(), then call Complete() to apply the state.</td></tr>
</tbody></table>

<div class="api-method-group-title">Statistics</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-set-add-statistic"><code>AddStatistic()</code></a></td><td>Adds a Statistic directly to this Set. The Statistic must have an ID so Catalyst can match incoming Modifiers to it, and it cannot already belong directly to another <a href="#catalyst-set"><code>CatalystSet</code></a>.</td></tr>
<tr><td><a href="#catalyst-set-remove-statistic"><code>RemoveStatistic()</code></a></td><td>Removes a Statistic from this Set without destroying it or its Modifiers.</td></tr>
<tr><td><a href="#catalyst-set-has-statistic"><code>HasStatistic()</code></a></td><td>Returns whether this Set directly contains a Statistic with the given ID.</td></tr>
<tr><td><a href="#catalyst-set-get-statistic"><code>GetStatistic()</code></a></td><td>Returns the directly added Statistic with the given ID.</td></tr>
<tr><td><a href="#catalyst-set-get-statistics"><code>GetStatistics()</code></a></td><td>Returns a new array containing direct Statistic members.</td></tr>
</tbody></table>

<div class="api-method-group-title">Resources</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-set-add-resource"><code>AddResource()</code></a></td><td>Adds a Resource as a direct member of this Set. The Resource must have an ID and cannot already be a direct member of another <a href="#catalyst-set"><code>CatalystSet</code></a>. The Set also passes its FactView/layer settings into Catalyst-owned Statistics inside the Resource.</td></tr>
<tr><td><a href="#catalyst-set-remove-resource"><code>RemoveResource()</code></a></td><td>Removes a Resource from this Set without destroying it or its Flows.</td></tr>
<tr><td><a href="#catalyst-set-has-resource"><code>HasResource()</code></a></td><td>Returns whether this Set directly contains a Resource with the given ID.</td></tr>
<tr><td><a href="#catalyst-set-get-resource"><code>GetResource()</code></a></td><td>Returns the directly added Resource with the given ID.</td></tr>
<tr><td><a href="#catalyst-set-get-resources"><code>GetResources()</code></a></td><td>Returns a new array containing direct Resource members.</td></tr>
</tbody></table>

<div class="api-method-group-title">Effect managers</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-set-add-effect-manager"><code>AddEffectManager()</code></a></td><td>Adds an EffectManager as a direct member of this Set. It must have an ID and cannot already be a direct member of another Set. Effects applied through this manager later receive the Set&#x27;s FactView and layer settings for their Catalyst-owned Statistics.</td></tr>
<tr><td><a href="#catalyst-set-remove-effect-manager"><code>RemoveEffectManager()</code></a></td><td>Removes an EffectManager from this Set without destroying it or its active Effects.</td></tr>
<tr><td><a href="#catalyst-set-has-effect-manager"><code>HasEffectManager()</code></a></td><td>Returns whether this Set directly contains an EffectManager with the given ID.</td></tr>
<tr><td><a href="#catalyst-set-get-effect-manager"><code>GetEffectManager()</code></a></td><td>Returns the directly added EffectManager with the given ID.</td></tr>
<tr><td><a href="#catalyst-set-get-effect-managers"><code>GetEffectManagers()</code></a></td><td>Returns a new array containing direct Effect Manager members.</td></tr>
</tbody></table>

<div class="api-method-group-title">Facts and layers</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-set-set-fact-view"><code>SetFactView()</code></a></td><td>Sets the OracleFactView that managed Statistics should read from. The Set applies it to direct Statistics and to Catalyst-owned Statistics inside Resources, Flows, and Effects.</td></tr>
<tr><td><a href="#catalyst-set-clear-fact-view"><code>ClearFactView()</code></a></td><td>Clears the Set FactView and removes it from the Statistics currently managed by this Set.</td></tr>
<tr><td><a href="#catalyst-set-get-fact-view"><code>GetFactView()</code></a></td><td>Returns the stored Fact View.</td></tr>
<tr><td><a href="#catalyst-set-set-layer-order"><code>SetLayerOrder()</code></a></td><td>Sets the Statistic layer order this Set should apply across its managed Catalyst values. Direct Statistics and Catalyst-owned Statistics inside Resources, Flows, and Effects receive the same order.</td></tr>
<tr><td><a href="#catalyst-set-clear-layer-order"><code>ClearLayerOrder()</code></a></td><td>Stops the Set from applying its layer order to future Statistics. Existing Statistics keep the order they already received.</td></tr>
<tr><td><a href="#catalyst-set-get-layer-order"><code>GetLayerOrder()</code></a></td><td>Returns the layer order stored by this Set, or undefined when none is set.</td></tr>
</tbody></table>

<div class="api-method-group-title">Preview and apply</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-set-preview"><code>Preview()</code></a></td><td>Checks where every Modifier in the incoming ModifierSet would go and calculates the resulting Statistic values without changing the Set.</td></tr>
<tr><td><a href="#catalyst-set-preview-swap"><code>PreviewSwap()</code></a></td><td>Calculates a proposed swap: remove the outgoing ModifierSet&#x27;s attached Modifiers and add the incoming ModifierSet&#x27;s Modifiers, without actually changing any Statistic.</td></tr>
<tr><td><a href="#catalyst-set-apply"><code>Apply()</code></a></td><td>Attaches every Modifier in the incoming ModifierSet to the Statistic matching its target ID. The operation is all-or-nothing: if any Modifier cannot be applied, none of them are attached.</td></tr>
<tr><td><a href="#catalyst-set-apply-swap"><code>ApplySwap()</code></a></td><td>Removes the outgoing ModifierSet&#x27;s attached Modifiers and attaches the incoming ModifierSet&#x27;s Modifiers by target ID. The whole swap is all-or-nothing: if any part fails validation, nothing changes.</td></tr>
</tbody></table>

<div class="api-method-group-title">Refresh and inspection</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-set-refresh"><code>Refresh()</code></a></td><td>Recalculates every Statistic managed by this Set, including Catalyst-owned Statistics inside Resources, Flows, and active Effects. It then refreshes Resources so changed minimum/maximum values are applied.</td></tr>
<tr><td><a href="#catalyst-set-get-details"><code>GetDetails()</code></a></td><td>Returns data intended for debug/inspection tools: Explain() details for managed Statistics plus the Set&#x27;s direct Resources and EffectManagers.</td></tr>
</tbody></table>

<div class="api-method-group-title">Lifecycle</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-set-destroy"><code>Destroy()</code></a></td><td>Destroys the Set container and removes its membership/configuration links. The Statistics, Resources, EffectManagers, Modifiers, Effects, and Flows themselves stay alive.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-set-set-identity">
  <div class="api-method-name">SetIdentity(identity)</div>
  <p class="api-method-summary">Sets this Set&#x27;s ID. Save/restore uses it to make sure captured state is being loaded into the intended Set.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real,Undefined</span>
      <span class="api-argument-description">Non-empty string or finite number used as an ID, or undefined to clear.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-set">CatalystSet</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-get-identity">
  <div class="api-method-name">GetIdentity()</div>
  <p class="api-method-summary">Returns the Set ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-set-name">
  <div class="api-method-name">SetName(name)</div>
  <p class="api-method-summary">Sets the Set name.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Name value.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-set">CatalystSet</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-get-name">
  <div class="api-method-name">GetName()</div>
  <p class="api-method-summary">Returns the Set name.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-set-meta">
  <div class="api-method-name">SetMeta(meta)</div>
  <p class="api-method-summary">Stores any extra project data you want to keep with this value. Catalyst does not interpret or change it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">meta</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Any extra project data you want to store here.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-set">CatalystSet</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-get-meta">
  <div class="api-method-name">GetMeta()</div>
  <p class="api-method-summary">Returns the extra project data previously stored with SetMeta().</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-capture-state">
  <div class="api-method-name">CaptureState()</div>
  <p class="api-method-summary">Collects the Catalyst data in this Set into a save-friendly struct. Call Succeeded() on the result before using GetState(); functions and other runtime-only values may require repair when the state is restored.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-state-capture-result">CatalystStateCaptureResult</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#catalyst-state-capture-result"><code>CatalystStateCaptureResult</code></a> <span aria-hidden="true">·</span> <a href="#catalyst-set-restore-state"><code>CatalystSet.RestoreState</code></a> <span aria-hidden="true">·</span> <a href="{{ '/catalyst/saving-and-loading' | relative_url }}">Saving &amp; Loading</a></div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-restore-state">
  <div class="api-method-name">RestoreState(state)</div>
  <p class="api-method-summary">Prepares previously captured state to load into this already-created Set. RestoreState() does not immediately change gameplay data. First supply any callbacks or custom countdown trackers the save file could not contain with Repair(), then call Complete() to apply the state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">state</span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">Struct returned by <a href="#catalyst-state-capture-result-get-state"><code>CatalystStateCaptureResult.GetState()</code></a>. It may have been saved with json_stringify() and loaded again with json_parse().</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-state-restore-result">CatalystStateRestoreResult</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#catalyst-state-restore-result"><code>CatalystStateRestoreResult</code></a> <span aria-hidden="true">·</span> <a href="#catalyst-repair"><code>CatalystRepair</code></a> <span aria-hidden="true">·</span> <a href="#catalyst-set-capture-state"><code>CatalystSet.CaptureState</code></a> <span aria-hidden="true">·</span> <a href="{{ '/catalyst/saving-and-loading' | relative_url }}">Saving &amp; Loading</a></div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-add-statistic">
  <div class="api-method-name">AddStatistic(statistic)</div>
  <p class="api-method-summary">Adds a Statistic directly to this Set. The Statistic must have an ID so Catalyst can match incoming Modifiers to it, and it cannot already belong directly to another <a href="#catalyst-set"><code>CatalystSet</code></a>.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">statistic</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
      <span class="api-argument-description">Statistic reference to add.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-set">CatalystSet</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-remove-statistic">
  <div class="api-method-name">RemoveStatistic(statistic)</div>
  <p class="api-method-summary">Removes a Statistic from this Set without destroying it or its Modifiers.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">statistic</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
      <span class="api-argument-description">Statistic reference to remove.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-has-statistic">
  <div class="api-method-name">HasStatistic(identity)</div>
  <p class="api-method-summary">Returns whether this Set directly contains a Statistic with the given ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">Statistic ID.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-get-statistic">
  <div class="api-method-name">GetStatistic(identity)</div>
  <p class="api-method-summary">Returns the directly added Statistic with the given ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">Statistic ID.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-get-statistics">
  <div class="api-method-name">GetStatistics()</div>
  <p class="api-method-summary">Returns a new array containing direct Statistic members.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-statistic">CatalystStatistic</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-add-resource">
  <div class="api-method-name">AddResource(resource)</div>
  <p class="api-method-summary">Adds a Resource as a direct member of this Set. The Resource must have an ID and cannot already be a direct member of another <a href="#catalyst-set"><code>CatalystSet</code></a>. The Set also passes its FactView/layer settings into Catalyst-owned Statistics inside the Resource.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">resource</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
      <span class="api-argument-description">Resource reference to add.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-set">CatalystSet</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-remove-resource">
  <div class="api-method-name">RemoveResource(resource)</div>
  <p class="api-method-summary">Removes a Resource from this Set without destroying it or its Flows.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">resource</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
      <span class="api-argument-description">Resource reference to remove.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-has-resource">
  <div class="api-method-name">HasResource(identity)</div>
  <p class="api-method-summary">Returns whether this Set directly contains a Resource with the given ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">Resource ID.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-get-resource">
  <div class="api-method-name">GetResource(identity)</div>
  <p class="api-method-summary">Returns the directly added Resource with the given ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">Resource ID.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource">CatalystResource</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-get-resources">
  <div class="api-method-name">GetResources()</div>
  <p class="api-method-summary">Returns a new array containing direct Resource members.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-resource">CatalystResource</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-add-effect-manager">
  <div class="api-method-name">AddEffectManager(manager)</div>
  <p class="api-method-summary">Adds an EffectManager as a direct member of this Set. It must have an ID and cannot already be a direct member of another Set. Effects applied through this manager later receive the Set&#x27;s FactView and layer settings for their Catalyst-owned Statistics.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">manager</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-effect-manager">CatalystEffectManager</a></span>
      <span class="api-argument-description">Effect Manager reference to add.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-set">CatalystSet</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-remove-effect-manager">
  <div class="api-method-name">RemoveEffectManager(manager)</div>
  <p class="api-method-summary">Removes an EffectManager from this Set without destroying it or its active Effects.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">manager</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-effect-manager">CatalystEffectManager</a></span>
      <span class="api-argument-description">Manager reference to remove.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-has-effect-manager">
  <div class="api-method-name">HasEffectManager(identity)</div>
  <p class="api-method-summary">Returns whether this Set directly contains an EffectManager with the given ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">EffectManager ID.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-get-effect-manager">
  <div class="api-method-name">GetEffectManager(identity)</div>
  <p class="api-method-summary">Returns the directly added EffectManager with the given ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">EffectManager ID.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-effect-manager">CatalystEffectManager</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-get-effect-managers">
  <div class="api-method-name">GetEffectManagers()</div>
  <p class="api-method-summary">Returns a new array containing direct Effect Manager members.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-effect-manager">CatalystEffectManager</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-set-fact-view">
  <div class="api-method-name">SetFactView(fact_view)</div>
  <p class="api-method-summary">Sets the OracleFactView that managed Statistics should read from. The Set applies it to direct Statistics and to Catalyst-owned Statistics inside Resources, Flows, and Effects.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fact_view</span>
      <span class="api-argument-type">Struct.OracleFactView</span>
      <span class="api-argument-description">Oracle FactView to apply to Statistics managed by this Set.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-set">CatalystSet</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-clear-fact-view">
  <div class="api-method-name">ClearFactView()</div>
  <p class="api-method-summary">Clears the Set FactView and removes it from the Statistics currently managed by this Set.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-set">CatalystSet</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-get-fact-view">
  <div class="api-method-name">GetFactView()</div>
  <p class="api-method-summary">Returns the stored Fact View.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.OracleFactView,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-set-layer-order">
  <div class="api-method-name">SetLayerOrder(layers)</div>
  <p class="api-method-summary">Sets the Statistic layer order this Set should apply across its managed Catalyst values. Direct Statistics and Catalyst-owned Statistics inside Resources, Flows, and Effects receive the same order.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">layers</span>
      <span class="api-argument-type">Array&lt;Any&gt;</span>
      <span class="api-argument-description">Layer IDs in the order Statistics should calculate them. Each ID must be unique; strings and finite numbers are supported.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-set">CatalystSet</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-clear-layer-order">
  <div class="api-method-name">ClearLayerOrder()</div>
  <p class="api-method-summary">Stops the Set from applying its layer order to future Statistics. Existing Statistics keep the order they already received.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-set">CatalystSet</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-get-layer-order">
  <div class="api-method-name">GetLayerOrder()</div>
  <p class="api-method-summary">Returns the layer order stored by this Set, or undefined when none is set.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Any&gt;,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-preview">
  <div class="api-method-name">Preview(incoming, [query])</div>
  <p class="api-method-summary">Checks where every Modifier in the incoming ModifierSet would go and calculates the resulting Statistic values without changing the Set.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">incoming</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier-set">CatalystModifierSet</a></span>
      <span class="api-argument-description">ModifierSet whose Modifiers should be tested as additions.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">query <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.OracleFactQuery,Struct</span>
      <span class="api-argument-description">Optional Oracle Fact query used only while calculating these values.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-set-preview-result">CatalystSetPreviewResult</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#catalyst-set-preview-result"><code>CatalystSetPreviewResult</code></a> <span aria-hidden="true">·</span> <a href="#catalyst-set-apply"><code>CatalystSet.Apply</code></a> <span aria-hidden="true">·</span> <a href="{{ '/catalyst/sets-and-previews' | relative_url }}">Sets &amp; Previews</a></div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-preview-swap">
  <div class="api-method-name">PreviewSwap(outgoing, incoming, [query])</div>
  <p class="api-method-summary">Calculates a proposed swap: remove the outgoing ModifierSet&#x27;s attached Modifiers and add the incoming ModifierSet&#x27;s Modifiers, without actually changing any Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">outgoing</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier-set">CatalystModifierSet</a></span>
      <span class="api-argument-description">ModifierSet whose currently attached Modifiers should be treated as removals.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">incoming</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier-set">CatalystModifierSet</a></span>
      <span class="api-argument-description">ModifierSet whose Modifiers should be tested as additions.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">query <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.OracleFactQuery,Struct</span>
      <span class="api-argument-description">Optional Oracle Fact query used only while calculating these values.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-set-preview-result">CatalystSetPreviewResult</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#catalyst-set-preview-result"><code>CatalystSetPreviewResult</code></a> <span aria-hidden="true">·</span> <a href="#catalyst-set-apply-swap"><code>CatalystSet.ApplySwap</code></a> <span aria-hidden="true">·</span> <a href="{{ '/catalyst/sets-and-previews' | relative_url }}">Sets &amp; Previews</a></div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-apply">
  <div class="api-method-name">Apply(incoming)</div>
  <p class="api-method-summary">Attaches every Modifier in the incoming ModifierSet to the Statistic matching its target ID. The operation is all-or-nothing: if any Modifier cannot be applied, none of them are attached.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">incoming</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier-set">CatalystModifierSet</a></span>
      <span class="api-argument-description">ModifierSet whose Modifiers should be tested as additions.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-set-apply-result">CatalystSetApplyResult</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#catalyst-set-apply-result"><code>CatalystSetApplyResult</code></a> <span aria-hidden="true">·</span> <a href="#catalyst-set-preview"><code>CatalystSet.Preview</code></a></div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-apply-swap">
  <div class="api-method-name">ApplySwap(outgoing, incoming)</div>
  <p class="api-method-summary">Removes the outgoing ModifierSet&#x27;s attached Modifiers and attaches the incoming ModifierSet&#x27;s Modifiers by target ID. The whole swap is all-or-nothing: if any part fails validation, nothing changes.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">outgoing</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier-set">CatalystModifierSet</a></span>
      <span class="api-argument-description">ModifierSet whose currently attached Modifiers should be treated as removals.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">incoming</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier-set">CatalystModifierSet</a></span>
      <span class="api-argument-description">ModifierSet whose Modifiers should be tested as additions.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-set-apply-result">CatalystSetApplyResult</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#catalyst-set-apply-result"><code>CatalystSetApplyResult</code></a> <span aria-hidden="true">·</span> <a href="#catalyst-set-preview-swap"><code>CatalystSet.PreviewSwap</code></a></div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-refresh">
  <div class="api-method-name">Refresh()</div>
  <p class="api-method-summary">Recalculates every Statistic managed by this Set, including Catalyst-owned Statistics inside Resources, Flows, and active Effects. It then refreshes Resources so changed minimum/maximum values are applied.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-set-refresh-result">CatalystSetRefreshResult</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-get-details">
  <div class="api-method-name">GetDetails([query])</div>
  <p class="api-method-summary">Returns data intended for debug/inspection tools: Explain() details for managed Statistics plus the Set&#x27;s direct Resources and EffectManagers.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">query <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Struct.OracleFactQuery,Struct</span>
      <span class="api-argument-description">Optional Oracle Fact query used only while calculating these values.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-set-details">CatalystSetDetails</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-destroy">
  <div class="api-method-name">Destroy()</div>
  <p class="api-method-summary">Destroys the Set container and removes its membership/configuration links. The Statistics, Resources, EffectManagers, Modifiers, Effects, and Flows themselves stay alive.</p>
</div>

### CatalystModifierSet
{: #catalyst-modifier-set .api-type-title }

Creates a reusable group of Modifiers for <a href="#catalyst-set"><code>CatalystSet</code></a> Preview(), Apply(), and swap operations. Each Modifier uses its target ID to choose a Statistic. The ModifierSet only groups references; it does not own, attach, detach, or destroy the Modifiers itself.

```gml
new CatalystModifierSet(identity)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">Optional ID for this ModifierSet, useful for your own lookup or save data.</span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Identity and metadata</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-modifier-set-set-identity"><code>SetIdentity()</code></a></td><td>Sets an optional ID for this ModifierSet so your own code can identify the package.</td></tr>
<tr><td><a href="#catalyst-modifier-set-get-identity"><code>GetIdentity()</code></a></td><td>Returns the package ID.</td></tr>
<tr><td><a href="#catalyst-modifier-set-set-name"><code>SetName()</code></a></td><td>Sets the package name.</td></tr>
<tr><td><a href="#catalyst-modifier-set-get-name"><code>GetName()</code></a></td><td>Returns the package name.</td></tr>
<tr><td><a href="#catalyst-modifier-set-set-meta"><code>SetMeta()</code></a></td><td>Stores any extra project data you want to keep with this value. Catalyst does not interpret or change it.</td></tr>
<tr><td><a href="#catalyst-modifier-set-get-meta"><code>GetMeta()</code></a></td><td>Returns the extra project data previously stored with SetMeta().</td></tr>
</tbody></table>

<div class="api-method-group-title">Modifiers</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-modifier-set-add-modifier"><code>AddModifier()</code></a></td><td>Adds a Modifier reference to this package. This does not attach the Modifier to a Statistic or transfer ownership; it only makes the Modifier part of future Set preview/apply operations.</td></tr>
<tr><td><a href="#catalyst-modifier-set-remove-modifier"><code>RemoveModifier()</code></a></td><td>Removes the Modifier reference from this package only. If the Modifier is attached somewhere, that attachment is unchanged.</td></tr>
<tr><td><a href="#catalyst-modifier-set-has-modifier"><code>HasModifier()</code></a></td><td>Returns whether this exact Modifier reference is currently included in the package.</td></tr>
<tr><td><a href="#catalyst-modifier-set-get-modifiers"><code>GetModifiers()</code></a></td><td>Returns the Modifiers in this package.</td></tr>
</tbody></table>

<div class="api-method-group-title">Lifecycle</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-modifier-set-destroy"><code>Destroy()</code></a></td><td>Clears this ModifierSet. The Modifiers themselves are not destroyed and any existing Statistic attachments stay unchanged.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-modifier-set-set-identity">
  <div class="api-method-name">SetIdentity(identity)</div>
  <p class="api-method-summary">Sets an optional ID for this ModifierSet so your own code can identify the package.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real,Undefined</span>
      <span class="api-argument-description">Non-empty string or finite number used as an ID, or undefined to clear.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier-set">CatalystModifierSet</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-get-identity">
  <div class="api-method-name">GetIdentity()</div>
  <p class="api-method-summary">Returns the package ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-set-name">
  <div class="api-method-name">SetName(name)</div>
  <p class="api-method-summary">Sets the package name.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Name value.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier-set">CatalystModifierSet</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-get-name">
  <div class="api-method-name">GetName()</div>
  <p class="api-method-summary">Returns the package name.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-set-meta">
  <div class="api-method-name">SetMeta(meta)</div>
  <p class="api-method-summary">Stores any extra project data you want to keep with this value. Catalyst does not interpret or change it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">meta</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Any extra project data you want to store here.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier-set">CatalystModifierSet</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-get-meta">
  <div class="api-method-name">GetMeta()</div>
  <p class="api-method-summary">Returns the extra project data previously stored with SetMeta().</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-add-modifier">
  <div class="api-method-name">AddModifier(modifier)</div>
  <p class="api-method-summary">Adds a Modifier reference to this package. This does not attach the Modifier to a Statistic or transfer ownership; it only makes the Modifier part of future Set preview/apply operations.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Modifier to package.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-modifier-set">CatalystModifierSet</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-remove-modifier">
  <div class="api-method-name">RemoveModifier(modifier)</div>
  <p class="api-method-summary">Removes the Modifier reference from this package only. If the Modifier is attached somewhere, that attachment is unchanged.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Modifier reference to remove.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-has-modifier">
  <div class="api-method-name">HasModifier(modifier)</div>
  <p class="api-method-summary">Returns whether this exact Modifier reference is currently included in the package.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Modifier to check.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-get-modifiers">
  <div class="api-method-name">GetModifiers()</div>
  <p class="api-method-summary">Returns the Modifiers in this package.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-modifier">CatalystModifier</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-modifier-set-destroy">
  <div class="api-method-name">Destroy()</div>
  <p class="api-method-summary">Clears this ModifierSet. The Modifiers themselves are not destroyed and any existing Statistic attachments stay unchanged.</p>
</div>

### CatalystSetPreviewResult
{: #catalyst-set-preview-result .api-type-title }

Stores the result of Preview() or PreviewSwap(). It tells you whether all requested Modifiers could be matched to Statistics, gives preview values for affected Statistics, and lists any problems. Nothing has been attached or removed.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-set-preview-result-get-status"><code>GetStatus()</code></a></td><td>Returns the overall preview status.</td></tr>
<tr><td><a href="#catalyst-set-preview-result-succeeded"><code>Succeeded()</code></a></td><td>Returns whether every Modifier in the preview could be matched to a valid target Statistic.</td></tr>
<tr><td><a href="#catalyst-set-preview-result-get-entries"><code>GetEntries()</code></a></td><td>Returns a new array containing preview entries.</td></tr>
<tr><td><a href="#catalyst-set-preview-result-get-diagnostics"><code>GetDiagnostics()</code></a></td><td>Returns the problems Catalyst found while matching Modifiers to target Statistics.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-set-preview-result-get-status">
  <div class="api-method-name">GetStatus()</div>
  <p class="api-method-summary">Returns the overall preview status.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-preview-result-succeeded">
  <div class="api-method-name">Succeeded()</div>
  <p class="api-method-summary">Returns whether every Modifier in the preview could be matched to a valid target Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-preview-result-get-entries">
  <div class="api-method-name">GetEntries()</div>
  <p class="api-method-summary">Returns a new array containing preview entries.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-set-preview-entry">CatalystSetPreviewEntry</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-preview-result-get-diagnostics">
  <div class="api-method-name">GetDiagnostics()</div>
  <p class="api-method-summary">Returns the problems Catalyst found while matching Modifiers to target Statistics.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-route-diagnostic">CatalystRouteDiagnostic</a>&gt;</span>
    </div>
  </div>
</div>

### CatalystSetPreviewEntry
{: #catalyst-set-preview-entry .api-type-title }

Shows how one Statistic would change during <a href="#catalyst-set-preview"><code>CatalystSet.Preview()</code></a> or PreviewSwap(), including its current value, proposed value, and which Modifiers would leave or enter.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-set-preview-entry-get-statistic"><code>GetStatistic()</code></a></td><td>Returns the target Statistic.</td></tr>
<tr><td><a href="#catalyst-set-preview-entry-get-current-value"><code>GetCurrentValue()</code></a></td><td>Returns this Statistic&#x27;s value before the proposed ModifierSet change.</td></tr>
<tr><td><a href="#catalyst-set-preview-entry-get-preview-value"><code>GetPreviewValue()</code></a></td><td>Returns what this Statistic&#x27;s value would be after the proposed ModifierSet change.</td></tr>
<tr><td><a href="#catalyst-set-preview-entry-get-evaluation"><code>GetEvaluation()</code></a></td><td>Returns Explain-style details showing exactly how Catalyst calculated this Statistic&#x27;s preview value.</td></tr>
<tr><td><a href="#catalyst-set-preview-entry-get-outgoing-modifiers"><code>GetOutgoingModifiers()</code></a></td><td>Returns a new array containing the Modifiers that would be removed by this preview.</td></tr>
<tr><td><a href="#catalyst-set-preview-entry-get-incoming-modifiers"><code>GetIncomingModifiers()</code></a></td><td>Returns a new array containing the Modifiers that would be added by this preview.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-set-preview-entry-get-statistic">
  <div class="api-method-name">GetStatistic()</div>
  <p class="api-method-summary">Returns the target Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-preview-entry-get-current-value">
  <div class="api-method-name">GetCurrentValue()</div>
  <p class="api-method-summary">Returns this Statistic&#x27;s value before the proposed ModifierSet change.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-preview-entry-get-preview-value">
  <div class="api-method-name">GetPreviewValue()</div>
  <p class="api-method-summary">Returns what this Statistic&#x27;s value would be after the proposed ModifierSet change.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-preview-entry-get-evaluation">
  <div class="api-method-name">GetEvaluation()</div>
  <p class="api-method-summary">Returns Explain-style details showing exactly how Catalyst calculated this Statistic&#x27;s preview value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic-evaluation">CatalystStatisticEvaluation</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-preview-entry-get-outgoing-modifiers">
  <div class="api-method-name">GetOutgoingModifiers()</div>
  <p class="api-method-summary">Returns a new array containing the Modifiers that would be removed by this preview.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-modifier">CatalystModifier</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-preview-entry-get-incoming-modifiers">
  <div class="api-method-name">GetIncomingModifiers()</div>
  <p class="api-method-summary">Returns a new array containing the Modifiers that would be added by this preview.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-modifier">CatalystModifier</a>&gt;</span>
    </div>
  </div>
</div>

### CatalystRouteDiagnostic
{: #catalyst-route-diagnostic .api-type-title }

Describes one problem found while a <a href="#catalyst-set"><code>CatalystSet</code></a> was trying to match a Modifier&#x27;s target ID to a Statistic and apply or preview it.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-route-diagnostic-get-outcome"><code>GetOutcome()</code></a></td><td>Returns the <a href="#enum-e-cat-route-outcome"><code>eCatRouteOutcome</code></a> value that explains what went wrong.</td></tr>
<tr><td><a href="#catalyst-route-diagnostic-get-subject"><code>GetSubject()</code></a></td><td>Returns the Modifier or other Catalyst value involved in this problem.</td></tr>
<tr><td><a href="#catalyst-route-diagnostic-get-target-identity"><code>GetTargetIdentity()</code></a></td><td>Returns the requested Statistic ID.</td></tr>
<tr><td><a href="#catalyst-route-diagnostic-get-statistic"><code>GetStatistic()</code></a></td><td>Returns the Statistic Catalyst found before the operation failed, or noone if no Statistic was found.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-route-diagnostic-get-outcome">
  <div class="api-method-name">GetOutcome()</div>
  <p class="api-method-summary">Returns the <a href="#enum-e-cat-route-outcome"><code>eCatRouteOutcome</code></a> value that explains what went wrong.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-route-diagnostic-get-subject">
  <div class="api-method-name">GetSubject()</div>
  <p class="api-method-summary">Returns the Modifier or other Catalyst value involved in this problem.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-route-diagnostic-get-target-identity">
  <div class="api-method-name">GetTargetIdentity()</div>
  <p class="api-method-summary">Returns the requested Statistic ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-route-diagnostic-get-statistic">
  <div class="api-method-name">GetStatistic()</div>
  <p class="api-method-summary">Returns the Statistic Catalyst found before the operation failed, or noone if no Statistic was found.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a>,Noone</span>
    </div>
  </div>
</div>

### CatalystSetApplyResult
{: #catalyst-set-apply-result .api-type-title }

Stores the result of Apply() or ApplySwap(). These operations are all-or-nothing: if any Modifier cannot be matched and applied safely, the Set leaves everything unchanged.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-set-apply-result-succeeded"><code>Succeeded()</code></a></td><td>Returns whether the complete apply or swap was performed.</td></tr>
<tr><td><a href="#catalyst-set-apply-result-get-diagnostics"><code>GetDiagnostics()</code></a></td><td>Returns the problems Catalyst found while matching Modifiers to target Statistics.</td></tr>
<tr><td><a href="#catalyst-set-apply-result-get-refresh-results"><code>GetRefreshResults()</code></a></td><td>Returns a new array containing refresh results for touched Statistics.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-set-apply-result-succeeded">
  <div class="api-method-name">Succeeded()</div>
  <p class="api-method-summary">Returns whether the complete apply or swap was performed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-apply-result-get-diagnostics">
  <div class="api-method-name">GetDiagnostics()</div>
  <p class="api-method-summary">Returns the problems Catalyst found while matching Modifiers to target Statistics.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-route-diagnostic">CatalystRouteDiagnostic</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-apply-result-get-refresh-results">
  <div class="api-method-name">GetRefreshResults()</div>
  <p class="api-method-summary">Returns a new array containing refresh results for touched Statistics.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-statistic-refresh-result">CatalystStatisticRefreshResult</a>&gt;</span>
    </div>
  </div>
</div>

### CatalystSetRefreshResult
{: #catalyst-set-refresh-result .api-type-title }

Reports what changed when a <a href="#catalyst-set"><code>CatalystSet</code></a> was refreshed.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-set-refresh-result-did-change"><code>DidChange()</code></a></td><td>Returns whether any refreshed Statistic or Resource changed current value.</td></tr>
<tr><td><a href="#catalyst-set-refresh-result-get-statistic-results"><code>GetStatisticResults()</code></a></td><td>Returns the Statistic refresh results.</td></tr>
<tr><td><a href="#catalyst-set-refresh-result-get-resource-results"><code>GetResourceResults()</code></a></td><td>Returns the Resource refresh results.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-set-refresh-result-did-change">
  <div class="api-method-name">DidChange()</div>
  <p class="api-method-summary">Returns whether any refreshed Statistic or Resource changed current value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-refresh-result-get-statistic-results">
  <div class="api-method-name">GetStatisticResults()</div>
  <p class="api-method-summary">Returns the Statistic refresh results.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-set-statistic-refresh-entry">CatalystSetStatisticRefreshEntry</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-refresh-result-get-resource-results">
  <div class="api-method-name">GetResourceResults()</div>
  <p class="api-method-summary">Returns the Resource refresh results.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-set-resource-refresh-entry">CatalystSetResourceRefreshEntry</a>&gt;</span>
    </div>
  </div>
</div>

### CatalystSetStatisticRefreshEntry
{: #catalyst-set-statistic-refresh-entry .api-type-title }

Pairs one refreshed Statistic with the result of that refresh.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-set-statistic-refresh-entry-get-statistic"><code>GetStatistic()</code></a></td><td>Returns the refreshed Statistic.</td></tr>
<tr><td><a href="#catalyst-set-statistic-refresh-entry-get-result"><code>GetResult()</code></a></td><td>Returns this Statistic&#x27;s refresh result.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-set-statistic-refresh-entry-get-statistic">
  <div class="api-method-name">GetStatistic()</div>
  <p class="api-method-summary">Returns the refreshed Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-statistic-refresh-entry-get-result">
  <div class="api-method-name">GetResult()</div>
  <p class="api-method-summary">Returns this Statistic&#x27;s refresh result.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic-refresh-result">CatalystStatisticRefreshResult</a></span>
    </div>
  </div>
</div>

### CatalystSetResourceRefreshEntry
{: #catalyst-set-resource-refresh-entry .api-type-title }

Pairs one refreshed Resource with its change result.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-set-resource-refresh-entry-get-resource"><code>GetResource()</code></a></td><td>Returns the refreshed Resource.</td></tr>
<tr><td><a href="#catalyst-set-resource-refresh-entry-get-result"><code>GetResult()</code></a></td><td>Returns this Resource&#x27;s refresh result.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-set-resource-refresh-entry-get-resource">
  <div class="api-method-name">GetResource()</div>
  <p class="api-method-summary">Returns the refreshed Resource.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource">CatalystResource</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-resource-refresh-entry-get-result">
  <div class="api-method-name">GetResult()</div>
  <p class="api-method-summary">Returns this Resource&#x27;s refresh result.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-resource-change">CatalystResourceChange</a></span>
    </div>
  </div>
</div>

### CatalystSetDetails
{: #catalyst-set-details .api-type-title }

Contains the Catalyst values currently managed by a Set for inspection or debug UI: Statistic calculation details, direct Resources, and direct EffectManagers.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-set-details-get-statistic-evaluations"><code>GetStatisticEvaluations()</code></a></td><td>Returns the Statistic inspection details.</td></tr>
<tr><td><a href="#catalyst-set-details-get-resources"><code>GetResources()</code></a></td><td>Returns direct Resource members.</td></tr>
<tr><td><a href="#catalyst-set-details-get-effect-managers"><code>GetEffectManagers()</code></a></td><td>Returns direct Effect Manager members.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-set-details-get-statistic-evaluations">
  <div class="api-method-name">GetStatisticEvaluations()</div>
  <p class="api-method-summary">Returns the Statistic inspection details.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-set-statistic-detail">CatalystSetStatisticDetail</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-details-get-resources">
  <div class="api-method-name">GetResources()</div>
  <p class="api-method-summary">Returns direct Resource members.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-resource">CatalystResource</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-details-get-effect-managers">
  <div class="api-method-name">GetEffectManagers()</div>
  <p class="api-method-summary">Returns direct Effect Manager members.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-effect-manager">CatalystEffectManager</a>&gt;</span>
    </div>
  </div>
</div>

### CatalystSetStatisticDetail
{: #catalyst-set-statistic-detail .api-type-title }

Keeps a Statistic together with the Explain() details showing how its current value was calculated.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-set-statistic-detail-get-statistic"><code>GetStatistic()</code></a></td><td>Returns the inspected Statistic.</td></tr>
<tr><td><a href="#catalyst-set-statistic-detail-get-evaluation"><code>GetEvaluation()</code></a></td><td>Returns Explain() details showing how this Statistic&#x27;s value was calculated.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-set-statistic-detail-get-statistic">
  <div class="api-method-name">GetStatistic()</div>
  <p class="api-method-summary">Returns the inspected Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic">CatalystStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-set-statistic-detail-get-evaluation">
  <div class="api-method-name">GetEvaluation()</div>
  <p class="api-method-summary">Returns Explain() details showing how this Statistic&#x27;s value was calculated.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-statistic-evaluation">CatalystStatisticEvaluation</a></span>
    </div>
  </div>
</div>

## Observation, facts, and timing

### CatalystSubscription
{: #catalyst-subscription .api-type-title }

Returned by OnChange() and similar methods when you subscribe to an event. Keep this value if you may want to stop that callback later with Unsubscribe().

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-subscription-unsubscribe"><code>Unsubscribe()</code></a></td><td>Stops this subscription, so its callback will no longer run. Calling Unsubscribe() again is safe and returns false because it is already stopped.</td></tr>
<tr><td><a href="#catalyst-subscription-is-active"><code>IsActive()</code></a></td><td>Returns whether this subscription is still active and able to receive callbacks.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-subscription-unsubscribe">
  <div class="api-method-name">Unsubscribe()</div>
  <p class="api-method-summary">Stops this subscription, so its callback will no longer run. Calling Unsubscribe() again is safe and returns false because it is already stopped.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-subscription-is-active">
  <div class="api-method-name">IsActive()</div>
  <p class="api-method-summary">Returns whether this subscription is still active and able to receive callbacks.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

### CatalystFactBinding
{: #catalyst-fact-binding .api-type-title }

Represents a live connection between a Catalyst Statistic or Resource and an Oracle Fact. PublishToFact() normally creates this for you; keep it if you may want to Sync() or Unbind() later.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-fact-binding-sync"><code>Sync()</code></a></td><td>Immediately writes the current Statistic or Resource value to Oracle again. This is useful after a silent state restore, which intentionally does not fire ordinary change callbacks.</td></tr>
<tr><td><a href="#catalyst-fact-binding-unbind"><code>Unbind()</code></a></td><td>Stops keeping the Oracle Fact updated. The Fact value already stored in Oracle is left in place.</td></tr>
<tr><td><a href="#catalyst-fact-binding-is-bound"><code>IsBound()</code></a></td><td>Returns whether this binding is still publishing changes.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-fact-binding-sync">
  <div class="api-method-name">Sync()</div>
  <p class="api-method-summary">Immediately writes the current Statistic or Resource value to Oracle again. This is useful after a silent state restore, which intentionally does not fire ordinary change callbacks.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-fact-binding">CatalystFactBinding</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-fact-binding-unbind">
  <div class="api-method-name">Unbind()</div>
  <p class="api-method-summary">Stops keeping the Oracle Fact updated. The Fact value already stored in Oracle is left in place.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-fact-binding-is-bound">
  <div class="api-method-name">IsBound()</div>
  <p class="api-method-summary">Returns whether this binding is still publishing changes.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

### CatalystCountdownTracker
{: #catalyst-countdown-tracker .api-type-title }

Creates a timer controller for timed ResourceFlows, Effects, and standalone Modifiers. It can be advanced manually or automatically once per frame.

```gml
new CatalystCountdownTracker()
```

#### Methods

<div class="api-method-group-title">Identity</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-countdown-tracker-set-identity"><code>SetIdentity()</code></a></td><td>Gives this custom countdown tracker an ID so Catalyst save/restore can reconnect timed values to the same tracker after loading.</td></tr>
<tr><td><a href="#catalyst-countdown-tracker-get-identity"><code>GetIdentity()</code></a></td><td>Returns the optional ID used to reconnect this custom countdown tracker during save/restore.</td></tr>
</tbody></table>

<div class="api-method-group-title">Tracked flows</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-countdown-tracker-add-flow"><code>AddFlow()</code></a></td><td>Adds a standalone ResourceFlow to this tracker so Countdown() advances its delay and moves its Resource over time.</td></tr>
<tr><td><a href="#catalyst-countdown-tracker-detach-flow"><code>DetachFlow()</code></a></td><td>Stops this tracker from advancing the Flow. The Flow itself is not destroyed or removed from its Resource.</td></tr>
<tr><td><a href="#catalyst-countdown-tracker-is-tracking-flow"><code>IsTrackingFlow()</code></a></td><td>Returns whether this tracker currently contains the given standalone flow.</td></tr>
</tbody></table>

<div class="api-method-group-title">Tracked effects</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-countdown-tracker-add-effect"><code>AddEffect()</code></a></td><td>Adds an active timed Effect to this tracker so Countdown() advances its duration and tick timing.</td></tr>
<tr><td><a href="#catalyst-countdown-tracker-detach-effect"><code>DetachEffect()</code></a></td><td>Stops this tracker from advancing the Effect&#x27;s timers. The Effect stays active on its EffectManager.</td></tr>
<tr><td><a href="#catalyst-countdown-tracker-is-tracking-effect"><code>IsTrackingEffect()</code></a></td><td>Returns whether this tracker currently contains the given timed effect.</td></tr>
</tbody></table>

<div class="api-method-group-title">Tracked modifiers</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-countdown-tracker-add-modifier"><code>AddModifier()</code></a></td><td>Adds a timed Modifier that is attached directly to a Statistic, so Countdown() advances its remaining duration. Detached Modifiers and Modifiers owned by Effects are ignored because they are timed elsewhere.</td></tr>
<tr><td><a href="#catalyst-countdown-tracker-detach-modifier"><code>DetachModifier()</code></a></td><td>Stops this tracker from advancing the Modifier&#x27;s duration. The Modifier stays attached to its Statistic.</td></tr>
<tr><td><a href="#catalyst-countdown-tracker-is-tracking-modifier"><code>IsTrackingModifier()</code></a></td><td>Returns whether this tracker currently contains the given modifier.</td></tr>
</tbody></table>

<div class="api-method-group-title">Timing</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-countdown-tracker-set-paused"><code>SetPaused()</code></a></td><td>Pauses or resumes this tracker. While paused, both manual Countdown() calls and automatic countdown leave all tracked timers unchanged.</td></tr>
<tr><td><a href="#catalyst-countdown-tracker-is-paused"><code>IsPaused()</code></a></td><td>Returns whether countdown is currently paused.</td></tr>
<tr><td><a href="#catalyst-countdown-tracker-set-time-scale"><code>SetTimeScale()</code></a></td><td>Scales all time passed through this tracker. For example, 0.5 makes timers advance at half speed, 2 doubles their speed, and 0 freezes them without changing the paused setting.</td></tr>
<tr><td><a href="#catalyst-countdown-tracker-get-time-scale"><code>GetTimeScale()</code></a></td><td>Returns the multiplier applied to every countdown step.</td></tr>
<tr><td><a href="#catalyst-countdown-tracker-start-automatic"><code>StartAutomatic()</code></a></td><td>Makes this tracker advance itself once per game frame. FRAMES advances by 1 each frame; DELTA_TIME advances by the frame&#x27;s elapsed time in seconds.</td></tr>
<tr><td><a href="#catalyst-countdown-tracker-stop-automatic"><code>StopAutomatic()</code></a></td><td>Stops automatic countdown without detaching tracked flows, effects, or modifiers.</td></tr>
<tr><td><a href="#catalyst-countdown-tracker-is-automatic"><code>IsAutomatic()</code></a></td><td>Returns whether this tracker is currently advancing itself automatically each frame.</td></tr>
<tr><td><a href="#catalyst-countdown-tracker-get-countdown-mode"><code>GetCountdownMode()</code></a></td><td>Returns the tracker&#x27;s current countdown mode.</td></tr>
<tr><td><a href="#catalyst-countdown-tracker-countdown"><code>Countdown()</code></a></td><td>Passes time to every Flow, Effect, and standalone Modifier tracked here. Time scale and pause state are applied automatically.</td></tr>
</tbody></table>

<div class="api-method-group-title">Debugging and lifecycle</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-countdown-tracker-debug-dump"><code>DebugDump()</code></a></td><td>Writes separate summaries of tracked standalone flows, timed effects, and timed modifiers to debug output.</td></tr>
<tr><td><a href="#catalyst-countdown-tracker-destroy"><code>Destroy()</code></a></td><td>Destroys this tracker and stops its automatic timing. Tracked values are detached from the tracker but are not otherwise destroyed. If called during Countdown(), cleanup finishes after the current countdown pass.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-countdown-tracker-set-identity">
  <div class="api-method-name">SetIdentity(identity)</div>
  <p class="api-method-summary">Gives this custom countdown tracker an ID so Catalyst save/restore can reconnect timed values to the same tracker after loading.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real,Undefined</span>
      <span class="api-argument-description">Non-empty string or finite number to use as the tracker ID, or undefined to clear it.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-countdown-tracker">CatalystCountdownTracker</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-get-identity">
  <div class="api-method-name">GetIdentity()</div>
  <p class="api-method-summary">Returns the optional ID used to reconnect this custom countdown tracker during save/restore.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-add-flow">
  <div class="api-method-name">AddFlow(flow)</div>
  <p class="api-method-summary">Adds a standalone ResourceFlow to this tracker so Countdown() advances its delay and moves its Resource over time.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flow</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
      <span class="api-argument-description">Flow to track.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-countdown-tracker">CatalystCountdownTracker</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-detach-flow">
  <div class="api-method-name">DetachFlow(flow)</div>
  <p class="api-method-summary">Stops this tracker from advancing the Flow. The Flow itself is not destroyed or removed from its Resource.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flow</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
      <span class="api-argument-description">Flow to detach.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-is-tracking-flow">
  <div class="api-method-name">IsTrackingFlow(flow)</div>
  <p class="api-method-summary">Returns whether this tracker currently contains the given standalone flow.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">flow</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-resource-flow">CatalystResourceFlow</a></span>
      <span class="api-argument-description">Flow to query.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-add-effect">
  <div class="api-method-name">AddEffect(effect)</div>
  <p class="api-method-summary">Adds an active timed Effect to this tracker so Countdown() advances its duration and tick timing.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">effect</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
      <span class="api-argument-description">Effect to track.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-countdown-tracker">CatalystCountdownTracker</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-detach-effect">
  <div class="api-method-name">DetachEffect(effect)</div>
  <p class="api-method-summary">Stops this tracker from advancing the Effect&#x27;s timers. The Effect stays active on its EffectManager.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">effect</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
      <span class="api-argument-description">Effect to detach.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-is-tracking-effect">
  <div class="api-method-name">IsTrackingEffect(effect)</div>
  <p class="api-method-summary">Returns whether this tracker currently contains the given timed effect.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">effect</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-effect">CatalystEffect</a></span>
      <span class="api-argument-description">Effect to query.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-add-modifier">
  <div class="api-method-name">AddModifier(modifier)</div>
  <p class="api-method-summary">Adds a timed Modifier that is attached directly to a Statistic, so Countdown() advances its remaining duration. Detached Modifiers and Modifiers owned by Effects are ignored because they are timed elsewhere.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Attached standalone Modifier to track.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-countdown-tracker">CatalystCountdownTracker</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-detach-modifier">
  <div class="api-method-name">DetachModifier(modifier)</div>
  <p class="api-method-summary">Stops this tracker from advancing the Modifier&#x27;s duration. The Modifier stays attached to its Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Modifier to detach.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-is-tracking-modifier">
  <div class="api-method-name">IsTrackingModifier(modifier)</div>
  <p class="api-method-summary">Returns whether this tracker currently contains the given modifier.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">modifier</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-modifier">CatalystModifier</a></span>
      <span class="api-argument-description">Modifier to query.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-set-paused">
  <div class="api-method-name">SetPaused(paused)</div>
  <p class="api-method-summary">Pauses or resumes this tracker. While paused, both manual Countdown() calls and automatic countdown leave all tracked timers unchanged.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">paused</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">True to pause countdown, false to resume.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-is-paused">
  <div class="api-method-name">IsPaused()</div>
  <p class="api-method-summary">Returns whether countdown is currently paused.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-set-time-scale">
  <div class="api-method-name">SetTimeScale(time_scale)</div>
  <p class="api-method-summary">Scales all time passed through this tracker. For example, 0.5 makes timers advance at half speed, 2 doubles their speed, and 0 freezes them without changing the paused setting.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">time_scale</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Time multiplier. Values below 0 are treated as 0.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-get-time-scale">
  <div class="api-method-name">GetTimeScale()</div>
  <p class="api-method-summary">Returns the multiplier applied to every countdown step.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-start-automatic">
  <div class="api-method-name">StartAutomatic([mode])</div>
  <p class="api-method-summary">Makes this tracker advance itself once per game frame. FRAMES advances by 1 each frame; DELTA_TIME advances by the frame&#x27;s elapsed time in seconds.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">mode <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Use <a href="#enum-e-cat-countdown-mode"><code>eCatCountdownMode</code></a>.FRAMES or <a href="#enum-e-cat-countdown-mode"><code>eCatCountdownMode</code></a>.DELTA_TIME. Defaults to FRAMES.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-countdown-tracker">CatalystCountdownTracker</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-stop-automatic">
  <div class="api-method-name">StopAutomatic()</div>
  <p class="api-method-summary">Stops automatic countdown without detaching tracked flows, effects, or modifiers.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-countdown-tracker">CatalystCountdownTracker</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-is-automatic">
  <div class="api-method-name">IsAutomatic()</div>
  <p class="api-method-summary">Returns whether this tracker is currently advancing itself automatically each frame.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-get-countdown-mode">
  <div class="api-method-name">GetCountdownMode()</div>
  <p class="api-method-summary">Returns the tracker&#x27;s current countdown mode.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-countdown">
  <div class="api-method-name">Countdown([step_size])</div>
  <p class="api-method-summary">Passes time to every Flow, Effect, and standalone Modifier tracked here. Time scale and pause state are applied automatically.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">step_size <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Amount of countdown time to pass. Defaults to 1.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-debug-dump">
  <div class="api-method-name">DebugDump()</div>
  <p class="api-method-summary">Writes separate summaries of tracked standalone flows, timed effects, and timed modifiers to debug output.</p>
</div>

<div class="api-method-entry" id="catalyst-countdown-tracker-destroy">
  <div class="api-method-name">Destroy()</div>
  <p class="api-method-summary">Destroys this tracker and stops its automatic timing. Tracked values are detached from the tracker but are not otherwise destroyed. If called during Countdown(), cleanup finishes after the current countdown pass.</p>
</div>

## Saving and loading

### CatalystStateCaptureResult
{: #catalyst-state-capture-result .api-type-title }

Result returned by <a href="#catalyst-set-capture-state"><code>CatalystSet.CaptureState()</code></a>. When Succeeded() is true, GetState() returns the save-friendly Catalyst data. When it is false, GetReport() explains what prevented the capture.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-state-capture-result-succeeded"><code>Succeeded()</code></a></td><td>Returns true when CaptureState() produced complete save data that can be passed to GetState().</td></tr>
<tr><td><a href="#catalyst-state-capture-result-get-state"><code>GetState()</code></a></td><td>Returns the complete captured state when capture succeeded.</td></tr>
<tr><td><a href="#catalyst-state-capture-result-get-report"><code>GetReport()</code></a></td><td>Returns a plain-data report describing whether capture succeeded and, if it failed, what Catalyst could not save. The report is safe to include in JSON or debug output.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-state-capture-result-succeeded">
  <div class="api-method-name">Succeeded()</div>
  <p class="api-method-summary">Returns true when CaptureState() produced complete save data that can be passed to GetState().</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-capture-result-get-state">
  <div class="api-method-name">GetState()</div>
  <p class="api-method-summary">Returns the complete captured state when capture succeeded.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-capture-result-get-report">
  <div class="api-method-name">GetReport()</div>
  <p class="api-method-summary">Returns a plain-data report describing whether capture succeeded and, if it failed, what Catalyst could not save. The report is safe to include in JSON or debug output.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Extra notes</div>
    <div class="api-extra-notes">
      <div class="api-field-list">
        <div class="api-field-row">
          <span class="api-field-name">report_version</span>
          <span class="api-field-type">Real</span>
          <span class="api-field-description">Version of the diagnostic report format.</span>
        </div>
        <div class="api-field-row">
          <span class="api-field-name">success</span>
          <span class="api-field-type">Bool</span>
          <span class="api-field-description">Whether capture succeeded.</span>
        </div>
        <div class="api-field-row">
          <span class="api-field-name">stage</span>
          <span class="api-field-type">String</span>
          <span class="api-field-description">Capture stage represented by this report.</span>
        </div>
        <div class="api-field-row">
          <span class="api-field-name">failures</span>
          <span class="api-field-type">Array&lt;Struct&gt;</span>
          <span class="api-field-description">Plain-data descriptions of values Catalyst could not capture.</span>
        </div>
        <div class="api-field-row">
          <span class="api-field-name">set_identity</span>
          <span class="api-field-type">String,Real,Undefined</span>
          <span class="api-field-description">Set identity when one was available.</span>
        </div>
      </div>
    </div>
  </div>
</div>

### CatalystStateRestoreResult
{: #catalyst-state-restore-result .api-type-title }

Prepared restore handle returned by <a href="#catalyst-set-restore-state"><code>CatalystSet.RestoreState()</code></a>. Use it to repair runtime-only dependencies and call Complete() when the load is ready.

#### Methods

<div class="api-method-group-title">Repair</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-state-restore-result-repair"><code>Repair()</code></a></td><td>Applies a <a href="#catalyst-repair"><code>CatalystRepair</code></a> table to this pending restore. Call this after RestoreState() when the save contains callbacks or custom countdown trackers that must be supplied again at runtime.</td></tr>
<tr><td><a href="#catalyst-state-restore-result-resolve-callbacks"><code>ResolveCallbacks()</code></a></td><td>Advanced alternative to <a href="#catalyst-repair"><code>CatalystRepair()</code></a>. Supplies missing callbacks from a struct grouped by Catalyst type and ID. For Statistics owned inside Resources, Flows, or Effects, put their callbacks inside the matching component entry such as minimum, rate, or chance_per_tick.</td></tr>
<tr><td><a href="#catalyst-state-restore-result-get-missing-callbacks"><code>GetMissingCallbacks()</code></a></td><td>Returns every callback that is still preventing Complete() from loading the captured state. Each requirement tells you what Catalyst value needs the callback and lets you Resolve() it directly.</td></tr>
<tr><td><a href="#catalyst-state-restore-result-get-missing-countdown-trackers"><code>GetMissingCountdownTrackers()</code></a></td><td>Returns every saved value that is still waiting to be reconnected to a custom <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> before Complete() can succeed.</td></tr>
<tr><td><a href="#catalyst-state-restore-result-ignore-missing"><code>IgnoreMissing()</code></a></td><td>Tells the restore to skip any temporary saved Effect, Flow, or Modifier that still cannot be repaired. Direct Set members and other permanent structure are never skipped, so unresolved permanent requirements will still block Complete().</td></tr>
</tbody></table>

<div class="api-method-group-title">Status and completion</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-state-restore-result-get-report"><code>GetReport()</code></a></td><td>Returns a plain-data report describing the current restore stage, unresolved requirements, ignored temporary values, and any failures. The report is safe to include in JSON or debug output.</td></tr>
<tr><td><a href="#catalyst-state-restore-result-is-complete"><code>IsComplete()</code></a></td><td>Returns whether Complete() has successfully applied the captured state to the live <a href="#catalyst-set"><code>CatalystSet</code></a>.</td></tr>
<tr><td><a href="#catalyst-state-restore-result-complete"><code>Complete()</code></a></td><td>Applies the prepared save data to the existing <a href="#catalyst-set"><code>CatalystSet</code></a> once all required callbacks and custom countdown trackers have been repaired or deliberately ignored. The load is gameplay-silent: Catalyst does not treat restored values as ordinary gameplay changes or fire normal change/apply/remove callbacks.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-state-restore-result-repair">
  <div class="api-method-name">Repair(repair)</div>
  <p class="api-method-summary">Applies a <a href="#catalyst-repair"><code>CatalystRepair</code></a> table to this pending restore. Call this after RestoreState() when the save contains callbacks or custom countdown trackers that must be supplied again at runtime.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">repair</span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">Repair table created with <a href="#catalyst-repair"><code>CatalystRepair()</code></a> and filled with the callbacks/trackers your game uses.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-state-restore-result">CatalystStateRestoreResult</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-restore-result-resolve-callbacks">
  <div class="api-method-name">ResolveCallbacks(callbacks)</div>
  <p class="api-method-summary">Advanced alternative to <a href="#catalyst-repair"><code>CatalystRepair()</code></a>. Supplies missing callbacks from a struct grouped by Catalyst type and ID. For Statistics owned inside Resources, Flows, or Effects, put their callbacks inside the matching component entry such as minimum, rate, or chance_per_tick.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callbacks</span>
      <span class="api-argument-type">Struct</span>
      <span class="api-argument-description">Struct containing callback entries grouped by Catalyst type and ID.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-state-restore-result">CatalystStateRestoreResult</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-restore-result-get-missing-callbacks">
  <div class="api-method-name">GetMissingCallbacks()</div>
  <p class="api-method-summary">Returns every callback that is still preventing Complete() from loading the captured state. Each requirement tells you what Catalyst value needs the callback and lets you Resolve() it directly.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-state-callback-requirement">CatalystStateCallbackRequirement</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-restore-result-get-missing-countdown-trackers">
  <div class="api-method-name">GetMissingCountdownTrackers()</div>
  <p class="api-method-summary">Returns every saved value that is still waiting to be reconnected to a custom <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> before Complete() can succeed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;Struct.<a href="#catalyst-state-countdown-tracker-requirement">CatalystStateCountdownTrackerRequirement</a>&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-restore-result-ignore-missing">
  <div class="api-method-name">IgnoreMissing()</div>
  <p class="api-method-summary">Tells the restore to skip any temporary saved Effect, Flow, or Modifier that still cannot be repaired. Direct Set members and other permanent structure are never skipped, so unresolved permanent requirements will still block Complete().</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-state-restore-result">CatalystStateRestoreResult</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-restore-result-get-report">
  <div class="api-method-name">GetReport()</div>
  <p class="api-method-summary">Returns a plain-data report describing the current restore stage, unresolved requirements, ignored temporary values, and any failures. The report is safe to include in JSON or debug output.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Extra notes</div>
    <div class="api-extra-notes">
      <div class="api-field-list">
        <div class="api-field-row">
          <span class="api-field-name">report_version</span>
          <span class="api-field-type">Real</span>
          <span class="api-field-description">Version of the diagnostic report format.</span>
        </div>
        <div class="api-field-row">
          <span class="api-field-name">success</span>
          <span class="api-field-type">Bool</span>
          <span class="api-field-description">Whether the prepared state has been completely applied.</span>
        </div>
        <div class="api-field-row">
          <span class="api-field-name">stage</span>
          <span class="api-field-type">String</span>
          <span class="api-field-description">Current restore stage, such as prepare, pending, ready, apply, or complete.</span>
        </div>
        <div class="api-field-row">
          <span class="api-field-name">salvaged</span>
          <span class="api-field-type">Bool</span>
          <span class="api-field-description">Whether temporary saved values were deliberately ignored so the restore could proceed.</span>
        </div>
        <div class="api-field-row">
          <span class="api-field-name">failures</span>
          <span class="api-field-type">Array&lt;Struct&gt;</span>
          <span class="api-field-description">Plain-data descriptions of unresolved or failed restore requirements.</span>
        </div>
        <div class="api-field-row">
          <span class="api-field-name">ignored</span>
          <span class="api-field-type">Array&lt;Struct&gt;</span>
          <span class="api-field-description">Temporary saved values deliberately skipped by the restore.</span>
        </div>
        <div class="api-field-row">
          <span class="api-field-name">set_identity</span>
          <span class="api-field-type">String,Real,Undefined</span>
          <span class="api-field-description">Live Set identity when available.</span>
        </div>
        <div class="api-field-row">
          <span class="api-field-name">saved_set_identity</span>
          <span class="api-field-type">String,Real,Undefined</span>
          <span class="api-field-description">Identity stored in the captured state when available.</span>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-restore-result-is-complete">
  <div class="api-method-name">IsComplete()</div>
  <p class="api-method-summary">Returns whether Complete() has successfully applied the captured state to the live <a href="#catalyst-set"><code>CatalystSet</code></a>.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-restore-result-complete">
  <div class="api-method-name">Complete()</div>
  <p class="api-method-summary">Applies the prepared save data to the existing <a href="#catalyst-set"><code>CatalystSet</code></a> once all required callbacks and custom countdown trackers have been repaired or deliberately ignored. The load is gameplay-silent: Catalyst does not treat restored values as ordinary gameplay changes or fire normal change/apply/remove callbacks.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

### CatalystStateCallbackRequirement
{: #catalyst-state-callback-requirement .api-type-title }

Represents one missing callback requirement returned by <a href="#catalyst-state-restore-result-get-missing-callbacks"><code>CatalystStateRestoreResult.GetMissingCallbacks()</code></a>.

#### Methods

<div class="api-method-group-title">Identification</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-state-callback-requirement-get-type"><code>GetType()</code></a></td><td>Returns which kind of Catalyst value is missing a callback, such as &quot;statistic&quot;, &quot;modifier&quot;, or &quot;effect&quot;.</td></tr>
<tr><td><a href="#catalyst-state-callback-requirement-get-identity"><code>GetIdentity()</code></a></td><td>Returns the ID of the Catalyst value whose callback needs to be supplied again.</td></tr>
<tr><td><a href="#catalyst-state-callback-requirement-get-component"><code>GetComponent()</code></a></td><td>Tells you which part of the Catalyst value owns the missing callback. For example, &quot;self&quot; means the main value, while &quot;rate&quot;, &quot;minimum&quot;, or &quot;chance_per_tick&quot; refers to an owned Statistic inside it.</td></tr>
<tr><td><a href="#catalyst-state-callback-requirement-get-path"><code>GetPath()</code></a></td><td>Returns a text path showing where this missing callback came from inside the captured state. This is mainly useful for debugging a restore problem.</td></tr>
<tr><td><a href="#catalyst-state-callback-requirement-get-struct"><code>GetStruct()</code></a></td><td>Returns the Catalyst value this missing-callback requirement belongs to. This lets advanced repair code inspect the value directly if needed.</td></tr>
</tbody></table>

<div class="api-method-group-title">Missing callbacks</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-state-callback-requirement-get-callbacks"><code>GetCallbacks()</code></a></td><td>Returns the names of callbacks that this Catalyst value still needs before the restore can complete.</td></tr>
<tr><td><a href="#catalyst-state-callback-requirement-needs"><code>Needs()</code></a></td><td>Returns whether this requirement is still waiting for the callback name you provide.</td></tr>
<tr><td><a href="#catalyst-state-callback-requirement-get-saved-callback-name"><code>GetSavedCallbackName()</code></a></td><td>If the original callback was a named GameMaker function, returns that saved function name. This can help your repair code decide which function to supply again.</td></tr>
<tr><td><a href="#catalyst-state-callback-requirement-resolve"><code>Resolve()</code></a></td><td>Supplies one function that the save file could not store. The function is held until Complete() applies the restored state.</td></tr>
</tbody></table>

<div class="api-method-group-title">Optional salvage</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-state-callback-requirement-can-ignore"><code>CanIgnore()</code></a></td><td>Returns whether you are allowed to skip the temporary saved Effect, Flow, or Modifier that needs this callback. Permanent Set members cannot be skipped.</td></tr>
<tr><td><a href="#catalyst-state-callback-requirement-ignore"><code>Ignore()</code></a></td><td>Marks the temporary saved Effect, Flow, or Modifier containing this missing callback to be skipped when Complete() applies the restore. Use CanIgnore() first.</td></tr>
<tr><td><a href="#catalyst-state-callback-requirement-get-ignore-type"><code>GetIgnoreType()</code></a></td><td>Returns the kind of temporary saved Catalyst value that Ignore() would skip, such as an Effect, Flow, or Modifier.</td></tr>
<tr><td><a href="#catalyst-state-callback-requirement-get-ignore-identity"><code>GetIgnoreIdentity()</code></a></td><td>Returns the ID of the temporary saved Catalyst value that Ignore() would skip.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-state-callback-requirement-get-type">
  <div class="api-method-name">GetType()</div>
  <p class="api-method-summary">Returns which kind of Catalyst value is missing a callback, such as &quot;statistic&quot;, &quot;modifier&quot;, or &quot;effect&quot;.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-callback-requirement-get-identity">
  <div class="api-method-name">GetIdentity()</div>
  <p class="api-method-summary">Returns the ID of the Catalyst value whose callback needs to be supplied again.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-callback-requirement-get-component">
  <div class="api-method-name">GetComponent()</div>
  <p class="api-method-summary">Tells you which part of the Catalyst value owns the missing callback. For example, &quot;self&quot; means the main value, while &quot;rate&quot;, &quot;minimum&quot;, or &quot;chance_per_tick&quot; refers to an owned Statistic inside it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-callback-requirement-get-path">
  <div class="api-method-name">GetPath()</div>
  <p class="api-method-summary">Returns a text path showing where this missing callback came from inside the captured state. This is mainly useful for debugging a restore problem.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-callback-requirement-can-ignore">
  <div class="api-method-name">CanIgnore()</div>
  <p class="api-method-summary">Returns whether you are allowed to skip the temporary saved Effect, Flow, or Modifier that needs this callback. Permanent Set members cannot be skipped.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-callback-requirement-ignore">
  <div class="api-method-name">Ignore()</div>
  <p class="api-method-summary">Marks the temporary saved Effect, Flow, or Modifier containing this missing callback to be skipped when Complete() applies the restore. Use CanIgnore() first.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-callback-requirement-get-ignore-type">
  <div class="api-method-name">GetIgnoreType()</div>
  <p class="api-method-summary">Returns the kind of temporary saved Catalyst value that Ignore() would skip, such as an Effect, Flow, or Modifier.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-callback-requirement-get-ignore-identity">
  <div class="api-method-name">GetIgnoreIdentity()</div>
  <p class="api-method-summary">Returns the ID of the temporary saved Catalyst value that Ignore() would skip.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-callback-requirement-get-struct">
  <div class="api-method-name">GetStruct()</div>
  <p class="api-method-summary">Returns the Catalyst value this missing-callback requirement belongs to. This lets advanced repair code inspect the value directly if needed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-callback-requirement-get-callbacks">
  <div class="api-method-name">GetCallbacks()</div>
  <p class="api-method-summary">Returns the names of callbacks that this Catalyst value still needs before the restore can complete.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;String&gt;</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-callback-requirement-needs">
  <div class="api-method-name">Needs(callback)</div>
  <p class="api-method-summary">Returns whether this requirement is still waiting for the callback name you provide.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Callback name, such as &quot;condition&quot;, &quot;on_apply&quot;, or another name returned by GetCallbacks().</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-callback-requirement-get-saved-callback-name">
  <div class="api-method-name">GetSavedCallbackName(callback)</div>
  <p class="api-method-summary">If the original callback was a named GameMaker function, returns that saved function name. This can help your repair code decide which function to supply again.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Callback slot from this requirement.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-callback-requirement-resolve">
  <div class="api-method-name">Resolve(callback, fn)</div>
  <p class="api-method-summary">Supplies one function that the save file could not store. The function is held until Complete() applies the restored state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Callback slot name returned by GetCallbacks().</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function to restore into this callback slot when Complete() succeeds.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

### CatalystStateCountdownTrackerRequirement
{: #catalyst-state-countdown-tracker-requirement .api-type-title }

Represents one missing custom countdown tracker requirement returned by <a href="#catalyst-state-restore-result-get-missing-countdown-trackers"><code>CatalystStateRestoreResult.GetMissingCountdownTrackers()</code></a>.

#### Methods

<div class="api-method-group-title">Identification</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-state-countdown-tracker-requirement-get-type"><code>GetType()</code></a></td><td>Returns which kind of Catalyst value is waiting for a custom <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a>, such as an Effect, Flow, or Modifier.</td></tr>
<tr><td><a href="#catalyst-state-countdown-tracker-requirement-get-identity"><code>GetIdentity()</code></a></td><td>Returns the ID of the Catalyst value that needs to be reconnected to a custom countdown tracker.</td></tr>
<tr><td><a href="#catalyst-state-countdown-tracker-requirement-get-tracker-identity"><code>GetTrackerIdentity()</code></a></td><td>Returns the ID of the custom <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> this saved value used before it was captured.</td></tr>
<tr><td><a href="#catalyst-state-countdown-tracker-requirement-get-path"><code>GetPath()</code></a></td><td>Returns the saved-state path containing the missing countdown tracker.</td></tr>
<tr><td><a href="#catalyst-state-countdown-tracker-requirement-get-struct"><code>GetStruct()</code></a></td><td>Returns the Catalyst value this missing-tracker requirement belongs to. This lets advanced repair code inspect the value directly if needed.</td></tr>
</tbody></table>

<div class="api-method-group-title">Resolution</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-state-countdown-tracker-requirement-resolve"><code>Resolve()</code></a></td><td>Reconnects this saved Catalyst value to the live custom <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> it used before saving.</td></tr>
</tbody></table>

<div class="api-method-group-title">Optional salvage</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-state-countdown-tracker-requirement-can-ignore"><code>CanIgnore()</code></a></td><td>Returns whether you are allowed to skip the temporary saved Effect, Flow, or Modifier that needs this tracker. Permanent Set members cannot be skipped.</td></tr>
<tr><td><a href="#catalyst-state-countdown-tracker-requirement-ignore"><code>Ignore()</code></a></td><td>Marks the temporary saved Effect, Flow, or Modifier containing this tracker to be skipped when Complete() applies the restore. Use CanIgnore() first.</td></tr>
<tr><td><a href="#catalyst-state-countdown-tracker-requirement-get-ignore-type"><code>GetIgnoreType()</code></a></td><td>Returns the kind of temporary saved Catalyst value that Ignore() would skip, such as an Effect, Flow, or Modifier.</td></tr>
<tr><td><a href="#catalyst-state-countdown-tracker-requirement-get-ignore-identity"><code>GetIgnoreIdentity()</code></a></td><td>Returns the ID of the temporary saved Catalyst value that Ignore() would skip.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-state-countdown-tracker-requirement-get-type">
  <div class="api-method-name">GetType()</div>
  <p class="api-method-summary">Returns which kind of Catalyst value is waiting for a custom <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a>, such as an Effect, Flow, or Modifier.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-countdown-tracker-requirement-get-identity">
  <div class="api-method-name">GetIdentity()</div>
  <p class="api-method-summary">Returns the ID of the Catalyst value that needs to be reconnected to a custom countdown tracker.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-countdown-tracker-requirement-get-tracker-identity">
  <div class="api-method-name">GetTrackerIdentity()</div>
  <p class="api-method-summary">Returns the ID of the custom <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> this saved value used before it was captured.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-countdown-tracker-requirement-get-path">
  <div class="api-method-name">GetPath()</div>
  <p class="api-method-summary">Returns the saved-state path containing the missing countdown tracker.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-countdown-tracker-requirement-can-ignore">
  <div class="api-method-name">CanIgnore()</div>
  <p class="api-method-summary">Returns whether you are allowed to skip the temporary saved Effect, Flow, or Modifier that needs this tracker. Permanent Set members cannot be skipped.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-countdown-tracker-requirement-ignore">
  <div class="api-method-name">Ignore()</div>
  <p class="api-method-summary">Marks the temporary saved Effect, Flow, or Modifier containing this tracker to be skipped when Complete() applies the restore. Use CanIgnore() first.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-countdown-tracker-requirement-get-ignore-type">
  <div class="api-method-name">GetIgnoreType()</div>
  <p class="api-method-summary">Returns the kind of temporary saved Catalyst value that Ignore() would skip, such as an Effect, Flow, or Modifier.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-countdown-tracker-requirement-get-ignore-identity">
  <div class="api-method-name">GetIgnoreIdentity()</div>
  <p class="api-method-summary">Returns the ID of the temporary saved Catalyst value that Ignore() would skip.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String,Real,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-countdown-tracker-requirement-get-struct">
  <div class="api-method-name">GetStruct()</div>
  <p class="api-method-summary">Returns the Catalyst value this missing-tracker requirement belongs to. This lets advanced repair code inspect the value directly if needed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-state-countdown-tracker-requirement-resolve">
  <div class="api-method-name">Resolve(tracker)</div>
  <p class="api-method-summary">Reconnects this saved Catalyst value to the live custom <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> it used before saving.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tracker</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-countdown-tracker">CatalystCountdownTracker</a></span>
      <span class="api-argument-description">Live tracker whose ID matches GetTrackerIdentity().</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

### CatalystRepair
{: #catalyst-repair .api-type-title }

Creates a repair table for Catalyst state loading. Save files can store ordinary data but cannot preserve every runtime function or live custom countdown tracker, so use this table to provide those values again before calling Complete(). Its helper methods are arranged to work well with GameMaker autocomplete.

```gml
new CatalystRepair()
```

#### Methods

<div class="api-method-group-title">Runtime repair</div>
<table class="api-methods"><tbody>
<tr><td><a href="#catalyst-repair-add-countdown-tracker"><code>AddCountdownTracker()</code></a></td><td>Adds a live custom <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> to this repair table so saved Effects, Flows, or Modifiers that used it can reconnect after loading. The tracker must have an ID.</td></tr>
<tr><td><a href="#catalyst-repair-add-statistic"><code>AddStatistic()</code></a></td><td>Opens the repair entry for the Statistic with this ID. Use the returned entry to supply callbacks that could not be stored in the save file.</td></tr>
<tr><td><a href="#catalyst-repair-add-resource"><code>AddResource()</code></a></td><td>Opens the repair entry for the Resource with this ID. From there you can repair callbacks on its minimum or maximum Statistics.</td></tr>
<tr><td><a href="#catalyst-repair-add-flow"><code>AddFlow()</code></a></td><td>Opens the repair entry for the ResourceFlow with this ID. From there you can repair callbacks on its rate Statistic.</td></tr>
<tr><td><a href="#catalyst-repair-add-modifier"><code>AddModifier()</code></a></td><td>Opens the repair entry for the Modifier with this ID so you can restore its condition or stack function.</td></tr>
<tr><td><a href="#catalyst-repair-add-effect"><code>AddEffect()</code></a></td><td>Opens the repair entry for the Effect with this ID so you can restore its callbacks and callbacks on its chance Statistics.</td></tr>
<tr><td><a href="#catalyst-repair-add-effect-manager"><code>AddEffectManager()</code></a></td><td>Opens the repair entry for the EffectManager with this ID so you can restore its custom random function.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-repair-add-countdown-tracker">
  <div class="api-method-name">AddCountdownTracker(tracker)</div>
  <p class="api-method-summary">Adds a live custom <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> to this repair table so saved Effects, Flows, or Modifiers that used it can reconnect after loading. The tracker must have an ID.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tracker</span>
      <span class="api-argument-type">Struct.<a href="#catalyst-countdown-tracker">CatalystCountdownTracker</a></span>
      <span class="api-argument-description">Live custom tracker with the same ID it had when the state was captured.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair">CatalystRepair</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-repair-add-statistic">
  <div class="api-method-name">AddStatistic(identity)</div>
  <p class="api-method-summary">Opens the repair entry for the Statistic with this ID. Use the returned entry to supply callbacks that could not be stored in the save file.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">ID of the Statistic you want to repair.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-statistic">__CatalystRepairStatistic</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-repair-add-resource">
  <div class="api-method-name">AddResource(identity)</div>
  <p class="api-method-summary">Opens the repair entry for the Resource with this ID. From there you can repair callbacks on its minimum or maximum Statistics.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">ID of the Resource you want to repair.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-resource">__CatalystRepairResource</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-repair-add-flow">
  <div class="api-method-name">AddFlow(identity)</div>
  <p class="api-method-summary">Opens the repair entry for the ResourceFlow with this ID. From there you can repair callbacks on its rate Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">ID of the Flow you want to repair.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-flow">__CatalystRepairFlow</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-repair-add-modifier">
  <div class="api-method-name">AddModifier(identity)</div>
  <p class="api-method-summary">Opens the repair entry for the Modifier with this ID so you can restore its condition or stack function.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">ID of the Modifier you want to repair.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-modifier">__CatalystRepairModifier</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-repair-add-effect">
  <div class="api-method-name">AddEffect(identity)</div>
  <p class="api-method-summary">Opens the repair entry for the Effect with this ID so you can restore its callbacks and callbacks on its chance Statistics.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">ID of the Effect you want to repair.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-effect">__CatalystRepairEffect</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-repair-add-effect-manager">
  <div class="api-method-name">AddEffectManager(identity)</div>
  <p class="api-method-summary">Opens the repair entry for the EffectManager with this ID so you can restore its custom random function.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">identity</span>
      <span class="api-argument-type">String,Real</span>
      <span class="api-argument-description">ID of the EffectManager you want to repair.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-effect-manager">__CatalystRepairEffectManager</a>,Undefined</span>
    </div>
  </div>
</div>

### Statistic repair row
{: #catalyst-repair-statistic .api-type-title }

Returned as `__CatalystRepairStatistic`.

Repair row created by <a href="#catalyst-repair-add-statistic"><code>CatalystRepair.AddStatistic()</code></a> or an owned-Statistic helper. It carries runtime-only Statistic callbacks for a pending restore.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-repair-statistic-base-func"><code>BaseFunc()</code></a></td><td>Supplies the Statistic&#x27;s SetBaseFunc() function for a pending state restore.</td></tr>
<tr><td><a href="#catalyst-repair-statistic-post-process"><code>PostProcess()</code></a></td><td>Supplies the Statistic&#x27;s SetPostProcess() function for a pending state restore.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-repair-statistic-base-func">
  <div class="api-method-name">BaseFunc(fn)</div>
  <p class="api-method-summary">Supplies the Statistic&#x27;s SetBaseFunc() function for a pending state restore.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function that should be restored into this callback slot.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-statistic">__CatalystRepairStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-repair-statistic-post-process">
  <div class="api-method-name">PostProcess(fn)</div>
  <p class="api-method-summary">Supplies the Statistic&#x27;s SetPostProcess() function for a pending state restore.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function that should be restored into this callback slot.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-statistic">__CatalystRepairStatistic</a></span>
    </div>
  </div>
</div>

### Resource repair row
{: #catalyst-repair-resource .api-type-title }

Returned as `__CatalystRepairResource`.

Repair row created by <a href="#catalyst-repair-add-resource"><code>CatalystRepair.AddResource()</code></a>. It exposes repair rows for the Resource&#x27;s owned minimum and maximum Statistics.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-repair-resource-minimum"><code>Minimum()</code></a></td><td>Opens the repair entry for callbacks belonging to this Resource&#x27;s minimum Statistic.</td></tr>
<tr><td><a href="#catalyst-repair-resource-maximum"><code>Maximum()</code></a></td><td>Opens the repair entry for callbacks belonging to this Resource&#x27;s maximum Statistic.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-repair-resource-minimum">
  <div class="api-method-name">Minimum()</div>
  <p class="api-method-summary">Opens the repair entry for callbacks belonging to this Resource&#x27;s minimum Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-statistic">__CatalystRepairStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-repair-resource-maximum">
  <div class="api-method-name">Maximum()</div>
  <p class="api-method-summary">Opens the repair entry for callbacks belonging to this Resource&#x27;s maximum Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-statistic">__CatalystRepairStatistic</a></span>
    </div>
  </div>
</div>

### Resource Flow repair row
{: #catalyst-repair-flow .api-type-title }

Returned as `__CatalystRepairFlow`.

Repair row created by <a href="#catalyst-repair-add-flow"><code>CatalystRepair.AddFlow()</code></a>. It exposes the repair row for the Flow&#x27;s owned rate Statistic.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-repair-flow-rate"><code>Rate()</code></a></td><td>Opens the repair entry for callbacks belonging to this Flow&#x27;s rate Statistic.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-repair-flow-rate">
  <div class="api-method-name">Rate()</div>
  <p class="api-method-summary">Opens the repair entry for callbacks belonging to this Flow&#x27;s rate Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-statistic">__CatalystRepairStatistic</a></span>
    </div>
  </div>
</div>

### Modifier repair row
{: #catalyst-repair-modifier .api-type-title }

Returned as `__CatalystRepairModifier`.

Repair row created by <a href="#catalyst-repair-add-modifier"><code>CatalystRepair.AddModifier()</code></a>. It carries runtime-only Modifier callbacks for a pending restore.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-repair-modifier-condition"><code>Condition()</code></a></td><td>Supplies the Modifier function normally set with SetCondition() for a pending state restore.</td></tr>
<tr><td><a href="#catalyst-repair-modifier-stack-func"><code>StackFunc()</code></a></td><td>Supplies the Modifier function normally set with SetStackFunc() for a pending state restore.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-repair-modifier-condition">
  <div class="api-method-name">Condition(fn)</div>
  <p class="api-method-summary">Supplies the Modifier function normally set with SetCondition() for a pending state restore.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function that should be restored into this callback slot.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-modifier">__CatalystRepairModifier</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-repair-modifier-stack-func">
  <div class="api-method-name">StackFunc(fn)</div>
  <p class="api-method-summary">Supplies the Modifier function normally set with SetStackFunc() for a pending state restore.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function that should be restored into this callback slot.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-modifier">__CatalystRepairModifier</a></span>
    </div>
  </div>
</div>

### Effect repair row
{: #catalyst-repair-effect .api-type-title }

Returned as `__CatalystRepairEffect`.

Repair row created by <a href="#catalyst-repair-add-effect"><code>CatalystRepair.AddEffect()</code></a>. It carries runtime-only Effect callbacks and exposes its owned chance Statistics for repair.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-repair-effect-on-apply"><code>OnApply()</code></a></td><td>Supplies the Effect callback normally set with SetOnApply() for a pending state restore.</td></tr>
<tr><td><a href="#catalyst-repair-effect-resolve-tick"><code>ResolveTick()</code></a></td><td>Supplies the Effect callback normally set with SetResolveTick() for a pending state restore.</td></tr>
<tr><td><a href="#catalyst-repair-effect-on-tick"><code>OnTick()</code></a></td><td>Supplies the Effect callback normally set with SetOnTick() for a pending state restore.</td></tr>
<tr><td><a href="#catalyst-repair-effect-on-remove"><code>OnRemove()</code></a></td><td>Supplies the Effect callback normally set with SetOnRemove() for a pending state restore.</td></tr>
<tr><td><a href="#catalyst-repair-effect-chance-to-apply"><code>ChanceToApply()</code></a></td><td>Opens the repair entry for callbacks belonging to this Effect&#x27;s chance-to-apply Statistic.</td></tr>
<tr><td><a href="#catalyst-repair-effect-chance-per-tick"><code>ChancePerTick()</code></a></td><td>Opens the repair entry for callbacks belonging to this Effect&#x27;s chance-per-tick Statistic.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-repair-effect-on-apply">
  <div class="api-method-name">OnApply(fn)</div>
  <p class="api-method-summary">Supplies the Effect callback normally set with SetOnApply() for a pending state restore.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function that should be restored into this callback slot.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-effect">__CatalystRepairEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-repair-effect-resolve-tick">
  <div class="api-method-name">ResolveTick(fn)</div>
  <p class="api-method-summary">Supplies the Effect callback normally set with SetResolveTick() for a pending state restore.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function that should be restored into this callback slot.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-effect">__CatalystRepairEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-repair-effect-on-tick">
  <div class="api-method-name">OnTick(fn)</div>
  <p class="api-method-summary">Supplies the Effect callback normally set with SetOnTick() for a pending state restore.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function that should be restored into this callback slot.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-effect">__CatalystRepairEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-repair-effect-on-remove">
  <div class="api-method-name">OnRemove(fn)</div>
  <p class="api-method-summary">Supplies the Effect callback normally set with SetOnRemove() for a pending state restore.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function that should be restored into this callback slot.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-effect">__CatalystRepairEffect</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-repair-effect-chance-to-apply">
  <div class="api-method-name">ChanceToApply()</div>
  <p class="api-method-summary">Opens the repair entry for callbacks belonging to this Effect&#x27;s chance-to-apply Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-statistic">__CatalystRepairStatistic</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="catalyst-repair-effect-chance-per-tick">
  <div class="api-method-name">ChancePerTick()</div>
  <p class="api-method-summary">Opens the repair entry for callbacks belonging to this Effect&#x27;s chance-per-tick Statistic.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-statistic">__CatalystRepairStatistic</a></span>
    </div>
  </div>
</div>

### Effect Manager repair row
{: #catalyst-repair-effect-manager .api-type-title }

Returned as `__CatalystRepairEffectManager`.

Repair row created by <a href="#catalyst-repair-add-effect-manager"><code>CatalystRepair.AddEffectManager()</code></a>. It carries the EffectManager&#x27;s runtime random function for a pending restore.

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#catalyst-repair-effect-manager-random-function"><code>RandomFunction()</code></a></td><td>Supplies the EffectManager function normally set with SetRandomFunction() for a pending state restore.</td></tr>
</tbody></table>

<div class="api-method-entry" id="catalyst-repair-effect-manager-random-function">
  <div class="api-method-name">RandomFunction(fn)</div>
  <p class="api-method-summary">Supplies the EffectManager function normally set with SetRandomFunction() for a pending state restore.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">fn</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function that should be restored into this callback slot.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#catalyst-repair-effect-manager">__CatalystRepairEffectManager</a></span>
    </div>
  </div>
</div>

## Global functions

<div class="api-method-entry" id="catalyst-countdown">
  <div class="api-method-name">CatalystCountdown([step_size])</div>
  <p class="api-method-summary">Advances the global <a href="#macro-catalyst-countdown"><code>CATALYST_COUNTDOWN</code></a> tracker by the amount you provide. You normally only need this when automatic countdown is disabled or when you want to drive Catalyst with your own time system.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">step_size <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Amount of countdown time to pass. Defaults to 1.</span>
    </div>
  </div>
</div>

## Enums

### Statistics and modifiers
{: .api-function-subsection-title .api-function-subsection-title-first }

<div class="api-enum-entry" id="enum-e-cat-math-ops">
  <div class="api-enum-name">eCatMathOps</div>
  <p class="api-enum-summary">Chooses how a Modifier changes a Statistic. ADD adds or subtracts a value, MULTIPLY scales it, and FORCE_MIN/FORCE_MAX set lower or upper limits.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">ADD</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">MULTIPLY</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">FORCE_MIN</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">FORCE_MAX</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-cat-modifier-order">
  <div class="api-enum-name">eCatModifierOrder</div>
  <p class="api-enum-summary">Chooses the order used for ADD and MULTIPLY Modifiers inside each Statistic layer.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">ADD_FIRST</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">MULTIPLY_FIRST</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">ATTACHMENT_ORDER</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-cat-stat-layer">
  <div class="api-enum-name">eCatStatLayer</div>
  <p class="api-enum-summary">Ready-made Statistic layer IDs. You can use these or provide your own string or number layer IDs.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">BASE_BONUS</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">EQUIPMENT</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">AUGMENTS</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">TEMP</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">GLOBAL</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-cat-stack-mode">
  <div class="api-enum-name">eCatStackMode</div>
  <p class="api-enum-summary">Chooses how multiple stacks of a MULTIPLY Modifier combine. COMPOUND multiplies once per stack; ADDITIVE combines the percentage first.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">COMPOUND</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">ADDITIVE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-cat-family-mode">
  <div class="api-enum-name">eCatFamilyMode</div>
  <p class="api-enum-summary">Chooses what happens when several Modifiers belong to the same family: use all of them, only the strongest, or only the weakest.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">STACK_ALL</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">STRONGEST</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">WEAKEST</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-cat-family-scope">
  <div class="api-enum-name">eCatFamilyScope</div>
  <p class="api-enum-summary">Chooses where Modifier family rules apply. LAYER compares family members only inside the same layer; STATISTIC compares them across the whole Statistic.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">LAYER</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">STATISTIC</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-cat-modifier-skip-reason">
  <div class="api-enum-name">eCatModifierSkipReason</div>
  <p class="api-enum-summary">Explains why a Modifier did not affect a Statistic calculation, such as a failed condition, zero stacks, losing its family comparison, or using an unknown layer.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NONE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">CONDITION_FAILED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">ZERO_STACKS</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">FAMILY_LOST</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">UNKNOWN_LAYER</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

### Resources
{: .api-function-subsection-title }

<div class="api-enum-entry" id="enum-e-cat-resource-bound-mode">
  <div class="api-enum-name">eCatResourceBoundMode</div>
  <p class="api-enum-summary">Chooses how a Resource minimum or maximum behaves. HARD never allows the value past the bound, SOFT blocks ordinary movement past it but can be crossed explicitly, and OPEN does not restrict the value.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">HARD</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">SOFT</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">OPEN</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-cat-resource-operation">
  <div class="api-enum-name">eCatResourceOperation</div>
  <p class="api-enum-summary">Identifies the kind of Resource change recorded in a <a href="#catalyst-resource-change"><code>CatalystResourceChange</code></a> result.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">SET</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">CHANGE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">INCREASE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">DECREASE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">FILL</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">EMPTY</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">RECONCILE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

### Effects
{: .api-function-subsection-title }

<div class="api-enum-entry" id="enum-e-cat-effect-reapply-policy">
  <div class="api-enum-name">eCatEffectReapplyPolicy</div>
  <p class="api-enum-summary">Chooses what an EffectManager does when an Effect is applied while another active Effect has the same ID.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">STACK</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">IGNORE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">REPLACE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">REFRESH</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">EXTEND</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-cat-effect-application-outcome">
  <div class="api-enum-name">eCatEffectApplicationOutcome</div>
  <p class="api-enum-summary">Explains what happened when <a href="#catalyst-effect-manager-add-effect"><code>CatalystEffectManager.AddEffect()</code></a> tried to apply an Effect.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">ADDED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">QUEUED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">FAILED_CHANCE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">IGNORED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">REPLACED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">REFRESHED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">EXTENDED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">INVALID_EFFECT</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">MANAGER_DESTROYING</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">ALREADY_MANAGED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">EXPIRED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">TRACKER_DESTROYING</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

### Sets and routing
{: .api-function-subsection-title }

<div class="api-enum-entry" id="enum-e-cat-set-preview-status">
  <div class="api-enum-name">eCatSetPreviewStatus</div>
  <p class="api-enum-summary">Summarises whether a <a href="#catalyst-set"><code>CatalystSet</code></a> preview could route every requested Modifier, only some of them, or none of them.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">SUCCESS</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">PARTIAL</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">FAILED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-cat-route-outcome">
  <div class="api-enum-name">eCatRouteOutcome</div>
  <p class="api-enum-summary">Explains why a <a href="#catalyst-set"><code>CatalystSet</code></a> could or could not match a Modifier to its target Statistic and perform the requested apply or swap.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">INVALID_TARGET_SET</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">INVALID_INCOMING_SET</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">INVALID_OUTGOING_SET</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">INVALID_MODIFIER</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">DUPLICATE_REFERENCE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">MISSING_TARGET_IDENTITY</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">TARGET_NOT_FOUND</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">UNKNOWN_TARGET_LAYER</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">MODIFIER_ALREADY_PRESENT</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">MODIFIER_ATTACHED_ELSEWHERE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">MODIFIER_EFFECT_OWNED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">OUTGOING_MODIFIER_NOT_ATTACHED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">OUTGOING_TARGET_NOT_IN_SET</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">OUTGOING_TARGET_IDENTITY_MISMATCH</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">MODIFIER_EXPIRED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">MODIFIER_TRACKER_DESTROYING</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

### Timing
{: .api-function-subsection-title }

<div class="api-enum-entry" id="enum-e-cat-countdown-mode">
  <div class="api-enum-name">eCatCountdownMode</div>
  <p class="api-enum-summary">Chooses how automatic countdown measures time. FRAMES counts one unit per game frame, while DELTA_TIME uses elapsed real time.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">MANUAL</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">FRAMES</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">DELTA_TIME</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

## Package globals

<div class="api-method-entry api-macro-entry api-macro-handle" id="macro-catalyst-countdown">
  <div class="api-method-name">CATALYST_COUNTDOWN</div>
  <p class="api-method-summary">Global default <a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> used by timed Catalyst values unless you assign a custom tracker. Catalyst creates it at package startup and runs it automatically in frame mode. Use a custom tracker when one model needs an independent timing source.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Type</div>
    <div class="api-return-row api-return-only"><span class="api-return-type">Struct.<a href="#catalyst-countdown-tracker">CatalystCountdownTracker</a></span></div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a> <span aria-hidden="true">·</span> <a href="#catalyst-countdown"><code>CatalystCountdown</code></a></div>
  </div>
</div>

## Symbol index

<div class="api-symbol-index">
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">_</div>
    <div class="api-symbol-row"><a href="#catalyst-repair-effect"><code>__CatalystRepairEffect</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-effect-manager"><code>__CatalystRepairEffectManager</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-flow"><code>__CatalystRepairFlow</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-modifier"><code>__CatalystRepairModifier</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-resource"><code>__CatalystRepairResource</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-statistic"><code>__CatalystRepairStatistic</code></a></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">A</div>
    <div class="api-symbol-row"><a href="#catalyst-repair-add-countdown-tracker"><code>AddCountdownTracker()</code></a> <span class="api-symbol-owner">| CatalystRepair</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-add-effect"><code>AddEffect()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-add-effect"><code>AddEffect()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-add-effect"><code>AddEffect()</code></a> <span class="api-symbol-owner">| CatalystRepair</span></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-add-effect-manager"><code>AddEffectManager()</code></a> <span class="api-symbol-owner">| CatalystRepair</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-add-effect-manager"><code>AddEffectManager()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-add-flow"><code>AddFlow()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-add-flow"><code>AddFlow()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-add-flow"><code>AddFlow()</code></a> <span class="api-symbol-owner">| CatalystRepair</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-add-flow"><code>AddFlow()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-add-maximum-modifier"><code>AddMaximumModifier()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-add-minimum-modifier"><code>AddMinimumModifier()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-add-modifier"><code>AddModifier()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-add-modifier"><code>AddModifier()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-add-modifier"><code>AddModifier()</code></a> <span class="api-symbol-owner">| CatalystModifierSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-add-modifier"><code>AddModifier()</code></a> <span class="api-symbol-owner">| CatalystRepair</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-add-modifier"><code>AddModifier()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-add-resource"><code>AddResource()</code></a> <span class="api-symbol-owner">| CatalystRepair</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-add-resource"><code>AddResource()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-add-stacks"><code>AddStacks()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-add-statistic"><code>AddStatistic()</code></a> <span class="api-symbol-owner">| CatalystRepair</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-add-statistic"><code>AddStatistic()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-add-tag"><code>AddTag()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-add-tag"><code>AddTag()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-add-tag"><code>AddTag()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-application-result-applied"><code>Applied()</code></a> <span class="api-symbol-owner">| CatalystEffectApplicationResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-evaluation-applied"><code>Applied()</code></a> <span class="api-symbol-owner">| CatalystModifierEvaluation</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-apply"><code>Apply()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-apply-swap"><code>ApplySwap()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">B</div>
    <div class="api-symbol-row"><a href="#catalyst-repair-statistic-base-func"><code>BaseFunc()</code></a> <span class="api-symbol-owner">| __CatalystRepairStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-bind-chance-per-tick-statistic"><code>BindChancePerTickStatistic()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-bind-chance-to-apply-statistic"><code>BindChanceToApplyStatistic()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-bind-maximum-statistic"><code>BindMaximumStatistic()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-bind-minimum-statistic"><code>BindMinimumStatistic()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-bind-rate-statistic"><code>BindRateStatistic()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">C</div>
    <div class="api-symbol-row"><a href="#catalyst-state-callback-requirement-can-ignore"><code>CanIgnore()</code></a> <span class="api-symbol-owner">| CatalystStateCallbackRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-countdown-tracker-requirement-can-ignore"><code>CanIgnore()</code></a> <span class="api-symbol-owner">| CatalystStateCountdownTrackerRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-capture-state"><code>CaptureState()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown"><code>CatalystCountdown()</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker"><code>CatalystCountdownTracker</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-effect"><code>CatalystEffect</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-application-result"><code>CatalystEffectApplicationResult</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager"><code>CatalystEffectManager</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-tick-result"><code>CatalystEffectTickResult</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-fact-binding"><code>CatalystFactBinding</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier"><code>CatalystModifier</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-evaluation"><code>CatalystModifierEvaluation</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set"><code>CatalystModifierSet</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-repair"><code>CatalystRepair</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-resource"><code>CatalystResource</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change"><code>CatalystResourceChange</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow"><code>CatalystResourceFlow</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-result"><code>CatalystResourceFlowResult</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-route-diagnostic"><code>CatalystRouteDiagnostic</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-set"><code>CatalystSet</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-set-apply-result"><code>CatalystSetApplyResult</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-set-details"><code>CatalystSetDetails</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-set-preview-entry"><code>CatalystSetPreviewEntry</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-set-preview-result"><code>CatalystSetPreviewResult</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-set-refresh-result"><code>CatalystSetRefreshResult</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-set-resource-refresh-entry"><code>CatalystSetResourceRefreshEntry</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-set-statistic-detail"><code>CatalystSetStatisticDetail</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-set-statistic-refresh-entry"><code>CatalystSetStatisticRefreshEntry</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-state-callback-requirement"><code>CatalystStateCallbackRequirement</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-state-capture-result"><code>CatalystStateCaptureResult</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-state-countdown-tracker-requirement"><code>CatalystStateCountdownTrackerRequirement</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-state-restore-result"><code>CatalystStateRestoreResult</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic"><code>CatalystStatistic</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-evaluation"><code>CatalystStatisticEvaluation</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-layer-evaluation"><code>CatalystStatisticLayerEvaluation</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-refresh-result"><code>CatalystStatisticRefreshResult</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-subscription"><code>CatalystSubscription</code></a></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-effect-chance-per-tick"><code>ChancePerTick()</code></a> <span class="api-symbol-owner">| __CatalystRepairEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-tick-result-chance-succeeded"><code>ChanceSucceeded()</code></a> <span class="api-symbol-owner">| CatalystEffectTickResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-effect-chance-to-apply"><code>ChanceToApply()</code></a> <span class="api-symbol-owner">| __CatalystRepairEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change"><code>Change()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-change-base-value"><code>ChangeBaseValue()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-change-max-value"><code>ChangeMaxValue()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-change-min-value"><code>ChangeMinValue()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change-past-bounds"><code>ChangePastBounds()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-clear-base-func"><code>ClearBaseFunc()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-clear-condition"><code>ClearCondition()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-clear-delay"><code>ClearDelay()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-clear-fact-view"><code>ClearFactView()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-clear-fact-view"><code>ClearFactView()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-clear-family"><code>ClearFamily()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-clear-layer-order"><code>ClearLayerOrder()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-clear-on-apply"><code>ClearOnApply()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-clear-on-remove"><code>ClearOnRemove()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-clear-on-tick"><code>ClearOnTick()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-clear-post-process"><code>ClearPostProcess()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-clear-random-function"><code>ClearRandomFunction()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-clear-resolve-tick"><code>ClearResolveTick()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-clear-rounding"><code>ClearRounding()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-clear-stack-func"><code>ClearStackFunc()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-clear-tags"><code>ClearTags()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-clear-tags"><code>ClearTags()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-clear-tags"><code>ClearTags()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-clear-tick-interval"><code>ClearTickInterval()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-restore-result-complete"><code>Complete()</code></a> <span class="api-symbol-owner">| CatalystStateRestoreResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-modifier-condition"><code>Condition()</code></a> <span class="api-symbol-owner">| __CatalystRepairModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-countdown"><code>Countdown()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">D</div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-debug-describe"><code>DebugDescribe()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-debug-dump"><code>DebugDump()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-decrease"><code>Decrease()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-decrease-past-minimum"><code>DecreasePastMinimum()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-delay"><code>Delay()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-destroy"><code>Destroy()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-destroy"><code>Destroy()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-destroy"><code>Destroy()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-destroy"><code>Destroy()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-destroy"><code>Destroy()</code></a> <span class="api-symbol-owner">| CatalystModifierSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-destroy"><code>Destroy()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-destroy"><code>Destroy()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-destroy-all-modifiers"><code>DestroyAllModifiers()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-destroy-flow"><code>DestroyFlow()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-destroy-maximum-modifier"><code>DestroyMaximumModifier()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-destroy-minimum-modifier"><code>DestroyMinimumModifier()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-destroy-modifier"><code>DestroyModifier()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-destroy-modifiers-by-source-id"><code>DestroyModifiersBySourceId()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-destroy-modifiers-by-source-label"><code>DestroyModifiersBySourceLabel()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-destroy-modifiers-by-source-meta"><code>DestroyModifiersBySourceMeta()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-destroy-modifiers-by-tag"><code>DestroyModifiersByTag()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-detach-effect"><code>DetachEffect()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-detach-flow"><code>DetachFlow()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-detach-modifier"><code>DetachModifier()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-detach-modifier"><code>DetachModifier()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change-did-change"><code>DidChange()</code></a> <span class="api-symbol-owner">| CatalystResourceChange</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-refresh-result-did-change"><code>DidChange()</code></a> <span class="api-symbol-owner">| CatalystSetRefreshResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-refresh-result-did-change"><code>DidChange()</code></a> <span class="api-symbol-owner">| CatalystStatisticRefreshResult</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">E</div>
    <div class="api-symbol-row"><a href="#catalyst-resource-empty"><code>Empty()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-evaluate"><code>Evaluate()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-explain"><code>Explain()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">F</div>
    <div class="api-symbol-row"><a href="#catalyst-resource-fill"><code>Fill()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-find-modifiers-by-source-id"><code>FindModifiersBySourceId()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-find-modifiers-by-source-label"><code>FindModifiersBySourceLabel()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-find-modifiers-by-source-meta"><code>FindModifiersBySourceMeta()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">G</div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change-get-applied"><code>GetApplied()</code></a> <span class="api-symbol-owner">| CatalystResourceChange</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-get-base-value"><code>GetBaseValue()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-evaluation-get-base-value"><code>GetBaseValue()</code></a> <span class="api-symbol-owner">| CatalystStatisticEvaluation</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-callback-requirement-get-callbacks"><code>GetCallbacks()</code></a> <span class="api-symbol-owner">| CatalystStateCallbackRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-application-result-get-chance"><code>GetChance()</code></a> <span class="api-symbol-owner">| CatalystEffectApplicationResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-tick-result-get-chance"><code>GetChance()</code></a> <span class="api-symbol-owner">| CatalystEffectTickResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-get-chance-per-tick-statistic"><code>GetChancePerTickStatistic()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-get-chance-to-apply-statistic"><code>GetChanceToApplyStatistic()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-result-get-change"><code>GetChange()</code></a> <span class="api-symbol-owner">| CatalystResourceFlowResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-callback-requirement-get-component"><code>GetComponent()</code></a> <span class="api-symbol-owner">| CatalystStateCallbackRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-evaluation-get-contribution"><code>GetContribution()</code></a> <span class="api-symbol-owner">| CatalystModifierEvaluation</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-result-get-countdown-amount"><code>GetCountdownAmount()</code></a> <span class="api-symbol-owner">| CatalystResourceFlowResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-get-countdown-mode"><code>GetCountdownMode()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-get-countdown-tracker"><code>GetCountdownTracker()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-get-countdown-tracker"><code>GetCountdownTracker()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-get-countdown-tracker"><code>GetCountdownTracker()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-get-current"><code>GetCurrent()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change-get-current"><code>GetCurrent()</code></a> <span class="api-symbol-owner">| CatalystResourceChange</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-refresh-result-get-current"><code>GetCurrent()</code></a> <span class="api-symbol-owner">| CatalystStatisticRefreshResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-preview-entry-get-current-value"><code>GetCurrentValue()</code></a> <span class="api-symbol-owner">| CatalystSetPreviewEntry</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-get-delay-remaining"><code>GetDelayRemaining()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-get-details"><code>GetDetails()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-apply-result-get-diagnostics"><code>GetDiagnostics()</code></a> <span class="api-symbol-owner">| CatalystSetApplyResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-preview-result-get-diagnostics"><code>GetDiagnostics()</code></a> <span class="api-symbol-owner">| CatalystSetPreviewResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-application-result-get-effect"><code>GetEffect()</code></a> <span class="api-symbol-owner">| CatalystEffectApplicationResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-tick-result-get-effect"><code>GetEffect()</code></a> <span class="api-symbol-owner">| CatalystEffectTickResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-evaluation-get-effective-stacks"><code>GetEffectiveStacks()</code></a> <span class="api-symbol-owner">| CatalystModifierEvaluation</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-get-effect-manager"><code>GetEffectManager()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-get-effect-managers"><code>GetEffectManagers()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-details-get-effect-managers"><code>GetEffectManagers()</code></a> <span class="api-symbol-owner">| CatalystSetDetails</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-get-effects"><code>GetEffects()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-get-effects-by-family"><code>GetEffectsByFamily()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-get-effects-by-identity"><code>GetEffectsByIdentity()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-get-effects-tagged"><code>GetEffectsTagged()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-preview-result-get-entries"><code>GetEntries()</code></a> <span class="api-symbol-owner">| CatalystSetPreviewResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-preview-entry-get-evaluation"><code>GetEvaluation()</code></a> <span class="api-symbol-owner">| CatalystSetPreviewEntry</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-statistic-detail-get-evaluation"><code>GetEvaluation()</code></a> <span class="api-symbol-owner">| CatalystSetStatisticDetail</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-get-fact-view"><code>GetFactView()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-get-fact-view"><code>GetFactView()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-get-family"><code>GetFamily()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-result-get-flow"><code>GetFlow()</code></a> <span class="api-symbol-owner">| CatalystResourceFlowResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-tick-result-get-flow-results"><code>GetFlowResults()</code></a> <span class="api-symbol-owner">| CatalystEffectTickResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-get-flows"><code>GetFlows()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-get-fraction"><code>GetFraction()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-get-identity"><code>GetIdentity()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-get-identity"><code>GetIdentity()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-get-identity"><code>GetIdentity()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-get-identity"><code>GetIdentity()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-get-identity"><code>GetIdentity()</code></a> <span class="api-symbol-owner">| CatalystModifierSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-get-identity"><code>GetIdentity()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-get-identity"><code>GetIdentity()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-get-identity"><code>GetIdentity()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-callback-requirement-get-identity"><code>GetIdentity()</code></a> <span class="api-symbol-owner">| CatalystStateCallbackRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-countdown-tracker-requirement-get-identity"><code>GetIdentity()</code></a> <span class="api-symbol-owner">| CatalystStateCountdownTrackerRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-get-identity"><code>GetIdentity()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-callback-requirement-get-ignore-identity"><code>GetIgnoreIdentity()</code></a> <span class="api-symbol-owner">| CatalystStateCallbackRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-countdown-tracker-requirement-get-ignore-identity"><code>GetIgnoreIdentity()</code></a> <span class="api-symbol-owner">| CatalystStateCountdownTrackerRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-callback-requirement-get-ignore-type"><code>GetIgnoreType()</code></a> <span class="api-symbol-owner">| CatalystStateCallbackRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-countdown-tracker-requirement-get-ignore-type"><code>GetIgnoreType()</code></a> <span class="api-symbol-owner">| CatalystStateCountdownTrackerRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-application-result-get-incoming-effect"><code>GetIncomingEffect()</code></a> <span class="api-symbol-owner">| CatalystEffectApplicationResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-preview-entry-get-incoming-modifiers"><code>GetIncomingModifiers()</code></a> <span class="api-symbol-owner">| CatalystSetPreviewEntry</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-get-last-change"><code>GetLastChange()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-layer-evaluation-get-layer"><code>GetLayer()</code></a> <span class="api-symbol-owner">| CatalystStatisticLayerEvaluation</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-get-layer-order"><code>GetLayerOrder()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-get-layer-order"><code>GetLayerOrder()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-evaluation-get-layers"><code>GetLayers()</code></a> <span class="api-symbol-owner">| CatalystStatisticEvaluation</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-get-maximum"><code>GetMaximum()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change-get-maximum"><code>GetMaximum()</code></a> <span class="api-symbol-owner">| CatalystResourceChange</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-get-maximum-bound-mode"><code>GetMaximumBoundMode()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-get-maximum-statistic"><code>GetMaximumStatistic()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-get-max-value"><code>GetMaxValue()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-get-meta"><code>GetMeta()</code></a> <span class="api-symbol-owner">| CatalystModifierSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change-get-meta"><code>GetMeta()</code></a> <span class="api-symbol-owner">| CatalystResourceChange</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-get-meta"><code>GetMeta()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-get-minimum"><code>GetMinimum()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change-get-minimum"><code>GetMinimum()</code></a> <span class="api-symbol-owner">| CatalystResourceChange</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-get-minimum-bound-mode"><code>GetMinimumBoundMode()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-get-minimum-statistic"><code>GetMinimumStatistic()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-get-min-value"><code>GetMinValue()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-get-missing"><code>GetMissing()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-restore-result-get-missing-callbacks"><code>GetMissingCallbacks()</code></a> <span class="api-symbol-owner">| CatalystStateRestoreResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-restore-result-get-missing-countdown-trackers"><code>GetMissingCountdownTrackers()</code></a> <span class="api-symbol-owner">| CatalystStateRestoreResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-evaluation-get-modifier"><code>GetModifier()</code></a> <span class="api-symbol-owner">| CatalystModifierEvaluation</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-get-modifier-order"><code>GetModifierOrder()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-evaluation-get-modifier-results"><code>GetModifierResults()</code></a> <span class="api-symbol-owner">| CatalystStatisticEvaluation</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-layer-evaluation-get-modifier-results"><code>GetModifierResults()</code></a> <span class="api-symbol-owner">| CatalystStatisticLayerEvaluation</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-get-modifiers"><code>GetModifiers()</code></a> <span class="api-symbol-owner">| CatalystModifierSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-get-modifiers"><code>GetModifiers()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-tick-result-get-multiplier"><code>GetMultiplier()</code></a> <span class="api-symbol-owner">| CatalystEffectTickResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-result-get-multiplier"><code>GetMultiplier()</code></a> <span class="api-symbol-owner">| CatalystResourceFlowResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-get-name"><code>GetName()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-get-name"><code>GetName()</code></a> <span class="api-symbol-owner">| CatalystModifierSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-get-name"><code>GetName()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-get-name"><code>GetName()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-get-name"><code>GetName()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-get-name"><code>GetName()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change-get-operation"><code>GetOperation()</code></a> <span class="api-symbol-owner">| CatalystResourceChange</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-application-result-get-outcome"><code>GetOutcome()</code></a> <span class="api-symbol-owner">| CatalystEffectApplicationResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-route-diagnostic-get-outcome"><code>GetOutcome()</code></a> <span class="api-symbol-owner">| CatalystRouteDiagnostic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-preview-entry-get-outgoing-modifiers"><code>GetOutgoingModifiers()</code></a> <span class="api-symbol-owner">| CatalystSetPreviewEntry</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-get-overflow"><code>GetOverflow()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-get-owner"><code>GetOwner()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-callback-requirement-get-path"><code>GetPath()</code></a> <span class="api-symbol-owner">| CatalystStateCallbackRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-countdown-tracker-requirement-get-path"><code>GetPath()</code></a> <span class="api-symbol-owner">| CatalystStateCountdownTrackerRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-preview-entry-get-preview-value"><code>GetPreviewValue()</code></a> <span class="api-symbol-owner">| CatalystSetPreviewEntry</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change-get-previous"><code>GetPrevious()</code></a> <span class="api-symbol-owner">| CatalystResourceChange</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-refresh-result-get-previous"><code>GetPrevious()</code></a> <span class="api-symbol-owner">| CatalystStatisticRefreshResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change-get-previous-maximum"><code>GetPreviousMaximum()</code></a> <span class="api-symbol-owner">| CatalystResourceChange</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change-get-previous-minimum"><code>GetPreviousMinimum()</code></a> <span class="api-symbol-owner">| CatalystResourceChange</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-result-get-rate"><code>GetRate()</code></a> <span class="api-symbol-owner">| CatalystResourceFlowResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-get-rate-statistic"><code>GetRateStatistic()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-get-reapply-policy"><code>GetReapplyPolicy()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change-get-reason"><code>GetReason()</code></a> <span class="api-symbol-owner">| CatalystResourceChange</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-apply-result-get-refresh-results"><code>GetRefreshResults()</code></a> <span class="api-symbol-owner">| CatalystSetApplyResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-capture-result-get-report"><code>GetReport()</code></a> <span class="api-symbol-owner">| CatalystStateCaptureResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-restore-result-get-report"><code>GetReport()</code></a> <span class="api-symbol-owner">| CatalystStateRestoreResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change-get-requested"><code>GetRequested()</code></a> <span class="api-symbol-owner">| CatalystResourceChange</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-result-get-requested"><code>GetRequested()</code></a> <span class="api-symbol-owner">| CatalystResourceFlowResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-result-get-resource"><code>GetResource()</code></a> <span class="api-symbol-owner">| CatalystResourceFlowResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-get-resource"><code>GetResource()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-resource-refresh-entry-get-resource"><code>GetResource()</code></a> <span class="api-symbol-owner">| CatalystSetResourceRefreshEntry</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-refresh-result-get-resource-results"><code>GetResourceResults()</code></a> <span class="api-symbol-owner">| CatalystSetRefreshResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-get-resources"><code>GetResources()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-details-get-resources"><code>GetResources()</code></a> <span class="api-symbol-owner">| CatalystSetDetails</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-resource-refresh-entry-get-result"><code>GetResult()</code></a> <span class="api-symbol-owner">| CatalystSetResourceRefreshEntry</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-statistic-refresh-entry-get-result"><code>GetResult()</code></a> <span class="api-symbol-owner">| CatalystSetStatisticRefreshEntry</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-application-result-get-roll"><code>GetRoll()</code></a> <span class="api-symbol-owner">| CatalystEffectApplicationResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-tick-result-get-roll"><code>GetRoll()</code></a> <span class="api-symbol-owner">| CatalystEffectTickResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-callback-requirement-get-saved-callback-name"><code>GetSavedCallbackName()</code></a> <span class="api-symbol-owner">| CatalystStateCallbackRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-evaluation-get-skip-reason"><code>GetSkipReason()</code></a> <span class="api-symbol-owner">| CatalystModifierEvaluation</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change-get-source"><code>GetSource()</code></a> <span class="api-symbol-owner">| CatalystResourceChange</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-get-stack-mode"><code>GetStackMode()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-get-starting-value"><code>GetStartingValue()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-capture-result-get-state"><code>GetState()</code></a> <span class="api-symbol-owner">| CatalystStateCaptureResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-route-diagnostic-get-statistic"><code>GetStatistic()</code></a> <span class="api-symbol-owner">| CatalystRouteDiagnostic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-get-statistic"><code>GetStatistic()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-preview-entry-get-statistic"><code>GetStatistic()</code></a> <span class="api-symbol-owner">| CatalystSetPreviewEntry</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-statistic-detail-get-statistic"><code>GetStatistic()</code></a> <span class="api-symbol-owner">| CatalystSetStatisticDetail</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-statistic-refresh-entry-get-statistic"><code>GetStatistic()</code></a> <span class="api-symbol-owner">| CatalystSetStatisticRefreshEntry</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-details-get-statistic-evaluations"><code>GetStatisticEvaluations()</code></a> <span class="api-symbol-owner">| CatalystSetDetails</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-refresh-result-get-statistic-results"><code>GetStatisticResults()</code></a> <span class="api-symbol-owner">| CatalystSetRefreshResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-get-statistics"><code>GetStatistics()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-preview-result-get-status"><code>GetStatus()</code></a> <span class="api-symbol-owner">| CatalystSetPreviewResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-callback-requirement-get-struct"><code>GetStruct()</code></a> <span class="api-symbol-owner">| CatalystStateCallbackRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-countdown-tracker-requirement-get-struct"><code>GetStruct()</code></a> <span class="api-symbol-owner">| CatalystStateCountdownTrackerRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-route-diagnostic-get-subject"><code>GetSubject()</code></a> <span class="api-symbol-owner">| CatalystRouteDiagnostic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change-get-target"><code>GetTarget()</code></a> <span class="api-symbol-owner">| CatalystResourceChange</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-get-target-identity"><code>GetTargetIdentity()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-route-diagnostic-get-target-identity"><code>GetTargetIdentity()</code></a> <span class="api-symbol-owner">| CatalystRouteDiagnostic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-tick-result-get-tick-duration"><code>GetTickDuration()</code></a> <span class="api-symbol-owner">| CatalystEffectTickResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-get-tick-interval"><code>GetTickInterval()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-get-time-scale"><code>GetTimeScale()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-countdown-tracker-requirement-get-tracker-identity"><code>GetTrackerIdentity()</code></a> <span class="api-symbol-owner">| CatalystStateCountdownTrackerRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-callback-requirement-get-type"><code>GetType()</code></a> <span class="api-symbol-owner">| CatalystStateCallbackRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-countdown-tracker-requirement-get-type"><code>GetType()</code></a> <span class="api-symbol-owner">| CatalystStateCountdownTrackerRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-get-underflow"><code>GetUnderflow()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-get-value"><code>GetValue()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-evaluation-get-value"><code>GetValue()</code></a> <span class="api-symbol-owner">| CatalystStatisticEvaluation</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-evaluation-get-value-after"><code>GetValueAfter()</code></a> <span class="api-symbol-owner">| CatalystModifierEvaluation</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-evaluation-get-value-before"><code>GetValueBefore()</code></a> <span class="api-symbol-owner">| CatalystModifierEvaluation</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">H</div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-has-effect"><code>HasEffect()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-has-effect-identity"><code>HasEffectIdentity()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-has-effect-manager"><code>HasEffectManager()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-has-flow"><code>HasFlow()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-has-layer"><code>HasLayer()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-has-modifier"><code>HasModifier()</code></a> <span class="api-symbol-owner">| CatalystModifierSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-has-modifier"><code>HasModifier()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-has-modifier-from-source-id"><code>HasModifierFromSourceId()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-has-modifier-from-source-label"><code>HasModifierFromSourceLabel()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-has-modifier-from-source-meta"><code>HasModifierFromSourceMeta()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-has-resource"><code>HasResource()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-has-statistic"><code>HasStatistic()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-has-tag"><code>HasTag()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-has-tag"><code>HasTag()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-has-tag"><code>HasTag()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-has-tag"><code>HasTag()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">I</div>
    <div class="api-symbol-row"><a href="#catalyst-state-callback-requirement-ignore"><code>Ignore()</code></a> <span class="api-symbol-owner">| CatalystStateCallbackRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-countdown-tracker-requirement-ignore"><code>Ignore()</code></a> <span class="api-symbol-owner">| CatalystStateCountdownTrackerRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-restore-result-ignore-missing"><code>IgnoreMissing()</code></a> <span class="api-symbol-owner">| CatalystStateRestoreResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-increase"><code>Increase()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-increase-past-maximum"><code>IncreasePastMaximum()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-is-active"><code>IsActive()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-subscription-is-active"><code>IsActive()</code></a> <span class="api-symbol-owner">| CatalystSubscription</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-is-automatic"><code>IsAutomatic()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-fact-binding-is-bound"><code>IsBound()</code></a> <span class="api-symbol-owner">| CatalystFactBinding</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-is-chance-per-tick-bound"><code>IsChancePerTickBound()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-is-chance-to-apply-bound"><code>IsChanceToApplyBound()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-restore-result-is-complete"><code>IsComplete()</code></a> <span class="api-symbol-owner">| CatalystStateRestoreResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-is-delayed"><code>IsDelayed()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-is-empty"><code>IsEmpty()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-is-full"><code>IsFull()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-is-maximum-bound"><code>IsMaximumBound()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-is-minimum-bound"><code>IsMinimumBound()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-is-paused"><code>IsPaused()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-is-rate-bound"><code>IsRateBound()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-is-tracking-effect"><code>IsTrackingEffect()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-is-tracking-flow"><code>IsTrackingFlow()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-is-tracking-modifier"><code>IsTrackingModifier()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">M</div>
    <div class="api-symbol-row"><a href="#catalyst-repair-resource-maximum"><code>Maximum()</code></a> <span class="api-symbol-owner">| __CatalystRepairResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-resource-minimum"><code>Minimum()</code></a> <span class="api-symbol-owner">| __CatalystRepairResource</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">N</div>
    <div class="api-symbol-row"><a href="#catalyst-state-callback-requirement-needs"><code>Needs()</code></a> <span class="api-symbol-owner">| CatalystStateCallbackRequirement</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">O</div>
    <div class="api-symbol-row"><a href="#catalyst-repair-effect-on-apply"><code>OnApply()</code></a> <span class="api-symbol-owner">| __CatalystRepairEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-on-change"><code>OnChange()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-on-change"><code>OnChange()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-on-effect-applied"><code>OnEffectApplied()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-on-effect-removed"><code>OnEffectRemoved()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-effect-on-remove"><code>OnRemove()</code></a> <span class="api-symbol-owner">| __CatalystRepairEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-effect-on-tick"><code>OnTick()</code></a> <span class="api-symbol-owner">| __CatalystRepairEffect</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">P</div>
    <div class="api-symbol-row"><a href="#catalyst-repair-statistic-post-process"><code>PostProcess()</code></a> <span class="api-symbol-owner">| __CatalystRepairStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-preview"><code>Preview()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-preview"><code>Preview()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-preview-modifiers"><code>PreviewModifiers()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-preview-swap"><code>PreviewSwap()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-publish-to-fact"><code>PublishToFact()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-publish-to-fact"><code>PublishToFact()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">Q</div>
    <div class="api-symbol-row"><a href="#catalyst-effect-application-result-queued"><code>Queued()</code></a> <span class="api-symbol-owner">| CatalystEffectApplicationResult</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">R</div>
    <div class="api-symbol-row"><a href="#catalyst-repair-effect-manager-random-function"><code>RandomFunction()</code></a> <span class="api-symbol-owner">| __CatalystRepairEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-flow-rate"><code>Rate()</code></a> <span class="api-symbol-owner">| __CatalystRepairFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-refresh"><code>Refresh()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-refresh"><code>Refresh()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-refresh"><code>Refresh()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-remove-effect"><code>RemoveEffect()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-remove-effect-manager"><code>RemoveEffectManager()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-remove-effects-by-identity"><code>RemoveEffectsByIdentity()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-remove-effects-tagged"><code>RemoveEffectsTagged()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-remove-flow"><code>RemoveFlow()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-remove-flow"><code>RemoveFlow()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-remove-modifier"><code>RemoveModifier()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-remove-modifier"><code>RemoveModifier()</code></a> <span class="api-symbol-owner">| CatalystModifierSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-remove-resource"><code>RemoveResource()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-remove-statistic"><code>RemoveStatistic()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-remove-tag"><code>RemoveTag()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-remove-tag"><code>RemoveTag()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-remove-tag"><code>RemoveTag()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-restore-result-repair"><code>Repair()</code></a> <span class="api-symbol-owner">| CatalystStateRestoreResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-reset-all"><code>ResetAll()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-reset-duration"><code>ResetDuration()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-reset-duration"><code>ResetDuration()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-reset-to-starting"><code>ResetToStarting()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-callback-requirement-resolve"><code>Resolve()</code></a> <span class="api-symbol-owner">| CatalystStateCallbackRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-countdown-tracker-requirement-resolve"><code>Resolve()</code></a> <span class="api-symbol-owner">| CatalystStateCountdownTrackerRequirement</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-restore-result-resolve-callbacks"><code>ResolveCallbacks()</code></a> <span class="api-symbol-owner">| CatalystStateRestoreResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-effect-resolve-tick"><code>ResolveTick()</code></a> <span class="api-symbol-owner">| __CatalystRepairEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-restore-state"><code>RestoreState()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">S</div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-set-active"><code>SetActive()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-set-base-func"><code>SetBaseFunc()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-set-base-value"><code>SetBaseValue()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-set-chance-per-tick"><code>SetChancePerTick()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-set-chance-to-apply"><code>SetChanceToApply()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-set-clamped"><code>SetClamped()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-condition"><code>SetCondition()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-set-countdown-tracker"><code>SetCountdownTracker()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-countdown-tracker"><code>SetCountdownTracker()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-set-countdown-tracker"><code>SetCountdownTracker()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-set-current"><code>SetCurrent()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-set-duration"><code>SetDuration()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-duration"><code>SetDuration()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-set-fact-view"><code>SetFactView()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-set-fact-view"><code>SetFactView()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-set-family"><code>SetFamily()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-family"><code>SetFamily()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-family-mode"><code>SetFamilyMode()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-family-scope"><code>SetFamilyScope()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-set-identity"><code>SetIdentity()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-set-identity"><code>SetIdentity()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-set-identity"><code>SetIdentity()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-identity"><code>SetIdentity()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-set-identity"><code>SetIdentity()</code></a> <span class="api-symbol-owner">| CatalystModifierSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-set-identity"><code>SetIdentity()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-set-identity"><code>SetIdentity()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-set-identity"><code>SetIdentity()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-set-identity"><code>SetIdentity()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-layer"><code>SetLayer()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-set-layer-order"><code>SetLayerOrder()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-set-layer-order"><code>SetLayerOrder()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-maths-op"><code>SetMathsOp()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-set-maximum"><code>SetMaximum()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-set-maximum-bound-mode"><code>SetMaximumBoundMode()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-max-stacks"><code>SetMaxStacks()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-set-max-value"><code>SetMaxValue()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-set-meta"><code>SetMeta()</code></a> <span class="api-symbol-owner">| CatalystModifierSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-set-meta"><code>SetMeta()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-set-minimum"><code>SetMinimum()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-set-minimum-bound-mode"><code>SetMinimumBoundMode()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-set-min-value"><code>SetMinValue()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-set-modifier-order"><code>SetModifierOrder()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-tick-result-set-multiplier"><code>SetMultiplier()</code></a> <span class="api-symbol-owner">| CatalystEffectTickResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-set-name"><code>SetName()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-set-name"><code>SetName()</code></a> <span class="api-symbol-owner">| CatalystModifierSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-set-name"><code>SetName()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-set-name"><code>SetName()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-set-name"><code>SetName()</code></a> <span class="api-symbol-owner">| CatalystSet</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-set-name"><code>SetName()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-set-on-apply"><code>SetOnApply()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-set-on-remove"><code>SetOnRemove()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-set-on-tick"><code>SetOnTick()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-set-paused"><code>SetPaused()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-set-post-process"><code>SetPostProcess()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-manager-set-random-function"><code>SetRandomFunction()</code></a> <span class="api-symbol-owner">| CatalystEffectManager</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-set-rate"><code>SetRate()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-set-reapply-policy"><code>SetReapplyPolicy()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-set-resolve-tick"><code>SetResolveTick()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-statistic-set-rounding-step"><code>SetRoundingStep()</code></a> <span class="api-symbol-owner">| CatalystStatistic</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-source-id"><code>SetSourceId()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-set-source-id"><code>SetSourceId()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-source-label"><code>SetSourceLabel()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-set-source-label"><code>SetSourceLabel()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-source-meta"><code>SetSourceMeta()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-set-source-meta"><code>SetSourceMeta()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-stack-func"><code>SetStackFunc()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-stack-mode"><code>SetStackMode()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-stacks"><code>SetStacks()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-tick-result-set-succeeded"><code>SetSucceeded()</code></a> <span class="api-symbol-owner">| CatalystEffectTickResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-target-identity"><code>SetTargetIdentity()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-set-tick-interval"><code>SetTickInterval()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-set-time-scale"><code>SetTimeScale()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-set-value"><code>SetValue()</code></a> <span class="api-symbol-owner">| CatalystModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-repair-modifier-stack-func"><code>StackFunc()</code></a> <span class="api-symbol-owner">| __CatalystRepairModifier</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-start-automatic"><code>StartAutomatic()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-countdown-tracker-stop-automatic"><code>StopAutomatic()</code></a> <span class="api-symbol-owner">| CatalystCountdownTracker</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-application-result-succeeded"><code>Succeeded()</code></a> <span class="api-symbol-owner">| CatalystEffectApplicationResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-tick-result-succeeded"><code>Succeeded()</code></a> <span class="api-symbol-owner">| CatalystEffectTickResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-change-succeeded"><code>Succeeded()</code></a> <span class="api-symbol-owner">| CatalystResourceChange</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-result-succeeded"><code>Succeeded()</code></a> <span class="api-symbol-owner">| CatalystResourceFlowResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-apply-result-succeeded"><code>Succeeded()</code></a> <span class="api-symbol-owner">| CatalystSetApplyResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-set-preview-result-succeeded"><code>Succeeded()</code></a> <span class="api-symbol-owner">| CatalystSetPreviewResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-state-capture-result-succeeded"><code>Succeeded()</code></a> <span class="api-symbol-owner">| CatalystStateCaptureResult</span></div>
    <div class="api-symbol-row"><a href="#catalyst-fact-binding-sync"><code>Sync()</code></a> <span class="api-symbol-owner">| CatalystFactBinding</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">U</div>
    <div class="api-symbol-row"><a href="#catalyst-fact-binding-unbind"><code>Unbind()</code></a> <span class="api-symbol-owner">| CatalystFactBinding</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-unbind-chance-per-tick-statistic"><code>UnbindChancePerTickStatistic()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-effect-unbind-chance-to-apply-statistic"><code>UnbindChanceToApplyStatistic()</code></a> <span class="api-symbol-owner">| CatalystEffect</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-unbind-maximum-statistic"><code>UnbindMaximumStatistic()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-unbind-minimum-statistic"><code>UnbindMinimumStatistic()</code></a> <span class="api-symbol-owner">| CatalystResource</span></div>
    <div class="api-symbol-row"><a href="#catalyst-resource-flow-unbind-rate-statistic"><code>UnbindRateStatistic()</code></a> <span class="api-symbol-owner">| CatalystResourceFlow</span></div>
    <div class="api-symbol-row"><a href="#catalyst-subscription-unsubscribe"><code>Unsubscribe()</code></a> <span class="api-symbol-owner">| CatalystSubscription</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">W</div>
    <div class="api-symbol-row"><a href="#catalyst-modifier-evaluation-won-family"><code>WonFamily()</code></a> <span class="api-symbol-owner">| CatalystModifierEvaluation</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">Enums</div>
    <div class="api-symbol-row"><a href="#enum-e-cat-countdown-mode"><code>eCatCountdownMode</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-cat-effect-application-outcome"><code>eCatEffectApplicationOutcome</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-cat-effect-reapply-policy"><code>eCatEffectReapplyPolicy</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-cat-family-mode"><code>eCatFamilyMode</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-cat-family-scope"><code>eCatFamilyScope</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-cat-math-ops"><code>eCatMathOps</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-cat-modifier-order"><code>eCatModifierOrder</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-cat-modifier-skip-reason"><code>eCatModifierSkipReason</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-cat-resource-bound-mode"><code>eCatResourceBoundMode</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-cat-resource-operation"><code>eCatResourceOperation</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-cat-route-outcome"><code>eCatRouteOutcome</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-cat-set-preview-status"><code>eCatSetPreviewStatus</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-cat-stack-mode"><code>eCatStackMode</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-cat-stat-layer"><code>eCatStatLayer</code></a><span class="api-symbol-owner">enum</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">Macros</div>
    <div class="api-symbol-row"><a href="#macro-catalyst-countdown"><code>CATALYST_COUNTDOWN</code></a><span class="api-symbol-owner">macro</span></div>
  </div>
</div>
