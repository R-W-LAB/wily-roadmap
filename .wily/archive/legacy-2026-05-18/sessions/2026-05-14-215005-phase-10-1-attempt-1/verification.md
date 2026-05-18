# Verification

Run focused update tests first, then the broader suite.

At minimum:

```bash
python3 -m unittest tests.test_wily_cli tests.test_wily_command_skills
python3 -m unittest discover
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
```

Manual checks:

- `./wily update --check` reports a zip/non-git install clearly when `.git` is absent in a temp copy.
- `./wily update --check` reports current version and commit in a git checkout.
- Dirty working trees are refused before any pull.

## Evidence

Focused self-update tests:

```text
python3 -m unittest tests.test_wily_cli.SelfUpdateCliTest
Ran 4 tests in 1.038s
OK
```

Command skill tests:

```text
python3 -m unittest tests.test_wily_command_skills
Ran 22 tests in 0.006s
OK
```

Focused CLI and command tests:

```text
python3 -m unittest tests.test_wily_cli tests.test_wily_command_skills
Ran 84 tests in 3.253s
OK (skipped=1)
```

Full suite:

```text
python3 -m unittest discover
Ran 138 tests in 3.663s
OK (skipped=2)
```

Manifest validation:

```text
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
exit 0
```

Compile check:

```text
python3 -m py_compile scripts/wily.py
exit 0
```

Manual dirty-tree safety check:

```text
./wily update --check
Current version: 0.1.0
Install type: git
Working tree has local changes.
...
Commit, stash, or use a fresh managed clone before updating.
exit 1
```
