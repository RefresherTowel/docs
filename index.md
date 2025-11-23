---
layout: default
title: Home
nav_order: 1
---

# Documentation Hub for RefresherTowel Games Systems

Welcome to the hub for all documentation related to the various GM-focused systems created by RefresherTowel Games. First I'll give a short overview of what each available system is.

## Statement

- **[Statement](/docs/statement/)**

Hve you ever found yourself writing tons of if statements trying to wrangle your player character so that their running, climbing, attack and jumping actions all function correctly?

Ever had animations bleed from one action to the next by accident?

Well, **Statement** is the solution for you!

Statement is a simple, but easily expandable state machine engine designed for practical use with flexibility for more advanced users in mind. Get a fully functioning state machine running with 5 simple lines of code, or delve into the hidden depth of the engine to build complex functionality with ease.

Initialise a state machine with a simple `sm = StatementCreate(id)`, easily create states with `StateCreate(id, "idle");`, give the states functionality `_idle.AddUpdate(function() { /* idle state code */ });`, apply them to the state machine `AddState(_idle);` and finally run the state machine `sm.Update()`.

Or, if you're a pro, delve into the wide variety of options available to you, such as queued states, state stacks (push a UI menu to the core state machine stack, and then simply pop it off to instantly get easy menu functionality), custom states (Statement comes with Enter, Update, Exit and Draw states by default, but you can set your own and call them wherever you want, such as an Animation End state), work with the full history of states a state machine has cycled through, etc. Nearly limitless depth is at your fingertips.

## Pulse

- **[Pulse](/docs/pulse/)**

Do you want damage to your character triggering an animation on your healthbar?

What about a modular effect applied to your weapon that intelligently understands to apply itself when you attack?

Then the **Pulse** is the system for you! Pulse is a fully featured "signal" system, allowing you to make things listen for, and act, when certain events happen ("signals").

Designed with both beginners and advanced users in mind, you can quickly and easily add listeners to signals and send out signals for those listeners, via `PulseSubscribe(id, "signal", function() { /* Signal action */ })` and `PulseSend("signal")`, or you can dive into the feature-rich belly, posting consumable signals (perhaps for clicking UI components, no more activating multiple buttons stacked on top of each other), tagging signals to sub-divide what should react when, take advantage of deferred signal processing, applying priorities, "from" filters (only listen to a signal when it's emitted from a specific thing), there are tons of options at your disposal.

## Catalyst

- **[Catalyst](/docs/catalyst/)**

Are you having trouble dealing with the stats in your game?

Ever tried to add multiple buffs and debuffs that all act on different timers and effect a single stat, ending up with some serious spaghetti code?

**Catalyst** is here to save your day!

Catalyst is a feature-rich framework for handling modifiable stats, such as speed, damage, poison resistance, etc. At its core, Catalyst is very easy to use, but it has been designed with a huge amount of flexibility in mind.

Set up stats easily with `speed = CatStat(10);`, add modifiers like `CatMod(-1, eCatMathOps.ADD);` and retrieve up to date values with `speed.GetValue()` and you're done!

Or you can delve into the deep functionality, with layer stacking (apply all your "base" effects before "rune" effects, for instance), restrict stacks in various ways (only the highest effect in an effect family is applied), build your base value from other stats (have your base max hp built automatically from your strength * constitution + vitality, for example), set clamps, min and/or max values, preview changes non-destructively (easy to see how the stats change if you add a new armour piece, for instance, without having to actually apply the new armour piece), remove modifiers based on a variety of options (such as tags, so effects like "cleanse" become simple to implement), the list is endless.

## Echo

- **[Echo](/docs/echo/)**

Debugging doesn't have to be boring. Spice up your old `show_debug_message()` calls with **Echo**!

Echo makes debugging a breeze by allowing you *options* when debugging. Give each debug message a priority and filter what hits your console, or dump a full debug history for the current session to file, get stack tracing in your console, and even switch Echo off completely with the flip of a single bit!