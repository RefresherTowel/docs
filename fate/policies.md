---
layout: default
title: Policies Guide
parent: Fate
nav_order: 4
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Policies Guide

Policies are the rule layer that modifies how Fate chooses entries. They let you implement pity, featured rate-up, duplicate protection, and batch guarantees.

## Beginner policy methods (recommended to experiment with first)

These helper methods are the easiest way to add common loot-table behavior without writing your own custom policy. They all live on `FateTable`, and they all answer a very specific kind of design question:

| If you want...                                                       | Use this helper                  |
| -------------------------------------------------------------------- | -------------------------------- |
| a rare result to become more likely the longer it hasn't appeared    | `EnablePity(...)`                |
| certain entries to be "featured" and show up more often              | `EnableRateUp(...)`              |
| recent results to not repeat right away                              | `EnableDuplicateProtection(...)` |
| at least some number of matching results inside a multi-roll         | `EnableBatchGuarantee(...)`      |
| a friendlier version of a batch guarantee for 10-pulls               | `EnableTenPullGuarantee(...)`    |
| a quick "banner-style" setup with pity and optional featured entries | `EnableStandardGachaRules(...)`  |

ALL of the helpers that target entries accept either:

* a single `FateEntry`
* an array of `FateEntry`

So these are both valid:

```js
loot_table.EnablePity(_five_star_entry, 90, 75, 0.06);
loot_table.EnablePity([_five_star_a, _five_star_b], 90, 75, 0.06);
```

## How to choose the right helper

`EnablePity(...)` is about *bad-luck protection over time*.

`EnableRateUp(...)` is about *making featured entries more likely than their normal weight would suggest*.

`EnableDuplicateProtection(...)` is about *recent-repeat control*. It's *not* a shuffle bag.

`EnableBatchGuarantee(...)` is about *making sure a single multi-roll contains enough matches*.

`EnableStandardGachaRules(...)` is just a convenience helper that wires a couple of the above together.

## EnablePity(...)

```js
EnablePity(_target_entries, _hard_at = 90, _soft_start = 75, _soft_step = 0.06, _scope_context_key = undefined)
```

Use pity when you want Fate to protect the player from long streaks of bad luck.

Pity tracks how many times the player has *missed* a target set of entries. The longer that miss streak gets, the more the policy helps the target entries.

### What it does

Pity only cares about the entries you pass in as `_target_entries`.

If a roll does *not* select one of those targets, the miss counter goes up.

If a roll *does* select one of those targets, the miss counter resets.

From there, pity can help in two different ways:

* **Soft pity**: once the miss counter reaches `_soft_start`, Fate starts adding extra weight to the target entries every time the player misses again.
* **Hard pity**: once the miss counter reaches `_hard_at`, the next selection is forced into the target set.

So if you use this:

```js
loot_table.EnablePity(_five_star_entries, 90, 75, 0.06);
```

the idea is:

* before 75 misses: normal odds
* from 75 misses onward: the target entries get extra weight (0.06 added each roll)
* after 90 misses: the player is guaranteed to hit the target set

### Arguments

`_target_entries`
The entry, or entries, that count as a "success" for this pity rule.

`_hard_at`
How many misses are allowed before hard pity kicks in.

If this is `90`, that means "after 90 misses, force the next result into the target set.", so it will drop on roll 91.

`_soft_start`
The miss count where soft pity begins.

If this is `75`, the extra help starts after the player has missed 75 times.

`_soft_step`
How much extra weight gets added per soft-pity step.

This is an *additive* weight increase, not a multiplier. Bigger values make the target entries ramp up faster.

`_scope_context_key`
An optional context key used to track pity separately per scope.

For example, if you pass `"profile_id"`, then each profile gets its own pity counter instead of sharing one global pity state.

> `_scope_context_key` is the name of the field Fate should read from the roll context. So if your context is `{ profile_id: "slot_2" }`, pass `"profile_id"`, not `"slot_2"`. This tells Fate to read the profile id from the context struct and use that value as the pity scope.
{: .note}

