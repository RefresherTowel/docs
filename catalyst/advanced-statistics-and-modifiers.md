---
layout: default
title: Advanced Statistics & Modifiers
parent: Catalyst
nav_order: 7
redirect_from:
  - /catalyst/advanced.html
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Advanced Statistics & Modifiers

Ok, you've thrown together a few Statistics. Maybe a couple of Modifiers have slipped in there. A Resource or two describes your players HP and maybe Mana, and you're feeling pretty slick having an automated regen Resource Flow running on your HP Resource. Now, let's venture into the darker corners of Catalyst and see just how much you can contort the shape of things to suit your exact design needs through the advanced rules.

Advanced rules come in when the rule itself becomes more particular: Several auras where only the strongest should count, a custom layer between equipment and temporary buffs, or a calculation you need Catalyst to explain because the final number looks wrong.

All of these features are extensions to the basic model of Catalyst that you have already learned, and you only need to think about these things when they are solving a specific problem. The default settings for most stuff in Catalyst is generally sensible for the majority of gameplay requirements.

---

## When related Modifiers shouldn't all stack

Suppose three nearby allies can provide the same movement aura:

- weak aura: +10%
- strong aura: +25%
- elite aura: +40%

If the design says only the strongest aura should count, attaching three ordinary Modifiers would be wrong. They would all stack.

Put them in the same **family** instead:

```js
weak_aura = new CatalystModifier(0.1, eCatMathOps.MULTIPLY)
    .SetFamily("movement_aura", eCatFamilyMode.STRONGEST);

strong_aura = new CatalystModifier(0.25, eCatMathOps.MULTIPLY)
    .SetFamily("movement_aura", eCatFamilyMode.STRONGEST);

elite_aura = new CatalystModifier(0.4, eCatMathOps.MULTIPLY)
    .SetFamily("movement_aura", eCatFamilyMode.STRONGEST);
```

Attach all three as usual:

```js
move_speed.AddModifier(weak_aura);
move_speed.AddModifier(strong_aura);
move_speed.AddModifier(elite_aura);
```

Catalyst checks which family members are actually eligible for the current evaluation, then lets the strongest eligible member apply.

An elite aura whose condition currently fails doesn't block the strong aura merely because its raw value is larger. Catalyst chooses from the family members that are actually eligible for this evaluation.

---

## `STRONGEST`, `WEAKEST`, and `STACK_ALL`

A family can use one of three modes:

```js
eCatFamilyMode.STRONGEST
eCatFamilyMode.WEAKEST
eCatFamilyMode.STACK_ALL
```

`STRONGEST` is the common “only the best buff counts” rule.

`WEAKEST` does the opposite: it keeps the eligible family member with the smallest effect magnitude. Catalyst measures that magnitude after stacks are resolved, so a `+5` ADD Modifier is weaker than `+15`, and a `+10%` MULTIPLY Modifier is weaker than `+25%`.

`STACK_ALL` keeps the family label for organisation but allows every eligible member to apply.

`SetFamily()` defaults to `STRONGEST`, so this is enough for the common case:

```js
elite_aura.SetFamily("movement_aura");
```

Catalyst compares how strong each Modifier actually is **after its current stacks are taken into account**. A three-stack +5 Modifier competes as +15, not merely as +5.

ADD families compete with other ADD members. MULTIPLY families compete with other MULTIPLY members. A +10 flat bonus and a +10% multiplier don't knock one another out simply because they share a family name.

If two competitors have exactly the same strength, the one that appears first in the Statistic's evaluation order wins the tie.

---

## Families usually compete inside one layer

By default, a family only compares members in the same layer.

This keeps an equipment bonus from unexpectedly suppressing a temporary aura just because both happen to share a family label in different stages of the calculation.

If this movement-aura family should compete across the entire Statistic instead, give every member of that family the same Statistic-wide scope:

```js
weak_aura.SetFamilyScope(eCatFamilyScope.STATISTIC);
strong_aura.SetFamilyScope(eCatFamilyScope.STATISTIC);
elite_aura.SetFamilyScope(eCatFamilyScope.STATISTIC);
```

Family scope is part of the family match. If only one aura used `STATISTIC` while the others stayed on the default `LAYER` scope, they would no longer be competing in the same family group.

The two options are:

```js
eCatFamilyScope.LAYER
eCatFamilyScope.STATISTIC
```

Use `LAYER` when the “pick one” rule belongs to one stage of the build. Use `STATISTIC` when the family really means “only one of these should affect this Statistic anywhere.”

Two Modifiers only take part in the same family comparison when they use the same family name, family mode, family scope, and maths operation.

---

## Hard floors and ceilings

Sometimes a rule isn't another bonus. Instead, it's a boundary that should be enforced after ordinary ADD and MULTIPLY Modifiers have done their work.

