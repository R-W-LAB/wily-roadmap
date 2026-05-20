"""Small user-facing message catalog for Wily CLI output."""

from __future__ import annotations

import os

SUPPORTED_LOCALES = {"ko", "en"}
DEFAULT_LOCALE = "ko"

MESSAGES = {
    "ko": {
        "available": "사용 가능: {commands}",
        "commands": "명령:",
        "description.claim": "태스크를 진행 중으로 전환",
        "description.cp": "태스크 체크포인트 진행 상황 기록",
        "description.done": "태스크를 완료 처리하고 result.md 작성",
        "description.go": "custom-workflow goal text 출력",
        "description.init": "인터뷰 기반 부트스트랩과 기존 프로젝트 채택",
        "description.next": "다음 수행 가능한 태스크 출력",
        "description.replan": "태스크 목록 변경 초안 작성 및 반영",
        "description.block": "태스크 차단 사유 기록",
        "description.land": "Wily trailer가 포함된 태스크 변경 커밋",
        "description.watch": "프로젝트 상태 화면 폴링 렌더링",
        "description.status": "프로젝트 상태 스냅샷 출력",
        "description.workspace": "manifest 기반 multi-repo workspace 상태 출력",
        "description.agent": "번들 heartbeat daemon 설치 및 관리",
        "description.doctor": "로컬 Wily 상태 헬스체크",
        "options": "옵션:",
        "removed": "오류: {command!r} 명령은 wily v3에서 제거되었습니다 (removed in wily v3). {detail}",
        "title": "wily v3 - 프로젝트 + 평면 goal-sized 태스크 관리자",
        "unknown": "알 수 없는 명령: {command!r}",
        "usage": "사용법:",
    },
    "en": {
        "available": "available: {commands}",
        "commands": "Commands:",
        "options": "Options:",
        "removed": "Error: {command!r} is removed in wily v3. {detail}",
        "title": "wily v3 - Project + flat goal-sized Task manager",
        "unknown": "unknown command: {command!r}",
        "usage": "Usage:",
    },
}


def current_locale() -> str:
    value = os.environ.get("WILY_LOCALE", DEFAULT_LOCALE).strip().lower()
    return value if value in SUPPORTED_LOCALES else DEFAULT_LOCALE


def text(key: str, **values: object) -> str:
    locale = current_locale()
    template = MESSAGES.get(locale, {}).get(key) or MESSAGES["en"].get(key) or key
    return template.format(**values)


def command_description(command: str, fallback: str) -> str:
    return text(f"description.{command}") if current_locale() == "ko" else fallback
