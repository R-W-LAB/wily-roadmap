# Verification

Completed:

```bash
git check-ignore -v .wily/roadmap.yaml .wily/phases/08-2-collaborative-wily-state-sync/phase.md .wily/sessions/example
python3 scripts/wily.py status
python3 scripts/wily.py next
python3 -m unittest tests.test_wily_cli
```

Results:

- `.wily/roadmap.yaml` is not ignored.
- `.wily/phases/08-2-collaborative-wily-state-sync/phase.md` is not ignored.
- `.wily/sessions/example` remains ignored.
- `python3 scripts/wily.py status` passed.
- `python3 scripts/wily.py next` reports no next ready phase because 08-2 is currently `in_progress`.
- `python3 -m unittest tests.test_wily_cli.CollaborationPolicyTest tests.test_wily_cli.WilyCliTest` passed: 36 tests, 1 skipped.
- `python3 -m unittest tests.test_wily_watch_ui tests.test_wily_cli` passed: 88 tests, 2 skipped.
- `python3 -m unittest discover` passed: 114 tests, 2 skipped.
- `python3 -m py_compile scripts/wily.py scripts/wily_watch_ui.py scripts/wily_state_summary.py` passed.
