# Make your game numbers react!

**Health, speed, crop growth, buffs, whatever your game needs.**

Catalyst is a gameplay stat, resource and effect toolkit for GameMaker. It gives you reusable building blocks for numbers that need to change, react to game state, be spent and restored, move over time, stack, expire, or be previewed before anything actually changes.

At some point you decide your game needs some modifiable stats. Move speed, attack damage, jump height, crop yield, factory output, whatever. At first it's fine: you have a variable and you add to it.

Then you need a buff that only lasts five seconds. Then another bonus that shouldn't stack with the first. Then a debuff that depends on what enemy you're fighting. Then health regeneration, stamina drain, or a status effect that changes several things at once. Eventually you're staring at a pile of variables, timers and conditionals that are buggy, painful to extend, and end up limiting what ideas are practical to add.

I've been through that enough times that I got fed up and built Catalyst instead.

## The basic pattern easy

```js
damage = new CatalystStatistic(10);

var _damage = damage.GetValue(); // _damage holds 10

sword_bonus = new CatalystModifier(5, eCatMathOps.ADD);
damage.AddModifier(sword_bonus); // Add a simple modifier

var _damage = damage.GetValue(); // _damage now holds 15
```

Create a Statistic, then attach a Modifier at some point, and ask for the current value at any time. That's the original Catalyst at its simplest.

But there's room for aggressive growth from that starting point!

Catalyst 2 builds outward from that same idea into a much broader set of tools for managing gameplay numbers and the rules around them.

## Statistics and Modifiers

Statistics are calculated numbers such as damage, armour, movement speed, jump height, power supply, crop yield or maximum health that you might want to modify in some way during gameplay.

Modifiers represent the individual things *currently* changing those values.

Catalyst handles:

* Flat and percentage changes
* Custom evaluation layers and ordering
* Stacking, including compound and additive percentage stacks
* Modifier families where only the strongest, weakest, or all members apply
* Conditional Modifiers
* Stack counts calculated from current game state
* Custom calculated base values
* Clamping, rounding and post-processing
* Hard minimum and maximum rules
* Tags, source labels and source IDs for finding and removing related Modifiers
* Timed Modifiers
* `Explain()` results showing exactly how a Statistic reached its current value

Ok, that's a lot to take in! Let's just say that Catalyst lets you do essentially whatever you want to your stats, in a simple, dependable and easy way.

## Resources and Resource Flows

But not every gameplay number is something you calculate.

Catalyst 2 introduces **Resources**: Health, mana, stamina, ammunition, population, stored power and boost charge all have a **current amount** that changes during play. These are Resources.

```js
hp = new CatalystResource(100);
hp.Decrease(20);

var _hp = hp.GetCurrent(); // 80
```

Again, a super simple starting point, but Catalyst gives you a lot of tools to make those Resources dynamic and exciting.

For instance, Resource limits are themselves be driven by Statistics, so maximum health, carrying capacity, battery capacity or any similar bound can change with all the tools outlined for Statistics above.

Then **Resource Flows** enter the scene. They handle amounts that move over time:

* Health regeneration
* Poison damage
* Stamina drain and recovery
* Crop growth
* Population growth
* Heat accumulation
* Fuel consumption
* Factory production

A Flow's rate is itself, again, a Statistic. So that rate can have Modifiers, conditions, facts and all the other rules available to normal Statistics.

Your factory doesn't just produce `20` steel forever. It can produce 20, gain another 20 for each active production line, lose 50% output during a power shortage, then recover automatically when power comes back.

## Effects tie related changes together

Gameplay states often affect several things at once.

Giving your player the **burning** debuff might:

* Drain health over time
* Reduce defence
* Last for five seconds
* Carry `fire` and `debuff` tags
* Tick once per second
* Be removed early by a cleanse

A Catalyst Effect lets you do all of that, quickly and easily.

Effects own Modifiers and Resource Flows, handle durations and ticking, use application and per-tick chances, run callbacks, carry tags, and decide what happens when the same Effect is applied again.

When the Effect ends, Catalyst cleans up everything automatically.

The same system works not just for obvious things like poison, rage and stun, but also storms, blackouts, festivals, factory breakdowns, match-wide rules, temporary difficulty changes or anything else that represents one temporary state with several consequences.

## Make rules react to the rest of the game

Catalyst 2 uses **Oracle Facts** for situational rules.

A Modifier can depend on things like:

* The target being frozen
* The player being below 25% health
* The current weather
* A factory having enough power
* The target being a boss
* The player standing in water
* The current difficulty or game mode

