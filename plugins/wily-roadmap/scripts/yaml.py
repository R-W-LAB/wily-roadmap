"""Tiny YAML compatibility layer for Wily v3 state files.

Wily v3 only writes JSON-compatible mappings/lists/scalars. JSON is valid YAML
1.2, so this local module provides the subset of PyYAML used by the plugin
without adding a runtime dependency.
"""

from __future__ import annotations

import json
from typing import Any


def safe_load(text: str) -> Any:
    if not text.strip():
        return None
    return json.loads(text)


def safe_dump(
    value: Any,
    *,
    sort_keys: bool = False,
    allow_unicode: bool = True,
    **_: Any,
) -> str:
    return json.dumps(value, ensure_ascii=not allow_unicode, indent=2, sort_keys=sort_keys) + "\n"
