# 29-5: Themes, dates, markdown, openapi-typescript

## next-themes

- `pnpm add next-themes`
- `app/layout.tsx`에 `<ThemeProvider attribute="data-theme" defaultTheme="system">`
- 기존 `components/theme-toggle.tsx` 제거하고 next-themes 권장 패턴으로 교체
- 첫 진입 FOUC 0 (서버에서 cookie 또는 prefers-color-scheme 기반 SSR)

## date-fns + ko

- `pnpm add date-fns`
- `lib/format.ts`의 시간 포맷 함수를 `formatDistanceToNow(date, { locale: ko, addSuffix: true })`로 교체
- 출력 예: "3분 전", "방금"

## react-markdown + sanitize

- `pnpm add react-markdown rehype-sanitize`
- `components/phase-list.tsx`의 `{phase.task && <p>{phase.task}</p>}` 부분을 마크다운 렌더로 변경
- `rehype-sanitize`로 raw HTML/스크립트 차단

## openapi-typescript

- `pnpm add -D openapi-typescript`
- FastAPI가 OpenAPI 스펙을 노출하는 엔드포인트 확인(`/openapi.json` 기본)
- `frontend/package.json` script 추가:
  ```
  "types:generate": "openapi-typescript http://127.0.0.1:8000/openapi.json -o lib/api-types.ts"
  ```
- `lib/types.ts`의 manual type을 `lib/api-types.ts`의 generated namespace 참조로 교체
- CI에 `types:generate` 실행 후 diff 없음을 검증하는 단계 추가 (drift 방지)

## 검증

- 다크모드 첫 진입 깜빡임 0
- 한국어 상대시간 출력
- markdown phase task에 코드블록/링크/볼드 적용됨, `<script>` 차단됨
- 백엔드 모델 한 필드 추가했을 때 `types:generate` 다시 돌리면 자동 반영
