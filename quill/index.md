---
layout: default
title: Quill          # children will use this as `parent:`
nav_order: 6              # order among top-level items
has_children: true        # marks this as a section (still supported)
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

![Quill icon](../assets/quill_icon.png)
{: .text-center}

*Let your players write with ease*
{: .text-center}

Quill is an advanced text input library for GameMaker. It's designed to be fast, easy to use and give you all the features a user expects when they encounter a textbox. This includes things like: caret movement, selection, clipboard, undo/redo, labels, right-click context menus, validation messaging, and proper theming, amongst many others.

Start here: [Getting Started](./getting-started.md) -> [Usage Guide](./usage.md) -> [Theming Guide](./theming.md) -> [API Reference](./api-reference.md)

## Quickstart

Create a text box, and bind it to a struct member variable (more on this later):

```js
// Create event
profile = { name: "" };

name_box = QuillSingle("Name", "Enter your name")
	.BindText(profile, "name")
```

Then draw it every frame in Draw GUI:

```js
// Draw GUI event
name_box.Draw(24, 24, 320);
QuillDrawOverlays();
```

By simply doing that, you get a fully functional text box that users can type in, select their text with either mouse or keyboard, right click to get a context menu, and do essentially everything they've come to expect from a textbox.

## Advanced features

Quill also comes with a ton of advanced features, like multi-line text boxes, tab focus jumps, a variety of filtering presets for textboxes (such as password, code, path, etc), interaction hooks (OnFocus, OnChange, etc), the ability to add or remove items from the right-click context menu per-textbox, and a lot more.

## Other Cool Stuff

If you like Quill, then be sure to check out my other libraries:

* [![Statement icon](../assets/statement_icon.png){: style="max-width: 128px;"} **Statement**](https://refreshertowel.itch.io/statement) - An easy to use state manager that comes packed with a lot of awesome features.

* [![Pulse icon](./assets/pulse_icon.png){: style="max-width: 128px;"} **Pulse**](https://refreshertowel.itch.io/pulse) - A signals & queries manager that allows you to easily uncouple dependencies and simplify your code.

* [![Echo icon](./assets/echo_icon.png){: style="max-width: 128px;"} **Echo**](https://refreshertowel.itch.io/echo) - A debug manager that comes with a very fully featured Debug UI builder (in fact, Quill comes directly from the textboxes in Echo)

* [![Catalyst icon](./assets/catalyst_icon.png){: style="max-width: 128px;"} **Catalyst**](https://refreshertowel.itch.io/catalyst) - An extremely powerful stat manager, allowing you to quickly build stats for your games (such as attack power, or jump height) that can be easily modified and altered in a variety of ways. 

* [![Whisper icon](./assets/whisper_icon.png){: style="max-width: 128px;"} **Whisper**](https://refreshertowel.itch.io/whisper) - A narrative manager that allows you to create complex, dynamic storytelling by providing simple rules that sit along your dialog/story. The roguelite "Hades" famous reactive storytelling is an example of what Whisper can help you do.