### When you should use it

Use pity when you want a rare tier to feel fair over long play.

Typical example:

* "A 5-star should eventually happen even if the player's luck is bad."

### When you should *not* use it

Don't use pity if your real goal is "don't repeat the same recent drops." That's duplicate protection, not pity.

Don't use pity if your goal is "every 10-pull should contain at least one 4-star." That's a batch guarantee.

## EnableRateUp(...)

```js
EnableRateUp(_featured_entries, _rate_up_mult = 1.5, _hard_at = undefined, _reset_on_any_hit = false, _scope_context_key = undefined)
```

Use rate-up when you already have a rare tier, but want some entries in that tier to be featured more strongly than others.

This is what you want for banner-style "this character is on rate-up" behavior.

### What it does

Rate-up only cares about the entries in `_featured_entries`.

When Fate evaluates one of those featured entries, it multiplies that entry's weight by `_rate_up_mult`.

Optionally, it can also hard guarantee a featured result after enough misses.

So if you use this:

```js
loot_table.EnableRateUp(_featured_entries, 1.5);
```

then featured entries become 1.5x as likely as they would otherwise be.

If you use this:

```js
loot_table.EnableRateUp(_featured_entries, 1.5, 2);
```

then after enough non-featured hits, Fate can hard force a featured result.

### Arguments

`_featured_entries`
The entry, or entries, that count as featured.

`_rate_up_mult`
The weight multiplier applied to featured entries.

`1.5` means featured entries get 1.5x their normal weight.
`2` means featured entries get 2x their normal weight.

`_hard_at`
Optional. If set, featured entries become hard-guaranteed after enough misses.

If left `undefined`, there is no hard featured guarantee, only the soft multiplier.

`_reset_on_any_hit`
Controls what resets the miss counter.

If `false`, the counter only resets when the player actually gets a featured result. This is the more common "featured guarantee" behavior.

If `true`, *any* result resets the counter. That makes the policy much gentler, because the counter does not keep building through ordinary non-featured hits.

`_scope_context_key`
Optional scope key, just like pity.

### When you should use it

Use rate-up when your question is:

* "I have a pool of good results, but I want these specific ones to be more likely."

### When you should *not* use it

Don't use rate-up to prevent repeats. It has nothing to do with repetition.

Don't use rate-up to guarantee something inside a 10-pull. That's a batch guarantee.

## EnableDuplicateProtection(...)

```js
EnableDuplicateProtection(_window = 1, _mode = "penalize", _penalty_mult = 0.25, _key_mode = "entry_id", _intra_roll_unique = true)
```

Use duplicate protection when you want recent results to stop showing up again immediately.

### What it does

Duplicate protection remembers a rolling history of recent results.

When a new candidate entry is being considered, Fate checks whether that entry matches something in the recent history window.

If it does, the policy either:

* **penalizes** it by reducing its weight, or
* **excludes** it completely

depending on `_mode`.

### The important mental model

This is a **rolling window of recent uniqueness**.

It's **not** a shuffle bag.

That means this helper does *not* say:

* "you must see every other possible result before this one can come back"

It says:

* "this result should not repeat while it's still inside the recent-history window"

If your window is `2`, Fate remembers the last two selected keys. Once an old result falls out of that window, it's allowed again.

So a result can repeat before every other result in the table has appeared. It's only blocking the *recent past*, not enforcing full-cycle exhaustion.

### Arguments

`_window`
How many past selected keys Fate remembers.

`1` means "protect against the most recent result."
`2` means "protect against the last two results."
`0` effectively means no recent-history protection.

`_mode`
How duplicates should be handled.

`"penalize"` means recent duplicates are still allowed, but their weight is reduced.
`"exclude"` means recent duplicates are removed from consideration entirely.

`_penalty_mult`
Only used in `"penalize"` mode.

If this is `0.25`, a recent duplicate keeps only 25% of its normal weight.

`_key_mode`
Controls what counts as "the same thing."

`"entry_id"` means each entry is treated as its own separate duplicate bucket.

