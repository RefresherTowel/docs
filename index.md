---
layout: default
title: Home
nav_order: 1
---

[![Framework icon](./assets/framework_bundle_icon.png){: style="width: 416px;" }]()
{: .text-center }
# Frameworks
{: .text-center}
*All you need in one bundle!*
{: .text-center}

Welcome to the hub for all documentation related to the GameMaker focused frameworks created by RefresherTowel Games.

Each framework is built to solve a specific pain point, with a clean API, full Feather support, and detailed docs.

---

[![Statement icon](./assets/statement_icon.png){: style="max-width: 256px;"}](/docs/statement/)
{: .text-center }
## [**STATEMENT**](/docs/statement/)
{: .text-center }
> #### *Turn your states into a Statement!*

Tired of giant `if` chains and switch blocks trying to keep your player or enemies in the right state?

**Statement** is a lightweight but feature rich state machine framework for GameMaker. It gives each object a clear set of states with `Enter`, `Update`, `Exit`, and optional `Draw` handlers.

- Clean, named states instead of scattered `state == ...` checks.
- Simple to start: one machine, a couple of states, and a single `Update()` call.
- Opt in extras when you need them: queued transitions, state stacks, history, transition payloads, non interruptible states, and more.

##### [**PURCHASE STATEMENT**]()
{: .text-center }
##### [**EXPLORE THE STATEMENT DOCS**](/docs/statement/)
{: .text-center }

---

[![Pulse icon](./assets/pulse_icon.png){: style="max-width: 256px;"}](/docs/pulse/)
{: .text-center }
## [**PULSE**](/docs/pulse/)
{: .text-center }
> #### *The beating heart of your game*

Want damage events to update your health bar, play a sound, and trigger screen shake, without wiring everything together by hand?

**Pulse** is a lightweight signals and events framework for GameMaker. It gives you a clean way to broadcast events and let any number of listeners react.

- Subscribe listeners once and decouple them from the sender.
- Fire a signal and let UI, audio, VFX, and gameplay all respond.
- Advanced tools for later: consumable signals, priorities, deferred processing, tags, and sender filters.

> Note: Pulse is not released yet. These docs are here as a preview and may change before launch. Right now, only **Statement** is available on itch.
{: .note}

##### [**LEARN MORE ABOUT PULSE**](/docs/pulse/)
{: .text-center }

---

[![Catalyst icon](./assets/catalyst_icon.png){: style="max-width: 256px;"}](/docs/catalyst/)
{: .text-center }
## [**CATALYST**](/docs/catalyst/)
{: .text-center }
> #### *Turn raw numbers into reactions*

Struggling to keep your stats, buffs, and item effects under control as your game grows?

**Catalyst** is a feature rich yet easy to use stats and modifiers framework for GameMaker. It treats stats as living systems instead of isolated numbers.

- Handle health, damage, resistances, buffs, debuffs, item bonuses, and more in one consistent way.
- Stack and combine effects without writing a new special case every time.
- Built for weird ideas: context aware modifiers, derived stats, and complex interactions without tearing up your code.

> Note: Catalyst is not released yet. These docs are here as a preview and may change before launch. Right now, only **Statement** is available on itch.
{: .note}

##### [**LEARN MORE ABOUT CATALYST**](/docs/catalyst/)
{: .text-center }

---

[![Echo icon](./assets/echo_icon.png){: style="max-width: 256px;"}](/docs/echo/)
{: .text-center }
## [**ECHO**](/docs/echo/)
{: .text-center }
> #### *Hear what your game is telling you*

Plain debug logs are fine at first, but quickly become noise once your project grows.

**Echo** is a lightweight **debugging** framework for GameMaker. Your game is always talking and Echo helps you hear what it is telling you. Instead of a wall of `show_debug_message()` calls, you get structured logs, levels, history, and tools that make problems stand out instead of hiding in the noise.

- Log at different levels and filter what hits the console.
- Keep a debug history for the current session and dump it to file when needed.
- Optional extras like stack traces and an easy way to mute all logging with a single setting.

Echo ships free with all available frameworks and integrates cleanly with their designs.
