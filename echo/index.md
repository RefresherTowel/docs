---
layout: default
title: Echo
nav_order: 4
has_children: true
---

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }

1. TOC
{:toc}

</details>
</div>

![Echo icon](../assets/echo_icon.png)
{: .text-center}
# Echo
{: .text-center}
*Hear what your game is telling you*
{: .text-center}

Echo is a lightweight debug logger for GameMaker. Your game is already telling you what is happening; Echo helps you actually hear it. Swap scattered `show_debug_message` calls for level based logs with tags, optional stack traces, and a history buffer you can dump to a file when something gets weird.

Echo respects the `ECHO_DEBUG_ENABLED` macro, so you can leave debug calls in your code without spamming release builds when it is off.

It's designed to sit alongside your other utility libraries (like `Statement`, `Pulse`, etc.) and stay out of the way until you need it.

Echo is part of the **RefresherTowel Games** suite of reusable frameworks for GameMaker.

> A bird's eye view of Echo is that it is a minimal, namespaced debug logger for GameMaker that gives you:
> 
> - Level-based filtering (`NONE` -> `COMPLETE`).
> - Tag-based filtering (for example, only display logs tagged "Physics")
> - Per-message urgency (`INFO`, `WARNING`, `SEVERE`).
> - Optional stack traces for severe logs or full debug builds.
> - Rolling in-memory history with a configurable cap.
> - One-shot dumping to a timestamped text file.
> 
> Use it wherever you'd normally sprinkle `show_debug_message`, and then **turn it up** when you need to chase something nasty through your game's callstack.
{: .note}

---

## Quick Start

1. **Import the Echo script** into your project (the file that defines the `EchoDebug*` functions and enums).
2. Make sure the macro at the top of the script is set appropriately:

   ```js
   #macro ECHO_DEBUG_ENABLED 1
   ```

   - `1` = Echo is fully enabled (history, stack traces, dump to file).
   - `0` = Echo is effectively disabled - calls either do nothing (most functions) or just fall back to a simple `show_debug_message`.

3. Start logging:

   ```js
   // Basic usage (default urgency = WARNING)
   EchoDebug("Player spawned");

   // Explicit urgencies
   EchoDebugInfo("Pet mood recalculated");
   EchoDebugWarn("Low ammo in magazine");
   EchoDebugSevere("Null reference in combat resolver!");

   // Optionally adjust level at runtime (default is eEchoDebugLevel.COMPREHENSIVE)
   EchoDebugSetLevel(eEchoDebugLevel.COMPLETE);
   ```

---

## Requirements

- **GameMaker version:**  
  Any version that supports:
  - Struct constructors: `function Name(args) constructor { ... }`
  - `method(owner, fn)`

- **Scripts you need:**
  - The Echo script library.

No additional extensions or assets are required.

---

## Configuration & enums

### Macro: `ECHO_DEBUG_ENABLED`

```js
#macro ECHO_DEBUG_ENABLED 1
```

Controls whether Echo is active:

- **When `ECHO_DEBUG_ENABLED == 1`**
  - All `EchoDebug*` functions behave as documented below.
  - History is recorded.
  - `EchoDebugSevere` (and any `EchoDebug` call with `SEVERE` urgency) includes a stack trace.
  - `EchoDebugDumpLog` writes a text file.

- **When `ECHO_DEBUG_ENABLED == 0`**
- `EchoDebug(...)` still calls `show_debug_message` with a simple `[URGENCY] - message` format, then returns `false`.
- All other `EchoDebug*` functions immediately return `false` and **do nothing**.
- No history or dump files are generated.
- Convenience helpers (`EchoDebugInfo/Warn/Severe`) are thin wrappers around `EchoDebug` and will also return `false` when disabled.
  - Tag filtering (see below) also returns `false` if Echo is disabled.

> Many getters that normally return a `Real`, `String` or `Array` will instead return `false` when Echo is disabled. Always check for `false` if you're calling them in code that might run with Echo off.
{: .warning}

---

### Enum: `eEchoDebugLevel`

Controls how much Echo logs:

```js
enum eEchoDebugLevel {
    NONE,
    SEVERE_ONLY,
    COMPREHENSIVE,
    COMPLETE,
}
```

Behaviour:

