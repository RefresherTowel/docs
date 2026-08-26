---
layout: default
title: Statistics & Modifiers
parent: Catalyst 2
nav_order: 1
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Statistics & Modifiers

Most of Catalyst starts with the same core problem: your game has a number, and you want it to change in a variety of different ways.

Suppose the player deals 10 damage. A sword adds 5, a rune increases the result by 20%, and a temporary weakness reduces it again. Later the sword is unequipped and the weakness wears off, so both changes need to disappear without disturbing anything else.

You can keep rebuilding that calculation yourself whenever the player's state changes, but Catalyst lets each contribution exist separately and works out the current result for you in an efficient and understandable way.

---

## Creating a Statistic

Start with the value the character has before anything else modifies it:

```js
damage = new CatalystStatistic(10);
```

`damage` is now a **Statistic** with a base value of `10`. Whenever the game needs the player's current damage, ask the Statistic for it:

```js
var _damage = damage.GetValue(); // 10
```

As equipment, buffs, debuffs, and other Modifiers come and go, `GetValue()` is how you get the correct value produced by everything that's currently affecting the Statistic.

A character will usually own several Statistics. Giving them names isn't required, but it makes them easier to recognise when you're inspecting or debugging them later:

```js
stats = {
    damage : new CatalystStatistic(10).SetName("Damage"),
    speed  : new CatalystStatistic(4).SetName("Move Speed"),
    armour : new CatalystStatistic(2).SetName("Armour")
};
```

---

## Adding a flat bonus

Now suppose the player equips a sword that adds 5 damage. The sword's contribution can be represented by a **Modifier** and attached to the damage Statistic:

```js
sword_bonus = new CatalystModifier(5, eCatMathOps.ADD);
damage.AddModifier(sword_bonus);
```

The damage is now 15:

```js
var _damage = damage.GetValue(); // 15
```

The underlying damage is still 10, with the sword contributing another 5 while its Modifier is attached. A penalty works the same way, so a weakness that removes 3 damage can use a negative `ADD` Modifier:

```js
weakness_penalty = new CatalystModifier(-3, eCatMathOps.ADD);
damage.AddModifier(weakness_penalty);
```

With both attached, Catalyst calculates:

```text
10 base damage
+5 sword
-3 weakness
-----------
12 damage
```

The sword and weakness haven't been collapsed into a permanent `+2`. They're still separate changes, so either one can disappear without you having to reconstruct the rest of the calculation.

---

## Percentage changes

Some effects should scale the result instead of adding a fixed amount. If a buff increases damage by 25%, use a `MULTIPLY` Modifier:

```js
damage = new CatalystStatistic(10);
power_buff = new CatalystModifier(0.25, eCatMathOps.MULTIPLY);
damage.AddModifier(power_buff);
```

For `MULTIPLY`, the Modifier value is the percentage change rather than the final multiplier. `0.25` means +25% (`1.25x`), `0.50` means +50% (`1.50x`), and `-0.20` means -20% (`0.80x`).

With the base damage at 10 and only this `0.25` Modifier attached, the Statistic returns 12.5:

```js
var _damage = damage.GetValue(); // 12.5
```

For ordinary stat changes, that gives you the two operations you'll use most often: `ADD` for flat changes and `MULTIPLY` for proportional ones.

---

## Removing a Modifier

A removable bonus should stop affecting the Statistic when the thing that created it goes away. Starting again with the simple sword example:

```js
damage = new CatalystStatistic(10);
sword_bonus = new CatalystModifier(5, eCatMathOps.ADD);
damage.AddModifier(sword_bonus);
```

When the sword is unequipped, remove that exact Modifier:

```js
damage.DestroyModifier(sword_bonus);
```

Damage immediately returns to 10. `DestroyModifier()` is the usual choice when that contribution is finished for good. If you want to keep the same Modifier object and attach it again later, use `DetachModifier()` instead.

Equipment, buffs, debuffs, talents, status effects, and similar removable changes are usually better represented by Modifiers than by direct changes to the Statistic's base value. Each one has its own lifetime and can disappear without rebuilding the rest of the calculation.

### Removing by source

Sometimes it's more convenient to identify Modifiers by where they came from instead of keeping a separate reference to each one. A Modifier can carry a source label:

