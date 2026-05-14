# Custom Workflow Skillset Routing

Wily Roadmap owns durable roadmap memory, phase lifecycle, dependency checks, attempts, status transitions, replans, and completion history.

Custom Workflow Skillset executes selected Wily phases. Wily does not bundle the Custom Workflow implementation files; it routes the active Codex agent to the installed `custom-workflow-skillset` plugin by skill name and receives the execution result through explicit artifacts.

## Routing Contract

`$wily-run` creates a Custom Workflow request with:

- phase id and title
- phase path and phase files
- roadmap context
- current Wily session path
- selected workflow engine
- autonomy mode label
- suggested native `/goal` command
- result target path
- completion, review, and blocker instructions

The request is written to `agent-handoffs/<phase-slug>-custom-workflow-request.md` and copied into `.wily/sessions/<session>/custom-workflow-request.md` for audit history.

## Required Custom Workflow Skills

The active agent must route execution through:

- `custom-workflow-skillset:plan-goal-runner` for the phase execution package and native `/goal` contract.
- `custom-workflow-skillset:parallel-lane-runner` only when the execution package returns `PARALLEL_SAFE` or `PARALLEL_SAFE_WITH_LIMITS`.

Custom Workflow owns phase implementation planning, progress tracking, bounded lane execution, and verification evidence. Wily owns phase lifecycle and final status transitions.

## Result Contract

Custom Workflow writes its result to:

- `agent-handoffs/<phase-slug>-custom-workflow-result.md`
- `.wily/sessions/<session>/custom-workflow-result.md`

The result should include:

- result summary
- verification evidence
- changed files
- progress log
- blocker text, if blocked
- recommended phase status: `needs_review`, `blocked`, `ready`, or `done`
- raw artifacts useful for audit

Custom Workflow must not mark Wily phases done directly. Final completion still requires Wily verification evidence and `$wily-complete`. If blocked, use `$wily-block`.

## Autonomy Modes

Wily owns the autonomy policy label passed to external workflows.

`conservative`:

- local edits use normal agent judgment
- remote actions require explicit approval
- destructive actions require explicit approval
- push, PR, merge, and GitHub comments require explicit approval

`goal_scoped`:

- local implementation and verification may continue within the approved phase
- dependency installs may proceed when clearly phase-scoped and non-destructive
- remote actions require explicit approval
- destructive actions require explicit approval

`yolo`:

- only for explicit autonomous runs in safe repositories
- hard stops still apply for broad destructive commands, payments, credential exposure, forbidden actions, and repeated verification failure without new evidence

Do not inherit an external workflow's more permissive default unchanged.

## Policy

- Do not bundle external workflow implementation files inside Wily.
- Route to the installed Custom Workflow Skillset plugin by explicit skill names.
- Copy Custom Workflow results back into Wily session artifacts before completion or block.
- Do not require hooks, MCP servers, or app integrations for core Wily behavior.
- Remote and destructive actions remain approval-first.
- Preserve current plugin discovery compatibility through `.codex-plugin/plugin.json` and top-level `skills/`.
- Use top-level wrapper skills only when direct plugin discovery requires them.
