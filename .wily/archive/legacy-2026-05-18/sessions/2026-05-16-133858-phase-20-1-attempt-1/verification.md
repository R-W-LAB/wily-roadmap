# Verification

Commands run:

- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_config.py::test_settings_parses_personal_repos tests/test_db.py::test_schema_stores_initial_repositories tests/test_db.py::test_upsert_repo_stores_personal_visibility -v`
  - Passed: 3 tests.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_config.py tests/test_db.py -v`
  - Passed: 13 tests.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run python -m py_compile app/config.py app/db/repo.py app/main.py`
  - Passed.
