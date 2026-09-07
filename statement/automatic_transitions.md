---
layout: default
title: Automatic Transitions
parent: Statement 2
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

# Automatic Transitions

Sometimes state changes happen at complicated moments that require a specific sequence of events to occur, but a lot of state changes are really simple rules that belong to the state for as long as it stays active. `Move`, for example, may always want to return to `Idle` once movement input reaches zero.

You can choose to put that check in Move's Update handler and there's nothing wrong with doing that, but as a state collects more and more exit conditions, keeping those conditions as **transition rules** can help separate the logic of your actual state from the logic of how your state is exited. Statement Lens can also inspect those those transition rules directly.

---

## Adding a transition rule

Here's a Move state with ordinary movement in Update and a rule that returns to Idle:

```js
var _move = new StatementState(self, "Move")
	.AddUpdate(function() {
		var _direction = keyboard_check(vk_right) - keyboard_check(vk_left);
		x += _direction * move_speed;
	})
	.AddTransition(
		new StatementTransitionRule("Idle", function() {
			var _direction = keyboard_check(vk_right) - keyboard_check(vk_left);
			return _direction == 0;
		})
	);
```

First, we call `AddTransition()`, which takes a `StatementTransitionRule` as an argument.

The `StatementTransitionRule` is constructor that takes two arguments: the destination state, `"Idle"` in this case, and then a condition function:

```js
function() {
	var _direction = keyboard_check(vk_right) - keyboard_check(vk_left);
	return _direction == 0;
}
```

Statement checks that function each logical update while `Move` is active. Returning `false` means that rule is inactive for the check. Returning `true` means the rule wants to transition to `Idle`, so Statement attempts that state change.

The rule is a struct rather than just a target name and function buried somewhere inside the state. This is so we can keep a proper reference to it for if we need to change its priority, turn it off temporarily, remove it, or inspect exactly that rule in Lens.

> A function whose sole purpose is to return a `true` or `false` value is often called a **predicate function**. You might see this term used occasionally throughout the docs (though I've tried to avoid it, as I think it's needless jargon, but it might slip through by accident).
{: .note}

---

## Rule conditions use the state owner

Transition-rule conditions run as the owner of the state or machine they're attached to, just like state handlers.

If this state belongs to the player:

```js
var _move = new StatementState(self, "Move");
```

then its condition can use the player's variables directly:

```js
_move.AddTransition(
	new StatementTransitionRule("Exhausted", function() {
		return stamina <= 0;
	})
);
```

You don't need to wrap the condition in `method(self, ...)`.

Statement can also give the condition the active state and the rule struct itself when you need them:

```js
new StatementTransitionRule("Idle", function(_state, _rule) {
	return _state.TimerGet() >= 30;
})
```

The arguments are just like the `_state` and `_transition` arguments we added to our state handlers, Statement automatically fills them with the appropriate data for you. Your function can call them whatever you like, and you can leave them out completely when the condition only needs owner variables.

For a rule attached directly to a state, `_state` is that active state. For a machine-wide rule, it's whichever state is active when the rule is being checked.

---

## Rules run after Update by default

A new rule starts in:

```js
eStatementTransitionPhase.AFTER_UPDATE
```

so one logical machine update normally reaches it in this order:

```text
Move is active
    ↓
Move Update runs
    ↓
Statement checks Move's AFTER_UPDATE rules
    ↓
first passing rule is attempted
```

That default works well for conditions that should be checked after the state has done its work for this update. If Move's Update changes the movement variables, for example, the rule sees their new values after the state runs, instead of the stale values from before the state ran its code.

---

## Checking a rule before Update

Sometimes the condition means the old state shouldn't get another Update at all.

Suppose `stun_pending` is set by some other gameplay system and `Normal` should give way to `Stunned` before Normal gets to act again:

```js
var _stun_rule = new StatementTransitionRule(
	"Stunned",
	function() {
		return stun_pending;
	}
)
.SetPhase(eStatementTransitionPhase.BEFORE_UPDATE);

_normal.AddTransition(_stun_rule);
```

Now the order is:

```text
Normal is active
    ↓
check BEFORE_UPDATE rules
    ↓
stun rule passes
    ↓
enter Stunned
    ↓
Stunned receives this logical update
```

The old `Normal` Update never runs for that opportunity. A Before-Update rule is therefore appropriate when passing the condition means "the current state shouldn't act again." After-Update is appropriate when the current state should finish its Update first.

---

## Several rules can compete

A state can have more than one transition rule:

```js
var _move = new StatementState(self, "Move")
	.AddTransition(
		new StatementTransitionRule("Attack", function() {
			return attack_pressed;
		})
	)
	.AddTransition(
		new StatementTransitionRule("Idle", function() {
			return move_axis == 0;
		})
	);
```

If only one condition returns `true`, there is no conflict. If both are going to pass during the same phase, priority decides which rule gets checked first and therefore which rule wins the transition.

