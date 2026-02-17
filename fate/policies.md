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

Policies are the rule layer that modifies how Fate chooses entries. In practice, they let you implement pity, featured rate-up, duplicate protection, and batch guarantees.

## Beginner policy methods (recommended first)

Start with the beginner helpers on `FateTable`:

```js
EnablePity(_target_entries, _hard_at = 90, _soft_start = 75, _soft_step = 0.06, _scope_context_key = undefined)
EnableRateUp(_featured_entries, _rate_up_mult = 1.5, _hard_at = undefined, _reset_on_any_hit = false, _scope_context_key = undefined)
EnableDuplicateProtection(_window = 1, _mode = "penalize", _penalty_mult = 0.25, _key_mode = "entry_id", _intra_roll_unique = true)
EnableBatchGuarantee(_target_entries, _min_count = 1, _roll_count_at_least = 10, _soft_mult = 1, _allow_bypass_filters = true)
EnableTenPullGuarantee(_target_entries, _min_count = 1, _soft_mult = 1, _allow_bypass_filters = true, _roll_count = 10)
EnableStandardGachaRules(_five_star_entries, _featured_entries = undefined, _pity_hard_at = 90, _pity_soft_start = 75, _rate_up_mult = 1.5)
```

These methods take direct `FateEntry` targets (a single entry or an array), which removes callback complexity for the common cases. This is likely all you need to create nice feeling loot tables that respect the player in the majority of cases. The rest of the policy functionality is for when you have very specific targeted tweaks you want to make.

## Common beginner examples

### Pity

```js
loot_table.EnablePity(_five_star_entries, 90, 75, 0.06);
```

### Featured rate-up

```js
loot_table.EnableRateUp(_featured_entries, 1.5, undefined, false);
```

### Duplicate protection

```js
loot_table.EnableDuplicateProtection(1, "penalize", 0.25, "entry_id", true);
```

Use `_key_mode = "unique_key"` if multiple entries should share the same duplicate bucket.

### Ten-pull guarantee

```js
loot_table.EnableTenPullGuarantee(_four_star_or_higher_entries, 1, 1, true, 10);
```

## Scope behavior (session/account/character)

`EnablePity` and `EnableRateUp` accept `_scope_context_key`.

If provided, Fate reads that key from roll context and tracks policy state per key value. This enables you to scope the context of a policy to a specific arena, such as per character, or per account.

```js
loot_table.EnablePity(_five_star_entries, 90, 75, 0.06, "profile_id");

var _ctx = { profile_id: "slot_2" };
FateRollValues(loot_table, 1, _ctx);
```

If `_scope_context_key` is omitted, policy scope is global.

## Advanced policy constructors

If the helpers aren't enough, use constructors and register with `AddPolicy(...)`. Fate ships with `FatePityPolicy`, `FateDuplicateProtectionPolicy`, `FateBatchGuaranteePolicy`, and `FateFeaturedRateUpPolicy`.

Then attach:

```js
var _policy = new FatePityPolicy({
	target_matcher: method(_scope, _scope.MatchFiveStar),
	hard_at: 90,
	soft_start: 75,
	soft_step: 0.06
});

table.AddPolicy(_policy);
```

## Custom policy contract (advanced)

These are for when you *really* want to get into the weeds with policies, and deal with specifics. You can create whatever policy style you like with these, and are no longer limited to the standard "pity", "rate up", etc style tweaks.

A custom policy struct must provide `ResolveForRoll(_context, _event)`, `OnSelected(_context, _event)`, and `OnRollFinished(_context, _summary)`.

Optional metadata/lifecycle methods are supported (`GetPolicyId`, `GetPolicyName`, `GetPriority`, `ValidateForTable`, `GetState`, `SetState`, `ResetScope`, `ResetAll`).

## Callback scope and method binding

When passing callback functions to policy constructors, it's often a good idea to bind explicit scope with `method(scope, fn)`, so you can ensure that your function acts on the thing you want it to act on (this isn't a requirement, just a general piece of advice).

```js
policy = new FateFeaturedRateUpPolicy({
	is_featured: method(my_scope, my_scope.IsFeatured)
});
```

This avoids scope bugs and keeps policy behavior predictable.

## Policy order and conflicts

Policies are evaluated in registration order, with policy priority used for hard-force conflict resolution. As you build your policies, you should try to register broad rules first, then register stronger or more specialized rules later, and only reach for priority when you need deterministic winners.
