# Wily Board — UI Visual Spec

이 문서는 `docs/wily-board-plan.md` §10을 *구현 가능한 수준*으로 구체화한 시각 명세서다. 빌드 PR을 만들기 전, 이 문서가 단일 출처다.

CLI 도구인 `wily-watch`와 *시각언어를 공유하지 않는다*. Wily Board는 웹 네이티브 반응형이고, watch의 ASCII rail/glyph는 정보 모델 차원에서만 참고한다.

---

## 1. 결정 요약

| 항목 | 결정 |
|---|---|
| 정보 구조 | Frontier focus — `Active right now` → `Up next` → `All repos` 순 |
| 톤 | Calm dashboard (Linear/Vercel 계열). 절제된 색, 넉넉한 여백, id만 모노 |
| 상세 페이지 | Single page per repo. Stage 카드를 세로 스택, Phase는 카드 내 서브리스트 |
| 인터랙션 | htmx 인라인 상태 토글, 페이지 새로고침 없음 |
| 쓰기 모델 | 모든 쓰기 → GitHub PR 생성(직접 commit 금지) |
| 반응형 | 데스크톱 ≥1024px 2-column, 600-1024 1-column wide, <600 모바일 compact |
| 다크모드 | `prefers-color-scheme` auto + 헤더 토글(localStorage 저장) |

---

## 2. 팔레트

CSS 변수 기반. Pico.css 위에 *얇게* 덧입힌다.

### 라이트
```css
--wb-bg:        #fafafa;     /* 페이지 배경 */
--wb-surface:   #ffffff;     /* 카드 */
--wb-surface-2: #f4f4f5;     /* 카드 위 미세 컨테이너 */
--wb-border:    #e4e4e7;     /* 경계 */
--wb-border-soft: #efeff1;
--wb-text:      #18181b;     /* 본문 */
--wb-text-muted:#71717a;     /* 보조 */
--wb-text-dim:  #a1a1aa;     /* 더 약한 보조 */
--wb-accent:    #5b8def;     /* 인터랙티브 (포커스, 링크, 토글) */
--wb-accent-soft: #e6efff;
```

### 다크
```css
--wb-bg:        #0b0c0f;
--wb-surface:   #15171c;
--wb-surface-2: #1c1e25;
--wb-border:    #2a2d36;
--wb-border-soft:#1f2228;
--wb-text:      #f4f4f5;
--wb-text-muted:#a1a1aa;
--wb-text-dim:  #71717a;
--wb-accent:    #7aa7ff;
--wb-accent-soft:#1d2a45;
```

### 상태 색

상태 색은 *작은 dot + 카드 좌측 보더 2px*에만 쓴다. 배경은 사용하지 않는다(절제).

| 상태 | dot/border | 라이트 | 다크 |
|---|---|---|---|
| done | `--wb-status-done` | `#16a34a` | `#22c55e` |
| ready | `--wb-status-ready` | `#0891b2` | `#22d3ee` |
| in_progress | `--wb-status-prog` | `#d97706` | `#f59e0b` |
| needs_review | `--wb-status-review` | `#7c3aed` | `#a78bfa` |
| blocked | `--wb-status-blocked` | `#dc2626` | `#ef4444` |
| pending | `--wb-status-pending` | `#a1a1aa` | `#71717a` |
| superseded | `--wb-status-superseded` | `#d4d4d8` | `#52525b` |

---

## 3. 타이포그래피

- **본문**: 시스템 sans (Pico 기본 stack 유지).
- **id 표기**: 별도 mono — `ui-monospace, SFMono-Regular, "JetBrains Mono", Menlo, monospace`.
- **사이즈 스케일** (rem):
  - 본문: `1.0`
  - 보조 텍스트: `0.875`
  - 메타·dim: `0.8125`
  - h1: `1.5`
  - h2(섹션 헤더): `1.125` letter-spacing `0.02em` uppercase
  - h3(카드 헤더): `1.0` semibold

