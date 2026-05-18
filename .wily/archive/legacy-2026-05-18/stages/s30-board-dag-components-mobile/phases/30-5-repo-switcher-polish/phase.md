# 30-5: Repo switcher and pin polish

## Repo switcher

- 현재 `repo-switcher.tsx`는 `[...payload.shared, ...payload.personal]`로 flat 정렬
- 변경:
  - 최근 방문한 repo (localStorage `wily.board.recentRepos`)를 최상단에 별도 그룹
  - 그 아래 `<Command.Group heading="Shared">` + `<Command.Group heading="Personal">`
  - 핀한 repo는 각 그룹 내 상단 + 별 아이콘
  - 검색은 그룹 무관하게 fuzzy match (cmdk 기본)

## Hub 페이지 repo 목록 정렬

- `app/me/page.tsx`에서 `RepoGroup`에 전달되는 repos를 pinned-first로 정렬
- 핀 토글이 trigger되면 즉시 정렬 갱신 (TanStack Query invalidation 또는 local state)

## 최근 방문 기록

- 각 repo workspace page 진입 시 `localStorage.recentRepos`에 unshift (max 10)
- 이미 있으면 중복 제거 후 맨 앞으로

## 검증

- ⌘K → 최근 본 repo 1개가 최상단
- Hub에서 ★ 토글 즉시 정렬 반영
- localStorage 비어있어도 정상 작동
