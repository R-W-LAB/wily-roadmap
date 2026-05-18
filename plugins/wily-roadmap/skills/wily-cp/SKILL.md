---
name: wily-cp
description: Use when recording or importing Wily checkpoint progress for a task.
---

# Wily CP

Record checkpoint progress in `.wily/tasks/<id>/progress.jsonl` so `wily watch` can render checkpoint bars and current cp state.

## Internal Command

```bash
python3 <plugin-root>/scripts/wily.py cp <task-id> <start|done|note|import-status> <cp-or-status-path> [--note TEXT] [--actor ID]
```

## Behavior

- State-changing: appends checkpoint events to the task `progress.jsonl`.
- Use `wily cp <id> start <cp>` when a custom-workflow checkpoint starts.
- Use `wily cp <id> done <cp>` when that checkpoint passes verification.
- Use `wily cp <id> import-status <agent-handoffs/...-status.md>` to backfill checkpoint events from a custom-workflow status board.
- Import is idempotent for existing checkpoint/event pairs.

## Response Style

- Use Korean when the user is speaking Korean.
- Report only the task id, cp action, and next action or blocker.
- Do not echo internal helper commands in normal user-facing responses.
