# Notes

Implemented attach resolution and operations docs.

Board:

- `replace_repo_state` now clears matching `live_items` when durable phase state becomes `done` or `blocked`.
- `upsert_live_item` honors `current_item_id` so replan/rename streams can attach to the new durable Phase id.
- This prevents completed local overlays from remaining stranded after GitHub sync catches up.

Docs:

- Added realtime local activity setup.
- Documented `.wily/local/board.json`.
- Documented hooks install for Codex and Claude.
- Documented Codex bridge fallback.
- Added `LIVE_WORK_SECONDS`.
- Added HMAC secret rotation and troubleshooting.

Durable smoke:

- Checked `.wily/roadmap.yaml` and Stage 22 `stage.yaml`; live runtime fields are not persisted there.
- Active runtime state is confined to `.wily/local/live`.
