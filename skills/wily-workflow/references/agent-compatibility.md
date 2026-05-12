# Agent Compatibility

Wily is maintained as a Codex-discoverable plugin, but its workflow contract is agent-neutral.

## Command Entry Points

Use the `$wily-*` text commands as user-facing entrypoints.

In Codex, plugin discovery can map those commands to Wily skills under `skills/`.

In Claude Code, use the same `$wily-*` command names as plain text instructions. If skill discovery is not available, read the matching `skills/wily-*/SKILL.md` file and follow its internal command and boundary sections.

## Helper Invocation

Run `python3 <plugin-root>/scripts/wily.py <command>` for deterministic local state operations.

The helper script owns file creation, roadmap state transitions, session directories, and watch/status rendering. The active agent still owns repository inspection, user approval, phase design, planner selection, implementation, verification, and concise reporting.

## Boundaries

Keep Wily local-first and approval-first in every agent environment.

Do not push, open pull requests, merge, install remote integrations, delete user work, or run destructive commands unless the user explicitly approves that specific action.

Keep `.codex-plugin/plugin.json` and `skills/` compatible with Codex plugin discovery even when adding Claude Code guidance.
