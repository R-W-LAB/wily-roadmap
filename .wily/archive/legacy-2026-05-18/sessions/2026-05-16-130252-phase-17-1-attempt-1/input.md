# Wily Phase Context

Phase: 17-1 - Heartbeat event contract and Board freshness model

## Phase

# Phase 17-1: Heartbeat event contract and Board freshness model

## Purpose

Extend Board live events with heartbeat semantics, freshness thresholds, and stale classification.

## Acceptance

- Board accepts heartbeat live events without mutating durable roadmap state.
- Live sessions expose fresh/stale classification from configurable thresholds.
- Existing command-boundary live overlay behavior remains compatible.

## Planner Adapter

# Planner

Recommended planner: manual

## Prompt

# Execution Prompt

Implement the Board-side heartbeat event contract and freshness model.

## Verification

# Verification

Run Board live event and DB tests.

## Handoff

# Handoff

Start from Stage s16 live overlay storage and event ingestion.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.
