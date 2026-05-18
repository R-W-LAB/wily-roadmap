# Phase 17-1: Heartbeat event contract and Board freshness model

## Purpose

Extend Board live events with heartbeat semantics, freshness thresholds, and stale classification.

## Acceptance

- Board accepts heartbeat live events without mutating durable roadmap state.
- Live sessions expose fresh/stale classification from configurable thresholds.
- Existing command-boundary live overlay behavior remains compatible.
