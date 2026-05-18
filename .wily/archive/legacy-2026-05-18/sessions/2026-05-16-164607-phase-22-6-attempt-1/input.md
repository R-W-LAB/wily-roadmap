# Wily Phase Context

Phase: 22-6 - Agent work signals and bridges

## Phase

# Phase 22-6: Agent work signals and bridges

## Purpose

Emit token-zero `worked` events for Codex and Claude activity.

## Acceptance

- Claude and Codex hooks resolve active sessions from `.wily/local/live/active/*.json`.
- Codex Desktop App Server bridge converts tool-completion events into `worked`.
- Missing bridge or hook failures degrade to heartbeat-only activity.
- The model never has to spend tokens calling `wily live-worked`.

## Planner Adapter

Missing.

## Prompt

# Execution Prompt

Execute agent work signals and bridges from the realtime heartbeat plan.

## Verification

# Verification

Run hook helper tests, bridge notification-stream tests, reconnect tests, and heartbeat-only fallback tests.

## Handoff

# Handoff

Token-zero is the hard requirement. Do not solve this by asking the model to emit progress commands.

## Existing Implementation Plan

No implementation plan exists yet.
Use the recommended planner to create one if this phase needs a detailed plan.
