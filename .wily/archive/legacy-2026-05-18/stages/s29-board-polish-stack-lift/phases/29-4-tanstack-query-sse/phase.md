# 29-4: TanStack Query + SSE key-based invalidation

## 작업

1. `pnpm add @tanstack/react-query`
2. App Router의 최상단 `<QueryClientProvider>` (Next.js App Router용 `react-query` 셋업 가이드 따름)
3. `lib/api.ts`의 fetch 함수들을 query hook으로 wrapping (`useDesk()`, `useRepoDetail()`, etc.)
4. `live-refresh.tsx`의 SSE 핸들러 변경:

```ts
source.addEventListener("live_item.updated", (event) => {
  const data = JSON.parse(event.data);
  queryClient.invalidateQueries({ queryKey: ["repo", data.repo.owner, data.repo.name] });
  queryClient.invalidateQueries({ queryKey: ["desk"] });
});
```

5. `router.refresh()` 호출 제거 — 더 이상 전체 페이지 재페치 불필요

## 검증

- 한 stage가 working으로 바뀌었을 때 해당 DAG 노드와 사이드 rail만 갱신 (전체 페이지 리렌더 없음 확인 — React DevTools Profiler)
- 다른 페이지에서 발생한 이벤트는 현재 페이지 쿼리에 영향 없음
- 연결 끊김 시 sonner toast 그대로 작동
