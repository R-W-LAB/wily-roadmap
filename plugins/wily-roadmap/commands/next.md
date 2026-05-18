---
description: Show the next ready Wily roadmap Phase
disable-model-invocation: true
allowed-tools: Bash, Read, Glob, Grep
---

Run the `wily-next` skill to surface the next executable Phase.

This is read-only. Do not create sessions, change Phase status, revise roadmap files, or implement phases. Use `${CLAUDE_PLUGIN_ROOT}/scripts/wily.py next` to compute the next ready Stage and next executable Phase, then report the canonical `<stage-id>/<phase-id>` ref, title, dependencies, recommended planner, and the `$wily-start <stage-id>/<phase-id>` (or `/wily:start <stage-id>/<phase-id>`) follow-up the user can run.
