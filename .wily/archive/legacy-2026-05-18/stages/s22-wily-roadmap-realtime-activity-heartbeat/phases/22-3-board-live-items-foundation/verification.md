# Verification

Board tests run in `/Users/wilycastle/Code/projects/wily-board`.

Red check:

```sh
uv run pytest tests/test_live_events.py tests/test_db.py::test_upsert_live_item_stores_session_id_and_ignores_client_clock tests/test_db.py::test_upsert_live_item_updates_duplicate_session_id_in_place tests/test_db.py::test_decorate_live_item_freshness_tracks_worked_window tests/test_config.py::test_settings_defaults_for_fixed_stage15_inputs
```

Result: failed before implementation because `decorate_live_item_freshness`, `list_live_items`, `upsert_live_item`, and `live_work_seconds` did not exist.

Green targeted check:

```sh
uv run pytest tests/test_live_events.py tests/test_db.py::test_upsert_live_item_stores_session_id_and_ignores_client_clock tests/test_db.py::test_upsert_live_item_updates_duplicate_session_id_in_place tests/test_db.py::test_decorate_live_item_freshness_tracks_worked_window tests/test_config.py::test_settings_defaults_for_fixed_stage15_inputs
```

Result: `10 passed`.

Expanded check:

```sh
uv run pytest tests/test_live_events.py tests/test_db.py tests/test_config.py tests/test_web_routes.py
```

Result: `40 passed, 18 warnings`.

Full Board check:

```sh
uv run pytest
```

Result: `55 passed, 21 warnings`.
