---
name: wily-execute
description: Use when the user asks an agent to execute a Wily task end-to-end via custom-workflow.
---

# Wily Execute

When the user says "T03 cw로 진행해줘" or asks to process the next Wily task, orchestrate the command sequence.

1. Run `wily status` or `wily next` to confirm the task.
2. Run `wily claim <id>` to record actor, timestamp, claim SHA, and progress file.
3. Run `wily go <id>` and pass the emitted block to `custom-workflow-skillset:plan-goal-runner`.
4. Let custom-workflow append cp events to `.wily/tasks/<id>/progress.jsonl` and use `Wily-Task: <id>` / `Wily-CP: <name>` commit trailers.
5. Compare the result against task acceptance and report scope drift.
6. Run `wily done <id>` only after verification.
7. Run `wily land <id>` only after explicit user approval.

## Guardrails

- Never call `wily done` after a failed custom-workflow run.
- Never call `wily land` without explicit approval.
- For another actor's observed work, use `wily done <id> --observed` only when the user asks.

## Response Style

- Use Korean when the user is speaking Korean.
- Report the task id, current step, and next required action or blocker.
- Do not echo internal helper commands in normal user-facing responses.
