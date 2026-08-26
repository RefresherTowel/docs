---
layout: default
title: Saving & Loading
parent: Catalyst 2
nav_order: 8
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Saving & Loading

## A brief primer on functions and methods

Before we get into saving and loading with Catalyst, it's important we have a quick primer on how GM deals with functions.

When data is saved to disk in JSON format, all functions and methods are stripped out of it. There are various comp-sci reasons why, but suffice it to say, you can only store "plain" data when saving. This isn't a Catalyst-specific limitation, it's a simple fact about GM's normal "serialisation" (converting your game data into a format that can be stored externally to the program) process.

However, there are some workarounds that we can deal with, and in order to understand how these workarounds work, and what you need to do when saving and loading Catalyst data, we need to learn a bit about how functions work in GM.

We have three (and a half) types of function declarations in GM:

1) A "script function":

```js
// scr_functions

function MyFunction() {
    // Some code
}
```

This is a named function that appears in a script asset. It has global scope, and importantly for us, is associated with a script index.

2) A "method variable":

```js
// obj_player Create Event

MyMethod = function() {
    // Some code
}
```

These are called "methods" in GM and they are functions assigned to a variable. Their scope is bound to the current scope (`self`) when they are created (i.e. if in `obj_player`, as this example, the scope will be the player instance). The actual variable `MyFunction` simply holds a reference to the method function.

3) An "inline" or "anonymous" method:

```js
// Anywhere
SomeApi(function() {
    // Some code
});
```

The anonymous method is **not** `SomeApi`, the anonymous method is the actual `function() {}` you can see provided as the *argument* for `SomeApi`. These are methods like type 2, with the exception that we aren't **directly** assigning them to a variable when we create them (although, technically they will almost always be assigned to a variable, in this example the `SomeApi` function will store the anonymous function in an argument variable, which we can then use inside the `SomeApi` function code). These act almost identically to type 2: they are scoped to the instance that they are created in.

3.5) Bound methods:

```js
// Anywhere

MyBoundMethod = method(some_scope, MyFunction);

// Or using a method
MyBoundMethod = method(some_scope, MyMethod);

// Or an anonymous function
MyBoundMethod = method(some_scope, function() {

})
```

Bound methods are slightly different in that they take an existing function or method bind it to a new scope (i.e. changing the scope from an instance of `obj_player` to an instance of `obj_sword` or something like that). You would still call it the same as any other function/method: `MyBoundMethod()`

---

## Why do we care about this?

GM treats each of those differently, and that means we have to handle them differently when we save Catalyst.

### Script functions.
Catalyst can automatically restore any script functions you call in your Catalyst code, so these should be the functions you reach for by default.

### Script functions assigned a new scope through `method()`.
Catalyst can restore the *function* but it can't restore all arbitrary possible *bound scopes*, so that has to actively be recreated during loading (there are a few circumstances where Catalyst can automatically restore the scope).

### Method variables.
Catalyst can't restore these, and will need the function to be either recreated or reassigned during load

### Anonymous methods.
Catalyst can't restore these, and will need the function to be recreated during load

### Method variables and anonymous methods assigned a new scope through `method()`.
Catalyst can't restore the function *or* the binding, and so both will have to be recreated during load.

---

## Bindings are the real difficulty

The majority of code for Catalyst can get away with being a script function, so you should naturally use those if you want to have your saving and loading *just work* without you doing anything extra. Methods and anonymous methods need to be recreated during load, but this is usually fairly simple. Bindings are where the real difficulties set in. 

Let's say you have a weapon instance, and you bind a callback (a callback is just a function/method being provided to Catalyst that Catalyst will execute at some later point) to that weapon instance. Instance IDs and struct references are "runtime identities" (meaning, they are created fresh each time the game runs), not persistent identities you can rely on surviving a save and reload. After reconstructing your game state, the new weapon identity may represent the same weapon in your game, but it's not necessarily the same runtime value the original method was bound to.

A method can't be bound to something that doesn't exist.

How your game handles this will be up to you, as Catalyst can't predict what your intention was, or what the possible solutions are that make sense in the context of your game.

---

## Now on to the actual Catalyst saving and loading

Catalyst tries very hard to make saving and loading a seamless experience for you.

Build the player, enemy, item, or whatever else like we have been throughout this documentation. When you want Catalyst to save a group of related Statistics, Resources, and Effect Managers, put them in a `CatalystSet` and give the Set and its members identities that you'll use again when the game loads.

A basic player setup might look like this:

```js
damage = new CatalystStatistic(20)
    .SetIdentity("damage");

hp = new CatalystResource(100, 75)
    .SetIdentity("hp");

effects = new CatalystEffectManager(self)
    .SetIdentity("effects");

player_set = new CatalystSet("player")
    .AddStatistic(damage)
    .AddResource(hp)
    .AddEffectManager(effects);
```

The identities are how Catalyst recognises the same parts when you load later. The save (after it has been created) will say it has state for `"hp"`, and you have a Resource that you have set the identity of to `"hp"` above, so Catalyst knows that the `"hp"` data in the save belongs to the `"hp"` resource that you have created and given that identity.

For the Set itself, and for each Statistic, Resource, or Effect Manager you add to it, use a non-empty string or a finite number as the identity. Strings are usually the easiest option, but enums can be useful if you like the autocomplete factor for them.

---

## Saving the Set

At the point that you want to save, you then ask the appropriate Set (or Sets) for its current state:

```js
var _capture = player_set.CaptureState();
```

`CaptureState()` returns a capture result. The result gives you the ordinary GML structs and arrays that you can pass into the save data you already have:

```js
var _capture = player_set.CaptureState(); // We attempt to save the player Set

if (_capture.Succeeded()) { // If it succeeds
    global.my_save_data.player_data = _capture.GetState(); // We store the state into our save data
}
```

Catalyst doesn't write the save file for you. It simply gives you a normal set of structs/arrays that can be inserted into your existing save system (if you are not using structs and/or arrays for your save system, then you would have to save the sets separately using `json_stringify()` and `json_parse()`, which you can read about in the manual [here](https://manual.gamemaker.io/monthly/en/GameMaker_Language/GML_Reference/File_Handling/Encoding_And_Hashing/Encoding_And_Hashing.htm)).

> How you wish to save and load your data is unique to your game and beyond the scope of this Catalyst documentation to instruct you on. In general, you would be using something like JSON or buffers to create your save data, and you would simply store the Catalyst data alongside/inside your existing save structure somewhere. Ini save files are not appropriate for this kind of data. There are many tutorials out there that cover sensible ways to store your game data if you need help with the overall system.
{: .note}

If `CaptureState()` fails, Catalyst found something in the Set that it can't safely rebuild later. The cases that can cause that are covered further down the page.

---

## Checking whether saving succeeded

`CaptureState()` returns a capture result struct with various methods you can use to check the results of the save. We've already used two so far: `Succeeded()` and `GetState()`.

