# Wily Phase Context

Phase: 22-7 - Attach resolution, smoke, and operations docs

## Phase

# Phase 22-7: Attach resolution, smoke, and operations docs

## Purpose

Connect provisional live activity to durable GitHub sync and document operations.

## Acceptance

- Board attaches local overlays after push using event-stream `current_item_id`.
- Replan rename does not break attach.
- Durable `.wily` YAML contains no live session fields.
- End-to-end smoke covers local-only work, Codex and Claude activity, stale transition, push attach, and secret rotation.
- Operations docs cover setup, troubleshooting, and HMAC rotation.

## Planner Adapter

Missing.

## Prompt

# Execution Prompt

Execute attach resolution, smoke, and operations documentation from the realtime heartbeat plan.

## Verification

# Verification

Run end-to-end smoke through local-only Stage, heartbeat/worked, stale transition, replan rename, GitHub sync attach, clean durable YAML diff, and HMAC rotation.

## Handoff

# Handoff

This Phase closes the loop between provisional local activity and durable GitHub-synced roadmap state.

## Existing Implementation Plan

No implementation plan exists yet.
Use the recommended planner to create one if this phase needs a detailed plan.
