# Wily Board 실시간 작업 현황 Overlay 검토 문서

## 결론 먼저

이 기능은 하는 것이 맞다.

다만 Board가 Git 상태를 대체하면 안 된다. Board는 두 층을 같이 보여줘야 한다.

- **공식 상태**: GitHub default branch의 `.wily/`에서 동기화된 상태
- **실시간 작업 현황**: 각 로컬 Wily CLI가 Board에 보내는 임시 상태

즉, push 전 작업은 Board에 보여주되 `done` 같은 공식 완료로 취급하지 않는다. push 전 완료는 `locally completed - awaiting push`처럼 표시한다.

## 왜 필요한가

지금 Board는 GitHub에 push된 `.wily/` 상태만 볼 수 있다. 그래서 누군가 `$wily-start`로 작업을 잡아도 push 전까지는 다른 사람이 알 수 없다.

협업에서는 이 공백이 크다.

- 같은 Phase를 두 사람이 동시에 잡을 수 있다.
- 누가 막혔는지 늦게 안다.
- 로컬에서는 끝났지만 push가 안 된 작업을 다른 사람이 다시 시작할 수 있다.
- Board가 “현재 작업판”이 아니라 “push 후 기록판”처럼 보인다.

Live overlay는 이 공백을 줄인다.

## 핵심 원칙

### 1. `.wily/`가 source of truth다

공식 로드맵 상태는 계속 `.wily/roadmap.yaml`과 `.wily/**/stage.yaml`이다.

Board의 live state는 협업 신호다. 편리하지만 최종 기록은 아니다.

### 2. push 전 상태는 provisional이다

`$wily-complete`가 로컬에서 성공해도 Board는 바로 공식 `done`으로 보이면 안 된다.

올바른 표시는 다음과 같다.

```text
durable status: pending 또는 in_progress
live overlay: completed locally - awaiting push
```

GitHub sync가 `.wily`의 `done`을 확인한 뒤에야 공식 완료로 반영한다.

### 3. 원격 전송은 opt-in이다

Wily CLI는 기본적으로 지금처럼 로컬만 수정한다.

Board live sync는 아래 설정이 있을 때만 켠다.

- `WILY_BOARD_URL`
- `WILY_BOARD_SECRET`
- `WILY_BOARD_REPO`
- `WILY_BOARD_ACTOR`

설정이 없으면 `$wily-start`, `$wily-complete`, `$wily-block`은 현재와 똑같이 동작한다.

### 4. Board 장애가 Wily 작업을 막으면 안 된다

Board가 죽었거나 네트워크가 실패해도 Wily 명령은 실패하면 안 된다.

Live event 전송은 best-effort다.

## 사용 흐름

### `$wily-start 16-1`

로컬:

- `.wily` session 생성
- Phase 상태를 로컬에서 `in_progress`로 변경

Board:

```text
airmang working locally
last seen now
```

다른 사람은 push 전에도 누가 작업을 잡았는지 볼 수 있다.

### 작업 중

첫 구현에서는 별도 heartbeat를 꼭 넣지 않는다.

명령 실행 시점의 이벤트만 보낸다.

나중에 필요하면 `wily live-heartbeat` 또는 `wily watch --board-heartbeat` 같은 방식으로 확장한다.

### `$wily-block 16-1 "API auth unclear"`

로컬:

- `.wily`에 blocker 기록

Board:

```text
blocked locally
API auth unclear
```

GitHub sync 전까지는 로컬 blocker로 표시한다.

### `$wily-complete 16-1`

로컬:

- `.wily` 상태를 `done`으로 변경
- session을 verified로 기록

Board:

```text
completed locally - awaiting push
```

이 상태는 “끝났다고 주장함”이지 “공식 완료”가 아니다.

### push 이후

기존 GitHub Actions workflow가 Board webhook을 호출한다.

