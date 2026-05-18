# Verification

Run focused parser and lifecycle tests:

```bash
python3 -m unittest tests.test_wily_state_summary tests.test_wily_cli
python3 -m py_compile scripts/wily.py scripts/wily_state_summary.py
```

Then run the full suite:

```bash
python3 -m unittest discover
```

Expected:

- block scalar summaries are preserved;
- block list dependencies are parsed as list values;
- `wily start` preserves semantic roadmap data and does not create bogus phases;
- existing inline roadmap tests still pass.

## Evidence

- `python3 -m unittest tests.test_wily_state_summary tests.test_wily_cli` -> 70 tests OK.
- `python3 -m py_compile scripts/wily.py scripts/wily_state_summary.py` -> exit 0.
- `python3 -m unittest discover` -> 144 tests OK, 1 skipped.
