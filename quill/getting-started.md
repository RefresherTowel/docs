---
layout: default
title: Getting Started
parent: Quill
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

# Getting Started

Here's where we get Quill up and running in a clean project.

## 1. Project Setup

Import Quill into GM: First click on the Tools in the menu bar, then click Import Local Package. In the "Open" popup, find the place where you downloaded the Quill file and open it. Click Add All in the window that pops up, and then click Import on the bottom left.

## 2. Create a textbox

Create Quill textboxes by running the `QuillSingle` or `QuillMulti()` functions and catching their return values in a variable. This is your textbox. You can create as many of them as you want. Don't create them inside Draw events, you should do it in a place that will run once (usually the Create event of your GUI object).

Here's a simple "form" struct with two bound fields:

```js
// obj_ui Create
form = {
	username: "",
	bio: ""
};

tb_username = QuillSingle("Username", "Type a username")
	.BindText(form, "username")
	.SetMaxLength(24)
	.SetInputMode(QUILL_TEXTMODE_IDENTIFIER)
	.SetSelectAllOnFocus(true);

tb_bio = QuillMulti("Bio", "Write something")
	.BindText(form, "bio")
	.SetWrap(true)
	.SetInputMode(QUILL_TEXTMODE_TEXT)
	.SetVisibleRows(8)
	.SetMinHeight(96);
```

You'll notice we have a `form` struct that we have created. Quill can "bind" to structs. Once bound, Quill will automatically update the contents of the struct when the user interacts with the textbox.

In the `tb_username` textbox, you can see that we bind it to the `form` struct, with the `username` variable **defined as a string**. This is important, you don't want to simply place the variable there, it **has** to be the variable name as a string. This will mean that if the user interacts with the `tb_username` textbox, the `username` variable in the `form` struct will be updated alongside it.

You can ignore bindings and manually update whatever you like via the `OnChange` or `OnSubmit` callback hooks, but bindings are a nice and clean way of automating textbox interactions.

## 3. Draw Each Frame

Draw in Draw GUI (it's the easiest place to start).

```js
// obj_ui Draw GUI
tb_username.Draw(24, 24, 340);
tb_bio.Draw(24, 88, 520, 180);

QuillDrawOverlays();
```

`QuillDrawOverlays()` draws any overlay UI that might be open, like context menus and the multiline editor overlay. If you forget this call, menus and overlays can open but you'll never see them. You can also draw each individual textboxes overlay like this: `tb_username.DrawOverlay()`, which allows you to draw different textboxes overlays over or under other items manually. Don't combine these two methods, either draw them all automatically with `QuillDrawOverlays()`, or draw each texbox's overlay manually.

## 4. Manager Step and PostDraw

Quill needs manager step/postdraw processing. The library auto-creates `obj_quill_core` during boot (and also ensures its existence when textboxes are registered).

Internally, the wiring is simple:

`obj_quill_core` runs `QUILL.__Step()` in Step, and runs `QUILL.__PostDraw()` in the Post Draw event.

You don't need to handle this at all, I'm just outlining it so you understand why there's a random `obj_quill_core` object being created when you start your game.

## 5. First Useful Callback

If your callback needs to write to something, bind a scope with `method(scope, fn)`.

```js
// obj_ui Create
on_name_scope = { edits: 0 };

tb_username.OnChange(method(on_name_scope, function(_tb, _value) {
	edits += 1;
	show_debug_message("Name changed to: " + _value);
}));
```

This binds the scope of the OnChange callback to the `on_name_scope` struct, which means that anything that runs inside the function you provide does so from the perspective of `on_name_scope`, allowing us to easily change `edits`.

## 6. Keyboard and Mouse Basics

Out of the box you get tab focus traversal (unless tab insertion is enabled on the focused box), Enter submit on single-line boxes, optional Ctrl+Enter submit on multiline, the usual Ctrl+A/C/X/V/Z/Y shortcuts, right-click context menus, and word/line selection via double and triple click.

## Common Mistakes

The most common issues are not scoping callbacks properly and forgetting to call either `QuillDrawOverlays()` or `textbox.DrawOverlay()` depending on which method you want to use (so menus/editors can open but stay invisible). Remember to use `method(scope, function)` so that you can tell your function what it needs to target, and don't forget to draw the overlays!
