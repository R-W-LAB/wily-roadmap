# 30-2: Headline strip + Tremor progress

## 작업

- `pnpm add @tremor/react`
- `frontend/components/headline.tsx` 신설
- 레이아웃: 한 줄, 좌측에 `{owner}/{name} · {done}/{total} stages`, 가운데 Tremor `<ProgressBar value={percent} color="emerald" />`, 우측에 `{remaining} left · {user_active_phase?}`
- repo workspace page(`/repos/[owner]/[name]/page.tsx`) 최상단(DAG 위)에 mount
- ETA는 spec §5.7대로 "wily next에 cost estimate가 있을 때만" — 없으면 omit

## 검증

- 모든 status 색상이 design token으로
- 0/N (init 필요 상태)에서도 안 깨짐
- Tremor가 Tailwind와 잘 공존하는지(이미 Tailwind 의존)
