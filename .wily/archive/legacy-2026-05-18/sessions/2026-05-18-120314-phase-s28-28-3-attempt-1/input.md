# Wily Phase Context

Phase: s28/28-3 - Route cutover to Next.js only

## Phase

# 28-3: Route cutover to Next.js only

`/` 라우트의 Jinja 응답을 제거하고, 사용자가 어떤 경로로 진입하든 Next.js 프론트로만 도달하게 한다.

## 작업

- `app/web/routes.py`의 `/` 핸들러 삭제 또는 `RedirectResponse("/", ...)` to Next.js host
- 단순화 방안: `app/web/routes.py` 전체 모듈 삭제 + `app/main.py`의 `include_router(web_router())` 제거
- 리버스 프록시(nginx/Caddy/Cloudflare 등) 설정 확인:
  - `/api/*`, `/sse/*`, `/auth/*` → FastAPI (port 8000)
  - 그 외 → Next.js (port 3000)
- `next.config.ts`의 `rewrites()`가 dev에서도 동일하게 작동하는지 확인

## 검증

- 브라우저로 `/` 진입 시 Next.js `/me` UI만 보임
- `curl -I /` 응답이 Next.js 헤더(또는 redirect)
- 로그인 흐름이 OAuth → cookie → Next.js 화면까지 깨지지 않음

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
