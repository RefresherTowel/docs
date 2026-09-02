---
layout: "default"
title: "API Reference"
parent: "Echo"
nav_order: 3
library_id: "echo"
doc_version: "current"
api_reference: true
---

<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. -->
<!-- Source: GML JSDoc + echo.yml -->

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>

1. TOC
{:toc}

</details>
</div>

# API Reference

Complete reference for Echo's logging, filtering, history, and tag APIs. For explanations and worked examples, start with the teaching pages; this page is for looking up exact capabilities.

---

## Functions

### Logging
{: .api-function-subsection-title .api-function-subsection-title-first }

<div class="api-method-entry" id="echo-debug">
  <div class="api-method-name">EchoDebug(message, [urgency], [tag], [colour])</div>
  <p class="api-method-summary">Logs a message at the chosen urgency and returns whether the current debug settings allowed it. If you set an allowed tag filter, untagged messages don&#x27;t pass the filter. This is intentional. The colour is stored as metadata. Echo itself doesn&#x27;t draw text. Echo Console uses the colour when showing structured history.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">message</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">The message to send to the debug logger</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">urgency <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">The level of urgency of the debug message (pick an entry from the <a href="#enum-e-echo-debug-urgency"><code>eEchoDebugUrgency</code></a> enum)</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">tag <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String|Array&lt;String&gt;</span>
      <span class="api-argument-description">Optional tag or tags to filter on (e.g., &quot;UI&quot;, [&quot;Physics&quot;,&quot;Jump&quot;]). Empty or empty array allows all.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">colour <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real|Undefined</span>
      <span class="api-argument-description">Optional text colour metadata for structured history / Echo Console display.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-debug-info">
  <div class="api-method-name">EchoDebugInfo(message, [tag], [colour])</div>
  <p class="api-method-summary">Logs an INFO message. Info messages are only shown when the debug level is <code>COMPLETE</code>.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">message</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">tag <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String|Array&lt;String&gt;</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">colour <span class="api-optional">optional</span></span>
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

<div class="api-method-entry" id="echo-debug-warn">
  <div class="api-method-name">EchoDebugWarn(message, [tag], [colour])</div>
  <p class="api-method-summary">Logs a WARNING message. Warning messages pass in <code>COMPREHENSIVE</code> and <code>COMPLETE</code>. In <code>COMPLETE</code>, warning messages include a stack trace.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">message</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">tag <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String|Array&lt;String&gt;</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">colour <span class="api-optional">optional</span></span>
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

<div class="api-method-entry" id="echo-debug-severe">
  <div class="api-method-name">EchoDebugSevere(message, [tag], [colour])</div>
  <p class="api-method-summary">Logs a SEVERE message and includes a stack trace. Severe messages pass in <code>SEVERE_ONLY</code>, <code>COMPREHENSIVE</code>, and <code>COMPLETE</code>. Severe messages include a stack trace to make the call site easier to identify.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">message</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">tag <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String|Array&lt;String&gt;</span>
      <span class="api-argument-description"></span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">colour <span class="api-optional">optional</span></span>
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

### Debug level
{: .api-function-subsection-title }

<div class="api-method-entry" id="echo-debug-set-level">
  <div class="api-method-name">EchoDebugSetLevel(level)</div>
  <p class="api-method-summary">Sets which message urgency levels Echo will log. Returns <code>false</code> if the value isn&#x27;t a valid debug level. This affects future logs only. It doesn&#x27;t delete old history.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">level</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">The level of logging (pick an entry from the <a href="#enum-e-echo-debug-level"><code>eEchoDebugLevel</code></a> enum)</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-debug-get-level">
  <div class="api-method-name">EchoDebugGetLevel([stringify])</div>
  <p class="api-method-summary">Returns the current <a href="#enum-e-echo-debug-level"><code>eEchoDebugLevel</code></a> value, or its name when _stringify is true.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">stringify <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether to return the debug level as a string, or as the plain real value.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Real|String|Bool</span>
      <span class="api-return-description">False if debug is disabled.</span>
    </div>
  </div>
</div>

### History and capture
{: .api-function-subsection-title }

