# Verification

Commands run:

- `/Users/wilycastle/Code/projects/wily-board`: local TestClient risk smoke
  - Passed: rendered blocked, dependency bottleneck, stale live, awaiting-push, and unclaimed-ready items in severity order.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest`
  - Passed: 45 tests.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run python -m py_compile app/db/repo.py app/web/routes.py`
  - Passed.
