# 30-1: react-flow dagre layout

## 작업

- `pnpm add dagre @types/dagre`
- `stage-map.tsx`의 `layoutStages` 함수에서 `position: { x: index * 250, y: index % 2 === 0 ? 40 : 160 }` 제거
- dagre graph 구성 → `dagre.layout(g)` → 각 노드/엣지 좌표를 react-flow 형식으로 변환
- 노드 폭/높이는 측정값(`useNodesInitialized`) 또는 기본 사이즈로 초기화
- Done blob도 단일 노드로 그래프에 포함
- 의존성 화살표가 한 방향(left-to-right or top-down)으로 흐르도록 `rankdir: "LR"` 설정

## 검증

- 20+ stage 시나리오에서 엣지 교차 없거나 최소
- Done blob 클릭 시 펼침 + dagre 재계산 → smooth 트랜지션 (s29의 framer 활용)
- minimap 비례 정상
- 모바일은 본 phase에서 처리하지 않고 30-4에서 fallback
