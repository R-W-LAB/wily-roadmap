# Wily Phase Context

Phase: 18-3 - Repository sync health panel

## Phase

# Phase 18-3: Repository sync health panel

## Purpose

Show whether each registered repository is syncing correctly.

## Acceptance

- Board shows last sync time, initialized/missing `.wily` state, and webhook freshness.
- Registered repos with no `.wily/roadmap.yaml` are clearly marked as not initialized.
- Health panel stays read-only.

## Planner Adapter

# Planner

Recommended planner: manual

## Prompt

# Execution Prompt

Implement repository sync health panel in Board.

## Verification

# Verification

Run Board DB and web route tests.

## Handoff

# Handoff

Use existing repo registration and sync event data where possible.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.
