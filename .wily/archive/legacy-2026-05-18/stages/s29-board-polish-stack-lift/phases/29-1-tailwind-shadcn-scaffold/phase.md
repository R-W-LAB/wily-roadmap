# 29-1: Tailwind + shadcn/ui scaffold + token mapping

## 작업

1. `pnpm add -D tailwindcss postcss autoprefixer` + `pnpm dlx shadcn@latest init`
2. `tailwind.config.ts`에 `--wb-*` 변수 → theme.colors 매핑 (spec §9 sketch 사용)
3. `globals.css`를 Tailwind directives + `:root` 변수 + 다크모드 `[data-theme="dark"]` 변수만 남기는 thin layer로 축소
4. `frontend/components.json` 생성, default style "new-york"
5. 빌드 통과 + 기존 페이지 외관 깨지지 않음 확인

## 검증

- `pnpm build` 통과
- 첫 페인트가 기존과 동일하거나 더 깔끔
- 다음 phase에서 shadcn `pnpm dlx shadcn add sheet dialog alert tooltip badge button` 실행 가능한 상태
