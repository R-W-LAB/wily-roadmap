# Verification

Passed:

```bash
python3 -m unittest tests.test_wily_command_skills
```

Result: 17 tests OK.

```bash
python3 -m unittest discover
```

Result: 94 tests OK, 2 skipped.

```bash
python3 -m py_compile scripts/wily.py
```

Result: exit 0.

Manual inspection from a Claude Code user's perspective:

- `agent-compatibility.md` explains `$wily-*` plain text command entrypoints.
- It documents reading matching `skills/wily-*/SKILL.md` files if skill discovery is unavailable.
- It preserves `python3 <plugin-root>/scripts/wily.py <command>` helper invocation.
- It keeps local-first and approval-first boundaries explicit.
- `.codex-plugin/plugin.json` and `skills/` compatibility are preserved for Codex plugin discovery.
