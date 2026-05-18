# Phase 21-2: CustomWorkflow checkpoint-to-Phase contract

## Purpose

Define how CustomWorkflow status board checkpoints attach to the current Wily Stage/Phase/session.

## Scope

- Map `agent-handoffs/*-status.md` fields to Wily runner progress: checkpoint id, status, current action, next checkpoint, blocker, verification, evidence, and recent events.
- Keep durable `.wily` Stage/Phase state authoritative; checkpoint progress is live runner overlay until Wily completion/block records verified history.
- Define drift repair for active runs where checkpoint progress advanced beyond the durable Wily Phase state.
- Define signed live event and Board API payload fields for checkpoint started, updated, completed, blocked, and verification updates.
- Keep CustomWorkflow external/reference-only; do not bundle its internals into Wily.