`"unique_key"` means Fate uses each entry's `unique_key` first, and falls back to `entry_id` if there is no `unique_key`.

This is useful when multiple entries should count as the same duplicate group.

For example, if two entries are alternate versions of the same character, you can give them the same `unique_key` and treat them as duplicates of each other.

`_intra_roll_unique`
Controls whether duplicates are also prevented *inside the same multi-roll*.

If `true`, once a key is selected in a multi-roll, that same key is also treated as a duplicate for later slots in that same roll.

If `false`, the policy only looks at prior history, not earlier picks in the current batch.

### When you should use it

Use duplicate protection when your question is:

* "I don't want the player seeing the same thing again right away."
* "I want the last X drops to act like a rolling no-repeat window."

### When you should *not* use it

Don't use this if you want full deck-like exhaustion. That's shuffle-bag behavior, not duplicate protection.

Don't use this if your goal is simply to make rare entries more likely after misses. That's pity.

### Examples

Prevent the immediately previous result from repeating:

```js
loot_table.EnableDuplicateProtection(1, "exclude");
```

Strongly discourage repeating anything from the last 3 drops:

```js
loot_table.EnableDuplicateProtection(3, "penalize", 0.1);
```

Treat multiple entries with the same `unique_key` as duplicates of each other:

```js
loot_table.EnableDuplicateProtection(2, "exclude", 0.25, "unique_key", true);
```

## EnableBatchGuarantee(...)

```js
EnableBatchGuarantee(_target_entries, _min_count = 1, _roll_count_at_least = 10, _soft_mult = 1, _allow_bypass_filters = true)
```

Use a batch guarantee when your rule is about a *single multi-roll as a whole*.

This is for "at least one 4-star in every 10-pull" style behavior.

### What it does

Batch guarantee checks the whole requested roll count.

If the player is not rolling enough entries, the policy does nothing.

If they *are* rolling enough entries, the policy tracks how many matching results have already appeared in that batch and how many slots are left.

It can help in two ways:

* **soft help**: multiply the weight of matching entries by `_soft_mult`
* **hard guarantee**: if the remaining slots must all be matching entries in order to satisfy the rule, Fate hard-forces them

This policy is not just "always force one match." It waits until it *has* to force in order to keep the batch guarantee true.

### Arguments

`_target_entries`
The entry, or entries, that count toward the guarantee.

`_min_count`
How many matching results you want inside the batch.

If this is `1`, you are saying "at least one."
If this is `2`, you are saying "at least two."

`_roll_count_at_least`
The minimum requested roll size needed before the policy does anything.

If this is `10`, then `Roll(1)` ignores the policy, while `Roll(10)` uses it.

`_soft_mult`
An optional multiplier for matching entries while the guarantee is still trying to be satisfied.

If this is `1`, there is no soft boost.
If this is greater than `1`, matching entries become more likely before the hard force point.

`_allow_bypass_filters`
Controls whether Fate is allowed to hard-force matching entries when it has to satisfy the guarantee.

If this is true, and the guarantee reaches a point where all remaining slots must be matching entries in order to satisfy the batch minimum, Fate can hard-force those remaining slots into the matching set.

If this is false, Fate can still soft-boost matching entries, but it will not force the remaining slots through exclusion-style filters.

### When you should use it

Use batch guarantee when your question is:

* "If the player does a 10-pull, I want at least one item from this quality tier."
* "If the player does a 20-pull, I want at least two healing items in that bundle."

### When you should *not* use it

Don't use batch guarantee for long-term bad-luck protection across many separate rolls. That's pity.

Don't use it for repeat control. That's duplicate protection.

## EnableTenPullGuarantee(...)

```js
EnableTenPullGuarantee(_target_entries, _min_count = 1, _soft_mult = 1, _allow_bypass_filters = true, _roll_count = 10)
```

This is just a friendlier wrapper around `EnableBatchGuarantee(...)`.

It exists because "10-pull guarantee" is a very common pattern in gacha-style tables.

You can think of this as:

