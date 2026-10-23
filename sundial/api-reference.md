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

A list of Sundial's functions and settings, including what each argument does and what each function returns. If you're new to Sundial, the other pages walk you through using it in your game.

---

## Sundial

### Sundial
{: #sundial .api-type-title }

Creates a <a href="#sundial"><code>Sundial</code></a> with default colours, brightness and day/night timings. It starts at Morning with Auto Time turned off. By default, it takes over drawing the application surface until CleanUp() is called.

```gml
new Sundial(manage_application_surface)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">manage_application_surface <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">True to disable GameMaker&#x27;s automatic application-surface drawing so Draw() can present the graded game. False to leave your renderer&#x27;s setting untouched. Defaults to true. Creating a second managing <a href="#sundial"><code>Sundial</code></a> before CleanUp() on the first causes an error.</span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Grading</div>
<table class="api-methods"><tbody>
<tr><td><a href="#sundial-set-grading"><code>SetGrading()</code></a></td><td>Changes the grading colour for one of the six parts of the day.</td></tr>
<tr><td><a href="#sundial-set-grading-strength"><code>SetGradingStrength()</code></a></td><td>Changes how strongly a grading colour affects the scene.</td></tr>
<tr><td><a href="#sundial-set-brightness"><code>SetBrightness()</code></a></td><td>Sets how bright the outdoor scene should be during the day and at night. <a href="#sundial"><code>Sundial</code></a> changes the brightness smoothly between the two.</td></tr>
</tbody></table>

<div class="api-method-group-title">Indoor and outdoor</div>
<table class="api-methods"><tbody>
<tr><td><a href="#sundial-set-indoor-grading"><code>SetIndoorGrading()</code></a></td><td>Sets the base colour used for indoor areas. The indoor mask decides which parts of the scene this affects.</td></tr>
<tr><td><a href="#sundial-set-indoor-grading-strength"><code>SetIndoorGradingStrength()</code></a></td><td>Changes how strongly the indoor grading colour affects the scene.</td></tr>
<tr><td><a href="#sundial-set-indoor-daylight-influence"><code>SetIndoorDaylightInfluence()</code></a></td><td>Controls how much of the outdoor grading colour reaches indoor areas. This changes colour, not brightness.</td></tr>
<tr><td><a href="#sundial-set-indoor-brightness"><code>SetIndoorBrightness()</code></a></td><td>Sets separate day and night brightness for indoor areas. <a href="#sundial"><code>Sundial</code></a> blends between them as the day passes.</td></tr>
<tr><td><a href="#sundial-set-mask"><code>SetMask()</code></a></td><td>Uses a surface to decide which parts of the scene are indoors. Black means outdoors, white means indoors, and grey blends the two. The mask can be any size. It will be stretched to fit the scene.</td></tr>
<tr><td><a href="#sundial-set-mask-sprite"><code>SetMaskSprite()</code></a></td><td>Uses a sprite instead of a surface for the indoor mask. Black means outdoors, white means indoors, and grey blends the two. The sprite is stretched to fit the scene.</td></tr>
<tr><td><a href="#sundial-clear-mask"><code>ClearMask()</code></a></td><td>Removes the indoor mask. The whole scene will use the outdoor grading again.</td></tr>
<tr><td><a href="#sundial-has-mask"><code>HasMask()</code></a></td><td>Checks whether the mask you supplied still exists, whether it is a surface or a sprite.</td></tr>
<tr><td><a href="#sundial-get-mask"><code>GetMask()</code></a></td><td>Gets the surface or sprite currently being used as the indoor mask. Use HasMask() to check whether it still exists.</td></tr>
</tbody></table>

<div class="api-method-group-title">Time and clock</div>
<table class="api-methods"><tbody>
<tr><td><a href="#sundial-set-time-of-day"><code>SetTimeOfDay()</code></a></td><td>Moves <a href="#sundial"><code>Sundial</code></a> to a position in the day from 0 to 1. Values outside that range wrap around. If a manual jump changes the period, only the new period&#x27;s callbacks run.</td></tr>
<tr><td><a href="#sundial-get-time-of-day"><code>GetTimeOfDay()</code></a></td><td>Gets the current position in the day as a number from 0 to 1, where 0 is Morning and 1 is the end of the day.</td></tr>
<tr><td><a href="#sundial-set-day-percent"><code>SetDayPercent()</code></a></td><td>Another name for SetTimeOfDay(). Sets how far through the day <a href="#sundial"><code>Sundial</code></a> is, using a number from 0 to 1.</td></tr>
<tr><td><a href="#sundial-get-day-percent"><code>GetDayPercent()</code></a></td><td>Another name for GetTimeOfDay(). Gets how far through the day <a href="#sundial"><code>Sundial</code></a> is.</td></tr>
<tr><td><a href="#sundial-set-morning-time"><code>SetMorningTime()</code></a></td><td>Sets what time on the 24-hour clock Morning begins. This changes the clock, not the length of the day or the grading.</td></tr>
<tr><td><a href="#sundial-get-morning-time"><code>GetMorningTime()</code></a></td><td>Gets the 24-hour clock time when Morning begins.</td></tr>
<tr><td><a href="#sundial-set-time"><code>SetTime()</code></a></td><td>Moves <a href="#sundial"><code>Sundial</code></a> to a particular time on the 24-hour clock. This does not turn Auto Time on or off, and skipped periods do not get their callbacks run.</td></tr>
<tr><td><a href="#sundial-get-time"><code>GetTime()</code></a></td><td>Gets the current time on <a href="#sundial"><code>Sundial</code></a>&#x27;s 24-hour clock.</td></tr>
<tr><td><a href="#sundial-get-hour"><code>GetHour()</code></a></td><td>Gets the hour from <a href="#sundial"><code>Sundial</code></a>&#x27;s current clock time.</td></tr>
<tr><td><a href="#sundial-get-minute"><code>GetMinute()</code></a></td><td>Gets the minute from <a href="#sundial"><code>Sundial</code></a>&#x27;s current clock time.</td></tr>
<tr><td><a href="#sundial-set-cycle-timing"><code>SetCycleTiming()</code></a></td><td>Changes when the different parts of the day start and how long the colour changes between them take. All six values use a fraction of the day from 0 to 1. Invalid ordering causes a fatal error.</td></tr>
</tbody></table>

<div class="api-method-group-title">Automatic time</div>
<table class="api-methods"><tbody>
<tr><td><a href="#sundial-set-auto-time"><code>SetAutoTime()</code></a></td><td>Turns automatic time on or off. When enabled, <a href="#sundial"><code>Sundial</code></a> advances its clock using elapsed real time.</td></tr>
<tr><td><a href="#sundial-get-auto-time"><code>GetAutoTime()</code></a></td><td>Checks whether Auto Time is turned on. It can still be turned on when the time speed is set to 0.</td></tr>
<tr><td><a href="#sundial-set-day-length"><code>SetDayLength()</code></a></td><td>Sets how many real seconds a complete day takes when Auto Time is on. This also changes the speed returned by GetSpeed().</td></tr>
<tr><td><a href="#sundial-get-day-length"><code>GetDayLength()</code></a></td><td>Gets how many real seconds a complete game day takes at the current speed.</td></tr>
<tr><td><a href="#sundial-set-speed"><code>SetSpeed()</code></a></td><td>Sets how quickly <a href="#sundial"><code>Sundial</code></a>&#x27;s clock moves when Auto Time is on. This also changes its day length. Use 0 to pause it without turning Auto Time off.</td></tr>
<tr><td><a href="#sundial-get-speed"><code>GetSpeed()</code></a></td><td>Gets the current speed of <a href="#sundial"><code>Sundial</code></a>&#x27;s automatic clock.</td></tr>
<tr><td><a href="#sundial-update"><code>Update()</code></a></td><td>Updates the automatic clock immediately, including any period callbacks. Normally you can leave this alone, as Draw() and getters such as GetTime() and GetPeriod() update it too.</td></tr>
</tbody></table>

<div class="api-method-group-title">Periods and callbacks</div>
<table class="api-methods"><tbody>
<tr><td><a href="#sundial-get-period"><code>GetPeriod()</code></a></td><td>Gets which of the six time periods is active. These are the periods you set in the IDE, rather than <a href="#sundial"><code>Sundial</code></a>&#x27;s additional colour-blending phases.</td></tr>
<tr><td><a href="#sundial-on-period-changed"><code>OnPeriodChanged()</code></a></td><td>Adds a function that runs when <a href="#sundial"><code>Sundial</code></a> moves from one period to another. You can add more than one.</td></tr>
<tr><td><a href="#sundial-on-period"><code>OnPeriod()</code></a></td><td>Adds a function to run when the specified period begins. Adding another function does not replace the ones already there.</td></tr>
<tr><td><a href="#sundial-on-morning"><code>OnMorning()</code></a></td><td>Adds a function to run when Morning begins.</td></tr>
<tr><td><a href="#sundial-on-day"><code>OnDay()</code></a></td><td>Adds a function to run when Day begins.</td></tr>
<tr><td><a href="#sundial-on-afternoon"><code>OnAfternoon()</code></a></td><td>Adds a function to run when Afternoon begins.</td></tr>
<tr><td><a href="#sundial-on-dusk"><code>OnDusk()</code></a></td><td>Adds a function to run when Dusk begins.</td></tr>
<tr><td><a href="#sundial-on-night"><code>OnNight()</code></a></td><td>Adds a function to run when Night begins.</td></tr>
<tr><td><a href="#sundial-on-dawn"><code>OnDawn()</code></a></td><td>Adds a function to run when Dawn begins.</td></tr>
</tbody></table>

<div class="api-method-group-title">Daylight and colour changes</div>
<table class="api-methods"><tbody>
<tr><td><a href="#sundial-get-sunlight-amount"><code>GetSunlightAmount()</code></a></td><td>Gets <a href="#sundial"><code>Sundial</code></a>&#x27;s current daylight value. <a href="#sundial"><code>Sundial</code></a> uses this to work out brightness, but you can use it for your own lighting, shadows or other effects.</td></tr>
<tr><td><a href="#sundial-get-phase"><code>GetPhase()</code></a></td><td>Gets the part of the day that currently has the strongest influence on the grading. This includes Sunset, Twilight and Predawn, which are separate from the six gameplay periods.</td></tr>
<tr><td><a href="#sundial-get-phase-name"><code>GetPhaseName()</code></a></td><td>Gets the name of the current grading phase, such as &quot;sunset&quot; or &quot;twilight&quot;.</td></tr>
</tbody></table>

<div class="api-method-group-title">Drawing and stopping</div>
<table class="api-methods"><tbody>
<tr><td><a href="#sundial-draw"><code>Draw()</code></a></td><td>Colour grades your game and draws the result on screen. For most games, just call Draw() in Post Draw. By default, <a href="#sundial"><code>Sundial</code></a> stops GameMaker from drawing your game a second time. You can also give it your own surface and choose where to draw it. The surface you give it is left unchanged.</td></tr>
<tr><td><a href="#sundial-clean-up"><code>CleanUp()</code></a></td><td>Restores the application-surface drawing setting captured when this <a href="#sundial"><code>Sundial</code></a> was created. Call this from your controller&#x27;s Clean Up event when it stops presenting the game. Repeated calls are safe. <a href="#sundial"><code>Sundial</code></a> does not free your surfaces or sprites.</td></tr>
</tbody></table>

<div class="api-method-entry" id="sundial-set-grading">
  <div class="api-method-name">SetGrading(stage, colour)</div>
  <p class="api-method-summary">Changes the grading colour for one of the six parts of the day.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">stage</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Which part of the day to change, using <a href="#enum-e-sundial"><code>eSundial</code></a> (for example, <a href="#enum-e-sundial"><code>eSundial</code></a>.DUSK).</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">colour</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">The GameMaker colour to use.</span>
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
  <p class="api-method-summary">Changes how strongly a grading colour affects the scene.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">stage</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Which part of the day to change, using <a href="#enum-e-sundial"><code>eSundial</code></a>.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">strength</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">0 removes this stage&#x27;s colour influence, 1 uses full strength, and values above 1 make it stronger. Cannot be negative.</span>
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
  <p class="api-method-summary">Sets how bright the outdoor scene should be during the day and at night. <a href="#sundial"><code>Sundial</code></a> changes the brightness smoothly between the two.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">day_brightness</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Brightness during full daylight. 1 leaves brightness unchanged. Higher values brighten the scene.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">night_brightness</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Brightness at night. 1 leaves brightness unchanged. Lower values darken the scene.</span>
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
  <p class="api-method-summary">Sets the base colour used for indoor areas. The indoor mask decides which parts of the scene this affects.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">colour</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">The GameMaker colour to use indoors.</span>
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
  <p class="api-method-summary">Changes how strongly the indoor grading colour affects the scene.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">strength</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">0 leaves the indoor base colour neutral, 1 uses the chosen indoor colour, and values above 1 make it stronger. Cannot be negative.</span>
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
  <p class="api-method-summary">Controls how much of the outdoor grading colour reaches indoor areas. This changes colour, not brightness.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">amount</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">0 uses only the indoor colour, while 1 uses the full outdoor colour grading. Values between 0 and 1 blend them.</span>
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
  <p class="api-method-summary">Sets separate day and night brightness for indoor areas. <a href="#sundial"><code>Sundial</code></a> blends between them as the day passes.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">day_brightness</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Indoor brightness during the day. 1 leaves brightness unchanged.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">night_brightness</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Indoor brightness at night. 1 leaves brightness unchanged.</span>
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
  <p class="api-method-summary">Uses a surface to decide which parts of the scene are indoors. Black means outdoors, white means indoors, and grey blends the two. The mask can be any size. It will be stretched to fit the scene.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">mask_surface</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">An existing surface to use as the mask. <a href="#sundial"><code>Sundial</code></a> reads its red channel but will not delete the surface for you. If GameMaker destroys it, recreate it and call SetMask() again.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#sundial-set-mask-sprite"><code>Sundial.SetMaskSprite</code></a> <span aria-hidden="true">·</span> <a href="#sundial-clear-mask"><code>Sundial.ClearMask</code></a> <span aria-hidden="true">·</span> <a href="#sundial-has-mask"><code>Sundial.HasMask</code></a> <span aria-hidden="true">·</span> <a href="#sundial-get-mask"><code>Sundial.GetMask</code></a></div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-mask-sprite">
  <div class="api-method-name">SetMaskSprite(mask_sprite, [subimage])</div>
  <p class="api-method-summary">Uses a sprite instead of a surface for the indoor mask. Black means outdoors, white means indoors, and grey blends the two. The sprite is stretched to fit the scene.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">mask_sprite</span>
      <span class="api-argument-type">Asset.GMSprite</span>
      <span class="api-argument-description">A bitmap sprite to use as the mask. <a href="#sundial"><code>Sundial</code></a> reads its red channel, not its transparency. The sprite origin is ignored, and areas trimmed away by GameMaker count as outdoors.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">subimage <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Which frame to use, starting from 0. Defaults to 0. <a href="#sundial"><code>Sundial</code></a> will not animate the mask for you.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#sundial-set-mask"><code>Sundial.SetMask</code></a> <span aria-hidden="true">·</span> <a href="#sundial-clear-mask"><code>Sundial.ClearMask</code></a> <span aria-hidden="true">·</span> <a href="#sundial-has-mask"><code>Sundial.HasMask</code></a> <span aria-hidden="true">·</span> <a href="#sundial-get-mask"><code>Sundial.GetMask</code></a></div>
  </div>
</div>

<div class="api-method-entry" id="sundial-clear-mask">
  <div class="api-method-name">ClearMask()</div>
  <p class="api-method-summary">Removes the indoor mask. The whole scene will use the outdoor grading again.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-has-mask">
  <div class="api-method-name">HasMask()</div>
  <p class="api-method-summary">Checks whether the mask you supplied still exists, whether it is a surface or a sprite.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-mask">
  <div class="api-method-name">GetMask()</div>
  <p class="api-method-summary">Gets the surface or sprite currently being used as the indoor mask. Use HasMask() to check whether it still exists.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real|Asset.GMSprite</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-time-of-day">
  <div class="api-method-name">GetTimeOfDay()</div>
  <p class="api-method-summary">Gets the current position in the day as a number from 0 to 1, where 0 is Morning and 1 is the end of the day.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-sunlight-amount">
  <div class="api-method-name">GetSunlightAmount()</div>
  <p class="api-method-summary">Gets <a href="#sundial"><code>Sundial</code></a>&#x27;s current daylight value. <a href="#sundial"><code>Sundial</code></a> uses this to work out brightness, but you can use it for your own lighting, shadows or other effects.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-phase">
  <div class="api-method-name">GetPhase()</div>
  <p class="api-method-summary">Gets the part of the day that currently has the strongest influence on the grading. This includes Sunset, Twilight and Predawn, which are separate from the six gameplay periods.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-phase-name">
  <div class="api-method-name">GetPhaseName()</div>
  <p class="api-method-summary">Gets the name of the current grading phase, such as &quot;sunset&quot; or &quot;twilight&quot;.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-cycle-timing">
  <div class="api-method-name">SetCycleTiming(day_fraction, morning_duration, afternoon_start, sunset_duration, twilight_duration, predawn_duration)</div>
  <p class="api-method-summary">Changes when the different parts of the day start and how long the colour changes between them take. All six values use a fraction of the day from 0 to 1. Invalid ordering causes a fatal error.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">day_fraction</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">The point in the day where Dusk begins.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">morning_duration</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">How long Morning takes to fade into Day.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">afternoon_start</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">When the Afternoon colour starts blending in. This is not the same as when the Afternoon period begins.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">sunset_duration</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">How much time before Dusk is used for the sunset colour change.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">twilight_duration</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">How much time after Dusk is used for twilight before Night.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">predawn_duration</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">How much of the end of Night is used to blend through Dawn into Morning.</span>
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
  <p class="api-method-summary">Moves <a href="#sundial"><code>Sundial</code></a> to a position in the day from 0 to 1. Values outside that range wrap around. If a manual jump changes the period, only the new period&#x27;s callbacks run.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">time_of_day</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Position in the day. 0 and 1 both represent Morning, at the start and end of the cycle.</span>
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
  <p class="api-method-summary">Turns automatic time on or off. When enabled, <a href="#sundial"><code>Sundial</code></a> advances its clock using elapsed real time.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">enabled</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">True to let <a href="#sundial"><code>Sundial</code></a> advance time, false if your game will control the time itself.</span>
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
  <p class="api-method-summary">Checks whether Auto Time is turned on. It can still be turned on when the time speed is set to 0.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-day-length">
  <div class="api-method-name">SetDayLength(seconds)</div>
  <p class="api-method-summary">Sets how many real seconds a complete day takes when Auto Time is on. This also changes the speed returned by GetSpeed().</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">seconds</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Number of real seconds in one game day. Must be greater than 0. For a ten-minute day, use 600.</span>
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
  <p class="api-method-summary">Gets how many real seconds a complete game day takes at the current speed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-speed">
  <div class="api-method-name">SetSpeed(speed)</div>
  <p class="api-method-summary">Sets how quickly <a href="#sundial"><code>Sundial</code></a>&#x27;s clock moves when Auto Time is on. This also changes its day length. Use 0 to pause it without turning Auto Time off.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">speed</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Number of game seconds that pass for every real second. For example, 120 makes two game minutes pass per second. Cannot be negative.</span>
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
  <p class="api-method-summary">Gets the current speed of <a href="#sundial"><code>Sundial</code></a>&#x27;s automatic clock.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-day-percent">
  <div class="api-method-name">SetDayPercent(percent)</div>
  <p class="api-method-summary">Another name for SetTimeOfDay(). Sets how far through the day <a href="#sundial"><code>Sundial</code></a> is, using a number from 0 to 1.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">percent</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Position in the day, from 0 to 1. Values outside this range wrap around.</span>
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
  <p class="api-method-summary">Another name for GetTimeOfDay(). Gets how far through the day <a href="#sundial"><code>Sundial</code></a> is.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-morning-time">
  <div class="api-method-name">SetMorningTime(hour)</div>
  <p class="api-method-summary">Sets what time on the 24-hour clock Morning begins. This changes the clock, not the length of the day or the grading.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">hour</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Clock time in decimal hours. 6 means 06:00 and 6.5 means 06:30. Values wrap around 24 hours.</span>
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
  <p class="api-method-summary">Gets the 24-hour clock time when Morning begins.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-set-time">
  <div class="api-method-name">SetTime(hour)</div>
  <p class="api-method-summary">Moves <a href="#sundial"><code>Sundial</code></a> to a particular time on the 24-hour clock. This does not turn Auto Time on or off, and skipped periods do not get their callbacks run.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">hour</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Clock time in decimal hours. For example, 18.5 means 18:30. Values wrap around 24 hours.</span>
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
  <p class="api-method-summary">Gets the current time on <a href="#sundial"><code>Sundial</code></a>&#x27;s 24-hour clock.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-hour">
  <div class="api-method-name">GetHour()</div>
  <p class="api-method-summary">Gets the hour from <a href="#sundial"><code>Sundial</code></a>&#x27;s current clock time.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-minute">
  <div class="api-method-name">GetMinute()</div>
  <p class="api-method-summary">Gets the minute from <a href="#sundial"><code>Sundial</code></a>&#x27;s current clock time.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-get-period">
  <div class="api-method-name">GetPeriod()</div>
  <p class="api-method-summary">Gets which of the six time periods is active. These are the periods you set in the IDE, rather than <a href="#sundial"><code>Sundial</code></a>&#x27;s additional colour-blending phases.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-on-period-changed">
  <div class="api-method-name">OnPeriodChanged(callback)</div>
  <p class="api-method-summary">Adds a function that runs when <a href="#sundial"><code>Sundial</code></a> moves from one period to another. You can add more than one.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function receiving the previous period and the new period, both as <a href="#enum-e-sundial-period"><code>eSundialPeriod</code></a> values.</span>
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
  <p class="api-method-summary">Adds a function to run when the specified period begins. Adding another function does not replace the ones already there.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">period</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Which period to watch, using <a href="#enum-e-sundial-period"><code>eSundialPeriod</code></a>.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function to run when that period begins.</span>
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
  <p class="api-method-summary">Adds a function to run when Morning begins.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function to run when Morning begins.</span>
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
  <p class="api-method-summary">Adds a function to run when Day begins.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function to run when Day begins.</span>
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
  <p class="api-method-summary">Adds a function to run when Afternoon begins.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function to run when Afternoon begins.</span>
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
  <p class="api-method-summary">Adds a function to run when Dusk begins.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function to run when Dusk begins.</span>
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
  <p class="api-method-summary">Adds a function to run when Night begins.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function to run when Night begins.</span>
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
  <p class="api-method-summary">Adds a function to run when Dawn begins.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">callback</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function to run when Dawn begins.</span>
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
  <p class="api-method-summary">Updates the automatic clock immediately, including any period callbacks. Normally you can leave this alone, as Draw() and getters such as GetTime() and GetPeriod() update it too.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="sundial-clean-up">
  <div class="api-method-name">CleanUp()</div>
  <p class="api-method-summary">Restores the application-surface drawing setting captured when this <a href="#sundial"><code>Sundial</code></a> was created. Call this from your controller&#x27;s Clean Up event when it stops presenting the game. Repeated calls are safe. <a href="#sundial"><code>Sundial</code></a> does not free your surfaces or sprites.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#sundial">Sundial</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#sundial-draw"><code>Sundial.Draw</code></a> <span aria-hidden="true">·</span> <a href="#sundial-start"><code>SundialStart</code></a> <span aria-hidden="true">·</span> <a href="#sundial-stop"><code>SundialStop</code></a></div>
  </div>
</div>

<div class="api-method-entry" id="sundial-draw">
  <div class="api-method-name">Draw([source_surface], [x], [y], [width], [height])</div>
  <p class="api-method-summary">Colour grades your game and draws the result on screen. For most games, just call Draw() in Post Draw. By default, <a href="#sundial"><code>Sundial</code></a> stops GameMaker from drawing your game a second time. You can also give it your own surface and choose where to draw it. The surface you give it is left unchanged.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">source_surface <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">The surface to grade. Leave this out in Post Draw to use the application surface. Omitting a surface while trying to Draw in another Draw event causes a fatal error (as you cannot draw a surface onto itself).</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">x <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Where to draw it horizontally. Defaults to the correct window position for the application surface, or 0 for your own surface.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">y <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Where to draw it vertically. Defaults to the correct window position for the application surface, or 0 for your own surface.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">width <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Draw width. Defaults to the application surface&#x27;s displayed width, or your supplied surface&#x27;s width.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">height <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Draw height. Defaults to the application surface&#x27;s displayed height, or your supplied surface&#x27;s height.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Id.Surface</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Example</div>
    <pre class="api-example"><code>// In Post Draw, colour grade your game.
sundial.Draw();

// Or draw your own surface at a chosen position and size.
sundial.Draw(my_surface, 0, 0, 1280, 720);</code></pre>
  </div>
</div>

## Starting, stopping and loading

<div class="api-method-entry" id="sundial-start">
  <div class="api-method-name">SundialStart([preset_name])</div>
  <p class="api-method-summary">Starts <a href="#sundial"><code>Sundial</code></a> using a preset from the Visual Editor. <a href="#sundial"><code>Sundial</code></a> will handle the drawing for you and keep working when you change rooms. If it&#x27;s already running, calling this again won&#x27;t restart the day or change the preset. Call <a href="#sundial-stop"><code>SundialStop()</code></a> first if you want to switch presets.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">preset_name <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">The name of the preset to load. Leave this out to use the default preset. To switch presets later, call <a href="#sundial-stop"><code>SundialStop()</code></a> first.</span>
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
    <pre class="api-example"><code>sundial = SundialStart();
sundial.SetDayLength(600);</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#sundial-stop"><code>SundialStop</code></a> <span aria-hidden="true">·</span> <a href="#sundial-import"><code>SundialImport</code></a> <span aria-hidden="true">·</span> <a href="#sundial-clean-up"><code>Sundial.CleanUp</code></a></div>
  </div>
</div>

<div class="api-method-entry" id="sundial-stop">
  <div class="api-method-name">SundialStop()</div>
  <p class="api-method-summary">Stops <a href="#sundial"><code>Sundial</code></a> if you started it with <a href="#sundial-start"><code>SundialStart()</code></a>. It puts GameMaker&#x27;s drawing setting back the way it was. You can call it more than once. It won&#x27;t change other Sundials you created yourself or masks you supplied.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Example</div>
    <pre class="api-example"><code>SundialStop();</code></pre>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#sundial-start"><code>SundialStart</code></a> <span aria-hidden="true">·</span> <a href="#sundial-clean-up"><code>Sundial.CleanUp</code></a></div>
  </div>
</div>

<div class="api-method-entry" id="sundial-import">
  <div class="api-method-name">SundialImport([preset_name], [manage_application_surface])</div>
  <p class="api-method-summary">Loads a <a href="#sundial"><code>Sundial</code></a> preset you saved using <a href="#sundial"><code>Sundial</code></a> Visual Editor. Without a name, it loads whichever preset you marked as Default.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">preset_name <span class="api-optional">optional</span></span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">Exact name of the preset to load. Leave this out to load the default preset. An unknown name causes an error.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">manage_application_surface <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">True to let <a href="#sundial"><code>Sundial</code></a> manage application-surface drawing until CleanUp() is called. False to leave your renderer&#x27;s setting untouched. Defaults to true. Pass undefined for the preset name to use the default preset with this option.</span>
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

### Grading colours
{: .api-function-subsection-title .api-function-subsection-title-first }

<div class="api-enum-entry" id="enum-e-sundial">
  <div class="api-enum-name">eSundial</div>
  <p class="api-enum-summary">The six parts of the day you can give their own colours and grading strengths.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row">
        <span class="api-enum-member">MORNING</span>
        <span class="api-enum-description">Use this to change the Morning colour.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">DAY</span>
        <span class="api-enum-description">Use this to change the Day colour.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">AFTERNOON</span>
        <span class="api-enum-description">Use this to change the Afternoon colour.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">DUSK</span>
        <span class="api-enum-description">Use this to change the Dusk colour, including sunset and twilight.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">NIGHT</span>
        <span class="api-enum-description">Use this to change the Night colour.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">DAWN</span>
        <span class="api-enum-description">Use this to change the Dawn colour, as night turns into Morning.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">NUM</span>
        <span class="api-enum-description">The number of grading choices. It is not a part of the day.</span>
      </div>
    </div>
  </div>
</div>

### Time
{: .api-function-subsection-title }

<div class="api-enum-entry" id="enum-e-sundial-period">
  <div class="api-enum-name">eSundialPeriod</div>
  <p class="api-enum-summary">The six parts of the day reported by GetPeriod() and used by functions such as OnMorning() and OnNight().</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row">
        <span class="api-enum-member">MORNING</span>
        <span class="api-enum-description">Morning, when <a href="#sundial"><code>Sundial</code></a>&#x27;s day begins.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">DAY</span>
        <span class="api-enum-description">Daytime.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">AFTERNOON</span>
        <span class="api-enum-description">Afternoon.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">DUSK</span>
        <span class="api-enum-description">Dusk.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">NIGHT</span>
        <span class="api-enum-description">Nighttime.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">DAWN</span>
        <span class="api-enum-description">Dawn.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">NUM</span>
        <span class="api-enum-description">The number of periods. Not a period itself.</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-sundial-phase">
  <div class="api-enum-name">eSundialPhase</div>
  <p class="api-enum-summary">More detailed parts of the day used by <a href="#sundial"><code>Sundial</code></a>&#x27;s colour changes, including Sunset, Twilight and Predawn.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row">
        <span class="api-enum-member">MORNING</span>
        <span class="api-enum-description">The Morning part of the colour changes.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">DAY</span>
        <span class="api-enum-description">The Day part of the colour changes.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">AFTERNOON</span>
        <span class="api-enum-description">The Afternoon part of the colour changes.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">SUNSET</span>
        <span class="api-enum-description">Sunset, when the colours are moving towards Dusk.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">TWILIGHT</span>
        <span class="api-enum-description">Twilight, between Dusk and Night.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">NIGHT</span>
        <span class="api-enum-description">Nighttime.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">PREDAWN</span>
        <span class="api-enum-description">The change from Night through Dawn and back to Morning.</span>
      </div>
      <div class="api-enum-row">
        <span class="api-enum-member">NUM</span>
        <span class="api-enum-description">The number of phases. Not a phase itself.</span>
      </div>
    </div>
  </div>
</div>

## Version

<div class="api-method-entry api-macro-entry api-macro-value" id="macro-sundial-version">
  <div class="api-method-name">SUNDIAL_VERSION</div>
  <p class="api-method-summary">The version of <a href="#sundial"><code>Sundial</code></a> you have installed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Value</div>
    <pre class="api-example"><code>&quot;1.0.0&quot;</code></pre>
  </div>
</div>

## Symbol index

<div class="api-symbol-index">
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">C</div>
    <div class="api-symbol-row"><a href="#sundial-clean-up"><code>CleanUp()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
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
    <div class="api-symbol-row"><a href="#sundial-set-mask-sprite"><code>SetMaskSprite()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-morning-time"><code>SetMorningTime()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-speed"><code>SetSpeed()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-time"><code>SetTime()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial-set-time-of-day"><code>SetTimeOfDay()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
    <div class="api-symbol-row"><a href="#sundial"><code>Sundial</code></a></div>
    <div class="api-symbol-row"><a href="#sundial-import"><code>SundialImport()</code></a></div>
    <div class="api-symbol-row"><a href="#sundial-start"><code>SundialStart()</code></a></div>
    <div class="api-symbol-row"><a href="#sundial-stop"><code>SundialStop()</code></a></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">U</div>
    <div class="api-symbol-row"><a href="#sundial-update"><code>Update()</code></a> <span class="api-symbol-owner">| Sundial</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">Enums</div>
    <div class="api-symbol-row"><a href="#enum-e-sundial"><code>eSundial</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-sundial-period"><code>eSundialPeriod</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-sundial-phase"><code>eSundialPhase</code></a><span class="api-symbol-owner">enum</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">Macros</div>
    <div class="api-symbol-row"><a href="#macro-sundial-version"><code>SUNDIAL_VERSION</code></a><span class="api-symbol-owner">macro</span></div>
  </div>
</div>
