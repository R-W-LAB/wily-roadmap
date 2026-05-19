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
- The emitted goal text tells custom-workflow to use `wily cp <id> start <cp-name>`, `wily cp <id> done <cp-name>`, and `wily cp <id> import-status <status.md>` so `.wily/tasks/<id>/progress.jsonl` remains the Roadmap checkpoint ledger.
- Custom Workflow interface contract: custom-workflow does not update Wily by itself; the emitted checklist closes the cp automation gap for keeping Wily in sync.
- The default import-status recovery path is `.wily/handoffs/<id>/status.md`; `.wily/handoffs/<task-id>/status.md` is the template form.
- Use `wily cp <id> import-status .wily/handoffs/<id>/status.md` when a status board exists before checkpoint events were recorded.
- Custom Workflow interface contract: the cp automation gap is closed manually with `wily cp <id> import-status` when checkpoint calls were missed.
- The default handoff status path is `.wily/handoffs/<id>/status.md`.

## Response Style

- Use Korean when the user is speaking Korean.
- Report only the requested roadmap output or concise answer.
- Avoid procedural narration before or after the result.
- Do not echo internal helper commands in normal user-facing responses.
