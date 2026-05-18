# s26: Wily Roadmap plugin 개선 및 정리

## 목적

Wily Roadmap plugin을 실제 사용하면서 드러난 유지보수 비용을 줄인다. 특히 plugin cache 반영, skill/command 문서 일관성, 테스트 환경 격리, handoff 운영 방식, update/release 흐름을 정리해서 다음 변경 때 더 빠르고 안전하게 움직일 수 있게 만든다.

## 범위

- 설치된 plugin cache와 marketplace source를 맞추는 절차를 문서화하거나 helper로 정리한다.
- 상태 변경형 skill과 command 문서가 Board reflection, local-first, approval-first 계약을 일관되게 따르는지 점검한다.
- 테스트가 사용자 홈 설정이나 production Board config에 흔들리지 않도록 격리 패턴을 정리한다.
- `agent-handoffs/`와 `.wily/revisions/`의 운영 기준을 다듬어 어떤 파일을 커밋하고 어떤 파일을 로컬로 남길지 명확히 한다.
- `wily-update`, plugin marketplace metadata, README, release guidance를 점검해 업데이트 가능성을 유지한다.
- 반복되는 검증 명령과 regression 체크를 명확히 한다.

## 비범위

- 새 hooks, MCP servers, app integrations를 추가하지 않는다.
- Board를 `.wily`의 durable source of truth로 만들지 않는다.
- production deploy, GitHub remote mutation, destructive cleanup은 명시적 승인 없이는 하지 않는다.
- 기존 완료 Stage 기록을 재작성하지 않는다.

## 예상 산출물

- 개선된 plugin 문서나 helper.
- 좁고 deterministic한 regression tests.
- cache/update/release 절차에 대한 검증 evidence.
- 필요한 경우 후속 Stage 또는 Phase 분해 제안.