Facts can represent ongoing state through an `OracleFactView`, or you can pass temporary information into `Evaluate()` when a calculation only depends on one particular situation.

Catalyst values can also publish themselves back into Oracle, allowing one calculated system to naturally feed another, creating truly dynamic, reactive effects and game state with a few simple lines of code.

That means you can build rules such as "+50% damage against frozen targets" or "migration rises while jobs and housing are available" without scattering special-case checks through the code that uses the final number.

## Preview changes without awkwardly editing things

Need an equipment comparison screen? A shop preview? A city policy screen? A vehicle upgrade menu?

You can preview detached Modifiers against a Statistic without applying them:

```js
var _preview = damage.Preview(new CatalystModifier(8, eCatMathOps.ADD));
```

For larger systems, `CatalystSet` and `CatalystModifierSet` let you package several related Statistics and Modifiers together.

For instance, a new weapon might change damage, attack speed and critical chance at the same time. Well, Catalyst can preview the entire package, compare it against the currently equipped package, hand you the data to show the player, and then perform the real swap when the player commits.

## Timing without a pile of timers

Catalyst has a shared Countdown Tracker for timed Modifiers, Flows and Effects.

It can run automatically using frames or delta time, or you can advance it manually when your game uses its own simulation clock (for instance, one turn in a turn-based game can be a "tick" of the timer).

Countdown Trackers can also be paused, time-scaled or created separately when different parts of the game need different clocks.

So a five-second buff, a turn-based poison, and a city simulation advancing once per day can all use the same Catalyst systems without being forced into the same timing model.

## Built for systems that grow

Catalyst 2 also includes:

* Change subscriptions for reacting when Statistics or Resources actually change
* Dynamic Resource bounds
* Custom Statistic layer orders
* Bulk cleanup through tags and source information
* Detailed evaluation and debug information
* Set-wide configuration and refresh
* Built-in support for saving and loading Catalyst state alongside your game's existing save data
* Oracle integration for sharing reactive state between systems

Catalyst doesn't try to dictate how your game should work. All it does is give you a set of tools that you can use to build simple, or highly complicated game rules out of.

A platformer can use it for movement speed and jump upgrades. A city builder can use it for population, housing and production. A roguelike can use it for buffs, resources and status effects. A racing game can use it for boost charge and vehicle upgrades.

Catalyst only cares about how the number behaves, not what genre the game belongs to.

## Echo included free

A purchase of Catalyst also includes **Echo**, my GameMaker debugging toolkit, at no additional cost.

Echo provides level-based logging, tags, filtering, optional stack traces, history, file dumps and in-game debugging tools.

## Bundles

You can also get Catalyst as part of the **Ignition Kit**, alongside Pulse and Statement, for a discount.

Or grab the **Full Suite Pass** to get access to all current and future RefresherTowel Games tools. The Full Suite Pass increases in price as more tools are released, so earlier purchases get the largest discount over buying everything separately.

## Documentation

Catalyst has full online documentation written to take you from the basic Statistic and Modifier pattern through Resources, Flows, situational rules, Effects, Sets, previews, saving and loading, and complete gameplay recipes.

**Catalyst Documentation:**
https://refreshertowel.github.io/docs/catalyst/

## Requirements

GameMaker 2024.8 or later.

## Support and feedback

If you run into a bug, want to request a feature, or just need help figuring out how to build something:

**GitHub Issues:**
https://github.com/RefresherTowel/Catalyst/issues

**Discord:**
https://discord.gg/qx6GtfVWJR

## Part of the RefresherTowel Games Toolkits

Catalyst is part of a growing collection of GameMaker libraries designed to work well together:

* **Whisper** - reactive narrative and dialogue systems inspired by games like Hades and Crusader Kings III.
* **Pulse** - signals, events and queries for communication between game systems.
* **Statement** - a state machine framework with a fully visual in-game debugger.
* **Fate** - weighted selection and drop systems, from simple loot tables to much more advanced setups.
* **Quill** - a free text box system with selection, context menus, multiline editing and more.
* **Echo** - advanced logging and in-game debug UI tools, included free with Catalyst.

Get **Pulse, Catalyst, Statement and Echo** together through the Ignition Kit, or grab the **Full Suite Pass** for the entire toolkit collection.

> **Existing Catalyst 1 users:** Catalyst 2 is a breaking redesign rather than a drop-in update. Check the v2 changelog before replacing Catalyst 1 in an existing project.
