# Wily Phase Context

Phase: 06-3 - zsh 레포 단독 실행 명령 제공

## Phase

# Phase 06-3: zsh 레포 단독 실행 명령 제공

## Purpose

레포 안에서 zsh 환경으로 간단한 단독 명령을 실행해 Wily 상태나 watch를 켤 수 있게 한다.

## Expected Starting Conditions

- Phase 05 is done.
- `scripts/wily.py` command behavior is stable.

## Likely Files

- `scripts/`
- `tools/` if a wrapper script is needed
- `README.md` or skill references
- `tests/test_wily_cli.py`
- `tests/test_wily_command_skills.py`

## Completion Criteria

- 레포 루트에서 복잡한 경로 없이 실행 가능한 단일 명령 또는 wrapper가 제공된다.
- zsh에서 동작하는 사용법이 문서화된다.
- 명령은 local-first이고 원격/destructive 작업을 수행하지 않는다.
- 테스트가 wrapper 또는 documented command contract를 검증한다.

## Known Risks

- shell alias, PATH 설치, plugin packaging의 책임 경계를 섞으면 유지보수가 어려워진다.
- 사용자의 shell 환경을 변경하는 방식은 approval-first로 남겨야 한다.

## Planner Adapter

# Planner Adapter

Recommended planner: superpowers:writing-plans

Use the planner to choose whether this should be a checked-in wrapper script, documented alias, or both.

## Prompt

# Execution Prompt

Provide a simple repo-local zsh command for Wily.

Scope:
- Decide the minimal command surface for repo-local usage.
- Prefer deterministic checked-in scripts over modifying user shell startup files.
- Document zsh usage.
- Add focused tests for script behavior or documented command paths.

## Verification

# Verification

Run:

```bash
python3 -m unittest tests.test_wily_cli tests.test_wily_command_skills
python3 -m unittest discover
```

Also run the chosen command manually from the repository root in zsh-compatible form.

## Handoff

# Handoff

Start by listing current ways to run Wily from the repo and identifying the shortest safe zsh command to support.

This phase can run in parallel with phases 06-1, 06-2, 06-4, and 06-5.

## Existing Implementation Plan

# Implementation Plan

No detailed implementation plan exists yet.

Generate one before adding or documenting a launcher.