| Level                       | Logs INFO | Logs WARNING | Logs SEVERE |
|----------------------------|:---------:|:------------:|:-----------:|
| `eEchoDebugLevel.NONE`        |    ✖    |      ✖      |     ✖      |
| `eEchoDebugLevel.SEVERE_ONLY` |    ✖    |      ✖      |     ✔      |
| `eEchoDebugLevel.COMPREHENSIVE`|   ✖   |      ✔      |     ✔      |
| `eEchoDebugLevel.COMPLETE`    |    ✔    |      ✔      |     ✔      |

Default level: `COMPREHENSIVE`.

---

### Enum: `eEchoDebugUrgency`

Used to mark the importance of a given message:

```js
enum eEchoDebugUrgency {
    INFO,
    WARNING,
    SEVERE
}
```

- `INFO` - low-priority noise, useful when debugging a specific subsystem.
- `WARNING` - potentially problematic state, but not a crash.
- `SEVERE` - serious error; Echo will **always** attach a stack trace when enabled.

---

## Public API

### `EchoDebug(message, [urgency], [tag]) -> Boolean`

```js
EchoDebug(message, [urgency = eEchoDebugUrgency.WARNING], [tag]);
```

Sends a message to Echo with an optional urgency.

- `message`: `String` - text to log.
- `urgency` (optional): `eEchoDebugUrgency` - `INFO`, `WARNING`, or `SEVERE` (default `WARNING`).
- `tag` (optional): `String` or `Array<String>` - one or more tags (e.g., `"UI"` or `["Physics","Jump"]`). Empty/omitted means "no tag".

- **Filters by level** according to `eEchoDebugLevel` (see table above).
- **Adds to history** with a timestamp in the form:

  ```text
[YYYY-MM-DD HH:MM:SS] (URGENCY)[tag1 | tag2]:
message
(optional stack trace...)
  ```

- **Prints to the GameMaker debug console** via `show_debug_message`.
- **Includes a stack trace** if:
  - The current debug level is `COMPLETE`, **or**
  - The urgency is `SEVERE`.

**Return value:**

- `true` if the message passed the level filter and was logged.
- `false` if:
  - The message was filtered out by the current level, **or**
  - `ECHO_DEBUG_ENABLED == 0` (in this case, it still prints a basic message to the console).
  - The tag filter (if set) did not match.

> When `ECHO_DEBUG_ENABLED == 0`, `EchoDebug` still prints a simple `[URGENCY] - message` line via `show_debug_message` before returning false.
{: .note}


Examples:

```js
EchoDebug("Spawning wave", eEchoDebugUrgency.INFO);
EchoDebug("Unexpected state in AI tree", eEchoDebugUrgency.WARNING);
EchoDebug("Failed to load save file!", eEchoDebugUrgency.SEVERE);
```

---

### Convenience helpers

#### `EchoDebugInfo(message, [tag])`

```js
EchoDebugInfo(message, [tag]);
```

Equivalent to:

```js
EchoDebug(message, eEchoDebugUrgency.INFO, tag);
```

#### `EchoDebugWarn(message, [tag])`

```js
EchoDebugWarn(message, [tag]);
```

Equivalent to:

```js
EchoDebug(message, eEchoDebugUrgency.WARNING, tag);
```

#### `EchoDebugSevere(message, [tag])`

```js
EchoDebugSevere(message, [tag]);
```

Equivalent to:

```js
EchoDebug(message, eEchoDebugUrgency.SEVERE, tag);
```

When Echo is enabled, this **always** includes a stack trace in the logged message (subject to the level filter as described above).

---

### Log level controls

#### `EchoDebugSetLevel(level) -> Boolean`

```js
EchoDebugSetLevel(eEchoDebugLevel.COMPLETE);
```

Sets the global debug level.

- `level` should be one of the entries from `eEchoDebugLevel`.
- Returns `true` on success.
- Returns `false` and prints a warning if:
  - `level` is not a real, or
  - `level` is outside the enum's range, or
  - `ECHO_DEBUG_ENABLED == 0`.

#### `EchoDebugGetLevel([stringify = false]) -> Real | String | Boolean`

```js
var _level      = EchoDebugGetLevel();          // -> Real enum value
var _level_name = EchoDebugGetLevel(true);      // -> "COMPLETE", "COMPREHENSIVE", etc.
```

