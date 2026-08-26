---
layout: default
title: Resources
parent: Catalyst 2
nav_order: 2
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Resources

Statistics are good at answering questions such as “how much damage does this character deal?” or “what is their maximum health?” Catalyst starts with a base value, applies whatever Modifiers are relevant, and gives you the result.

Health itself has a different problem. If the player has 73 HP out of 100 and takes 20 damage, we don't want to be tracking a bunch of modifiers to make that change, it gets complicated and confusing fast. Instead, they've simply lost some of the health they currently have. Mana, stamina, ammunition, shields and charge meters usually behave the same way: they have a range, but something inside that range is being spent and restored during play.

Catalyst represents that kind of value with a `CatalystResource`.

---

## Creating a Resource

Suppose the player has 100 maximum HP and starts at full health:

```js
hp = new CatalystResource(100);
```

The first argument is the Resource's maximum. If you don't provide anything else, Catalyst uses a minimum of `0` and starts the current value at the maximum, so this Resource begins as:

```text
minimum:   0
current: 100
maximum: 100
```

You can read each part directly:

```js
var _current = hp.GetCurrent(); // 100
var _minimum = hp.GetMinimum(); // 0
var _maximum = hp.GetMaximum(); // 100
```

Unlike a Statistic, `GetCurrent()` isn't asking Catalyst to calculate “what HP should be.” It's reading an amount that can change over time, and the Resource remembers that current amount until something changes it again.

If the player should start partially injured, provide the starting current value as the second argument:

```js
hp = new CatalystResource(100, 65);
```

Now the Resource still ranges from 0 to 100, but `GetCurrent()` returns `65`.

You can also provide a different minimum as the third argument when a Resource shouldn't bottom out at zero:

```js
temperature = new CatalystResource(100, 20, -50);
```

That Resource starts with a maximum value of `100`, a current value of `20` and a minimum value of `-50`.

---

## Spending a Resource

Now the player takes 20 damage. Call `Decrease()` with the amount that should be removed:

```js
hp = new CatalystResource(100);

hp.Decrease(20);

var _current = hp.GetCurrent(); // 80
```

`Decrease(20)` tells the Resource to move its current value downward by a magnitude of 20. Catalyst reads the current value, subtracts 20, applies the Resource's bounds, then stores the resulting current value back on the Resource.

Starting from 100 HP, the change works out like this:

```text
current value: 100
requested decrease: 20
target value: 80
bounded result: 80
new current value: 80
```

The amount passed to `Decrease()` is always forced into a positive number. `Decrease(-20)` still decreases the Resource by 20 because Catalyst applies `abs()` to the argument. That makes calls such as `hp.Decrease(_damage)` safe when `_damage` represents “how much damage happened” rather than a signed mathematical delta.

To move the Resource upward again, use `Increase()`:

```js
hp.Increase(15);

var _current = hp.GetCurrent(); // 95
```

`Increase()` also treats its argument as a positive magnitude, but moves the current value upward instead.

### Why not just use `Change()`?

Catalyst also has a signed `Change()` method. Starting from the same Resource value, these alternatives move the current amount in the same direction by the same amount:

```js
hp = new CatalystResource(100);
hp.Decrease(20); // 80

hp = new CatalystResource(100);
hp.Change(-20); // 80
```

and the same is true in the other direction:

```js
hp = new CatalystResource(100, 50);
hp.Increase(20); // 70

hp = new CatalystResource(100, 50);
hp.Change(20); // 70
```

They aren't completely identical, because the returned change result remembers which method you called. `Change()` also keeps the signed value you supplied as `requested`. The Resource itself moves the same way when the values correspond.

Use `Increase()` and `Decrease()` when your code already knows the meaning of the action: healing increases HP, taking damage decreases HP, firing a weapon decreases ammunition. The call describes the gameplay intent and Catalyst handles the sign for you.

