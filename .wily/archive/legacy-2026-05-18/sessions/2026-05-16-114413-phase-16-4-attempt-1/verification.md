# Verification

Ran in `/Users/wilycastle/Code/projects/wily-board`:

```sh
uv run pytest tests/test_operations_doc.py tests/test_live_events.py tests/test_web_routes.py
```

Result: 11 passed, 5 warnings.

```sh
WILY_BOARD_SECRET=secret SYNC_REPOS=R-W-LAB/wily-roadmap SQLITE_PATH=/private/tmp/wily-board-live-smoke2.sqlite uv run uvicorn app.main:create_app --factory --host 127.0.0.1 --port 8765
```

Then ran Wily CLI from an isolated temp project with:

```sh
WILY_BOARD_URL=http://127.0.0.1:8765 WILY_BOARD_SECRET=secret WILY_BOARD_REPO=R-W-LAB/wily-roadmap WILY_BOARD_ACTOR=airmang python3 /Users/wilycastle/Code/projects/wily-roadmap/plugins/wily-roadmap/scripts/wily.py start 02
```

SQLite verification:

```text
02|airmang|claimed|sessions/2026-05-16-114609-phase-02-attempt-1
```

The first smoke attempt was accidentally run with the wrong cwd. The accidental session and roadmap mutation were removed, and the smoke was rerun from the temp project cwd.

Final verification:

```sh
uv run pytest
```

Result: 30 passed, 8 warnings. Warnings are existing Starlette TestClient cookie deprecations.

```sh
python3 -m unittest plugins.wily-roadmap.tests.test_wily_cli plugins.wily-roadmap.tests.test_wily_command_skills
```

Result: 100 tests passed, 1 skipped.

```sh
python3 -m py_compile plugins/wily-roadmap/scripts/wily.py plugins/wily-roadmap/scripts/wily_state_summary.py
```

Result: passed.

```sh
uv run python -m py_compile app/db/repo.py app/web/routes.py app/live/events.py app/main.py
```

Result: passed.
