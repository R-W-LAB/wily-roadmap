# Wily Phase Context

Phase: s28/28-1 - Remove legacy Jinja templates

## Phase

# 28-1: Remove legacy Jinja templates

레거시 Board UI 템플릿 파일을 삭제하고, 더 이상 어떤 라우트도 이 템플릿을 렌더하지 않음을 보장한다.

## 삭제 대상

- `app/web/templates/board.html`
- `app/web/templates/repo_detail.html`
- `app/web/templates/_phase_row.html`
- `app/web/templates/base.html`
- `app/web/templates/_toast.html`
- (옵션) `app/web/static/app.css`가 사용되지 않으면 함께 삭제

## 검증

- `grep -r "TemplateResponse\|templates/" app/` 결과 0건 (templates 디렉터리 자체 삭제 가능)
- `pytest` 통과

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
