# Implementation Plan

1. Add failing tests for token-zero work signals:
   - `live-worked` resolves active sessions and updates `last_worked_at`
   - hook mode without an active session exits successfully
   - Codex hook installer writes a `PostToolUse` command
   - Claude hook installer writes a `PostToolUse` command
   - Codex bridge fixture converts `item/completed` into `worked`
   - missing bridge fixture degrades to heartbeat-only
2. Add `wily live-worked`.
3. Add hook installation helpers for Codex and Claude.
4. Add a Codex bridge fixture mode that translates App Server notifications into `worked`.
5. Keep hook/bridge failures non-blocking.
6. Run targeted tests and the full Wily CLI suite.
