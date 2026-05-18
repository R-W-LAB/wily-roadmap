# Implementation Plan

1. Add failing Board attach tests:
   - durable sync clears matching `completed_local` live items
   - `current_item_id` allows attach after replan/rename
2. Patch Board live item normalization and sync clearing.
3. Update operations docs:
   - realtime local activity setup
   - hooks and Codex bridge
   - HMAC secret rotation
   - troubleshooting
   - `LIVE_WORK_SECONDS`
4. Run Board targeted tests, full Board tests, full Wily CLI tests, and durable YAML smoke.
5. Complete Phase 22-7 so the active local registry is cleaned.
