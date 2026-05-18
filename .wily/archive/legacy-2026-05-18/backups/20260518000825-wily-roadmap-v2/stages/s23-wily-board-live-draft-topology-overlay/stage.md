# s23: Wily Board live draft topology overlay

## Purpose

Close the realtime Board gap where local Stage decomposition is visible in `wily status` but invisible on Wily Board until commit and GitHub sync.

This Stage adds a provisional topology draft path for local roadmap structure changes. Presence events continue to show who is working; draft topology events show what local Stage/Phase structure exists before it is pushed.

## Scope

- Emit a signed `stage_decomposed_local` event from `decompose-stage`.
- Store draft topology separately from heartbeat/presence state.
- Render locally decomposed child phases as provisional `local draft` and `awaiting push` rows.
- Clear matching drafts after durable `stage.yaml` sync imports real child phases.
- Add diagnostics so missing local Board config is immediately visible.

## Non-Goals

- Do not make Board mutate repositories directly.
- Do not replace GitHub sync as durable source of truth.
- Do not poll developer machines from Board.
- Do not broaden this into arbitrary collaborative editing of `.wily` files.

## Design Reference

- `docs/superpowers/specs/2026-05-17-wily-board-live-draft-topology-design.md`
- `docs/superpowers/plans/2026-05-17-wily-board-live-draft-topology.md`
