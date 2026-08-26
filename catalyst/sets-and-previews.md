---
layout: default
title: Sets & Previews
parent: Catalyst
nav_order: 6
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Sets & Previews

Sometimes the game needs an answer about something without actually changing anything concrete in the game state. A shop UI might need to show what `damage` would become if the player equipped a weapon, while the actual live character should stay exactly as they are until the player buys it and equips it.

For one Statistic, you can easily ask that question directly.

---

## Previewing one Modifier

Suppose the player currently has 20 damage and is looking at a weapon that would add 8:

```js
damage = new CatalystStatistic(20);

var _shop_bonus = new CatalystModifier(8, eCatMathOps.ADD);
```

`_shop_bonus` is still detached. Pass it to `Preview()` to calculate the Statistic as though that Modifier were attached:

```js
var _preview_damage = damage.Preview(_shop_bonus); // 28
var _live_damage = damage.GetValue();              // still 20
```

Nothing has been attached and the Statistic's normal current value hasn't changed. If the player closes the shop, there's nothing to undo.

Several detached Modifiers can be previewed against the same Statistic at once:

```js
var _preview_damage = damage.PreviewModifiers([
    new CatalystModifier(8, eCatMathOps.ADD),
    new CatalystModifier(0.20, eCatMathOps.MULTIPLY)
]);
```

Note how we are **storing the modifiers in an array** as we submit them. This uses the same calculation rules as the live Statistic, including layers, conditions, stacks, and any facts used by the evaluation. Every Modifier supplied to `Preview()` or `PreviewModifiers()` must be detached (i.e. not already added to an existing Statistic) because Catalyst is answering a hypothetical question, not temporarily moving a live Modifier around.

A single-Statistic preview is simple enough when one number is changing. But equipment, loadouts, policy packages, and similar choices often affect several Statistics at once, which is where Sets become useful.

---

## Previewing a whole model

A sword might change damage, attack speed and critical chance at once. Before the player equips it, the UI may need to answer:

> What would all of these stats look like if this package replaced the one I'm currently using?

A **CatalystSet** groups related Catalyst objects so one operation can work across the model. A **CatalystModifierSet** is a reusable package of Modifiers, such as one item's collection of stat changes, that the Set can preview or apply.

### Building the Set

Suppose a character has three combat Statistics:

```js
damage = new CatalystStatistic(20)
    .SetIdentity("damage")
    .SetName("Damage");

attack_speed = new CatalystStatistic(1)
    .SetIdentity("attack_speed")
    .SetName("Attack Speed");

critical_chance = new CatalystStatistic(0.05, 0, 1)
    .SetClamped()
    .SetIdentity("critical_chance")
    .SetName("Critical Chance");
```

Treat the strings passed to `SetIdentity()` as stable IDs for the parts of this model: `"damage"` means the damage Statistic, `"attack_speed"` means attack speed, and so on. A packaged Modifier can then say “I belong on `damage`” without holding a direct reference to this particular character's damage Statistic.

Once a Statistic, Resource, or Effect Manager has been added to a Set, remove it from that Set before changing its identity. The Set relies on those IDs staying stable while the object belongs to it.

Now put those Statistics into one Set:

```js
combat_stats = new CatalystSet("combat_stats")
    .AddStatistic(damage)
    .AddStatistic(attack_speed)
    .AddStatistic(critical_chance);
```

The Set does **not** take ownership of them. Destroying `combat_stats` later won't destroy `damage`, `attack_speed`, or `critical_chance`. Think of a Set as simply a useful container.

A Statistic, Resource, or Effect Manager can only be a direct member of one `CatalystSet` at a time. If you want to move one to another Set, remove it from the first Set before adding it to the second.

---

## Packaging several Modifiers together

Now suppose the player's current sword gives +5 damage and +10% attack speed:

```js
sword_damage = new CatalystModifier(5, eCatMathOps.ADD)
    .SetTargetIdentity("damage");

sword_speed = new CatalystModifier(0.1, eCatMathOps.MULTIPLY)
    .SetTargetIdentity("attack_speed");

current_sword = new CatalystModifierSet("iron_sword")
    .AddModifier(sword_damage)
    .AddModifier(sword_speed);
```

`SetTargetIdentity()` tells the package which Statistic each Modifier is meant for. When this package is used with `combat_stats`, Catalyst can match `"damage"` to the Statistic whose identity was set to `"damage"`, and `"attack_speed"` to the Statistic whose identity was set to `"attack_speed"`.

The `CatalystModifierSet` doesn't attach or destroy those Modifiers by itself. It keeps the package together so the `CatalystSet` can work with all of them as one item.

Apply the package to the character:

