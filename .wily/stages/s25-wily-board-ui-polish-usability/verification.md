# Verification

Verify Stage s25 with:

- Browser screenshots for Hub and repo detail at desktop and mobile widths.
- Canvas/DOM checks that visible text does not overlap, truncate awkwardly, or resize layout unexpectedly.
- Frontend lint and production build in `R-W-LAB/wily-board`.
- Relevant backend API tests if read-only payload shape changes.
- SSE/live-update manual or automated smoke showing connected, heartbeat/refreshed, retrying, and stale states behave without noisy false disconnect toasts.
- Accessibility checks for keyboard focus order, command palette/repo switcher, anchors, and theme controls.
- Production rollout evidence only after approval-gated deploy/push actions.

No completion claim should be made without fresh verification evidence.
