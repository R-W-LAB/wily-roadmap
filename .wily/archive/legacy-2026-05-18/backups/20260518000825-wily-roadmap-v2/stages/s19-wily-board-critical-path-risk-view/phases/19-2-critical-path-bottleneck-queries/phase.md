# Phase 19-2: Critical path and bottleneck queries

## Purpose

Compute attention items from Board's durable and live state.

## Acceptance

- Query helpers identify blocked chains and high-fanout dependencies.
- Query helpers identify ready but unclaimed work.
- Query helpers identify stale or awaiting-push live sessions.
