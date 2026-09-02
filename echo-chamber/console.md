---
layout: default
title: Echo Console
parent: Echo Chamber
nav_order: 2
redirect_from:
  - /echo/echo_chamber/console.html
  - /echo/echo_chamber/console/
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

# Echo Console

Echo Console is the debugger that already ships with Echo Chamber. You can open it over a running game and start inspecting what is happening without building a custom debug window first.

The Console starts with Echo's log history, but it also gives you a way to point the debugger at a live instance, keep values visible while they change, run repeatable debug actions, collect a text snapshot of the game's current state, capture useful crash information, and use GameMaker's input recording, all from the same interface.

You don't need to learn all of those systems at once, and there's likely only a portion that will be immediately useful in any one project, but it's all there available to you if you wish.

Open the Console, get comfortable searching logs, then come back to the later sections when the need arises (or just click through it and explore, like I usually do when learning stuff like this).

---

## Opening the console

With the normal bundled setup, press F1.

You can also open it from code:

```js
EchoChamberOpenConsole(GetEchoChamberRoot());
```

`GetEchoChamberRoot()` gets the shared debug desktop and `EchoChamberOpenConsole()` opens Echo Console on that desktop.

Most examples on this page keep that root in an instance variable because several different events or callbacks may need it later:

```js
/// obj_debug_controller Create
ui_root = GetEchoChamberRoot();
```

Put that kind of setup somewhere that runs once, such as a debug controller's Create event. The bundled Echo Chamber controller is already running the shared root every frame, so don't also call `RunDesktop()` on it yourself.

If you deliberately create a completely separate root, the situation changes: *you* own that root, so you also have to run it. This example creates a separate root with a theme, opens the Console on it, then runs that same root from Draw GUI End:

```js
/// obj_debug_controller Create
ui_root = new EchoChamberRoot(new EchoChamberThemeMidnightNeon()); // Create your custom root
EchoChamberOpenConsole(ui_root); // Supply the root you want the console to run on

/// obj_debug_controller Draw GUI End
ui_root.RunDesktop(); // Draw your custom root
```

`new EchoChamberRoot(...)` creates another debug desktop rather than using the bundled shared one. `EchoChamberThemeMidnightNeon()` supplies the visual theme for that new desktop. `EchoChamberOpenConsole(ui_root)` adds the Console to it, and `ui_root.RunDesktop()` is what actually processes and draws that desktop each frame.

The Console belongs to a particular `EchoChamberRoot`, and that root has to be running. Use the bundled shared root and controller for the ordinary setup. Create and run your own root only when you intentionally want a separate desktop.

---

## Launch macros

The first few macros in `scr_echo_chamber_macros.gml` control the automatic Console setup that Echo Chamber provides for you:

- `ECHO_CHAMBER_CONSOLE_ENABLED` decides whether that automatic Console/controller setup is enabled at all.
- `ECHO_CHAMBER_CONSOLE_KEY` chooses the key the bundled controller watches for opening and closing the Console. The default is F1.
- `ECHO_CHAMBER_LAUNCH_ON_STARTUP` decides whether the Console should already be open when the bundled controller starts.
- `ECHO_CHAMBER_DEBUG_THEME` chooses the look used by Echo Console and the other built-in debug windows. Its choices are `eEchoChamberDebugTheme.PHOSPHOR_TERMINAL`, `BIOHAZARD_CONSOLE`, and `EMERALD_ULTRAVIOLET`. The source default is `EMERALD_ULTRAVIOLET`.

These macros only control the automatic bundled setup. Disabling it doesn't make the Console API unusable, and you can still create or obtain a root and open the Console yourself.

The built-in debugger windows use their own window-level theme. Changing the normal root theme therefore changes your ordinary custom windows without recolouring the Console. Use `ECHO_CHAMBER_DEBUG_THEME` when you specifically want the built-in debugger's look to change.

---

## The main console window

When the Console opens, think of it as four jobs collected into one window.

At the top, the debugger area tells you what the Console is currently inspecting and gives you access to the Inspector, Watches, other built-in tools, and any debugger launchers registered by installed libraries.

Below that, the query row filters the debug log entries you're looking at. It can also keep the list following new entries and open the settings that decide what Echo records in the first place.

The large list is the captured debug log. Clicking an entry selects it and shows its details. Right-clicking an entry gives you actions around that particular message, such as copying it or making a filter from it.

The command bar is for typed debug actions. It can run Echo Console's built-in commands and any commands your project registers. While that text variable has focus, Up and Down move through earlier command lines.