### 헤딩 패턴
섹션 헤더는 *작고 차분하게*. 큰 진하게 검정 H1은 쓰지 않는다.

```
ACTIVE RIGHT NOW           ← uppercase 0.8125rem, color muted, tracking +
                              그 아래 항목들이 본 콘텐츠
```

---

## 4. 스페이싱

8px 그리드.

| 토큰 | 값 |
|---|---|
| `--sp-0` | `4px` |
| `--sp-1` | `8px` |
| `--sp-2` | `12px` |
| `--sp-3` | `16px` |
| `--sp-4` | `24px` |
| `--sp-5` | `32px` |
| `--sp-6` | `48px` |

- 카드 패딩: `--sp-3` (16px)
- 카드 사이 간격: `--sp-2` (12px)
- 섹션 사이 간격: `--sp-5` (32px)
- 컨테이너 max-width: `1100px`, 좌우 패딩 `--sp-4`

---

## 5. 컴포넌트 해부

### 5.1 TopBar

```
─────────────────────────────────────────────────
[Wily Board]                       [⌕] [☾] [@me]
─────────────────────────────────────────────────
```

- 좌: 로고/이름 (`/`로 링크). 한 줄.
- 우: 검색(추후), 다크모드 토글, 로그인 아바타+이름.
- 높이 56px, sticky, 하단 1px `--wb-border`.

### 5.2 SectionHeader

```
ACTIVE RIGHT NOW                    3 items
```

- uppercase 0.8125rem `--wb-text-muted`, letter-spacing 0.06em.
- 우측 끝에 보조 메타(개수, 필터 칩 등).
- 아래 12px 간격으로 본문.

### 5.3 ActiveCard (Frontier 항목 1개)

데스크톱 모습:
```
┌───────────────────────────────────────────────────┐
│ ● wily-roadmap     s15 · 15-6                      │
│                                                    │
│ UI implementation                                  │
│                                                    │
│ @claude                              [Open ▸]      │
└───────────────────────────────────────────────────┘
```

요소:
- 좌측 4px `--wb-status-prog` 보더(상태색).
- 상단 한 줄: `dot` + repo full name(`owner/name`) + breadcrumb id `s15 · 15-6` (mono).
- 본문 한 줄: phase title.
- 메타: assignee chip + 우측 `Open ▸` 텍스트 링크(스테이지 상세로 이동).
- hover: `box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.04)` + 살짝 위로 `transform: translateY(-1px)`.
- 폭: 1-column 또는 2-column 그리드 자동.

### 5.4 UpNextRow

리스트 형태(밀도 높음):
```
○  wily-roadmap   s16    Polish dashboard               @kokyuhyun  ›
```

- 카드보다 가벼움 — 32-40px row, 좌측 dot, mono id, title, owner, chevron.
- 호버 시 row 전체에 `--wb-surface-2` 배경.
- 필터 칩 그룹 위치: 섹션 헤더 옆.

### 5.5 RepoProgressRow

```
wily-roadmap     14 / 15     ████████████░░  93%
```

- repo full name(좌) — 진행 카운트(중앙 정렬, mono) — `<progress>` bar — 퍼센트(우, mono).
- bar: `<progress>` 사용. height 6px, border-radius 3px, fill `--wb-status-done`.
- repo의 상태가 done이면 fill 색 동일, idle이면 `--wb-text-dim`.
- "(init 필요)" 같은 메타는 회색 작은 칩으로 우측 끝에.

### 5.6 StageCard (Repo 상세 페이지)

```
┌─────────────────────────────────────────────────┐
│ ● s15  Wily Board external dashboard            │
│        1 / 7 phases     in_progress             │
│ ────────────────────────────────────────────── │
│  ● 15-1  repository contract            done    │
│  ● 15-2  azure box bootstrap            done    │
│  ◐ 15-6  UI implementation              [▼] [Open PR]  ← active 행 강조
│  ○ 15-7  multi-repo onboarding          done    │
└─────────────────────────────────────────────────┘
```

