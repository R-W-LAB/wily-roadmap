"""`wily land <id>` - commit local task changes with a Wily trailer."""

from __future__ import annotations

import fnmatch
import subprocess
import sys
from pathlib import Path

from ..config import load_tasks
from ..models import TaskStatus
from ..paths import WilyPaths, WilyRootNotFound, find_wily_root
from . import _common

DESCRIPTION = "commit local task changes with a Wily trailer"
USAGE = "usage: wily land <task-id> [--push|--no-push] [--force]"
HELP = "\n".join(
    [
        "Options:",
        "  --push     push after committing",
        "  --no-push  skip push after committing",
        "  --force    include out-of-scope files or land before done",
    ]
)


def main(args: list[str]) -> int:
    force = "--force" in args
    push = "--push" in args
    no_push = "--no-push" in args
    if push and no_push:
        _common.emit_error("choose only one of --push or --no-push")
        return _common.EXIT_USAGE
    positional = [arg for arg in args if not arg.startswith("--")]
    if len(positional) != 1:
        _common.emit_error("usage: wily land <task-id> [--push|--no-push] [--force]")
        return _common.EXIT_USAGE
    task_id = positional[0]
    try:
        root = find_wily_root(Path.cwd())
    except WilyRootNotFound as exc:
        _common.emit_error(str(exc))
        return _common.EXIT_FAILURE
    paths = WilyPaths(root)
    _, tasks = load_tasks(paths)
    task = next((item for item in tasks if item.id == task_id), None)
    if task is None:
        _common.emit_error(f"task not found: {task_id}")
        return _common.EXIT_FAILURE
    if task.status != TaskStatus.DONE and not force:
        _common.emit_error(f"{task_id} is {task.status.value}; run wily done first")
        return _common.EXIT_TRANSITION
    changed = _changed(root)
    if not changed:
        _common.emit_error("nothing to commit")
        return _common.EXIT_FAILURE
    in_scope, out_scope = _split(changed, task.scope)
    files = changed if force or not out_scope else in_scope
    if out_scope and not force:
        _common.emit_text(f"warning: {len(out_scope)} file(s) outside scope; use --force to include")
    if not files:
        _common.emit_error("no in-scope files to commit")
        return _common.EXIT_FAILURE
    subprocess.run(["git", "add", *files], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", _message(paths, task.id, task.title, pre_done=task.status != TaskStatus.DONE)], cwd=root, check=True)
    _common.emit_text(f"committed: {task.id}: {task.title}")
    if no_push or not push:
        _common.emit_text("(push skipped: --no-push)")
        return _common.EXIT_OK
    return _common.EXIT_OK if _do_push(root) else _common.EXIT_FAILURE


def _changed(root: Path) -> list[str]:
    out = subprocess.run(["git", "status", "--porcelain=v2"], cwd=root, capture_output=True, text=True, check=True).stdout
    files: list[str] = []
    for line in out.splitlines():
        if not line.strip() or line.startswith("? "):
            if line.startswith("? "):
                files.append(line[2:])
            continue
        parts = line.split("\t")
        head = parts[0].split()
        if line.startswith("1 ") and len(head) >= 9:
            files.append(" ".join(head[8:]))
        elif line.startswith("2 ") and len(parts) >= 2:
            files.append(parts[0].split()[-1])
    return files


def _split(files: list[str], scope: list[str]) -> tuple[list[str], list[str]]:
    if not scope:
        return files, []
    inside = [file for file in files if any(fnmatch.fnmatch(file, pattern) for pattern in scope)]
    outside = [file for file in files if file not in inside]
    return inside, outside


def _message(paths: WilyPaths, task_id: str, title: str, *, pre_done: bool = False) -> str:
    body = ""
    result = paths.result_md(task_id)
    if result.exists():
        bullets = [line for line in result.read_text(encoding="utf-8").splitlines() if line.startswith("- ")]
        body = "\n".join(bullets[:6])
    pre_done_line = "Wily-Pre-Done: true\n" if pre_done else ""
    return f"{task_id}: {title}\n\n{body}\n\nWily-Task: {task_id}\n{pre_done_line}"


def _do_push(root: Path) -> bool:
    return subprocess.run(["git", "push"], cwd=root, check=False).returncode == 0
