# Verification

Commands run:

- `/Users/wilycastle/Code/projects/wily-board`: local TestClient smoke for conflict + queue + sync health
  - Passed: rendered `Claim conflict`, `Needs follow-up`, `awaiting push`, `PR open`, `Sync health`, `sync ok`, `sync stale`, and `not initialized`.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest`
  - Passed: 41 tests.
- `/Users/wilycastle/Code/projects/wily-roadmap`: `python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli plugins.wily-roadmap.tests.test_wily_command_skills`
  - Passed: 104 tests, 1 skipped.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run python -m py_compile app/actions/routes.py app/db/repo.py app/live/events.py app/web/routes.py`
  - Passed.
- `/Users/wilycastle/Code/projects/wily-roadmap`: `python3 -m py_compile plugins/wily-roadmap/scripts/wily.py`
  - Passed.
