# Result

Implemented phase 12-1.

- `$wily-watch` SGR mouse parsing now preserves button codes.
- Expand/collapse toggling now requires a left mouse press on the rendered body area, or the existing `d` key fallback.
- Right mouse press opens a tmux context menu so app mouse reporting does not swallow the user's tmux pane menu.
- Middle mouse presses, release events, and wheel events no longer toggle folding.
- Wheel up/down events scroll expanded completed-stage content.
- Expanded watch rendering accepts a clamped scroll offset and keeps `--once` deterministic.
- `wily-watch` skill guidance and tests now describe left-click toggle plus wheel scrolling.
