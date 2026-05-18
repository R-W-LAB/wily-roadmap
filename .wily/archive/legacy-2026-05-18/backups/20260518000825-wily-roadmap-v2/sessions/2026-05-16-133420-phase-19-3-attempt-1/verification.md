# Verification

Commands run:

- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_web_routes.py::test_board_renders_attention_risk_items tests/test_web_routes.py::test_board_renders_quiet_attention_empty_state -v`
  - Passed: 2 tests.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_web_routes.py tests/test_db.py -v`
  - Passed: 25 tests.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run python -m py_compile app/db/repo.py app/web/routes.py`
  - Passed.
