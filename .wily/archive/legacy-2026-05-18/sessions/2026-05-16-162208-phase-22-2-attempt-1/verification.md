# Verification

Ran Board focused tests in `/Users/wilycastle/Code/projects/wily-board`:

```sh
uv run pytest tests/test_live_events.py tests/test_db.py::test_decorate_live_session_freshness_classifies_fresh_and_stale tests/test_db.py::test_list_live_claim_conflicts_ignores_self_and_stale_claims tests/test_web_routes.py::test_board_excludes_stale_live_session_from_active_and_allows_up_next tests/test_web_routes.py::test_repo_detail_renders_stale_live_session_with_last_seen_label
```

Result: `8 passed, 2 warnings`.

Ran local tool checks:

```sh
codex --version
claude --version
codex app-server --help
codex app-server generate-json-schema --out <tmpdir>
codex app-server generate-ts --out <tmpdir>
```

Results:

- Codex CLI: `codex-cli 0.130.0`
- Claude Code: `2.1.143`
- App Server command is available.
- Generated schemas/types include the needed turn, hook, item, and raw response notifications.

Ran Wily smoke:

```sh
python3 plugins/wily-roadmap/scripts/wily.py status
python3 plugins/wily-roadmap/scripts/wily.py next
```

Result: Stage 22 renders as a separate Stage section and Phase 22-2 is active.
