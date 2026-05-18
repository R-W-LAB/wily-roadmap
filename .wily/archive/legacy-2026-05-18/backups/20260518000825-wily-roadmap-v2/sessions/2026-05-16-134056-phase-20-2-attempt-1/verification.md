# Verification

Commands run:

- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_db.py::test_list_visible_repos_returns_shared_plus_own_personal tests/test_web_routes.py::test_board_filters_personal_repos_by_login_and_denies_direct_access -v`
  - Passed: 2 tests.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_db.py tests/test_web_routes.py -v`
  - Passed: 28 tests.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run python -m py_compile app/db/repo.py app/web/routes.py`
  - Passed.
