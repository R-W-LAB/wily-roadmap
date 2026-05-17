---
name: wily-run
description: Use when the user types $wily-run to route an executable Wily phase into Custom Workflow Skillset without completing the phase.
metadata:
  short-description: Route a Wily phase to Custom Workflow
---

# Wily Run

Use `$wily-run <phase-id> [--runner custom-workflow] [--autonomy conservative|goal_scoped|yolo]` to route a selected Wily phase into Custom Workflow Skillset.

This is state-changing. It may start or attach to a Wily execution session, creates Custom Workflow request/result artifacts, and marks the phase `in_progress`. It must not mark the phase `done`. Final completion remains a separate verified `$wily-complete <phase-id>` action.

## Internal Command

```bash
python3 <plugin-root>/scripts/wily.py run <phase-id> [--runner custom-workflow] [--autonomy conservative|goal_scoped|yolo]
```

## Arguments

- `<phase-id>` is required.
- `--runner custom-workflow` is accepted as an alias for `custom-workflow-skillset`.
- `--autonomy conservative|goal_scoped|yolo` optionally labels the requested autonomy mode.

## Routing Responsibilities

`$wily-run` should:

- read applicable `AGENTS.md`
- read `.wily/roadmap.yaml`
- validate that the phase exists and is executable
- record the Custom Workflow Skillset engine and autonomy mode
- start or attach the Wily session
- build a concise phase context request for Custom Workflow Skillset
- write `agent-handoffs/<phase-slug>-custom-workflow-request.md`
- write `agent-handoffs/<phase-slug>-custom-workflow-result.md`
- write `.wily/sessions/<session>/custom-workflow-request.md`
- write `.wily/sessions/<session>/custom-workflow-result.md`
- include an exact `/goal` command when the runtime cannot set it directly
- route into Custom Workflow Skillset through `custom-workflow-skillset:plan-goal-runner`
- use `custom-workflow-skillset:parallel-lane-runner` only when the generated execution package says `PARALLEL_SAFE` or `PARALLEL_SAFE_WITH_LIMITS`
- after Custom Workflow finishes, copy or ensure its summary, changed files, verification evidence, blocker text, and recommended Wily status are in `custom-workflow-result.md`
- never mark the Wily phase `done`

Custom Workflow checkpoint/status-board updates should be reflected to Board through `checkpoint-sync` or an equivalent helper path. The Board event is `checkpoint_updated`, and the runner should retain deterministic evidence from the emit result, API, SSE, or SSR HTML.

The Wily plugin does not bundle Custom Workflow implementation files and does not require bundled runner files. It routes the active agent to the installed `custom-workflow-skillset` plugin by skill name. Custom Workflow may recommend `needs_review`, `blocked`, `ready`, or `done`, but Wily completion still requires verification evidence and `$wily-complete`.

## Boundaries

The helper script prepares routing artifacts and prints the required Codex skill route. The active agent owns invoking `custom-workflow-skillset:plan-goal-runner`, running the resulting phase execution, and writing `custom-workflow-result.md`. `$wily-complete` and `$wily-block` snapshot that result into the Wily session when recording the final state.

## Autonomy Policy

- `conservative`: remote actions and destructive actions require explicit approval.
- `goal_scoped`: local phase-scoped implementation and verification may continue through Custom Workflow Skillset; remote and destructive actions still require explicit approval.
- `yolo`: use only when explicitly requested for a safe repository; hard stops still apply for broad destructive commands, payments, credential exposure, forbidden actions, and repeated verification failure without new evidence.

Remote actions and destructive actions remain approval-first in every mode.

## Board Reflection Contract

- Follow the Board reflection contract in `references/board-reflection-contract.md` after local run/session and Custom Workflow routing artifacts are written.
- Preserve durable `.wily` state first, then reflect the run/checkpoint live projection when Board live config is available.
- Record deterministic evidence such as emit result, API, SSE, or SSR HTML.
- Use actual-site visual verification only for Board failures, mismatches, explicit visual requests, or Board UI/rendering changes.
- If reflection fails, warn with the changed Wily state, failed projection, recovery command, and whether actual-site visual verification remains incomplete.

## Response Style

- When announcing Wily plugin or skill usage, use Korean if the user is speaking Korean.
- Do not echo internal helper commands in normal user-facing responses.
- Report only the result, the relevant path or artifact, and the next action or blocker.
- Keep safety-critical approval requirements when they apply.
- Report the phase id, selected workflow engine, selected autonomy mode, and whether the Custom Workflow request/result files are available.
- Report the session path, request path, result path, required `custom-workflow-skillset:plan-goal-runner` route, and exact native goal command when routing succeeds.
- Tell the user that `$wily-run` does not complete the phase; use `$wily-complete <phase-id>` only after verification evidence exists.