When a log row is selected, the details area can show its time, urgency, tags, message, and stack trace separately. Echo keeps those pieces separately in its structured history rather than flattening everything into one string, which is why the Console can search or display one variable without parsing a formatted line back apart.

---

## Search the logs you already have

The query variable answers: **which of the messages I already have do I want to see right now?** It doesn't actually effect anything about what logs get captured, it's simply a filter to allow you to target specific classes of log entries.

Plain text searches the whole entry. Add a variable name when you want to search one particular part:

```text
tag:ui
-tag:network
msg:"layout failed"
stack:PlayerStep
level:severe
level>=warning
since:5s
```

Hopefully those are at least somewhat intuitive:

- `tag:ui` means "show entries tagged UI".
- `-tag:network` means "hide entries tagged Network".
- `msg:"layout failed"` means "look for that phrase in the message text".
- `stack:PlayerStep` means "look for that text in the stack trace".
- `level:severe` means "only severe entries".
- `level>=warning` means "warnings or anything more serious".
- `since:5s` means "only entries from the last five seconds".

If you write several positive `tag:` terms, an entry must contain all of them. A value containing spaces should be quoted:

```text
msg:"failed to build layout"
tag:"Player Movement"
```

Durations for `since:` can use `ms`, `s`, `m`, or `h`. Anything that isn't recognised as one of the variable forms is treated as an ordinary case-insensitive search term.

The Console checks the query while you type. If the syntax is invalid, the query input shows the problem instead of silently changing what you're looking at. **Clear** removes the current query and shows the captured history again.

The query runs *after* capture. If a message was never kept anywhere, a query can't recover it. Capture Settings controls what actually gets captured.

---

## Decide what Echo should keep

**Capture Settings** answers a different question from the query variable: **what should Echo keep or output as the game runs?**

The settings are:

- **Capture Level** - which urgencies can enter Echo's normal filtered history and GameMaker debug output.
- **History Limit** - how many entries Echo may keep in each history. `0` means no limit.
- **Raw Capture** - whether Echo also remembers messages *before* the level and tag filters decide whether they belong in the normal log.
- **Capture Tags** - an optional comma-separated list of tags allowed into the normal filtered history. Empty means no tag filter.
- **Clear Logs** - removes the current filtered and raw histories.
- **Save Log** - writes the history source currently being inspected to a timestamped text file.

Suppose the logger is currently set to show only warnings and severe messages because ordinary information was too noisy. A bug happens. *Afterward* you realise an info message from three seconds earlier would tell you what the player was doing before the warning.

If Raw Capture was off, that info message was filtered away and the Console can't search for it now. If Raw Capture was on, Echo kept a second copy before the normal level/tag filters, so the Console can still search backward through that earlier information.

Raw history can keep messages even while Capture Level is **Off** (`eEchoDebugLevel.NONE`). `NONE` stops messages entering the normal filtered history and output, but it doesn't override the separate Raw Capture setting.

When Raw Capture is off, the Console works from the normal filtered history instead. Switching which history the Console is browsing clears the selected row because the two histories are separate lists.

Raw Capture is obviously quite useful, but if you're constantly spamming debug messages, it can grow pretty large pretty quickly, so just be aware of that fact when using it.

You can change the same logger settings from code:

```js
EchoDebugSetLevel(eEchoDebugLevel.COMPREHENSIVE);
EchoDebugSetHistorySize(1000);
EchoDebugSetRawHistoryCapture(true);
EchoDebugSetTags(["UI", "Combat"]);
```

`EchoDebugSetLevel()` changes the normal urgency filter, `EchoDebugSetHistorySize(1000)` caps the kept history at 1,000 entries, `EchoDebugSetRawHistoryCapture(true)` preserves pre-filter messages for tools that use raw history, and `EchoDebugSetTags(["UI", "Combat"])` limits the normal filtered log to messages sharing at least one of those tags.

Use the query variable when you want to **look at less of what has already been captured**. Use Capture Settings when you want Echo to **capture or output less from this point onward**.

---

## Built-in debug windows

The Console's **Tools** menu opens focused windows for common debugging jobs:

