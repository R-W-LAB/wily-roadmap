---
description: Revise the future Wily roadmap and increment its version
argument-hint: '[reason or summary of change]'
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion
---

Run the `wily-replan` skill to revise the future roadmap without rewriting completed history.

Only `pending` / `ready` / `blocked` phases may be reshaped. Completed phases stay intact; replaced or obsoleted phases must be marked `superseded` rather than deleted. Record the change in `revisions/` and invoke `${CLAUDE_PLUGIN_ROOT}/scripts/wily.py replan <reason>` to bump the roadmap version.

Board reflection contract: after local `.wily` state changes, reflect Board live/provisional state when configured, record deterministic evidence, and use actual-site visual verification only for failures, mismatches, explicit visual requests, or Board UI/rendering changes.

Revision reason or summary (may be empty):

$ARGUMENTS