Use `Change()` when the value you're applying is already signed and either direction is meaningful:

```js
var _net_change = -8;
hp.Change(_net_change);
```

A positive result raises the Resource and a negative result lowers it.

---

## Resources stay inside their bounds (mostly)

A Resource usually won't move above its maximum or below its minimum.

Suppose the player has 90 HP and receives a 30-point heal:

```js
hp = new CatalystResource(100, 90);

hp.Increase(30);

var _current = hp.GetCurrent(); // 100
```

The requested increase would target 120, but the Resource's maximum is 100, so Catalyst stores 100 instead.

The same thing happens at the bottom of the range:

```js
hp = new CatalystResource(100, 15);

hp.Decrease(40);

var _current = hp.GetCurrent(); // 0
```

The damage targets `-25`, but the Resource stops at its minimum of 0.

You don't need to clamp these changes yourself. With the default `HARD` boundaries, the Resource keeps its current amount inside its minimum and maximum automatically.

---

## Breaking the limits

Occasionally, you might want to "overload" or "underload" a resource, such as a health increase that gives you more health than your maximum, or a temperature dropping below the usual minimum for a set piece.

Catalyst gives you options for this. You can change how a resource behaves when an attempt is made to push it past its bounds via:

```js
hp.SetMaximumBoundMode(eCatResourceBoundMode.OPEN);
hp.SetMinimumBoundMode(eCatResourceBoundMode.SOFT);
```

Catalyst allows three different boundary modes: `HARD`, `SOFT` and `OPEN`, and you can configure the minimum and maximum boundaries differently.

`HARD` is the default, and the usual way you want resources to behave. If an attempt is made to go past the boundary, the resource will get capped. We've already covered this behaviour above. If the boundary itself moves (you decrease maximum `hp`, for example) the resource will clamp the current value to the new bound.

`SOFT` means that normal resource movement gets capped, like the `HARD` mode, but you have the ability to push it past the boundaries through the `IncreasePastMaximum()`, `DecreasePastMinimum()` and `ChangePastBounds()` methods. These behave exactly as the `Increase()`, `Decrease()` and `Change()` methods we have already touched on, except they're allowed to cross a `SOFT` boundary.

Since `HARD` is the default, you can't create an overflowing (or underflowing) Resource immediately. For instance, this will implicitly clamp the current value:

```js
hp = new CatalystResource(100, 120);
hp.SetMaximumBoundMode(eCatResourceBoundMode.SOFT);
// hp is now 100 / 100
```

Instead, you have to manually set the current value after setting the boundary mode:

```js
hp = new CatalystResource(100);
hp.SetMaximumBoundMode(eCatResourceBoundMode.SOFT);
hp.SetCurrent(120);
// hp is now 120 / 100
```

The `Increase()`, `Decrease()` or `Change()` methods have specific behaviour when a Resource boundary is set to `SOFT`, for instance:

```js
// 120 / 100 with a SOFT maximum

hp.Increase(10); // stays at 120
hp.Decrease(10); // drops to 110
```

An `Increase()` method won't push the current value any higher if it's past the maximum boundary, the same as `Decrease()` won't push it any lower if it's past the minimum (you would call the `IncreasePastMaximum()`, `DecreasePastMinimum()` or `ChangePastBounds()` if you wanted that). It also won't clamp the current value to the maximum or minimum either.

`OPEN` means the boundary no longer restricts movement. The maximum and minimum still exist and are still used by Resource queries and helpers, but changes are free to move past them.

If you call the `SetCurrent()` method, it will respect `HARD` boundaries, but allow the value to go past the boundaries for either `SOFT` or `OPEN`.

If a Resource is currently overflowing, and you switch it back to a `HARD` boundary, it will immediately clamp back inside that boundary:

```js
hp = new CatalystResource(100);

hp.SetMaximumBoundMode(eCatResourceBoundMode.SOFT);
hp.SetCurrent(120); // 120 / 100

hp.SetMaximumBoundMode(eCatResourceBoundMode.HARD);
// hp is immediately clamped to 100 / 100
```

