# Phase 24-3: Board checkpoint overlay API, SSE, and UI parity

Make Board receive and display checkpoint overlay state.

Acceptance:

- Board accepts signed checkpoint overlay events and rejects malformed or unsigned payloads.
- Checkpoint overlay storage remains separate from durable roadmap tables.
- Board JSON and SSE APIs expose current checkpoint, current action, blocker, verification, evidence, actor, agent, and freshness.
- Board Hub and repo detail render the same checkpoint/live state shown by Wily status/watch.
- Durable Git sync remains authoritative for Stage/Phase progress counts.
