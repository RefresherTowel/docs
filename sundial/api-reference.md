---
layout: "default"
title: "API Reference"
parent: "Sundial"
nav_order: 6
library_id: "sundial"
doc_version: "current"
api_reference: true
---

<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. -->
<!-- Source: GML JSDoc + sundial.yml -->

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>

1. TOC
{:toc}

</details>
</div>

# API Reference

Complete reference for Sundial's grading, time, mask and callback API. For explanations and worked examples, start with the teaching pages; this page is for looking up exact methods, arguments, return values and enum members.

---

## Sundial

### Sundial
{: #sundial .api-type-title }

Creates a lightweight time-of-day colour grader with configurable phase colours, strengths, brightness, and cycle timing.

```gml
new Sundial()
```

#### Methods

<div class="api-method-group-title">Grading</div>
<table class="api-methods"><tbody>
<tr><td><a href="#sundial-set-grading"><code>SetGrading()</code></a></td><td>Sets the grading colour for one time-of-day stage.</td></tr>
<tr><td><a href="#sundial-set-grading-strength"><code>SetGradingStrength()</code></a></td><td>Sets how strongly one time-of-day stage biases scene colour.</td></tr>
<tr><td><a href="#sundial-set-brightness"><code>SetBrightness()</code></a></td><td>Sets full-day and full-night brightness used by the continuous daylight blend.</td></tr>
</tbody></table>

<div class="api-method-group-title">Indoor and outdoor masking</div>
<table class="api-methods"><tbody>
<tr><td><a href="#sundial-set-indoor-grading"><code>SetIndoorGrading()</code></a></td><td>Sets the neutral indoor grading colour used before outdoor time-of-day influence is applied.</td></tr>
<tr><td><a href="#sundial-set-indoor-grading-strength"><code>SetIndoorGradingStrength()</code></a></td><td>Sets how strongly the indoor base colour biases indoor pixels.</td></tr>
<tr><td><a href="#sundial-set-indoor-daylight-influence"><code>SetIndoorDaylightInfluence()</code></a></td><td>Sets how much of the resolved outdoor time-of-day colour is inherited by indoor pixels.</td></tr>
<tr><td><a href="#sundial-set-indoor-brightness"><code>SetIndoorBrightness()</code></a></td><td>Sets full-day and full-night brightness used for masked indoor pixels.</td></tr>
<tr><td><a href="#sundial-set-mask"><code>SetMask()</code></a></td><td>Sets the red-channel mask used to blend indoor and outdoor grading. White is masked indoor and black is unmasked outdoor.</td></tr>
<tr><td><a href="#sundial-clear-mask"><code>ClearMask()</code></a></td><td>Removes the current indoor/outdoor mask so the outdoor grade applies to the entire source surface.</td></tr>
<tr><td><a href="#sundial-has-mask"><code>HasMask()</code></a></td><td>Reports whether the currently configured mask surface still exists.</td></tr>
<tr><td><a href="#sundial-get-mask"><code>GetMask()</code></a></td><td>Returns the configured mask surface handle.</td></tr>
</tbody></table>

<div class="api-method-group-title">Time and clock</div>
<table class="api-methods"><tbody>
<tr><td><a href="#sundial-set-time-of-day"><code>SetTimeOfDay()</code></a></td><td>Sets the current normalized cycle position. Values outside 0..1 wrap around the cycle while 1 is preserved as the cycle endpoint.</td></tr>
<tr><td><a href="#sundial-get-time-of-day"><code>GetTimeOfDay()</code></a></td><td>Returns the current normalized position in the full daylight cycle.</td></tr>
<tr><td><a href="#sundial-set-day-percent"><code>SetDayPercent()</code></a></td><td>Sets the normalized 0..1 day position. This is an alias for SetTimeOfDay().</td></tr>
<tr><td><a href="#sundial-get-day-percent"><code>GetDayPercent()</code></a></td><td>Returns the normalized 0..1 day position. This is an alias for GetTimeOfDay().</td></tr>
<tr><td><a href="#sundial-set-morning-time"><code>SetMorningTime()</code></a></td><td>Sets the 24-hour clock time represented by the Morning node at normalized cycle position zero.</td></tr>
<tr><td><a href="#sundial-get-morning-time"><code>GetMorningTime()</code></a></td><td>Returns the decimal 24-hour clock time represented by the Morning node.</td></tr>
<tr><td><a href="#sundial-set-time"><code>SetTime()</code></a></td><td>Jumps to a decimal 24-hour clock time without changing Auto Time state.</td></tr>
<tr><td><a href="#sundial-get-time"><code>GetTime()</code></a></td><td>Returns the current decimal 24-hour clock time.</td></tr>
<tr><td><a href="#sundial-get-hour"><code>GetHour()</code></a></td><td>Returns the hour component of the current 24-hour clock time.</td></tr>
<tr><td><a href="#sundial-get-minute"><code>GetMinute()</code></a></td><td>Returns the minute component of the current 24-hour clock time.</td></tr>
<tr><td><a href="#sundial-set-cycle-timing"><code>SetCycleTiming()</code></a></td><td>Configures normalized phase timing for the full 0..1 daylight cycle.</td></tr>
</tbody></table>

<div class="api-method-group-title">Automatic progression</div>
<table class="api-methods"><tbody>
<tr><td><a href="#sundial-set-auto-time"><code>SetAutoTime()</code></a></td><td>Enables or disables automatic forward time progression.</td></tr>
<tr><td><a href="#sundial-get-auto-time"><code>GetAutoTime()</code></a></td><td>Returns whether automatic time progression is enabled.</td></tr>
<tr><td><a href="#sundial-set-day-length"><code>SetDayLength()</code></a></td><td>Sets the real-world seconds required for one complete game day.</td></tr>
<tr><td><a href="#sundial-get-day-length"><code>GetDayLength()</code></a></td><td>Returns the real-world seconds required for one complete game day.</td></tr>
<tr><td><a href="#sundial-set-speed"><code>SetSpeed()</code></a></td><td>Sets game seconds advanced per real-world second. Zero pauses progression without disabling Auto Time.</td></tr>
<tr><td><a href="#sundial-get-speed"><code>GetSpeed()</code></a></td><td>Returns the current automatic time speed in game seconds per real-world second.</td></tr>
<tr><td><a href="#sundial-update"><code>Update()</code></a></td><td>Synchronizes automatic time immediately. Optional for advanced gameplay logic because Draw() and time queries also synchronize.</td></tr>
</tbody></table>

<div class="api-method-group-title">Periods and callbacks</div>
<table class="api-methods"><tbody>
<tr><td><a href="#sundial-get-period"><code>GetPeriod()</code></a></td><td>Returns the currently active authored time-of-day period.</td></tr>
<tr><td><a href="#sundial-on-period-changed"><code>OnPeriodChanged()</code></a></td><td>Adds a callback that runs whenever <a href="#sundial"><code>Sundial</code></a> enters a different semantic period.</td></tr>
<tr><td><a href="#sundial-on-period"><code>OnPeriod()</code></a></td><td>Adds a callback that runs whenever <a href="#sundial"><code>Sundial</code></a> enters one specific semantic period.</td></tr>
<tr><td><a href="#sundial-on-morning"><code>OnMorning()</code></a></td><td>Adds a callback that runs whenever <a href="#sundial"><code>Sundial</code></a> enters Morning.</td></tr>
<tr><td><a href="#sundial-on-day"><code>OnDay()</code></a></td><td>Adds a callback that runs whenever <a href="#sundial"><code>Sundial</code></a> enters Day.</td></tr>
<tr><td><a href="#sundial-on-afternoon"><code>OnAfternoon()</code></a></td><td>Adds a callback that runs whenever <a href="#sundial"><code>Sundial</code></a> enters Afternoon.</td></tr>
<tr><td><a href="#sundial-on-dusk"><code>OnDusk()</code></a></td><td>Adds a callback that runs whenever <a href="#sundial"><code>Sundial</code></a> enters Dusk.</td></tr>
<tr><td><a href="#sundial-on-night"><code>OnNight()</code></a></td><td>Adds a callback that runs whenever <a href="#sundial"><code>Sundial</code></a> enters Night.</td></tr>
<tr><td><a href="#sundial-on-dawn"><code>OnDawn()</code></a></td><td>Adds a callback that runs whenever <a href="#sundial"><code>Sundial</code></a> enters Dawn.</td></tr>
</tbody></table>

<div class="api-method-group-title">Resolver information</div>
<table class="api-methods"><tbody>
<tr><td><a href="#sundial-get-sunlight-amount"><code>GetSunlightAmount()</code></a></td><td>Returns the current continuous daylight amount used by brightness blending.</td></tr>
<tr><td><a href="#sundial-get-phase"><code>GetPhase()</code></a></td><td>Returns the currently dominant temporal phase.</td></tr>
<tr><td><a href="#sundial-get-phase-name"><code>GetPhaseName()</code></a></td><td>Returns a readable lowercase name for the currently dominant temporal phase.</td></tr>
</tbody></table>

<div class="api-method-group-title">Drawing</div>
<table class="api-methods"><tbody>
<tr><td><a href="#sundial-draw"><code>Draw()</code></a></td><td>Draws one source surface through the current daylight grade onto the active render target.</td></tr>
</tbody></table>

<div class="api-method-entry" id="sundial-set-grading">
  <div class="api-method-name">SetGrading(stage, colour)</div>
  <p class="api-method-summary">Sets the grading colour for one time-of-day stage.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">stage</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-sundial"><code>eSundial</code></a> enum.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">colour</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">GameMaker colour used to bias this stage.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-grading-strength">
  <div class="api-method-name">SetGradingStrength(stage, strength)</div>
  <p class="api-method-summary">Sets how strongly one time-of-day stage biases scene colour.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">stage</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-sundial"><code>eSundial</code></a> enum.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">strength</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Non-negative grading strength. Values above 1 deliberately exaggerate the tint.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-brightness">
  <div class="api-method-name">SetBrightness(day_brightness, night_brightness)</div>
  <p class="api-method-summary">Sets full-day and full-night brightness used by the continuous daylight blend.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">day_brightness</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Brightness multiplier at full daylight.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">night_brightness</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Brightness multiplier at full night.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-indoor-grading">
  <div class="api-method-name">SetIndoorGrading(colour)</div>
  <p class="api-method-summary">Sets the neutral indoor grading colour used before outdoor time-of-day influence is applied.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">colour</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">GameMaker colour used as the indoor base grade.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-indoor-grading-strength">
  <div class="api-method-name">SetIndoorGradingStrength(strength)</div>
  <p class="api-method-summary">Sets how strongly the indoor base colour biases indoor pixels.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">strength</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Non-negative grading strength. Values above 1 deliberately exaggerate the tint.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-indoor-daylight-influence">
  <div class="api-method-name">SetIndoorDaylightInfluence(amount)</div>
  <p class="api-method-summary">Sets how much of the resolved outdoor time-of-day colour is inherited by indoor pixels.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">amount</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Outdoor grading influence from 0 for none to 1 for full inheritance.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-indoor-brightness">
  <div class="api-method-name">SetIndoorBrightness(day_brightness, night_brightness)</div>
  <p class="api-method-summary">Sets full-day and full-night brightness used for masked indoor pixels.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">day_brightness</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Indoor brightness multiplier at full daylight.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">night_brightness</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Indoor brightness multiplier at full night.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-mask">
  <div class="api-method-name">SetMask(mask_surface)</div>
  <p class="api-method-summary">Sets the red-channel mask used to blend indoor and outdoor grading. White is masked indoor and black is unmasked outdoor.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">mask_surface</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Surface whose red channel defines indoor mask influence. It must match the source surface dimensions passed to Draw().</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Extra notes</div>
    <div class="api-extra-notes">
      <p>The mask surface must match the source surface dimensions used by Draw(). Only the red channel is read; black is outdoor and white is indoor.</p>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#sundial-clear-mask"><code>Sundial.ClearMask</code></a> <span aria-hidden="true">·</span> <a href="#sundial-has-mask"><code>Sundial.HasMask</code></a> <span aria-hidden="true">·</span> <a href="#sundial-get-mask"><code>Sundial.GetMask</code></a></div>
  </div>
</div>

<div class="api-method-entry" id="sundial-clear-mask">
  <div class="api-method-name">ClearMask()</div>
  <p class="api-method-summary">Removes the current indoor/outdoor mask so the outdoor grade applies to the entire source surface.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-has-mask">
  <div class="api-method-name">HasMask()</div>
  <p class="api-method-summary">Reports whether the currently configured mask surface still exists.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-mask">
  <div class="api-method-name">GetMask()</div>
  <p class="api-method-summary">Returns the configured mask surface handle.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-time-of-day">
  <div class="api-method-name">GetTimeOfDay()</div>
  <p class="api-method-summary">Returns the current normalized position in the full daylight cycle.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-sunlight-amount">
  <div class="api-method-name">GetSunlightAmount()</div>
  <p class="api-method-summary">Returns the current continuous daylight amount used by brightness blending.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-phase">
  <div class="api-method-name">GetPhase()</div>
  <p class="api-method-summary">Returns the currently dominant temporal phase.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-phase-name">
  <div class="api-method-name">GetPhaseName()</div>
  <p class="api-method-summary">Returns a readable lowercase name for the currently dominant temporal phase.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-cycle-timing">
  <div class="api-method-name">SetCycleTiming(day_fraction, morning_duration, afternoon_start, sunset_duration, twilight_duration, predawn_duration)</div>
  <p class="api-method-summary">Configures normalized phase timing for the full 0..1 daylight cycle.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">day_fraction</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Cycle position where daytime ends and twilight begins.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">morning_duration</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Full-cycle duration over which morning fades into day.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">afternoon_start</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Full-cycle position where afternoon begins blending in.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">sunset_duration</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Full-cycle duration before day end used for the sunset blend.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">twilight_duration</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Full-cycle duration after day end used for twilight.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">predawn_duration</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Full-cycle duration before cycle end used for predawn.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-time-of-day">
  <div class="api-method-name">SetTimeOfDay(time_of_day)</div>
  <p class="api-method-summary">Sets the current normalized cycle position. Values outside 0..1 wrap around the cycle while 1 is preserved as the cycle endpoint.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">time_of_day</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Normalized cycle position, where 0 and 1 meet at morning.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-auto-time">
  <div class="api-method-name">SetAutoTime(enabled)</div>
  <p class="api-method-summary">Enables or disables automatic forward time progression.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">enabled</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether <a href="#sundial"><code>Sundial</code></a> should advance automatically from elapsed real time.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-auto-time">
  <div class="api-method-name">GetAutoTime()</div>
  <p class="api-method-summary">Returns whether automatic time progression is enabled.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-day-length">
  <div class="api-method-name">SetDayLength(seconds)</div>
  <p class="api-method-summary">Sets the real-world seconds required for one complete game day.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">seconds</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Positive number of real-world seconds per complete game day.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-day-length">
  <div class="api-method-name">GetDayLength()</div>
  <p class="api-method-summary">Returns the real-world seconds required for one complete game day.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-speed">
  <div class="api-method-name">SetSpeed(speed)</div>
  <p class="api-method-summary">Sets game seconds advanced per real-world second. Zero pauses progression without disabling Auto Time.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">speed</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Non-negative game seconds advanced per real-world second.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-speed">
  <div class="api-method-name">GetSpeed()</div>
  <p class="api-method-summary">Returns the current automatic time speed in game seconds per real-world second.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-day-percent">
  <div class="api-method-name">SetDayPercent(percent)</div>
  <p class="api-method-summary">Sets the normalized 0..1 day position. This is an alias for SetTimeOfDay().</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">percent</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Normalized cycle position.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-day-percent">
  <div class="api-method-name">GetDayPercent()</div>
  <p class="api-method-summary">Returns the normalized 0..1 day position. This is an alias for GetTimeOfDay().</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-morning-time">
  <div class="api-method-name">SetMorningTime(hour)</div>
  <p class="api-method-summary">Sets the 24-hour clock time represented by the Morning node at normalized cycle position zero.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">hour</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Decimal 24-hour clock time to use for Morning. Values wrap around 24 hours.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-morning-time">
  <div class="api-method-name">GetMorningTime()</div>
  <p class="api-method-summary">Returns the decimal 24-hour clock time represented by the Morning node.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-time">
  <div class="api-method-name">SetTime(hour)</div>
  <p class="api-method-summary">Jumps to a decimal 24-hour clock time without changing Auto Time state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">hour</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Decimal 24-hour clock time. Values wrap around 24 hours.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Example</div>
    <pre class="api-example"><code>sundial.SetTime(18.5); // 18:30</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#sundial-get-time"><code>Sundial.GetTime</code></a> <span aria-hidden="true">·</span> <a href="#sundial-set-morning-time"><code>Sundial.SetMorningTime</code></a> <span aria-hidden="true">·</span> <a href="#sundial-set-time-of-day"><code>Sundial.SetTimeOfDay</code></a></div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-time">
  <div class="api-method-name">GetTime()</div>
  <p class="api-method-summary">Returns the current decimal 24-hour clock time.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-hour">
  <div class="api-method-name">GetHour()</div>
  <p class="api-method-summary">Returns the hour component of the current 24-hour clock time.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-minute">
  <div class="api-method-name">GetMinute()</div>
  <p class="api-method-summary">Returns the minute component of the current 24-hour clock time.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-period">
  <div class="api-method-name">GetPeriod()</div>
  <p class="api-method-summary">Returns the currently active authored time-of-day period.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-on-period-changed">
  <div class="api-method-name">OnPeriodChanged(callback)</div>
  <p class="api-method-summary">Adds a callback that runs whenever <a href="#sundial"><code>Sundial</code></a> enters a different semantic period.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Callback receiving the previous and new <a href="#enum-e-sundial-period"><code>eSundialPeriod</code></a> values.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Example</div>
    <pre class="api-example"><code>sundial.OnPeriodChanged(function(_from, _to) {
    global.current_period = _to;
});</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#sundial-on-period"><code>Sundial.OnPeriod</code></a> <span aria-hidden="true">·</span> <a href="#enum-e-sundial-period"><code>eSundialPeriod</code></a></div>
  </div>
</div>

<div class="api-method-entry" id="sundial-on-period">
  <div class="api-method-name">OnPeriod(period, callback)</div>
  <p class="api-method-summary">Adds a callback that runs whenever <a href="#sundial"><code>Sundial</code></a> enters one specific semantic period.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">period</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Target <a href="#enum-e-sundial-period"><code>eSundialPeriod</code></a> value.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Callback invoked when that period is entered.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-on-morning">
  <div class="api-method-name">OnMorning(callback)</div>
  <p class="api-method-summary">Adds a callback that runs whenever <a href="#sundial"><code>Sundial</code></a> enters Morning.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Callback invoked when Morning begins.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-on-day">
  <div class="api-method-name">OnDay(callback)</div>
  <p class="api-method-summary">Adds a callback that runs whenever <a href="#sundial"><code>Sundial</code></a> enters Day.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Callback invoked when Day begins.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-on-afternoon">
  <div class="api-method-name">OnAfternoon(callback)</div>
  <p class="api-method-summary">Adds a callback that runs whenever <a href="#sundial"><code>Sundial</code></a> enters Afternoon.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Callback invoked when Afternoon begins.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-on-dusk">
  <div class="api-method-name">OnDusk(callback)</div>
  <p class="api-method-summary">Adds a callback that runs whenever <a href="#sundial"><code>Sundial</code></a> enters Dusk.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Callback invoked when Dusk begins.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-on-night">
  <div class="api-method-name">OnNight(callback)</div>
  <p class="api-method-summary">Adds a callback that runs whenever <a href="#sundial"><code>Sundial</code></a> enters Night.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Callback invoked when Night begins.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-on-dawn">
  <div class="api-method-name">OnDawn(callback)</div>
  <p class="api-method-summary">Adds a callback that runs whenever <a href="#sundial"><code>Sundial</code></a> enters Dawn.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Callback invoked when Dawn begins.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-update">
  <div class="api-method-name">Update()</div>
  <p class="api-method-summary">Synchronizes automatic time immediately. Optional for advanced gameplay logic because Draw() and time queries also synchronize.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-draw">
  <div class="api-method-name">Draw(source_surface, [x], [y], [width], [height])</div>
  <p class="api-method-summary">Draws one source surface through the current daylight grade onto the active render target.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source_surface</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Surface containing the scene to grade.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">x <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Destination x position on the active render target.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">y <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Destination y position on the active render target.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">width <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Destination width. Defaults to the source surface width.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">height <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Destination height. Defaults to the source surface height.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Example</div>
    <pre class="api-example"><code>sundial.Draw(application_surface);

// Or choose the destination rectangle explicitly.
sundial.Draw(application_surface, 0, 0, 1280, 720);</code></pre>
  </div>
</div>

## Top-level functions

<div class="api-method-entry" id="sundial-import">
  <div class="api-method-name">SundialImport([preset_name])</div>
  <p class="api-method-summary">Creates a <a href="#sundial"><code>Sundial</code></a> configured from the IDE-authored compiled runtime data.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">preset_name <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Exact preset name. Omit to use the authored default.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Example</div>
    <pre class="api-example"><code>sundial = SundialImport();

// Or load one named preset.
winter_sundial = SundialImport(&quot;Winter&quot;);</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#sundial"><code>Sundial</code></a></div>
  </div>
</div>

## Enums

### Grading
{: .api-function-subsection-title .api-function-subsection-title-first }

<div class="api-enum-entry" id="enum-e-sundial">
  <div class="api-enum-name">eSundial</div>
  <p class="api-enum-summary">The six authored grading anchors <a href="#sundial"><code>Sundial</code></a> blends through over one full day.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row">
        <span class="api-enum-member">MORNING</span>
        <span class="api-enum-description">Morning grading anchor.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">DAY</span>
        <span class="api-enum-description">Day grading anchor.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">AFTERNOON</span>
        <span class="api-enum-description">Afternoon grading anchor.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">DUSK</span>
        <span class="api-enum-description">Dusk grading anchor. <a href="#sundial"><code>Sundial</code></a>&#x27;s internal Sunset and Twilight phases both resolve through this authored grade.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">NIGHT</span>
        <span class="api-enum-description">Night grading anchor.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">DAWN</span>
        <span class="api-enum-description">Dawn grading anchor used during the later part of Predawn.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">NUM</span>
        <span class="api-enum-description">Sentinel/count value.</span>
      </div>
    </div>
  </div>
</div>

### Time
{: .api-function-subsection-title }

<div class="api-enum-entry" id="enum-e-sundial-period">
  <div class="api-enum-name">eSundialPeriod</div>
  <p class="api-enum-summary">The six semantic schedule periods used by GetPeriod() and period callbacks.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row">
        <span class="api-enum-member">MORNING</span>
        <span class="api-enum-description">Morning period beginning at the normalized cycle seam.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">DAY</span>
        <span class="api-enum-description">Day period.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">AFTERNOON</span>
        <span class="api-enum-description">Afternoon period.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">DUSK</span>
        <span class="api-enum-description">Dusk period.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">NIGHT</span>
        <span class="api-enum-description">Night period.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">DAWN</span>
        <span class="api-enum-description">Dawn period.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">NUM</span>
        <span class="api-enum-description">Sentinel/count value.</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-sundial-phase">
  <div class="api-enum-name">eSundialPhase</div>
  <p class="api-enum-summary">The more detailed internal temporal phases used by <a href="#sundial"><code>Sundial</code></a>&#x27;s continuous visual resolver.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row">
        <span class="api-enum-member">MORNING</span>
        <span class="api-enum-description">Morning is the dominant resolver phase.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">DAY</span>
        <span class="api-enum-description">Day is the dominant resolver phase.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">AFTERNOON</span>
        <span class="api-enum-description">Afternoon is the dominant resolver phase.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">SUNSET</span>
        <span class="api-enum-description">Sunset is the dominant resolver phase and contributes to the authored Dusk grade.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">TWILIGHT</span>
        <span class="api-enum-description">Twilight is the dominant resolver phase and contributes to the authored Dusk grade.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">NIGHT</span>
        <span class="api-enum-description">Night is the dominant resolver phase.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">PREDAWN</span>
        <span class="api-enum-description">Predawn is the dominant resolver phase and hands the grade from Night through Dawn toward Morning.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">NUM</span>
        <span class="api-enum-description">Sentinel/count value.</span>
      </div>
    </div>
  </div>
</div>

## Symbol index

<div class="api-symbol-index">
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">C</div>
    <div class="api-symbol-row"><a href="#sundial-clear-mask"><code>ClearMask()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">D</div>
    <div class="api-symbol-row"><a href="#sundial-draw"><code>Draw()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">G</div>
    <div class="api-symbol-row"><a href="#sundial-get-auto-time"><code>GetAutoTime()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-get-day-length"><code>GetDayLength()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-get-day-percent"><code>GetDayPercent()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-get-hour"><code>GetHour()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-get-mask"><code>GetMask()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-get-minute"><code>GetMinute()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-get-morning-time"><code>GetMorningTime()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-get-period"><code>GetPeriod()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-get-phase"><code>GetPhase()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-get-phase-name"><code>GetPhaseName()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-get-speed"><code>GetSpeed()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-get-sunlight-amount"><code>GetSunlightAmount()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-get-time"><code>GetTime()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-get-time-of-day"><code>GetTimeOfDay()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">H</div>
    <div class="api-symbol-row"><a href="#sundial-has-mask"><code>HasMask()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">O</div>
    <div class="api-symbol-row"><a href="#sundial-on-afternoon"><code>OnAfternoon()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-on-dawn"><code>OnDawn()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-on-day"><code>OnDay()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-on-dusk"><code>OnDusk()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-on-morning"><code>OnMorning()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-on-night"><code>OnNight()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-on-period"><code>OnPeriod()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-on-period-changed"><code>OnPeriodChanged()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">S</div>
    <div class="api-symbol-row"><a href="#sundial-set-auto-time"><code>SetAutoTime()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-brightness"><code>SetBrightness()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-cycle-timing"><code>SetCycleTiming()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-day-length"><code>SetDayLength()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-day-percent"><code>SetDayPercent()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-grading"><code>SetGrading()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-grading-strength"><code>SetGradingStrength()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-indoor-brightness"><code>SetIndoorBrightness()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-indoor-daylight-influence"><code>SetIndoorDaylightInfluence()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-indoor-grading"><code>SetIndoorGrading()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-indoor-grading-strength"><code>SetIndoorGradingStrength()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-mask"><code>SetMask()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-morning-time"><code>SetMorningTime()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-speed"><code>SetSpeed()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-time"><code>SetTime()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-time-of-day"><code>SetTimeOfDay()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial"><code>Sundial</code></a></div>
    <div class="api-symbol-row"><a href="#sundial-import"><code>SundialImport()</code></a></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">U</div>
    <div class="api-symbol-row"><a href="#sundial-update"><code>Update()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">Enums</div>
    <div class="api-symbol-row"><a href="#enum-e-sundial"><code>eSundial</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-sundial-period"><code>eSundialPeriod</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-sundial-phase"><code>eSundialPhase</code></a><span class="api-symbol-owner">enum</span></div>
  </div>
</div>
