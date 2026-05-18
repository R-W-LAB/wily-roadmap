---
description: Mark a Wily phase blocked and record the reason
argument-hint: '<stage-id>/<phase-id> [reason]'
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion
---

Run the `wily-block` skill to record a blocked phase with its reason.

The skill captures the blocking reason on the session and roadmap, then invokes `${CLAUDE_PLUGIN_ROOT}/scripts/wily.py block <stage-id>/<phase-id> <reason>`. Stage ids are not executable in v2. If the user did not supply a reason, ask once before writing.

Board reflection contract: after local `.wily` state changes, reflect Board live/provisional state when configured, record deterministic evidence, and use actual-site visual verification only for failures, mismatches, explicit visual requests, or Board UI/rendering changes.

Arguments (phase id, then free-form reason):

$ARGUMENTS
