---
name: wily-retry
description: Use when the user types $wily-retry or wants to create a new attempt for an unfinished Wily phase.
metadata:
  short-description: Retry a Wily phase
---

# Wily Retry

Use `$wily-retry <stage-id>/<phase-id>` to create a new session attempt for an unfinished phase. In `wily-roadmap-v2` repositories, the canonical Phase ref is required; Stage ids are not executable. Legacy phase-only refs are accepted only in legacy non-v2 repositories.

This is state-changing. It preserves prior attempts, creates the next attempt session, and marks the phase `in_progress`.

## Internal Command

```bash
python3 <plugin-root>/scripts/wily.py retry <stage-id>/<phase-id>
```

## Boundaries

- Do not delete or overwrite prior sessions.
- Read the new `session/input.md` before continuing.
- Keep the new attempt scoped to the same phase unless the roadmap is explicitly replanned.

## Board Reflection Contract

- Follow the Board reflection contract in `references/board-reflection-contract.md` after local retry/session state is written.
- Preserve durable `.wily` state first, then reflect the retry/claim live projection when Board live config is available.
- Record deterministic evidence such as emit result, API, SSE, or SSR HTML.
- Use actual-site visual verification only for Board failures, mismatches, explicit visual requests, or Board UI/rendering changes.
- If reflection fails, warn with the changed Wily state, failed projection, recovery command, and whether actual-site visual verification remains incomplete.

## Response Style

- When announcing Wily plugin or skill usage, use Korean if the user is speaking Korean.
- Do not echo internal helper commands in normal user-facing responses.
- Report only the result, the relevant path or artifact, and the next action or blocker.
- Keep safety-critical approval requirements when they apply.
- For a successful retry, include the phase id, new attempt/session path, and scoped next action.