Suppose the player's movement speed should never fall below `2` while a particular protection is active:

```js
minimum_speed = new CatalystModifier(2, eCatMathOps.FORCE_MIN);
move_speed.AddModifier(minimum_speed);
```

After the ordinary layers are calculated, `FORCE_MIN` raises the result to at least `2`.

A hard ceiling works the other way:

```js
maximum_speed = new CatalystModifier(8, eCatMathOps.FORCE_MAX);
move_speed.AddModifier(maximum_speed);
```

`FORCE_MAX` lowers the result to at most `8`.

### Why not use Statistic clamping?

Statistic clamping describes an inherent final range for the Statistic itself:

```js
critical_chance = new CatalystStatistic(0.05, 0, 1)
    .SetClamped(true);
```

A FORCE Modifier is better when the floor or ceiling comes from a removable gameplay source: a status, rule, difficulty modifier, area effect, item, or similar contribution.

Remove the FORCE Modifier and that temporary boundary disappears with it.

### FORCE Modifiers behave sensibly

FORCE Modifiers aren't ordinary layer contributions, so Catalyst rejects configuration that would make their meaning ambiguous, including layers, stacks, stack functions, stack modes, and families.

A FORCE Modifier says one thing: after ordinary layer math, force the value up to this minimum or down to this maximum.

`FORCE_MIN` is processed before `FORCE_MAX`.

---

## Custom layer order

The built-in layers cover many games:

```js
eCatStatLayer.BASE_BONUS
eCatStatLayer.EQUIPMENT
eCatStatLayer.AUGMENTS
eCatStatLayer.TEMP
eCatStatLayer.GLOBAL
```

But your game's ordering rules may not fit those names.

Suppose you need a dedicated difficulty layer after equipment but before temporary buffs. Layer identities can be strings or finite numbers, so you can define your own:

```js
damage = new CatalystStatistic(10)
    .SetName("Damage");

damage.SetLayerOrder([
    eCatStatLayer.BASE_BONUS,
    eCatStatLayer.EQUIPMENT,
    "difficulty",
    eCatStatLayer.TEMP,
    eCatStatLayer.GLOBAL
]);
```

Then put a Modifier on it:

```js
nightmare_bonus = new CatalystModifier(0.25, eCatMathOps.MULTIPLY)
    .SetLayer("difficulty");
```

`SetLayerOrder()` replaces the Statistic's complete layer order, so Catalyst won't silently append unknown layers afterward. If a Modifier uses a layer that the Statistic doesn't know, that Modifier won't affect the result.

You can check before using a layer:

```js
if (damage.HasLayer("difficulty")) {
    damage.AddModifier(nightmare_bonus);
}
```

If many related Statistics should share one custom order, put that configuration on their [CatalystSet](sets-and-previews) instead of repeating it on every Statistic.

You could replace the entire layer order, using either strings or enums (technically any number works, but enums are usually a more sensible choice for "numbered") and ignore the default enums entirely if you wanted.

---

## Choosing how ADD and MULTIPLY are ordered inside a layer

By default, attachment order doesn't decide the maths inside a layer.

Catalyst Statistics start with `eCatModifierOrder.ADD_FIRST`, which means that within each configured layer, Catalyst resolves all eligible `ADD` Modifiers first, then all eligible `MULTIPLY` Modifiers.

Suppose a layer contains:

```text
base entering the layer = 100

+50% MULTIPLY
+20 ADD
```

With the default `ADD_FIRST` order, Catalyst calculates:

```text
(100 + 20) * 1.5 = 180
```

You get the same result whether the multiplier was attached before or after the flat bonus.

However, this ordering is configurable. `SetModifierOrder()` lets you choose between three different rules:

```js
stat.SetModifierOrder(eCatModifierOrder.ADD_FIRST);
stat.SetModifierOrder(eCatModifierOrder.MULTIPLY_FIRST);
stat.SetModifierOrder(eCatModifierOrder.ATTACHMENT_ORDER);
```

`ADD_FIRST` is the default behaviour shown above.

`MULTIPLY_FIRST` reverses the two operations inside each layer. With the same `+50%` and `+20` Modifiers:

```text
(100 * 1.5) + 20 = 170
```

`ATTACHMENT_ORDER` instead resolves `ADD` and `MULTIPLY` Modifiers in the order they were attached. If the `+20` Modifier was attached first, followed by the `+50%` Modifier:

```text
(100 + 20) * 1.5 = 180
```

If the multiplier was attached first:

```text
(100 * 1.5) + 20 = 170
```

This only changes the order of Modifiers **inside each layer**. Your configured layer order still takes priority, so Catalyst finishes one layer before moving on to the next regardless of when Modifiers in different layers were attached.

