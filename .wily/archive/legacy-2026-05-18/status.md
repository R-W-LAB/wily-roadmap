# Wily Status

Roadmap schema `wily-roadmap-v2` is complete through Stage s30. Stages s25 and s26 remain canceled as `superseded`.

Current baseline:
- Stage s15 created and deployed `R-W-LAB/wily-board` as the separate Wily Board service.
- Stages s16-s20 added live local work overlays, heartbeat freshness, collaboration operations, risk/attention views, and personal/shared repo visibility.
- Stage s21 delivered the read-only Next.js Wily Board UI redesign.
- Stage s22 connected Wily Roadmap realtime activity heartbeat into `wily-watch` and Wily Board.
- Stage s23 added provisional live draft topology overlays for local Stage decomposition.
- Stage s24 hardened the realtime Board bridge end to end across Wily live sessions, CustomWorkflow checkpoint status, Codex worked signals, Board API/SSE/UI, and local E2E proof.
- Stage s28 completed the Wily Board read-only cutover by removing legacy Jinja/mutating routes from the active app.
- Stage s29 lifted the Wily Board frontend stack onto Tailwind, shadcn/ui primitives, Framer Motion, TanStack Query invalidation, next-themes, date-fns Korean relative time, sanitized markdown rendering, and generated OpenAPI types.
- Stage s30 completed Wily Board DAG dagre layout, Headline and Attention components, mobile stage-list/bottom-sheet fallback, and repo switcher/pin ordering polish.

Verification:
- s29 verification evidence is recorded in `.wily/stages/s29-board-polish-stack-lift/verification.md`.
- s30 verification evidence is recorded in `.wily/stages/s30-board-dag-components-mobile/verification.md`.

Next action:
- Stage s31 is ready: Heartbeat 잔여 + SSE polish.
