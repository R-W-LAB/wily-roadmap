---
name: wily-claim
description: Use when the user types $wily-claim or says they are starting a Wily task.
---

# Wily Claim

Claim a ready or blocked task and record actor, claim timestamp, claim SHA, and progress file.

## Internal Command

```bash
python3 <plugin-root>/scripts/wily.py claim <id> [--force]
```

## Behavior

- State-changing: updates `tasks.yaml` and creates `.wily/tasks/<id>/progress.jsonl`.
- Invalid transitions return exit code 3.

## Response Style

- Use Korean when the user is speaking Korean.
- Report only the result, the relevant path or artifact, and the next action or blocker.
- Keep safety-critical approval requirements when they apply.
- Do not echo internal helper commands in normal user-facing responses.
