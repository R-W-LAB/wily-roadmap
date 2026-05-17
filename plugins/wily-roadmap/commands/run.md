---
description: Route a Wily phase to Custom Workflow Skillset without marking the phase done
argument-hint: '<phase-id> [--runner custom-workflow] [--autonomy conservative|goal_scoped|yolo]'
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion
---

Run the `wily-run` skill to route the requested phase to Custom Workflow Skillset.

Use `${CLAUDE_PLUGIN_ROOT}/scripts/wily.py run <phase-id> [--runner custom-workflow] [--autonomy conservative|goal_scoped|yolo]` to prepare Custom Workflow request/result artifacts. Then route the active agent through `custom-workflow-skillset:plan-goal-runner`; use `custom-workflow-skillset:parallel-lane-runner` only when the generated execution package allows bounded parallel lanes. It must not mark the phase `done`; verified completion remains a later `/wily:complete <phase-id>` action. Keep remote and destructive actions approval-first in every autonomy mode.

Board reflection contract: after local `.wily` state changes, reflect Board live/provisional state when configured, sync Custom Workflow checkpoints through `checkpoint-sync`, record deterministic evidence, and use actual-site visual verification only for failures, mismatches, explicit visual requests, or Board UI/rendering changes.

Phase id and options:

$ARGUMENTS