```js
var _result = combat_stats.Apply(current_sword);

if (!_result.Succeeded()) {
    show_debug_message("Could not equip the sword");
}
```

`Apply()` is all-or-nothing. Before changing the character, Catalyst checks that every Modifier can find the Statistic named by its target identity. If even one target is missing or invalid, none of the package is attached, so pay attention to the result when testing, and check if you've made any spelling errors if the result isn't turning out how you expected.

Because Catalyst validates the whole package first, you don't end up with half an item equipped because the third Modifier failed.

---

## Previewing an upgrade without changing the game

Now the player highlights a different sword in the inventory, after having equipped the sword from the previous example. This one gives +8 damage and +20% critical chance:

```js
upgrade_damage = new CatalystModifier(8, eCatMathOps.ADD)
    .SetTargetIdentity("damage");

upgrade_crit = new CatalystModifier(0.2, eCatMathOps.ADD)
    .SetTargetIdentity("critical_chance");

upgrade_sword = new CatalystModifierSet("duelist_sword")
    .AddModifier(upgrade_damage)
    .AddModifier(upgrade_crit);
```

The player hasn't equipped the new sword yet, so we don't want to touch the live Statistics. Ask the Set to preview the swap instead:

```js
var _preview = combat_stats.PreviewSwap(current_sword, upgrade_sword);
```

`PreviewSwap()` works out what each incoming Modifier would affect and what the resulting values would be, but it doesn't remove the current sword or attach the new one.

In general, you would want to store the variables you are using to hold the Sets. A sword instance might have a variable holding the Modifier Set of its modifiers, and when the player equips it, you would store the Modifier Set alongside the other information about the sword. That way you can compare stuff easily without having to constantly try to rebuild the Sets from scratch. Exactly *how* you store it is up to the shape of your game and what feels natural to you.

Each affected Statistic gets a preview entry:

```js
var _entries = _preview.GetEntries();

for (var i = 0; i < array_length(_entries); i++) {
    var _entry = _entries[i];
    var _stat = _entry.GetStatistic();

    show_debug_message(
        _stat.GetName()
        + ": "
        + string(_entry.GetCurrentValue())
        + " -> "
        + string(_entry.GetPreviewValue())
    );
}
```

For this swap, the UI can show the player exactly which Statistics would change and what their resulting values would be.

Everything for the live build still remains untouched.

---

## Preview and apply use the same package

If the player accepts the upgrade, apply the exact swap you just previewed:

```js
var _old_sword = current_sword;

var _result = combat_stats.ApplySwap(_old_sword, upgrade_sword);

if (_result.Succeeded()) {
    current_sword = upgrade_sword;
    inventory.Add(_old_sword); // A hypothetical example of storing the old sword in your inventory, you would replace this with the actual code that your inventory uses
}
```

`ApplySwap()` removes the exact Modifiers from the outgoing package and attaches the incoming package in one all-or-nothing change.

