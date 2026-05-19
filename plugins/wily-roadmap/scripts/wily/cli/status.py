"""`wily status` - one-shot project snapshot."""

from __future__ import annotations

from pathlib import Path

from ..config import load_actors, load_tasks, repo_mode
from ..models import TaskStatus
from ..observation import fetch_observation_remote, list_commits_since_fork, list_remote_commits, observation_base
from ..paths import WilyPaths, WilyRootNotFound, find_wily_root
from ..progress import cp_summary
from ..ui.watch_render import render_watch
from . import _common

DESCRIPTION = "print a one-shot project snapshot"
USAGE = "usage: wily status [--json] [--ui <auto|ascii>] [--compact] [--show-timeline] [--hide-log]"
HELP = "\n".join(
    [
        "Options:",
        "  --json          emit project state as JSON",
        "  --ui <mode>     choose renderer mode",
        "  --compact       reduce output density",
        "  --show-timeline include checkpoint timeline",
        "  --hide-log      hide observed git log entries",
    ]
)


def main(args: list[str]) -> int:
    as_json = "--json" in args
    ui = _ui_mode(args)
    if ui is None:
        return _common.EXIT_USAGE
    try:
        root = find_wily_root(Path.cwd())
    except WilyRootNotFound as exc:
        _common.emit_error(str(exc))
        return _common.EXIT_FAILURE
    paths = WilyPaths(root)
    project_title, tasks = load_tasks(paths)
    actors = load_actors(paths)
    mode = repo_mode(paths)
    summaries = {task.id: cp_summary(paths, task.id) for task in tasks}
    observed = []
    try:
        remote_ref = fetch_observation_remote(root)
        if remote_ref:
            observed.extend(list_remote_commits(root, remote_ref, limit=20))
        observed.extend(list_commits_since_fork(root, observation_base(root), limit=20))
        seen: set[str] = set()
        observed = [commit for commit in observed if not (commit.sha in seen or seen.add(commit.sha))]
    except Exception:
        observed = []
    if as_json:
        _common.emit_json(
            {
                "project_title": project_title,
                "mode": mode,
                "tasks": [task.to_dict() for task in tasks],
                "actors": [{"id": actor.id, **actor.to_dict()} for actor in actors],
                "cp": {task_id: summary.__dict__ for task_id, summary in summaries.items()},
            }
        )
    else:
        compact = "--compact" in args
        show_timeline = "--show-timeline" in args
        show_log = "--hide-log" not in args
        _common.emit_text(
            render_watch(
                project_title=project_title,
                tasks=tasks,
                actors=actors,
                observed_commits=observed,
                cp_summaries=summaries,
                mode=mode,
                ui=ui,
                compact=compact,
                show_timeline=show_timeline,
                show_log=show_log,
            )
        )
    if any(task.status == TaskStatus.BLOCKED for task in tasks):
        return 2
    if any(task.status in {TaskStatus.READY, TaskStatus.IN_PROGRESS} for task in tasks):
        return 1
    return 0


def _ui_mode(args: list[str]) -> str | None:
    if "--ui" not in args:
        return "auto"
    index = args.index("--ui")
    if index + 1 >= len(args):
        _common.emit_error("--ui requires one of: auto, rich, ascii")
        return None
    mode = args[index + 1]
    if mode not in {"auto", "rich", "ascii"}:
        _common.emit_error("--ui requires one of: auto, rich, ascii")
        return None
    return mode
