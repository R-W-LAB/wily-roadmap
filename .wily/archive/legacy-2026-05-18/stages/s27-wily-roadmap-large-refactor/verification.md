# Verification

Stage s27 완료 전 fresh evidence:

- `python3 -m unittest plugins/wily-roadmap/tests/test_wily_command_skills.py`
- `python3 -m unittest plugins/wily-roadmap/tests/test_wily_cli.py`
- `python3 -m unittest discover plugins/wily-roadmap/tests`
- `git diff --check`
- Board live config and deterministic reflection check when state-changing behavior is touched.
- installed plugin cache comparison when plugin source changes should be reflected immediately.

리팩토링이 Board UI/API 또는 production behavior를 바꾸는 경우 별도 browser/API verification을 추가한다.