`GetState()` is the ordinary JSON-safe Catalyst state made from structs and arrays that you should be putting into your save data.

If the capture fails, `GetState()` returns `undefined` and `Succeeded()` returns `false`, and the result can explain what went wrong using `GetReport()`:

```js
var _capture = player_set.CaptureState();

if (!_capture.Succeeded()) {
    var _report = _capture.GetReport();
    show_debug_message(json_stringify(_report))
}
```

`GetReport()` returns JSON-safe data, so you can log it, include it in a bug report, or handle it however your project handles save errors.

Common capture problems include:

- the Set doesn't have a stable identity
- a Catalyst relationship points to a Statistic or Resource outside the Set
- a temporary Effect, Modifier, or Flow will need callback repair later but has no identity Catalyst can use for that repair
- a custom countdown tracker doesn't have an identity
- two different custom trackers used by the Set share the same identity
- capture was attempted while an Effect Manager was still finishing a change to its active Effects

Catalyst reports persistence problems that belong to Catalyst. Data you place in your own metadata still follows GameMaker's normal save rules, so if you're trying to save instance ids, struct references, asset references or any other non-persistent data, you have to deal with that accordingly.

---

## Loading the Set

When the player loads a save, you don't need to alter your existing Catalyst setup. You would still create your Statistics, Resources, Flows, Timers, Effect Managers, and so on, exactly as you did before you were trying to load:

```js
damage = new CatalystStatistic(20)
    .SetIdentity("damage");

hp = new CatalystResource(100, 75)
    .SetIdentity("hp");

effects = new CatalystEffectManager(self)
    .SetIdentity("effects");

player_set = new CatalystSet("player")
    .AddStatistic(damage)
    .AddResource(hp)
    .AddEffectManager(effects);
```

After you have done that, you then parse the saved JSON and restore it into that Set:

```js
// Retrieve the Catalyst JSON data you stored to disk
var _player_set_json = global.save_game_data.player_set; // For example

// Convert it from a json string into normal structs/arrays if necessary
var _player_set = json_parse(_player_set_json); // No need to do this if you have already done the json_parse() step when loading your game data in obviously

// Finally, restore it into your actual player_set that you created before
var _restore = player_set.RestoreState(_player_set);

// And the last step is checking if it all worked correctly and completing the restore
if (_restore.Complete()) {
    // Loading worked
}
```

For the basic player setup above, if there's no complications in the load process, that's the whole Catalyst side of the load.

Suppose the newly created `hp` starts at 75, but the save says the player had 28 HP. `Complete()` puts the saved value back into the `hp` Resource you already created.

The same thing happens to `damage` and the Effect Manager. Catalyst doesn't replace your `hp` or `damage` Resources/Statistics with newly created ones from the save data, it simply inserts the save data into your existing setup.

That also means anything else in your project that already refers to `hp` still refers to the same `hp` after loading.

---

## What happens to Effects, Modifiers, and Flows that were created during play?

The permanent parts of the your Set that you create during initialisation are only half the story.

The player might have saved while poisoned, or while a temporary damage bonus was active, or while a Resource Flow still had time remaining and these things do not exist at all when your normal player setup first runs.

If the save contains an active Effect, attached Modifier, or Flow that isn't currently present, `RestoreState()` prepares a new one from the saved Catalyst state. When `Complete()` succeeds, it's attached again with its saved duration, stacks, timers, values, and other Catalyst settings.

So the load has two parts:

```text
Your game builds the normal Catalyst setup you created.
Catalyst restores the previous Catalyst state into your existing setup.
```

For Effects, Modifiers, and Flows using **script functions that are not rebound with `method()`** Catalyst can do that without any help at all.

---

## Named script functions can be restored automatically

Imagine the player can catch fire. The Effect ticks once per second, and its tick behaviour is a script function declared in a Script asset:

```js
function BurnTick(_tick_duration, _result) {
    show_debug_message("Burn ticked");
}
```

The Effect can use it normally:

```js
var _burn = new CatalystEffect("burn", 5)
    .SetTickInterval(1)
    .SetOnTick(BurnTick); // Notice how we provide the script function *without* the () at the end

effects.AddEffect(_burn);
```

If the player saves with three seconds of `burn` remaining, the next game session starts with an empty Effect Manager as usual. `RestoreState()` rebuilds the saved Effect, restores its remaining duration, and finds the `BurnTick` script function again by name automatically.

You don't have to register `BurnTick` with a separate save system or recreate the Effect yourself.

GameMaker functions declared with `function Name(...)` in a Script asset are global script functions, which gives Catalyst a stable function name it can look up again when the game loads.

The same idea applies elsewhere in Catalyst. If a saved callback points to a named Script function and doesn't depend on a particular struct or instance being bound to it, Catalyst can find that function again.

**I highly recommend you use this shape as much as possible, as it means any saving and loading with Catalyst becomes extremely easy**. The rest of this page is essentially dealing with the times you can't (or simply decide not to) use a script function for a callable.

> A common error people make is **calling** the function instead of **supplying** the function. The key difference is whether or not you include the `()` after the function name. You should **NOT** include the `()` when supplying a named function to Catalyst. 
> This is **correct**:
> ```js
> .SetOnTick(BurnTick);
> ```
> This is **incorrect**:
> ```js
> .SetOnTick(BurnTick());
> ```
> Make sure you always do the former, and never the latter.
{: .note}

---

## Anonymous methods are different when Catalyst has to rebuild the object

Now write the same Effect with its tick function as an anonymous method:

```js
var _burn = new CatalystEffect("burn", 5)
    .SetTickInterval(1)
    .SetOnTick(function(_tick_duration, _result) {
        show_debug_message("Burn ticked");
    });

effects.AddEffect(_burn);
```

The Effect can still be saved. Catalyst can restore its identity, remaining duration, tick progress, and the rest of its Catalyst data.

What Catalyst can't do is recreate that anonymous method in a future run of the game. There is no named Script function for it to find again.

When that happens, `RestoreState()` tells you which callback is missing before anything is applied (using our example code from before):


## Most games will not need the rest of this page

If you use named Script functions for Catalyst callbacks wherever you can and you're not binding them to a new scope, Catalyst can find those functions again by itself. If your load setup creates the same permanent Statistics, Resources, Effect Managers, custom countdown trackers, and other game objects that it normally creates, then Catalyst won't run into any problems.

As long as you're trying to follow those guidelines then the rest of this page need not apply to you.

However, sometimes it's necessary (or simply easier) to use a method or an anonymous function, or you might need to bind a scope to something. In those cases, you'll need to perform some manual "repair" to restore the pieces of saved state that Catalyst **can't** finish rebuilding automatically.

A useful way to think about loading is:

1. Your game runs its normal setup and loads the game-owned things it normally loads.
2. Catalyst restores everything it can from the saved state.
3. If Catalyst still needs help with a temporary Effect, Modifier, or Flow, decide whether you actually care about keeping that temporary thing.
4. If you don't care about keeping it, you can choose to ignore it.
5. If you do care about keeping it, repair the missing piece.

