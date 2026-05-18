# Wily Phase Context

Phase: 22-1 - Stage/Phase Watch contract guardrail

## Phase

# Phase 22-1: Stage/Phase Watch contract guardrail

## Purpose

Patch the Wily plugin so Watch uses the established Stage/Phase visual contract and a ready decomposed Stage cannot quietly show up as a single flat Stage line when child Phases are missing.

## Root Cause Captured

Current Watch grouping reuses the legacy Phase DAG-depth grouping for Stage mode. As a result, a real Stage ID such as `s22` can be rendered in the same visual group as `s18` when its dependency depth is 18 (`s22 -> s20 -> s16 -> ...`). Stage mode must group and label by Stage identity/order, not by inferred dependency-layer number.

## Acceptance

- `wily status` / `wily watch --once` render decomposed work as a `Stage N` separator/header with child Phase rows underneath.
- Stage mode never places `s22` under a `Stage 18` visual group just because the dependency depth is 18.
- `wily status` / `wily watch --once` make the missing decomposition state obvious for any ready Stage with `execution_mode: decomposed` and no child Phases.
- `wily next` points the user toward decomposition or the first child Phase, not a misleading flat Stage execution path.
- A regression test covers a ready decomposed Stage with missing `stage.yaml` or an empty `phases` list.
- The correct Watch pattern remains Stage header plus child Phase rows once decomposition exists.

## Planner Adapter

Missing.

## Prompt

# Execution Prompt

Implement Phase 22-1: Stage/Phase Watch contract guardrail.

Focus on two failures:

- Decomposed Stages should render as a `Stage N` separator/header with child Phase rows, not as a lone flat Stage item.
- A future ready Stage added with `execution_mode: decomposed` but no child `stage.yaml`/Phases should be caught immediately.
- Stage mode should not reuse legacy Phase dependency-depth grouping in a way that puts `s22` into a visual `Stage 18` group.

Keep changes local-first and scoped to the Wily Roadmap plugin.

## Verification

# Verification

- Add or update CLI tests for ready decomposed Stage with no child Phases.
- Verify decomposed Stage output includes a `Stage N` separator/header and child Phase rows.
- Add a regression fixture where `s22` depends on `s20` and confirm Watch does not visually group it under Stage 18 or beside `s18`.
- Verify `wily status` and `wily watch --once` expose the missing decomposition state.
- Verify decomposed Stages with valid child Phases still render Stage header plus Phase rows.
- Verify `wily next` behavior is not misleading for missing child Phases.

## Handoff

# Handoff

Start here before realtime heartbeat implementation.

The patch should make future roadmap authoring mistakes visible immediately in Watch and tests.

## Existing Implementation Plan

No implementation plan exists yet.
Use the recommended planner to create one if this phase needs a detailed plan.
