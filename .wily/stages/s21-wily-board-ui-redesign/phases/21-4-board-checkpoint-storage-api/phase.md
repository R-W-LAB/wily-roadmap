# Phase 21-4: Board checkpoint storage and SSE API

## Purpose

Let Wily Board receive, store, stream, and serve Phase-linked checkpoint overlay state.

## Scope

- Add storage for checkpoint live state without changing durable roadmap tables.
- Accept signed checkpoint live events and reject malformed or unauthenticated payloads.
- Expose read-only checkpoint data in repo, phase detail, desk, and SSE responses.
- Reconcile checkpoint overlay when durable Wily sync catches up or when a runner result is archived.
- Preserve existing GitHub App sync and authentication behavior.
