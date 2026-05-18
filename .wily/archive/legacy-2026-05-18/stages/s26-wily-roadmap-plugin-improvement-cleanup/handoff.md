# Handoff

Stage s26은 S25 이후의 plugin 유지보수 Stage다. S25가 Board UI polish를 다루는 반면, S26은 Wily Roadmap plugin 자체의 반복 운영 비용과 문서/테스트 일관성을 줄이는 데 집중한다.

처음 할 일:

1. `plugins/wily-roadmap/`과 `/Users/wilycastle/.codex/plugins/cache/wily-castle/wily-roadmap/0.1.0/`의 차이를 확인한다.
2. 상태 변경형 skill/command 문서와 tests가 새 Board reflection contract를 계속 만족하는지 확인한다.
3. 사용자의 홈 config나 production config에 의존하는 테스트가 있는지 찾는다.
4. 개선이 여러 갈래로 커지면 `$wily-decompose-stage s26`으로 Phase를 나눈다.

주의:

- `.wily` durable state는 Git-backed source of truth다.
- plugin cache는 현재 사용성을 위한 projection이며, source tree와 어긋나면 명확히 기록한다.
- 기존 dirty worktree 변경은 되돌리지 않는다.
