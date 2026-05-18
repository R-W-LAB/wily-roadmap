# Result

Implemented the risk signal model baseline.

- Added deterministic severity values for `blocked`, `dependency_bottleneck`, `stale_live_session`, `awaiting_push`, and `unclaimed_ready`.
- Added `make_risk_item` with stable fields for later query and UI work.
- Kept scoring local and data-driven.
