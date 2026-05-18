# Execution Prompt

Stage s26을 실행하라: Wily Roadmap plugin 개선 및 정리.

먼저 현재 plugin source, 설치 cache, skill/command 문서, tests, update/release 경로를 점검한다. 반복되는 수동 절차나 불안정한 테스트 격리 문제를 찾아 가장 작은 변경 단위로 개선한다.

local-first와 approval-first 정책을 유지한다. 새 hooks, MCP servers, app integrations, production deploy, remote mutation은 사용자가 명시적으로 요청하지 않는 한 추가하거나 실행하지 않는다.
