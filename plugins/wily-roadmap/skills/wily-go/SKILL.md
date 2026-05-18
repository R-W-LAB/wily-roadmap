---
name: wily-go
description: Use when the user types $wily-go to get the goal text for custom-workflow.
---

# Wily Go

Emit a task goal block for `custom-workflow-skillset:plan-goal-runner`. Wily does not call custom-workflow directly.

## Internal Command

```bash
python3 <plugin-root>/scripts/wily.py go <id> [--json]
```

## Behavior

- Read-only: status is not changed.
- Requires the task to be `in_progress`.

## Response Style

- Use Korean when the user is speaking Korean.
- Report only the requested roadmap output or concise answer.
- Avoid procedural narration before or after the result.
- Do not echo internal helper commands in normal user-facing responses.
