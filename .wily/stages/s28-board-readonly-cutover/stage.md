# s28: Board read-only cutover + 레거시 제거

## 목적

UI redesign spec(`docs/superpowers/specs/2026-05-16-wily-board-ui-redesign-design.md`)이 명시한 "Board는 read-only" 원칙을 코드 레벨에서 실제로 실행한다. Next.js 프론트는 이미 살아있지만 레거시 Jinja 템플릿과 PR/status mutating 라우트가 그대로 남아있어, 누가 직접 `/`로 진입하면 여전히 mutating UI가 노출되는 상태다. Spec §10 Phase F/G(cutover + cleanup)를 실제로 실행한다.

## 범위

- `app/web/templates/{board,repo_detail,_phase_row,base,_toast}.html` 삭제
- `app/actions/{toggle_status,pr_writer}.py` 삭제 + 관련 라우트/import 정리
- `app/web/routes.py`의 `/` Jinja 응답 제거 또는 Next.js로 redirect
- 리버스 프록시 라우팅 점검: `/api/*` → FastAPI, 그 외 → Next.js
- mutating endpoint 부재를 보장하는 회귀 테스트(백엔드 + 프론트엔드 스모크)

## 비범위

- Next.js 프론트의 폴리시(s29 범위)
- DAG 레이아웃 교체나 추가 컴포넌트(s30 범위)
- live event 수신 endpoint(`/api/live/events`)는 read-only 원칙과 충돌하지 않으므로 유지
- production 배포는 본 stage 검증 통과 후 별도 승인 단계

## 예상 산출물

- Jinja 템플릿/액션 파일 삭제 PR
- `/` 라우트가 Next.js로만 도달하는 라우팅 패치
- 백엔드 회귀 테스트: 모든 라우트 enumerate해서 mutating handler 0 확인
- 프론트엔드 스모크: `/`, `/repos/owner/name`에 status select/Open PR 미존재 확인