- 카드 헤더: stage dot + mono id + title. 부제로 done/total · 상태.
- 본문: Phase row 리스트. 각 row는 height 36-40px.
- frontier phase row는 미세하게 강조 (배경 `--wb-accent-soft`, 또는 좌측 2px `--wb-accent`).
- frontier가 아닌 phase row는 액션 노출 안 함, hover 시에만 인라인 액션 노출.

### 5.7 PhaseRow 인라인 액션

```
◐ 15-6  UI implementation       @claude    [in_progress ▾]  [Open PR]
```

- 상태 드롭다운: 현재 상태가 select 안의 선택값. 변경 시 자동 활성화되는 `Open PR` 버튼.
- htmx: `hx-post="/actions/phase/status"` `hx-target="closest .phase-row"` `hx-swap="outerHTML"`. 서버는 동일 row 마크업 + 토스트 partial 반환.
- 성공 시 toast: "PR opened → #123" with link.
- 실패 시: row 색 살짝 적색 깜빡, 사유 inline.

### 5.8 Toast

페이지 하단 우측 fixed, max-width 360, slide-up 200ms ease-out, auto-dismiss 6s + close 버튼.
htmx OOB swap으로 갱신.

### 5.9 EmptyState (mac2win·BounceBall처럼 `.wily/` 없는 레포)

```
┌─────────────────────────────────────────────────┐
│ mac2win                                          │
│                                                  │
│   Wily roadmap not initialized yet.              │
│   Run `$wily-init` on this repo to onboard.     │
│                                                  │
└─────────────────────────────────────────────────┘
```

- 카드 안에서 보조 텍스트만, 컬러 dim.
- 카운트는 `0 / 0`, progress bar는 표시하지 않음.

---

## 6. 반응형

### 브레이크포인트
- `--bp-sm`: 600px
- `--bp-md`: 1024px
- 컨테이너 max 1100px.

### 6.1 ≥1024 데스크톱
- 컨테이너 max-width 1100px, 중앙 정렬.
- ActiveCard 그리드: `grid-template-columns: repeat(auto-fit, minmax(360px, 1fr))` — 1100px에서는 3 cards / row.
- Repo 상세: Stage 카드를 `auto-fit, minmax(440px, 1fr)` 2-column.

### 6.2 600-1024
- 컨테이너 패딩 `--sp-3`.
- ActiveCard 그리드 자동 1-2 column.
- Stage 카드 1-column.

### 6.3 <600 모바일
- 컨테이너 패딩 `--sp-2`.
- TopBar: 로고만 + 우측 메뉴 아이콘(다크/계정 묶음 드롭다운).
- 섹션 헤더 sticky(스크롤 시 짧게 고정), 그 아래 콘텐츠.
- ActiveCard: 1-column, 카드 padding `--sp-2`.
- UpNextRow: title 줄바꿈 허용, owner는 다음 줄로.
- 터치 hit area ≥44px.
- 상태 드롭다운: full-width, 모바일에서는 `<select>`가 OS 네이티브 picker로 열리도록 유지.

---

## 7. 인터랙션 패턴

- **로딩**: 페이지 진입 시 깜빡임 없도록 view transition이 없는 정적 렌더. htmx 액션에는 `hx-indicator` SVG spinner(작게).
- **포커스**: 모든 인터랙티브 요소는 `:focus-visible`에 `outline: 2px solid var(--wb-accent); outline-offset: 2px`.
- **링크 hover**: 색 변화 + underline-offset 4px.
- **카드 hover**: 살짝 위로(translateY -1px) + soft shadow. 모바일에서는 끔.
- **드래그 앤 드롭**: 도입하지 않음(쓰기는 PR 경유라 즉시성 보장이 어렵고, 잘못된 기대를 줌).

---

## 8. 다크모드 토글

