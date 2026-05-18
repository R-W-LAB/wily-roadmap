---
description: Start a Wily phase session (creates session directory, marks phase in_progress)
argument-hint: '<stage-id>/<phase-id>'
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion
---

Run the `wily-start` skill to begin a session for the requested phase.

The skill owns approval prompts, planner selection, and context bundle creation. Use `${CLAUDE_PLUGIN_ROOT}/scripts/wily.py start <stage-id>/<phase-id>` to create the session directory and flip the Phase to `in_progress`. Stage ids are not executable in v2; use the suggested next ready Phase, `$wily-decompose-stage`, or `wily migrate-state --to wily-roadmap-v2 --dry-run`. Do not execute the phase implementation; the start step only opens the session.

Board reflection contract: after local `.wily` state changes, reflect Board live/provisional state when configured, record deterministic evidence, and use actual-site visual verification only for failures, mismatches, explicit visual requests, or Board UI/rendering changes.

Phase id (required):

$ARGUMENTS
