---
layout: default
title: Concepts
parent: Whisper
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

# Concepts

If you've never heard the word "storylet" before, you're not missing much. It's not some secret narrative lore. It's just a useful label for a thing most of us end up building by accident anyway.

In essence, you start with a couple of barks or little encounter lines, and it feels fine. Then you add a few more. Then you add conditions. Then you add cooldowns. Then you add "only once". Then you add "only once per day". Then you add "only if the player hasn't done X but has done Y and also it's raining" and suddenly your dialogue system is a ball of if statements with feelings. Storylets, as a concept, are a way to organise this kind of mess into a coherent system, and Whisper is a storylet manager for GM.

This page is about building a proper understanding what storylets are and how you should think about Whisper. There's very little code on purpose. If you understand the shape of the system, then the code pages will feel obvious instead of mysterious.

---

## What a storylet actually is

A storylet is a small piece of content that can happen when it's allowed to.

That's it.

A storylet might be a bark, a tiny narration beat, a little encounter, a hint, a one-line reaction, or a micro event that nudges the game forward. The important part isn't what it looks like on screen, the important part is that it has rules attached to it, so it doesn't show up at the wrong time.

If you've ever written "only say this line once" or "don't repeat this too often" or "only show this in the sewers", you were already thinking in storylets. You just didn't have a system that treated that as the default.

---

## Why storylets beat spaghetti logic

You can absolutely do all of this with if statements. And honestly, for small stuff, that's fine.

The pain starts when your content grows and your rules grow with it. The logic ends up scattered across objects, scripts, cutscene controllers, UI code, quest code, and whatever else happened to be nearby when you wrote that one line at 2am.

Whisper flips the direction of control. Instead of your game saying "I will manually decide which line to show", your game says "here's the situation, Whisper, you pick something that fits". Your content carries its own rules, and your gameplay code stays focused on gameplay.

In practice, that means you can keep adding content in a fast and coherent way without having to rewrite your selection logic constantly or refactor your project multiple times.

---

## The simplest mental model of Whisper

Whisper does four things:

It stores storylets. It checks which storylets are allowed right now. It picks one (usually from a pool). Then it hands you a result you can show to the player.

Whisper doesn't draw your dialogue box. It doesn't advance text. It doesn't decide when your game should talk. It just answers the question: "What should happen right now, given these rules?"

Think about it like this: your game is the director, and Whisper is the casting department, deciding what narration fits into the current role.

---

## Pools: "where are we pulling from?"

A pool is just a named group of storylets. Think of it like general categories of narration.

Pools keep you from asking Whisper to pick from the entire universe when you really meant "pick one of the blacksmith's barks" or "pick a town gossip line". You get to be clear about where you're drawing from, and that makes your content more predictable and easier to test.

In real projects, pools usually map to something you can say out loud. "Bridge chatter." "Combat taunts." "Tutorial hints." "Forest encounters." If you can name the category, it probably deserves a pool.

---

## Context: "what's going on right now?"

Context is a struct you pass into Whisper when you ask it to pick something. It's basically you handing Whisper the information it needs to make sensible decisions.

This is one of Whisper's biggest strengths: Whisper doesn't need to know anything about your game. It doesn't need to know what your quest system looks like, or what your player object is called, or how you store flags. You pass in what matters, and your storylets can read it.

If you see the word "predicate" in the Whisper, just remember: Predicates are just a function that returns true or false. It's the storylet asking: "Am I allowed right now, given this context?"

So context is where you put whatever your predicates need. The player. The location. The current quest stage. The mood. The difficulty. Whatever makes sense for your game. And then you write out simple predicates that are attached to different parts of the narrative (i.e. "Has the player visited the well?").

---

## The knobs storylets usually have

This is where storylets stop being "random lines" and start feeling intentional and procedurally generated.

### Tags

Tags are labels. They're strings you attach to storylets so you can filter or prefer certain kinds of content.

The important thing is how they feel in practice. Tags are your way of saying "this line belongs to this vibe". Then later you can ask Whisper for that vibe. You can require tags, exclude tags, or just gently prefer tags without making them mandatory.

If you're a beginner, here's the comfort takeaway: tags are optional. You can start without them and add them later when your content gets bigger.

A good example of how tags can be super useful is this: Imagine you are making Mass Effect. You have the Renegade and the Paragon morality system. How would you decide which lines of dialogue characters choose to say based on the morality system? Well, you'd write a "positive" line and tag it "paragon" and a negative line and tag it "renegade", then when it comes time for a character to choose what line they want to say, you'd just provide Whisper with the appropriate tag and everything else falls out cleanly.

### Weight

Weight is how common something is compared to other things. If one storylet has weight 10 and another has weight 1, the weight 10 one will show up roughly ten times as often, assuming both are eligible.

