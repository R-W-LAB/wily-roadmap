# Handoff

Stage s27은 남은 s25/s26 work를 취소하고 시작하는 대규모 리팩토링 Stage다.

처음 할 일:

1. `plugins/wily-roadmap/scripts/wily.py`의 command와 helper를 분류한다.
2. state-changing Wily commands의 Board reflection contract를 재검토한다.
3. replan/task-candidate/direct-stage draft의 협업 안전성을 설계한다.
4. 리팩토링이 한 번에 너무 크면 `$wily-decompose-stage s27`로 Phase를 만든다.

주의:

- 완료된 s01-s24는 변경하지 않는다.
- s25와 s26은 superseded 상태다.
- durable roadmap 변경은 commit/push 전까지 local state다.