- 헤더의 ☾/☀ 토글. 클릭 시 `data-theme="light|dark|auto"`를 `<html>`에 부여 + localStorage.
- 초기 진입: localStorage 우선, 없으면 `prefers-color-scheme`.
- 토글은 *3-상태* (auto / light / dark)로 갈지 *2-상태* (light / dark)로 갈지 — 일단 **2-상태 + 첫 진입 auto 추종**.

---

## 9. 정적 자원

- Pico.css 2 CDN 그대로 유지 (이미 base.html에 있음).
- 자체 CSS는 `app/web/static/app.css` 한 파일. 변수+컴포넌트별 클래스만.
- 아이콘은 Lucide 또는 단순 SVG 인라인. 외부 폰트 패밀리 추가 없음.

---

## 10. 변경 영향 (Codex 스텁 → 신규)

| 파일 | 변경 |
|---|---|
| `app/web/templates/base.html` | TopBar 변경, 다크 토글, 컨테이너 클래스 정리 |
| `app/web/templates/board.html` | 전면 재작성(Frontier 3섹션) |
| `app/web/templates/repo_detail.html` | 전면 재작성(단일 페이지, Stage 카드 스택) |
| `app/web/templates/stage_detail.html` | 제거 또는 anchor 리다이렉트(/repos/.../stages/x → /repos/.../#x) |
| `app/web/templates/phase_card.html` | row 형태로 재작성 + htmx attributes |
| `app/web/templates/_toast.html` | 신규 (htmx OOB) |
| `app/web/static/app.css` | 변수+컴포넌트 전면 작성 |
| `app/web/routes.py` | 상세 페이지 통합, htmx 응답 분기, toast partial |
| `app/actions/toggle_status.py` | 응답 포맷에 row partial + toast OOB 추가 |

---

## 11. 미래 테마(R-W-LAB 컨셉) 호환성

이 베이스는 추후 *Right 박사 + Wily 박사의 연구소* 분위기로 전면 테마 교체될 예정이다. 그 교체가 *추가 작업 없이 변수 스왑만으로* 가능하도록 다음 규칙을 지킨다.

1. **모든 색·폰트·보더·그림자는 CSS 변수로만 정의**. 템플릿에 hex 박지 않는다.
2. **컴포넌트 클래스는 의미 기반**으로 명명 (`.stage-card`, `.phase-row`, `.active-card`). 톤 종속 명명(`.calm-*`) 금지.
3. **테마 분기는 `data-theme` 속성**으로. 예: `<html data-theme="calm">` (기본), 미래에 `data-theme="lab"` 추가 시 동일 마크업 그대로.
4. **테마별 자산(아이콘·폰트)은 별도 파일**에 격리. base에는 공용 자산만.
5. **레이아웃(그리드·간격·반응형 브레이크포인트)은 톤 중립**으로. 테마 교체 시 레이아웃 변경 0.

후보 테마 방향(추후 결정):
- *Blueprint console* — deep navy + cyan grid + 도면 패널
- *Lab notebook* — 크림 페이퍼 + 손그림 보더 + serif
- *CRT terminal* — 8-bit 색 + 스캔라인
- *Robot rack* — 브러시드 메탈 + 리벳 + LED dot

이 단계에선 빌드 안 함. 기록만.

---

## 12. 검증 기준 (수동 + 자동)

- 데스크톱 1280px 너비에서 Frontier 화면이 1 스크린에 안 잘리고 들어옴 (Active 3개 + Up next 4개 + Repo 4개 기준).
- 모바일 360px 너비에서 모든 카드가 가독성 유지, hit area 44px+.
- 라이트/다크 두 모드 전환 시 깜빡임 없음.
- htmx 인라인 토글 후 같은 화면에서 row 갱신 + toast 표출.
- 키보드 탐색: Tab으로 Frontier → Up next → Repo progress → Stage → Phase action 순회 가능, focus ring 보임.
- Lighthouse mobile 점수 Performance ≥90, Accessibility ≥95 목표.
