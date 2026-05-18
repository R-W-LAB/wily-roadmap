# Verification

Commands run:

- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_db.py::test_list_live_claim_conflicts_ignores_self_and_stale_claims tests/test_live_events.py::test_live_claims_returns_fresh_other_actor_and_ignores_stale tests/test_web_routes.py::test_repo_detail_renders_claim_conflict_warning_for_fresh_other_actor -v`
  - Passed: 3 tests.
- `/Users/wilycastle/Code/projects/wily-roadmap`: `python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli.WilyCliTest.test_start_warns_when_board_reports_other_fresh_claim`
  - Passed: 1 test.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run pytest tests/test_db.py tests/test_live_events.py tests/test_web_routes.py -v`
  - Passed: 21 tests.
- `/Users/wilycastle/Code/projects/wily-roadmap`: `python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli`
  - Passed: 80 tests, 1 skipped.
- `/Users/wilycastle/Code/projects/wily-roadmap`: `python3 -m py_compile plugins/wily-roadmap/scripts/wily.py`
  - Passed.
- `/Users/wilycastle/Code/projects/wily-board`: `uv run python -m py_compile app/db/repo.py app/live/events.py app/web/routes.py`
  - Passed.