```js
EnableBatchGuarantee(_target_entries, _min_count, _roll_count, _soft_mult, _allow_bypass_filters)
```

So if you write:

```js
loot_table.EnableTenPullGuarantee(_four_star_or_higher_entries, 1);
```

you are basically saying:

* "When the player rolls 10 at once, make sure at least 1 result matches this target set."

If you want some roll count other than 10, change `_roll_count`.

## EnableStandardGachaRules(...)

```js
EnableStandardGachaRules(_five_star_entries, _featured_entries = undefined, _pity_hard_at = 90, _pity_soft_start = 75, _rate_up_mult = 1.5)
```

Use this when you want a quick "banner-like" setup without wiring each helper manually.

### What it does

This helper adds:

* pity for `_five_star_entries`
* optional featured rate-up for `_featured_entries`

So it's a convenience helper for a common pattern:

* a rare tier that eventually guarantees
* optional featured entries inside that rare tier

### Arguments

`_five_star_entries`
The entries that count as your rare-tier pity target.

`_featured_entries`
Optional. The entries that should receive featured rate-up behavior.

`_pity_hard_at`
The hard pity threshold for the rare tier.

`_pity_soft_start`
Passed through to the pity helper.

`_rate_up_mult`
The featured-entry weight multiplier.

### Important note

By default, this helper wires in pity with a soft-pity step of `0`.

So it behaves like this:

* hard pity on the target rare tier
* optional featured rate-up

In other words, it's a convenience helper, but it's not an "every possible gacha rule preset."

If you want full manual control over soft pity behavior, just call `EnablePity(...)` and `EnableRateUp(...)` yourself.

## How multi-rolls work

Not every helper thinks about `Roll(10)` the same way, so here's a breakdown of the differences.

### Pity and rate-up

Pity and featured rate-up progress once per selected slot.

That means this:

```js
table.Roll(10, _ctx, _rng);
```

advances those policies the same way as ten sequential `Roll(1)` calls, assuming the same starting state, scope, and RNG outcomes.

### Batch guarantees

Batch guarantees are different by design.

They are batch-scoped rules. They look at the requested batch size, track how many matching results have already appeared in the batch, and only hard force when the remaining slots make that necessary.

So a batch guarantee is more like "a promise about this bundle," not "a long-term account history rule."

## Scope behavior

`EnablePity(...)` and `EnableRateUp(...)` accept `_scope_context_key`.

If you provide it, Fate reads the value stored under that field in the roll context and tracks the policy separately for each unique value it finds there.

That lets you do things like:

* separate pity per save slot
* separate pity per character
* separate featured counters per profile

Example:

```js
loot_table.EnablePity(_five_star_entries, 90, 75, 0.06, "profile_id");

var _ctx = { profile_id: "slot_2" };
FateRollValues(loot_table, 1, _ctx);
```

If you omit `_scope_context_key`, the helper uses global policy state for that table.

## Advanced policy constructors

In general, use the beginner helpers first, they solve the most common gacha-style issues.

Move to the constructors when the helper is *almost* right, but you need one extra layer of control, like:

* your target set is determined by a callback instead of a fixed entry list
* you want policy state scoped by something more specific than a global table
* you want duplicate protection keyed by your own rule, not just `entry_id` or `unique_key`
* you want duplicate protection to react differently for already-owned entries
* you want a different reset rule than the beginner helper exposes
* you want a batch guarantee based on a custom matcher

In other words, the constructors are the "same family of behavior, but with the wiring exposed."

So this is a bridge between the "beginner helpers" and "completely custom policy", as most people do **not** need a fully custom policy just because the beginner helper missed a setting or something.

## When to leave the helper layer

A good rule of thumb:

* If you still want **pity**, use `FatePityPolicy(...)`.
* If you still want **featured rate-up**, use `FateFeaturedRateUpPolicy(...)`.
* If you still want **duplicate protection**, use `FateDuplicateProtectionPolicy(...)`.
* If you still want **batch guarantees**, use `FateBatchGuaranteePolicy(...)`.
* Only build a fully custom policy when none of the built-ins describe your behavior anymore.

