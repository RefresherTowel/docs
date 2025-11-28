---
layout: default
title: Echo
nav_order: 4
has_children: true
---

# Echo - Debug Logger for GameMaker

Echo is a lightweight, drop-in debug logging helper for GameMaker that centralises your debug output, adds optional stack traces, and keeps a rolling in-memory history you can dump to disk when you need it.

It's designed to sit alongside your other utility libraries (like `Statement`, `Pulse`, etc.) and stay out of the way until you need it.

Echo is part of the **RefresherTowel Games** suite of reusable frameworks for GameMaker.

---

## Quick start

1. **Import the Echo script** into your project (the file that defines the `EchoDebug*` functions and enums).
2. Make sure the macro at the top of the script is set appropriately:

   ```gml
   #macro ECHO_DEBUG_ENABLED 1
   ```

   - `1` = Echo is fully enabled (history, stack traces, dump to file).
   - `0` = Echo is effectively disabled - calls either do nothing (most functions) or just fall back to a simple `show_debug_message`.

3. Start logging:

   ```gml
   // Basic usage (default urgency = WARNING)
   EchoDebug("Player spawned");

   // Explicit urgencies
   EchoDebugInfo("Pet mood recalculated");
   EchoDebugWarn("Low ammo in magazine");
   EchoDebugSevere("Null reference in combat resolver!");

   // Adjust level at runtime
   EchoDebugSetLevel(__ECHO_eDebugLevel.COMPLETE);
   ```

---

## Configuration & enums

### Macro: `ECHO_DEBUG_ENABLED`

```gml
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

> ⚠️ **Important:** Many getters that normally return a `Real`, `String` or `Array` will instead return `false` when Echo is disabled. Always check for `false` if you're calling them in code that might run with Echo off.

---

### Enum: `__ECHO_eDebugLevel`

Controls how much Echo logs:

```gml
enum __ECHO_eDebugLevel {
    NONE,
    SEVERE_ONLY,
    COMPREHENSIVE,
    COMPLETE,
}
```

Behaviour:
```
| Level                       | Logs INFO | Logs WARNING | Logs SEVERE |
|----------------------------|:---------:|:------------:|:-----------:|
| `__ECHO_eDebugLevel.NONE`        |    ✖    |      ✖      |     ✖      |
| `__ECHO_eDebugLevel.SEVERE_ONLY` |    ✖    |      ✖      |     ✔      |
| `__ECHO_eDebugLevel.COMPREHENSIVE`|   ✖   |      ✔      |     ✔      |
| `__ECHO_eDebugLevel.COMPLETE`    |    ✔    |      ✔      |     ✔      |
```

Default level: `COMPREHENSIVE`.

---

### Enum: `__ECHO_eDebugUrgency`

Used to mark the importance of a given message:

```gml
enum __ECHO_eDebugUrgency {
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

```gml
EchoDebug(message, [urgency = __ECHO_eDebugUrgency.WARNING], [tag]);
```

Sends a message to Echo with an optional urgency.

- `message`: `String` – text to log.
- `urgency` (optional): `__ECHO_eDebugUrgency` – `INFO`, `WARNING`, or `SEVERE` (default `WARNING`).
- `tag` (optional): `String` or `Array<String>` – one or more tags (e.g., `"UI"` or `["Physics","Jump"]`). Empty/omitted means “no tag”.

- **Filters by level** according to `__ECHO_eDebugLevel` (see table above).
- **Adds to history** with a timestamp in the form:

  ```text
  [YYYY-MM-DD HH:MM:SS] (URGENCY): message + optional stack trace
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

Examples:

```gml
EchoDebug("Spawning wave", __ECHO_eDebugUrgency.INFO);
EchoDebug("Unexpected state in AI tree", __ECHO_eDebugUrgency.WARNING);
EchoDebug("Failed to load save file!", __ECHO_eDebugUrgency.SEVERE);
```

---

### Convenience helpers

#### `EchoDebugInfo(message, [tag])`

```gml
EchoDebugInfo(message, [tag]);
```

Equivalent to:

```gml
EchoDebug(message, __ECHO_eDebugUrgency.INFO, tag);
```

#### `EchoDebugWarn(message, [tag])`

```gml
EchoDebugWarn(message, [tag]);
```

Equivalent to:

```gml
EchoDebug(message, __ECHO_eDebugUrgency.WARNING, tag);
```

#### `EchoDebugSevere(message, [tag])`

```gml
EchoDebugSevere(message, [tag]);
```

Equivalent to:

```gml
EchoDebug(message, __ECHO_eDebugUrgency.SEVERE, tag);
```

When Echo is enabled, this **always** includes a stack trace in the logged message (subject to the level filter as described above).

---

### Log level controls

#### `EchoDebugSetLevel(level) -> Boolean`

```gml
EchoDebugSetLevel(__ECHO_eDebugLevel.COMPLETE);
```

Sets the global debug level.

- `level` should be one of the entries from `__ECHO_eDebugLevel`.
- Returns `true` on success.
- Returns `false` and prints a warning if:
  - `level` is not a real, or
  - `level` is outside the enum's range, or
  - `ECHO_DEBUG_ENABLED == 0`.

#### `EchoDebugGetLevel([stringify = false]) -> Real | String | Boolean`

```gml
var level      = EchoDebugGetLevel();          // -> Real enum value
var level_name = EchoDebugGetLevel(true);      // -> "COMPLETE", "COMPREHENSIVE", etc.
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

- `EchoDebugSetTags(["UI","Physics"])` – only log messages whose `tag` overlaps this list.
- `EchoDebugClearTags()` – remove the filter (log all tags).
- `EchoDebugGetTags()` – read the current tag filter (empty array means “allow all”).

If the tag filter is non-empty, `EchoDebug` (and its helpers) will only log messages whose `tag` matches at least one allowed tag. Messages that don’t match return `false` and are not recorded.

---

### History, dump

Echo keeps an in-memory history of log lines (simple strings). This can be bounded or unbounded, inspected at runtime, and dumped to disk.

#### `EchoDebugGetHistorySize() -> Real | Boolean`

```gml
var max_entries = EchoDebugGetHistorySize();
```

- When enabled: returns the **maximum number of entries** Echo will keep in history.
  - `0` means "no limit".
- When disabled: returns `false`.

#### `EchoDebugSetHistorySize(max) -> Boolean`

```gml
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

```gml
EchoDebugClearHistory();
```

Clears all entries from the in-memory history.

- Returns `true` when Echo is enabled.
- Returns `false` and does nothing when `ECHO_DEBUG_ENABLED == 0`.

#### `EchoDebugGetHistory() -> Array<String> | Boolean`

```gml
var history = EchoDebugGetHistory();
if (history != false) {
    // history is a new array; you can safely read/mutate it
}
```

- When enabled: returns a **new array** containing the current log history.
  - Mutating this array does **not** affect Echo's internal buffer.
- When disabled: returns `false`.

#### `EchoDebugDumpLog() -> Boolean`

```gml
var ok = EchoDebugDumpLog();
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

## Summary

Echo is a small, namespaced debug logger for GameMaker that gives you:

- Level-based filtering (`NONE` → `COMPLETE`).
- Per-message urgency (`INFO`, `WARNING`, `SEVERE`).
- Optional stack traces for severe logs or full debug builds.
- Rolling in-memory history with a configurable cap.
- One-shot dumping to a timestamped text file.

Use it wherever you'd normally sprinkle `show_debug_message`, and then **turn it up** when you need to chase something nasty through your game's callstack.
