---
name: wily-done
description: Use when the user types $wily-done after a task has been verified.
---

# Wily Done

Mark an in-progress task done and write `.wily/tasks/<id>/result.md`.

## Internal Command

```bash
python3 <plugin-root>/scripts/wily.py done <id> [--note <text>|--observed|--force]
```

## Behavior

- State-changing: flips status to done and writes result metadata.
- Does not run a verification gate; the user's command is the closure signal.

## Response Style

- Use Korean when the user is speaking Korean.
- Report only the result, the relevant path or artifact, and the next action or blocker.
- Keep safety-critical approval requirements when they apply.
- Do not echo internal helper commands in normal user-facing responses.
