# s27: Wily Roadmap 대규모 리팩토링

## 목적

Wily Roadmap plugin을 누적 패치 중심 구조에서 장기 유지보수가 가능한 구조로 재정렬한다. CLI, skill 계약, Board live reflection, roadmap state model, test isolation, cache/update 흐름을 함께 검토해 서로 충돌하지 않는 운영 모델로 정리한다.

## 범위

- `scripts/wily.py`의 command surface와 helper boundaries를 재검토한다.
- state-changing command와 read-only command의 책임을 명확히 분리한다.
- Board live/provisional reflection 모델을 재정의한다. 특히 replan, task candidate, direct Stage draft, decomposed Stage draft를 구분한다.
- `.wily` durable state, `.wily/local`, `agent-handoffs/`, installed plugin cache의 source-of-truth 관계를 정리한다.
- skill 문서와 command docs의 중복을 줄이고, 상세 정책은 references로 이동한다.
- 테스트가 사용자 홈 config, production Board config, local cache 상태에 흔들리지 않도록 격리한다.
- plugin update/release 경로와 cache sync 검증을 명확히 한다.

## 비범위

- 새 hooks, MCP servers, app integrations를 추가하지 않는다.
- Board를 durable roadmap source of truth로 만들지 않는다.
- production deploy, GitHub remote mutation, destructive cleanup은 명시적 승인 없이 하지 않는다.
- 완료된 s01-s24 이력은 재작성하지 않는다.

## 예상 산출물

- 리팩토링 설계 또는 실행 패키지.
- 필요하면 Stage-local Phase decomposition.
- CLI/skill/docs/test 변경.
- fresh verification evidence.