```js
var _sword_bonus = new CatalystModifier(5, eCatMathOps.ADD)
    .SetSourceLabel("Iron Sword");

damage.AddModifier(_sword_bonus);
```

Later, you can destroy every Modifier on that Statistic with the matching label:

```js
damage.DestroyModifiersBySourceLabel("Iron Sword");
```

Source labels are useful when a readable name is enough. Catalyst can also remember the exact object that created a Modifier, or extra source information supplied by your game. Those options become useful later when several Modifiers came from the same item, status effect, enemy, or gameplay system.

---

## Changing the base value

Not every change belongs in a Modifier. Suppose the character permanently gains 2 base damage when they level up. There's nothing to unequip or cleanse later because the character's underlying damage has actually changed.

In that case, change the Statistic itself:

```js
damage.ChangeBaseValue(2);
```

A base value of 10 is now 12, and any attached Modifiers are calculated from that new base. If you already know the exact value you want, you can replace it directly instead:

```js
damage.SetBaseValue(20);
```

Change the **base value** when the underlying stat itself changes, and use a **Modifier** when some separate thing is currently affecting that stat. Games will occasionally have reasons to blur that line, but keeping the distinction clear makes most stat systems much easier to work with.

---

## Timed Modifiers

Suppose a haste pickup gives +30% movement speed for five seconds.

Catalyst lets you do this through the `CatalystCountdownTracker`. Catalyst creates a default global countdown tracker when your game boots. You can reference it via the macro `CATALYST_COUNTDOWN`. Everything timed within Catalyst subscribes to this global countdown tracker by default, and the tracker counts in terms of frames by default (so one "tick" for the tracker corresponds to one game frame, exactly like a Step Event).

Let's setup a modifier that lasts for exactly 5 seconds.

```js
move_speed = new CatalystStatistic(5)
    .SetName("Move Speed");

haste = new CatalystModifier(0.3, eCatMathOps.MULTIPLY, game_get_speed(gamespeed_fps) * 5);

move_speed.AddModifier(haste);
```

You can see that we setup the Statistic and Modifier in exactly the same way as before, with the exception being that we've added a third argument to the `CatalystModifier()` constructor. This is the `_duration` argument, and it tells the Modifier how many "ticks" of the countdown tracker it is assigned to should pass before the Modifier removes itself automatically.

The argument we are providing for `_duration` is the `game_get_speed()` function. This function is a built in GM function, and providing it with the argument `gamespeed_fps` asks: "How many frames is considered a second in this project". GM defaults to 60, but it doesn't matter if you change it, as the result from this function will always be the amount of frames in a second. Then we multiply it by 5 to get the number of frames in 5 seconds for this project.

So, the Modifier now counts down for five seconds and destroys itself when its duration reaches zero.

You can also manually set the current and maximum duration for a Modifier later on with the `SetDuration()` method:

```js
haste.SetDuration(game_get_speed(gamespeed_fps) * 10);
```

This would increase the duration of the Modifier to 10 seconds.

A negative duration means the Modifier is permanent, which is the default setting for Modifiers, so neglecting to provide the third `_duration` argument and not calling `SetDuration()` means the corresponding Modifier will be permanently attached until you manually remove it.

### Refreshing the timer

If another haste pickup should restart the existing duration rather than create another Modifier, we use `ResetDuration()` to reset the duration:

```js
haste.ResetDuration();
```

`ResetDuration()` restores the duration to the maximum last supplied through `SetDuration()`.

### Using a different clock

As we established before, timed Modifiers use `CATALYST_COUNTDOWN` unless you give them another tracker:

```js
cutscene_clock = new CatalystCountdownTracker();
cutscene_clock.StartAutomatic(eCatCountdownMode.DELTA_TIME);

haste.SetCountdownTracker(cutscene_clock);
haste.SetDuration(5);
```

A new countdown tracker starts in manual mode, so this example starts `cutscene_clock` explicitly before moving the timed Modifier onto it. We have also set this custom tracker to use delta time. When a tracker is using delta time, it "ticks" once per second, rather than once per frame. This means that instead of having to call `game_get_speed()` to time a Modifier by seconds, we can simply provide `5`, and the Modifier will last for 5 seconds.

