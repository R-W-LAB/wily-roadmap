# Verification

Passed:

```bash
python3 -m unittest tests.test_wily_cli tests.test_wily_command_skills
```

Result: 48 tests OK, 1 skipped.

```bash
python3 -m unittest discover
```

Result: 98 tests OK, 2 skipped.

Manual zsh-compatible smoke checks:

```bash
zsh ./wily status
```

Result: exit 0; printed the `Wily Roadmap` pane.

```bash
zsh ./wily watch --once --ui ascii
```

Result: exit 0; printed the `Wily Roadmap` pane without opening tmux.

Safety grep:

```bash
rg -n "\\.zshrc|\\.zprofile|PATH|alias wily|git push|gh pr|curl |rm -rf" wily README.md tests/test_wily_cli.py tests/test_wily_command_skills.py
```

Result: only README explanatory text and the test forbidden-list matched.
