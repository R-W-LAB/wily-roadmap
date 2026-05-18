# Wily Phase Context

Phase: 05 - Plugin discovery and release polish

## Phase

# Phase 05: Plugin Discovery and Release Polish

## Purpose

Prepare the plugin for reliable local use after the core skill and CLI polish phases are complete.

## Expected Starting Conditions

- Phases 04-1 and 04-2 are done.
- Command skills and helper scripts are stable.

## Likely Files

- `.codex-plugin/plugin.json`
- `skills/`
- `scripts/`
- `tests/`
- `docs/superpowers/`

## Completion Criteria

- Plugin manifest is valid and accurately describes Wily Roadmap.
- Skill directories remain discoverable by Codex.
- Tests and compile checks pass.
- Documentation reflects the final workflow state.
- Any release, commit, push, or PR action is left for explicit user approval.

## Known Risks

- Packaging polish can drift into remote actions; keep this phase local unless the user asks otherwise.
- Avoid adding plugin layers such as hooks, MCP servers, or apps without explicit direction.

## Planner Adapter

# Planner Adapter

Recommended planner: superpowers:writing-plans

Use the planner to build a final verification checklist before release-oriented cleanup.

## Prompt

# Execution Prompt

Polish Wily Roadmap plugin discovery and local release readiness.

Scope:
- Validate plugin manifest and skill discovery assumptions.
- Run full tests and compile checks.
- Update docs only where they lag actual behavior.
- Do not commit, push, publish, or open PRs without explicit user approval.

## Verification

# Verification

Run:

```bash
python3 -m unittest discover
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
python3 -m py_compile scripts/wily.py scripts/wily_state_summary.py
rg -n "TODO|TBD|placeholder|old external workflow" .codex-plugin skills scripts tests docs
```

Review `git status --short` and summarize changed files before asking for any commit approval.

## Handoff

# Handoff

Use this as the final local polish phase after the script and skill contracts are stable.

Start with plugin discovery files, then run full verification before recommending any next action.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.

Generate a checklist before making release-readiness edits.
