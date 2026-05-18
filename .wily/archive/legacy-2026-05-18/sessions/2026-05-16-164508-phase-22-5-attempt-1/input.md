# Wily Phase Context

Phase: 22-5 - Wily CLI event client and heartbeat lifecycle

## Phase

# Phase 22-5: Wily CLI event client and heartbeat lifecycle

## Purpose

Make Wily CLI own session identity, live event emission, and heartbeat lifecycle.

## Acceptance

- Board config loads from env, user config, and repo-local untracked config.
- `wily start` writes `.wily/local/live/active/<session-id>.json`.
- The detached heartbeat sidecar returns the terminal immediately.
- Parent-shell PID watch, `.alive`, PID file, TTL, `--foreground`, and orphan recovery are implemented.
- `complete`, `block`, `release`, and replan rename events cleanly update live state.

## Planner Adapter

Missing.

## Prompt

# Execution Prompt

Execute the Wily CLI event client and heartbeat lifecycle from the realtime heartbeat plan.

## Verification

# Verification

Run CLI tests for config loading, signed event payloads, sidecar lifecycle, TTL, parent-shell exit, foreground SIGINT release, and orphan recovery.

## Handoff

# Handoff

Keep heartbeat best-effort. Board downtime must not break core Wily commands.

## Existing Implementation Plan

No implementation plan exists yet.
Use the recommended planner to create one if this phase needs a detailed plan.
