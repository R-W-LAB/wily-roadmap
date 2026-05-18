# Verification

Executed verification:

```bash
python3 -m unittest tests.test_wily_cli.WatchInputTest
```

Result: PASS, 8 tests.

```bash
python3 -m unittest tests.test_wily_watch_ui
```

Result: PASS, 50 tests, 1 skipped.

```bash
python3 -m unittest tests.test_wily_cli tests.test_wily_watch_ui tests.test_wily_command_skills
```

Result: PASS, 128 tests, 1 skipped.

```bash
python3 -m py_compile scripts/wily.py scripts/wily_watch_ui.py
```

Result: PASS.

```bash
python3 -m unittest discover
```

Result: PASS, 134 tests, 1 skipped.

```bash
./wily watch --once --ui ascii
```

Result: PASS, rendered roadmap v11 with phase 12-1 in progress and deterministic ASCII output.

Pseudo-TTY smoke:

```bash
./wily watch --here --ui ascii --interval 0.2
```

Result: PASS. Sent left-click SGR input to expand completed stages, sent wheel-down SGR input to scroll expanded content, then sent `q`; process exited with code 0 and restored mouse mode.

Post-completion checks:

```bash
python3 scripts/wily.py status
```

Result: PASS, roadmap v11 shows 26/26 phases done.

```bash
python3 -m unittest tests.test_wily_cli.WatchInputTest tests.test_wily_watch_ui tests.test_wily_command_skills && python3 -m py_compile scripts/wily.py scripts/wily_watch_ui.py
```

Result: PASS, 80 tests, 1 skipped, and compile succeeded.

```bash
git diff --check
```

Result: PASS.