```js
var _attack_rule = new StatementTransitionRule(
	"Attack",
	function() {
		return attack_pressed;
	}
)
.SetPriority(20);

var _idle_rule = new StatementTransitionRule(
	"Idle",
	function() {
		return move_axis == 0;
	}
)
.SetPriority(0);

_move
	.AddTransition(_attack_rule)
	.AddTransition(_idle_rule);
```

Higher numbers are evaluated first:

```text
Attack priority 20 -> checked first
Idle   priority 0  -> checked later if needed
```

Rules with the same priority keep the order they were added. You only need to set priorities where two true conditions genuinely need an ordering. Leaving ordinary rules at the default priority of `0` is usually fine unless you explicitly want one rule to win a tie.

---

## The first passing rule ends that phase's search

Once a rule returns `true`, Statement attempts that transition and stops evaluating later rules for the same phase.

If the transition is blocked by an exit lock or exit guard, Statement doesn't fall through and try the next rule as an alternative:

```text
Attack rule passes
    ↓
Attack transition is blocked by an exit lock
    ↓
Idle rule is not checked as a fallback
```

The condition has already said which transition this evaluation wants. A lock or guard rejecting that transition doesn't turn a lower-priority rule into a second choice.

There is one deliberate exception for self-target rules. If the passing rule points to the state that's already active, Statement skips that rule and keeps looking. Automatic rules don't re-enter the current state. Use a literal `ReenterState()` command in the Update code for that.

---

## If Update changes state, the old After-Update rules are finished

Direct changes and automatic rules can live on the same state without fighting each other.

```js
var _move = new StatementState(self, "Move")
	.AddUpdate(function() {
		if (hp <= 0) {
			state_machine.ChangeState("Dead");
			return;
		}
	})
	.AddTransition(
		new StatementTransitionRule("Idle", function() {
			return move_axis == 0;
		})
	);
```

If Move's Update successfully enters `Dead`, Statement doesn't then evaluate Move's After-Update rules. Move is no longer active, so its remaining rules no longer describe the current situation.

The same idea applies whenever a rule condition or data provider itself changes state. Statement notices that the active state changed and stops that evaluation rather than applying a rule from a state that has already been left.

---

## Giving a rule fixed transition data

Automatic transitions can carry the same kind of payload as `ChangeState()`.

```js
var _timeout_rule = new StatementTransitionRule(
	"Patrol",
	function() {
		return state_machine.GetStateTime() >= 120;
	}
)
.SetData({ reason: "timeout" });

_waiting.AddTransition(_timeout_rule);
```

When the rule fires, `Patrol` receives that payload through its Enter transition:

```js
var _patrol = new StatementState(self, "Patrol")
	.AddEnter(function(_state, _transition) {
		var _data = _transition.GetData();
		EchoDebugInfo("Entered Patrol because " + string(_data.reason));
	});
```

Use `SetData()` when the payload is part of the rule's definition and doesn't need to be rebuilt each time it fires.

---

## Building the payload when the rule fires

Sometimes the data should capture values from the exact moment the condition passes.

Suppose an enemy should enter `Targeted` with whichever player is currently nearest:

```js
var _target_rule = new StatementTransitionRule(
	"Targeted",
	function() {
		return instance_exists(nearest_player);
	}
)
.SetDataProvider(function() {
	return {
		target: nearest_player,
		distance: point_distance(x, y, nearest_player.x, nearest_player.y)
	};
});
```

The provider doesn't run every time the condition is checked. Statement calls it after the condition has passed, just before attempting that transition. That avoids building payloads for rules that aren't firing and makes the data describe the world at the moment of the attempt.

Like a condition, a data provider can receive the active state and rule when needed:

```js
.SetDataProvider(function(_state, _rule) {
	return {
		state_time: state_machine.GetStateTime()
	};
})
```

`SetData()` removes any existing provider, while `SetDataProvider()` makes the provider the source of transition data instead. A rule uses one or the other.

---

## Temporarily disabling one rule

If a rule still belongs to the state but shouldn't participate for a while, keep a reference to the rule you added:

```js
attack_rule = new StatementTransitionRule(
	"Attack",
	function() {
		return attack_pressed;
	}
);

_move.AddTransition(attack_rule);
```

and disable it:

```js
attack_rule.SetEnabled(false);
```

Later:

```js
attack_rule.SetEnabled(true);
```

The rule remains attached with the same target, priority, phase, and data. Statement just skips it while it's disabled.

---

## Removing rules

When a particular rule no longer belongs to the state at all, you can remove it completely with:

```js
attack_rule.Remove();
```

or:

```js
_move.RemoveTransition(attack_rule);
```

Both detach that exact rule. To remove every transition rule from one state:

```js
_move.ClearTransitions();
```

A rule can only be attached to one state, machine, or template at a time. If two places need the same behaviour, create separate rules (templates automatically clone their rules when they build states).

