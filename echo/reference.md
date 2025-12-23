---
layout: default
title: Scripting Reference
parent: Echo
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

# Reference

This is the full public API for Echo + Echo Chamber.

Private rule: anything starting with `__` and/or marked with `/// @ignore` is considered internal and is intentionally not documented here.

## Echo

Echo is the logger: it decides what to print, what to store, and how to filter it.

### Enums
#### `eEchoDebugLevel`
- `NONE`
- `SEVERE_ONLY`
- `COMPREHENSIVE`
- `COMPLETE`

#### `eEchoDebugUrgency`
- `INFO`
- `WARNING`
- `SEVERE`

### Functions
### `EchoDebug(_message, _urgency = eEchoDebugUrgency.WARNING, _tag = "")`
Send a message to the debug logger with a specific urgency level. Returns true if the message meets current debug level critera, false if not.
**Parameters**
- `_message` `String`: The message to send to the debug logger
- `[_urgency]` `Real`: The level of urgency of the debug message (pick an entry from the eEchoDebugUrgency enum)
- `[_tag]` `String,Array<String>`: Optional tag or tags to filter on (e.g., "UI", ["Physics","Jump"]). Empty or empty array allows all.
**Returns**: `Boolean`

### `EchoDebugInfo(_message, _tag = "")`
Logs a debug message with an INFO urgency level
**Parameters**
- `_message` `String`
- `[_tag]` `String,Array<String>`

### `EchoDebugWarn(_message, _tag = "")`
Logs a debug message with a WARNING urgency level
**Parameters**
- `_message` `String`
- `[_tag]` `String,Array<String>`

### `EchoDebugSevere(_message, _tag = "")`
Logs a debug message with a SEVERE urgency level (includes stack trace)
**Parameters**
- `_message` `String`
- `[_tag]` `String,Array<String>`

### `EchoDebugSetLevel(_level)`
Sets the debug logging level, which determines what urgency criteria messages must meet in order to be logged.
**Parameters**
- `_level` `Real`: The level of logging (pick an entry from the eEchoDebugLevel enum)
**Returns**: `Boolean`

### `EchoDebugGetLevel(_stringify = false)`
Returns the current debug logging level (will be equivalent to one of the entries from the eEchoDebugLevel enum).
**Parameters**
- `_stringify` `Boolean`: Whether to return the debug level as a string, or as the plain real value.
**Returns**: `Real,String,Bool` - False if debug is disabled.

### `EchoDebugDumpLog()`
Dumps the entire debug log history to a file (file naming convention is "echo_debug_dump-[current_date]-([time_since_game_started]).txt). Returns true if dump succeeded, false if not
**Returns**: `Boolean`

### `EchoDebugGetHistorySize()`
Returns the current maximum number of entries allowed in the debug log history
**Returns**: `Real,Bool` - False if debug is disabled.

### `EchoDebugSetHistorySize(_max)`
Sets the maximum number of entries allowed in the debug log history. Setting it to 0 means there is no limit.
**Parameters**
- `_max` `Real`
**Returns**: `Boolean`

### `EchoDebugClearHistory()`
Clears all entries from the debug log history
**Returns**: `Boolean` - False if debug is disabled, otherwise true after clearing.

### `EchoDebugGetHistory()`
Returns a new array filled with the entries from debug log history
**Returns**: `Array<String>,Boolean` - False if debug is disabled.

### `EchoDebugGetRevision()`
Returns the current log revision number. This increments whenever history changes.
**Returns**: `Real,Boolean` - False if debug is disabled.

### `EchoDebugGetStructuredHistory()`
Returns a new array of structured history entries for UI rendering.
**Returns**: `Array<Struct>,Boolean` - False if debug is disabled.

### `EchoDebugSetTags(_tags)`
Sets which tags are allowed to log. An empty array means "allow all".
**Parameters**
- `_tags` `Array<String>`
**Returns**: `Boolean`

### `EchoDebugClearTags()`
Clears any tag filter so all tags are allowed.
**Returns**: `Boolean`

### `EchoDebugGetTags()`
Gets the current allowed tags array (empty means "allow all").
**Returns**: `Array<String>,Boolean`