## FatePityPolicy(opts)

Use this when `EnablePity(...)` is conceptually right, but you need more control over *how targets are matched* or *how the pity counter resets*.

### What it adds over `EnablePity(...)`

The helper version takes a fixed entry or entry array.

The constructor version lets you define your own `target_matcher(entry, context)` callback, so the target set can be dynamic.

It also exposes `reset_mode`, which is not configurable in the helper version.

### Options

`target_matcher`
Required. A callback that returns `true` when an entry should count as a pity target.

Signature:

```js id="40hzwc"
function(_entry, _context) -> bool
```

`scope_key`
Optional. A callback that returns the pity scope key.

Signature:

```js id="c9ctzx"
function(_context) -> any
```

Returned values are stringified internally, so any stable value is fine, but a string is probably cleanest in general.

`soft_start`
Optional. Miss count where soft pity begins.

`soft_step`
Optional. Additive weight increase per soft-pity step.

`hard_at`
Optional. Miss count where hard pity begins.

`reset_mode`
Optional. Controls when the miss counter resets.

Valid values:

* `"target_hit"` -> reset only when a target is selected
* `"any_hit"` -> reset on every selection
* `"never"` -> never reset automatically

`policy_name`
Optional. Custom debug/state name.

`priority`
Optional. Used when policy conflicts need deterministic resolution.

### When you would actually use this

Use the constructor when your pity target is not just "this fixed entry list."

Examples:

* "Any 5-star tagged as weapon"
* "Any reward in the legendary tier for this profile"
* "Any entry whose rarity is high enough for the current event"

### Example

This example creates a pity policy that treats **any entry with `rarity = 5`** as a pity target.

The `_is_five_star(...)` callback checks an entry's metadata and returns `true` only when that entry is a 5-star.

That callback is passed directly into `FatePityPolicy(...)` as `target_matcher`, which means the policy is not tied to a fixed entry list. Instead, it uses a rule: if an entry is a 5-star, it counts as a pity success.

In this example:

* before 75 misses, 5-star entries keep their normal odds
* from 75 misses onward, 5-star entries gain extra weight
* after 90 misses, the next 5-star is hard-guaranteed
* `reset_mode: "target_hit"` means the pity counter only resets when a 5-star is actually selected

```js id="gk7oh3"
var _is_five_star = function(_entry, _context) {
	return _entry.GetMetadata("rarity") == 5;
};

var _pity = new FatePityPolicy({
	target_matcher: _is_five_star,
	hard_at: 90,
	soft_start: 75,
	soft_step: 0.06,
	reset_mode: "target_hit"
});

loot_table.AddPolicy(_pity);
```

## FateFeaturedRateUpPolicy(opts)

Use this when `EnableRateUp(...)` is the right idea, but your featured logic is more complex than "this fixed entry list."

### What it adds over `EnableRateUp(...)`

The helper version resolves a fixed set of featured entries.

The constructor version lets you define your own `is_featured(entry, context)` callback and your own `scope_key(context)` callback.

It also exposes `reset_mode` directly.

### Options

`is_featured`
Required. Returns `true` when an entry should count as featured.

Signature:

```js id="o6xrls"
function(_entry, _context) -> bool
```

`scope_key`
Optional. Returns the scope key for the featured miss counter.

`rate_up_mult`
Optional. Multiplies the weight of featured entries.

`hard_at`
Optional. After this many misses, featured entries become hard-forced.

`reset_mode`
Optional. Controls when the miss counter resets.

Valid values:

* `"featured_hit"` -> reset only when a featured entry is selected
* `"any_hit"` -> reset on every selection
* `"never"` -> never reset automatically

`policy_name`
Optional. Custom debug/state name.

`priority`
Optional. Conflict-resolution priority.

### When you would actually use this

Use it when "featured" is a rule, not just a fixed entry set.

Examples:

* "Any entry tagged current_banner"
* "Any character from the selected faction"
* "Any featured skin matching the active event"

### Example

