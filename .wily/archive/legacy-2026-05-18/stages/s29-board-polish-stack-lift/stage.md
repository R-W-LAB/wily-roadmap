# s29: Board polish stack lift

## 목적

UI redesign spec(`docs/superpowers/specs/2026-05-16-wily-board-ui-redesign-design.md`) §4가 약속한 Linear-tier 폴리시를 실제로 가능하게 만드는 라이브러리 인프라를 들여온다. 현재 frontend는 vanilla CSS + 수제 dialog로 작동은 하지만, spec이 약속한 shadcn/ui, framer-motion, TanStack Query, next-themes 등이 빠져있어 "멋진 대시보드"의 천장이 낮다.

## 범위

- Tailwind CSS + shadcn/ui 스캐폴드, `--wb-*` 변수의 Tailwind theme 매핑
- 수제 dialog-overlay, rail, chip 등을 shadcn Sheet/Dialog/Alert/Tooltip/Badge/Button으로 교체
- framer-motion 도입: rail 슬라이드, 노드 enter/exit, Done blob 펼침, 토스트 슬라이드
- `prefers-reduced-motion` 전역 존중
- @tanstack/react-query 도입: SSE event를 key 단위 invalidation으로 변환(`router.refresh()` 전체 재페치 제거)
- next-themes 도입(FOUC 해소)
- date-fns + ko locale로 상대시간 ("3분 전")
- react-markdown + rehype-sanitize로 phase task 본문 마크다운 렌더
- openapi-typescript 파이프라인: FastAPI Pydantic → 프론트 `lib/types.ts` 자동 생성

## 비범위

- 새 컴포넌트(Headline, Attention 등) 추가는 s30 범위
- DAG 레이아웃 교체는 s30 범위
- 모바일 fallback은 s30 범위
- 백엔드 API 시그니처 변경 (openapi-typescript는 기존 시그니처를 단순히 type으로 변환)

## 예상 산출물

- `frontend/package.json`에 신규 deps: tailwindcss, shadcn/ui (postinstall된 컴포넌트들), framer-motion, @tanstack/react-query, next-themes, date-fns, react-markdown, rehype-sanitize, openapi-typescript
- `frontend/tailwind.config.ts` + `frontend/components.json`(shadcn 설정) + `frontend/components/ui/*` (shadcn 생성)
- 기존 컴포넌트(local-desk, repo-switcher, theme-toggle, desk, phase-list)가 shadcn primitive 위에서 작동
- SSE 핸들러가 `queryClient.invalidateQueries({ queryKey: [...] })` 호출
- 빌드 통과, dev server 동작, dark/light 토글 깜빡임 없음