> Use named Script functions for Catalyst callbacks wherever it makes sense. They are the easiest persistence path because Catalyst can normally restore them automatically.
{: .note}

---

## When to ignore something

Catalyst allows you to ignore certain problems, if it can rebuild a stable load state after removing that problem.

Imagine the player saves while a five-second slowing debuff has two seconds left.

Catalyst can save the Modifier itself: its value, duration, stacks, target Statistic, and the rest of its Catalyst state.

Suppose, however, that its condition was a function scoped to the enemy that caused the debuff, or the function was an anonymous function. Catalyst can't recreate that automatically.

Now you have a choice.

If this is an important temporary state for your game design that should survive loading, you can supply the missing function or figure out a way to deal with the method scope.

If you don't care whether two seconds of this debuff survives a save and load, you can tell Catalyst to leave the debuff out by ignoring it.

Ignoring is often the more practical choice for short combat Effects, temporary buffs, debuffs, and Flows that Catalyst can't recreate automatically. It's not impossible to save and restore those effects, indeed, the rest of this documentation is essentially telling you how to do that, but you don't need to rebuild every piece of temporary gameplay state just because Catalyst is capable of restoring it.

Permanent Set state is different. Catalyst won't silently drop a missing permanent Statistic, Resource, Effect Manager, or permanent relationship just to make the load succeed, otherwise it would potentially corrupt your game state.

---

## Ignoring temporary stuff you do not care about

The easiest policy is often:

> Restore everything that works automatically, repair the temporary things I actually care about, and ignore any remaining temporary things that are safe to lose.

Once you've loaded your saved state, you can tell Catalyst to ignore the missing stuff it can't rebuild:

```js
_restore.IgnoreMissing();

if (_restore.Complete()) {
    // Load finished.
}
```

`IgnoreMissing()` only affects **remaining blockers** that belong to temporary Effects, standalone Modifiers, or standalone Flows that Catalyst knows can be safely omitted as complete restore roots.

If a saved Effect can already be restored automatically, `IgnoreMissing()` won't throw it away. It only comes into play when something about a temporary object is preventing the restore from completing, and it's safe to ignore that thing.

It also doesn't ignore permanent structural problems, as those aren't safe to ignore.

For example, if the saved player has a permanent `"health"` Resource and your current player Set no longer contains that Resource, `IgnoreMissing()` will not pretend that this is fine.

So it's not an "I can just ignore everything and every single possible save state that could be conjured is completely fine" function. It's "Ask Catalyst to do its best to repair the problems in this save state".

You can also ignore one particular unresolved temporary flow/effect/whatever the problem is instead of ignoring every safe remaining one, we'll touch on this later on.

---

## Repairing temporary state you do care about

Suppose the player can be burning, and the `burn` Effect was created during play with an anonymous `on_tick` function:

```js
var _burn = new CatalystEffect("burn", 5)
    .SetTickInterval(1)
    .SetOnTick(function(_tick_duration, _result) {
        show_debug_message("Burn ticked");
    })

effects.AddEffect(_burn);
```

If the player saves while `burn` is still active, Catalyst can save the Effect's Catalyst state, but it can't recreate that anonymous function in the next game session.

> For clarities sake, I want to point out that the first argument for the `CatalystEffect()` constructor call is the **identity** of the effect. We will learn more about identities and refer to them throughout the rest of this page, as they are an important part of saving.
{: .note}

If you want the Effect to survive loading, we have a special tool called `CatalystRepair`:

```js
var _repair = new CatalystRepair();

_repair.AddEffect("burn")
    .OnTick(function(_tick_duration, _result) {
        show_debug_message("Burn ticked");
    })
```

