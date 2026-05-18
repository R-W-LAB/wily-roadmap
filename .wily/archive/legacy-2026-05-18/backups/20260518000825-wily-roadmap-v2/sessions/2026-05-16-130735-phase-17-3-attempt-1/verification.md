# Verification

Commands run:

- `uv run pytest tests/test_web_routes.py::test_board_excludes_stale_live_session_from_active_and_allows_up_next tests/test_web_routes.py::test_repo_detail_renders_stale_live_session_with_last_seen_label -v`
  - Passed: 2 tests.
- `uv run pytest tests/test_web_routes.py tests/test_db.py tests/test_config.py tests/test_live_events.py -v`
  - Passed: 19 tests.
- `uv run python -m py_compile app/config.py app/db/repo.py app/web/routes.py app/live/events.py`
  - Passed.
