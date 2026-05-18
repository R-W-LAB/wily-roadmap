# Verification

Passed:

```bash
python3 -m unittest tests.test_wily_command_skills
```

Result: included in `python3 -m unittest tests.test_wily_cli tests.test_wily_command_skills`: 55 tests OK, 1 skipped.

```bash
python3 -m unittest discover
```

Result: 106 tests OK, 2 skipped.

```bash
python3 -m py_compile scripts/wily.py
```

Result: exit 0.

```bash
python3 -m json.tool .codex-plugin/plugin.json
```

Result: exit 0.

Manual fixture smoke:

- `$wily-issues` with `WILY_ISSUES_JSON` showed unlinked open issue suggestions and did not mutate roadmap.
- `$wily-issues --add-to-roadmap` with the same fixture created a local Wily phase and stored `github_issues`, `github_urls`, and `sync_policy: "manual"`.
