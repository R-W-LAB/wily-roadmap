---
name: wily-decompose-stage
description: Use when the user types $wily-decompose-stage to explicitly break a Wily Stage into internal Phases and optional parallel lanes.
metadata:
  short-description: Decompose a Wily Stage
---

# Wily Decompose Stage

Use `$wily-decompose-stage <stage-id>` only when the user explicitly chooses to split a Stage into smaller work.

This is state-changing when applied. It records child Phases under the selected Stage directory and may record parallel lane metadata for later execution routing. It must never happen automatically during `$wily-init` or `$wily-start`.

## Internal Command

```bash
python3 <plugin-root>/scripts/wily.py decompose-stage <stage-id>
```

Approved decomposition can be applied from a local JSON file:

```bash
python3 <plugin-root>/scripts/wily.py decompose-stage <stage-id> --from-json <path>
```

## Boundaries

- Decomposition is explicit and user-approved.
- A Stage can be executed directly without decomposition.
- Do not start implementation while handling this command.
- Do not call subagents while decomposing; only record lane boundaries and write scopes for a later runner.
- Parallel lanes must have non-overlapping write scopes.
- Applied JSON must be a list of child Phase objects with `id`, `title`, optional `depends_on`, and optional `lanes`.
- Keep child Phase and lane details in `.wily/stages/<stage-id>/stage.yaml`; keep `.wily/roadmap.yaml` at Stage-level to reduce collaboration conflicts.
- Keep existing phase-only roadmaps compatible.

## Board Reflection Contract

- Follow the Board reflection contract in `references/board-reflection-contract.md` after local Stage topology files are written.
- Preserve durable `.wily` state first, then reflect or replay the `stage_decomposed_local` draft topology projection when Board live config is available.
- Use `python3 <plugin-root>/scripts/wily.py board sync-local <stage-id>` to replay the local draft after fixing Board config or reachability.
- Record deterministic evidence such as emit result, API, SSE, or SSR HTML.
- Use actual-site visual verification only for Board failures, mismatches, explicit visual requests, or Board UI/rendering changes.
- If reflection fails, warn with the changed Wily state, failed projection, recovery command, and whether actual-site visual verification remains incomplete.

## Response Style

- When announcing Wily plugin or skill usage, use Korean if the user is speaking Korean.
- Do not echo internal helper commands in normal user-facing responses.
- Report only the result, the relevant path or artifact, and the next action or blocker.
- Keep safety-critical approval requirements when they apply.
- For a successful decomposition, include the stage id, created child Phase count, and whether parallel lanes were recorded.
