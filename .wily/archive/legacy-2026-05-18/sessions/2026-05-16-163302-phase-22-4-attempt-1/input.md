# Wily Phase Context

Phase: 22-4 - Board and Wily Watch live rendering

## Phase

# Phase 22-4: Board and Wily Watch live rendering

## Purpose

Render realtime activity clearly in both Wily Board and `wily-watch`.

## Acceptance

- Board shows local-only activity awaiting push.
- Board renders one chip per `(actor, agent)` session.
- Board and Watch distinguish `working`, `active`, `idle`, and `stale`.
- `wily-watch` reads `.wily/local/live/active/*.json` without emitting network events.
- Durable roadmap progress stays visually separate from live session state.

## Planner Adapter

Missing.

## Prompt

# Execution Prompt

Execute Board and Wily Watch live rendering from the realtime heartbeat plan.

## Verification

# Verification

Run Board route/render tests and Wily Watch output tests for local-only rows, multi-agent chips, freshness states, and durable/live separation.

## Handoff

# Handoff

Keep `wily-watch` read-only. Event emission belongs to Wily commands and heartbeat sidecars.

## Existing Implementation Plan

No implementation plan exists yet.
Use the recommended planner to create one if this phase needs a detailed plan.
