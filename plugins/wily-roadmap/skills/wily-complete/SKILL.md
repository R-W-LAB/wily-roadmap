---
name: wily-complete
description: Use when the user types $wily-complete after a Wily phase has been implemented and verified.
metadata:
  short-description: Complete a verified Wily phase
---

# Wily Complete

Use `$wily-complete <phase-id>` to mark a verified phase as done.

This is state-changing. It marks the phase `done`, clears stale phase blocker metadata, marks the current session `verified` when one exists, and snapshots Custom Workflow Skillset result artifacts back into the session archive when they exist.

## Internal Command

```bash
python3 <plugin-root>/scripts/wily.py complete <phase-id>
```

## Required Before Running

- The phase implementation matches the approved scope.
- Verification has run, or the reason it could not run is recorded.
- Changed files and result are summarized in the current session.
- If `$wily-run` routed the phase through Custom Workflow Skillset, read `custom-workflow-result.md` and use it as the result and verification evidence source.
- The user approved completion when review is required.
- In shared Wily repositories, completion should be committed with both implementation changes and shared Wily state changes so collaborators can pull the updated progress.
- If remote sync matters, prefer checking/pulling latest state before completion or clearly report that it was not checked.

Complete does not implement the phase or run broad verification by default. It closes a verified execution attempt.

## Board Reflection Contract

- Follow the Board reflection contract in `references/board-reflection-contract.md` after local completion/session state is written.
- Preserve durable `.wily` state first, then reflect the Board-visible `completed_local` status when Board live config is available.
- Record deterministic evidence such as emit result, API, SSE, or SSR HTML in the response for this important transition.
- Use actual-site visual verification only for Board failures, mismatches, explicit visual requests, or Board UI/rendering changes.
- If reflection fails, warn with the changed Wily state, failed projection, recovery command, and whether actual-site visual verification remains incomplete.

## Response Style

- When announcing Wily plugin or skill usage, use Korean if the user is speaking Korean.
- Do not echo internal helper commands in normal user-facing responses.
- Report only the result, the relevant path or artifact, and the next action or blocker.
- Keep safety-critical approval requirements when they apply.
- For a successful complete, include the phase id, completion result, and verification/session status.
