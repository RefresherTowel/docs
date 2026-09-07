---
layout: "default"
title: "API Reference"
parent: "Statement 2"
nav_order: 12
library_id: "statement"
doc_version: "current"
api_reference: true
---

<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. -->
<!-- Source: GML JSDoc + statement.yml -->

<div class="sticky-toc" markdown="block">
<details open markdown="block">
  <summary>On this page</summary>

1. TOC
{:toc}

</details>
</div>

# API Reference

Complete reference for Statement's machines, states, transitions, templates, timing, debug tooling, and Statement Lens API. For explanations and worked examples, start with the teaching pages; this page is for looking up exact constructors, methods, enums, settings, and top-level helpers.

---

## Machines and states

### Statement
{: #statement .api-type-title }

Creates a <a href="#statement"><code>Statement</code></a> state machine bound to an instance or struct owner.

```gml
new Statement(id)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">Id.Instance,Struct</span>
      <span class="api-argument-description">The instance or struct whose scope is used for state handlers and callbacks.</span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Setup and lifecycle</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-set-initial-state"><code>SetInitialState()</code></a></td><td>Sets which registered state should be entered when this machine starts.</td></tr>
<tr><td><a href="#statement-set-reset-mode"><code>SetResetMode()</code></a></td><td>Sets how this machine behaves when its host state exits.</td></tr>
<tr><td><a href="#statement-set-inherit-pause"><code>SetInheritPause()</code></a></td><td>Sets whether this machine is paused when its parent machine is paused.</td></tr>
<tr><td><a href="#statement-is-running"><code>IsRunning()</code></a></td><td>Checks whether this machine currently has an active state.</td></tr>
<tr><td><a href="#statement-start"><code>Start()</code></a></td><td>Explicitly starts this machine by entering its configured initial state.</td></tr>
<tr><td><a href="#statement-stop"><code>Stop()</code></a></td><td>Stops the machine, exiting child machines first while keeping its states and settings.</td></tr>
<tr><td><a href="#statement-reset"><code>Reset()</code></a></td><td>Stops this machine and starts it again from its configured initial state.</td></tr>
<tr><td><a href="#statement-clear-states"><code>ClearStates()</code></a></td><td>Stops the machine and removes all states and machine-wide transition rules without resetting its settings.</td></tr>
<tr><td><a href="#statement-destroy"><code>Destroy()</code></a></td><td>Destroys the machine, its child machines, states, hooks, and debug registration.</td></tr>
</tbody></table>

<div class="api-method-group-title">States and hierarchy</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-add-state"><code>AddState()</code></a></td><td>Registers a state definition without running gameplay code. The first state added becomes the default initial state.</td></tr>
<tr><td><a href="#statement-add-state-template"><code>AddStateTemplate()</code></a></td><td>Builds a state from a template and registers it without starting the machine.</td></tr>
<tr><td><a href="#statement-get-state"><code>GetState()</code></a></td><td>Returns a registered state by name/tag value, or returns the active state when no name is supplied.</td></tr>
<tr><td><a href="#statement-remove-state"><code>RemoveState()</code></a></td><td>Removes a registered state. Removing the active state stops the machine first.</td></tr>
<tr><td><a href="#statement-get-state-name"><code>GetStateName()</code></a></td><td>Returns the active state&#x27;s name/tag value.</td></tr>
<tr><td><a href="#statement-is-in-state"><code>IsInState()</code></a></td><td>Returns whether the supplied state name or <a href="#statement-state"><code>StatementState</code></a> is the active state of this machine.</td></tr>
<tr><td><a href="#statement-is-in-path"><code>IsInPath()</code></a></td><td>Returns whether this machine&#x27;s active hierarchy matches a supplied nested state path.</td></tr>
<tr><td><a href="#statement-ensure-state"><code>EnsureState()</code></a></td><td>Requests the supplied state and naturally reports SAME_STATE when it is already active.</td></tr>
<tr><td><a href="#statement-get-child-machine"><code>GetChildMachine()</code></a></td><td>Returns the submachine hosted by the active state, if any.</td></tr>
<tr><td><a href="#statement-get-child-state"><code>GetChildState()</code></a></td><td>Returns the active state of the current state&#x27;s hosted submachine, if any.</td></tr>
</tbody></table>

<div class="api-method-group-title">Direct transitions</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-change-state"><code>ChangeState()</code></a></td><td>Requests a normal transition to a registered state.</td></tr>
<tr><td><a href="#statement-reenter-state"><code>ReenterState()</code></a></td><td>Runs the active state&#x27;s Exit and Enter handlers again without changing to another state first.</td></tr>
<tr><td><a href="#statement-previous-state"><code>PreviousState()</code></a></td><td>Attempts to return to the most recent previous state retained in runtime history.</td></tr>
</tbody></table>

<div class="api-method-group-title">Queued transitions</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-set-queue-phase"><code>SetQueuePhase()</code></a></td><td>Sets when queued transitions are processed automatically, or disables automatic processing with MANUAL.</td></tr>
<tr><td><a href="#statement-get-queue-phase"><code>GetQueuePhase()</code></a></td><td>Returns when queued transitions are processed automatically.</td></tr>
<tr><td><a href="#statement-queue-state"><code>QueueState()</code></a></td><td>Stores one buffered transition request to be processed according to this machine&#x27;s queue phase.</td></tr>
<tr><td><a href="#statement-process-queued-state"><code>ProcessQueuedState()</code></a></td><td>Immediately attempts the currently buffered transition. Exit-lock and exit-guard failures keep the request pending.</td></tr>
<tr><td><a href="#statement-has-queued-state"><code>HasQueuedState()</code></a></td><td>Returns whether a buffered transition is currently pending.</td></tr>
<tr><td><a href="#statement-get-queued-state-name"><code>GetQueuedStateName()</code></a></td><td>Returns the queued target state name when a request is pending.</td></tr>
<tr><td><a href="#statement-get-queued-state-data"><code>GetQueuedStateData()</code></a></td><td>Returns the payload associated with the queued transition when one is pending.</td></tr>
<tr><td><a href="#statement-clear-queued-state"><code>ClearQueuedState()</code></a></td><td>Clears the buffered transition request without processing it.</td></tr>
</tbody></table>

<div class="api-method-group-title">Stack and history</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-set-history-limit"><code>SetHistoryLimit()</code></a></td><td>Sets how many previous states are kept in history. Values at or below zero mean no limit.</td></tr>
<tr><td><a href="#statement-get-history-count"><code>GetHistoryCount()</code></a></td><td>Returns how many states are currently stored in history.</td></tr>
<tr><td><a href="#statement-get-history-at"><code>GetHistoryAt()</code></a></td><td>Returns a state retained at the supplied history index.</td></tr>
<tr><td><a href="#statement-clear-history"><code>ClearHistory()</code></a></td><td>Clears state history without changing the active state.</td></tr>
<tr><td><a href="#statement-was-previously-in-state"><code>WasPreviouslyInState()</code></a></td><td>Returns whether the state at the requested history depth matches a supplied state name.</td></tr>
<tr><td><a href="#statement-push-state"><code>PushState()</code></a></td><td>Transitions to another state and records the previous state on the stack only when the transition succeeds.</td></tr>
<tr><td><a href="#statement-pop-state"><code>PopState()</code></a></td><td>Attempts to return to the most recently pushed state and removes the stack entry only after success.</td></tr>
<tr><td><a href="#statement-get-state-stack-depth"><code>GetStateStackDepth()</code></a></td><td>Returns the number of saved states on the push/pop stack.</td></tr>
<tr><td><a href="#statement-peek-state-stack"><code>PeekStateStack()</code></a></td><td>Returns the most recently pushed state without mutating the stack.</td></tr>
<tr><td><a href="#statement-clear-state-stack"><code>ClearStateStack()</code></a></td><td>Clears the push/pop stack without changing the active state.</td></tr>
<tr><td><a href="#statement-get-previous-state-name"><code>GetPreviousStateName()</code></a></td><td>Returns the name of the most recent previous state in the history, if any.</td></tr>
<tr><td><a href="#statement-get-last-transition-data"><code>GetLastTransitionData()</code></a></td><td>Returns the payload associated with the last successful state transition, if any.</td></tr>
</tbody></table>

<div class="api-method-group-title">Rules and hooks</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-add-transition"><code>AddTransition()</code></a></td><td>Adds a machine-wide transition rule that can fire from any active state.</td></tr>
<tr><td><a href="#statement-remove-transition"><code>RemoveTransition()</code></a></td><td>Removes a specific machine-wide transition rule.</td></tr>
<tr><td><a href="#statement-clear-transitions"><code>ClearTransitions()</code></a></td><td>Removes all machine-wide transition rules.</td></tr>
<tr><td><a href="#statement-add-any-exit-hook"><code>AddAnyExitHook()</code></a></td><td>Adds a hook that runs after the current state&#x27;s Exit handlers but before the state changes. It is called as fn(result).</td></tr>
<tr><td><a href="#statement-add-any-enter-hook"><code>AddAnyEnterHook()</code></a></td><td>Adds a hook that runs after the state changes but before the new state enters. It is called as fn(result).</td></tr>
<tr><td><a href="#statement-add-any-transition-hook"><code>AddAnyTransitionHook()</code></a></td><td>Adds a hook that runs immediately after the state changes, before enter hooks and the new state Enter handler. It is called as fn(result).</td></tr>
<tr><td><a href="#statement-clear-any-exit-hooks"><code>ClearAnyExitHooks()</code></a></td><td>Removes all any-exit hooks from this machine.</td></tr>
<tr><td><a href="#statement-clear-any-enter-hooks"><code>ClearAnyEnterHooks()</code></a></td><td>Removes all any-enter hooks from this machine.</td></tr>
<tr><td><a href="#statement-clear-any-transition-hooks"><code>ClearAnyTransitionHooks()</code></a></td><td>Removes all any-transition hooks from this machine.</td></tr>
</tbody></table>

<div class="api-method-group-title">Timing, pause, and events</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-set-time-scale"><code>SetTimeScale()</code></a></td><td>Sets this machine&#x27;s logical update rate.</td></tr>
<tr><td><a href="#statement-get-time-scale"><code>GetTimeScale()</code></a></td><td>Returns this machine&#x27;s logical update scale.</td></tr>
<tr><td><a href="#statement-get-global-time-scale"><code>GetGlobalTimeScale()</code></a></td><td>Returns the global time scale applied to externally driven root machines.</td></tr>
<tr><td><a href="#statement-set-paused"><code>SetPaused()</code></a></td><td>Sets this machine&#x27;s own pause state without changing pause inherited from its host or parent.</td></tr>
<tr><td><a href="#statement-is-paused"><code>IsPaused()</code></a></td><td>Checks whether this machine is paused for any reason.</td></tr>
<tr><td><a href="#statement-get-state-time"><code>GetStateTime()</code></a></td><td>Returns the number of logical <a href="#statement"><code>Statement</code></a> updates spent in the current state.</td></tr>
<tr><td><a href="#statement-set-state-time"><code>SetStateTime()</code></a></td><td>Sets the recorded logical update age of the current state.</td></tr>
<tr><td><a href="#statement-update"><code>Update()</code></a></td><td>Updates this machine using the global <a href="#statement"><code>Statement</code></a> update mode. Event mode supplies one update credit per call. Delta-time mode converts elapsed time into credit for externally driven root machines.</td></tr>
<tr><td><a href="#statement-draw"><code>Draw()</code></a></td><td>Runs Draw on the active state and each active child state, from parent to deepest child.</td></tr>
<tr><td><a href="#statement-run-state"><code>RunState()</code></a></td><td>Sends a built-in or custom event through the active state hierarchy using the chosen dispatch mode.</td></tr>
<tr><td><a href="#statement-evaluate-transitions"><code>EvaluateTransitions()</code></a></td><td>Checks transition rules by priority and runs the first passing rule that can change state. Machine rules win ties, and self-target rules are skipped.</td></tr>
</tbody></table>

<div class="api-method-group-title">Debugging and inspection</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-print-state-names"><code>PrintStateNames()</code></a></td><td>Prints all registered state names to Echo at INFO level.</td></tr>
<tr><td><a href="#statement-debug-describe"><code>DebugDescribe()</code></a></td><td>Prints a one-line INFO summary of this machine&#x27;s owner, state, queue, stack, and history.</td></tr>
<tr><td><a href="#statement-print-state-history"><code>PrintStateHistory()</code></a></td><td>Prints this machine&#x27;s previous states from most recent to oldest.</td></tr>
<tr><td><a href="#statement-set-debug-enabled"><code>SetDebugEnabled()</code></a></td><td>Enables or disables debug tracking for this machine.</td></tr>
<tr><td><a href="#statement-is-debug-enabled"><code>IsDebugEnabled()</code></a></td><td>Returns whether debug tracking is enabled for this machine.</td></tr>
<tr><td><a href="#statement-set-debug-name"><code>SetDebugName()</code></a></td><td>Sets a friendly name for this machine in debug UIs.</td></tr>
<tr><td><a href="#statement-debug-tag"><code>DebugTag()</code></a></td><td>Sets a tag (or comma-separated tags) for grouping/filtering in debug UIs.</td></tr>
<tr><td><a href="#statement-get-debug-tag"><code>GetDebugTag()</code></a></td><td>Returns the debug tag string, if set.</td></tr>
<tr><td><a href="#statement-debug-pause"><code>DebugPause()</code></a></td><td>Pause this machine for debug purposes.</td></tr>
<tr><td><a href="#statement-debug-resume"><code>DebugResume()</code></a></td><td>Resume this machine from a debug pause.</td></tr>
<tr><td><a href="#statement-debug-step"><code>DebugStep()</code></a></td><td>Runs exactly one logical machine update while debug-paused, ignoring update scheduling and time scale.</td></tr>
<tr><td><a href="#statement-is-debug-paused"><code>IsDebugPaused()</code></a></td><td>Returns whether this machine is paused by a machine-local debug condition.</td></tr>
<tr><td><a href="#statement-get-debug-pause-reason"><code>GetDebugPauseReason()</code></a></td><td>Returns the active machine-local debug pause reason.</td></tr>
<tr><td><a href="#statement-get-debug-name"><code>GetDebugName()</code></a></td><td>Returns the friendly debug name, or a fallback based on the owner.</td></tr>
<tr><td><a href="#statement-debug-jump-to-state"><code>DebugJumpToState()</code></a></td><td>Requests a transition from debug tooling using the target state&#x27;s configured debug payload.</td></tr>
<tr><td><a href="#statement-get-debug-graph"><code>GetDebugGraph()</code></a></td><td>Returns this machine&#x27;s debug graph data.</td></tr>
<tr><td><a href="#statement-get-debug-state-stats"><code>GetDebugStateStats()</code></a></td><td>Returns the per-state debug stats map.</td></tr>
<tr><td><a href="#statement-get-debug-state-stats-for"><code>GetDebugStateStatsFor()</code></a></td><td>Returns the debug stats record for the supplied state name/tag value.</td></tr>
<tr><td><a href="#statement-get-debug-transition-history"><code>GetDebugTransitionHistory()</code></a></td><td>Returns the recent transition history records.</td></tr>
<tr><td><a href="#statement-clear-debug-transition-history"><code>ClearDebugTransitionHistory()</code></a></td><td>Clears any recorded transition history entries.</td></tr>
<tr><td><a href="#statement-debug-set-error-behavior"><code>DebugSetErrorBehavior()</code></a></td><td>Sets how the machine reacts to caught errors: PAUSE (default) or RETHROW.</td></tr>
<tr><td><a href="#statement-debug-set-log-errors-to-file"><code>DebugSetLogErrorsToFile()</code></a></td><td>Control whether caught errors append to debug_statement_errors.log before optional rethrow.</td></tr>
</tbody></table>

<div class="api-method-entry" id="statement-set-initial-state">
  <div class="api-method-name">SetInitialState(name)</div>
  <p class="api-method-summary">Sets which registered state should be entered when this machine starts.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The state name/tag value to use as the initial state.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-set-reset-mode">
  <div class="api-method-name">SetResetMode(mode)</div>
  <p class="api-method-summary">Sets how this machine behaves when its host state exits.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">mode</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-statement-reset-mode"><code>eStatementResetMode</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-set-inherit-pause">
  <div class="api-method-name">SetInheritPause(enabled)</div>
  <p class="api-method-summary">Sets whether this machine is paused when its parent machine is paused.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">enabled</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether parent runtime pause should affect this machine.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-is-running">
  <div class="api-method-name">IsRunning()</div>
  <p class="api-method-summary">Checks whether this machine currently has an active state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-start">
  <div class="api-method-name">Start([data])</div>
  <p class="api-method-summary">Explicitly starts this machine by entering its configured initial state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">data <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional payload supplied to the initial state&#x27;s Enter lifecycle.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-result">StatementTransitionResult</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-stop">
  <div class="api-method-name">Stop()</div>
  <p class="api-method-summary">Stops the machine, exiting child machines first while keeping its states and settings.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-result">StatementTransitionResult</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-reset">
  <div class="api-method-name">Reset([data])</div>
  <p class="api-method-summary">Stops this machine and starts it again from its configured initial state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">data <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional payload supplied to the fresh initial-state entry.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-result">StatementTransitionResult</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-clear-states">
  <div class="api-method-name">ClearStates()</div>
  <p class="api-method-summary">Stops the machine and removes all states and machine-wide transition rules without resetting its settings.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-set-history-limit">
  <div class="api-method-name">SetHistoryLimit(limit)</div>
  <p class="api-method-summary">Sets how many previous states are kept in history. Values at or below zero mean no limit.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">limit</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Maximum number of previous states to retain.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-history-count">
  <div class="api-method-name">GetHistoryCount()</div>
  <p class="api-method-summary">Returns how many states are currently stored in history.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-history-at">
  <div class="api-method-name">GetHistoryAt(index)</div>
  <p class="api-method-summary">Returns a state retained at the supplied history index.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">index</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">The zero-based history index to retrieve.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-clear-history">
  <div class="api-method-name">ClearHistory()</div>
  <p class="api-method-summary">Clears state history without changing the active state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-was-previously-in-state">
  <div class="api-method-name">WasPreviouslyInState(name, [depth])</div>
  <p class="api-method-summary">Returns whether the state at the requested history depth matches a supplied state name.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The state name to compare against.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">depth <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">History depth where 1 is the most recent previous state.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-set-queue-phase">
  <div class="api-method-name">SetQueuePhase(phase)</div>
  <p class="api-method-summary">Sets when queued transitions are processed automatically, or disables automatic processing with MANUAL.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">phase</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-statement-queue-phase"><code>eStatementQueuePhase</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-queue-phase">
  <div class="api-method-name">GetQueuePhase()</div>
  <p class="api-method-summary">Returns when queued transitions are processed automatically.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-state">
  <div class="api-method-name">GetState([state_name])</div>
  <p class="api-method-summary">Returns a registered state by name/tag value, or returns the active state when no name is supplied.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">state_name <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional state name/tag value to look up.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-add-transition">
  <div class="api-method-name">AddTransition(rule)</div>
  <p class="api-method-summary">Adds a machine-wide transition rule that can fire from any active state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">rule</span>
      <span class="api-argument-type">Struct.<a href="#statement-transition-rule">StatementTransitionRule</a></span>
      <span class="api-argument-description">The unattached rule to bind to this machine.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-remove-transition">
  <div class="api-method-name">RemoveTransition(rule)</div>
  <p class="api-method-summary">Removes a specific machine-wide transition rule.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">rule</span>
      <span class="api-argument-type">Struct.<a href="#statement-transition-rule">StatementTransitionRule</a></span>
      <span class="api-argument-description">The attached rule to remove.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-clear-transitions">
  <div class="api-method-name">ClearTransitions()</div>
  <p class="api-method-summary">Removes all machine-wide transition rules.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-add-state">
  <div class="api-method-name">AddState(state)</div>
  <p class="api-method-summary">Registers a state definition without running gameplay code. The first state added becomes the default initial state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">state</span>
      <span class="api-argument-type">Struct.<a href="#statement-state">StatementState</a></span>
      <span class="api-argument-description">The state definition to register.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-add-state-template">
  <div class="api-method-name">AddStateTemplate(template, [config], [name], [clone])</div>
  <p class="api-method-summary">Builds a state from a template and registers it without starting the machine.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">template</span>
      <span class="api-argument-type">Struct.<a href="#statement-state-template">StatementStateTemplate</a></span>
      <span class="api-argument-description">The template to build from.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">config <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional config to assign to the created state.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">name <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional override for the state&#x27;s name.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">clone <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Optional override for config cloning.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-change-state">
  <div class="api-method-name">ChangeState(name, [data], [force])</div>
  <p class="api-method-summary">Requests a normal transition to a registered state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The target state name/tag value.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">data <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional payload associated with this transition.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">force <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether to bypass exit locks and guards.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-result">StatementTransitionResult</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#statement-transition-result"><code>StatementTransitionResult</code></a> <span aria-hidden="true">·</span> <a href="{{ '/statement/changing-states-and-data' | relative_url }}">Changing States &amp; Passing Data</a></div>
  </div>
</div>

<div class="api-method-entry" id="statement-reenter-state">
  <div class="api-method-name">ReenterState([data], [force])</div>
  <p class="api-method-summary">Runs the active state&#x27;s Exit and Enter handlers again without changing to another state first.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">data <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional payload associated with the re-entry.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">force <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether to bypass exit locks and guards.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-result">StatementTransitionResult</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-add-any-exit-hook">
  <div class="api-method-name">AddAnyExitHook(function)</div>
  <p class="api-method-summary">Adds a hook that runs after the current state&#x27;s Exit handlers but before the state changes. It is called as fn(result).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">function</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">The hook function.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-add-any-enter-hook">
  <div class="api-method-name">AddAnyEnterHook(function)</div>
  <p class="api-method-summary">Adds a hook that runs after the state changes but before the new state enters. It is called as fn(result).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">function</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">The hook function.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-add-any-transition-hook">
  <div class="api-method-name">AddAnyTransitionHook(function)</div>
  <p class="api-method-summary">Adds a hook that runs immediately after the state changes, before enter hooks and the new state Enter handler. It is called as fn(result).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">function</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">The hook function.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-clear-any-exit-hooks">
  <div class="api-method-name">ClearAnyExitHooks()</div>
  <p class="api-method-summary">Removes all any-exit hooks from this machine.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-clear-any-enter-hooks">
  <div class="api-method-name">ClearAnyEnterHooks()</div>
  <p class="api-method-summary">Removes all any-enter hooks from this machine.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-clear-any-transition-hooks">
  <div class="api-method-name">ClearAnyTransitionHooks()</div>
  <p class="api-method-summary">Removes all any-transition hooks from this machine.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-queue-state">
  <div class="api-method-name">QueueState(name, [data], [force])</div>
  <p class="api-method-summary">Stores one buffered transition request to be processed according to this machine&#x27;s queue phase.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The target state name/tag value.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">data <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional payload associated with the queued transition.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">force <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether the queued transition should bypass exit restrictions.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="{{ '/statement/locks-and-queues' | relative_url }}">Locks &amp; Queues</a></div>
  </div>
</div>

<div class="api-method-entry" id="statement-process-queued-state">
  <div class="api-method-name">ProcessQueuedState()</div>
  <p class="api-method-summary">Immediately attempts the currently buffered transition. Exit-lock and exit-guard failures keep the request pending.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-result">StatementTransitionResult</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-has-queued-state">
  <div class="api-method-name">HasQueuedState()</div>
  <p class="api-method-summary">Returns whether a buffered transition is currently pending.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-queued-state-name">
  <div class="api-method-name">GetQueuedStateName()</div>
  <p class="api-method-summary">Returns the queued target state name when a request is pending.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-queued-state-data">
  <div class="api-method-name">GetQueuedStateData()</div>
  <p class="api-method-summary">Returns the payload associated with the queued transition when one is pending.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-clear-queued-state">
  <div class="api-method-name">ClearQueuedState()</div>
  <p class="api-method-summary">Clears the buffered transition request without processing it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-push-state">
  <div class="api-method-name">PushState(name, [data], [force])</div>
  <p class="api-method-summary">Transitions to another state and records the previous state on the stack only when the transition succeeds.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The target state name/tag value.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">data <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional transition payload.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">force <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether to bypass exit restrictions.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-result">StatementTransitionResult</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#statement-pop-state"><code>Statement.PopState</code></a> <span aria-hidden="true">·</span> <a href="{{ '/statement/temporary-states-and-history' | relative_url }}">Temporary States &amp; History</a></div>
  </div>
</div>

<div class="api-method-entry" id="statement-pop-state">
  <div class="api-method-name">PopState([data], [force])</div>
  <p class="api-method-summary">Attempts to return to the most recently pushed state and removes the stack entry only after success.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">data <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional transition payload.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">force <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether to bypass exit restrictions.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-result">StatementTransitionResult</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-state-stack-depth">
  <div class="api-method-name">GetStateStackDepth()</div>
  <p class="api-method-summary">Returns the number of saved states on the push/pop stack.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-peek-state-stack">
  <div class="api-method-name">PeekStateStack()</div>
  <p class="api-method-summary">Returns the most recently pushed state without mutating the stack.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-clear-state-stack">
  <div class="api-method-name">ClearStateStack()</div>
  <p class="api-method-summary">Clears the push/pop stack without changing the active state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-previous-state">
  <div class="api-method-name">PreviousState([data], [force])</div>
  <p class="api-method-summary">Attempts to return to the most recent previous state retained in runtime history.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">data <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional transition payload.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">force <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether to bypass exit restrictions.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-result">StatementTransitionResult</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-state-name">
  <div class="api-method-name">GetStateName()</div>
  <p class="api-method-summary">Returns the active state&#x27;s name/tag value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-child-machine">
  <div class="api-method-name">GetChildMachine()</div>
  <p class="api-method-summary">Returns the submachine hosted by the active state, if any.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-child-state">
  <div class="api-method-name">GetChildState()</div>
  <p class="api-method-summary">Returns the active state of the current state&#x27;s hosted submachine, if any.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-is-in-path">
  <div class="api-method-name">IsInPath(path)</div>
  <p class="api-method-summary">Returns whether this machine&#x27;s active hierarchy matches a supplied nested state path.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">path</span>
      <span class="api-argument-type">String,Array</span>
      <span class="api-argument-description">A slash-delimited string or array of nested state names.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-is-in-state">
  <div class="api-method-name">IsInState(state_or_state_struct)</div>
  <p class="api-method-summary">Returns whether the supplied state name or <a href="#statement-state"><code>StatementState</code></a> is the active state of this machine.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">state_or_state_struct</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">A state name/tag value or registered <a href="#statement-state"><code>StatementState</code></a>.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-set-paused">
  <div class="api-method-name">SetPaused(paused)</div>
  <p class="api-method-summary">Sets this machine&#x27;s own pause state without changing pause inherited from its host or parent.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">paused</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether this machine should be locally paused.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-is-paused">
  <div class="api-method-name">IsPaused()</div>
  <p class="api-method-summary">Checks whether this machine is paused for any reason.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-ensure-state">
  <div class="api-method-name">EnsureState(name, [data], [force])</div>
  <p class="api-method-summary">Requests the supplied state and naturally reports SAME_STATE when it is already active.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The target state name/tag value.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">data <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional transition payload.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">force <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether to bypass exit restrictions.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-result">StatementTransitionResult</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-state-time">
  <div class="api-method-name">GetStateTime()</div>
  <p class="api-method-summary">Returns the number of logical <a href="#statement"><code>Statement</code></a> updates spent in the current state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-set-state-time">
  <div class="api-method-name">SetStateTime(time)</div>
  <p class="api-method-summary">Sets the recorded logical update age of the current state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">time</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">The new logical state age.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-update">
  <div class="api-method-name">Update()</div>
  <p class="api-method-summary">Updates this machine using the global <a href="#statement"><code>Statement</code></a> update mode. Event mode supplies one update credit per call. Delta-time mode converts elapsed time into credit for externally driven root machines.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-draw">
  <div class="api-method-name">Draw()</div>
  <p class="api-method-summary">Runs Draw on the active state and each active child state, from parent to deepest child.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-run-state">
  <div class="api-method-name">RunState(event, [payload], [dispatch])</div>
  <p class="api-method-summary">Sends a built-in or custom event through the active state hierarchy using the chosen dispatch mode.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">event</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">A built-in <a href="#enum-e-statement-events"><code>eStatementEvents</code></a> value or <a href="#statement-event"><code>StatementEvent</code></a> identity.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">payload <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Payload supplied to custom handlers.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">dispatch <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses <a href="#enum-e-statement-event-dispatch"><code>eStatementEventDispatch</code></a>. Defaults to CURRENT.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-evaluate-transitions">
  <div class="api-method-name">EvaluateTransitions([phase])</div>
  <p class="api-method-summary">Checks transition rules by priority and runs the first passing rule that can change state. Machine rules win ties, and self-target rules are skipped.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">phase <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses <a href="#enum-e-statement-transition-phase"><code>eStatementTransitionPhase</code></a>. Defaults to AFTER_UPDATE.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-result">StatementTransitionResult</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-remove-state">
  <div class="api-method-name">RemoveState(name)</div>
  <p class="api-method-summary">Removes a registered state. Removing the active state stops the machine first.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The name/tag value of the state to remove.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-print-state-names">
  <div class="api-method-name">PrintStateNames()</div>
  <p class="api-method-summary">Prints all registered state names to Echo at INFO level.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-debug-describe">
  <div class="api-method-name">DebugDescribe()</div>
  <p class="api-method-summary">Prints a one-line INFO summary of this machine&#x27;s owner, state, queue, stack, and history.</p>
</div>

<div class="api-method-entry" id="statement-print-state-history">
  <div class="api-method-name">PrintStateHistory([limit])</div>
  <p class="api-method-summary">Prints this machine&#x27;s previous states from most recent to oldest.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">limit <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Maximum number of history entries to print (1 = most recent only). Use 0 or a negative value to print all entries.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-previous-state-name">
  <div class="api-method-name">GetPreviousStateName()</div>
  <p class="api-method-summary">Returns the name of the most recent previous state in the history, if any.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-last-transition-data">
  <div class="api-method-name">GetLastTransitionData()</div>
  <p class="api-method-summary">Returns the payload associated with the last successful state transition, if any.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-destroy">
  <div class="api-method-name">Destroy()</div>
  <p class="api-method-summary">Destroys the machine, its child machines, states, hooks, and debug registration.</p>
</div>

<div class="api-method-entry" id="statement-set-debug-enabled">
  <div class="api-method-name">SetDebugEnabled(enabled)</div>
  <p class="api-method-summary">Enables or disables debug tracking for this machine.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">enabled</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-is-debug-enabled">
  <div class="api-method-name">IsDebugEnabled()</div>
  <p class="api-method-summary">Returns whether debug tracking is enabled for this machine.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-set-debug-name">
  <div class="api-method-name">SetDebugName(name)</div>
  <p class="api-method-summary">Sets a friendly name for this machine in debug UIs.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-set-time-scale">
  <div class="api-method-name">SetTimeScale(scale)</div>
  <p class="api-method-summary">Sets this machine&#x27;s logical update rate.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">scale</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#statement-set-global-time-scale"><code>StatementSetGlobalTimeScale</code></a> <span aria-hidden="true">·</span> <a href="{{ '/statement/timing-pause-and-updates' | relative_url }}">Timing, Pause &amp; Update Behaviour</a></div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-time-scale">
  <div class="api-method-name">GetTimeScale()</div>
  <p class="api-method-summary">Returns this machine&#x27;s logical update scale.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-global-time-scale">
  <div class="api-method-name">GetGlobalTimeScale()</div>
  <p class="api-method-summary">Returns the global time scale applied to externally driven root machines.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-debug-tag">
  <div class="api-method-name">DebugTag(tag)</div>
  <p class="api-method-summary">Sets a tag (or comma-separated tags) for grouping/filtering in debug UIs.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tag</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-debug-tag">
  <div class="api-method-name">GetDebugTag()</div>
  <p class="api-method-summary">Returns the debug tag string, if set.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-debug-pause">
  <div class="api-method-name">DebugPause()</div>
  <p class="api-method-summary">Pause this machine for debug purposes.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-debug-resume">
  <div class="api-method-name">DebugResume()</div>
  <p class="api-method-summary">Resume this machine from a debug pause.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-debug-step">
  <div class="api-method-name">DebugStep()</div>
  <p class="api-method-summary">Runs exactly one logical machine update while debug-paused, ignoring update scheduling and time scale.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-is-debug-paused">
  <div class="api-method-name">IsDebugPaused()</div>
  <p class="api-method-summary">Returns whether this machine is paused by a machine-local debug condition.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-debug-pause-reason">
  <div class="api-method-name">GetDebugPauseReason()</div>
  <p class="api-method-summary">Returns the active machine-local debug pause reason.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-debug-name">
  <div class="api-method-name">GetDebugName()</div>
  <p class="api-method-summary">Returns the friendly debug name, or a fallback based on the owner.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-debug-jump-to-state">
  <div class="api-method-name">DebugJumpToState(name, [force])</div>
  <p class="api-method-summary">Requests a transition from debug tooling using the target state&#x27;s configured debug payload.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The target state name/tag value.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">force <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether to bypass exit restrictions.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-result">StatementTransitionResult</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-debug-graph">
  <div class="api-method-name">GetDebugGraph()</div>
  <p class="api-method-summary">Returns this machine&#x27;s debug graph data.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-debug-state-stats">
  <div class="api-method-name">GetDebugStateStats()</div>
  <p class="api-method-summary">Returns the per-state debug stats map.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-debug-state-stats-for">
  <div class="api-method-name">GetDebugStateStatsFor(state_name)</div>
  <p class="api-method-summary">Returns the debug stats record for the supplied state name/tag value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">state_name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The state name/tag value to look up.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-debug-transition-history">
  <div class="api-method-name">GetDebugTransitionHistory()</div>
  <p class="api-method-summary">Returns the recent transition history records.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Array,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-clear-debug-transition-history">
  <div class="api-method-name">ClearDebugTransitionHistory()</div>
  <p class="api-method-summary">Clears any recorded transition history entries.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-debug-set-error-behavior">
  <div class="api-method-name">DebugSetErrorBehavior(behavior)</div>
  <p class="api-method-summary">Sets how the machine reacts to caught errors: PAUSE (default) or RETHROW.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">behavior</span>
      <span class="api-argument-type">Constant.<a href="#enum-e-statement-error-behavior">eStatementErrorBehavior</a></span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-debug-set-log-errors-to-file">
  <div class="api-method-name">DebugSetLogErrorsToFile(log_to_file)</div>
  <p class="api-method-summary">Control whether caught errors append to debug_statement_errors.log before optional rethrow.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">log_to_file</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description"></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

### StatementState
{: #statement-state .api-type-title }

Creates a state bound to the given owner and identified by the supplied name/tag value.

```gml
new StatementState(id, name)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">id</span>
      <span class="api-argument-type">Id.Instance,Struct</span>
      <span class="api-argument-description">The instance or struct the state belongs to.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The unique state name/tag value within its machine.</span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Submachines</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-state-create-sub-machine"><code>CreateSubMachine()</code></a></td><td>Creates and attaches a child <a href="#statement"><code>Statement</code></a> machine to this state.</td></tr>
<tr><td><a href="#statement-state-has-sub-machine"><code>HasSubMachine()</code></a></td><td>Returns whether this state hosts a child machine.</td></tr>
<tr><td><a href="#statement-state-get-sub-machine"><code>GetSubMachine()</code></a></td><td>Returns the child machine hosted by this state.</td></tr>
<tr><td><a href="#statement-state-lock-exit-until-sub-in"><code>LockExitUntilSubIn()</code></a></td><td>Prevents normal exits while this state&#x27;s child machine is not currently in the supplied state. Does not restrict exit when no child machine exists.</td></tr>
<tr><td><a href="#statement-state-lock-exit-while-sub-not"><code>LockExitWhileSubNot()</code></a></td><td>Prevents normal exits while the supplied child-machine condition returns false. The callback is called as fn(submachine). Does not restrict exit when no child machine exists.</td></tr>
<tr><td><a href="#statement-state-on-submachine-enter"><code>OnSubmachineEnter()</code></a></td><td>Sets a callback that runs after this state enters and its child machine is ready. It is called as fn(state, submachine, transition).</td></tr>
<tr><td><a href="#statement-state-on-submachine-exit"><code>OnSubmachineExit()</code></a></td><td>Sets a callback that runs when this state exits and its child machine stops or suspends. It is called as fn(state, submachine, transition).</td></tr>
</tbody></table>

<div class="api-method-group-title">Exit locks and guards</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-state-lock-exit"><code>LockExit()</code></a></td><td>Adds a named exit lock. Any active exit lock blocks normal transitions out of this state.</td></tr>
<tr><td><a href="#statement-state-unlock-exit"><code>UnlockExit()</code></a></td><td>Removes one named exit lock without affecting other active locks.</td></tr>
<tr><td><a href="#statement-state-clear-exit-locks"><code>ClearExitLocks()</code></a></td><td>Removes every named exit lock from this state.</td></tr>
<tr><td><a href="#statement-state-is-exit-locked"><code>IsExitLocked()</code></a></td><td>Returns whether at least one named exit lock is active.</td></tr>
<tr><td><a href="#statement-state-has-exit-lock"><code>HasExitLock()</code></a></td><td>Returns whether the supplied named exit lock is active.</td></tr>
<tr><td><a href="#statement-state-get-exit-lock-count"><code>GetExitLockCount()</code></a></td><td>Returns the number of independent exit locks active on this state.</td></tr>
<tr><td><a href="#statement-state-add-exit-guard"><code>AddExitGuard()</code></a></td><td>Adds a named exit check. Every exit check must return true before a normal transition can leave this state. It is called as fn(state, transition).</td></tr>
<tr><td><a href="#statement-state-remove-exit-guard"><code>RemoveExitGuard()</code></a></td><td>Removes one exit guard by name.</td></tr>
<tr><td><a href="#statement-state-clear-exit-guards"><code>ClearExitGuards()</code></a></td><td>Removes every exit guard from this state.</td></tr>
<tr><td><a href="#statement-state-has-exit-guard"><code>HasExitGuard()</code></a></td><td>Returns whether an exit guard with the supplied name exists.</td></tr>
<tr><td><a href="#statement-state-get-exit-guard-count"><code>GetExitGuardCount()</code></a></td><td>Returns how many independent exit guards are attached to this state.</td></tr>
</tbody></table>

<div class="api-method-group-title">Config and timer</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-state-set-config"><code>SetConfig()</code></a></td><td>Sets config data for this state, optionally cloning the supplied value.</td></tr>
<tr><td><a href="#statement-state-get-config"><code>GetConfig()</code></a></td><td>Returns this state&#x27;s config data.</td></tr>
<tr><td><a href="#statement-state-timer-start"><code>TimerStart()</code></a></td><td>Enables this state&#x27;s lightweight timer, resets it to zero, and begins advancing it while this state is active.</td></tr>
<tr><td><a href="#statement-state-timer-set"><code>TimerSet()</code></a></td><td>Replaces the current state-timer value without changing whether the timer is running.</td></tr>
<tr><td><a href="#statement-state-timer-get"><code>TimerGet()</code></a></td><td>Returns the current state-timer value.</td></tr>
<tr><td><a href="#statement-state-timer-pause"><code>TimerPause()</code></a></td><td>Pauses this state&#x27;s timer without changing its current value.</td></tr>
<tr><td><a href="#statement-state-timer-resume"><code>TimerResume()</code></a></td><td>Resumes a timer that has previously been enabled with TimerStart().</td></tr>
<tr><td><a href="#statement-state-timer-stop"><code>TimerStop()</code></a></td><td>Disables this state&#x27;s timer and resets its value to zero. Call TimerStart() to enable it again.</td></tr>
<tr><td><a href="#statement-state-timer-is-running"><code>TimerIsRunning()</code></a></td><td>Returns whether this state&#x27;s timer is currently enabled and advancing while the state is active.</td></tr>
</tbody></table>

<div class="api-method-group-title">Handlers and events</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-state-add-enter"><code>AddEnter()</code></a></td><td>Binds an owner-scoped Enter handler called as fn(state, transition).</td></tr>
<tr><td><a href="#statement-state-add-update"><code>AddUpdate()</code></a></td><td>Binds an owner-scoped Update handler called as fn(state).</td></tr>
<tr><td><a href="#statement-state-add-exit"><code>AddExit()</code></a></td><td>Binds an owner-scoped Exit handler called as fn(state, transition).</td></tr>
<tr><td><a href="#statement-state-add-draw"><code>AddDraw()</code></a></td><td>Binds an owner-scoped Draw handler called as fn(state).</td></tr>
<tr><td><a href="#statement-state-add-state-event"><code>AddStateEvent()</code></a></td><td>Sets a handler for a built-in event or custom <a href="#statement-event"><code>StatementEvent</code></a>. Custom handlers are called as fn(state, payload).</td></tr>
<tr><td><a href="#statement-state-has-state-event"><code>HasStateEvent()</code></a></td><td>Checks whether this state handles the given built-in or custom event.</td></tr>
</tbody></table>

<div class="api-method-group-title">Transition rules</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-state-add-transition"><code>AddTransition()</code></a></td><td>Adds a transition rule to this state.</td></tr>
<tr><td><a href="#statement-state-remove-transition"><code>RemoveTransition()</code></a></td><td>Removes a specific transition rule.</td></tr>
<tr><td><a href="#statement-state-clear-transitions"><code>ClearTransitions()</code></a></td><td>Removes all transition rules from this state.</td></tr>
</tbody></table>

<div class="api-method-group-title">Debug metadata</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-state-debug-link-to"><code>DebugLinkTo()</code></a></td><td>Declares a debug-only visual connection from this state to another state.</td></tr>
<tr><td><a href="#statement-state-debug-payload"><code>DebugPayload()</code></a></td><td>Sets the default payload used when debug tooling jumps to this state.</td></tr>
<tr><td><a href="#statement-state-debug-break-on-enter"><code>DebugBreakOnEnter()</code></a></td><td>Enables or disables a debug breakpoint whenever this state is entered.</td></tr>
<tr><td><a href="#statement-state-debug-tag"><code>DebugTag()</code></a></td><td>Assigns a tag used for grouping and filtering in debug tooling.</td></tr>
</tbody></table>

<div class="api-method-entry" id="statement-state-create-sub-machine">
  <div class="api-method-name">CreateSubMachine([name])</div>
  <p class="api-method-summary">Creates and attaches a child <a href="#statement"><code>Statement</code></a> machine to this state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional friendly child-machine name used by debug tooling.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#enum-e-statement-reset-mode"><code>eStatementResetMode</code></a> <span aria-hidden="true">·</span> <a href="{{ '/statement/submachines' | relative_url }}">Nested State Machines</a></div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-has-sub-machine">
  <div class="api-method-name">HasSubMachine()</div>
  <p class="api-method-summary">Returns whether this state hosts a child machine.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-get-sub-machine">
  <div class="api-method-name">GetSubMachine()</div>
  <p class="api-method-summary">Returns the child machine hosted by this state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-on-submachine-enter">
  <div class="api-method-name">OnSubmachineEnter(function)</div>
  <p class="api-method-summary">Sets a callback that runs after this state enters and its child machine is ready. It is called as fn(state, submachine, transition).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">function</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">The callback function.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-on-submachine-exit">
  <div class="api-method-name">OnSubmachineExit(function)</div>
  <p class="api-method-summary">Sets a callback that runs when this state exits and its child machine stops or suspends. It is called as fn(state, submachine, transition).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">function</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">The callback function.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-lock-exit-until-sub-in">
  <div class="api-method-name">LockExitUntilSubIn(state_name)</div>
  <p class="api-method-summary">Prevents normal exits while this state&#x27;s child machine is not currently in the supplied state. Does not restrict exit when no child machine exists.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">state_name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The child state name/tag value required before the host may exit.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-lock-exit-while-sub-not">
  <div class="api-method-name">LockExitWhileSubNot(condition)</div>
  <p class="api-method-summary">Prevents normal exits while the supplied child-machine condition returns false. The callback is called as fn(submachine). Does not restrict exit when no child machine exists.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">condition</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function that returns true when the host state may exit.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-lock-exit">
  <div class="api-method-name">LockExit([name])</div>
  <p class="api-method-summary">Adds a named exit lock. Any active exit lock blocks normal transitions out of this state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Lock identity. Defaults to &quot;default&quot;.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-unlock-exit">
  <div class="api-method-name">UnlockExit([name])</div>
  <p class="api-method-summary">Removes one named exit lock without affecting other active locks.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Lock identity. Defaults to &quot;default&quot;.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-clear-exit-locks">
  <div class="api-method-name">ClearExitLocks()</div>
  <p class="api-method-summary">Removes every named exit lock from this state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-is-exit-locked">
  <div class="api-method-name">IsExitLocked()</div>
  <p class="api-method-summary">Returns whether at least one named exit lock is active.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-has-exit-lock">
  <div class="api-method-name">HasExitLock(name)</div>
  <p class="api-method-summary">Returns whether the supplied named exit lock is active.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The lock identity to test.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-get-exit-lock-count">
  <div class="api-method-name">GetExitLockCount()</div>
  <p class="api-method-summary">Returns the number of independent exit locks active on this state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-add-exit-guard">
  <div class="api-method-name">AddExitGuard(name, condition)</div>
  <p class="api-method-summary">Adds a named exit check. Every exit check must return true before a normal transition can leave this state. It is called as fn(state, transition).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Unique guard identity used for removal and transition diagnostics.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">condition</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function that returns true when the state may exit.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-remove-exit-guard">
  <div class="api-method-name">RemoveExitGuard(name)</div>
  <p class="api-method-summary">Removes one exit guard by name.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The guard identity to remove.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-clear-exit-guards">
  <div class="api-method-name">ClearExitGuards()</div>
  <p class="api-method-summary">Removes every exit guard from this state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-has-exit-guard">
  <div class="api-method-name">HasExitGuard(name)</div>
  <p class="api-method-summary">Returns whether an exit guard with the supplied name exists.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The guard identity to test.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-get-exit-guard-count">
  <div class="api-method-name">GetExitGuardCount()</div>
  <p class="api-method-summary">Returns how many independent exit guards are attached to this state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-set-config">
  <div class="api-method-name">SetConfig(config, [clone])</div>
  <p class="api-method-summary">Sets config data for this state, optionally cloning the supplied value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">config</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The config data stored by this state.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">clone <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Optional override for this state&#x27;s config cloning default.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-get-config">
  <div class="api-method-name">GetConfig()</div>
  <p class="api-method-summary">Returns this state&#x27;s config data.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-timer-start">
  <div class="api-method-name">TimerStart()</div>
  <p class="api-method-summary">Enables this state&#x27;s lightweight timer, resets it to zero, and begins advancing it while this state is active.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-timer-set">
  <div class="api-method-name">TimerSet(time)</div>
  <p class="api-method-summary">Replaces the current state-timer value without changing whether the timer is running.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">time</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">The timer value to store.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-timer-get">
  <div class="api-method-name">TimerGet()</div>
  <p class="api-method-summary">Returns the current state-timer value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-timer-pause">
  <div class="api-method-name">TimerPause()</div>
  <p class="api-method-summary">Pauses this state&#x27;s timer without changing its current value.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-timer-resume">
  <div class="api-method-name">TimerResume()</div>
  <p class="api-method-summary">Resumes a timer that has previously been enabled with TimerStart().</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-timer-stop">
  <div class="api-method-name">TimerStop()</div>
  <p class="api-method-summary">Disables this state&#x27;s timer and resets its value to zero. Call TimerStart() to enable it again.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-timer-is-running">
  <div class="api-method-name">TimerIsRunning()</div>
  <p class="api-method-summary">Returns whether this state&#x27;s timer is currently enabled and advancing while the state is active.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-add-enter">
  <div class="api-method-name">AddEnter(function, [mode])</div>
  <p class="api-method-summary">Binds an owner-scoped Enter handler called as fn(state, transition).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">function</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">The Enter handler to bind.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">mode <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-statement-bind-mode"><code>eStatementBindMode</code></a> enum. Defaults to REPLACE.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-add-update">
  <div class="api-method-name">AddUpdate(function, [mode])</div>
  <p class="api-method-summary">Binds an owner-scoped Update handler called as fn(state).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">function</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">The Update handler to bind.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">mode <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-statement-bind-mode"><code>eStatementBindMode</code></a> enum. Defaults to REPLACE.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-add-exit">
  <div class="api-method-name">AddExit(function, [mode])</div>
  <p class="api-method-summary">Binds an owner-scoped Exit handler called as fn(state, transition).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">function</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">The Exit handler to bind.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">mode <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-statement-bind-mode"><code>eStatementBindMode</code></a> enum. Defaults to REPLACE.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-add-draw">
  <div class="api-method-name">AddDraw(function, [mode])</div>
  <p class="api-method-summary">Binds an owner-scoped Draw handler called as fn(state).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">function</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">The Draw handler to bind.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">mode <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-statement-bind-mode"><code>eStatementBindMode</code></a> enum. Defaults to REPLACE.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-add-state-event">
  <div class="api-method-name">AddStateEvent(event, function, [mode])</div>
  <p class="api-method-summary">Sets a handler for a built-in event or custom <a href="#statement-event"><code>StatementEvent</code></a>. Custom handlers are called as fn(state, payload).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">event</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">A built-in <a href="#enum-e-statement-events"><code>eStatementEvents</code></a> value or <a href="#statement-event"><code>StatementEvent</code></a> identity.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">function</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">The handler function to bind to this state&#x27;s owner.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">mode <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-statement-bind-mode"><code>eStatementBindMode</code></a> enum. Defaults to REPLACE.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-has-state-event">
  <div class="api-method-name">HasStateEvent(event)</div>
  <p class="api-method-summary">Checks whether this state handles the given built-in or custom event.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">event</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The event identity to test.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-add-transition">
  <div class="api-method-name">AddTransition(rule)</div>
  <p class="api-method-summary">Adds a transition rule to this state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">rule</span>
      <span class="api-argument-type">Struct.<a href="#statement-transition-rule">StatementTransitionRule</a></span>
      <span class="api-argument-description">The unattached rule to bind to this state.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-remove-transition">
  <div class="api-method-name">RemoveTransition(rule)</div>
  <p class="api-method-summary">Removes a specific transition rule.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">rule</span>
      <span class="api-argument-type">Struct.<a href="#statement-transition-rule">StatementTransitionRule</a></span>
      <span class="api-argument-description">The attached rule to remove.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-clear-transitions">
  <div class="api-method-name">ClearTransitions()</div>
  <p class="api-method-summary">Removes all transition rules from this state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-debug-link-to">
  <div class="api-method-name">DebugLinkTo(target_name)</div>
  <p class="api-method-summary">Declares a debug-only visual connection from this state to another state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">target_name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The state name shown as the connection destination.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-debug-payload">
  <div class="api-method-name">DebugPayload(payload)</div>
  <p class="api-method-summary">Sets the default payload used when debug tooling jumps to this state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">payload</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The debug transition payload.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-debug-break-on-enter">
  <div class="api-method-name">DebugBreakOnEnter([break_on_enter])</div>
  <p class="api-method-summary">Enables or disables a debug breakpoint whenever this state is entered.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">break_on_enter <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether entering this state should pause debug execution. Defaults to true.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-debug-tag">
  <div class="api-method-name">DebugTag(tag)</div>
  <p class="api-method-summary">Assigns a tag used for grouping and filtering in debug tooling.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tag</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">The debug tag value.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a></span>
    </div>
  </div>
</div>

## Transitions and results

### StatementTransitionRule
{: #statement-transition-rule .api-type-title }

Creates a transition rule for a state or whole machine.

```gml
new StatementTransitionRule(target_name, condition)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">target_name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The state name entered when this rule passes.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">condition</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Owner-bound condition called as fn(state, rule) and expected to return true when the rule should fire.</span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Target and ordering</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-transition-rule-get-target-name"><code>GetTargetName()</code></a></td><td>Returns this rule&#x27;s destination state name.</td></tr>
<tr><td><a href="#statement-transition-rule-set-priority"><code>SetPriority()</code></a></td><td>Sets the rule priority. Higher values are checked first within the same phase.</td></tr>
<tr><td><a href="#statement-transition-rule-get-priority"><code>GetPriority()</code></a></td><td>Returns this rule&#x27;s evaluation priority.</td></tr>
<tr><td><a href="#statement-transition-rule-set-phase"><code>SetPhase()</code></a></td><td>Sets whether the rule is checked before or after the active state&#x27;s Update handler.</td></tr>
<tr><td><a href="#statement-transition-rule-get-phase"><code>GetPhase()</code></a></td><td>Returns when the rule is checked automatically.</td></tr>
</tbody></table>

<div class="api-method-group-title">Enable and force</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-transition-rule-set-enabled"><code>SetEnabled()</code></a></td><td>Enables or disables the rule without removing it.</td></tr>
<tr><td><a href="#statement-transition-rule-is-enabled"><code>IsEnabled()</code></a></td><td>Checks whether the rule is currently enabled.</td></tr>
<tr><td><a href="#statement-transition-rule-set-force"><code>SetForce()</code></a></td><td>Sets whether the rule ignores exit locks and guards when it fires.</td></tr>
<tr><td><a href="#statement-transition-rule-is-forced"><code>IsForced()</code></a></td><td>Checks whether the rule ignores exit restrictions when it fires.</td></tr>
</tbody></table>

<div class="api-method-group-title">Payload</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-transition-rule-set-data"><code>SetData()</code></a></td><td>Sets a fixed payload for the rule and removes any payload function.</td></tr>
<tr><td><a href="#statement-transition-rule-set-data-provider"><code>SetDataProvider()</code></a></td><td>Sets a function that creates the payload only when the rule fires. It is called as fn(state, rule).</td></tr>
<tr><td><a href="#statement-transition-rule-get-data"><code>GetData()</code></a></td><td>Returns the fixed payload. Payload functions only run when the rule fires.</td></tr>
</tbody></table>

<div class="api-method-group-title">Lifecycle</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-transition-rule-remove"><code>Remove()</code></a></td><td>Removes the rule from its state or machine.</td></tr>
<tr><td><a href="#statement-transition-rule-clone"><code>Clone()</code></a></td><td>Creates a copy of the rule without attaching it to a state or machine.</td></tr>
</tbody></table>

<div class="api-method-entry" id="statement-transition-rule-get-target-name">
  <div class="api-method-name">GetTargetName()</div>
  <p class="api-method-summary">Returns this rule&#x27;s destination state name.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-rule-set-priority">
  <div class="api-method-name">SetPriority(priority)</div>
  <p class="api-method-summary">Sets the rule priority. Higher values are checked first within the same phase.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">priority</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">The new rule priority.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-rule">StatementTransitionRule</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-rule-get-priority">
  <div class="api-method-name">GetPriority()</div>
  <p class="api-method-summary">Returns this rule&#x27;s evaluation priority.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-rule-set-phase">
  <div class="api-method-name">SetPhase(phase)</div>
  <p class="api-method-summary">Sets whether the rule is checked before or after the active state&#x27;s Update handler.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">phase</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-statement-transition-phase"><code>eStatementTransitionPhase</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-rule">StatementTransitionRule</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-rule-get-phase">
  <div class="api-method-name">GetPhase()</div>
  <p class="api-method-summary">Returns when the rule is checked automatically.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-rule-set-enabled">
  <div class="api-method-name">SetEnabled(enabled)</div>
  <p class="api-method-summary">Enables or disables the rule without removing it.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">enabled</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether this rule should participate in evaluation.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-rule">StatementTransitionRule</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-rule-is-enabled">
  <div class="api-method-name">IsEnabled()</div>
  <p class="api-method-summary">Checks whether the rule is currently enabled.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-rule-set-force">
  <div class="api-method-name">SetForce([force])</div>
  <p class="api-method-summary">Sets whether the rule ignores exit locks and guards when it fires.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">force <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether the rule should force its transition. Defaults to true.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-rule">StatementTransitionRule</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-rule-is-forced">
  <div class="api-method-name">IsForced()</div>
  <p class="api-method-summary">Checks whether the rule ignores exit restrictions when it fires.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-rule-set-data">
  <div class="api-method-name">SetData(data)</div>
  <p class="api-method-summary">Sets a fixed payload for the rule and removes any payload function.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">data</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The fixed transition payload.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-rule">StatementTransitionRule</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-rule-set-data-provider">
  <div class="api-method-name">SetDataProvider(function)</div>
  <p class="api-method-summary">Sets a function that creates the payload only when the rule fires. It is called as fn(state, rule).</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">function</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">Function used to create the payload when the rule fires.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-rule">StatementTransitionRule</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-rule-get-data">
  <div class="api-method-name">GetData()</div>
  <p class="api-method-summary">Returns the fixed payload. Payload functions only run when the rule fires.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-rule-remove">
  <div class="api-method-name">Remove()</div>
  <p class="api-method-summary">Removes the rule from its state or machine.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-rule">StatementTransitionRule</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-rule-clone">
  <div class="api-method-name">Clone()</div>
  <p class="api-method-summary">Creates a copy of the rule without attaching it to a state or machine.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-transition-rule">StatementTransitionRule</a></span>
    </div>
  </div>
</div>

### StatementTransitionResult
{: #statement-transition-result .api-type-title }

Stores the result of a state transition.

#### Methods

<div class="api-method-group-title">Status</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-transition-result-succeeded"><code>Succeeded()</code></a></td><td>Checks whether the transition finished successfully.</td></tr>
<tr><td><a href="#statement-transition-result-blocked"><code>Blocked()</code></a></td><td>Checks whether the transition finished without changing state.</td></tr>
<tr><td><a href="#statement-transition-result-is-pending"><code>IsPending()</code></a></td><td>Checks whether the transition is still being processed.</td></tr>
<tr><td><a href="#statement-transition-result-get-block-reason"><code>GetBlockReason()</code></a></td><td>Returns why the transition did not happen.</td></tr>
<tr><td><a href="#statement-transition-result-get-block-detail"><code>GetBlockDetail()</code></a></td><td>Returns extra information about why the transition was blocked.</td></tr>
</tbody></table>

<div class="api-method-group-title">Source and destination</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-transition-result-get-from-state"><code>GetFromState()</code></a></td><td>Returns the state that was active when the transition started.</td></tr>
<tr><td><a href="#statement-transition-result-get-from-name"><code>GetFromName()</code></a></td><td>Returns the name of the state that was active when the transition started.</td></tr>
<tr><td><a href="#statement-transition-result-get-to-state"><code>GetToState()</code></a></td><td>Returns the state entered by the transition.</td></tr>
<tr><td><a href="#statement-transition-result-get-to-name"><code>GetToName()</code></a></td><td>Returns the name of the state entered by the transition.</td></tr>
<tr><td><a href="#statement-transition-result-get-target-state"><code>GetTargetState()</code></a></td><td>Returns the final target state, even if the transition was blocked.</td></tr>
<tr><td><a href="#statement-transition-result-get-target-name"><code>GetTargetName()</code></a></td><td>Returns the final target state name after any redirect.</td></tr>
</tbody></table>

<div class="api-method-group-title">Request context</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-transition-result-get-machine"><code>GetMachine()</code></a></td><td>Returns the machine that handled this transition.</td></tr>
<tr><td><a href="#statement-transition-result-get-requested-name"><code>GetRequestedName()</code></a></td><td>Returns the state name originally requested.</td></tr>
<tr><td><a href="#statement-transition-result-get-tick"><code>GetTick()</code></a></td><td>Returns the debug tick for this transition, or -1 if none was recorded.</td></tr>
<tr><td><a href="#statement-transition-result-get-data"><code>GetData()</code></a></td><td>Returns the transition payload.</td></tr>
<tr><td><a href="#statement-transition-result-was-forced"><code>WasForced()</code></a></td><td>Checks whether the original transition request bypassed exit restrictions.</td></tr>
<tr><td><a href="#statement-transition-result-get-cause"><code>GetCause()</code></a></td><td>Returns what started this transition.</td></tr>
<tr><td><a href="#statement-transition-result-was-redirected"><code>WasRedirected()</code></a></td><td>Checks whether Exit code or a transition hook changed the destination before the transition finished.</td></tr>
<tr><td><a href="#statement-transition-result-get-redirect-count"><code>GetRedirectCount()</code></a></td><td>Returns how many times the destination changed before the transition finished.</td></tr>
</tbody></table>

<div class="api-method-entry" id="statement-transition-result-succeeded">
  <div class="api-method-name">Succeeded()</div>
  <p class="api-method-summary">Checks whether the transition finished successfully.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-blocked">
  <div class="api-method-name">Blocked()</div>
  <p class="api-method-summary">Checks whether the transition finished without changing state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-is-pending">
  <div class="api-method-name">IsPending()</div>
  <p class="api-method-summary">Checks whether the transition is still being processed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-get-block-reason">
  <div class="api-method-name">GetBlockReason()</div>
  <p class="api-method-summary">Returns why the transition did not happen.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-get-block-detail">
  <div class="api-method-name">GetBlockDetail()</div>
  <p class="api-method-summary">Returns extra information about why the transition was blocked.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-get-machine">
  <div class="api-method-name">GetMachine()</div>
  <p class="api-method-summary">Returns the machine that handled this transition.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement">Statement</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-get-from-state">
  <div class="api-method-name">GetFromState()</div>
  <p class="api-method-summary">Returns the state that was active when the transition started.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-get-from-name">
  <div class="api-method-name">GetFromName()</div>
  <p class="api-method-summary">Returns the name of the state that was active when the transition started.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-get-to-state">
  <div class="api-method-name">GetToState()</div>
  <p class="api-method-summary">Returns the state entered by the transition.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-get-to-name">
  <div class="api-method-name">GetToName()</div>
  <p class="api-method-summary">Returns the name of the state entered by the transition.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-get-requested-name">
  <div class="api-method-name">GetRequestedName()</div>
  <p class="api-method-summary">Returns the state name originally requested.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-get-target-state">
  <div class="api-method-name">GetTargetState()</div>
  <p class="api-method-summary">Returns the final target state, even if the transition was blocked.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-get-target-name">
  <div class="api-method-name">GetTargetName()</div>
  <p class="api-method-summary">Returns the final target state name after any redirect.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-get-tick">
  <div class="api-method-name">GetTick()</div>
  <p class="api-method-summary">Returns the debug tick for this transition, or -1 if none was recorded.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-get-data">
  <div class="api-method-name">GetData()</div>
  <p class="api-method-summary">Returns the transition payload.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-was-forced">
  <div class="api-method-name">WasForced()</div>
  <p class="api-method-summary">Checks whether the original transition request bypassed exit restrictions.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-get-cause">
  <div class="api-method-name">GetCause()</div>
  <p class="api-method-summary">Returns what started this transition.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-was-redirected">
  <div class="api-method-name">WasRedirected()</div>
  <p class="api-method-summary">Checks whether Exit code or a transition hook changed the destination before the transition finished.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-transition-result-get-redirect-count">
  <div class="api-method-name">GetRedirectCount()</div>
  <p class="api-method-summary">Returns how many times the destination changed before the transition finished.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

## Templates and custom events

### StatementStateTemplate
{: #statement-state-template .api-type-title }

Defines a reusable template for building <a href="#statement-state"><code>StatementState</code></a> instances.

```gml
new StatementStateTemplate(name)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The template name/tag value and default state name.</span>
    </div>
  </div>
</div>

#### Methods

<div class="api-method-group-title">Config</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-state-template-set-config-clone"><code>SetConfigClone()</code></a></td><td>Controls whether config data is deep-cloned when this template builds a state.</td></tr>
</tbody></table>

<div class="api-method-group-title">Handlers and events</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-state-template-add-state-event"><code>AddStateEvent()</code></a></td><td>Stores a handler for a built-in event or custom <a href="#statement-event"><code>StatementEvent</code></a>. The handler is bound to the state owner when the state is built.</td></tr>
<tr><td><a href="#statement-state-template-add-enter"><code>AddEnter()</code></a></td><td>Adds an Enter handler to states built from this template.</td></tr>
<tr><td><a href="#statement-state-template-add-update"><code>AddUpdate()</code></a></td><td>Adds an Update handler to states built from this template.</td></tr>
<tr><td><a href="#statement-state-template-add-exit"><code>AddExit()</code></a></td><td>Adds an Exit handler to states built from this template.</td></tr>
<tr><td><a href="#statement-state-template-add-draw"><code>AddDraw()</code></a></td><td>Adds a Draw handler to states built from this template.</td></tr>
</tbody></table>

<div class="api-method-group-title">Transition rules</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-state-template-add-transition"><code>AddTransition()</code></a></td><td>Adds a reusable transition rule to this template.</td></tr>
<tr><td><a href="#statement-state-template-remove-transition"><code>RemoveTransition()</code></a></td><td>Removes a specific transition rule from this template.</td></tr>
<tr><td><a href="#statement-state-template-clear-transitions"><code>ClearTransitions()</code></a></td><td>Removes all transition rules from this template.</td></tr>
</tbody></table>

<div class="api-method-group-title">Debug metadata</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-state-template-debug-link-to"><code>DebugLinkTo()</code></a></td><td>Declares a debug-only visual connection copied into each built state.</td></tr>
<tr><td><a href="#statement-state-template-debug-payload"><code>DebugPayload()</code></a></td><td>Sets the default debug-jump payload copied into each built state.</td></tr>
<tr><td><a href="#statement-state-template-debug-break-on-enter"><code>DebugBreakOnEnter()</code></a></td><td>Controls whether built states pause debug execution when entered.</td></tr>
<tr><td><a href="#statement-state-template-debug-tag"><code>DebugTag()</code></a></td><td>Assigns the debug tag copied into each built state.</td></tr>
</tbody></table>

<div class="api-method-group-title">Build</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-state-template-build"><code>Build()</code></a></td><td>Builds a new <a href="#statement-state"><code>StatementState</code></a> from this template without coercing an overridden state name to a string.</td></tr>
</tbody></table>

<div class="api-method-entry" id="statement-state-template-set-config-clone">
  <div class="api-method-name">SetConfigClone(enabled)</div>
  <p class="api-method-summary">Controls whether config data is deep-cloned when this template builds a state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">enabled</span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether built states should clone supplied config by default.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state-template">StatementStateTemplate</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-template-add-state-event">
  <div class="api-method-name">AddStateEvent(event, function, [mode])</div>
  <p class="api-method-summary">Stores a handler for a built-in event or custom <a href="#statement-event"><code>StatementEvent</code></a>. The handler is bound to the state owner when the state is built.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">event</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">A built-in <a href="#enum-e-statement-events"><code>eStatementEvents</code></a> value or <a href="#statement-event"><code>StatementEvent</code></a> identity.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">function</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">The handler function copied into each built state.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">mode <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-statement-bind-mode"><code>eStatementBindMode</code></a> enum. Defaults to REPLACE.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state-template">StatementStateTemplate</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-template-add-enter">
  <div class="api-method-name">AddEnter(function, [mode])</div>
  <p class="api-method-summary">Adds an Enter handler to states built from this template.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">function</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">The Enter handler copied into built states.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">mode <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-statement-bind-mode"><code>eStatementBindMode</code></a> enum. Defaults to REPLACE.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state-template">StatementStateTemplate</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-template-add-update">
  <div class="api-method-name">AddUpdate(function, [mode])</div>
  <p class="api-method-summary">Adds an Update handler to states built from this template.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">function</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">The Update handler copied into built states.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">mode <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-statement-bind-mode"><code>eStatementBindMode</code></a> enum. Defaults to REPLACE.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state-template">StatementStateTemplate</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-template-add-exit">
  <div class="api-method-name">AddExit(function, [mode])</div>
  <p class="api-method-summary">Adds an Exit handler to states built from this template.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">function</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">The Exit handler copied into built states.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">mode <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-statement-bind-mode"><code>eStatementBindMode</code></a> enum. Defaults to REPLACE.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state-template">StatementStateTemplate</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-template-add-draw">
  <div class="api-method-name">AddDraw(function, [mode])</div>
  <p class="api-method-summary">Adds a Draw handler to states built from this template.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">function</span>
      <span class="api-argument-type">Function</span>
      <span class="api-argument-description">The Draw handler copied into built states.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">mode <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-statement-bind-mode"><code>eStatementBindMode</code></a> enum. Defaults to REPLACE.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state-template">StatementStateTemplate</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-template-add-transition">
  <div class="api-method-name">AddTransition(rule)</div>
  <p class="api-method-summary">Adds a reusable transition rule to this template.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">rule</span>
      <span class="api-argument-type">Struct.<a href="#statement-transition-rule">StatementTransitionRule</a></span>
      <span class="api-argument-description">The unattached rule to store in this template.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state-template">StatementStateTemplate</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-template-remove-transition">
  <div class="api-method-name">RemoveTransition(rule)</div>
  <p class="api-method-summary">Removes a specific transition rule from this template.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">rule</span>
      <span class="api-argument-type">Struct.<a href="#statement-transition-rule">StatementTransitionRule</a></span>
      <span class="api-argument-description">The rule to remove.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state-template">StatementStateTemplate</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-template-clear-transitions">
  <div class="api-method-name">ClearTransitions()</div>
  <p class="api-method-summary">Removes all transition rules from this template.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state-template">StatementStateTemplate</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-template-debug-link-to">
  <div class="api-method-name">DebugLinkTo(target_name)</div>
  <p class="api-method-summary">Declares a debug-only visual connection copied into each built state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">target_name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The state name shown as the connection destination.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state-template">StatementStateTemplate</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-template-debug-payload">
  <div class="api-method-name">DebugPayload(payload)</div>
  <p class="api-method-summary">Sets the default debug-jump payload copied into each built state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">payload</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">The debug payload.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state-template">StatementStateTemplate</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-template-debug-break-on-enter">
  <div class="api-method-name">DebugBreakOnEnter([break_on_enter])</div>
  <p class="api-method-summary">Controls whether built states pause debug execution when entered.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">break_on_enter <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether built states should break on Enter. Defaults to true.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state-template">StatementStateTemplate</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-template-debug-tag">
  <div class="api-method-name">DebugTag(tag)</div>
  <p class="api-method-summary">Assigns the debug tag copied into each built state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">tag</span>
      <span class="api-argument-type">String</span>
      <span class="api-argument-description">The debug tag value.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state-template">StatementStateTemplate</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-state-template-build">
  <div class="api-method-name">Build(owner, [config], [name], [clone])</div>
  <p class="api-method-summary">Builds a new <a href="#statement-state"><code>StatementState</code></a> from this template without coercing an overridden state name to a string.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">owner</span>
      <span class="api-argument-type">Id.Instance,Struct</span>
      <span class="api-argument-description">The instance or struct the built state belongs to.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">config <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional config assigned to the built state.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">name <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Optional state name/tag override. The supplied value is preserved exactly.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">clone <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Optional override for config cloning.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-state">StatementState</a>,Undefined</span>
    </div>
  </div>
</div>

### StatementEvent
{: #statement-event .api-type-title }

Creates a named custom state event.

```gml
new StatementEvent(name)
```

<div class="api-constructor-meta">
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">Name shown in debug tools.</span>
    </div>
  </div>
</div>

#### Methods

<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>
<tr><td><a href="#statement-event-get-name"><code>GetName()</code></a></td><td>Returns this event&#x27;s friendly name.</td></tr>
</tbody></table>

<div class="api-method-entry" id="statement-event-get-name">
  <div class="api-method-name">GetName()</div>
  <p class="api-method-summary">Returns this event&#x27;s friendly name.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Any</span>
    </div>
  </div>
</div>

## Statement Lens

### StatementLens
{: #statement-lens .api-type-title }

Stores <a href="#statement"><code>Statement</code></a> Lens selection, saved views, caches, and per-frame state.

#### Methods

<div class="api-method-group-title">Machine selection</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-lens-set-machine"><code>SetMachine()</code></a></td><td>Selects a live <a href="#statement"><code>Statement</code></a> machine and resets selection to its current state.</td></tr>
<tr><td><a href="#statement-lens-select-machine-overview"><code>SelectMachineOverview()</code></a></td><td>Selects the machine overview page.</td></tr>
<tr><td><a href="#statement-lens-select-relative-machine"><code>SelectRelativeMachine()</code></a></td><td>Selects the previous or next live machine in the current picker filter.</td></tr>
</tbody></table>

<div class="api-method-group-title">State and connection selection</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-lens-select-state"><code>SelectState()</code></a></td><td>Selects a state for inspection without mutating the running machine.</td></tr>
</tbody></table>

<div class="api-method-group-title">View and search</div>
<table class="api-methods"><tbody>
<tr><td><a href="#statement-lens-set-layout"><code>SetLayout()</code></a></td><td>Changes graph layout and restores its per-machine camera.</td></tr>
<tr><td><a href="#statement-lens-save-current-view"><code>SaveCurrentView()</code></a></td><td>Saves the current session view for the selected machine.</td></tr>
<tr><td><a href="#statement-lens-load-saved-view"><code>LoadSavedView()</code></a></td><td>Loads a named session view for the selected machine.</td></tr>
</tbody></table>

<div class="api-method-entry" id="statement-lens-set-machine">
  <div class="api-method-name">SetMachine(machine)</div>
  <p class="api-method-summary">Selects a live <a href="#statement"><code>Statement</code></a> machine and resets selection to its current state.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">machine</span>
      <span class="api-argument-type">Struct.<a href="#statement">Statement</a></span>
      <span class="api-argument-description">Machine to inspect.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-lens">StatementLens</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-lens-select-state">
  <div class="api-method-name">SelectState(state_name, [centre])</div>
  <p class="api-method-summary">Selects a state for inspection without mutating the running machine.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">state_name</span>
      <span class="api-argument-type">Any</span>
      <span class="api-argument-description">State name/tag value to select.</span>
    </div>
    <div class="api-argument">
      <span class="api-argument-name">centre <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether to centre the graph on the state.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-lens">StatementLens</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-lens-select-machine-overview">
  <div class="api-method-name">SelectMachineOverview()</div>
  <p class="api-method-summary">Selects the machine overview page.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-lens">StatementLens</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-lens-set-layout">
  <div class="api-method-name">SetLayout(layout)</div>
  <p class="api-method-summary">Changes graph layout and restores its per-machine camera.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">layout</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Uses the <a href="#enum-e-statement-lens-layout"><code>eStatementLensLayout</code></a> enum.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-lens">StatementLens</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-lens-select-relative-machine">
  <div class="api-method-name">SelectRelativeMachine(direction)</div>
  <p class="api-method-summary">Selects the previous or next live machine in the current picker filter.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">direction</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Negative selects previous. positive selects next.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-lens">StatementLens</a></span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-lens-save-current-view">
  <div class="api-method-name">SaveCurrentView()</div>
  <p class="api-method-summary">Saves the current session view for the selected machine.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">String</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-lens-load-saved-view">
  <div class="api-method-name">LoadSavedView(index)</div>
  <p class="api-method-summary">Loads a named session view for the selected machine.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">index</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">Saved-view index.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Bool</span>
    </div>
  </div>
</div>

## Top-level functions

### Update scheduling
{: .api-function-subsection-title .api-function-subsection-title-first }

<div class="api-method-entry" id="statement-set-update-mode">
  <div class="api-method-name">StatementSetUpdateMode(mode)</div>
  <p class="api-method-summary">Sets how externally driven <a href="#statement"><code>Statement</code></a> machines turn Update calls into update credit.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">mode</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">A value from <a href="#enum-e-statement-update-mode"><code>eStatementUpdateMode</code></a>.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#statement-get-update-mode"><code>StatementGetUpdateMode</code></a> <span aria-hidden="true">·</span> <a href="#enum-e-statement-update-mode"><code>eStatementUpdateMode</code></a> <span aria-hidden="true">·</span> <a href="{{ '/statement/timing-pause-and-updates' | relative_url }}">Timing, Pause &amp; Update Behaviour</a></div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-update-mode">
  <div class="api-method-name">StatementGetUpdateMode()</div>
  <p class="api-method-summary">Gets the global <a href="#statement"><code>Statement</code></a> update mode.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-set-global-time-scale">
  <div class="api-method-name">StatementSetGlobalTimeScale(scale)</div>
  <p class="api-method-summary">Sets the global update scale for externally driven root <a href="#statement"><code>Statement</code></a> machines.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">scale</span>
      <span class="api-argument-type">Real</span>
      <span class="api-argument-description">The new global update scale. Values below zero are clamped to zero.</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-get-global-time-scale">
  <div class="api-method-name">StatementGetGlobalTimeScale()</div>
  <p class="api-method-summary">Gets the global update scale for externally driven root <a href="#statement"><code>Statement</code></a> machines.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

### Statement Lens
{: .api-function-subsection-title }

<div class="api-method-entry" id="statement-lens-get">
  <div class="api-method-name">StatementLensGet()</div>
  <p class="api-method-summary">Returns the startup-owned <a href="#statement"><code>Statement</code></a> Lens view model.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.<a href="#statement-lens">StatementLens</a>,Undefined</span>
    </div>
  </div>
</div>

<div class="api-method-entry" id="statement-lens-update">
  <div class="api-method-name">StatementLensUpdate()</div>
  <p class="api-method-summary">Updates <a href="#statement"><code>Statement</code></a> Lens manually until its automatic handler has started.</p>
</div>

<div class="api-method-entry" id="statement-lens-open">
  <div class="api-method-name">StatementLensOpen(ui_root)</div>
  <p class="api-method-summary">Creates or reveals the <a href="#statement"><code>Statement</code></a> Lens window and ensures its automatic updates are running.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">ui_root</span>
      <span class="api-argument-type">Struct.EchoChamberRoot</span>
      <span class="api-argument-description">Echo Chamber root that owns the desktop.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Struct.EchoChamberWindow,Undefined</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">See also</div>
    <div class="api-see-also"><a href="#statement-lens-get"><code>StatementLensGet</code></a> <span aria-hidden="true">·</span> <a href="{{ '/statement/visual-debugger-guide' | relative_url }}">Statement Lens</a></div>
  </div>
</div>

<div class="api-method-entry" id="statement-debug-prune-registry">
  <div class="api-method-name">StatementDebugPruneRegistry([prune_destroyed_owners])</div>
  <p class="api-method-summary">Removes dead debug entries and can also remove machines whose instance owner was destroyed.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Arguments</div>
    <div class="api-argument">
      <span class="api-argument-name">prune_destroyed_owners <span class="api-optional">optional</span></span>
      <span class="api-argument-type">Bool</span>
      <span class="api-argument-description">Whether destroyed instance owners should be removed.</span>
    </div>
  </div>
  <div class="api-detail-section">
    <div class="api-detail-heading">Returns</div>
    <div class="api-return-row api-return-only">
      <span class="api-return-type">Real</span>
    </div>
  </div>
</div>

## Enums

### Events and handlers
{: .api-function-subsection-title .api-function-subsection-title-first }

<div class="api-enum-entry" id="enum-e-statement-events">
  <div class="api-enum-name">eStatementEvents</div>
  <p class="api-enum-summary">Built-in state events used by lifecycle handlers, AddStateEvent(), and RunState().</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">ENTER</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">EXIT</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">STEP</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">DRAW</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-statement-event-dispatch">
  <div class="api-enum-name">eStatementEventDispatch</div>
  <p class="api-enum-summary">Controls how RunState() dispatches an event through the active submachine hierarchy.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">CURRENT</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">DEEPEST</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">PATH</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-statement-bind-mode">
  <div class="api-enum-name">eStatementBindMode</div>
  <p class="api-enum-summary">Controls how a newly bound state-event handler combines with an existing handler.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">REPLACE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">APPEND</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">PREPEND</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

### Transitions and queues
{: .api-function-subsection-title }

<div class="api-enum-entry" id="enum-e-statement-transition-cause">
  <div class="api-enum-name">eStatementTransitionCause</div>
  <p class="api-enum-summary">Identifies which operation initiated a <a href="#statement"><code>Statement</code></a> transition result.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">START</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">STOP</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">DIRECT</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">DECLARATIVE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">QUEUED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">PUSH</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">POP</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">PREVIOUS</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">REENTER</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">DEBUG_JUMP</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-statement-transition-block-reason">
  <div class="api-enum-name">eStatementTransitionBlockReason</div>
  <p class="api-enum-summary">Explains why a <a href="#statement"><code>Statement</code></a> transition request did not commit.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NONE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">RUNTIME_STOPPING</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">TARGET_MISSING</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">SAME_STATE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">EXIT_LOCKED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">EXIT_GUARD</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">ALREADY_RUNNING</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NO_INITIAL_STATE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NO_ACTIVE_STATE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NO_QUEUED_STATE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">STACK_EMPTY</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NO_PREVIOUS_STATE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-statement-transition-phase">
  <div class="api-enum-name">eStatementTransitionPhase</div>
  <p class="api-enum-summary">Controls whether an automatic transition rule is evaluated before or after the active state Update handler.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">BEFORE_UPDATE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">AFTER_UPDATE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-statement-queue-phase">
  <div class="api-enum-name">eStatementQueuePhase</div>
  <p class="api-enum-summary">Controls when queued transition requests are processed automatically.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">BEFORE_UPDATE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">AFTER_UPDATE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">MANUAL</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

### Runtime and submachines
{: .api-function-subsection-title }

<div class="api-enum-entry" id="enum-e-statement-update-mode">
  <div class="api-enum-name">eStatementUpdateMode</div>
  <p class="api-enum-summary">Controls how externally driven <a href="#statement"><code>Statement</code></a> Update calls accumulate logical update credit.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">EVENT</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">ELAPSED_TIME</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-statement-reset-mode">
  <div class="api-enum-name">eStatementResetMode</div>
  <p class="api-enum-summary">Controls how a hosted submachine is reset or remembered across host-state lifecycle changes.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">RESET_ON_EXIT</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">REMEMBER</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">RESET_ON_ENTER</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

### Debugging
{: .api-function-subsection-title }

<div class="api-enum-entry" id="enum-e-statement-debug-pause-reason">
  <div class="api-enum-name">eStatementDebugPauseReason</div>
  <p class="api-enum-summary">Identifies why a machine is paused by <a href="#statement"><code>Statement</code></a> debug tooling.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NONE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">MANUAL</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">STATE_BREAKPOINT</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">CONNECTION_BREAKPOINT</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">STATE_ERROR</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">CONNECTION_ERROR</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-statement-error-behavior">
  <div class="api-enum-name">eStatementErrorBehavior</div>
  <p class="api-enum-summary">Controls how <a href="#statement"><code>Statement</code></a> debug handling reacts to caught state or transition errors.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">PAUSE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">RETHROW</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

### Statement Lens
{: .api-function-subsection-title }

<div class="api-enum-entry" id="enum-e-statement-lens-selection-kind">
  <div class="api-enum-name">eStatementLensSelectionKind</div>
  <p class="api-enum-summary">Identifies the kind of item currently selected in <a href="#statement"><code>Statement</code></a> Lens.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">MACHINE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">STATE</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">CONNECTION</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-statement-lens-layout">
  <div class="api-enum-name">eStatementLensLayout</div>
  <p class="api-enum-summary">Selects the graph layout used by <a href="#statement"><code>Statement</code></a> Lens.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">LAYERED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">RADIAL</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">CLUSTERED</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NEIGHBOURHOOD</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

<div class="api-enum-entry" id="enum-e-statement-lens-activity">
  <div class="api-enum-name">eStatementLensActivity</div>
  <p class="api-enum-summary">Selects the runtime activity metric visualised by <a href="#statement"><code>Statement</code></a> Lens.</p>
  <div class="api-detail-section api-enum-values">
    <div class="api-detail-heading">Values</div>
    <div class="api-enum-members">
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">OFF</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">TOTAL_ACTIVE_TIME</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">ENTRIES</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">RECENT_ACTIVITY</span>
      </div>
      <div class="api-enum-row api-enum-row-compact">
        <span class="api-enum-member">NUM</span>
      </div>
    </div>
  </div>
</div>

## Macros

### Version
{: .api-function-subsection-title .api-function-subsection-title-first }

<div class="api-method-entry api-macro-entry api-macro-metadata" id="macro-statement-version">
  <div class="api-method-name">STATEMENT_VERSION</div>
  <p class="api-method-summary">Current <a href="#statement"><code>Statement</code></a> package version.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Value</div>
    <pre class="api-example"><code>&quot;3.0.0&quot;</code></pre>
  </div>
</div>

### Core settings
{: .api-function-subsection-title }

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-statement-debug">
  <div class="api-method-name">STATEMENT_DEBUG</div>
  <p class="api-method-summary">Controls whether <a href="#statement"><code>Statement</code></a> debug tracking and <a href="#statement"><code>Statement</code></a> Lens support are enabled.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>1</code></pre>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-statement-max-updates-per-call">
  <div class="api-method-name">STATEMENT_MAX_UPDATES_PER_CALL</div>
  <p class="api-method-summary">Maximum number of logical updates one machine can process during a single Update call when catch-up credit accumulates.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>8</code></pre>
  </div>
</div>

### Statement Lens settings
{: .api-function-subsection-title }

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-statement-lens-graph-pan-button">
  <div class="api-method-name">STATEMENT_LENS_GRAPH_PAN_BUTTON</div>
  <p class="api-method-summary">Mouse button used to pan the <a href="#statement"><code>Statement</code></a> Lens graph.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>mb_middle</code></pre>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-statement-lens-state-card-name-limit">
  <div class="api-method-name">STATEMENT_LENS_STATE_CARD_NAME_LIMIT</div>
  <p class="api-method-summary">Maximum number of characters shown in a <a href="#statement"><code>Statement</code></a> Lens state-card name before it is truncated.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>24</code></pre>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-statement-lens-bind-close-inspector">
  <div class="api-method-name">STATEMENT_LENS_BIND_CLOSE_INSPECTOR</div>
  <p class="api-method-summary">Default Echo Chamber input binding used to close a <a href="#statement"><code>Statement</code></a> Lens inspector.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(vk_escape)</code></pre>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-statement-lens-bind-prev-machine">
  <div class="api-method-name">STATEMENT_LENS_BIND_PREV_MACHINE</div>
  <p class="api-method-summary">Default Echo Chamber input binding used to select the previous machine in <a href="#statement"><code>Statement</code></a> Lens.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(vk_pageup)</code></pre>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-statement-lens-bind-next-machine">
  <div class="api-method-name">STATEMENT_LENS_BIND_NEXT_MACHINE</div>
  <p class="api-method-summary">Default Echo Chamber input binding used to select the next machine in <a href="#statement"><code>Statement</code></a> Lens.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(vk_pagedown)</code></pre>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-statement-lens-bind-open-search-palette">
  <div class="api-method-name">STATEMENT_LENS_BIND_OPEN_SEARCH_PALETTE</div>
  <p class="api-method-summary">Default Echo Chamber input binding used to open the <a href="#statement"><code>Statement</code></a> Lens search palette.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(ord(&quot;F&quot;), eEchoChamberInputCheck.PRESSED, true)</code></pre>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-statement-lens-bind-close-search-palette">
  <div class="api-method-name">STATEMENT_LENS_BIND_CLOSE_SEARCH_PALETTE</div>
  <p class="api-method-summary">Default Echo Chamber input binding used to close the <a href="#statement"><code>Statement</code></a> Lens search palette.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(vk_escape)</code></pre>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-statement-lens-bind-scroll-up-search-palette">
  <div class="api-method-name">STATEMENT_LENS_BIND_SCROLL_UP_SEARCH_PALETTE</div>
  <p class="api-method-summary">Default Echo Chamber input binding used to move upward through <a href="#statement"><code>Statement</code></a> Lens search results.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(vk_up)</code></pre>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-statement-lens-bind-scroll-down-search-palette">
  <div class="api-method-name">STATEMENT_LENS_BIND_SCROLL_DOWN_SEARCH_PALETTE</div>
  <p class="api-method-summary">Default Echo Chamber input binding used to move downward through <a href="#statement"><code>Statement</code></a> Lens search results.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(vk_down)</code></pre>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-statement-lens-bind-accept-search-palette">
  <div class="api-method-name">STATEMENT_LENS_BIND_ACCEPT_SEARCH_PALETTE</div>
  <p class="api-method-summary">Default Echo Chamber input binding used to accept the selected <a href="#statement"><code>Statement</code></a> Lens search result.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(vk_enter)</code></pre>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-statement-lens-bind-fit-graph">
  <div class="api-method-name">STATEMENT_LENS_BIND_FIT_GRAPH</div>
  <p class="api-method-summary">Default Echo Chamber input binding used to fit the <a href="#statement"><code>Statement</code></a> Lens graph to its visible contents.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(ord(&quot;F&quot;))</code></pre>
  </div>
</div>

<div class="api-method-entry api-macro-entry api-macro-setting" id="macro-statement-lens-bind-select-active">
  <div class="api-method-name">STATEMENT_LENS_BIND_SELECT_ACTIVE</div>
  <p class="api-method-summary">Default Echo Chamber input binding used to select the currently active state in <a href="#statement"><code>Statement</code></a> Lens.</p>
  <div class="api-detail-section">
    <div class="api-detail-heading">Default</div>
    <pre class="api-example"><code>new EchoChamberInputBindingKey(ord(&quot;A&quot;))</code></pre>
  </div>
</div>

## Symbol index

<div class="api-symbol-index">
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">A</div>
    <div class="api-symbol-row"><a href="#statement-add-any-enter-hook"><code>AddAnyEnterHook()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-add-any-exit-hook"><code>AddAnyExitHook()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-add-any-transition-hook"><code>AddAnyTransitionHook()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-state-add-draw"><code>AddDraw()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-template-add-draw"><code>AddDraw()</code></a> <span class="api-symbol-owner">| StatementStateTemplate</span></div>
    <div class="api-symbol-row"><a href="#statement-state-add-enter"><code>AddEnter()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-template-add-enter"><code>AddEnter()</code></a> <span class="api-symbol-owner">| StatementStateTemplate</span></div>
    <div class="api-symbol-row"><a href="#statement-state-add-exit"><code>AddExit()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-template-add-exit"><code>AddExit()</code></a> <span class="api-symbol-owner">| StatementStateTemplate</span></div>
    <div class="api-symbol-row"><a href="#statement-state-add-exit-guard"><code>AddExitGuard()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-add-state"><code>AddState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-state-add-state-event"><code>AddStateEvent()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-template-add-state-event"><code>AddStateEvent()</code></a> <span class="api-symbol-owner">| StatementStateTemplate</span></div>
    <div class="api-symbol-row"><a href="#statement-add-state-template"><code>AddStateTemplate()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-add-transition"><code>AddTransition()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-state-add-transition"><code>AddTransition()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-template-add-transition"><code>AddTransition()</code></a> <span class="api-symbol-owner">| StatementStateTemplate</span></div>
    <div class="api-symbol-row"><a href="#statement-state-add-update"><code>AddUpdate()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-template-add-update"><code>AddUpdate()</code></a> <span class="api-symbol-owner">| StatementStateTemplate</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">B</div>
    <div class="api-symbol-row"><a href="#statement-transition-result-blocked"><code>Blocked()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
    <div class="api-symbol-row"><a href="#statement-state-template-build"><code>Build()</code></a> <span class="api-symbol-owner">| StatementStateTemplate</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">C</div>
    <div class="api-symbol-row"><a href="#statement-change-state"><code>ChangeState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-clear-any-enter-hooks"><code>ClearAnyEnterHooks()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-clear-any-exit-hooks"><code>ClearAnyExitHooks()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-clear-any-transition-hooks"><code>ClearAnyTransitionHooks()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-clear-debug-transition-history"><code>ClearDebugTransitionHistory()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-state-clear-exit-guards"><code>ClearExitGuards()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-clear-exit-locks"><code>ClearExitLocks()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-clear-history"><code>ClearHistory()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-clear-queued-state"><code>ClearQueuedState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-clear-states"><code>ClearStates()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-clear-state-stack"><code>ClearStateStack()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-clear-transitions"><code>ClearTransitions()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-state-clear-transitions"><code>ClearTransitions()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-template-clear-transitions"><code>ClearTransitions()</code></a> <span class="api-symbol-owner">| StatementStateTemplate</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-rule-clone"><code>Clone()</code></a> <span class="api-symbol-owner">| StatementTransitionRule</span></div>
    <div class="api-symbol-row"><a href="#statement-state-create-sub-machine"><code>CreateSubMachine()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">D</div>
    <div class="api-symbol-row"><a href="#statement-state-debug-break-on-enter"><code>DebugBreakOnEnter()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-template-debug-break-on-enter"><code>DebugBreakOnEnter()</code></a> <span class="api-symbol-owner">| StatementStateTemplate</span></div>
    <div class="api-symbol-row"><a href="#statement-debug-describe"><code>DebugDescribe()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-debug-jump-to-state"><code>DebugJumpToState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-state-debug-link-to"><code>DebugLinkTo()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-template-debug-link-to"><code>DebugLinkTo()</code></a> <span class="api-symbol-owner">| StatementStateTemplate</span></div>
    <div class="api-symbol-row"><a href="#statement-debug-pause"><code>DebugPause()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-state-debug-payload"><code>DebugPayload()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-template-debug-payload"><code>DebugPayload()</code></a> <span class="api-symbol-owner">| StatementStateTemplate</span></div>
    <div class="api-symbol-row"><a href="#statement-debug-resume"><code>DebugResume()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-debug-set-error-behavior"><code>DebugSetErrorBehavior()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-debug-set-log-errors-to-file"><code>DebugSetLogErrorsToFile()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-debug-step"><code>DebugStep()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-debug-tag"><code>DebugTag()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-state-debug-tag"><code>DebugTag()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-template-debug-tag"><code>DebugTag()</code></a> <span class="api-symbol-owner">| StatementStateTemplate</span></div>
    <div class="api-symbol-row"><a href="#statement-destroy"><code>Destroy()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-draw"><code>Draw()</code></a> <span class="api-symbol-owner">| Statement</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">E</div>
    <div class="api-symbol-row"><a href="#statement-ensure-state"><code>EnsureState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-evaluate-transitions"><code>EvaluateTransitions()</code></a> <span class="api-symbol-owner">| Statement</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">G</div>
    <div class="api-symbol-row"><a href="#statement-transition-result-get-block-detail"><code>GetBlockDetail()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-result-get-block-reason"><code>GetBlockReason()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-result-get-cause"><code>GetCause()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
    <div class="api-symbol-row"><a href="#statement-get-child-machine"><code>GetChildMachine()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-get-child-state"><code>GetChildState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-state-get-config"><code>GetConfig()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-result-get-data"><code>GetData()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-rule-get-data"><code>GetData()</code></a> <span class="api-symbol-owner">| StatementTransitionRule</span></div>
    <div class="api-symbol-row"><a href="#statement-get-debug-graph"><code>GetDebugGraph()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-get-debug-name"><code>GetDebugName()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-get-debug-pause-reason"><code>GetDebugPauseReason()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-get-debug-state-stats"><code>GetDebugStateStats()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-get-debug-state-stats-for"><code>GetDebugStateStatsFor()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-get-debug-tag"><code>GetDebugTag()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-get-debug-transition-history"><code>GetDebugTransitionHistory()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-state-get-exit-guard-count"><code>GetExitGuardCount()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-get-exit-lock-count"><code>GetExitLockCount()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-result-get-from-name"><code>GetFromName()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-result-get-from-state"><code>GetFromState()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
    <div class="api-symbol-row"><a href="#statement-get-global-time-scale"><code>GetGlobalTimeScale()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-get-history-at"><code>GetHistoryAt()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-get-history-count"><code>GetHistoryCount()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-get-last-transition-data"><code>GetLastTransitionData()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-result-get-machine"><code>GetMachine()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
    <div class="api-symbol-row"><a href="#statement-event-get-name"><code>GetName()</code></a> <span class="api-symbol-owner">| StatementEvent</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-rule-get-phase"><code>GetPhase()</code></a> <span class="api-symbol-owner">| StatementTransitionRule</span></div>
    <div class="api-symbol-row"><a href="#statement-get-previous-state-name"><code>GetPreviousStateName()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-rule-get-priority"><code>GetPriority()</code></a> <span class="api-symbol-owner">| StatementTransitionRule</span></div>
    <div class="api-symbol-row"><a href="#statement-get-queued-state-data"><code>GetQueuedStateData()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-get-queued-state-name"><code>GetQueuedStateName()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-get-queue-phase"><code>GetQueuePhase()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-result-get-redirect-count"><code>GetRedirectCount()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-result-get-requested-name"><code>GetRequestedName()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
    <div class="api-symbol-row"><a href="#statement-get-state"><code>GetState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-get-state-name"><code>GetStateName()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-get-state-stack-depth"><code>GetStateStackDepth()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-get-state-time"><code>GetStateTime()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-state-get-sub-machine"><code>GetSubMachine()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-result-get-target-name"><code>GetTargetName()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-rule-get-target-name"><code>GetTargetName()</code></a> <span class="api-symbol-owner">| StatementTransitionRule</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-result-get-target-state"><code>GetTargetState()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-result-get-tick"><code>GetTick()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
    <div class="api-symbol-row"><a href="#statement-get-time-scale"><code>GetTimeScale()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-result-get-to-name"><code>GetToName()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-result-get-to-state"><code>GetToState()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">H</div>
    <div class="api-symbol-row"><a href="#statement-state-has-exit-guard"><code>HasExitGuard()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-has-exit-lock"><code>HasExitLock()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-has-queued-state"><code>HasQueuedState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-state-has-state-event"><code>HasStateEvent()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-has-sub-machine"><code>HasSubMachine()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">I</div>
    <div class="api-symbol-row"><a href="#statement-is-debug-enabled"><code>IsDebugEnabled()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-is-debug-paused"><code>IsDebugPaused()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-rule-is-enabled"><code>IsEnabled()</code></a> <span class="api-symbol-owner">| StatementTransitionRule</span></div>
    <div class="api-symbol-row"><a href="#statement-state-is-exit-locked"><code>IsExitLocked()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-rule-is-forced"><code>IsForced()</code></a> <span class="api-symbol-owner">| StatementTransitionRule</span></div>
    <div class="api-symbol-row"><a href="#statement-is-in-path"><code>IsInPath()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-is-in-state"><code>IsInState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-is-paused"><code>IsPaused()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-result-is-pending"><code>IsPending()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
    <div class="api-symbol-row"><a href="#statement-is-running"><code>IsRunning()</code></a> <span class="api-symbol-owner">| Statement</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">L</div>
    <div class="api-symbol-row"><a href="#statement-lens-load-saved-view"><code>LoadSavedView()</code></a> <span class="api-symbol-owner">| StatementLens</span></div>
    <div class="api-symbol-row"><a href="#statement-state-lock-exit"><code>LockExit()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-lock-exit-until-sub-in"><code>LockExitUntilSubIn()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-lock-exit-while-sub-not"><code>LockExitWhileSubNot()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">O</div>
    <div class="api-symbol-row"><a href="#statement-state-on-submachine-enter"><code>OnSubmachineEnter()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-on-submachine-exit"><code>OnSubmachineExit()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">P</div>
    <div class="api-symbol-row"><a href="#statement-peek-state-stack"><code>PeekStateStack()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-pop-state"><code>PopState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-previous-state"><code>PreviousState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-print-state-history"><code>PrintStateHistory()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-print-state-names"><code>PrintStateNames()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-process-queued-state"><code>ProcessQueuedState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-push-state"><code>PushState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">Q</div>
    <div class="api-symbol-row"><a href="#statement-queue-state"><code>QueueState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">R</div>
    <div class="api-symbol-row"><a href="#statement-reenter-state"><code>ReenterState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-rule-remove"><code>Remove()</code></a> <span class="api-symbol-owner">| StatementTransitionRule</span></div>
    <div class="api-symbol-row"><a href="#statement-state-remove-exit-guard"><code>RemoveExitGuard()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-remove-state"><code>RemoveState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-remove-transition"><code>RemoveTransition()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-state-remove-transition"><code>RemoveTransition()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-template-remove-transition"><code>RemoveTransition()</code></a> <span class="api-symbol-owner">| StatementStateTemplate</span></div>
    <div class="api-symbol-row"><a href="#statement-reset"><code>Reset()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-run-state"><code>RunState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">S</div>
    <div class="api-symbol-row"><a href="#statement-lens-save-current-view"><code>SaveCurrentView()</code></a> <span class="api-symbol-owner">| StatementLens</span></div>
    <div class="api-symbol-row"><a href="#statement-lens-select-machine-overview"><code>SelectMachineOverview()</code></a> <span class="api-symbol-owner">| StatementLens</span></div>
    <div class="api-symbol-row"><a href="#statement-lens-select-relative-machine"><code>SelectRelativeMachine()</code></a> <span class="api-symbol-owner">| StatementLens</span></div>
    <div class="api-symbol-row"><a href="#statement-lens-select-state"><code>SelectState()</code></a> <span class="api-symbol-owner">| StatementLens</span></div>
    <div class="api-symbol-row"><a href="#statement-state-set-config"><code>SetConfig()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-template-set-config-clone"><code>SetConfigClone()</code></a> <span class="api-symbol-owner">| StatementStateTemplate</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-rule-set-data"><code>SetData()</code></a> <span class="api-symbol-owner">| StatementTransitionRule</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-rule-set-data-provider"><code>SetDataProvider()</code></a> <span class="api-symbol-owner">| StatementTransitionRule</span></div>
    <div class="api-symbol-row"><a href="#statement-set-debug-enabled"><code>SetDebugEnabled()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-set-debug-name"><code>SetDebugName()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-rule-set-enabled"><code>SetEnabled()</code></a> <span class="api-symbol-owner">| StatementTransitionRule</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-rule-set-force"><code>SetForce()</code></a> <span class="api-symbol-owner">| StatementTransitionRule</span></div>
    <div class="api-symbol-row"><a href="#statement-set-history-limit"><code>SetHistoryLimit()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-set-inherit-pause"><code>SetInheritPause()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-set-initial-state"><code>SetInitialState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-lens-set-layout"><code>SetLayout()</code></a> <span class="api-symbol-owner">| StatementLens</span></div>
    <div class="api-symbol-row"><a href="#statement-lens-set-machine"><code>SetMachine()</code></a> <span class="api-symbol-owner">| StatementLens</span></div>
    <div class="api-symbol-row"><a href="#statement-set-paused"><code>SetPaused()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-rule-set-phase"><code>SetPhase()</code></a> <span class="api-symbol-owner">| StatementTransitionRule</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-rule-set-priority"><code>SetPriority()</code></a> <span class="api-symbol-owner">| StatementTransitionRule</span></div>
    <div class="api-symbol-row"><a href="#statement-set-queue-phase"><code>SetQueuePhase()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-set-reset-mode"><code>SetResetMode()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-set-state-time"><code>SetStateTime()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-set-time-scale"><code>SetTimeScale()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-start"><code>Start()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement"><code>Statement</code></a></div>
    <div class="api-symbol-row"><a href="#statement-debug-prune-registry"><code>StatementDebugPruneRegistry()</code></a></div>
    <div class="api-symbol-row"><a href="#statement-event"><code>StatementEvent</code></a></div>
    <div class="api-symbol-row"><a href="#statement-get-global-time-scale"><code>StatementGetGlobalTimeScale()</code></a></div>
    <div class="api-symbol-row"><a href="#statement-get-update-mode"><code>StatementGetUpdateMode()</code></a></div>
    <div class="api-symbol-row"><a href="#statement-lens"><code>StatementLens</code></a></div>
    <div class="api-symbol-row"><a href="#statement-lens-get"><code>StatementLensGet()</code></a></div>
    <div class="api-symbol-row"><a href="#statement-lens-open"><code>StatementLensOpen()</code></a></div>
    <div class="api-symbol-row"><a href="#statement-lens-update"><code>StatementLensUpdate()</code></a></div>
    <div class="api-symbol-row"><a href="#statement-set-global-time-scale"><code>StatementSetGlobalTimeScale()</code></a></div>
    <div class="api-symbol-row"><a href="#statement-set-update-mode"><code>StatementSetUpdateMode()</code></a></div>
    <div class="api-symbol-row"><a href="#statement-state"><code>StatementState</code></a></div>
    <div class="api-symbol-row"><a href="#statement-state-template"><code>StatementStateTemplate</code></a></div>
    <div class="api-symbol-row"><a href="#statement-transition-result"><code>StatementTransitionResult</code></a></div>
    <div class="api-symbol-row"><a href="#statement-transition-rule"><code>StatementTransitionRule</code></a></div>
    <div class="api-symbol-row"><a href="#statement-stop"><code>Stop()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-result-succeeded"><code>Succeeded()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">T</div>
    <div class="api-symbol-row"><a href="#statement-state-timer-get"><code>TimerGet()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-timer-is-running"><code>TimerIsRunning()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-timer-pause"><code>TimerPause()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-timer-resume"><code>TimerResume()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-timer-set"><code>TimerSet()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-timer-start"><code>TimerStart()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-state-timer-stop"><code>TimerStop()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">U</div>
    <div class="api-symbol-row"><a href="#statement-state-unlock-exit"><code>UnlockExit()</code></a> <span class="api-symbol-owner">| StatementState</span></div>
    <div class="api-symbol-row"><a href="#statement-update"><code>Update()</code></a> <span class="api-symbol-owner">| Statement</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">W</div>
    <div class="api-symbol-row"><a href="#statement-transition-result-was-forced"><code>WasForced()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
    <div class="api-symbol-row"><a href="#statement-was-previously-in-state"><code>WasPreviouslyInState()</code></a> <span class="api-symbol-owner">| Statement</span></div>
    <div class="api-symbol-row"><a href="#statement-transition-result-was-redirected"><code>WasRedirected()</code></a> <span class="api-symbol-owner">| StatementTransitionResult</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">Enums</div>
    <div class="api-symbol-row"><a href="#enum-e-statement-bind-mode"><code>eStatementBindMode</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-statement-debug-pause-reason"><code>eStatementDebugPauseReason</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-statement-error-behavior"><code>eStatementErrorBehavior</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-statement-event-dispatch"><code>eStatementEventDispatch</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-statement-events"><code>eStatementEvents</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-statement-lens-activity"><code>eStatementLensActivity</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-statement-lens-layout"><code>eStatementLensLayout</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-statement-lens-selection-kind"><code>eStatementLensSelectionKind</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-statement-queue-phase"><code>eStatementQueuePhase</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-statement-reset-mode"><code>eStatementResetMode</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-statement-transition-block-reason"><code>eStatementTransitionBlockReason</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-statement-transition-cause"><code>eStatementTransitionCause</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-statement-transition-phase"><code>eStatementTransitionPhase</code></a><span class="api-symbol-owner">enum</span></div>
    <div class="api-symbol-row"><a href="#enum-e-statement-update-mode"><code>eStatementUpdateMode</code></a><span class="api-symbol-owner">enum</span></div>
  </div>
  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">Macros</div>
    <div class="api-symbol-row"><a href="#macro-statement-debug"><code>STATEMENT_DEBUG</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-statement-lens-bind-accept-search-palette"><code>STATEMENT_LENS_BIND_ACCEPT_SEARCH_PALETTE</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-statement-lens-bind-close-inspector"><code>STATEMENT_LENS_BIND_CLOSE_INSPECTOR</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-statement-lens-bind-close-search-palette"><code>STATEMENT_LENS_BIND_CLOSE_SEARCH_PALETTE</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-statement-lens-bind-fit-graph"><code>STATEMENT_LENS_BIND_FIT_GRAPH</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-statement-lens-bind-next-machine"><code>STATEMENT_LENS_BIND_NEXT_MACHINE</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-statement-lens-bind-open-search-palette"><code>STATEMENT_LENS_BIND_OPEN_SEARCH_PALETTE</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-statement-lens-bind-prev-machine"><code>STATEMENT_LENS_BIND_PREV_MACHINE</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-statement-lens-bind-scroll-down-search-palette"><code>STATEMENT_LENS_BIND_SCROLL_DOWN_SEARCH_PALETTE</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-statement-lens-bind-scroll-up-search-palette"><code>STATEMENT_LENS_BIND_SCROLL_UP_SEARCH_PALETTE</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-statement-lens-bind-select-active"><code>STATEMENT_LENS_BIND_SELECT_ACTIVE</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-statement-lens-graph-pan-button"><code>STATEMENT_LENS_GRAPH_PAN_BUTTON</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-statement-lens-state-card-name-limit"><code>STATEMENT_LENS_STATE_CARD_NAME_LIMIT</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-statement-max-updates-per-call"><code>STATEMENT_MAX_UPDATES_PER_CALL</code></a><span class="api-symbol-owner">macro</span></div>
    <div class="api-symbol-row"><a href="#macro-statement-version"><code>STATEMENT_VERSION</code></a><span class="api-symbol-owner">macro</span></div>
  </div>
</div>
