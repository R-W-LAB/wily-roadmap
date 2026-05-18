---
description: Create the next Wily retry attempt for a phase, preserving previous sessions
argument-hint: '<stage-id>/<phase-id>'
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion
---

Run the `wily-retry` skill to start a new attempt for the requested phase.

The previous session is preserved as history; the new attempt becomes the current session. Use `${CLAUDE_PLUGIN_ROOT}/scripts/wily.py retry <stage-id>/<phase-id>` to create the attempt. Stage ids are not executable in v2. Do not delete or rewrite previous session directories.

Board reflection contract: after local `.wily` state changes, reflect Board live/provisional state when configured, record deterministic evidence, and use actual-site visual verification only for failures, mismatches, explicit visual requests, or Board UI/rendering changes.

Phase ref (required):

$ARGUMENTS