- **Command Help** shows the commands the command bar understands and how to call them.
- **Inspector** shows the current debug target and lets you inspect or edit its variables where the targeted instance supports it (i.e. you can't edit readonly variables, obviously).
- **Watches** keeps chosen instance variables, global variables, or calculated values visible as the game runs.
- **Game Options** exposes game/runtime settings.
- **Runtime Monitor** shows live engine and runtime information.
- **Data Structure Scanner** lets you inspect supported GameMaker DS structures (mostly useful for trying to track down ds-related memory leaks).
- **Input Debugger** controls GameMaker debug input recording and playback.
- **Crash Reports** shows the most recently captured unhandled exception report.
- **Snapshot** builds a text report of useful current debug state that you can copy or save.

Your own code can open one of these windows with its window-id macro:

```js
EchoConsoleOpenWindow(ui_root, ECHO_DEBUG_WINDOW_WATCHES);
```

Here `ECHO_DEBUG_WINDOW_WATCHES` names the built-in Watches window. `EchoConsoleOpenWindow()` asks the debug system attached to `ui_root` to open that registered tool and returns the window if it can be opened.

---

## Picking an target to inspect

An Inspector is much more useful when it knows *which thing in the running game* you mean. Echo Console keeps one current value as the **debug target** so several other Console tools can all reference it.

A target can represent several kinds of debug value, but the most common workflow is a live GameMaker instance. In the Console, **Select Instance** starts a picking mode and lets you click the instance in the game.

If your game already has the instance reference, you can set it directly. This example looks for the first `obj_player` instance and only sets the target if that instance actually exists:

```js
var _player = instance_find(obj_player, 0);
if (instance_exists(_player)) {
	EchoConsoleSetInstanceTarget(ui_root, _player);
}
```

(`obj_player` is an example project object, not an object supplied by Echo Chamber. Replace it with whatever object or instance reference your game uses.)

`EchoConsoleSetInstanceTarget(ui_root, _player)` makes that exact live instance the current target for the debug manager on `ui_root`. The Inspector and target-aware commands can now work from the same selected instance.

When you no longer want a target, clear it:

```js
EchoConsoleClearTarget(ui_root);
```

To start the same click-an-instance workflow from your own debug UI:

```js
EchoConsoleStartInstancePick(ui_root);
```

While picking, a left click can choose an instance and right click or the Cancel action can leave picking mode. Your own code can cancel it explicitly too:

```js
EchoConsoleCancelPick(ui_root);
```

A selected instance can later be destroyed by the game. At that point it's no longer a valid live instance target and the inspector won't continue trying to track it.

---

## Keep important values visible with watches

The Inspector is good when you want to explore an instance. It's annoying when you're chasing one variable and repeatedly reopening the Inspector just to watch the same number change.

A **watch** means "keep this particular value up to date in the Watches window".

You can create watches from the Console UI or from code. There are three common sources for a watched value.

First, watch a variable on one particular live instance:

```js
player_hp_watch_id = -1;

var _player = instance_find(obj_player, 0);
if (instance_exists(_player)) {
	player_hp_watch_id = EchoConsoleAddInstanceWatch(ui_root, _player, "hp");
}
```

It works the same way as binding, we need to refer to the variable by its name as a string. This example keeps `player_hp_watch_id` as an instance variable because it wants to remove this same watch later. `EchoConsoleAddInstanceWatch()` receives the root, the instance reference, and the variable name `"hp"`. If the watch is successfully added, it returns its numeric watch id. `-1` means it couldn't be added.

Again, `obj_player` and `"hp"` are examples for what might exist in your project, not things that are inherent to Echo Console.

Second, watch a global variable by name:

```js
var _global_watch_id = EchoConsoleAddGlobalWatch(ui_root, "current_room_name");
```

This tells the Watches system to read the global variable called `current_room_name` when it needs the current value.

Third, provide a small function when the value isn't stored in one variable at all (perhaps you want some calculation done first), or it's a built-in global variable (such as `fps_real` below):

```js
var _fps_watch_id = EchoConsoleAddCallbackWatch(ui_root, "FPS", function() {
	return fps_real;
});
```

`EchoConsoleAddCallbackWatch()` stores the label `"FPS"` alongside a getter function. Whenever the watch is evaluated, the function returns the current `fps_real` value.

Callback watches are useful for calculated values, but again, try to keep their getter functions cheap. The Watches window and Snapshot system can call them more than once per step.

Remove one particular watch by the id returned when it was created:

```js
if (player_hp_watch_id != -1) {
	EchoConsoleRemoveWatch(ui_root, player_hp_watch_id);
	player_hp_watch_id = -1;
}
```

The check avoids trying to remove a watch that was never added. After successful removal, the example resets its stored id to `-1` so the controller also knows it no longer owns a live watch.

Or remove every watch at once:

```js
EchoConsoleClearWatches(ui_root);
```

The three watch kinds all solve the same practical problem: keep something important visible without repeatedly navigating back to it.

---

## Run debug actions as commands

Buttons are useful for actions you want permanently visible. The command bar is useful when you want a lot of debug actions without filling the screen with buttons, or when an action naturally takes typed arguments.

Built-in commands include:

- `help [command]`
- `clear`
- `dump`
- `target`
- `select`
- `inspect`
- `watches`
- `game`
- `runtime`
- `input`
- `snapshot [copy|save]`
- `crash [open|copy|clear|enable|disable]`
- `open <help|inspector|watches|game|runtime|ds|input|crash|snapshot>`
- `watch target <variable>`
- `watch global <variable>`
- `clear watches`
- `get target <variable>`
- `get global <variable>`
- `set target <variable> <value>`
- `speed <fps>`
- `texfilter <on|off>`
- `fullscreen <on|off>`
- `gm <overlay|log>`

Your code can send text through the same command parser the Console bar uses:

```js
EchoConsoleRunCommand(ui_root, "snapshot copy");
```

That line is equivalent to entering `snapshot copy` in the command bar. The parser finds the `snapshot` command, reads `copy` as its argument, and runs the registered action.

---

## Add your own commands

Project-specific commands become useful when you keep performing the same debug action but the exact value changes each time. Instead of making ten Nudge buttons, for example, one `nudge_x` command can accept the distance you type.

This command moves whichever live instance is currently selected as the debug target:

```js
EchoConsoleAddCommand(
	ui_root,
	"nudge_x",
	"Move the active target horizontally.",
	[
		new EchoConsoleCommandArg("distance", eEchoConsoleCommandArgType.REAL, false, "Horizontal distance", 16)
	],
	function(_args, _context) {
		var _target = _context.debug_manager.GetTargetValue();
		if (instance_exists(_target)) {
			_target.x += _args.distance;
			return "Moved target by " + string(_args.distance);
		}
		return "No valid instance target.";
	}
);
```

There are five arguments to `EchoConsoleAddCommand()` here.

`ui_root` says which Echo Console/debug manager should receive the command.

`"nudge_x"` is the text the user types to invoke it. The next string, `"Move the active target horizontally."`, is the help description shown for the command.

The array contains the command's argument definitions. This example has one argument named `"distance"`. `eEchoConsoleCommandArgType.REAL` tells the parser to turn that token into a real number. `false` means the argument isn't required. `"Horizontal distance"` is its help text, and `16` is the default value used when the user leaves the optional argument out.

Both command lines are valid: `nudge_x` uses 16, while `nudge_x -32` uses -32.

The final argument is the function you provide that performs the command. Echo Chamber calls it with `_args` and `_context` after the command line has been parsed successfully.

`_args.distance` is already the parsed number because the argument definition named that variable `distance`. `_context.debug_manager.GetTargetValue()` asks the shared debug manager for the current target's underlying value. A debug target can hold more than just instances, so the callback checks `instance_exists(_target)` before using the instance-specific `x` variable.

When the target is a live instance, the function moves it and returns a string for the command output. Otherwise it returns the `"No valid instance target."` message.

If one argument should be free-form text containing spaces, use `eEchoConsoleCommandArgType.TEXT` for that final argument so it consumes the rest of the command line.

Remove a project command when you no longer want the Console to recognise it:

```js
EchoConsoleUnregisterCommand(ui_root, "nudge_x");
```

Built-in commands can't be unregistered this way. The unregister helper is only for commands manually added to the manager.

---

## Capture a snapshot when the bug is happening

Sometimes the hard part of a bug report isn't reproducing the problem. It's remembering all the useful state that was present in the five seconds when the problem was actually on screen.

An **Echo Snapshot** collects that debugging information into plain text at one moment. The report includes current runtime information, the current debug target, an instance dump when the target is an instance, watches, the Console's active filters, and recent filtered Echo logs. The Snapshot window lets you choose how many recent logs and object-population entries are included.

As with everything else, you can also capture the current report and keep the returned text yourself via code:

```js
var _text = EchoConsoleCaptureSnapshot(ui_root);
```

`EchoConsoleCaptureSnapshot()` builds the snapshot immediately and returns its text when successful.

If you simply want that fresh report on the clipboard:

```js
EchoConsoleCopySnapshot(ui_root);
```

`EchoConsoleCopySnapshot()` captures a new snapshot first, then copies it.

To capture a fresh report and save it to a text file:

```js
EchoConsoleSaveSnapshot(ui_root);
```

The Snapshot window can also keep captured snapshots during its current session. Clear those saved entries with:

```js
EchoConsoleClearSavedSnapshots(ui_root);
```

Snapshots are useful when the bug depends on several pieces of state at once and one self-contained text artifact is easier to inspect or share than a collection of screenshots and/or trying to remember a bunch of different values.

---

## Capture the last unhandled crash

Echo Crash Reports can install an unhandled-exception handler. If the game reaches an unhandled exception, Echo records a report containing useful debug information before the crash finishes.

This doesn't make the exception safe or prevent the game from crashing. The feature is about preserving evidence from the failure.

You can also enable crash capture through code:

```js
EchoConsoleEnableCrashCapture(ui_root, true);
```

The `true` argument asks Echo to call the unhandled-exception handler that was installed before Echo's handler after Echo has captured its report. Leave that chaining enabled when another system also needs to see the same unhandled exception.

Disable Echo's crash capture again:

```js
EchoConsoleDisableCrashCapture(ui_root);
```

When a report exists, you can copy it and clear the stored report:

```js
if (EchoConsoleHasCrashReport(ui_root)) {
	EchoConsoleCopyCrashReport(ui_root);
	EchoConsoleClearCrashReport(ui_root);
}
```

`EchoConsoleHasCrashReport()` lets the code avoid copy/clear work when nothing has been captured. `EchoConsoleCopyCrashReport()` copies the stored text, and `EchoConsoleClearCrashReport()` removes that stored report afterward.

---

## Record and replay input

GameMaker has a debug input-recording system that can save a sequence of input and play the same sequence back later. Echo Console wraps that feature so you can use it from the same debugging environment as the rest of your tools.

Input recording helps when a bug depends on a fiddly sequence that's hard to reproduce by hand exactly the same way each time.

If you want to activate it through code instead of the Console, start recording with one of GameMaker's `debug_input_filter_*` masks:

```js
EchoConsoleStartInputRecording(ui_root, debug_input_filter_all);
```

The example uses `debug_input_filter_all`, so the GameMaker recorder is asked to include all of the supported debug input categories selected by that mask.

Stop recording and save the result to a file:

```js
EchoConsoleStopInputRecording(ui_root, "echo_input_recording.json");
```

Play that saved recording later:

```js
EchoConsolePlayInputRecording(ui_root, "echo_input_recording.json");
```

Part of GameMaker's recording/playback workflow reports back through the Async System event. In the normal Echo Chamber setup, the bundled controller already forwards that event to the debug manager. You don't add another forwarding call in that setup.

If you deliberately opted out of the bundled controller and are running the root yourself, your own Async System event must forward `async_load`:

```js
/// Async - System
EchoConsoleHandleAsyncSystem(ui_root, async_load);
```

`EchoConsoleHandleAsyncSystem(ui_root, async_load)` gives the debug manager the GameMaker Async System event data it needs for input recording/playback state.

> If a manual setup appears to start recording or playback but never receives the expected completion/update state, missing this event forwarding is the first thing to check.
{: .note}

---

## Inspect GameMaker data structures

The Data Structure Scanner is for looking inside supported GameMaker DS structures while the game is running. It can inspect DS lists, maps, grids, queues, stacks, and priority queues.

Open it from code with:

```js
EchoConsoleOpenDataStructureScanner(ui_root);
```

The supported kinds are also listed in `eEchoConsoleDsKind` in the Scripting Reference.

Walking and displaying a huge DS can itself become expensive, so the scanner obeys limits from `scr_echo_chamber_macros.gml`. Those limits keep an accidental inspection from trying to walk or draw an unreasonable amount of data in one frame.

---

## Let another library add its debugger

Echo Console's **Libraries** menu is for optional development tools supplied by other libraries. A library can register its own launcher so the user can open that specialist debugger from the same Console hub via the `Libraries` button.

For instance, Statement Lens uses the pattern shown here to allow itself to be launched:

```js
EchoConsoleLibraryRegistration("Statement Lens", StatementLensOpen, STATEMENT_DEBUG);
```

This is an actual integration example, so `StatementLensOpen` and `STATEMENT_DEBUG` come from Statement/Statement Lens rather than Echo Chamber itself.

`"Statement Lens"` is the text shown in Echo Console's Libraries menu. `StatementLensOpen` is the function Echo Console calls when the user chooses that entry, with the Console's current root passed as `_ui_root`. This is a function you would need to write yourself that launches whatever debug interface the library you are adding has. `STATEMENT_DEBUG` decides whether that library's debugger should be available (for when you turn off a library via a macro or something).

This registration belongs in `scr_echo_chamber_library_registration`, before Echo Console builds its hub. The hub reads the available library registrations when it's created. Adding one afterward doesn't rewrite an already-created Console controller, so the new entry appears the next time a Console controller is created.

Use library registration for development-tool integrations, not for normal in-game menus for players.

---

That's about it for the Echo Console. There's a lot to explore in it so take your time and test things out. It's still fairly new, so there may be some obscure bugs hanging around, please file reports on any bugs you encounter using the information provided on the [Echo homepage](../echo/).