We can also set the global Catalyst countdown tracker to delta time if we wish:

```js
CATALYST_COUNTDOWN.StartAutomatic(eCatCountdownMode.DELTA_TIME);
```

This would make it so that everything subscribed to the global tracker counts down in seconds instead of frames.

There are more ways we can alter the way time works in Catalyst. The [Resource Flows](resource-flows) guide covers countdown trackers in more detail.

---

## When order matters

Now suppose the player has 10 base damage, a sword that adds 5, and a rune that increases damage by 20%.

If the sword applies first, you get:

```text
(10 + 5) × 1.20 = 18
```

If the rune applies first, you get:

```text
(10 × 1.20) + 5 = 17
```

Neither answer is inherently correct because it depends on the rules of your game.

Catalyst solves this with two concepts: **layers** and **modifier order**. Each layer is evaluated before the next one, so you can decide that equipment should always be included before augments such as runes or talents:

```js
damage = new CatalystStatistic(10);

sword_bonus = new CatalystModifier(5, eCatMathOps.ADD)
    .SetLayer(eCatStatLayer.EQUIPMENT);

rune_bonus = new CatalystModifier(0.20, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.AUGMENTS);

damage.AddModifier(rune_bonus);
damage.AddModifier(sword_bonus);
```

Even though the rune was attached first here, `EQUIPMENT` is evaluated before `AUGMENTS`, so the sword's +5 is applied before the rune's +20%.

Catalyst evaluates the normal stat layers in this order:

1. `eCatStatLayer.BASE_BONUS`
2. `eCatStatLayer.EQUIPMENT`
3. `eCatStatLayer.AUGMENTS`
4. `eCatStatLayer.TEMP`
5. `eCatStatLayer.GLOBAL`

The names are intended to fit common game rules: early attribute or progression bonuses in `BASE_BONUS`, equipment in `EQUIPMENT`, runes or talents in `AUGMENTS`, temporary buffs in `TEMP`, and late global changes in `GLOBAL`. Catalyst only cares about the order, though, so your game can decide exactly what those layers mean.

>Modifiers use `eCatStatLayer.TEMP` by default. If the order doesn't matter for a Modifier, you don't need to assign a layer just for the sake of assigning one.
{: .note}

### Order inside a layer

Inside each layer, Catalyst applies every eligible `ADD` Modifier first, then every eligible `MULTIPLY` Modifier by default. 

For example, these two Modifiers are both in `EQUIPMENT`:

```js
damage = new CatalystStatistic(10);

var _flat = new CatalystModifier(5, eCatMathOps.ADD)
    .SetLayer(eCatStatLayer.EQUIPMENT);

var _percent = new CatalystModifier(0.20, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.EQUIPMENT);

// Attach the percentage first to show that attachment order doesn't decide the maths.
damage.AddModifier(_percent);
damage.AddModifier(_flat);

var _damage = damage.GetValue(); // 18
```

Even though the percentage Modifier was attached first, this layer produces `(10 + 5) * 1.20 = 18`.

If you wanted multipliers to be calculated first, you would call:

```js
damage.SetOrderModifier(eCatModifierOrder.MULTIPLY_FIRST);
```

And now Catalyst will run through all the multipliers in the layer before moving onto the additions. You could also set it to `eCatModifierOrder.ATTACHMENT_ORDER`, which would make it so that the modifiers are calculated in the order they are added to the statistic.

You can also retrieve the modifier order for a particular stat with:

```js
var _mod_order = damage.GetModifierOrder();
```

Which would return whatever `eCatModifierOrder` enum it was set to.

So layers decide the order between categories of changes. Then, within each layer, Catalyst evaluates your modifiers based on the modifier order you have set (again, it defaults to `eCatModifierOrder.ADD_FIRST`, so if that suits your game, no need to set a modifier order at all).

---

## Keeping a Statistic within limits

Some calculated values shouldn't be allowed outside a particular range. Accuracy, for example, might be represented from 0 to 1:

```js
accuracy = new CatalystStatistic(0.75, 0, 1)
    .SetClamped();
```

The second and third constructor arguments define the minimum and maximum, while `SetClamped()` tells Catalyst to enforce them. Even if attached Modifiers would push accuracy above 1 or below 0, `GetValue()` stays inside that range:

