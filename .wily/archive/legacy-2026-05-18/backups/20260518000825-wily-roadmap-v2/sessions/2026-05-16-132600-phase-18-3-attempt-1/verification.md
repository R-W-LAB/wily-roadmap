# Verification

Commands run:

- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_db.py::test_list_repo_health_classifies_ok_stale_and_not_initialized tests/test_web_routes.py::test_board_renders_sync_health_for_registered_repositories -v`
  - Passed: 2 tests.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_db.py tests/test_web_routes.py -v`
  - Passed: 21 tests.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run python -m py_compile app/db/repo.py app/web/routes.py`
  - Passed.
