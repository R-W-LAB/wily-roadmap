# Phase 22-5: Wily CLI event client and heartbeat lifecycle

## Purpose

Make Wily CLI own session identity, live event emission, and heartbeat lifecycle.

## Acceptance

- Board config loads from env, user config, and repo-local untracked config.
- `wily start` writes `.wily/local/live/active/<session-id>.json`.
- The detached heartbeat sidecar returns the terminal immediately.
- Parent-shell PID watch, `.alive`, PID file, TTL, `--foreground`, and orphan recovery are implemented.
- `complete`, `block`, `release`, and replan rename events cleanly update live state.
