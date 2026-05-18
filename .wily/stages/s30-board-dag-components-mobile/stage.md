# s30: Board DAG + 누락 컴포넌트 + 모바일

## 목적

UI redesign spec §5 컴포넌트 인벤토리에서 빠진 것들과 §5.4 DAG의 dagre 레이아웃 약속, §8 모바일 동작을 한 stage에 묶어 완성한다. s29의 라이브러리 인프라(Tailwind/shadcn/framer/TanStack) 위에서 자연스럽게 구현된다.

## 범위

- `stage-map.tsx`의 단순 `index * 250` 지그재그 레이아웃을 dagre 기반 레이아웃으로 교체
- Headline strip 컴포넌트 신설 (Tremor ProgressBar)
- Attention 섹션 컴포넌트 신설 (shadcn Alert, blocked + needs_review 묶음)
- 모바일 fallback: DAG → 세로 stage 리스트, rail → bottom sheet
- Repo switcher 정렬 개선 (recent + visibility split + pinned 우선), Pin이 Hub 목록 정렬에 반영

## 비범위

- 신규 라이브러리 도입 (s29에서 끝남)
- read-only invariant 회귀 테스트 (s28에서 끝남)
- Heartbeat/SSE 거동 변경 (s31 범위)

## 예상 산출물

- 의존성 기반으로 정렬된 DAG가 visual 회귀 없이 작동 (Done blob 보존)
- 레포 workspace 상단에 Headline 한 줄
- 막힘/리뷰 대기 있을 때만 Attention 카드 노출
- iPhone SE(375px) 폭에서 DAG 대신 세로 list, rail 대신 bottom sheet
- Repo switcher에서 최근/핀/visibility 정렬 확인
