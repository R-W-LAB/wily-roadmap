# Verification

Passed:

```bash
python3 -m unittest tests.test_wily_state_summary
```

Result: 6 tests passed.

```bash
python3 -m unittest discover
```

Result: 27 tests passed.

```bash
python3 -m py_compile scripts/wily.py scripts/wily_state_summary.py
```

Result: passed with no output.

Manual check:

```bash
python3 scripts/wily.py status
```

Result: passed. Output used Korean headings and `Phase 흐름:` with stage-based DAG grouping. Stage 4 grouped `04-1` and `04-2` together, and Stage 5 showed `05` with `의존: 04-1, 04-2`.

Review follow-up:

```bash
python3 -m unittest tests.test_wily_state_summary.WilyStateSummaryTest.test_summarizes_superseded_replacement_metadata
```

Result: failed before the fix because replacement detail still rendered `04R replaces 04`; passed after changing it to `04R 대체: 04`.
