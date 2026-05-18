# Execution Prompt

Stage s27을 실행하라: Wily Roadmap 대규모 리팩토링.

먼저 현재 Wily Roadmap plugin의 CLI, skill 문서, command docs, Board reflection 계약, `.wily` state layout, installed cache sync, tests를 감사한다. 리팩토링 범위가 넓으면 구현 전에 `$wily-decompose-stage s27`로 Phase와 lane을 나눈다.

완료된 s01-s24 이력은 보존한다. s25와 s26은 superseded로 취소된 future work로 취급한다. local-first와 approval-first 정책을 유지하고, remote push/deploy/destructive cleanup은 명시적 승인 없이는 하지 않는다.
