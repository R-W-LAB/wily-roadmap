# Wily Phase Context

Phase: s31/31-2 - event_id payload + server dedup

## Phase

# 31-2: event_id payload + server dedup

## 클라이언트(wily.py)

- 모든 live event payload에 `event_id` 필드 추가 — Python `ulid` 패키지 또는 stdlib UUID7
- 같은 event를 재시도할 때(네트워크 flaky) 동일 event_id 재사용
- backoff retry 자체는 best-effort 로직 유지

## 서버(app/live/events.py)

- 처리 전 `(session_id, event_id)` 5분 LRU 캐시 조회
- 중복이면 200 OK + JSON body `{"dedup": true}` 반환 + DB write skip
- LRU 구현: 메모리 dict + 만료 정리(threading.Timer 또는 lazy expiry)
- 캐시 크기 상한 (예: 10,000개) — 초과 시 oldest 제거

## 검증

- pytest: 동일 event_id로 두 번 POST → 두 번째는 dedup 응답 + DB row 1개
- 5분 + 1초 후 동일 event_id → 새 row 생성 (만료 확인)
- 다른 session_id + 동일 event_id → 별개로 처리

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