If the boundary is `SOFT` or `OPEN`, then no clamping occurs:

```js
hp = new CatalystResource(100);

hp.SetMaximumBoundMode(eCatResourceBoundMode.SOFT);
hp.SetCurrent(120); // 120 / 100

hp.SetMaximum(80);
// hp is not clamped and so the final result is 120 / 80
```

## Finding out what actually changed

Sometimes knowing the final current value is enough, but combat and UI code often needs to know what actually happened. If the player at 90 HP receives 30 healing, for example, only 10 HP can really be restored before the Resource reaches its maximum.

Every method that changes a Resource returns a `CatalystResourceChange` describing that attempt:

```js
hp = new CatalystResource(100, 90);

var _change = hp.Increase(30);
```

For this heal, the useful methods are:

```js
_change.GetPrevious();  // 90
_change.GetRequested(); // 30
_change.GetTarget();    // 120
_change.GetApplied();   // 10
_change.GetCurrent();   // 100
_change.GetMinimum();   // 0
_change.GetMaximum();   // 100
_change.DidChange();   // true
```

Together, those methods describe the whole change: `GetPrevious()` tells you where the Resource started, `GetRequested()` is the amount you asked for, and `GetTarget()` is where that request would have taken the Resource without bounds. `GetApplied()` is the signed amount that really changed, while `GetCurrent()` is where the Resource ended up.

When overflow is possible, a healing number can display the amount actually restored rather than the amount requested:

```js
var _change = hp.Increase(30);
show_debug_message($"Healed for {_change.GetApplied()} HP");
```

Likewise, if 40 damage hits a character with only 15 HP remaining, the Resource reaches 0 and `_change.GetApplied()` is `-15`. The requested damage was 40, but only 15 points of Resource movement were possible before the minimum was reached.

> `GetApplied()` is signed: increases are positive and decreases are negative. If you only need the magnitude of damage actually removed, use `abs(_change.GetApplied())`.
{: .note}

### Attaching a reason or source

A Resource change can also remember why it happened. Pass a struct as the optional second argument:

```js
var _change = hp.Decrease(20, {
    reason : "attack",
    source : "Goblin"
});
```

Catalyst copies `reason`, `source` and optional `meta` values into the returned change result, so code handling the result can tell that this change came from an attack and which enemy caused it:

```js
_change.GetReason(); // "attack"
_change.GetSource(); // "Goblin"
```

Catalyst doesn't assign meaning to those values. They're there for your game to use. You might use `reason` to distinguish attacks from poison or scripted costs, `source` to identify the actor or object responsible, and `meta` for any extra information a particular system needs.

You don't need this extra information for ordinary changes, so only provide it when some other part of the game actually cares why the Resource moved.

---

## Reacting when a Resource changes

Sometimes another system needs to hear about Resource changes as they happen. A health bar, for example, may want to update when HP changes or when a maximum-HP Modifier changes the Resource's range.

Subscribe once:

```js
hp_subscription = hp.OnChange(
    function(_resource, _change) {
        show_debug_message(
            "HP: "
            + string(_change.GetPrevious())
            + " -> "
            + string(_change.GetCurrent())
        );
    }
);
```

The callback receives the Resource and the same `CatalystResourceChange` returned by the methods above. It runs when the current amount changes **or when the Resource's current minimum or maximum changes**.

When that observer is no longer needed:

```js
hp_subscription.Unsubscribe();
```

The returned `CatalystSubscription` is the same subscription handle used by Statistic `OnChange()` later in the docs.

---

## Setting an exact amount

Sometimes you aren't increasing or decreasing a Resource because you already know exactly what its current value should become. Use `SetCurrent()` for that:

```js
hp.SetCurrent(50);
```

