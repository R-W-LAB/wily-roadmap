# Wily Phase Context

Phase: 07-1 - GitHub Issues 선택적 연동 계약 정의

## Phase

# Phase 07-1: GitHub Issues 선택적 연동 계약 정의

## Purpose

Wily roadmap이 GitHub Issues를 사용하는 협업 프로젝트와 연결될 수 있도록 선택적 linkage 계약을 정의한다. GitHub Issues를 쓰지 않는 프로젝트에서는 기존 local-first Wily 흐름이 그대로 동작해야 한다.

## Dependencies

- 06-3 zsh repo launcher
- 06-4 mature repo init contract
- 06-5 watch pane compaction

## Parallel Group

07

## Expected Starting Conditions

- Phase 06 work is done.
- Wily remains local-first and approval-first for remote actions.
- GitHub Issues are not assumed to exist for every project.

## Expected Output

- Wily phase metadata에서 GitHub issue 번호/URL을 선택적으로 표현하는 계약이 문서화된다.
- GitHub Issues와 Wily phase/session의 source-of-truth 경계가 명확해진다.
- GitHub issue 조회가 자동 기본 동작이 아니라 explicit request 또는 별도 command skill 후보임이 정리된다.
- GitHub 없는 프로젝트에서 영향이 없다는 테스트/문서 계약이 생긴다.

## Likely Files

- `skills/wily-workflow/SKILL.md`
- `skills/wily-workflow/references/`
- `skills/wily-next/SKILL.md`
- `tests/test_wily_command_skills.py`
- `.codex-plugin/plugin.json` only if new command skill metadata is added

## Known Risks

- GitHub 조회를 기본 command path에 넣으면 GitHub를 쓰지 않는 프로젝트가 느려지거나 불필요한 remote dependency를 갖게 된다.
- Issue body를 Wily state에 복제하면 두 source of truth가 충돌할 수 있다.
- GitHub API/CLI 호출은 remote inspection이므로 approval-first 경계를 흐리면 안 된다.

## Planner Adapter

# Planner Adapter

Recommended planner: superpowers:writing-plans

Use the planner because this phase needs a compatibility and remote-boundary contract before any GitHub command skill or helper is added.

## Prompt

# Execution Prompt

Define optional GitHub Issues linkage for Wily.

Scope:
- Keep Wily usable without GitHub Issues.
- Define optional phase metadata for issue numbers or URLs.
- Document source-of-truth boundaries: GitHub Issues for collaboration/assignment/discussion, Wily for local roadmap/session execution.
- Decide whether a future `$wily-issues` command skill should exist, but do not implement remote issue lookup unless explicitly approved.
- Keep remote inspection approval-first.
- Add focused tests for documentation and metadata contract where practical.

## Verification

# Verification

Run:

```bash
python3 -m unittest tests.test_wily_command_skills
python3 -m unittest discover
```

Manually inspect the guidance from both perspectives:

- a project that uses GitHub Issues for assignment and collaboration,
- a project that does not use GitHub Issues at all.

## Handoff

# Handoff

Start by designing the linkage contract, not by calling GitHub.

Recommended initial approach:

- Add a `github-issues-policy.md` reference under `skills/wily-workflow/references/`.
- Document optional metadata such as `github_issues: ["#123"]`, `github_url`, `owner`, and `sync_policy: "manual"`.
- Keep `$wily-status`, `$wily-next`, and `$wily-start` local-only by default.
- Treat `$wily-issues` as a future optional command skill if the contract justifies it.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.

Generate one before adding GitHub Issues policy or command guidance.
