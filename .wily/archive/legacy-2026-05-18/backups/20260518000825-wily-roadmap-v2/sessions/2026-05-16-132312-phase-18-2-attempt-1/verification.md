# Verification

Commands run:

- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_db.py::test_list_review_queue_includes_awaiting_push_needs_review_and_open_pr tests/test_web_routes.py::test_board_renders_follow_up_queue_for_review_and_awaiting_push -v`
  - Passed: 2 tests.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_db.py tests/test_web_routes.py tests/test_action_routes.py -v`
  - Passed: 21 tests.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run python -m py_compile app/db/repo.py app/web/routes.py app/actions/routes.py`
  - Passed.
