# Verification

Focused command skill test:

```bash
python3 -m unittest tests.test_wily_command_skills
```

Result:

```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.002s

OK
```

Full unittest discovery:

```bash
python3 -m unittest discover
```

Result:

```text
........................
----------------------------------------------------------------------
Ran 24 tests in 0.620s

OK
```

Plugin manifest JSON validation:

```bash
python3 -m json.tool .codex-plugin/plugin.json
```

Result: exited 0.

Placeholder scan:

```bash
rg -n "TODO|TBD|placeholder|old external workflow" skills .codex-plugin tests
```

Result: no matches.

Command skill slow-path scan:

```bash
rg -n "Use the recommended planner|superpowers:|writing-plans|pytest|python3 -m unittest|npm test|cargo test|go test|test-driven|TDD" skills/wily-{init,status,next,start,complete,block,retry,replan}/SKILL.md
```

Result: no matches.