<div class="api-method-entry" id="echo-debug-dump-log">
  <div class="api-method-name">EchoDebugDumpLog([raw])</div>
  <p class="api-method-summary">Writes debug history to a text file. By default this dumps filtered history; pass true to dump raw history instead. The file name starts with <code>echo_debug_dump-</code>. This dumps the formatted text history, not every internal structured field. Returns <code>false</code> if the file can&#x27;t be created.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">raw <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether to dump raw history instead of filtered history.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-debug-get-history"><code>EchoDebugGetHistory</code></a> <span aria-hidden="true">·</span> <a href="#echo-debug-set-raw-history-capture"><code>EchoDebugSetRawHistoryCapture</code></a> <span aria-hidden="true">·</span> <a href="#echo-debug-get-raw-history-capture"><code>EchoDebugGetRawHistoryCapture</code></a></div>
  </div>
</div>

<div class="api-method-entry" id="echo-debug-get-history-size">
  <div class="api-method-name">EchoDebugGetHistorySize()</div>
  <p class="api-method-summary">Returns the maximum number of entries kept in debug history. <code>0</code> means the history is unlimited.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Real|Bool</span>
      <span class="api-return-description">False if debug is disabled.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-debug-set-history-size">
  <div class="api-method-name">EchoDebugSetHistorySize(max)</div>
  <p class="api-method-summary">Sets how many entries debug history keeps. Use 0 for no limit. When the history is over the limit, Echo trims the oldest entries first.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">max</span>
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

<div class="api-method-entry" id="echo-debug-set-raw-history-capture">
  <div class="api-method-name">EchoDebugSetRawHistoryCapture(enabled)</div>
  <p class="api-method-summary">Enables or disables raw history capture for the Echo Console. Raw history remembers messages before the current level and tag filters decide whether they belong in the normal log. Echo Console can then search messages that were filtered out when they happened. Raw capture can still retain messages while the debug level is <code>NONE</code>. They don&#x27;t appear in the normal output or filtered history.</p>
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
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-debug-get-raw-history-capture">
  <div class="api-method-name">EchoDebugGetRawHistoryCapture()</div>
  <p class="api-method-summary">Returns whether raw history capture is enabled for the Echo Console.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Bool</span>
      <span class="api-return-description">False if debug is disabled.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-debug-clear-history">
  <div class="api-method-name">EchoDebugClearHistory()</div>
  <p class="api-method-summary">Clears all entries from the debug log history This clears the normal and raw histories, including both plain-text and structured entries.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Bool</span>
      <span class="api-return-description">False if debug is disabled, otherwise true after clearing.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-debug-get-history">
  <div class="api-method-name">EchoDebugGetHistory()</div>
  <p class="api-method-summary">Returns a copy of the current debug history.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Array&lt;String&gt;|Bool</span>
      <span class="api-return-description">False if debug is disabled.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-debug-get-revision">
  <div class="api-method-name">EchoDebugGetRevision()</div>
  <p class="api-method-summary">Returns the current filtered-history revision number. This revision tracks filtered history only; raw history has its own internal revision.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Real|Bool</span>
      <span class="api-return-description">False if debug is disabled.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-debug-get-structured-history">
  <div class="api-method-name">EchoDebugGetStructuredHistory()</div>
  <p class="api-method-summary">Returns a new array of structured history entries for UI rendering. A UI can use this to draw the message, urgency, tags, time, stack trace, or colour separately instead of parsing <a href="#echo-debug-get-history"><code>EchoDebugGetHistory()</code></a> strings.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row">
      <span class="api-return-type">Array&lt;Struct&gt;|Bool</span>
      <span class="api-return-description">False if debug is disabled.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-debug-get-history"><code>EchoDebugGetHistory</code></a> <span aria-hidden="true">·</span> <a href="#echo-debug-get-revision"><code>EchoDebugGetRevision</code></a></div>
  </div>
</div>

### Tags
{: .api-function-subsection-title }

<div class="api-method-entry" id="echo-debug-set-tags">
  <div class="api-method-name">EchoDebugSetTags(tags)</div>
  <p class="api-method-summary">Sets which tags are allowed to log. An empty array means &quot;allow all&quot;. If the allowed list isn&#x27;t empty, a log must share at least one tag with that list.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tags</span>
      <span class="api-argument-type">Array&lt;String&gt;</span>
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

<div class="api-method-entry" id="echo-debug-clear-tags">
  <div class="api-method-name">EchoDebugClearTags()</div>
  <p class="api-method-summary">Clears any tag filter so all tags are allowed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="echo-debug-get-tags">
  <div class="api-method-name">EchoDebugGetTags()</div>
  <p class="api-method-summary">Returns the current allowed tags. An empty array means all tags are allowed. Returns <code>false</code> when Echo is disabled.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array&lt;String&gt;|Bool</span>
    </div>
  </div>
</div>

