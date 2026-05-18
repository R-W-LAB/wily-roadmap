# Wily Phase Context

Phase: 02 - Harden command skill consistency

## Phase

# Phase 02: Harden Command Skill Consistency

## Purpose

Make the `$wily-*` command skills consistently short, discoverable, and aligned with shared workflow policy.

## Expected Starting Conditions

- Phase 01 is done.
- Korean response-style guidance is already settled and tested.

## Likely Files

- `skills/wily-init/SKILL.md`
- `skills/wily-status/SKILL.md`
- `skills/wily-next/SKILL.md`
- `skills/wily-start/SKILL.md`
- `skills/wily-complete/SKILL.md`
- `skills/wily-block/SKILL.md`
- `skills/wily-retry/SKILL.md`
- `skills/wily-replan/SKILL.md`
- `skills/wily-workflow/SKILL.md`
- `skills/wily-workflow/references/*.md`
- `tests/test_wily_command_skills.py`

## Completion Criteria

- Each command skill has a clear trigger, helper command, boundary, and response style.
- Shared policy stays in `skills/wily-workflow/references/` instead of being duplicated across command skills.
- Frontmatter remains valid for Codex skill discovery.
- Tests cover the consistency requirements that matter for future edits.

## Known Risks

- Over-documenting each command skill would violate the repo guidance to keep skill bodies concise.
- Tests should verify important invariants without hard-coding brittle prose.

## Planner Adapter

# Planner Adapter

Recommended planner: superpowers:writing-plans

Use the planner to produce a tight checklist before changing many skill files.

## Prompt

# Execution Prompt

Audit and tighten Wily command skill consistency.

Scope:
- Keep command skills concise.
- Move detailed policy to references when needed.
- Preserve plugin discovery compatibility.
- Add or adjust tests for durable command-skill invariants.

## Verification

# Verification

Run:

```bash
python3 -m unittest tests.test_wily_command_skills
python3 -m unittest discover
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
```

Search for obvious placeholders:

```bash
rg -n "TODO|TBD|placeholder|old external workflow" skills .codex-plugin tests
```

## Handoff

# Handoff

Use this phase after phase 01 is complete.

Begin by reading:
- `AGENTS.md`
- `skills/wily-workflow/SKILL.md`
- `skills/wily-workflow/references/routing-policy.md`
- `tests/test_wily_command_skills.py`

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.

Use the recommended planner if the audit finds more than one independent documentation issue.
