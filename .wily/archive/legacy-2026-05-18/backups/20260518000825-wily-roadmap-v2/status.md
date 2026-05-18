# Wily Status

Roadmap version 29 is complete through Stage s24. Remaining future work from s25 and s26 is canceled as `superseded`; Stage s27 is the next ready Stage for a large Wily Roadmap refactor.

Current baseline:
- Stage s15 created and deployed `R-W-LAB/wily-board` as the separate Wily Board service.
- Stages s16-s20 added live local work overlays, heartbeat freshness, collaboration operations, risk/attention views, and personal/shared repo visibility.
- Stage s21 delivered the read-only Next.js Wily Board UI redesign.
- Stage s22 connected Wily Roadmap realtime activity heartbeat into `wily-watch` and Wily Board.
- Stage s23 added provisional live draft topology overlays for local Stage decomposition.
- Stage s24 hardened the realtime Board bridge end to end across Wily live sessions, CustomWorkflow checkpoint status, Codex worked signals, Board API/SSE/UI, and local E2E proof.
- A follow-up production SSE fix was applied in `R-W-LAB/wily-board` so `/api/sse/live` stays connected with periodic heartbeat events instead of closing after one snapshot.

New roadmap revision:
- `.wily/revisions/2026-05-17-132403-replan-26.md`
- Added Stage s25: Wily Board UI polish and usability improvements.
- `.wily/revisions/2026-05-17-204434-replan-27.md`
- Added Stage s26: Wily Roadmap plugin 개선 및 정리.
- `.wily/revisions/2026-05-17-205537-replan-28.md`
- Superseded remaining s25 phases and s26.
- Added Stage s27: Wily Roadmap 대규모 리팩토링.

Next action:
- Review Stage s27 scope, then either run it directly or decompose it before implementation.
