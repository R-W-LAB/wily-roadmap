# Phase 21-3: Wily live checkpoint adapter

## Purpose

Make Wily read runner checkpoint boards and expose checkpoint progress as a local live overlay on the attached Phase.

## Scope

- Parse CustomWorkflow status board and progress files from `agent-handoffs/`.
- Attach checkpoint state to the active Wily Stage/Phase using session and handoff metadata.
- Emit signed local checkpoint live events through the existing live activity path.
- Render current checkpoint, next checkpoint, blocker, verification, and evidence in Wily status/watch output.
- Do not mark durable Wily Phases done from checkpoint completion alone.