- When Echo is enabled:
  - Returns the numeric level (`Real`) when `stringify == false`.
  - Returns the level name (`String`) when `stringify == true` (e.g. `"SEVERE ONLY"`).
- When `ECHO_DEBUG_ENABLED == 0`:
  - Returns `false`.

---

### Tag controls

Echo allows you to restrict debug messages to only those that have a specific tag, allowing you to filter what messages get through on the fly.

#### Applying tags:

Simply provide either a string, or an array of strings to the `EchoDebug()` or it's helper functions to the tag argument:
- `EchoDebugWarn("Physics is wonky","Physics"); // Tagged with "Physics"`
- `EchoDebugInfo("I only show if either 'Jump' or 'Attack' tags are allowed through",["Jump","Attack"]); // Tagged with both "Jump" and "Attack"`

#### Filtering via tags

You can manipulate which tags are allowed through the debugger at any point in time via these helper functions:

- `EchoDebugSetTags(["UI","Physics"])` - only log messages whose `tag` overlaps this list.
- `EchoDebugClearTags()` - remove the filter (log all tags).
- `EchoDebugGetTags()` - read the current tag filter (empty array means "allow all").

If the tag filter is non-empty, `EchoDebug` (and its helpers) will only log messages whose `tag` matches at least one allowed tag. Messages that don't match return `false` and are not recorded.

---

### History, dump

Echo keeps an in-memory history of log lines (simple strings). This can be bounded or unbounded, inspected at runtime, and dumped to disk.

#### `EchoDebugGetHistorySize() -> Real | Boolean`

```js
var _max_entries = EchoDebugGetHistorySize();
```

- When enabled: returns the **maximum number of entries** Echo will keep in history.
  - `0` means "no limit".
- When disabled: returns `false`.

#### `EchoDebugSetHistorySize(max) -> Boolean`

```js
EchoDebugSetHistorySize(200);   // Keep up to 200 most recent entries
EchoDebugSetHistorySize(0);     // Unlimited history
```

- `max` must be a real number ≥ 0.
- The value is floored to an integer.
- When `max > 0`, Echo will trim the oldest entries while `history_length > max`.
- Returns `true` on success, `false` (and prints a warning) if:
  - `max` is not a real, or
  - `max < 0`, or
  - Echo is disabled.

#### `EchoDebugClearHistory() -> Boolean`

```js
EchoDebugClearHistory();
```

Clears all entries from the in-memory history.

- Returns `true` when Echo is enabled.
- Returns `false` and does nothing when `ECHO_DEBUG_ENABLED == 0`.

#### `EchoDebugGetHistory() -> Array<String> | Boolean`

```js
var _history = EchoDebugGetHistory();
if (_history != false) {
    // _history is a new array; you can safely read/mutate it
}
```

- When enabled: returns a **new array** containing the current log history.
  - Mutating this array does **not** affect Echo's internal buffer.
- When disabled: returns `false`.

#### `EchoDebugDumpLog() -> Boolean`

```js
var _ok = EchoDebugDumpLog();
```

Writes the current history to a text file in the project's working directory.

- Filename format:

  ```text
  echo_debug_dump-YYYY-MM-DD_HH-MM-SS-(TICKS).txt
  ```

  Where:
  - The date/time is based on `date_current_datetime()`.
  - `TICKS` is `get_timer()` (microseconds since game start).

- Returns:
  - `true` on success.
  - `false` if:
    - Echo is disabled, or
    - The file could not be created (and an error is printed via `show_debug_message`).

---

## Help & Support

#### **Bug reports / feature requests:**  
  The best place to report bugs and request features is the GitHub Issues page:

  [**Echo issues**](https://github.com/RefresherTowel/Echo/issues)

  Please include:

  - A short code snippet.
  - Which functions you called (`EchoDebugSetTags`, `EchoDebug`, etc).
  - Any relevant debug output from `EchoDebugInfo/EchoDebugWarn/EchoDebugSevere`.

  If you are not comfortable using GitHub, you can also post in the [**Echo channel on the RefresherTowel Games Discord**](https://discord.gg/w5NWDBwNta) and I can file an issue for you.

#### **Questions / discussion / examples:**  
  Join the project's Discord:
  
  [**RefresherTowel Games - Echo Channel**](https://discord.gg/w5NWDBwNta)

  That's where you can:
  - Ask implementation questions.
  - Share snippets and patterns.
  - See example integrations from other users.