# s21: Wily Board UI redesign

## Purpose

Redesign Wily Board so it works as a practical operating surface for daily roadmap coordination, not just a list of synced repositories.

This Stage is intentionally deferred until Stage s22 lands the realtime local activity foundation. The UI redesign should not guess around the live model; it should render the final `live_items`, Wily Watch, heartbeat, and work-signal behavior produced by s22.

The redesigned UI should make these questions easy to answer at a glance:

- What is active right now?
- What needs attention?
- Which repo or stage should be picked next?
- What is shared collaboration work versus personal work?
- Which status is durable Git state and which status is provisional live overlay?

## Scope

- Rework the Board dashboard information architecture around operational priority.
- Improve scanability for repo progress, active sessions, stale sessions, blockers, awaiting-push work, and unclaimed ready work.
- Render the Stage s22 live activity model cleanly: local-only entries, per-agent chips, `working` / `active` / `idle` / `stale` status, and durable sync attach state.
- Clarify personal/shared filters and repo visibility without adding a workspace model.
- Keep durable `.wily` Git state visually distinct from live local overlay state.
- Preserve existing FastAPI, SQLite, htmx, GitHub App, and signed webhook architecture.

## Non-Goals

- Do not replace `.wily` Git state as the source of truth.
- Do not add new MCP servers, hooks, app integrations, or workspace permissions.
- Do not redesign the Wily CLI watch pane in this stage.
- Do not change GitHub PR write safety behavior.
- Do not invent another live activity model; consume the model delivered by Stage s22.

## Child Phase Direction

Initial decomposition should likely split into:

- Information architecture and dashboard layout.
- Repo detail and phase row redesign.
- Responsive/mobile polish.
- Visual QA and route-level regression coverage.
