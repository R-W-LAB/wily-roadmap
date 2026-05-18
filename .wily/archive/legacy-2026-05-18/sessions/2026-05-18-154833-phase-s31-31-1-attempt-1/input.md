# Wily Phase Context

Phase: s31/31-1 - Emit renamed event on slug change

## Phase

# 31-1: Emit renamed event on slug change

## 작업

- `wily.py`에서 slug 변경이 발생하는 경로 식별: `wily replan`, 직접 slug 수정 명령
- 변경 직전에 `.wily/local/live/active/` 디렉터리를 읽어 해당 item_id에 대한 active session_id 추출
- 매칭되는 session_id가 있으면 `renamed(session_id, old_item_id, new_item_id)` 이벤트를 `/api/live/events`로 emit
- 동시에 active/<sid>.json 파일의 `item_id` 필드 in-place 업데이트
- Board측 `app/live/events.py`에 `renamed` 이벤트 핸들러 추가: `live_items` row의 `current_item_id` 갱신

## 검증

- 테스트: s21 active 세션 중 `wily replan`으로 s22로 rename → Board에 `renamed` 이벤트 도착 + live_items.current_item_id 변경 확인
- attach resolution(s24-3에서 도입): durable webhook 도착 시 new_item_id 기준 attach 확인

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
