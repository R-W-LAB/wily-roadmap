# Notes

Implemented the Wily CLI live session lifecycle.

Config:

- env values still work.
- repo-local untracked config is read from `.wily/local/board.json`.
- user config is read from `~/.wily/board.json` unless `WILY_BOARD_USER_CONFIG` overrides it.
- optional `agent`, heartbeat enablement, and heartbeat interval are supported.

Lifecycle:

- `wily start` creates `.wily/local/live/active/<session-id>.json`.
- `session_id` is not written to durable roadmap YAML.
- `.wily/local/live/<session-id>.alive` is created as the explicit liveness marker.
- `live-heartbeat` writes `.wily/local/live/<session-id>.pid`.
- `complete`, `block`, and `release` remove active registry and `.alive`.
- orphan active registry files without `.alive` are cleaned on the next `start`.

Heartbeat:

- detached sidecar spawning is enabled by `WILY_BOARD_HEARTBEAT=1`.
- sidecar command uses `live-heartbeat <id> --session <sid> --parent-shell-pid <pid>`.
- `live-heartbeat` supports `--session`, `--parent-shell-pid`, `--ttl`, and `--foreground`.
- parent-shell disappearance emits `released` and cleans local live state.

Carry-forward:

- Phase 22-6 still needs Codex/Claude hook and App Server work signals.
- Phase 22-7 still needs final operational docs and attach-after-sync cleanup rules.
