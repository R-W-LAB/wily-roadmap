# Execution Prompt

Execute Stage s22: Wily Roadmap realtime activity heartbeat.

Use `docs/superpowers/plans/2026-05-16-wily-board-local-activity-heartbeat.md` as the implementation contract.

Preserve these constraints:

- Durable `.wily` Git state remains the source of truth and never stores `session_id` or runtime heartbeat data.
- Live activity is a provisional local overlay that Board and Watch render separately from durable status.
- Heartbeat is session-scoped and starts as a detached sidecar only when enabled, not as a global daemon.
- `worked` signals must be token-zero: emitted by hooks, runtime bridge, or local helper code, not by prompting the model to call a command.
- Board write actions remain approval-first and PR-based.

Start with Phase 22-1. Patch the plugin guardrail first so this class of roadmap/Watch mismatch is caught before future realtime work starts.
