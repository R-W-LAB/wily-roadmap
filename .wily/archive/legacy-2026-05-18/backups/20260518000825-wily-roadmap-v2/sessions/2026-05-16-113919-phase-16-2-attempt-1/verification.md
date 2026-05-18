# Verification

Ran in `/Users/wilycastle/Code/projects/wily-board`:

```sh
uv run pytest tests/test_web_routes.py::test_repo_detail_renders_live_overlay_chip tests/test_web_routes.py::test_board_active_section_includes_live_claimed_phase -v
```

Result: 2 passed, 2 warnings.

```sh
uv run pytest
```

Result: 30 passed, 8 warnings. Warnings are existing Starlette TestClient cookie deprecations.

```sh
uv run python -m py_compile app/db/repo.py app/web/routes.py app/live/events.py app/main.py
```

Result: passed.