---

## Machine-wide rules

Some conditions apply regardless of which ordinary state is active. Health reaching zero is a common example:

```js
var _death_rule = new StatementTransitionRule(
	"Dead",
	function() {
		return hp <= 0;
	}
)
.SetPriority(100)
.SetPhase(eStatementTransitionPhase.BEFORE_UPDATE);

state_machine.AddTransition(_death_rule);
```

Because the rule is attached to the machine rather than one state, Statement considers it from any active state. You don't need to copy the same death condition onto Idle, Move, Attack, Hurt, or any state you add later.

Machine-wide and state-local rules are evaluated together. Priority still decides their order, and when a machine rule and state rule have the same phase and priority, the machine-wide rule wins that tie. Equal-priority rules within the same container keep their insertion order.

Machine-wide rules can therefore win the tie without needing an arbitrary priority bump just to get ahead of an otherwise identically prioritised local rule.

---

## Forced rules

Rules normally respect the active state's exit locks and guards. A rule that should ignore those gates can be marked as forced:

```js
var _death_rule = new StatementTransitionRule(
	"Dead",
	function() {
		return hp <= 0;
	}
)
.SetForce();
```

This is the rule equivalent of:

```js
state_machine.ChangeState("Dead", undefined, true);
```

`SetForce()` defaults to `true`, so no argument is needed when you're enabling it. Use a forced rule for a transition that outranks the normal exit restrictions, not as a way to paper over a lock or guard that was configured incorrectly.

---

## Evaluating a phase yourself

`Update()` normally evaluates Before-Update and After-Update rules at the right points automatically.

Code with its own scheduling can ask Statement to evaluate one phase directly:

```js
var _result = state_machine.EvaluateTransitions(
	eStatementTransitionPhase.AFTER_UPDATE
);
```

If no rule passes, the return value is `undefined`. If a rule passes, you get the transition result from the attempted change, including a blocked result if a lock or guard rejected it.

Calling this yourself only evaluates transition rules. It doesn't stand in for the rest of `Update()` such as state Update handlers, queue processing, state age, or anything else like that.

---

## Direct changes and rules solve different problems

Use a direct transition when a particular piece of code has just made the decision, especially if that chunk of code might be a part of some complicated machinery (for instance, several layers deep in a stack chain of calls or in the middle of some loop or something):

```js
if (attack_pressed) {
	// Just some pseudo-scenario where you might be triggering a state change in the middle of a loop
	var _col = collision_line_list(x1, y1, x2, y2, obj_enemy, false, true, col_list, true);
	for (var i = 0; i < _col; i++) {
		if (!col_list[| i].blocking) {
			state_machine.ChangeState("Attack");
			break;
		}
	}
}
```

Use a rule when the condition has a clear execution point that doesn't belong to any surrounding code in the Update. Rules are often neater to work with, since you can see them all separately lined up, rather than a state change nestled in the middle of a big codeblock in the Update:

```js
_move.AddTransition(
	new StatementTransitionRule("Idle", function() {
		return move_axis == 0;
	})
);
```

You don't need to convert every `ChangeState()` into a rule. A state can use both, and which one you choose really depends on your personal preferences and the shape of the code that triggers the state change.

---

## Putting it together

Here's a small player machine where Move owns its return-to-idle rule and the machine owns a death rule that applies everywhere:

```js
state_machine = new Statement(self);

var _idle = new StatementState(self, "Idle")
	.AddUpdate(function() {
		if (move_axis != 0) {
			state_machine.ChangeState("Move");
		}
	});

var _move = new StatementState(self, "Move")
	.AddUpdate(function() {
		x += move_axis * move_speed;
	})
	.AddTransition(
		new StatementTransitionRule("Idle", function() {
			return move_axis == 0;
		})
	);

var _dead = new StatementState(self, "Dead")
	.AddEnter(function() {
		sprite_index = spr_player_dead;
	});

var _death_rule = new StatementTransitionRule(
	"Dead",
	function() {
		return hp <= 0;
	}
)
.SetPriority(100)
.SetPhase(eStatementTransitionPhase.BEFORE_UPDATE)
.SetForce();

state_machine
	.AddState(_idle)
	.AddState(_move)
	.AddState(_dead)
	.AddTransition(_death_rule)
	.Start();
```

`Move -> Idle` only means something while Move is active, so it belongs explicitly on Move. `Anything -> Dead` belongs to the machine, so it's declared once at the machine level.

---

## Next: locks and queues

A transition rule can decide that a state wants to leave, but the active state may not be ready to allow that transition yet. An attack state might lock you into a commitment for a second or two, for example, but the player is already pressing the next input to cancel it.

[**Locks & Queues**](locks_and_queues) covers the two parts of that problem separately: locks and guards decide whether the current state may be left, while the queue can remember one requested transition until it gets another chance to succeed.