This example creates a featured rate-up policy where an entry counts as featured only if its `banner_id` matches the current banner in the roll context.

The `_is_featured(...)` callback compares the entry's metadata against `_context.banner_id`, so the same policy can work for different banners depending on the context you pass in.

That's the key difference from the beginner helper. Instead of hardcoding a fixed featured entry list, the policy decides at roll time whether an entry is featured.

In this example:

* matching entries get a `1.5x` weight multiplier
* after 2 non-featured hits, a featured result becomes hard-guaranteed
* `reset_mode: "featured_hit"` means the counter only resets when a featured entry is actually selected

```js id="r9a3xb"
var _is_featured = function(_entry, _context) {
	return _entry.GetMetadata("banner_id") == _context.banner_id;
};

var _rate_up = new FateFeaturedRateUpPolicy({
	is_featured: _is_featured,
	rate_up_mult: 1.5,
	hard_at: 2,
	reset_mode: "featured_hit"
});

loot_table.AddPolicy(_rate_up);
```

If your roll context was `{ banner_id: 7 }`, then only entries tagged with banner `7` would count as featured for that roll.

## FateDuplicateProtectionPolicy(opts)

Use this when `EnableDuplicateProtection(...)` is the right family of behavior, but you need more control over *what counts as a duplicate* or *how duplicate pressure interacts with ownership and scope*.

This is probably the constructor that gives the biggest upgrade over the helper layer.

### What it adds over `EnableDuplicateProtection(...)`

The helper version gives you:

* a recent-history window
* penalize vs exclude
* `entry_id` vs `unique_key`
* optional intra-roll uniqueness

The constructor version also lets you define:

* your own `entry_key(entry, context)`
* your own `scope_key(context)`
* your own `owned_check(entry, context)`
* a separate `owned_penalty_mult`

That means you can make duplicate protection behave per account, per character, per deck, per event, and so on.

### Options

`entry_key`
Required. Returns the duplicate bucket key for an entry.

Signature:

```js id="uhfmvt"
function(_entry, _context) -> any
```

If two entries return the same key, they count as duplicates of each other.

`scope_key`
Optional. Returns the scope key for duplicate history.

This is how you make the recent-history window separate per profile, per character, and so on.

`window`
Optional. Number of recent selected keys to remember.

`mode`
Optional. `"penalize"` or `"exclude"`.

`penalty_mult`
Optional. Used in `"penalize"` mode.

`intra_roll_unique`
Optional. If `true`, duplicates are also tracked inside the current multi-roll.

`owned_check`
Optional. A callback that returns whether the entry is already owned.

Signature:

```js id="m0ivgj"
function(_entry, _context) -> bool
```

`owned_penalty_mult`
Optional. Additional multiplier applied when `owned_check(...)` returns `true`.

`policy_name`
Optional. Custom debug/state name.

`priority`
Optional. Conflict-resolution priority.

### What `owned_check` is for

This lets you say something like:

* "Recent duplicates are heavily discouraged"
* "Already-owned entries are also discouraged, even if they are not recent"

That is a different design axis than recent-history protection, and it is exactly the kind of thing the constructor layer is for.

### When you would actually use this

Use it when the helper version is too blunt.

Examples:

* "Treat all variants of the same item as duplicates"
* "Keep duplicate history separate per player profile"
* "Reduce the odds of already-owned cosmetics"
* "Use one duplicate bucket for character unlock and character shard versions"

### Example

This example uses duplicate protection for a more complex case:

* entries are grouped by `character_id`, so alternate versions of the same character count as duplicates of each other
* duplicate history is tracked separately per profile
* already-owned characters are also penalized, even if they are not recent duplicates

This needs the constructor version instead of the helper version because there are three separate callback rules:

* `_entry_key(...)` decides what counts as "the same thing"
* `_scope_key(...)` decides whose duplicate history is being used
* `_is_owned(...)` checks whether the player already owns the character

The helper can handle simple duplicate windows, but it cannot express all three of those rules together.

In this example:

