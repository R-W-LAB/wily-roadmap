# Wily Phase Context

Phase: 17-2 - Wily CLI heartbeat mode

## Phase

# Phase 17-2: Wily CLI heartbeat mode

## Purpose

Add an explicit opt-in Wily CLI heartbeat loop for active local sessions.

## Acceptance

- CLI heartbeat uses configured Board URL, secret, repo, and actor.
- Default interval is conservative, such as 15 or 30 seconds.
- Ctrl-C exits cleanly.
- Board failures are best-effort and do not corrupt local Wily state.

## Planner Adapter

# Planner

Recommended planner: manual

## Prompt

# Execution Prompt

Implement explicit Wily CLI heartbeat mode.

## Verification

# Verification

Run Wily CLI tests and a local Board heartbeat smoke.

## Handoff

# Handoff

Build on Phase 17-1 heartbeat event contract.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.
