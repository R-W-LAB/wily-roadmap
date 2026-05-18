# Verification

Passed:

```bash
python3 -m unittest tests.test_wily_watch_ui
```

Result: 45 tests OK, 1 skipped.

```bash
python3 -m unittest discover
```

Result: 101 tests OK, 2 skipped.

```bash
python3 -m py_compile scripts/wily_watch_ui.py
```

Result: exit 0.

Manual short-pane smoke:

```bash
LINES=9 COLUMNS=70 zsh ./wily watch --once --ui ascii
```

Result: printed `8 phases done across 6 stages` and preserved current 06-4/06-5 lines.
