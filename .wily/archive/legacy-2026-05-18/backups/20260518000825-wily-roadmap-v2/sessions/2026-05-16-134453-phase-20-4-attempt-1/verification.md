# Verification

Commands run:

- `/Users/wilycastle/Code/projects/wily-board`: local TestClient personal visibility smoke
  - Passed: `airmang` all/shared/mine filters and `Julirsia` shared-only + direct 404.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest`
  - Passed: 50 tests.
- `/Users/wilycastle/Code/projects/wily-roadmap`: `python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli plugins.wily-roadmap.tests.test_wily_command_skills`
  - Passed: 104 tests, 1 skipped.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run python -m py_compile app/config.py app/main.py app/actions/routes.py app/db/repo.py app/live/events.py app/web/routes.py`
  - Passed.
- `/Users/wilycastle/Code/projects/wily-roadmap`: `python3 -m py_compile plugins/wily-roadmap/scripts/wily.py`
  - Passed.