* Fate remembers the last 3 selected character ids per profile
* recent duplicates are penalized down to `10%` of their normal weight
* duplicates are also prevented inside the same multi-roll
* already-owned characters get an additional `0.5x` weight penalty

```js id="68w2zw"
var _entry_key = function(_entry, _context) {
	return _entry.GetMetadata("character_id");
};

var _scope_key = function(_context) {
	return _context.profile_id;
};

var _is_owned = function(_entry, _context) {
	// This assumes you have provided some lookup structure in the context that can answer
	// "does the player already own this character id?"
	return struct_exists(_context.owned_character_ids, string(_entry.GetMetadata("character_id")));
};

var _dup_protect = new FateDuplicateProtectionPolicy({
	entry_key: _entry_key,
	scope_key: _scope_key,
	window: 3,
	mode: "penalize",
	penalty_mult: 0.1,
	intra_roll_unique: true,
	owned_check: _is_owned,
	owned_penalty_mult: 0.5
});

loot_table.AddPolicy(_dup_protect);
```

The important thing to note here is that "duplicate" no longer means "same entry id." It means "same character id in this profile's recent history."

## FateBatchGuaranteePolicy(opts)

Use this when `EnableBatchGuarantee(...)` is the right idea, but your matching rule is more complex than a fixed entry list.

### What it adds over `EnableBatchGuarantee(...)`

The helper version accepts a fixed entry or entry array.

The constructor version lets you define your own `matcher(entry, context)` callback.

That is useful whenever the guarantee is about a category, tag, tier, or dynamic condition rather than a hardcoded entry list.

### Options

`matcher`
Required. Returns `true` when an entry should count toward the batch guarantee.

Signature:

```js id="zt9n3y"
function(_entry, _context) -> bool
```

`min_count`
Optional. Minimum number of matching results required inside the batch.

`only_when_roll_count_at_least`
Optional. Minimum requested roll size needed before the policy applies.

`soft_mult`
Optional. Weight multiplier for matching entries while the guarantee is still trying to be satisfied.

`allow_bypass_filters`
Optional. Allows hard-force behavior when the remaining slots must match to satisfy the guarantee.

`policy_name`
Optional. Custom debug/state name.

`priority`
Optional. Conflict-resolution priority.

### When you would actually use this

Use it when the batch rule is category-based.

Examples:

* "Every 10-pull must contain at least one 4-star or higher"
* "Every 5-pull of consumables must contain at least one healing item"
* "Every promotional pack must contain at least two event-tagged rewards"

### Example

This example creates a batch guarantee that applies to **any entry with rarity 4 or higher**.

The `_is_four_star_or_higher(...)` callback checks metadata instead of matching a fixed entry list, which makes the policy easier to maintain if the table changes later.

The example ensures:

* the guarantee only activates on rolls of 10 or more
* the player must receive at least 1 entry matching the callback
* because `allow_bypass_filters` is `true`, Fate is allowed to hard-force the remaining slots if that becomes necessary to satisfy the guarantee

```js id="ul5jt0"
var _is_four_star_or_higher = function(_entry, _context) {
	return _entry.GetMetadata("rarity") >= 4;
};

var _guarantee = new FateBatchGuaranteePolicy({
	matcher: _is_four_star_or_higher,
	min_count: 1,
	only_when_roll_count_at_least: 10,
	soft_mult: 1,
	allow_bypass_filters: true
});

loot_table.AddPolicy(_guarantee);
```

So this policy says: "If the player does a 10-pull, make sure at least one result is 4-star or higher."

## Custom policy contract (advanced)

Only write a fully custom policy when the built-in constructors no longer describe what you are doing.

That is the point where you are no longer saying "I want pity, but with custom matching." You are saying "I want a completely different policy rule."

A custom policy struct must provide these three methods:

### `ResolveForRoll(_context, _event)`

This is where the policy inspects the current candidate entry and says what should happen to it.

Return either:

* `undefined` to do nothing
* a directive struct describing the modification to apply

Supported directive fields are:

`hard_force`
If `true`, this candidate is hard-forced.

