# Catalyst 2 + Statement 2 voice analysis for Sundial

This is the writing model used for the new Sundial docs. The comparison excludes the generated API-reference pages because those are intentionally a different, terse reference register.

## The core voice

The docs speak like an experienced GameMaker developer explaining a system to another developer while actively using it. They are conversational, but the conversation always serves the mechanics. They do not put on a generic "friendly docs" voice and they do not begin by taxonomising everything the library contains.

The strongest recurring move is **problem first, abstraction second**. A page usually opens with something the reader already understands in game terms, then introduces the library concept as the answer to that problem. Resources begin from "73 HP out of 100 takes 20 damage", Effects begin from burning being several related behaviours with one lifetime, Statement begins from the familiar state-variable-to-Frankenstein-switch progression. The abstraction earns its name after the reader already has a reason to want it.

That is the main thing Sundial needs to preserve. "A full-screen tint becomes awkward when an interior and a sunset are visible at once" is much closer to the existing voice than "Sundial supports red-channel masks for indoor/outdoor segmentation."

## Reader relationship

The docs use **you** constantly and **we** when walking through an example together. The corpus is full of constructions such as "Suppose the player...", "Now...", "If you...", "You can...", and "We can...". This makes the docs feel like someone building the example beside the reader rather than issuing instructions from outside it.

First person appears occasionally when there is a genuine authorial judgement: "I encourage you not to pigeon-hole...", "I've tried to avoid it...", or "I won't touch on that here." It is not used to manufacture personality into every paragraph.

The reader is assumed to be capable. Beginner questions are answered directly, but the text does not become baby talk. When jargon is useful, it is introduced in plain language and then used normally afterward.

## Explanation pattern

A common section rhythm is:

1. establish the concrete game problem;
2. show the smallest useful code;
3. explain what the call actually did;
4. show the next consequence or variation;
5. explain why the API is shaped that way;
6. only then move into edge cases or advanced control.

The docs rarely drop a large code sample and expect the reader to infer the model from it. Code is followed by prose that explains ownership, lifetime, ordering, or the meaning of the returned value.

This is especially visible when the API could otherwise look arbitrary. The docs explain *why* `Decrease()` treats its argument as a magnitude, *why* a Resource is different from a Statistic, *why* transition rules are separated from state Update code, and *why* some manager callbacks exist instead of telling the reader only that those methods exist.

## Concrete examples do most of the teaching

Examples are not decoration. They are the primary explanatory mechanism.

Catalyst repeatedly uses HP, damage, weapons, poison, stamina, population, city growth and equipment. Statement uses Idle/Move/Attack, hurt states, boss phases and buffered input. The examples stay concrete long enough for the reader to build a mental model, then the prose generalises the lesson.

The examples also deliberately move outside the most obvious genre when a concept risks being pigeon-holed. Catalyst explicitly jumps from RPG stats to platformer jump height and city-builder population. That is an authorial habit worth keeping when Sundial risks being read as "only for open-world day/night games".

## Tone and humour

The index pages are allowed to be looser and funnier. Statement's two-storey switch block and absurd ladder bug are doing real work: they identify the pain point in recognisable developer language before the library is introduced.

Deep teaching pages become calmer. There are still small asides and ordinary phrases such as "there isn't much reason", "you may dynamically want", "or something like that", and "this distinction rarely matters", but jokes do not compete with the explanation.

The docs are willing to state preferences. They say when one pattern is normally easier to read, when a feature is probably unnecessary for most gameplay code, or when a different architecture would be better but is outside the scope of the page. This makes them sound authored rather than neutralised.

## Sentence rhythm and punctuation

Across the non-generated Catalyst and Statement teaching pages, the average sentence is roughly 21 to 23 words. The writing often uses medium-length causal sentences rather than lots of tiny punchy fragments.

Fragments do appear for effect on landing pages, but they are not the default rhythm.

The current corpus uses effectively no em dashes and almost no semicolons. Parentheses are common for natural asides. Colons are common when introducing examples or small lists. Contractions are normal: "don't", "isn't", "you'll", "doesn't".

Questions are used when they represent the reader's real next question, not as a marketing tic. Headings such as "Why not just use `Change()`?" work because the preceding explanation naturally creates that question.

## Reassurance without hand-holding

A repeated pattern is narrowing the amount the reader needs to care about right now:

- "You don't need to..."
- "Most gameplay code will..."
- "Normally..."
- "For ordinary use..."
- "Later..."

This is not generic reassurance. It is scope control. The docs tell the reader which complexity is relevant now and which part can safely be ignored until a real problem requires it.

Sundial benefits heavily from this because the runtime contains normalized timing, internal phases, period boundaries, clock origin, automatic synchronization and a compiled IDE bridge. The docs should expose those only when the reader has a reason to care about them.

## Notes and asides

Callout notes are often used for the thing a reasonably curious reader is likely to wonder about but which would derail the main progression if explained inline. They can be fairly substantial. The tone is usually "here is what is actually happening underneath" rather than a generic warning box.

The docs also openly distinguish the simple model from implementation detail. Statement explains where an injected handler argument really comes from. Catalyst explains ordinary GameMaker serialisation before discussing save repair. This is useful when a piece of behaviour otherwise looks magical.

## Page architecture

Both current doc sets are progressive courses disguised as reference documentation.

The index gives a minimal successful setup, establishes the conceptual model, and tells the reader exactly where to go next. Teaching pages then add one problem at a time. Pages commonly end by summarising what was just learned and bridging directly into the next concept.

The API Reference is deliberately last. Its intro explicitly tells the reader that it is for exact lookup and that the teaching pages are where explanations and worked examples live.

For Sundial, that suggests a much smaller tree because there are fewer independent concepts:

- Index
- Using the IDE Plugin
- Runtime Usage
- Time, Periods & Callbacks
- Indoor & Outdoor Grading
- Configuring Sundial in Code
- API Reference

The IDE page belongs immediately after the index because visual authoring is the intended path and because it prevents the manual normalized timing API from becoming the reader's first impression of the library.

## Formatting conventions to preserve

Pages use the same Just-the-Docs front matter, sticky "On this page" block and heading structure. Code examples are fenced as `js` even though the code is GML. API symbols are consistently backticked. Horizontal rules separate major conceptual steps. Current library indexes include the shared library footer; ordinary child pages do not.

The generated API pages use `library_id`, `doc_version: current`, the shared generator, a YAML presentation manifest, and source JSDoc as the factual source of signatures and descriptions. Sundial should use that same system rather than introducing a hand-maintained one-off API page.

## Guardrails used while writing Sundial

The Sundial pass therefore follows these rules:

- Start sections from the game-development problem, not from the type or method name.
- Prefer one complete, understandable example over several abstract micro-examples.
- Explain why a control exists whenever two neighbouring controls could otherwise feel redundant, especially grading versus brightness, periods versus phases, and preview masks versus runtime masks.
- Use the IDE as the beginner path and expose normalized cycle timing later.
- Keep implementation details available, but do not make the reader learn the compiled runtime bridge before they can draw a graded surface.
- Use direct recommendations when the source design clearly has an intended path.
- Avoid generic filler transitions, slogan-like summary lines, em dashes and artificial punchiness.
- End each teaching page by handing the reader to the next problem.
