# Result

Implemented interactive completed-stage expansion for the Wily watch pane.

- `watch --here` now enables keyboard and SGR mouse interaction when stdin/stdout are TTYs.
- Clicking the folded completed-stage summary or pressing `d` toggles completed stages between folded and expanded views.
- `r` refreshes immediately, and `q` or Ctrl-C exits while restoring terminal mode and mouse reporting.
- `watch --once` remains deterministic and non-interactive.
- Added `--show-done` for starting a watch render with completed stages expanded and `--no-interactive` for the passive refresh loop.
