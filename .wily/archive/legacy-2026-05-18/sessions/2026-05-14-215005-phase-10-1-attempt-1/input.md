# Wily Phase Context

Phase: 10-1 - Zip bootstrap에서 GitHub self-update 경로 제공

## Phase

# Phase 10-1: Zip bootstrap에서 GitHub self-update 경로 제공

## Purpose

Zip으로 공유된 Wily 설치본이 다음 릴리즈부터 GitHub 기반 managed install로 전환하거나 스스로 업데이트할 수 있게 한다.

## Source Spec

- `docs/superpowers/specs/2026-05-14-wily-self-update-design.md`

## Dependencies

- 09-6 Optional runner hooks와 watch progress 후속 통합

## Expected Output

- `./wily update` CLI command.
- `$wily-update` Codex skill entrypoint.
- Zip install detection and clear migration guidance.
- Git-managed install update check and fast-forward-only update path.
- README guidance for zip bootstrap and managed GitHub install.
- Tests that avoid real network access.

## Known Risks

- The command must not update in the background.
- Zip installs must not be overwritten or deleted automatically.
- Dirty plugin checkouts must be protected from accidental pulls.
- Remote operations must remain explicit and approval-first.

## Planner Adapter

# Planner

Use `superpowers:writing-plans` before implementation.

The plan should be test-driven and should keep the implementation local-first:

- model update states before changing code
- test zip/non-git detection first
- test dirty git refusal
- test already-current local repository behavior with a local bare remote
- add command skill and manifest exposure after CLI behavior is stable

## Prompt

# Execution Prompt

Implement Wily self-update support from the approved design.

Scope:

- Add `update` support to `scripts/wily.py`.
- Add `$wily-update` skill and command metadata.
- Expose the command in plugin defaults if appropriate.
- Support `--check`, `--migrate`, and `--yes`.
- Keep all remote or file-changing work explicit.
- Update README with zip bootstrap and managed GitHub install instructions.

Do not add background update checks, hooks, MCP servers, app integrations, or global shell changes.

## Verification

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

## Handoff

# Handoff

Not started.

## Existing Implementation Plan

No implementation plan exists yet.
Use the recommended planner to create one if this phase needs a detailed plan.
