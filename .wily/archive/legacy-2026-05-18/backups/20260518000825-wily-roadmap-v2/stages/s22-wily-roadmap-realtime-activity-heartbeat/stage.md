# s22: Wily Roadmap realtime activity heartbeat

## Purpose

Make Wily Roadmap show local work in realtime in both `wily-watch` and Wily Board, even before `.wily/` changes are committed and pushed.

The desired flow is:

- Local Stage or Phase work appears immediately as local-only activity.
- Codex, Claude, and human sessions get one live row per session, not one overwritten shared status.
- Heartbeat shows whether the session process is alive.
- Token-zero `worked` signals show whether the agent is actively doing work.
- If heartbeat stops, Board and Watch mark the session stale instead of pretending it is still active.
- After push, GitHub sync attaches or clears the provisional overlay without putting session data in durable YAML.

## Source Plan

Implement from:

- `docs/superpowers/plans/2026-05-16-wily-board-local-activity-heartbeat.md`

That plan is the product and technical contract for this Stage.

## Scope

- Add Board support for a general `live_items` model keyed by `session_id`, with server-clock freshness and `current_item_id` attach resolution.
- Render local-only Stage/Phase work on Board before push, including one chip per `(actor, agent)` session.
- Update `wily-watch` and one-shot status rendering to read `.wily/local/live/active/*.json` and show the same local session reality without sending network events.
- Extend Wily CLI live events around `created_local`, `claimed`, `heartbeat`, `worked`, `renamed`, `completed_local`, `blocked_local`, and `released`.
- Implement a session-scoped detached heartbeat sidecar with parent-shell PID watch, `.alive` marker, PID file, and TTL.
- Add token-zero agent work signals through Claude/Codex hooks and the Codex Desktop App Server bridge path described in the plan.
- Keep `.wily/` durable state clean: no `session_id`, no live secret, no pushed runtime files.

## Non-Goals

- Do not replace GitHub-synced `.wily` state as the durable source of truth.
- Do not add a global always-running daemon.
- Do not make heartbeat failures block Wily commands.
- Do not require Board write actions to push directly; PR-only write safety remains.
- Do not start the broad Board UI redesign from s21 in this Stage, beyond UI needed to expose the realtime activity model.

## Child Phase Direction

This Stage is decomposed so Watch renders `Stage 22` with child Phases, matching the established roadmap pattern.

- 22-1 Stage/Phase Watch contract guardrail.
- 22-2 Plan reconciliation and surface verification.
- 22-3 Board `live_items` foundation.
- 22-4 Board and Wily Watch live rendering.
- 22-5 Wily CLI event client and heartbeat lifecycle.
- 22-6 Agent work signals and bridges.
- 22-7 Attach resolution, smoke, and operations docs.