```js
accuracy.AddModifier(
    new CatalystModifier(0.50, eCatMathOps.ADD)
);

var _accuracy = accuracy.GetValue(); // 1
```

You can change the limits later with `SetMinValue()` and `SetMaxValue()` if the allowed range itself changes during the game.

---

## Rounding the result

Catalyst leaves Statistics unrounded by default, which means fractional results are allowed. If a particular stat should land on fixed steps, enable rounding explicitly:

```js
armour = new CatalystStatistic(10)
    .SetRoundingStep(1);
```

A step of `1` rounds to whole numbers, `0.1` rounds to tenths, and `0.01` rounds to hundredths. Clamping and rounding can also be combined when both rules belong to the same stat:

```js
accuracy = new CatalystStatistic(0.75, 0, 1)
    .SetClamped()
    .SetRoundingStep(0.01);
```

There's no need to enable rounding globally or by habit. Leave a Statistic unrounded unless its design actually calls for discrete steps.

---

## Stacking one Modifier

Sometimes one effect gets stronger in discrete stacks. Suppose each stack of Fury adds 2 damage, up to five stacks. You don't need five separate Modifiers for that:

```js
fury_bonus = new CatalystModifier(2, eCatMathOps.ADD)
    .SetMaxStacks(5);

damage.AddModifier(fury_bonus);
```

A Modifier starts with one stack. You can add another when the player gains one:

```js
fury_bonus.AddStacks();
```

Or set the current stack count directly:

```js
fury_bonus.SetStacks(4);
```

At four stacks, this Modifier contributes +8 damage. `SetMaxStacks(5)` prevents it from going above five stacks, while `SetStacks()` keeps the current value between zero and that maximum.

Multiplicative stacks have one extra choice: how repeated percentages combine. Suppose Momentum gives +10% speed per stack:

```js
momentum = new CatalystModifier(0.10, eCatMathOps.MULTIPLY)
    .SetMaxStacks(5)
    .SetStacks(3);
```

`MULTIPLY` uses **compound** stacking by default, so three stacks apply `1.10 * 1.10 * 1.10`, giving about +33.1%.

Some games want repeated percentage stacks to add together instead. Set the stack mode when that's the rule you mean:

```js
momentum.SetStackMode(eCatStackMode.ADDITIVE);
```

Now the same three `0.10` stacks become one +30% multiplier. `COMPOUND` models “multiply again for each stack,” while `ADDITIVE` models “add the stack percentages together, then multiply once.”

Here we're changing the stack count directly because something in the game has explicitly gained or lost a stack. The Situational Statistics guide later shows how Catalyst can work out the stack count dynamically from what's happening around the character instead.

---

## Putting it all together

A normal damage setup can now keep the underlying value on the Statistic while equipment and augments each describe their own contribution:

```js
damage = new CatalystStatistic(10)
    .SetName("Damage");

sword_bonus = new CatalystModifier(5, eCatMathOps.ADD)
    .SetLayer(eCatStatLayer.EQUIPMENT)
    .SetSourceLabel("Iron Sword");

damage.AddModifier(sword_bonus);

rune_bonus = new CatalystModifier(0.20, eCatMathOps.MULTIPLY)
    .SetLayer(eCatStatLayer.AUGMENTS)
    .SetSourceLabel("Rune of Force");

damage.AddModifier(rune_bonus);

var _damage = damage.GetValue(); // 18
```

When the sword is removed, only its contribution disappears:

```js
damage.DestroyModifier(sword_bonus);

var _damage = damage.GetValue(); // 12
```

The rune doesn't need to know that the sword exists, and the sword doesn't need to know about the rune. Each system owns the change it contributes, while the Statistic combines whatever is currently attached to it.

---

## Next: Resources

Statistics are useful when Catalyst should calculate a value from a base and the things currently modifying it. Some gameplay numbers have a different job: they need to remember how much of something is left.

Health, stamina, mana, shields, ammunition and charge are all examples. Their maximum might still be a modifiable Statistic, but taking damage or spending stamina should change a current amount rather than rewrite the formula that calculates the maximum, or having to track a bunch of modifiers to calculate the current value.

Continue with **[Resources](resources)** to add that second core kind of Catalyst number before we start making Statistics react to the wider game state.
