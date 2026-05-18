# Verification

Run in implementation worktree:

```bash
python3 -m unittest tests.test_wily_command_skills
python3 -m unittest discover
```

Results:

```text
python3 -m unittest tests.test_wily_command_skills
Ran 15 tests in 0.002s
OK

python3 -m unittest discover
Ran 92 tests in 1.189s
OK (skipped=2)
```

Manual inspection:

- `rg` confirmed each command skill includes the quiet response phrase.
- `rg` confirmed mutating skills include result/path/next-action response wording.
- `rg` confirmed read-only skills include concise-output and no-procedural-narration wording.
- `rg` confirmed helper commands remain discoverable under `## Internal Command`.