`SetCurrent(50)` asks for a current value of exactly 50, then keeps that value inside the Resource's minimum and maximum just like every other change (assuming the default `HARD` boundary mode). If a boundary is set to `SOFT` or `OPEN`, then `SetCurrent()` can cross the boundary.

Use it for things such as loading saved state, resetting a round to a known value, or applying a mechanic that explicitly sets a Resource rather than changing it by a delta.

You might be tempted to calculate the difference yourself and call `Change()`:

```js
hp.Change(50 - hp.GetCurrent());
```

but if your rule is simply “HP is now 50,” `SetCurrent(50)` says that directly and leaves Catalyst to handle the range.

---

## Filling and emptying a Resource

For the common cases where a Resource should jump directly to one of its bounds, you don't need to look up that bound first.

`Fill()` sets the current value to whatever the Resource's maximum is right now, unless the Resource is overflowing, in which case it won't alter the value:

```js
hp.Fill();
```

`Empty()` sets it to whatever the minimum is right now, unless the Resource is underflowing, in which case it also won't alter the value:

```js
hp.Empty();
```

If a Resource is overflowing, and you wanted to force it to the maximum, you would do this:

```js
hp.SetCurrent(hp.GetMaximum());
```

The same goes for forcing it to the minimum if it's underflowing:

```js
hp.SetCurrent(hp.GetMinimum());
```

Both methods return the same kind of change result as `Increase()`, `Decrease()`, `Change()` and `SetCurrent()`.

---

## Asking about the current state

Resources have a few small helpers for common gameplay and UI questions.

To check whether the Resource has reached either end of its range:

```js
if (hp.IsEmpty()) {
    // The current value is at the minimum.
}

if (hp.IsFull()) {
    // The current value is at the maximum.
}
```

For a normal 0-to-100 HP Resource, `IsEmpty()` means HP is 0 and `IsFull()` means HP is 100. These methods use the Resource's actual current minimum and maximum, so they still work when those bounds change later. If the Resource is overflowing, `IsFull()` returns true, and if it's underflowing `IsEmpty()` returns true. To get the overflow/underflow values, you would call `GetOverflow()` or `GetUnderflow()`:

```js
var _overflow = hp.GetOverflow();
var _underflow = hp.GetUnderflow();
```

`GetMissing()` tells you how much room remains before the maximum:

```js
hp = new CatalystResource(100, 65);

var _missing = hp.GetMissing(); // 35
```

It’s handy when an item can restore “up to 25 HP” or when UI needs to know how much of a pool can still be filled. It will never go negative, even if the Resource is overflowing.

`GetFraction()` returns the current position between the Resource's minimum and maximum as a value from 0 to 1:

```js
var _health_fraction = hp.GetFraction();
```

With 65 HP in a 0-to-100 range, it returns `0.65`, which a health bar can use directly for its fill amount without repeating the range calculation elsewhere. This method clamps the output to between 0 and 1. This is so that an overflowing health bar won't suddenly draw past its boundaries, or other situations like that. If you want to get the actual raw fraction of the Resource, use `GetRawFraction()`:

```js
var _health_raw_fraction = hp.GetRawFraction();
```

With 120 HP in a 0-to-100 range, it would return `1.2`. The same goes for underflowing, -20 HP would return `-0.2`. If minimum and maximum are equal, it will always return `1`.

The calculation uses both bounds rather than assuming the minimum is zero. A Resource ranging from `-50` to `50` with a current value of `0` is halfway through its range, so both `GetFraction()` and `GetRawFraction()` return `0.5`.

---

## The maximum can be modified too

A Resource's range doesn't have to stay fixed. The current amount can remain mutable while the maximum responds to equipment, buffs or other stat rules.

Suppose the player has 100 HP and equips a Vitality Charm that grants +25 maximum HP. You might think about keeping a separate `max_hp` Statistic and manually synchronising the Resource with it, but Catalyst already represents a Resource's minimum and maximum as Statistics internally, so the Modifier system you've learned can act directly on those bounds.

