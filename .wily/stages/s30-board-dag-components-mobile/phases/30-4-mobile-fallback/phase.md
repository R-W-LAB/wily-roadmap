# 30-4: Mobile fallback (DAG vertical list + bottom sheet rail)

## 작업

- viewport <600px 감지: `useMediaQuery('(max-width: 599px)')` (shadcn 또는 자체 hook)
- DAG 분기:
  - 데스크톱: 기존 react-flow 컴포넌트
  - 모바일: `<StageVerticalList>` 신설 — 위에서 아래로 stage 순차 표시, status dot/색/live chip 동일, Done은 collapsed 그룹
- Local Desk rail 분기:
  - 데스크톱: 기존 expandable rail (s29의 shadcn `<Sheet side="right">`)
  - 모바일: rail 자체 hidden, 상단 sticky `<Button>⚡ N` 배지가 `<Sheet side="bottom">` 열기
- 시트 콘텐츠는 데스크톱 rail과 동일한 Desk 컴포넌트 재사용
- 모든 인터랙티브 hit area ≥44px

## 검증

- iPhone SE(375px) 폭에서 DAG 대신 세로 list 정상 렌더
- 모바일 bottom sheet swipe down으로 닫힘
- 회전 시(landscape 600px+) 데스크톱 레이아웃으로 자연 전환
