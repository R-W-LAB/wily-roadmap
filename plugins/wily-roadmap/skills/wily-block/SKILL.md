---
name: wily-block
description: Use when the user types $wily-block and a Wily task cannot continue.
---

# Wily Block

Record a blocker on a ready or in-progress task.

## Internal Command

```bash
python3 <plugin-root>/scripts/wily.py block <id> <reason>
```

## Behavior

- State-changing: sets status to blocked and records blocker text.
- `wily claim <id>` clears the blocker.

## Response Style

- Use Korean when the user is speaking Korean.
- Report only the result, the relevant path or artifact, and the next action or blocker.
- Keep safety-critical approval requirements when they apply.
- Do not echo internal helper commands in normal user-facing responses.
