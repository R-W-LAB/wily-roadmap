# Verification

Commands run:

- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_web_routes.py::test_board_supports_all_shared_and_mine_visibility_filters -v`
  - Passed: 1 test.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_web_routes.py tests/test_db.py -v`
  - Passed: 29 tests.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run python -m py_compile app/web/routes.py`
  - Passed.