## Enums

<div class="api-enum-entry" id="enum-e-echo-debug-level">
  <div class="api-enum-name">eEchoDebugLevel</div>
  <p>Controls which messages pass into Echo&#x27;s normal output and filtered history. Raw capture is separate and can remember messages before this filter is applied.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">NONE</span>
      <span class="api-enum-description">Nothing passes into normal output or filtered history.</span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">SEVERE_ONLY</span>
      <span class="api-enum-description">Only severe messages pass.</span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">COMPREHENSIVE</span>
      <span class="api-enum-description">Warnings and severe messages pass. This is the default.</span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">COMPLETE</span>
      <span class="api-enum-description">Info, warning, and severe messages pass.</span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">NUM</span>
      <span class="api-enum-description">Enum sentinel used internally for validation. Don&#x27;t use it as a debug level.</span>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-echo-debug-urgency">
  <div class="api-enum-name">eEchoDebugUrgency</div>
  <p>Describes how important one message is.</p>
  <div class="api-enum-members">
    <div class="api-enum-row">
      <span class="api-enum-member">INFO</span>
      <span class="api-enum-description">Normal information.</span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">WARNING</span>
      <span class="api-enum-description">Something looks wrong, but the game can probably continue.</span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">SEVERE</span>
      <span class="api-enum-description">Something is broken enough that you should investigate it immediately.</span>
    </div>
    <div class="api-enum-row">
      <span class="api-enum-member">NUM</span>
      <span class="api-enum-description">Enum sentinel used internally for validation. Don&#x27;t use it as a message urgency.</span>
    </div>
  </div>
</div>

## Macros

### Version
{: .api-function-subsection-title .api-function-subsection-title-first }

<div class="api-method-entry api-macro-entry api-macro-metadata" id="macro-echo-version">
  <div class="api-method-name">ECHO_VERSION</div>
  <p class="api-method-summary">Current Echo source version string.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Value</div>
    <pre class="api-example"><code>&quot;3.0.0&quot;</code></pre>
  </div>
</div>

### Debug setup
{: .api-function-subsection-title }

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-echo-debug-enabled">
  <div class="api-method-name">ECHO_DEBUG_ENABLED</div>
  <p class="api-method-summary">Compile-time Echo debug on/off switch. When set to 0, public <a href="#echo-debug"><code>EchoDebug</code></a>* calls return false. Use <a href="#echo-debug-set-level"><code>EchoDebugSetLevel()</code></a> when you need to change logging verbosity at runtime.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>1</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#echo-debug-set-level"><code>EchoDebugSetLevel</code></a> <span aria-hidden="true">·</span> <a href="#enum-e-echo-debug-level"><code>eEchoDebugLevel</code></a></div>
  </div>
</div>

## Symbol index

<div class="api-symbol-index">
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">E</div>
    <div class="api-symbol-row"><a href="#echo-debug"><code>EchoDebug()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-clear-history"><code>EchoDebugClearHistory()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-clear-tags"><code>EchoDebugClearTags()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-dump-log"><code>EchoDebugDumpLog()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-get-history"><code>EchoDebugGetHistory()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-get-history-size"><code>EchoDebugGetHistorySize()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-get-level"><code>EchoDebugGetLevel()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-get-raw-history-capture"><code>EchoDebugGetRawHistoryCapture()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-get-revision"><code>EchoDebugGetRevision()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-get-structured-history"><code>EchoDebugGetStructuredHistory()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-get-tags"><code>EchoDebugGetTags()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-info"><code>EchoDebugInfo()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-set-history-size"><code>EchoDebugSetHistorySize()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-set-level"><code>EchoDebugSetLevel()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-set-raw-history-capture"><code>EchoDebugSetRawHistoryCapture()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-set-tags"><code>EchoDebugSetTags()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-severe"><code>EchoDebugSevere()</code></a></div>
    <div class="api-symbol-row"><a href="#echo-debug-warn"><code>EchoDebugWarn()</code></a></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">Enums</div>
    <div class="api-symbol-row"><a href="#enum-e-echo-debug-level"><code>eEchoDebugLevel</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-echo-debug-urgency"><code>eEchoDebugUrgency</code></a><span class="api-symbol-owner">enum</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">Macros</div>
    <div class="api-symbol-row"><a href="#macro-echo-debug-enabled"><code>ECHO_DEBUG_ENABLED</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-echo-version"><code>ECHO_VERSION</code></a><span class="api-symbol-owner">macro</span></div>
  </div>
</div>
