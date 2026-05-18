# Phase 24-4: Local E2E proof and production smoke gate

Prove realtime behavior end to end and gate production actions explicitly.

Acceptance:

- Local Board E2E smoke proves Wily session, CustomWorkflow checkpoint update, Codex worked signal, Board API/SSE, Board Hub, repo detail, and Wily status/watch agree.
- The old false-success case is covered: missing `.wily/board.json` or hooks prevents realtime success from being claimed.
- Production smoke checklist exists and is approval-gated for secrets, push, deploy, restart, and live event emission.
- Final reporting clearly names whether evidence is local E2E only or approved production smoke.
