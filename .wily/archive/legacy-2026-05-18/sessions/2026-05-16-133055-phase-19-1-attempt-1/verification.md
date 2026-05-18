# Verification

Commands run:

- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_db.py::test_risk_signal_severity_and_item_shape_are_deterministic -v`
  - Passed: 1 test.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_db.py -v`
  - Passed: 9 tests.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run python -m py_compile app/db/repo.py`
  - Passed.
