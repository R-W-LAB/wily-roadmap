# Wily Phase Context

Phase: 22-3 - Board live_items foundation

## Phase

# Phase 22-3: Board live_items foundation

## Purpose

Add the Board data model and event contract needed for local-only realtime activity.

## Acceptance

- `live_items` stores one row per live session using `session_id`.
- Freshness derives from server clock, not client clock.
- `worked` events update `last_worked_at`.
- Duplicate events are idempotent.
- Existing legacy live payloads remain accepted during migration.

## Planner Adapter

Missing.

## Prompt

# Execution Prompt

Execute the Board live item foundation from the realtime heartbeat plan.

## Verification

# Verification

Run Board DB and event ingestion tests for `live_items`, dedup, server-clock freshness, terminal states, and legacy payload compatibility.

## Handoff

# Handoff

Build on the existing Board live overlay implementation without changing durable roadmap sync semantics.

## Existing Implementation Plan

No implementation plan exists yet.
Use the recommended planner to create one if this phase needs a detailed plan.
