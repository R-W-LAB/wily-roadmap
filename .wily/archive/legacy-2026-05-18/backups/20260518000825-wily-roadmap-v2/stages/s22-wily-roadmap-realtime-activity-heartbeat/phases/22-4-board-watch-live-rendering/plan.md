# Implementation Plan

1. Add failing Board route tests:
   - item-scoped Stage activity renders in a local activity section
   - multiple live item sessions render as separate chips on the same Phase row
2. Add failing Wily Watch tests:
   - `.wily/local/live/active/*.json` renders a live chip on the matching Phase row
   - local-only live items render without changing durable progress counts
3. Update Board live rendering:
   - persist/display `agent` on `live_items`
   - decorate `working`, `active`, `idle`, and `stale`
   - show local activity awaiting push on the dashboard
   - show multiple live item chips on repo detail Phase rows
4. Update Wily Watch rendering:
   - read the local active session registry
   - append live details to matching Stage/Phase rows
   - render unmatched registry items under `Local activity`
   - keep done/total durable progress unchanged
5. Run targeted tests, full Board tests, and full Wily CLI tests.