Create the Resource normally:

```js
hp = new CatalystResource(100);
```

Then create the same kind of Modifier we'd use on any other Statistic:

```js
vitality_charm = new CatalystModifier(25, eCatMathOps.ADD)
    .SetLayer(eCatStatLayer.EQUIPMENT)
    .SetSourceLabel("Vitality Charm");
```

Instead of attaching it to a standalone Statistic with `AddModifier()`, attach it to the Resource's maximum with `AddMaximumModifier()`:

```js
hp.AddMaximumModifier(vitality_charm);
```

Now:

```js
var _maximum = hp.GetMaximum(); // 125
```

A Resource uses a Statistic to calculate its maximum, so `AddMaximumModifier()` puts this Modifier onto that maximum-HP calculation. The same rules you already know apply: its maths operation, layer, and stacks all affect the maximum. You don't need to work with the underlying Statistic directly for an ordinary max-HP bonus.

The current amount doesn't automatically fill when the maximum grows. The charm changes how much HP the player **can** have, not how much HP they **currently** have:

```js
var _current = hp.GetCurrent(); // 100
var _maximum = hp.GetMaximum(); // 125
```

If the design says equipping the charm should also heal the player, that's a separate gameplay action and you can express it separately with `Increase()` or `Fill()`.

### Removing a maximum Modifier

Remove the exact Modifier when the charm is unequipped:

```js
hp.DestroyMaximumModifier(vitality_charm);
```

The maximum returns to 100.

Now consider a character who had 120 HP when the charm was removed. Their new maximum is only 100, so 120 is no longer a valid current value. When `DestroyMaximumModifier()` removes the bonus, Catalyst immediately brings current HP back inside the new range if the maximum boundary is set to `HARD`:

```text
before charm removal:
current: 120
maximum: 125

charm removed:
new maximum: 100

after removal:
current: 100
maximum: 100
```

When using the default `HARD` boundary mode, you don't need to manually clamp current HP when maximum-HP Modifiers change through the Resource API. Catalyst brings the current amount back inside the newly calculated range as part of that bound change.

If the boundary is `SOFT` or `OPEN`, the current value won't change, allowing you to keep the excess rather than having it secretly clamp because you changed the boundary. This is useful for resources like carrying capacity, or, as we can see here, maximum health.

`GetLastChange()` lets you inspect the most recent Resource change, including one caused by the Resource having to move back inside changed bounds:

```js
var _last_change = hp.GetLastChange();
```

Before anything has changed the Resource, `GetLastChange()` returns `undefined`. Afterward it returns the same `CatalystResourceChange` used everywhere else. If the current amount had to move because a bound changed, the result reports `eCatResourceOperation.RECONCILE`, so code that cares about the cause can distinguish “maximum HP shrank” from “something called `Decrease()`.”

---

## Using an existing Statistic as a bound

Sometimes maximum HP already exists as a Statistic because several systems need to work with it directly. In that case, pass the Statistic itself to the Resource:

```js
max_hp = new CatalystStatistic(100)
    .SetName("Maximum HP");

hp = new CatalystResource(max_hp, 100);
```

The Resource now uses that exact Statistic as its maximum, so if equipment changes `max_hp`, `hp.GetMaximum()` sees the same result without a second copy to keep synchronized.

While the Resource is using that shared `max_hp` Statistic, `hp.SetMaximum()` is deliberately rejected. Otherwise a call on `hp` could quietly replace the very Statistic that the rest of your game still expects to control maximum HP. If the Resource should stop sharing `max_hp`, make that change explicitly:

```js
hp.UnbindMaximumStatistic();
hp.SetMaximum(120);
```

`UnbindMaximumStatistic()` stops sharing `max_hp` and gives the Resource a new maximum Statistic starting at the value `max_hp` currently calculates. The same pattern is available for minimum bounds.