`hard_exclude`
If `true`, this candidate is excluded completely.

`weight_mult`
Multiplies the candidate's weight.

`weight_add`
Adds to the candidate's weight.

`weight_override`
Replaces the candidate's resolved weight entirely.

`selected_via`
Optional debug label explaining why the entry was selected.

This is the "decision" phase of the policy.

### `OnSelected(_context, _event)`

Called after an entry is selected.

Use this to update policy state, like:

* pity counters
* duplicate history
* per-roll tracking
* ownership streaks
* any other running memory

This is the "state update per selected slot" phase.

### `OnRollFinished(_context, _summary)`

Called after the roll is finished.

Use this for cleanup or end-of-roll bookkeeping, especially for batch-scoped temporary state.

This is the "close out the roll" phase.

## Optional policy methods

These are not required, but they are very useful.

### `ValidateForTable(_strictness, _table_id)`

Use this to reject invalid policy config up front.

This is the best place to say things like:

* "this policy requires a callable matcher"
* "this policy requires a non-empty state key"
* "these two settings cannot be combined"

### `GetPolicyId()`

Returns a stable numeric id for the policy.

### `GetPolicyName()`

Returns a readable name used for diagnostics and state.

### `GetPriority()`

Returns policy priority.

Use this when hard-force conflicts need deterministic winners.

### `GetState()` and `SetState(_state)`

Use these when your policy has persistent state that should be saved and restored.

Examples:

* pity miss counters
* duplicate history
* featured miss counters

### `ResetScope(_scope_key)` and `ResetAll()`

Use these when your policy maintains scoped state and you want to reset some or all of it.

## Minimal custom policy skeleton

This example shows the smallest useful custom policy shape.

It doesn't actually *do* anything yet, it's simply to show the three required methods and where your logic would go.

* `ResolveForRoll(...)` decides whether the current candidate entry should be modified
* `OnSelected(...)` updates policy state after an entry is chosen
* `OnRollFinished(...)` handles end-of-roll cleanup

```js id="pb6vra"
var _policy = {
	ResolveForRoll: function(_context, _event) {
		return undefined;
	},

	OnSelected: function(_context, _event) {
	},

	OnRollFinished: function(_context, _summary) {
		return undefined;
	},

	GetPolicyName: function() {
		return "my_custom_policy";
	},

	GetPriority: function() {
		return 0;
	}
};

loot_table.AddPolicy(_policy);
```

By building off this basic shape, you can really go buckwild and implement any kind of policy you can dream of. You can store metadata in the `_policy` struct to help track things, make extra helper functions, whatever, as long as it retains these building block components.

## Callback scope and method binding

When you pass callbacks into constructor policies, bind them with method(scope, fn) if the callback needs access to extra scope data that Fate does not already provide through that callback's normal arguments.

That ensures you have access to the correct scope within your function and gives you flexibility beyond what Fate can provide.

```js id="4ixk5l"
var _id = id;
var _some_other_data = "Hello";
var _scope = {
	my_id: _id,
	my_other_data: _some_other_data,
};

var _is_featured = function(_entry, _context) {
	if (instance_exists(my_id) && my_other_data == "Hello")  {
		return _entry.GetMetadata("banner_id") == 7;
	}
	return false;
}

var _policy = new FateFeaturedRateUpPolicy({
	is_featured: method(_scope, _is_featured)
});
```

In that example, we want access to the id of the instance that is running the code, and some extra metadata ("Hello"), so we build a little local scope struct, and bind the function to that scope via the `method()` function. This means you have direct access to `my_id` and `my_other_data` inside the function. Obviously, the toy example where I'm checking whether the instance exists and the other data is "Hello" is just some example code to show usage.

## Policy order and conflicts

Policies are evaluated in registration order. That means broad rules should usually be added first, and more specialized rules later.

Priority exists for the moments where you need a deterministic winner, especially for hard-force conflicts.

A good default strategy is:

* register broad policies first
* register stronger, more specific policies after them
* only use priority when order alone is not enough

That keeps policy interactions understandable overall.
