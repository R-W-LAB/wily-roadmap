"""Interview question registry for Wily v3."""

from __future__ import annotations

from .interview import Draft

GREENFIELD_KEYS = ("purpose", "users", "success", "non_goals", "actors_setup")
BROWNFIELD_KEYS = ("analysis_confirm", "purpose_revise", "success", "non_goals", "actors_setup")

QUESTION_TEXT_KO = {
    "purpose": "이 프로젝트의 한 줄 목적은?",
    "users": "누가 쓰나? 사용자/이해관계자를 알려줘.",
    "success": "무엇이 되면 성공인가? 객관적 조건으로 적어줘.",
    "non_goals": "절대 안 하는 것 / 제약은?",
    "actors_setup": "협업 actor와 git author 매핑은? 예: wily Wily 박사, emails=me@example.com",
    "analysis_confirm": "자동 분석 결과가 맞나? 맞으면 ok, 아니면 revise: <설명>.",
    "purpose_revise": "큰 그림을 보강해줘. 없으면 없음.",
}


def keys_for_mode(mode: str) -> tuple[str, ...]:
    return BROWNFIELD_KEYS if mode == "brownfield" else GREENFIELD_KEYS


def next_question(draft: Draft) -> str | None:
    for key in keys_for_mode(draft.mode):
        if key not in draft.answers:
            return key
    return None


def ready_for_tasks(draft: Draft) -> bool:
    return next_question(draft) is None


def question_text(key: str) -> str:
    return QUESTION_TEXT_KO.get(key, f"{key}?")
