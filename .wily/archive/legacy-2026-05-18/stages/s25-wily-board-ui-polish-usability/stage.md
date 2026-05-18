# s25: Wily Board UI polish and usability improvements

## Purpose

Turn the now-functional realtime Wily Board into a sharper daily operating surface.

S21 delivered the read-only Next.js Board redesign, S24 proved the realtime checkpoint/live bridge, and the SSE disconnect fix stabilized live updates in production. This Stage is a focused UI improvement pass that should make the Board easier to scan, navigate, and trust during real work.

## Scope

- Audit the current production Board UI against daily workflows: "what is active", "what needs attention", "what repo/stage should I pick next", and "is this durable or live overlay state".
- Improve information density, hierarchy, and layout for Hub, MY DESK, repo detail, Stage/Phase rows, checkpoint/live chips, and Attention sections.
- Polish live-update feedback so connected, retrying, stale, and refreshed states are visible without noisy toasts.
- Improve navigation ergonomics: repo switching, anchors, back/forward flow, keyboard/focus behavior, and mobile access to dense views.
- Improve responsive layout across desktop and phone widths without card nesting, overlapping text, or marketing-style hero treatment.
- Capture browser screenshots and regression checks for the main dashboard and repo detail views.

## Non-Goals

- Do not make Board the source of truth for `.wily` roadmap state.
- Do not add mutation workflows, PR-writing controls, admin panels, hooks, MCP servers, or app integrations.
- Do not change auth, GitHub sync, signed live-event ingestion, or database schema unless a UI bug proves a narrow read-only API adjustment is required.
- Do not broaden this into a new activity model; consume the existing durable roadmap, live item, checkpoint, and draft topology APIs.

## Child Phases

- 25-1 UI audit and improvement backlog.
- 25-2 Hub and MY DESK scanability pass.
- 25-3 Repo detail, Stage map, and checkpoint row polish.
- 25-4 Responsive/browser QA and production rollout evidence.
