---
name: wily-replan
description: Use when the user types $wily-replan to add, revise, drop, assign, or commit Wily tasks.
---

# Wily Replan

Stage task list edits in `.wily/init/draft.yaml`, validate dependencies, and commit changes to `tasks.yaml`.

## Internal Command

```bash
python3 <plugin-root>/scripts/wily.py replan [add|revise-task|drop|assign|project|commit|cancel]
```

## Behavior

- State-changing: only `commit` updates durable task state.
- Done tasks cannot be dropped and non-cosmetic done-task edits are rejected.

## Response Style

- Use Korean when the user is speaking Korean.
- Report only the result, the relevant path or artifact, and the next action or blocker.
- Keep safety-critical approval requirements when they apply.
- Do not echo internal helper commands in normal user-facing responses.
