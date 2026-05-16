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