For most games, the default `ADD_FIRST` behaviour means attachment order follows an understandable defined order. If the order itself is part of your game's maths, `MULTIPLY_FIRST` or `ATTACHMENT_ORDER` let you make that rule explicit.

---

## When the base value is itself calculated

Sometimes the starting point for a Statistic isn't a simple number.

Suppose you want a Carrying Capacity Statistic, but it's derived from another Strength Statistic:

```text
capacity = 20 + strength * 2
```

Start with a Strength Statistic, then make capacity calculate its base when it evaluates:

```js
strength = new CatalystStatistic(8)
    .SetName("Strength");

carry_capacity = new CatalystStatistic(20)
    .SetBaseFunc(function(_statistic, _facts) {
        return 20 + strength.GetValue() * 2;
    });
```

Modifiers still apply afterward exactly as usual.

The callback also receives the facts resolved for this evaluation, which is useful when the base itself depends on current world state:

```js
world_facts = new OracleFacts({
    is_night : false
});

world_fact_view = new OracleFactView()
    .AddTo("world", world_facts);

visibility = new CatalystStatistic(1)
    .SetFactView(world_fact_view)
    .SetBaseFunc(function(_statistic, _facts) {
        var _is_night = _facts.GetFrom("world", "is_night") ?? false;
        if (_is_night) {
            return 0.6;
        }
        return 1;
    });
```

Use `SetBaseFunc()` when a changing relationship defines the Statistic's starting value.

Call `ClearBaseFunc()` to return to the stored base value.

### Clamping and rounding don't rewrite the stored base

`SetBaseValue()` and `ChangeBaseValue()` change the Statistic's stored base number. Catalyst doesn't clamp or round that stored number as you assign it.

Clamping and rounding apply to the **finished calculated result** instead, so the base can move outside the Statistic's final displayed range before Modifiers or post-processing are applied.

---

## Transforming the completed result

Sometimes the full Catalyst calculation is correct, but the game needs one final rule after Modifiers.

For example, an initiative score might need to convert the completed value into a discrete step:

```js
initiative = new CatalystStatistic(25);

initiative.SetPostProcess(function(_statistic, _value, _facts) {
    return max(0, floor(_value / 5));
});
```

Post-processing runs after ordinary and FORCE Modifiers, but before Statistic clamping and rounding.

Use it for rules that genuinely describe the final interpretation of the Statistic. If “+5 from boots” or “+20% while enraged” can be represented as a normal contribution, keep that rule as a Modifier instead. Modifiers remain easier to add, remove, inspect, preview, and attribute to their sources. Post processing is usually reserved for explicit shaping of a result.

Call `ClearPostProcess()` to remove the final transform.

---

## Reacting when the Statistic's current value changes

Suppose the UI should update whenever movement speed actually changes.

Subscribe once:

```js
move_speed_subscription = move_speed.OnChange(
    function(_statistic, _previous, _current) {
        show_debug_message(
            "Move speed: "
            + string(_previous)
            + " -> "
            + string(_current)
        );
    }
);
```

The callback receives the Statistic, the value it previously returned as its current value, and the new current value.

When you no longer want the callback:

```js
move_speed_subscription.Unsubscribe();
```

You can check the handle with:

```js
if (move_speed_subscription.IsActive()) {
    // Still subscribed.
}
```

### Refreshing at a specific point

`GetValue()` automatically refreshes a Statistic when Catalyst knows it's stale. You can also ask for that refresh directly:

```js
var _refresh = move_speed.Refresh();

if (_refresh.DidChange()) {
    show_debug_message(
        string(_refresh.GetPrevious())
        + " -> "
        + string(_refresh.GetCurrent())
    );
}
```

Call `Refresh()` after your game changes facts or other state that a Statistic depends on when you want Catalyst to update its current value, including any `OnChange()` subscriptions, at that specific point. Catalyst tries very hard to keep values up to date when needed, so `Refresh()` is more of an emergency escape hatch, rather than something you need to worry about doing much.

---

## Finding Modifiers by where they came from

Keeping the exact Modifier reference is the simplest way to remove one:

```js
move_speed.DestroyModifier(haste);
```

Sometimes the game instead wants to remove a whole category of changes that came from the same source.

### Source labels

A human-readable source label works well when the source is a named gameplay rule:

```js
blessing = new CatalystModifier(0.2, eCatMathOps.MULTIPLY)
    .SetSourceLabel("Blessing of Wind");
```

Later:

```js
move_speed.DestroyModifiersBySourceLabel("Blessing of Wind");
```

### Source IDs

When the current object itself is the source, store that reference instead:

```js
boots_bonus = new CatalystModifier(0.15, eCatMathOps.MULTIPLY)
    .SetSourceId(self);
```

Then remove everything from that exact source:

