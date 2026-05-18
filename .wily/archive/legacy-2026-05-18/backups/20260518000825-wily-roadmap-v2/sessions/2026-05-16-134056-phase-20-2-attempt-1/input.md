# Wily Phase Context

Phase: 20-2 - Login-scoped repo filtering and access control

## Phase

# Phase 20-2: Login-scoped repo filtering and access control

## Purpose

Ensure each login only sees repositories it is allowed to see.

## Acceptance

- Shared repos are visible to both allowed users.
- Personal repos are visible only to `visible_to`.
- Direct repo detail URLs deny access to unauthorized users.
- Sync and live event ingestion can store personal repo state without exposing it to other users.

## Planner Adapter

# Planner

Recommended planner: manual

## Prompt

# Execution Prompt

Implement login-scoped repo filtering and direct access checks.

## Verification

# Verification

Run Board web route tests for `airmang` and `Julirsia`.

## Handoff

# Handoff

Do not rely on hiding links only. Enforce access in route/query code.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.
