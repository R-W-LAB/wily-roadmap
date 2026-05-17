---
description: Mark a Wily phase done and verify its session
argument-hint: '<phase-id>'
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion
---

Run the `wily-complete` skill to finish the requested phase.

Approval is required before flipping a phase to `done`. The skill verifies the phase's session (verification commands, handoff notes) before invoking `${CLAUDE_PLUGIN_ROOT}/scripts/wily.py complete <phase-id>`. Do not remove or rewrite completed history.

Board reflection contract: after local `.wily` state changes, reflect Board live/provisional state when configured, record deterministic evidence, and use actual-site visual verification only for failures, mismatches, explicit visual requests, or Board UI/rendering changes.

Phase id (required):

$ARGUMENTS