Board가 GitHub에서 `.wily`를 다시 읽고 durable status가 `done`임을 확인하면 live overlay를 지운다.

## Board에 추가할 것

### API

새 endpoint:

```text
POST /api/live/events
```

기존 webhook과 같은 HMAC 서명 방식을 쓴다.

```text
X-Wily-Signature: sha256=<hmac>
```

### DB

새 테이블:

```text
live_sessions
```

저장할 값:

- repo
- phase id
- stage id
- actor
- session path
- live status
- note
- first seen
- last seen
- cleared at
- raw payload

기존 durable stage/phase 테이블은 live event가 직접 수정하지 않는다.

### UI

Phase row에서 공식 상태와 live overlay를 분리해서 보여준다.

예시:

```text
16-1  Add live overlay API        pending
      airmang working locally
```

```text
16-1  Add live overlay API        in_progress
      completed locally - awaiting push
```

공식 status dot은 durable state 기준으로 유지한다. Live chip은 더 약한 시각 요소로 둔다.

## Stale 처리

실시간 상태는 오래되면 신뢰도가 떨어진다.

기본 기준:

- 2분 이내: fresh
- 5분 초과: stale

fresh 상태는 `Active right now`에 보인다.

stale 상태는 상세 페이지에는 남기되, `Up next`에서 다른 사람이 잡는 것을 막지 않는다.

## 충돌 처리

충돌은 막는 것보다 보이게 하는 쪽이 맞다.

예시:

- 두 사람이 같은 phase를 잡음
- 한 사람은 `completed locally`, Git 상태는 아직 `pending`
- durable 상태는 `done`인데 오래된 heartbeat가 계속 들어옴

처리 원칙:

- 공식 progress 계산은 durable state만 사용한다.
- live overlay는 별도 chip으로 보여준다.
- 같은 phase를 여러 사람이 잡으면 여러 actor를 표시한다.
- durable state가 `done`이 되면 오래된 session heartbeat는 무시한다.

## 리스크

### Secret 범위

첫 버전은 `WILY_BOARD_SECRET`을 재사용한다.

빠르게 구현하기에는 좋지만, 장기적으로는 per-user 또는 per-repo live token이 더 안전하다.

판단:

- 개인/소규모 협업이면 첫 버전에서 재사용 가능
- 외부 사용자가 늘어나면 token 분리 필요

### “완료” 오해

push 전 `completed_local`을 너무 강하게 표시하면 공식 완료처럼 오해할 수 있다.

UI 문구는 반드시 `awaiting push`를 포함해야 한다.

### Heartbeat 범위

진짜 실시간을 만들려면 heartbeat가 필요하다.

하지만 첫 버전에서 background process까지 넣으면 복잡도가 올라간다. 우선 `$wily-start`, `$wily-block`, `$wily-complete` 이벤트만으로 충분히 가치가 있다.

## 추천 구현 순서

1. Board에 `live_sessions` 테이블과 `/api/live/events` 추가
2. Board query에 live overlay join 추가
3. UI에 live chip 추가
4. Wily CLI에 live event helper 추가
5. `$wily-start`, `$wily-block`, `$wily-complete`에서 best-effort 전송
6. push 후 GitHub sync가 overlay를 clear하는 로직 추가
7. 로컬 Board에서 start, block, complete, push-clear 흐름 검증

## 구현하지 않을 것

첫 버전에서는 하지 않는다.

- Board를 공식 source of truth로 만들기
- Wily CLI가 자동 push하기
- background heartbeat daemon 만들기
- MCP server나 app integration 추가하기
- push 전 완료를 공식 `done`으로 계산하기

## 판단 기준

이 설계가 맞으려면 다음 문장이 맞아야 한다.

> Board는 누가 지금 무엇을 하고 있는지 즉시 보여준다. 하지만 공식 로드맵 진행률은 Git에 기록된 `.wily`만 믿는다.

이 문장이 제품 방향과 맞으면 구현해도 된다.
