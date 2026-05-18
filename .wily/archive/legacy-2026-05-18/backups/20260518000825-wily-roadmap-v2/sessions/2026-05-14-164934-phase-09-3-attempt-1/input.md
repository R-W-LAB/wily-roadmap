# Wily Phase Context

Phase: 09-3 - wily-run 명령과 skill 추가

## Phase

# Phase 09-3: wily-run 명령과 skill 추가

## Purpose

Wily phase를 runner로 dispatch하는 사용자-facing command/skill surface를 추가한다.

## Source Spec

- `docs/superpowers/specs/2026-05-14-wily-bundled-runner-architecture.md`

## Dependencies

- 09-1 Runner adapter 계약과 Custom Workflow manifest 정의

## Parallel Group

09

## Expected Output

- `skills/wily-run/SKILL.md`
- Claude Code slash command wrapper such as `commands/wily-run.md` if command discovery is in scope.
- Plugin default prompt updates only if useful.
- Command docs for `$wily-run <phase-id> [--runner <id>] [--autonomy ...]`.

## Known Risks

- `wily-run` must not mark phases done.
- Remote or destructive actions remain approval-first.

## Planner Adapter

# Planner Adapter

Recommended planner: superpowers:writing-plans

Use the planner to keep the command UX small and consistent with existing Wily skills.

## Prompt

# Execution Prompt

Add the `wily-run` command and skill surface.

Scope:
- Create `skills/wily-run/SKILL.md`.
- Create or update command wrappers needed for the repo's supported plugin targets.
- Document runner and autonomy override flags.
- Keep dispatch implementation out of this phase unless it is only a thin placeholder.

## Verification

# Verification

Run focused command/skill tests, for example:

```bash
python3 -m unittest tests.test_wily_cli
```

If command wrapper tests exist, include them.

## Handoff

# Handoff

Start from existing Wily command skill style. Keep response style Korean-aware and local-first.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.