This is perfect for "common lines" versus "rare lines" without you writing special-case logic.

### Cooldown

Cooldown is Whisper's built-in "stop spamming this" tool. After a storylet fires, it won't be eligible again until enough time has passed.

What counts as "time" is up to you. It can be real seconds, turns, in-game minutes, or whatever clock your project uses. Whisper doesn't care, as long as you're consistent. If your time unit is turns, your cooldown values should be in turns. If it's "visited new rooms" then progress it every time a new room is entered. By default it acts as seconds though.

### Max uses

Max uses is the hard limit. "This can only happen N times."

There are two kinds: total uses, and per-run uses. Total uses is the strict one: once it's used up, it's gone forever. Per-run uses is the nicer one: it can happen again later, but not too much within the same session.

---

## Runs: what that means, without roguelike baggage

A "run" is just a reset boundary you define. That's all.

A run could be a roguelike run, sure, but it could also be one conversation, one mission, one day, one dungeon floor, one room visit, or whatever chunk makes sense in your game.

Per-run limits exist because sometimes you want content to feel special without permanently deleting it from the game. Maybe a hint can happen once per conversation, or a rare bark can happen once per day, or an encounter can happen twice per mission. Runs give you a clean way to express that.

---

## Pick vs Fire: why Whisper separates them

You'll see two ideas in Whisper: picking and firing.

Picking is selecting which storylet would happen. Firing is committing to it. Firing is when Whisper updates cooldowns and usage counts, and runs hooks.

If you just want the easy path, you can treat this as one step and never think about it again. Whisper has helpers that pick and fire together.

But the separation is there because sometimes you want control. Maybe you're previewing options for a UI menu. Maybe you're testing. Maybe you're doing a "choose one of these three lines" thing. Pick lets you inspect and decide. Fire is the moment you say "ok, that happened".

In other words: pick is offering choice, fire is marking the choice as used.

---

## Why Whisper returns more than a string

A lot of systems just give you text. Whisper can do that too, but it also supports two extra features that are worth understanding:

Insertions are template replacements, like writing "Hey, ##player_name##" and having Whisper fill it in.

Verbs are timed events inside text, like triggering a sound or an animation partway through a line while your typewriter effect is revealing it.

Because of that, Whisper often returns a result that includes the final `text` plus an `events` list. If you're not using verbs, you can ignore events completely and just display the text like normal.

The important concept here is that Whisper can keep your text and your little timed effects in sync, without you having to split one line into ten pieces to get the timing right.

---

## An example of storylets in usage

Imagine a town square. You add some ambient lines so it doesn't feel dead.

At first it's easy. You just pick a random line.

Then you notice problems. One line shouldn't show up after a quest is complete. Another line is funny, but not funny every ten seconds. Another line is meant to be rare. Another line should only happen at night.

If you do this with raw if statements, you end up tracking cooldowns yourself, tracking "already said" flags yourself, and putting quest checks everywhere.

With storylets, you attach those rules to the content itself. The "well quest" line carries the rule "only if the well quest isn't solved". The funny line carries the rule "cooldown 10 minutes". The rare line carries a smaller weight. The night line checks the context for time-of-day.

Then, when the player enters the town square, your game asks: "give me a town square line for this situation". Whisper does the boring bookkeeping, and you get to keep writing content.

That's the real pitch. Whisper controls the backend and allows you to scale up your complexity with ease.

---

## When storylets are a great fit (and when they aren't)

Storylets are a great fit when your game has lots of small beats and you want variety without chaos. They're especially good for barks, ambient chatter, reactive narration, hints, and small encounters that should feel context-aware. The roguelike Hades is a perfect example of the kind of system that Whisper is designed to build. Lots of small bits of content that can become available under specific conditions, and a selection system that keeps things feeling fresh across repeated play.

They aren't the best tool for strictly linear scenes where you need exact ordering every time. For those, you'll probably still use a dialogue tree or a scripted sequence.

Most games end up using both: fixed scenes for the big moments, storylets for the world feeling like it notices what the player is doing.

It's important reinforcing that storylets (and Whisper) aren't a **dialogue system**. They don't draw the dialogue on the screen for you. They are intended to be the backend system that decides *what* dialogue your existing dialogue system should show, allowing you to use rules and "vibes" to procedurally surface the correct dialogue for the moment.

---

## What to read next

If this page made storylets and Whisper click for you, the next step is the Usage page. That's where we take these ideas and turn them into a clean workflow you can copy into a real project.

After that, if you want the fun stuff, jump into Verbs and Insertions. That's where Whisper goes from "smart line picker" to "text that can dynamically change and actually do things at the right moment".
