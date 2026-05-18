# 29-2: Migrate custom UI to shadcn primitives

## 교체 매핑

| 현재 | shadcn primitive |
|---|---|
| `dialog-overlay` div + 직접 mount (repo-switcher) | `<Dialog>` / `<CommandDialog>` |
| `local-desk.tsx`의 collapse 패턴 | `<Sheet side="right">` + 자체 `<Collapsible>` |
| Attention chip 묶음 (이후 s30 Attention 컴포넌트 대비) | `<Alert variant="warning">` 베이스 |
| `chip` 클래스 산재 | `<Badge variant="secondary|outline">` |
| `icon-button` | `<Button variant="ghost" size="icon">` |
| Pin 동작 시 표시할 메시지 | `<Tooltip>` |

## 검증

- 기존 호출부 API 거의 동일 (예: `<LocalDesk repo={...} desk={...} />` 시그니처 유지)
- 접근성: focus ring, ESC 닫기, aria-label 모두 shadcn 기본으로 충족
- dark mode 정상
