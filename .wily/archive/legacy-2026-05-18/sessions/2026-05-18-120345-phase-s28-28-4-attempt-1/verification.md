# Verification

- RED observed first: `uv run pytest tests/test_readonly_invariants.py -q` failed on legacy mutation helper references before implementation.
- PASS: `uv run pytest tests/test_readonly_invariants.py tests/test_action_routes.py tests/test_web_routes.py tests/test_packaging.py tests/test_deploy_files.py tests/test_github_app.py -q` -> 13 passed, 1 warning.
- PASS: `uv run pytest -q` -> 76 passed, 14 warnings.
- PASS: `npm run lint`.
- PASS: `npm run build`.
