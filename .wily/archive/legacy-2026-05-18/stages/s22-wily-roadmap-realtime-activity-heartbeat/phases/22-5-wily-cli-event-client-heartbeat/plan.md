# Implementation Plan

1. Add failing Wily CLI lifecycle tests:
   - config loads from repo-local untracked `.wily/local/board.json`
   - `wily start` writes `.wily/local/live/active/<session-id>.json`
   - `wily start` keeps `session_id` out of durable roadmap YAML
   - heartbeat sidecar is spawned detached when enabled
   - `complete` cleans the registry and `.alive` marker
   - heartbeat writes `.pid` and updates the registry
   - parent-shell disappearance releases the live session
   - `release` cleans live state without changing durable status
   - start recovers orphan registry files
2. Add Board config loading from env, user config, and repo-local untracked config.
3. Add live registry helpers for active JSON files, `.alive`, `.pid`, session id generation, orphan recovery, and cleanup.
4. Integrate registry open/close into `start`, `complete`, `block`, and `release`.
5. Extend `live-heartbeat` with `--session`, `--parent-shell-pid`, `--ttl`, and `--foreground`.
6. Run targeted lifecycle tests and full Wily CLI tests.
