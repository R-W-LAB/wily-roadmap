# Verification

Completed:

```bash
python3 -m unittest tests.test_wily_cli tests.test_wily_watch_ui
python3 -m py_compile scripts/wily.py
python3 -m unittest discover
python3 scripts/wily.py status
```

Results:

- Focused CLI/watch tests: 90 tests passed, 2 skipped.
- Full unittest discovery: 116 tests passed, 2 skipped.
- `python3 -m py_compile scripts/wily.py`: passed.
- `python3 scripts/wily.py status`: passed and showed 09-1 in progress.
- Plugin cache smoke: `runner-adapter-contract` and `runners/custom-workflow/runner.yaml` references are present in the cached plugin.
