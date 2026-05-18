# 31-3: Dual HMAC secret rotation

## 작업

- Board `app/config.py`에서 `WILY_BOARD_SECRET` 단일에 더해 `WILY_BOARD_SECRETS` (comma-separated) 환경변수 지원
- 둘 다 있으면 secrets list = SECRETS.split(",") + [SECRET]; dedupe
- HMAC 검증: payload signature를 secrets 리스트의 *어느 하나*와 일치하면 통과
- 우선순위: SECRETS 첫 값이 current로 간주, 그 뒤가 previous

## 운영 문서

- `docs/OPERATIONS.md` (또는 board 운영 문서)에 rotation 절차 추가:
  1. 새 시크릿 생성 (`openssl rand -hex 32`)
  2. 새 시크릿을 Board의 `WILY_BOARD_SECRETS`에 prepend → `new,old`
  3. 7일 대기하면서 모든 사용자가 1Password에서 새 키 동기화
  4. 7일 후 `WILY_BOARD_SECRETS`에서 old 제거 → `new`
  5. 1Password 공유 항목의 description에 마지막 rotation 일자 기록
- 손상 의심 시 즉시 회전 절차 별도 명시

## 검증

- pytest: 두 시크릿 모두 valid HMAC을 검증
- pytest: invalid HMAC은 둘 다 거부
- 통합: dev 환경에서 키를 prepend한 뒤 기존 wily 사이드카가 그대로 동작
