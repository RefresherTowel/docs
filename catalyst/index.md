---
layout: default
title: Catalyst 2
nav_order: 4
has_children: true
redirect_from:
  - /catalyst/quickstart.html
  - /catalyst/integration.html
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

![Catalyst icon](../assets/catalyst_icon.png)
{: .text-center}

*Make your game numbers react*
{: .text-center}

**Catalyst 2** is the new version of Catalyst. It now manages statistics, resources and effects for your gameplay! 

What are statistics and resources?

Things like damage, armour, movement speed, health, mana, and stamina: numbers that often start as plain and simple values, then become harder and harder to manage as your game starts to demand more from them (things like multiple modifiers that can be added or removed, or groups of statistic affecting things like damage over time effects, or other frequently encountered game design scenarios like that).

At the centre of Catalyst are five numerical building blocks:

- A **Statistic** calculates a value such as damage, armour, movement speed, or maximum health.
- A **Modifier** represents one thing currently changing a Statistic, such as a weapon bonus, curse, upgrade, or temporary buff.
- A **Resource** stores a current amount inside a range, such as HP, mana, stamina, ammunition, or charge.
- A **Resource Flow** makes resources dynamically reactive, such as HP regen, poison effects, power consumption, etc.
- An **Effect** bundles everything together into one coherent package, with a defined lifetime and grouped behaviour.

They all work together. Statistics calculate the numbers your rules need, Modifiers describe where changes to those numbers come from, Resources hold the values that get spent and restored during play, Resource Flows tell Resources how to behave and Effects make full gameplay behaviours, like a timed poison or ammo recharge, easy to deal with.

I encourage you not to pigeon-hole these concepts into "RPG". A platformer can use them for things like jump height increases, or running speed increases, a city builder can use them for things like population and population growth, a roguelike can use them for augments or long term character growth, and so on. Anytime a game reaches for a number, there's a chance that Catalyst can make it flexible and exciting.

You don't need to do a lot of boilerplate setup to get Catalyst working, it's designed to be simple to use for beginners and extremely flexible for whatever advanced situations your game design requires.

>Catalyst is part of the **RefresherTowel Games** suite of libraries for GameMaker.
{: .note}

---

## Your first Catalyst setup

Suppose the player starts with 10 damage and an enemy starts with 100 HP, let's see how we would set that up:

**Players Create Event**
```js
damage = new CatalystStatistic(10);
```

**Enemies Create Event**
```js
hp = new CatalystResource(100);
```

Now suppose the player equips a sword that adds 5 damage:

```js
sword_bonus = new CatalystModifier(5, eCatMathOps.ADD);
damage.AddModifier(sword_bonus);
```

When the player attacks, ask the Statistic for the damage it currently calculates, then use that result to change the enemy's HP Resource:

```js
var _damage = damage.GetValue(); // 15
_enemy.hp.Decrease(_damage);

var _remaining_hp = _enemy.hp.GetCurrent(); // 85
```

You can see that setup and use is quite simple.

If the sword is unequipped, remove its Modifier:

```js
damage.DestroyModifier(sword_bonus);

var _damage = damage.GetValue(); // 10
```

This is obviously a quite simple scenario, but you can already see how easy Catalyst makes this kind of thing. Normally, there would be a lot of boilerplate you would have to write to allow this kind of thing, and you'd often need to rewrite and rewrite the system as you figure out new things you might want to do with your game.

Catalyst takes care of all of that for you.

You don't have to keep track of any `base_damage` values, or worry about whether you've permanently changed damage and can't remove the sword modifier, and you can add or remove as many modifiers as you like, while always having the end result be mathematically accurate.

---

## Effects tie related changes together

As game rules become more involved, several Catalyst pieces may belong to one "gameplay state" (an "effect" in other words).

An enemy with **burning** applied, for example, might damage HP over time, reduce a defence Statistic, last for five seconds, carry a `fire` tag that a cleanse can recognise, and needs to remove all of those changes when the burn ends.

Catalyst **Effects** allow you to group related temporary changes under one simple lifetime. Instead of your burn code separately remembering the damage-over-time rule, defence penalty, timer, and cleanup, the Effect becomes the thing they belong to. When the burn ends, its related changes end with it.

Later you'll also meet **Resource Flows**, which are Catalyst's way of moving Resources over time (think health regen, stamina drain, city growth, or even a plants watering meter). Effects can combine all of these to create easily composable behaviours that allow a huge amount of design expression in your games with a relatively small amount of code.

---

## What to look at next

This documentation builds outward from those core pieces as new problems appear and teaches you how to use Catalyst from the ground up.

Start with **[Statistics & Modifiers](statistics-and-modifiers)** to learn how calculated values change through equipment, buffs, debuffs, stacking, layers, limits, and rounding.

Then move to **[Resources](resources)** for values with a current amount that gets spent and restored. Once Statistics and Resources are familiar, **[Situational Statistics](situational-statistics)** shows how calculated values can react to ongoing game state or to one particular question, including publishing Resource state into Oracle facts.

**[Resource Flows](resource-flows)** combine both ideas: a Flow changes a Resource over time, while the Flow's rate is itself a Statistic that can use Modifiers and situational rules.

**[Effects](effects)** bring those pieces together into gameplay states with shared duration and cleanup. The later guides cover Sets and previews, advanced Statistic rules, saving and loading, and complete gameplay patterns.

{% include library-footer.html %}
