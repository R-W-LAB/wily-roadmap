# 29-3: framer-motion transitions

## 적용 지점

- **Local Desk rail 펼침/접힘**: `<motion.aside animate={{ width: collapsed ? 56 : 320 }}>`
- **Stage 노드 enter/exit**: SSE로 stage 추가/삭제 시 fade + scale (react-flow 노드는 `nodeOrigin`과 `<AnimatePresence>` 조합)
- **Done blob 펼침**: blob → N개 노드로 변할 때 layout transition
- **Toast slide-in**: sonner 자체가 트랜지션 가지지만, 필요시 한 줄로 motion override
- **MY DESK 항목 staggered enter**: 첫 진입 시 0.05s 간격으로 페이드 인

## prefers-reduced-motion

- 모든 motion 컴포넌트는 `useReducedMotion()` 또는 `transition={{ duration: prefersReducedMotion ? 0 : 0.2 }}`
- 전역 reset 한 곳에서 처리

## 검증

- DevTools에서 "Emulate prefers-reduced-motion: reduce" 토글했을 때 모든 애니메이션 즉시 정지
- Lighthouse Performance 점수 떨어지지 않음
