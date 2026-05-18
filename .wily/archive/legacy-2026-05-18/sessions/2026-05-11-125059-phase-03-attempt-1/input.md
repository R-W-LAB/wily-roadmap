# Wily Phase Context

Phase: 03 - Korean stage-based DAG status output

## Phase

# Phase 03: Korean Stage-Based DAG Status Output

## Purpose

Change `wily-status` from English prose lists to Korean user-facing status output with a compact stage-based DAG summary.

## Expected Starting Conditions

- Phase 02 is done.
- Command skill consistency rules are settled.
- Current `wily-status` output already shows all phases and executable pending phases.

## Likely Files

- `scripts/wily_state_summary.py`
- `tests/test_wily_state_summary.py`
- `skills/wily-status/SKILL.md`
- `skills/wily-workflow/SKILL.md`
- `skills/wily-workflow/references/planning-style.md`

## Completion Criteria

- `wily-status` prints Korean labels for user-facing headings and progress text.
- Phase status labels display in Korean while stored roadmap markers remain English.
- The phase overview uses a stage-based DAG layout, not recursive indentation that drifts right as roadmaps grow.
- Parallel phases with the same dependency level are grouped under the same stage.
- Multi-dependency phases show an explicit `의존:` line instead of forcing an inaccurate tree edge.
- Tests cover Korean labels, the stage layout, parallel grouping, and multi-dependency annotation.

## Known Risks

- The helper script currently has no locale flag. This phase may choose Korean as the Wily default for status output, while keeping machine-facing file markers in English.
- DAG layout should stay deterministic and simple. Do not introduce Graphviz or Mermaid rendering as a dependency in this phase.

## Planner Adapter

# Planner Adapter

Recommended planner: superpowers:writing-plans

Use the planner before implementation because this phase changes CLI output contracts and tests.

## Prompt

# Execution Prompt

Implement Korean stage-based DAG output for `wily-status`.

Scope:
- Keep `.wily/roadmap.yaml` status values in English.
- Translate only user-facing status output.
- Replace `All phases:` list with a `Phase 흐름:` or equivalent stage-based DAG section.
- Keep output stable for tests.
- Do not add external renderer dependencies.

## Verification

# Verification

Run:

```bash
python3 -m unittest tests.test_wily_state_summary
python3 -m unittest discover
python3 -m py_compile scripts/wily.py scripts/wily_state_summary.py
```

Manual check:

```bash
python3 scripts/wily.py status
```

Confirm the output uses Korean headings and a stage-based DAG layout.

## Handoff

# Handoff

Start from `scripts/wily_state_summary.py`.

Useful design decision:
- Use stage/rank layout instead of nested tree layout.
- Keep each stage near the left edge.
- Show multi-dependency phases with `의존: ...`.
- Consider Graphviz/Mermaid export only as a later optional feature.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.

Expected first implementation step:
- Add failing tests for Korean `wily-status` labels and stage-based DAG output.
