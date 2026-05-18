# Wily Phase Context

Phase: s28/28-4 - Read-only invariant regression tests

## Phase

# 28-4: Read-only invariant regression tests

이후 누군가 실수로 mutating 라우트나 mutating UI를 다시 추가하지 못하도록 회귀 테스트로 invariant를 박는다.

## 백엔드 테스트

```python
def test_no_mutating_roadmap_routes(app):
    allowed_mutating = {"/api/live/events"}  # ingest는 mutation 아님
    for route in app.routes:
        if getattr(route, "methods", None) and route.methods & {"POST", "PUT", "PATCH", "DELETE"}:
            assert route.path in allowed_mutating, f"mutating route detected: {route.path}"
```

## 프론트엔드 스모크

- `/`와 `/repos/{seed_owner}/{seed_name}` 로드
- DOM에 `<select name="new_status">`, `Open PR` 버튼, `<form action="/actions/">` 미존재
- Playwright/Vitest 둘 다 가능 — 기존 테스트 인프라에 맞춰 선택

## 검증

- 위 테스트 두 개가 main에서 통과
- 실수 시뮬레이션: toggle_status.py 임시 복원하면 백엔드 테스트가 실패해야 함

## Planner Adapter

Missing.

## Prompt

Missing.

## Verification

Missing.

## Handoff

Missing.

## Existing Implementation Plan

No implementation plan exists yet.
Use the recommended planner to create one if this phase needs a detailed plan.
