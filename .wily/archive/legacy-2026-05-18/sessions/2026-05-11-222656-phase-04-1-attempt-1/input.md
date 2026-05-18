# Wily Phase Context

Phase: 04-1 - Improve init roadmap authoring

## Phase

# Phase 04-1: Improve Init Roadmap Authoring

## Purpose

Improve the `$wily-init` experience so roadmap creation is easier to run repeatedly and less dependent on ad hoc manual scaffolding.

## Expected Starting Conditions

- Phase 03 is done.
- Command skill contracts and tests are stable.

## Likely Files

- `scripts/wily.py`
- `tests/test_wily_cli.py`
- `skills/wily-init/SKILL.md`
- `skills/wily-workflow/references/planning-style.md`
- `docs/superpowers/specs/2026-05-11-wily-roadmap-design.md`

## Completion Criteria

- Any deterministic init behavior belongs in `scripts/wily.py`.
- `$wily-init` still scans first and asks for a goal when none is supplied.
- Existing `.wily/` state is never overwritten without approval.
- Tests document the intended init behavior.

## Known Risks

- Fully automatic roadmap generation may be too broad or too interpretive for a deterministic script.
- Keep Codex responsible for project interpretation unless the behavior is deterministic.

## Planner Adapter

# Planner Adapter

Recommended planner: superpowers:writing-plans

Use the planner before changing init behavior because this phase can affect state creation semantics.

## Prompt

# Execution Prompt

Improve Wily init roadmap-authoring ergonomics without implementing project-specific roadmap intelligence.

Scope:
- Identify deterministic init behavior worth moving into `scripts/wily.py`.
- Preserve approval-first overwrite behavior.
- Add focused tests before implementation.
- Update skill docs only where behavior changes.

## Verification

# Verification

Run:

```bash
python3 -m unittest tests.test_wily_cli
python3 -m unittest discover
python3 -m py_compile scripts/wily.py scripts/wily_state_summary.py
```

Also test a temporary project init path manually if script behavior changes.

## Handoff

# Handoff

This phase can run in parallel with phase 04-2 after phase 03 is done.

Start by comparing the documented init flow in `skills/wily-init/SKILL.md` with the actual `command_init` implementation in `scripts/wily.py`.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.

Generate one before editing `scripts/wily.py`.
