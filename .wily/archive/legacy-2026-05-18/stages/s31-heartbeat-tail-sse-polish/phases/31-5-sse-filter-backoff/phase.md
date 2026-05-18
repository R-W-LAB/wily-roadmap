# 31-5: SSE per-page filter + backoff + tab focus

## per-page 구독 필터

- `live-refresh.tsx` 또는 후속 query hook에서 EventSource URL에 `?repo=owner/name` 쿼리 추가
- 서버 `/api/sse/live` 핸들러가 쿼리 파라미터 받으면 해당 repo 이벤트만 push
- Hub(`/me`) 페이지는 필터 없이 모든 visible repo 이벤트 수신 (기존 동작)

## exponential backoff

- 기본 EventSource는 3s fixed retry — 이를 무력화하기 위해 `source.onerror` 시 manual `source.close()` 후 setTimeout으로 재연결
- 시퀀스: 1s → 2s → 5s → 15s → 15s ... (15s에 cap)
- 성공적으로 open되면 backoff 카운터 reset
- 5회 이상 실패하면 sonner toast "Connection lost — refresh page" (자동 재시도는 유지)

## tab visibility

- `document.addEventListener("visibilitychange", ...)`:
  - hidden 진입 시 `source.close()` (대역폭/배터리 절약)
  - visible 복귀 시 `queryClient.invalidateQueries()` 한 번 + 재연결
- 모바일에서 백그라운드 → 포어그라운드 복귀 시 상태가 즉시 fresh

## 검증

- repo workspace에서 DevTools Network → `?repo=` 쿼리 확인
- 백엔드 셧다운 후 backoff 시퀀스 (DevTools Network에서 1/2/5/15 간격 확인)
- 탭 백그라운드 → 30초 → 포어그라운드 복귀 시 1회 재연결 + 데이터 fresh
