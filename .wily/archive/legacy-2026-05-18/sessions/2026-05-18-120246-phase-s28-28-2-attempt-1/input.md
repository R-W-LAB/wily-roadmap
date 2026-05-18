# Wily Phase Context

Phase: s28/28-2 - Remove write actions and PR mutator

## Phase

# 28-2: Remove write actions and PR mutator

PR 생성/status 변경 같은 Board UI에서 트리거되는 mutating 액션을 제거한다.

## 삭제 대상

- `app/actions/toggle_status.py`
- `app/actions/pr_writer.py`
- `app/main.py` 또는 라우터 include에서 위 모듈 import/등록 제거

## 보존

- live event 수신 엔드포인트(`/api/live/events`)는 mutating이 아니라 ingest이므로 유지

## 검증

- `grep -r "toggle_status\|pr_writer" app/` 결과 0건
- 기존 테스트 중 위 모듈에 의존하던 것은 삭제하거나 read-only assertion으로 치환

## Planner Adapter

Missing.

## Prompt

Missing.

## Verification

Missing.

## Handoff

Missing.

## Existing Implementation Plan

No implementation plan exists yet.
Use the recommended planner to create one if this phase needs a detailed plan.