This builds out a kind of "shadow" version of your Statistics, Modifiers, Effects and so on. Whenever you add an anonymous function to a callback, or bind a callback to a particular instance (in other words, any time you provide something as a callback to Catalyst that isn't a script function), you should add its "shadow" to the repair call that you make during a load.

As you can see, the anonymous function we provided to the `burn` `OnTick` method in the repair is identical to the one provided to the actual `burn` effect example we provided above.

This gives Catalyst the connective tissue it needs to complete the `burn` Effect. It can look through the Effects present in your load, and when it finds one called `burn` that is missing an `OnTick` function, it can look through your `CatalystRepair` and go "Ah, I see that there is a `burn` effect in here, and this is its `OnTick` function, so I'll stick that onto the `burn` that is being loaded in.

In this way, you can ensure that Catalyst has the in-game knowledge it needs to fix the state that can't be saved.

After you've built out your full repair section, with all the anonymous functions, methods, and so on that you've used in your game, then you can hand it to the pending restore with `Repair` and it will repair the problems in the save with the extra data you provide in the `CatalystRepair`.

```js
var _restore = player_set.RestoreState(_state);

_restore.Repair(_repair);

if (_restore.Complete()) {
    // Load finished.
}
```

Let's go over the `CatalystRepair` again:

```js
var _repair = new CatalystRepair();

_repair.AddEffect("burn")
    .OnTick(function(_tick_duration, _result) {
        show_debug_message("Burn ticked");
    })
```

`AddEffect("burn")` means that this repair information belongs to saved Effects whose identity is `"burn"`. You don't need to first check whether the current save contains `burn`. If it doesn't need that repair entry for a particular save, Catalyst ignores it.

Then we call the specific method we are interested in. Since our actual `burn` Effect example used `SetOnTick()` for the anonymous function, we use `OnTick()` for our identical anonymous function in our repair. If there was also an anonymous function provided to the `burn` Effect for `SetOnApply()`, we would just chain it:

```js
_repair.AddEffect("burn")
    .OnTick(function(_tick_duration, _result) {
        show_debug_message("Burn ticked");
    })
    .OnApply(function() {
        show_debug_message("Burn applied");
    });
```

---

## An anonymous function is fine when your normal setup already created it

An anonymous function does **not** automatically mean that you need repair code.

Suppose `damage` is part of the player's normal setup:

```js
damage = new CatalystStatistic(20)
    .SetIdentity("damage")
    .SetBaseFunc(function(_statistic, _facts) {
        return _statistic.GetBaseValue() * 1.1;
    })
```

Your normal game setup here creates `damage` *with the anonymous function* before you even attempt to load in a state with `RestoreState()`. Because the live Statistic already has its base function, the load will ignore it and you don't need to try to repair it.

Repair is only for things that happen dynamically in your game *after* initial setup. A burn Effect that gets applied by some enemy on level 7 likely isn't created as soon as the game loads in, instead it's created when the enemy hits the player with the spell and the burn Effect is applied.

That's a dynamically applied Effect, and we would need to repair it if it used a binding or an anonymous function.

But the base function above is immediately applied to your `damage` Statistic before you start loading, so it's not dynamic in the same sense.

In this case, Catalyst restores the saved Statistic state into that same `damage` Statistic and **keeps the callback** that your normal setup supplied.

The `burn` example above is different because the Effect only existed because the player happened to be burning when the save was made. Your normal setup did not create that Effect, so Catalyst had to rebuild it from the save.

Understanding this distinction removes a lot of unnecessary repair work:

- if your normal setup already created the object and its callback, you usually do nothing
- if Catalyst rebuilds a temporary object and its callbacks are named Script functions, Catalyst can usually restore them automatically and you usually do nothing
- if Catalyst rebuilds a temporary object and still needs a callback, either ignore that temporary object or repair the missing callback

---

## Identities: What they are and how to use them.

Since runtime states (things like struct references and instance ids) don't survive a save/load cycle, we need some way of telling Catalyst "this thing in the game is the same as this thing in the load". For this, we use **identities**. Identities are simply a string or a number that we use as a stable id for that thing. We've already touched on them quite a few times so far: "damage", "burn" and so on.

Not everything that needs to be saved needs an identity however. For instance, a temporary Effect, Modifier, or Flow doesn't need an identity *just* because it can be saved.

An identity becomes necessary when Catalyst may need to ask your load code for something belonging to that object.

For example:

```js
var _bonus = new CatalystModifier(5, eCatMathOps.ADD)
    .SetIdentity("burn_bonus")
    .SetCondition(function(_statistic, _facts) {
        return _facts.Get("target_burning") == true;
    })

damage.AddModifier(_bonus)
```

If Catalyst has to rebuild this Modifier, `"burn_bonus"` gives the repair code a stable way to identify it:

```js
_repair.AddModifier("burn_bonus")
    .Condition(function(_statistic, _facts) {
        return _facts.Get("target_burning") == true;
    })
```

If Catalyst knows during capture that a temporary Modifier (for example) will need a callback supplied later but the Modifier has no usable identity, the capture fails instead of creating a save that can't be repaired reliably.

Several saved things can share an identity when they use the same repair information. One `"burn"` repair entry can supply the same callback to several saved `"burn"` Effects.

If two objects share an identity but need different runtime callbacks, we have to fall back to a more primitive form of repair, which will be covered later on this page.

---

## `CatalystRepair` mirrors the callback APIs you already use

The repair methods use names that match the normal Catalyst callback setters, without `Set` at the front.

For example:

```js
.SetBaseFunc(...)
```

becomes:

```js
.BaseFunc(...)
```

and:

```js
.SetOnTick(...)
```

becomes:

```js
.OnTick(...)
```

A Statistic can repair its base and post-process functions:

```js
_repair.AddStatistic("damage")
    .BaseFunc(DamageBase)
    .PostProcess(DamagePostProcess);
```

A Modifier can repair its condition and stack function:

```js
_repair.AddModifier("berserk")
    .Condition(BerserkCondition)
    .StackFunc(BerserkStacks);
```

An Effect can repair its lifecycle callbacks:

```js
_repair.AddEffect("burn")
    .OnApply(BurnApply)
    .ResolveTick(BurnResolveTick)
    .OnTick(BurnTick)
    .OnRemove(BurnRemove);
```

An Effect Manager can repair its random function:

```js
_repair.AddEffectManager("effects")
    .RandomFunction(ChooseEffectRandom);
```

You only need to add callbacks that your game actually needs Catalyst to supply during loading, as we have already touched on. A `damage` Statistic that is initially set up with a base function doesn't need to have its base function repaired, but a `burn` Effect that is applied in the middle of gameplay, after any loading that happens, may need to have its callback repaired, if it's not a script function.

Calling the same `Add...()` method again with the same identity returns the same repair entry, so the repair can be built in several places if that fits your project better:

```js
_repair.AddEffect("burn")
    .OnTick(BurnTick);

_repair.AddEffect("burn")
    .OnRemove(BurnRemove);
```

Is identical to:

```js
_repair.AddEffect("burn")
    .OnTick(BurnTick)
    .OnRemove(BurnRemove);
```

Both calls describe the same `"burn"` repair entry, you're not creating two independent `"burn"` entries.

---

## Callbacks on Statistics inside Resources, Flows, and Effects

Resources, Flows, and Effects can own Statistics internally.

For example, when you create a Flow from a number:

```js
var _poison = new CatalystResourceFlow(-1)
    .SetIdentity("poison")
```

Catalyst automatically creates the Flow's rate Statistic for you, and sets it to -1. You can then go on to configure that Statistic if you wish:

```js
_poison.GetRateStatistic()
    .SetBaseFunc(function(_statistic, _facts) {
        return -2
    })

hp.AddFlow(_poison)
```

However, in this example, we've used an anonymous function, not a script function, so it needs to be repaired during load. If Catalyst has to rebuild the Flow and you decide that the Flow is important enough to keep, you would then repair the rate Statistic like this:

```js
_repair.AddFlow("poison")
    .Rate() // Retrieve the rate Statistic from the Flow
    .BaseFunc(function(_statistic, _facts) { // And set its anonymous function
        return -2
    })
```

The same shape applies to the other Statistics owned by Catalyst Resources, Effects and so on.

A Resource's minimum and maximum Statistics:

```js
_repair.AddResource("hp")
    .Minimum()
    .BaseFunc(HealthMinimum)

_repair.AddResource("hp")
    .Maximum()
    .PostProcess(HealthMaximumPostProcess)
```

An Effect's chance Statistics:

```js
_repair.AddEffect("stun")
    .ChanceToApply()
    .BaseFunc(StunChance)

_repair.AddEffect("poison")
    .ChancePerTick()
    .PostProcess(PoisonTickChancePostProcess)
```

`Minimum()`, `Maximum()`, `Rate()`, `ChanceToApply()`, and `ChancePerTick()` take the repair builder to the appropriate internal Statistic. From there, `BaseFunc()` and `PostProcess()` work the same way as they do for a normal Statistic repair.

If these callbacks were already created by your normal setup, or are named Script functions Catalyst can recover automatically, none of this extra repair code is needed.

---

## Bound methods use the game object that already exists after loading

A named Script function can be found again by name, but a method created with `method()` also has a scope: the struct or instance that should become `self`.

Suppose this function exists in a Script asset:

```js
function TargetIsBurning(_statistic, _facts) {
    return self.is_burning
}
```

During play, a Modifier might bind it to an enemy:

```js
var _bonus = new CatalystModifier(5, eCatMathOps.ADD)
    .SetIdentity("burn_bonus")
    .SetCondition(method(enemy, TargetIsBurning))

damage.AddModifier(_bonus)
```

Catalyst can remember the function name `TargetIsBurning`, but it can't decide which runtime enemy should be used as the method scope after loading.

It's possible that an appropriate instance or struct exists in your game during the load that you can set the method's scope to during the repair process:

```js
_repair.AddModifier("burn_bonus")
    .Condition(method(loaded_enemy, TargetIsBurning))
```

But sometimes, there's not really a sensible way to scope that method correctly. For instance, an appropriate enemy might not spawn in until the player reaches a certain point, or any other number of situations where the idea of "This scope belonged to this thing" doesn't make as much sense after a load as it did during the save.

It's usually best to ignore these Modifiers or Effects. Repair is certainly possible, but you'll have to have a clear understanding of scope and a good loading sequence in order to be able to do.

Effect lifecycle callbacks are a little different. `SetOnApply()`, `SetResolveTick()`, `SetOnTick()`, and `SetOnRemove()` actually strip any existing scope and run in the Effect's own scope. If the function behind one of those callbacks uses a script function, Catalyst can restore them automatically.

---

## Custom countdown trackers

A timed Modifier, Flow, or Effect can use:

- the normal global `CATALYST_COUNTDOWN`
- `noone`
- a custom `CatalystCountdownTracker`

The first two need no special repair.

For custom countdown trackers Catalyst remembers the **identity of the tracker** rather than trying to preserve the actual custom countdown itself.

For example, your normal game setup might already contain:

```js
combat_time = new CatalystCountdownTracker()
    .SetIdentity("combat_time");
```

and your Effects use it normally:

```js
var _burn = new CatalystEffect("burn", 5)
    .SetCountdownTracker(combat_time)
    .SetOnTick(BurnTick);
```

When loading, the important thing is that a live tracker identified as `"combat_time"` exists.

In most projects, that will simply be the tracker your normal setup has already created. Give that existing tracker to the repair:

```js
var _repair = new CatalystRepair()

_repair.AddCountdownTracker(combat_time)
```

If your game only creates that tracker in some situations, make sure the appropriate tracker exists before repairing the restore.

If the timed Effect, Modifier, etc already exists in the live setup and already uses the matching custom tracker, Catalyst can also recognise that relationship while preparing the restore. Registering the trackers your game already knows about is still a simple general approach for temporary Effects, Modifiers, and Flows that Catalyst has to rebuild.

A custom tracker must have a stable identity before capture. Two different custom trackers used by the same captured Set can't share the same identity, because the saved state would not be able to distinguish them.

The tracker's identity is only for persistence. It doesn't change how that tracker ticks, pauses, scales time, or otherwise behaves.

> A timed Effect, Modifier, or Flow doesn't need its own identity just because it uses a custom tracker. The tracker relationship uses the tracker's identity. The timed thing only needs its own identity when something else, such as a callback, needs to be repaired by the things identity.
{: .note}

If a temporary Effect or Modifier needs a custom tracker that is not available during loading and you do not care about preserving it, then ignoring it's usually simpler than inventing extra tracker lifecycle code.

---

## Ignore then Repair then inspect anything still missing

For most projects, `CatalystRepair` should handle every runtime piece you intentionally want to preserve:

```js
_restore.Repair(_repair);
```

If you also use:

```js
_restore.IgnoreMissing();
```

then any remaining temporary blockers that are safe to lose are removed from the pending restore.

Only specifically unusual cases need the lowest-level requirement APIs described here.

For example:

- two saved objects share an identity but need different callbacks
- the correct callback depends on which project-owned object was loaded for this particular save
- a modular system doesn't know which repair is appropriate until it sees the saved object

After normal repair, ask for the callback requirements that are still unresolved:

```js
_restore.Repair(_repair);
_restore.IgnoreMissing();
var _missing = _restore.GetMissingCallbacks();
```

Each requirement tells you which saved Catalyst object still needs help:

```js
for (var i = 0; i < array_length(_missing); i++) {
    var _requirement = _missing[i];

    show_debug_message(_requirement.GetType());
    show_debug_message(_requirement.GetIdentity());
    show_debug_message(_requirement.GetCallbacks());
}
```

`GetCallbacks()` contains only the callback slots that are still missing.

You can ask about one slot with:

```js
if (_requirement.Needs("condition")) {
    // This condition is still unresolved.
}
```

and supply it directly:

```js
_requirement.Resolve(
    "condition",
    method(loaded_enemy, TargetIsBurning)
)
```

If the original callback came from a named Script function but its method binding could not be restored, you can also inspect the saved function name:

```js
var _name = _requirement.GetSavedCallbackName("condition")
```

For callbacks on an internal Statistic, `GetComponent()` tells you which internal Statistic owns the callback. Common values are:

- `"minimum"` and `"maximum"` for Resources
- `"rate"` for Flows
- `"chance_to_apply"` and `"chance_per_tick"` for Effects
- `"self"` for callbacks directly on the object

`GetStruct()` gives you the exact rebuilt Catalyst struct represented by the requirement when your load code genuinely needs that level of control.

---

## Ignoring one particular unresolved temporary Modifier / Effect / Flow / etc

The same callback requirement can tell you whether the temporary Catalyst struct it belongs to is safe to omit:

```js
if (_requirement.CanIgnore()) {
    _requirement.Ignore()
}
```

`Ignore()` doesn't mean "ignore this callback but keep the rest of the struct."

It means "do not restore the temporary Effect, Flow, or Modifier that this problem belongs to."

For example, if a missing Modifier callback belongs to an Effect payload, ignoring the requirement drops the Effect as a whole. Catalyst doesn't rebuild half of an Effect and pretend it's the same struct that was saved.

You can inspect what would be omitted with:

```js
_requirement.GetIgnoreType()
_requirement.GetIgnoreIdentity()
```

Permanent Set state can't be ignored this way.

---

## Custom countdown trackers have the same manual fallback

Anything still waiting for a custom tracker after normal repair can be inspected with:

```js
var _missing_trackers = _restore.GetMissingCountdownTrackers()
```

A tracker requirement exposes the tracker identity it needs:

```js
for (var i = 0; i < array_length(_missing_trackers); i++) {
    var _requirement = _missing_trackers[i]

    if (_requirement.GetTrackerIdentity() == "combat_time") {
        _requirement.Resolve(combat_time)
    }
}
```

Normally:

```js
_repair.AddCountdownTracker(combat_time)
```

is simpler.

The manual requirement API exists for cases where your game needs to choose a tracker dynamically.

A tracker requirement can also be ignored when its containing temporary restore root is safe to lose:

```js
if (_requirement.CanIgnore()) {
    _requirement.Ignore()
}
```

---

## Understanding restore reports

`RestoreState()` always returns a restore result, including when Catalyst could not prepare the saved state for the current Set.

You can inspect it with:

```js
var _restore = player_set.RestoreState(_state)
var _report = _restore.GetReport()
```

The report's `stage` tells you how far the operation got:

- `"prepare"` means Catalyst could not safely prepare the saved state for the current Set
- `"pending"` means the restore is prepared but something still needs repair, or the Set is temporarily unavailable for completion
- `"ready"` means everything required is available
- `"apply"` means Catalyst started applying the restore but the operation failed
- `"complete"` means the restore committed successfully

A `"pending"` restore can still be completed. Supply the missing repair, ignore safe temporary blockers if that matches your load policy, and call `Complete()` again.

If an `"apply"` failure occurs, start a fresh load from the original saved state after fixing the cause. Catalyst may already have started changing the live Set by that stage.

When temporary saved state is deliberately ignored, the final report records that:

```js
var _report = _restore.GetReport()

if (_report.salvaged) {
    show_debug_message(json_stringify(_report.ignored))
}
```

A successful load can therefore have:

```js
success: true
salvaged: true
```

which means the permanent restore completed successfully, but one or more safe temporary objects were deliberately left out.

`GetReport()` returns fresh JSON-safe data each time, so it can be passed directly to:

```js
json_stringify(_report)
```

For most projects, the report is there for diagnostics. You do not need to write code for every possible `reason` value unless your own save system has a reason to react differently to them.

---

## Saving or loading from inside an Effect callback

Effect Managers can temporarily defer changes to their active Effects while one of their Effect callbacks is running.

If you attempt to capture or restore the same Set during that small window, Catalyst refuses the persistence operation rather than working from an Effect list that is still being changed.

The report identifies this as:

```js
reason: "effect_manager_busy"
```

In normal game code, perform the save or load after the current Effect callback has finished.

You do not need to manage Catalyst's internal Effect changes yourself.

---

## Put connected Catalyst structs in the same Set

A Set can only restore Catalyst relationships between structs that belong to that Set.

Suppose the player's maximum HP is a shared Statistic:

```js
max_hp = new CatalystStatistic(100)
    .SetIdentity("max_hp")

hp = new CatalystResource(max_hp, 75)
    .SetIdentity("hp")
```

Because `hp` refers to `max_hp`, both belong in the same Set if that relationship needs to survive saving and loading:

```js
player_set = new CatalystSet("player")
    .AddStatistic(max_hp)
    .AddResource(hp)
```

The same applies when an Effect owns a Modifier that targets a Statistic, or a Flow that targets a Resource.

If a saved Catalyst relationship leaves the Set, capture fails instead of writing a relationship that Catalyst can't rebuild later.

This doesn't mean that every Catalyst object in your game belongs in one enormous Set. Group together the objects whose Catalyst relationships need to survive as one saved model.

---

## Loading is silent

Loading 28 HP from a save shouldn't look like the player just took damage from the newly-created value of 75.

Catalyst restores Set state silently.

Normal Statistic and Resource change subscriptions are not fired merely because saved values are being put back, and restoring an Effect Manager doesn't replay ordinary Effect application or removal callbacks.

After `Complete()` succeeds, update wider game systems that specifically need to know that a load occurred.

---

## Sync Oracle facts after loading

The silent restore also affects values published to Oracle with `PublishToFact()`.

Suppose HP is published like this:

```js
player_facts = new OracleFacts()

health_fact = hp.PublishToFact(
    player_facts,
    "health",
    function(_resource) {
        return _resource.GetCurrent()
    }
)
```

That binding normally republishes when HP changes during play.

Since loading is silent, you should sync it once after a successful restore:

```js
if (_restore.Complete()) {
    health_fact.Sync()
}
```

Do the same for any other `CatalystFactBinding` whose Catalyst value was restored by the Set.

---

## How the load grows as your game gets more complicated

The basic case where you have only used unbound script functions as callbacks for Catalyst remains fairly simple:

```js
var _restore = player_set.RestoreState(_state);

if (_restore.Complete()) {
    // Loaded.
}
```

If some temporary state can't be rebuilt automatically and you don't care about keeping it:

```js
var _restore = player_set.RestoreState(_state);

_restore.IgnoreMissing();

if (_restore.Complete()) {
    // Loaded, possibly without some temporary state.
}
```

If some temporary state matters enough to repair:

```js
var _repair = new CatalystRepair();

_repair.AddEffect("burn")
    .OnTick(BurnTick);

var _restore = player_set.RestoreState(_state);

_restore.Repair(_repair);
_restore.IgnoreMissing();

if (_restore.Complete()) {
    // The repaired state was kept.
    // Other safe unresolved temporary state was dropped.
}
```

If a repair needs a game-owned object such as an enemy or RNG, use the object your own load sequence has already produced:

```js
_repair.AddModifier("burn_bonus")
    .Condition(method(loaded_enemy, TargetIsBurning));
```

If your normal setup already created a custom countdown tracker, register that same tracker:

```js
_repair.AddCountdownTracker(combat_time);
```

Only if the reusable repair table is not enough do you inspect the remaining requirements directly.

---

## A complete complicated example

The following example deliberately combines several persistence complications. it's **not** the normal amount of code required to load a Catalyst Set.

Imagine:

- the player's permanent Catalyst setup contains `damage`, `fortune`, `hp`, and an Effect Manager
- a saved `burn` Effect uses an anonymous callback that the game wants to preserve
- a saved `burn_bonus` Modifier is bound to an enemy that the game's normal load process has already loaded
- a saved `poison` Flow has an anonymous rate function
- those temporary objects used a custom `combat_time` tracker that the player's normal setup already creates
- the Effect Manager has a random function bound to the player's loaded RNG object
- some other short-lived temporary state may be missing runtime pieces, and the game doesn't care about preserving it
- an older game save version used the Statistic identity `"luck"` instead of `"fortune"`

### Save the Catalyst state inside your normal save

```js
var _capture = player_set.CaptureState();

if (_capture.Succeeded()) {
    global.my_save_data.save_version = 4;
    global.my_save_data.player_data = _capture.GetState();
}
else {
    show_debug_message(json_stringify(_capture.GetReport()));
}
```

Your normal save code then writes `global.my_save_data` to disk.

### Read and migrate the game save

```js
var _save = json_parse(_json);
```

Apply the game's migration before Catalyst sees the state:

```js
if (_save.save_version < 4) {
    var _state = _save.player_data;

    for (var i = 0; i < array_length(_state.statistics); i++) {
        if (_state.statistics[i].identity == "luck") {
            _state.statistics[i].identity = "fortune";
        }
    }

    _save.save_version = 4;
}
```

### Run the normal game setup

The current game creates its permanent Catalyst objects exactly as it normally does:

```js
damage = new CatalystStatistic(20)
    .SetIdentity("damage")
    .SetBaseFunc(function(_statistic, _facts) {
        return _statistic.GetBaseValue() * 1.1;
    });

fortune = new CatalystStatistic(0)
    .SetIdentity("fortune");

hp = new CatalystResource(100, 75)
    .SetIdentity("hp");

effects = new CatalystEffectManager(self)
    .SetIdentity("effects");

player_set = new CatalystSet("player")
    .AddStatistic(damage)
    .AddStatistic(fortune)
    .AddResource(hp)
    .AddEffectManager(effects);
```

The inline `damage` base function needs no persistence repair because this setup already created it.

The same normal setup also creates the player's custom countdown tracker:

```js
combat_time = new CatalystCountdownTracker()
    .SetIdentity("combat_time");
```

There is no second `combat_time` created for persistence. The restore will use this existing tracker.

Suppose the rest of the game's load process has also already produced:

```js
var _enemy = loaded_enemy;
var _rng = loaded_rng;
```

These are the normal game objects that the restored bindings should point to.

### Build the repair for temporary state you care about

```js
var _repair = new CatalystRepair();

_repair.AddCountdownTracker(combat_time);

_repair.AddEffect("burn")
    .OnTick(function(_tick_duration, _result) {
        show_debug_message("Burn ticked")
    });

_repair.AddModifier("burn_bonus")
    .Condition(method(_enemy, TargetIsBurning));

_repair.AddFlow("poison")
    .Rate()
    .BaseFunc(function(_statistic, _facts) {
        return -2;
    });

_repair.AddEffectManager("effects")
    .RandomFunction(method(_rng, ChooseEffectRandom));
```

Named Script callbacks that Catalyst can restore automatically do not need entries here.

Permanent callbacks already recreated by the current setup do not need entries here either.

### Prepare, repair, and drop temporary leftovers you do not care about

```js
var _restore = player_set.RestoreState(_save.player_data);

_restore.Repair(_repair);
_restore.IgnoreMissing();
```

At this point:

- state Catalyst could restore automatically is ready
- the temporary state covered by `_repair` has the runtime pieces you chose to preserve
- any remaining safe temporary blocker is marked to be omitted
- any permanent incompatibility is still a real failure

### Complete the restore

```js
if (_restore.Complete()) {
    health_fact.Sync();

    var _report = _restore.GetReport();

    if (_report.salvaged) {
        show_debug_message(json_stringify(_report));
    }
}
else {
    show_debug_message(json_stringify(_restore.GetReport()));
}
```

If the load completed after ignoring temporary state, the report has `success: true` and `salvaged: true`.

If a permanent part of the saved Set is incompatible with the current game, or some non-ignorable requirement is still unresolved, `Complete()` remains `false` and the report explains what is blocking the load.

The important part is that the complicated example still follows the same order as the simple one: the game runs its normal setup first, Catalyst restores what it can automatically, you repair only the temporary state you care about preserving, and you can ignore safe temporary leftovers that are not worth reconstructing. Failures are returned in a way that you can save them to disk, send them to an online bug report repository or even pass them to the player to report back to you if necessary.

---

## Catalyst's state version

Catalyst's captured state contains:

```js
version: 1
```

That is the version of **Catalyst's persistence format**.

It's not your game's save version, and you shouldn't change it when your game gets an update.

Your game should keep its own save version in its own save data:

```js
global.my_save_data = {
    save_version: 4,
    player_data: _capture.GetState()
}
```

The two values mean different things:

- `save_version` belongs to your game and tells your migration code which version of your game's saved data this is
- Catalyst's `version` belongs to Catalyst and describes the shape of Catalyst's saved state

Leave Catalyst's `version` alone, as it's important for internal use.

---

## Catalyst persistence format version 1: the complete saved shape

If you are writing a migration, you need to know what is actually inside the Catalyst state you are editing.

The following is the complete shape returned by:

```js
_capture.GetState()
```

for Catalyst persistence format version `1`.

You do not need to memorise this structure for normal saving and loading. This section is a reference for code that needs to inspect or change an older Catalyst save after your game has had an update that invalidates part (or all) of the older save before passing it to `RestoreState()`.

The only values below that Catalyst can't describe any further are `meta`, `source_id`, and `source_meta`, because those are values supplied by your own game.

### The Set state

The top-level state is:

```js
{
    version: 1,

    identity: <Set identity>,
    name: <Set name>,
    meta: <your Set meta>,

    layer_order: <array or undefined>,

    statistics: [
        <Statistic state>,
        ...
    ],

    resources: [
        <Resource state>,
        ...
    ],

    effect_managers: [
        <Effect Manager state>,
        ...
    ]
}
```

When a migration needs a particular Statistic, Resource, Effect Manager, Effect, Modifier, or Flow, find it by its saved `identity`. Do not use an array position as the persistent identity of that struct.

For example:

```js
for (var i = 0; i < array_length(_state.statistics); i++) {
    var _statistic = _state.statistics[i];

    if (_statistic.identity == "fortune") {
        // This is the saved fortune Statistic.
    }
}
```

### Statistic state

A saved Statistic has this complete shape:

```js
{
    identity: <identity>,
    name: <name>,

    starting_value: <value>,
    base_value: <value>,

    min_value: <value>,
    max_value: <value>,

    clamped: <bool>,
    rounded: <bool>,
    round_step: <value>,

    modifier_order: <modifier ordering value>,

    layer_order: [
        <layer>,
        ...
    ],

    tags: [
        <tag>,
        ...
    ],

    callbacks: {
        base_func: <callback descriptor>,
        post_process: <callback descriptor>
    },

    modifiers: [
        <standalone Modifier state>,
        ...
    ]
}
```

The `modifiers` array contains the standalone Modifiers attached to that Statistic. Modifiers that belong to an Effect are saved with that Effect instead, so they are not duplicated here.

### Modifier state

A saved Modifier has this complete shape:

```js
{
    identity: <identity>,
    target_identity: <target identity>,

    source_label: <source label>,
    source_id: <your source id>,
    source_meta: <your source meta>,

    value: <value>,
    operation: <operation>,

    duration: <remaining duration>,
    duration_max: <maximum duration>,

    tracker: "default" | "none" | "custom",
    tracker_identity: <custom tracker identity or undefined>,

    stacks: <current stacks>,
    max_stacks: <maximum stacks>,
    stack_mode: <stack mode>,

    layer: <layer>,

    family: <family>,
    family_mode: <family mode>,
    family_scope: <family scope>,

    tags: [
        <tag>,
        ...
    ],

    callbacks: {
        condition: <callback descriptor>,
        stack_func: <callback descriptor>
    }
}
```

`tracker_identity` is only meaningful when `tracker` is `"custom"`.

### Resource state

A saved Resource has this complete shape:

```js
{
    identity: <identity>,
    name: <name>,

    current: <current value>,

    minimum_bound_mode: <minimum bound mode>,
    maximum_bound_mode: <maximum bound mode>,

    minimum: <Statistic binding>,
    maximum: <Statistic binding>,

    flows: [
        <standalone Flow state>,
        ...
    ]
}
```

The `flows` array contains standalone Flows attached to that Resource. Flows that belong to an Effect are saved with that Effect instead.

### Statistic bindings

Several Catalyst structs can either own their own Statistic or refer to a direct Statistic in the Set.

This is used for:

- a Resource's `minimum`
- a Resource's `maximum`
- a Flow's `rate`
- an Effect's `chance_to_apply`
- an Effect's `chance_per_tick`

If the Statistic is owned by that Catalyst struct, the saved binding is:

```js
{
    bound: false,
    state: <full Statistic state>
}
```

If it refers to a direct Statistic in the Set, the saved binding is:

```js
{
    bound: true,
    identity: <identity of the direct Statistic>
}
```

This distinction is important during migration. A nested owned Statistic lives inside `state`, while a bound Statistic is only a reference to one of the entries in the Set's top-level `statistics` array.

### Flow state

A saved Flow has this complete shape:

```js
{
    identity: <identity>,
    name: <name>,

    rate: <Statistic binding>,

    active: <bool>,
    delay_remaining: <remaining delay>,

    source_label: <source label>,
    source_id: <your source id>,
    source_meta: <your source meta>,

    tracker: "default" | "none" | "custom",
    tracker_identity: <custom tracker identity or undefined>,

    effect_eligible_amount: <amount>
}
```

As with Modifiers, `tracker_identity` is only meaningful when `tracker` is `"custom"`.

### Effect Manager state

A saved Effect Manager has this complete shape:

```js
{
    identity: <identity>,
    name: <name>,

    callbacks: {
        random_function: <callback descriptor>
    },

    effects: [
        <Effect state>,
        ...
    ]
}
```

### Effect state

A saved Effect has this complete shape:

```js
{
    identity: <identity>,

    family: <family>,
    reapply_policy: <reapply policy>,

    source_label: <source label>,
    source_id: <your source id>,
    source_meta: <your source meta>,

    tags: [
        <tag>,
        ...
    ],

    duration: <remaining duration>,
    duration_max: <maximum duration>,

    tracker: "default" | "none" | "custom",
    tracker_identity: <custom tracker identity or undefined>,

    chance_to_apply: <Statistic binding>,

    tick_interval: <tick interval>,
    tick_accumulator: <current tick accumulator>,

    chance_per_tick: <Statistic binding>,

    callbacks: {
        on_apply: <callback descriptor>,
        resolve_tick: <callback descriptor>,
        on_tick: <callback descriptor>,
        on_remove: <callback descriptor>
    },

    flows: [
        {
            resource_identity: <identity of a direct Resource in the Set>,
            flow: <Flow state>
        },
        ...
    ],

    modifiers: [
        {
            statistic_identity: <identity of a direct Statistic in the Set>,
            modifier: <Modifier state>
        },
        ...
    ]
}
```

An Effect's Flow and Modifier payloads contain both the saved Flow or Modifier and the identity of the direct Set member that payload belongs to.

For example:

```js
_effect.flows[i].resource_identity
```

tells Catalyst which direct Resource should receive:

```js
_effect.flows[i].flow
```

and:

```js
_effect.modifiers[i].statistic_identity
```

tells Catalyst which direct Statistic should receive:

```js
_effect.modifiers[i].modifier
```

### Callback descriptors

Callbacks do not appear in the saved state as live functions. Each callback slot contains one of these descriptor shapes.

No callback was present:

```js
{
    kind: "none"
}
```

Catalyst saved a named Script function that it can attempt to find again:

```js
{
    kind: "named",
    name: "BurnTick"
}
```

Catalyst needs the callback to be supplied manually and there is no reusable Script-function name:

```js
{
    kind: "manual"
}
```

Catalyst needs the callback to be supplied manually, but it knows the name of the Script function that was used before it was bound to a runtime scope:

```js
{
    kind: "manual",
    name: "TargetIsBurning"
}
```

Those four shapes are the complete callback descriptor format in persistence version `1`.

### Where direct Set identities are referenced

When you rename the identity of a direct Set member during a game migration, changing the entry itself may not be enough. Other saved Catalyst state can refer to that identity.

A direct Statistic identity can appear in:

- `statistics[i].identity`
- any bound Statistic binding as `identity`
- `effect_managers[i].effects[j].modifiers[k].statistic_identity`

A direct Resource identity can appear in:

- `resources[i].identity`
- `effect_managers[i].effects[j].flows[k].resource_identity`

An Effect Manager identity appears in:

- `effect_managers[i].identity`

The Set identity appears in:

- the top-level `identity`

For example, if a direct Statistic is renamed from `"luck"` to `"fortune"`, a migration should change the Statistic's own identity and any saved Catalyst references that point to that same direct Statistic.

The fields `target_identity`, `source_id`, `source_meta`, and `meta` are not Catalyst Set-member references that Catalyst resolves through these arrays. They are saved values belonging to their respective APIs, so any game-specific migration of those values is up to your own save format.

---

## Updating old Catalyst state when your game changes

A later version of your game may change the Catalyst model itself.

For example, you might:

- rename a Statistic or Resource identity
- remove a permanent Set member
- replace one gameplay system with another
- decide that old saved configuration should be changed to a new value
- change permanent child state underneath an existing Statistic, Resource, or Effect Manager

Catalyst can't know what those game-design changes mean.

If an old save contains a Statistic called `"luck"` and the current game creates a Statistic called `"fortune"`, Catalyst can't guess that they are the same Statistic.

Handle that as part of your normal game-save migration.

Catalyst state is plain structs and arrays, so you can edit it before passing it to `RestoreState()`.

Suppose game save version 3 renamed `"luck"` to `"fortune"`:

```js
var _save = json_parse(_json)

if (_save.save_version < 4) {
    var _state = _save.player_data

    for (var i = 0; i < array_length(_state.statistics); i++) {
        if (_state.statistics[i].identity == "luck") {
            _state.statistics[i].identity = "fortune"
        }
    }

    _save.save_version = 4
}
```

After migration, build the current game setup normally and restore the migrated state:

```js
var _restore = player_set.RestoreState(_save.player_data)
```

If other saved Catalyst relationships also refer to the renamed identity, update those relationships as part of the same migration.

A game with several historical save versions will normally apply its migrations in order:

```js
if (_save.save_version < 2) {
    // Migrate game save version 1 -> 2.
    _save.save_version = 2
}

if (_save.save_version < 3) {
    // Migrate game save version 2 -> 3.
    _save.save_version = 3
}

if (_save.save_version < 4) {
    // Migrate game save version 3 -> 4.
    _save.save_version = 4
}
```

Catalyst state can be changed inside those migrations just like inventory data, quest state, world state, or any other part of your game's save.

---

## Migration and ignoring solve different problems

Migration is for an old save whose **meaning has changed because your game changed**.

Ignoring is for temporary runtime state that Catalyst can't currently finish restoring and that your game doesn't care enough about preserving.

For example, if `"luck"` was renamed to `"fortune"`, migrate it. That is permanent game state and the rename has a specific meaning.

If a two-second combat debuff needs an old enemy binding before it can be restored and you do not care whether that debuff survives loading, ignore the debuff.

`IgnoreMissing()` is not a replacement for migrating permanent Set structure.

---

## Next: patterns and recipes

Continue with **[Patterns & Recipes](patterns-and-recipes)** for complete gameplay examples that combine Statistics, Resources, Flows, Effects, Oracle facts, and Sets without turning every problem into the same kind of object.
