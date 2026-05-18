# Wily Phase Context

Phase: 20-1 - Repo visibility fields and config contract

## Phase

# Phase 20-1: Repo visibility fields and config contract

## Purpose

Add simple repo visibility fields and a config contract for personal repositories.

## Acceptance

- `repos` stores `visibility` with default `shared`.
- `repos` stores optional `visible_to`.
- Existing registered repositories remain shared by default.
- Personal repo config can map repo full names to a login, such as `airmang/solo-tool:airmang`.

## Planner Adapter

# Planner

Recommended planner: manual

## Prompt

# Execution Prompt

Implement Wily Board repo visibility fields and simple personal repo config.

## Verification

# Verification

Run Board config and DB tests.

## Handoff

# Handoff

Keep existing shared repo behavior unchanged.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.