```js
move_speed.DestroyModifiersBySourceId(self);
```

`HasModifierFromSourceId()` lets you ask whether any such Modifier is still attached. In a real equipment system, that source might instead be the live item instance or data struct that created the Modifier.

### Source metadata

`source_meta` is for project-specific information that doesn't fit a simple label or object reference:

```js
season_bonus = new CatalystModifier(3, eCatMathOps.ADD)
    .SetSourceMeta({ season: "winter", region: "north" });
```

You can match it with a predicate:

```js
var _has_winter_bonus = move_speed.HasModifierFromSourceMeta(
    function(_meta) {
        return is_struct(_meta) && _meta[$ "season"] == "winter";
    }
);
```

`DestroyModifiersBySourceMeta()` uses the same kind of predicate when you want to destroy all matches.

---

## Tags for broad categories

A source answers “where did this come from?” A tag answers “what kind of Modifier is this?”

A curse might come from several different enemies, items, or systems while still sharing one useful category:

```js
slowness = new CatalystModifier(-1, eCatMathOps.ADD)
    .AddTag("curse");
```

Then a cleanse can remove every attached curse Modifier:

```js
move_speed.DestroyModifiersByTag("curse");
```

Use source information when you care **which thing created the Modifier**. Use tags when Modifiers from different sources should all count as the same broader kind of change.

---

## When the number looks wrong: `Explain()`

Once a Statistic has conditions, dynamic stacks, families, custom layers, and force rules, the final number can be hard to reason about from the outside.

Ask Catalyst to explain one evaluation:

```js
var _evaluation = damage.Explain();
```

The result gives you the final value and the base Catalyst started from:

```js
show_debug_message(_evaluation.GetBaseValue());
show_debug_message(_evaluation.GetValue());
```

It also gives one result for every Modifier considered:

```js
var _results = _evaluation.GetModifierResults();

for (var i = 0; i < array_length(_results); i++) {
    var _result = _results[i];

    show_debug_message(
        "Modifier " + string(i)
        + " applied="
        + string(_result.Applied())
        + " stacks="
        + string(_result.GetEffectiveStacks())
        + " before="
        + string(_result.GetValueBefore())
        + " after="
        + string(_result.GetValueAfter())
    );
}
```

If a Modifier did not apply, `GetSkipReason()` tells you whether its condition failed, it resolved to zero stacks, it lost a family comparison, or it used a layer this Statistic doesn't know.

`GetLayers()` groups the same Modifier results by layer when that view is more useful for a debugger or stat breakdown UI.

Use `Explain()` when you need the story of the calculation. Use `GetValue()` when you only need the answer.

If these Statistics belong to a `CatalystSet`, the Set can gather those explanations alongside its Resources and Effect Managers. Here `player_model` is the character Set built in the Sets guide:

```js
var _details = player_model.GetDetails();
var _stat_details = _details.GetStatisticEvaluations();
```

A model-wide debugger or detailed UI can use that to inspect the related Catalyst objects together.

---

## The complete Statistic calculation

For one evaluation, Catalyst does this:

1. Resolve the current Oracle facts, plus any one-off query facts.
2. Resolve the base from `SetBaseFunc()` if one exists, otherwise use the stored base.
3. Walk the configured layers in order.
4. Inside each layer, resolve eligible ADD Modifiers and MULTIPLY Modifiers, according to the Modifier Order rule applied.
5. Choose family winners after conditions have been checked and the actual stack counts are known.
6. Apply `FORCE_MIN` Modifiers.
7. Apply `FORCE_MAX` Modifiers.
8. Run `SetPostProcess()` if present.
9. Clamp the final result when clamping is enabled.
10. Round the final result when rounding is enabled.

The rules you've authored - layers, maths operations, families, conditions, and stacks - decide the overall calculation.

---

## Resetting a Statistic

If a reusable Statistic needs to return to its original base while keeping its current configuration and Modifiers:

```js
damage.ResetToStarting();
```

`ResetAll()` is much more destructive:

```js
damage.ResetAll();
```

It restores the starting base value and removes nearly all of the Statistic's current setup: attached Modifiers, clamping, rounding, post-processing, base functions, tags, Fact View, and subscriptions. The Statistic keeps its name, identity, and layer order.

Use `ResetAll()` when you genuinely want to rebuild the Statistic from a clean gameplay state, not as a routine way to refresh it.

---

## Next: saving and loading

The old Catalyst workflow required project code to repair loaded Statistic structs after JSON had stripped their methods. That's gone.

The current save boundary is a `CatalystSet`, which can capture and restore the connected Catalyst model while preserving the live objects your game already references.

Continue with **[Saving & Loading](saving-and-loading)** to save a whole Catalyst model together and handle the few things JSON can't recreate on its own, such as callback functions and custom countdown trackers.
