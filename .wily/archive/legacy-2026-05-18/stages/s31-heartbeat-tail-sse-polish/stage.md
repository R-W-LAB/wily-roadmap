# s31: Heartbeat 잔여 + SSE polish

## 목적

`docs/superpowers/plans/2026-05-16-wily-board-local-activity-heartbeat.md` 플랜 중 s24가 잡지 못한 마무리 항목 4개와, UI redesign spec §6.3에서 약속한 SSE 거동 정합성을 한 stage에 묶는다. s28-s30과 의존성 없는 병렬 트랙.

## 범위

- `renamed` 이벤트 emit: replan/슬러그 변경 시 attach key 안정성 보장
- `event_id` 페이로드 + 서버 `(session_id, event_id)` 5분 LRU dedup
- `WILY_BOARD_SECRETS` 듀얼 시크릿 회전 (current,previous, 7일 grace)
- `WILY_BOARD_HEARTBEAT_TTL_SECONDS=14400` env-driven 기본값
- 프론트 SSE 구독 per-page `?repo=` 필터 + exponential backoff + tab visibility 핸들링

## 비범위

- Codex Desktop bridge 자체 (s24-1/2/3에서 이미 처리됨)
- 신규 컴포넌트나 UI 변경 (s30 범위)
- HMAC 시크릿의 *생성/배포* (1Password 운영 절차는 별도 운영 stage)

## 예상 산출물

- `wily.py`에 `renamed` event 발신 + `event_id` 필드
- Board `app/live/events.py`에 dedup 로직 + `WILY_BOARD_SECRETS` 다중 키 검증
- Board `app/config.py`에 `live_heartbeat_ttl_seconds` 설정 + wily.py가 env 읽음
- Frontend `live-refresh.tsx`가 `?repo=` 쿼리 포함 + backoff + `document.visibilitychange` 핸들러
- 회귀 테스트: TTL 만료 시 사이드카 자살 + dedup + dual-secret 모두 통과