Share an existing Statistic when other systems should continue controlling that same maximum. Use `SetMaximum()` or `SetMinimum()` when the Resource's own bound is the thing you want to change.

---

## Updating a Resource after a shared bound changes

When you read a Resource, Catalyst checks the latest values of its minimum and maximum and brings the current amount back inside them if the boundary is using the default `HARD` mode. `SOFT` and `OPEN` won't change the current value. Ordinary gameplay therefore doesn't usually need a separate update call.

`Refresh()` is useful when the Resource is sharing a bound Statistic owned elsewhere and you want that check to happen **now**, before some later system reads the Resource. For example, if another system has just changed the shared `max_hp` Statistic:

```js
max_hp.ChangeBaseValue(20);

var _change = hp.Refresh();

if (_change.DidChange()) {
    show_debug_message(
        "HP or its bounds changed during refresh"
    );
}
```

`Refresh()` updates the Statistics used for the Resource's bounds, then makes sure the current amount still fits inside the resulting range if appropriate. The returned `CatalystResourceChange` reports the same current-value and bound changes that `OnChange()` receives.


---

## Changing the base bounds

Modifiers are appropriate when some separate thing is temporarily affecting a Resource's range. If the underlying range itself changes, use `SetMaximum()` or `SetMinimum()` instead.

For example, if a permanent upgrade changes the character's base maximum HP from 100 to 120:

```js
hp.SetMaximum(120);
```

That changes the base value of the Resource's maximum Statistic. Any Modifiers attached to the maximum are then calculated from the new base, just as they would be on an ordinary Statistic.

The same rule of thumb from the Statistics page applies here:

- use `SetMaximum()` or `SetMinimum()` when the Resource's underlying bound has changed,
- use `AddMaximumModifier()` or `AddMinimumModifier()` when another game element is currently modifying that bound.

For most Resources, the minimum will stay at 0 and you'll mainly work with the maximum, but Catalyst supports both sides of the range in the same way.

---

## A complete HP example

A basic HP setup using these pieces might look like this:

```js
hp = new CatalystResource(100);

vitality_charm = new CatalystModifier(25, eCatMathOps.ADD)
    .SetLayer(eCatStatLayer.EQUIPMENT)
    .SetSourceLabel("Vitality Charm");

hp.AddMaximumModifier(vitality_charm);
```

The player starts with 100 current HP out of a possible 125. When an enemy attacks:

```js
var _damage_change = hp.Decrease(30, {
    reason : "attack",
    source : "Goblin"
});
```

The Resource now has 70 current HP. A health bar can read its normalised fill amount with:

```js
var _health_fraction = hp.GetFraction(); // 70 / 125 = 0.56
```

Later, a healing item can restore HP without exceeding the current maximum:

```js
var _healing_change = hp.Increase(80, {
    reason : "healing_item",
    source : "Health Potion"
});
```

The requested heal is 80, but only 55 can fit, so the Resource ends at 125 and `_healing_change.GetApplied()` is `55`.

Nothing in the damage code needs to know how maximum HP is calculated, and the Vitality Charm doesn't need to know how much HP the player currently has. The Resource remembers current HP, while the Statistics behind its minimum and maximum decide the range that current HP is allowed to occupy, depending on the boundary mode that you have selected for the maximum and minimum.

---

## Next: Situational Statistics

Statistics and Resources now cover Catalyst's two basic kinds of number: calculated values and mutable current amounts. The next problem is making those calculations care about what is happening elsewhere in the game.

A damage bonus might only apply to frozen targets, armour might rise when the player's HP Resource falls below 30%, or movement speed might gain a stack for every burning enemy nearby.

Continue with **[Situational Statistics](situational-statistics)** to give Modifiers conditions and fact-driven stacks, ask one-off questions with `Evaluate()`, and let ordinary `GetValue()` calls react to ongoing state such as the player's current HP.
