# Notes

Implemented Board and Watch live rendering.

Board:

- `live_items` now stores `agent`.
- dashboard renders a `Local activity awaiting push` section from `live_items`.
- repo detail renders one chip per live item session on matching Phase rows.
- live item decoration distinguishes `working`, `active`, `idle`, and `stale`.
- stale live items are excluded from dashboard priority rendering.

Wily Watch:

- reads `.wily/local/live/active/*.json` locally.
- renders live details such as `codex working` on matching Stage/Phase rows.
- renders unmatched registry entries under `Local activity`.
- does not emit network events.
- durable progress counts remain based only on roadmap state.

Carry-forward:

- Phase 22-5 still needs to create and maintain the active registry automatically.
- Phase 22-7 still needs durable sync attach/clear behavior for `live_items`.
