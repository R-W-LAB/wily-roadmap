# Verification

Stage s26 완료 전 fresh evidence:

- `python3 -m unittest plugins/wily-roadmap/tests/test_wily_command_skills.py`
- `python3 -m unittest plugins/wily-roadmap/tests/test_wily_cli.py`
- `python3 -m unittest discover plugins/wily-roadmap/tests`
- `git diff --check`
- 설치 cache와 `plugins/wily-roadmap/` 비교 결과.
- 변경된 skill/command docs가 Board reflection, local-first, approval-first 계약을 유지하는지 확인.

원격 push, release, production 확인은 사용자가 명시적으로 승인한 경우에만 수행한다.