The outgoing Modifiers are **detached, not destroyed**, so `_old_sword` is still a usable package afterward, containing the sword you just unequipped for the upgraded sword. You can store it in the inventory (as we've done hypothetically in this example), preview switching back to it, or equip it again later.

A Set swap detaches modifiers, instead of trying to destroy them, because equipment packages are often meant to remain reusable.

---

## A preview can explain why part of a package doesn't fit

A preview can still be useful when part of a package is invalid.

Suppose an unfinished upgrade contains one valid damage Modifier and another Modifier targeting `"poise"`, which `combat_stats` doesn't contain. Build that package and preview it directly:

```js
unfinished_upgrade = new CatalystModifierSet("unfinished_upgrade")
    .AddModifier(
        new CatalystModifier(3, eCatMathOps.ADD)
            .SetTargetIdentity("damage")
    )
    .AddModifier(
        new CatalystModifier(1, eCatMathOps.ADD)
            .SetTargetIdentity("poise")
    );

var _preview = combat_stats.Preview(unfinished_upgrade);
```

The damage target can be previewed, while `"poise"` can't be matched. That makes this preview `PARTIAL`. Check the overall status when your UI needs to distinguish that from a completely valid or completely invalid package:

```js
switch (_preview.GetStatus()) {
    case eCatSetPreviewStatus.SUCCESS:
        // Everything could be previewed.
        break;

    case eCatSetPreviewStatus.PARTIAL:
        // Some targets worked and some did not.
        break;

    case eCatSetPreviewStatus.FAILED:
        // Nothing could be previewed.
        break;
}
```

`Succeeded()` is true only for `SUCCESS`.

When you need to show or log why something failed, inspect the diagnostics:

```js
var _diagnostics = _preview.GetDiagnostics();

for (var i = 0; i < array_length(_diagnostics); i++) {
    var _problem = _diagnostics[i];

    show_debug_message(
        "Target: "
        + string(_problem.GetTargetIdentity())
        + " outcome: "
        + string(_problem.GetOutcome())
    );
}
```

A real `Apply()` or `ApplySwap()` is stricter: if any Modifier can't find a valid target, Catalyst changes nothing.

---

## Previewing a package without a swap

Not every package replaces something. A skill screen might preview a passive bonus that isn't currently active.

```js
passive_bonus = new CatalystModifierSet("berserker_training")
    .AddModifier(
        new CatalystModifier(3, eCatMathOps.ADD)
            .SetTargetIdentity("damage")
    );
```

Use `Preview()` when there is only an incoming package:

```js
var _preview = combat_stats.Preview(passive_bonus);
```

If the player unlocks it later:

```js
combat_stats.Apply(passive_bonus);
```

Use the pair that matches the operation:

- `Preview()` / `Apply()` add one package.
- `PreviewSwap()` / `ApplySwap()` replace an outgoing package with an incoming one.

---

## A Set can also hold Resources and Effect Managers

CatalystSet isn't limited to direct Statistics. A character model might include health and an Effect Manager as well:

```js
hp = new CatalystResource(100)
    .SetIdentity("hp")
    .SetName("Health");

effects = new CatalystEffectManager(self)
    .SetIdentity("effects")
    .SetName("Status Effects");

player_model = new CatalystSet("player")
    .AddStatistic(damage)
    .AddStatistic(attack_speed)
    .AddResource(hp)
    .AddEffectManager(effects);
```

Resources and Effect Managers also need stable identities before they're added. The Set uses those IDs to recognise the same parts of the model later, especially during saving and loading.

Adding them to a Set doesn't give the Set ownership of their lifetimes. Destroying the Set doesn't destroy the Resource or Effect Manager.

---

## Giving the whole model one Fact View

Earlier we attached an `OracleFactView` directly to a Statistic. If a whole character model should see the same ongoing facts, doing that Statistic by Statistic is unnecessary.

Suppose these are the player's ongoing facts:

```js
player_facts = new OracleFacts({
    is_night : false
});

player_fact_view = new OracleFactView()
    .Add(player_facts);
```

Set the Fact View once on the Set:

```js
player_model.SetFactView(player_fact_view);
```

The Set passes that Fact View to the Statistics that belong to this Catalyst model. That includes Statistics Catalyst creates inside things such as Resources, Flows, and Effects.

A Resource maximum, Flow rate, or Effect application chance can all see the same player facts without you finding every one of those Statistics and assigning the view yourself.

If you later call:

```js
player_model.ClearFactView();
```

the Set forgets its shared Fact View and removes that view from the Statistics it currently manages. Catalyst-owned Statistics added later won't receive a Set-level Fact View either.

A Statistic supplied by your game from outside the Set is different. If a Resource or Effect is sharing such a Statistic, Catalyst leaves that Statistic's Fact View alone instead of silently changing something another part of your project owns.

---

## Giving the whole model one layer order

Custom layers are covered in the advanced Statistics guide, but Sets make them easier to manage across a model.

If every Statistic in the model should use the same layer order:

```js
player_model.SetLayerOrder([
    eCatStatLayer.BASE_BONUS,
    eCatStatLayer.EQUIPMENT,
    eCatStatLayer.AUGMENTS,
    eCatStatLayer.TEMP,
    eCatStatLayer.GLOBAL
]);
```

The Set remembers that order and gives it to the current and future Statistics that belong to this Catalyst model.

`ClearLayerOrder()` stops the Set from assigning that shared order from then on. It doesn't go back through existing Statistics and rewrite the order they already have.

---

## Refreshing a whole model

Sometimes you change several pieces of game state together and want the whole Catalyst model updated before the next system reads from it. For example, you might change several Oracle facts, then want every Statistic and Resource bound in the character model to reflect those new facts immediately.

Instead of manually refreshing every piece:

```js
var _refresh = player_model.Refresh();

if (_refresh.DidChange()) {
    // At least one Statistic or Resource in the Set changed.
}
```

The returned result also lets you inspect the individual Statistic and Resource refresh results when you need them.

---

## Next: advanced Statistics and Modifiers

At this point you can preview one Statistic directly, or use a Set when several related Catalyst objects need to be handled as one model. Set applications are all-or-nothing, swaps leave outgoing Modifier packages alive for reuse, and shared Fact View or layer configuration can live on the Set instead of being repeated across every Statistic.

Continue with **[Advanced Statistics & Modifiers](advanced-statistics-and-modifiers)** for timed Modifiers, modifier families, hard floors and ceilings, custom layers, callbacks, and the tools for inspecting more complicated calculations.
