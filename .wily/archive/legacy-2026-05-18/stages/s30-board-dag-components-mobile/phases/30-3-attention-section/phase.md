# 30-3: Attention section component

## 작업

- `frontend/components/attention.tsx` 신설
- 입력: 현재 repo의 stages → blocked status + needs_review status인 phase들을 추출
- 비어있으면 컴포넌트 자체 미렌더 (null return)
- 비어있지 않으면 shadcn `<Alert variant="destructive">` 또는 `variant="default">`로 묶음 카드
- 각 항목: 상태 아이콘 + `s{stage}/p{phase}` + 짧은 reason
- repo workspace page의 DAG 아래 또는 Headline 아래에 배치 (spec §5.8: "DAG 아래" 기본)

## 검증

- 빈 상태에서 DOM에 노출 0
- 막힘 1개 이상 시 카드 노출, 클릭 시 해당 phase로 anchor
- dark mode 정상
