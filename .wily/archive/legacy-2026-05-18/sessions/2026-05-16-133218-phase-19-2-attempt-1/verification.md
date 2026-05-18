# Verification

Commands run:

- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_db.py::test_list_risk_items_combines_blocked_bottleneck_stale_awaiting_and_ready -v`
  - Passed: 1 test.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_db.py -v`
  - Passed: 10 tests.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run python -m py_compile app/db/repo.py`
  - Passed.
