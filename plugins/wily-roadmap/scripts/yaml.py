"""Tiny YAML compatibility layer for Wily v3 state files.

Wily v3 only writes JSON-compatible mappings/lists/scalars. JSON is valid YAML
1.2, so this local module provides the subset of PyYAML used by the plugin
without adding a runtime dependency.
"""

from __future__ import annotations

import json
import importlib
import sys
from typing import Any

_PY_YAML: Any | None = None


def safe_load(text: str) -> Any:
    if not text.strip():
        return None
    parser = _pyyaml()
    if parser is not None:
        return parser.safe_load(text)
    stripped = text.lstrip()
    if stripped.startswith("{") or stripped.startswith("["):
        return json.loads(text)
    return _parse_yaml_subset(text)


def safe_dump(
    value: Any,
    *,
    sort_keys: bool = False,
    allow_unicode: bool = True,
    **_: Any,
) -> str:
    dumper = _pyyaml()
    if dumper is not None:
        return dumper.safe_dump(value, sort_keys=sort_keys, allow_unicode=allow_unicode)
    return json.dumps(value, ensure_ascii=not allow_unicode, indent=2, sort_keys=sort_keys) + "\n"


def _pyyaml() -> Any | None:
    global _PY_YAML
    if _PY_YAML is not None:
        return _PY_YAML
    current = sys.modules.get(__name__)
    original_yaml = sys.modules.pop("yaml", None)
    original_path = list(sys.path)
    try:
        here = __file__
        sys.path = [entry for entry in sys.path if not here.startswith(entry.rstrip("/") + "/")]
        module = importlib.import_module("yaml")
        if getattr(module, "__file__", None) != __file__:
            _PY_YAML = module
            return module
    except Exception:
        return None
    finally:
        sys.path = original_path
        if current is not None:
            sys.modules["yaml"] = current
        elif original_yaml is not None:
            sys.modules["yaml"] = original_yaml
    return None


def _parse_yaml_subset(text: str) -> Any:
    lines = _logical_lines(text)
    if not lines:
        return None
    value, _ = _parse_block(lines, 0, lines[0][0])
    return value


def _logical_lines(text: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        out.append((indent, raw.strip()))
    return out


def _parse_block(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        return None, index
    if lines[index][1].startswith("- "):
        return _parse_list(lines, index, indent)
    return _parse_map(lines, index, indent)


def _parse_map(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    while index < len(lines):
        line_indent, content = lines[index]
        if line_indent < indent or content.startswith("- "):
            break
        if line_indent > indent:
            index += 1
            continue
        key, sep, raw_value = content.partition(":")
        if not sep:
            index += 1
            continue
        key = key.strip().strip("\"'")
        raw_value = raw_value.strip()
        index += 1
        if raw_value:
            result[key] = _parse_scalar(raw_value)
        elif index < len(lines) and lines[index][0] > line_indent:
            result[key], index = _parse_block(lines, index, lines[index][0])
        else:
            result[key] = None
    return result, index


def _parse_list(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[list[Any], int]:
    result: list[Any] = []
    while index < len(lines):
        line_indent, content = lines[index]
        if line_indent != indent or not content.startswith("- "):
            break
        item = content[2:].strip()
        index += 1
        if not item:
            if index < len(lines) and lines[index][0] > line_indent:
                value, index = _parse_block(lines, index, lines[index][0])
            else:
                value = None
        elif ":" in item and not item.startswith(("'", '"')):
            key, _, raw_value = item.partition(":")
            value = {key.strip().strip("\"'"): _parse_scalar(raw_value.strip()) if raw_value.strip() else None}
            if index < len(lines) and lines[index][0] > line_indent:
                nested, index = _parse_map(lines, index, lines[index][0])
                value.update(nested)
        else:
            value = _parse_scalar(item)
        result.append(value)
    return result, index


def _parse_scalar(value: str) -> Any:
    if value == "":
        return None
    if value in {"[]", "{}"}:
        return [] if value == "[]" else {}
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(part.strip()) for part in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    try:
        return int(value)
    except ValueError:
        return value
