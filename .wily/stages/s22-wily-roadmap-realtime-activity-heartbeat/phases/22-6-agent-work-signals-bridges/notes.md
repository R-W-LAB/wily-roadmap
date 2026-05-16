# Notes

Implemented token-zero work signal paths.

Commands:

- `wily live-worked [item-id] --session <sid> --agent <agent> --from-hook`
- `wily hooks install --target codex|claude`
- `wily codex-bridge --session <sid> --fixture <jsonl> --once`

Behavior:

- hooks resolve active sessions from `.wily/local/live/active/*.json`.
- `live-worked` updates `event=worked`, `last_worked_at`, `tool`, and optional `summary`.
- `--from-hook` exits successfully when no active session is available, so hook failures degrade to heartbeat-only.
- Codex and Claude hook installers write `PostToolUse` command hooks that call `wily live-worked --from-hook`.
- Codex bridge fixture mode converts `item/completed` and `hook/completed` notifications into `worked`.
- missing bridge input prints a warning and leaves heartbeat-only activity intact.

Carry-forward:

- Phase 22-7 should document real installation paths, HMAC setup, and bridge troubleshooting.
