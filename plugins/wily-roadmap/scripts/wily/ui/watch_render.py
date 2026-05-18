"""Pure renderer for `wily status` and `wily watch`."""

from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from shutil import get_terminal_size
import sys

from ..models import Actor, Task, TaskStatus
from ..observation import CommitInfo, guess_task_id, match_actor
from ..progress import CpSummary
from .watch_layout import WatchLayoutConfig
from .watch_activity import build_activity_lines

STATUS_META = {
    TaskStatus.DONE: ("●", "done", "green dim"),
    TaskStatus.IN_PROGRESS: ("◐", "in_progress", "bold yellow"),
    TaskStatus.READY: ("▶", "ready", "bold cyan"),
    TaskStatus.BLOCKED: ("✗", "blocked", "bold red"),
}
STATUS_META_ASCII = {
    TaskStatus.DONE: ("*", "done", ""),
    TaskStatus.IN_PROGRESS: ("~", "in_progress", ""),
    TaskStatus.READY: (">", "ready", ""),
    TaskStatus.BLOCKED: ("x", "blocked", ""),
}
STATUS_PRIORITY = {
    TaskStatus.IN_PROGRESS: 0,
    TaskStatus.BLOCKED: 1,
    TaskStatus.READY: 2,
    TaskStatus.DONE: 3,
}


@dataclass
class WatchRow:
    task_id: str
    glyph: str
    status_label: str
    style: str
    actor_display: str
    title: str
    cp_gauge: str = ""
    cp_timeline: str = ""
    blocker: str | None = None
    dependency_text: str | None = None
    meta_text: str | None = None
    guessed_text: str | None = None


def _truncate(text: str, width: int) -> str:
    if len(text) <= width:
        return text
    return text[: width - 1] + "…"


def _meta_for_task(task: Task) -> str | None:
    if task.status == TaskStatus.DONE and task.done_at:
        return f"[done: {task.done_at}]"
    if task.status == TaskStatus.IN_PROGRESS and task.claim_at:
        return f"[claimed: {task.claim_at}]"
    if task.depends_on:
        pending = [d for d in task.depends_on]
        if pending:
            return f"[depends: {','.join(pending)}]"
    return None


def _dependency_text_for_task(task: Task, task_map: dict[str, Task]) -> str | None:
    if not task.depends_on:
        return None
    pending = []
    for dep_id in task.depends_on:
        dep = task_map.get(dep_id)
        if dep and dep.status != TaskStatus.DONE:
            pending.append(f"{dep_id} ({dep.status.value})")
    if pending:
        return f"waiting for: {', '.join(pending)}"
    return None


def build_grouped_rows(
    tasks: list[Task],
    *,
    actors: list[Actor],
    observed_commits: list[CommitInfo],
    cp_summaries: dict[str, CpSummary],
    ascii_mode: bool = False,
    show_timeline: bool = False,
) -> dict[TaskStatus, list[WatchRow]]:
    meta = STATUS_META_ASCII if ascii_mode else STATUS_META
    task_map = {t.id: t for t in tasks}
    grouped: dict[TaskStatus, list[WatchRow]] = {
        TaskStatus.IN_PROGRESS: [],
        TaskStatus.BLOCKED: [],
        TaskStatus.READY: [],
        TaskStatus.DONE: [],
    }
    for task in tasks:
        cp = cp_summaries.get(task.id)
        gauge = ""
        timeline = ""
        if cp and cp.total:
            full, empty = ("#", "-") if ascii_mode else ("█", "░")
            left, right = ("[", "]") if ascii_mode else ("▕", "▏")
            blocks = full * cp.done + empty * max(cp.total - cp.done, 0)
            current = f" current:{cp.current_cp}" if cp.current_cp else ""
            gauge = f"{left}{blocks}{right} {cp.done}/{cp.total} cp{current}"
            if show_timeline and cp.cp_names:
                if ascii_mode:
                    timeline_parts = []
                    for name in cp.cp_names:
                        if timeline_parts:
                            timeline_parts.append(">")
                        done_set = {e.cp for e in []}
                        is_done = name in done_set
                        is_current = cp.current_cp == name
                        if is_done:
                            timeline_parts.append(f"[{name}]")
                        elif is_current:
                            timeline_parts.append(f"{{{name}}}")
                        else:
                            timeline_parts.append(name)
                    timeline = " ".join(timeline_parts)
                else:
                    timeline_parts = []
                    for name in cp.cp_names:
                        if timeline_parts:
                            timeline_parts.append(" › ")
                        is_current = cp.current_cp == name
                        if is_current:
                            timeline_parts.append(name)
                        else:
                            timeline_parts.append(name)
                    timeline = "".join(timeline_parts)
                    if cp.current_cp and cp.current_cp in cp.cp_names:
                        idx = cp.cp_names.index(cp.current_cp)
                        timeline += f"  ↑ {cp.current_cp}"
        glyph, status_label, style = meta[task.status]
        row = WatchRow(
            task_id=task.id,
            glyph=glyph,
            status_label=status_label,
            style=style,
            actor_display=task.actor or task.assignee or "—",
            title=task.title,
            cp_gauge=gauge,
            cp_timeline=timeline,
            blocker=task.blocker,
            dependency_text=_dependency_text_for_task(task, task_map),
            meta_text=_meta_for_task(task),
        )
        grouped[task.status].append(row)
    for commit in observed_commits:
        if commit.trailers.get("Wily-Task"):
            continue
        actor = match_actor(actors, email=commit.author_email, name=commit.author_name)
        guessed = guess_task_id(tasks, commit.files)
        row = WatchRow(
            task_id="-",
            glyph=">" if ascii_mode else "⏵",
            status_label="observed",
            style="dim",
            actor_display=actor.id if actor else "unknown",
            title=commit.subject,
            guessed_text=f"guessed task: {guessed} (no trailer)" if guessed else "no scope match",
        )
        grouped.setdefault(TaskStatus.READY, []).append(row)
    return grouped


def rich_available() -> bool:
    try:
        import rich.console  # noqa: F401
    except ImportError:
        _add_watch_venv_site_packages()
        try:
            import rich.console  # noqa: F401
        except ImportError:
            return False
    return True


def _add_watch_venv_site_packages() -> None:
    candidates = [Path.cwd() / ".venv-watch"]
    candidates.extend(parent / ".venv-watch" for parent in Path(__file__).resolve().parents)
    for venv in candidates:
        lib_dir = venv / "lib"
        if not lib_dir.exists():
            continue
        for site_packages in lib_dir.glob("python*/site-packages"):
            site_path = str(site_packages)
            if site_path not in sys.path:
                sys.path.insert(0, site_path)


def render_watch(
    *,
    project_title: str,
    tasks: list[Task],
    actors: list[Actor],
    observed_commits: list[CommitInfo],
    cp_summaries: dict[str, CpSummary],
    mode: str,
    ui: str = "auto",
    compact: bool = False,
    show_timeline: bool = False,
    show_log: bool = True,
) -> str:
    if ui not in {"auto", "rich", "ascii"}:
        raise ValueError(f"unknown watch ui: {ui}")
    ascii_mode = ui == "ascii"
    rich_requested = ui in {"auto", "rich"} and not ascii_mode
    rich_enabled = rich_requested and rich_available()
    term_width = max(72, min(get_terminal_size((96, 24)).columns, 160))
    layout = WatchLayoutConfig(
        width=term_width,
        ascii_mode=ascii_mode,
        compact=compact,
        show_observed=show_log,
        show_checkpoint_timeline=show_timeline,
    )
    lines = _styled_lines(
        project_title=project_title,
        tasks=tasks,
        actors=actors,
        observed_commits=observed_commits,
        cp_summaries=cp_summaries,
        mode=mode,
        ascii_mode=ascii_mode,
        layout=layout,
        show_timeline=show_timeline,
        show_log=show_log,
    )
    body = _render_rich(lines) if rich_enabled else "\n".join(text for text, _style in lines)
    if ui == "rich" and not rich_enabled:
        return "\n".join(
            [
                "Rich UI is not installed.",
                "Run: python3 -m pip install -r plugins/wily-roadmap/requirements-watch.txt",
                "Fallback: using plain watch UI.",
                body,
            ]
        )
    return body


def _header_lines(
    project_title: str,
    mode: str,
    *,
    ascii_mode: bool,
    width: int,
) -> list[tuple[str, str]]:
    rule = "-" if ascii_mode else "─"
    return [
        (f"Wily Roadmap v3  {project_title or '(untitled)'}", "bold"),
        (rule * width, "dim"),
    ]


def _summary_lines(
    tasks: list[Task],
    mode: str,
    *,
    ascii_mode: bool,
    width: int,
) -> list[tuple[str, str]]:
    rule = "-" if ascii_mode else "─"
    left, right = ("[", "]") if ascii_mode else ("▕", "▏")
    full, empty = ("#", "-") if ascii_mode else ("█", "░")
    done = sum(1 for task in tasks if task.status == TaskStatus.DONE)
    total = len(tasks)
    blocked = sum(1 for task in tasks if task.status == TaskStatus.BLOCKED)
    active = sum(1 for task in tasks if task.status == TaskStatus.IN_PROGRESS)
    bar_width = max(10, min(width // 3, 28))
    filled = int(round((done / total) * bar_width)) if total else 0
    bar = full * filled + empty * max(bar_width - filled, 0)
    pct = int(round((done / total) * 100)) if total else 0
    kpi = f"{blocked} blocked  {active} active" if (blocked or active) else ""
    progress = f"Progress {left}{bar}{right}  {done}/{total} · {pct}%"
    if kpi:
        progress += f"   {kpi}"
    return [
        (progress, "green" if done == total and total else "cyan"),
        (f"Mode {mode}", "dim"),
        (rule * width, "dim"),
    ]


def _task_group_lines(
    grouped: dict[TaskStatus, list[WatchRow]],
    *,
    ascii_mode: bool,
    width: int,
    compact: bool,
    show_timeline: bool,
) -> list[tuple[str, str]]:
    lines: list[tuple[str, str]] = []
    rule = "-" if ascii_mode else "─"
    group_labels = {
        TaskStatus.IN_PROGRESS: "IN PROGRESS",
        TaskStatus.BLOCKED: "BLOCKED",
        TaskStatus.READY: "READY",
        TaskStatus.DONE: "DONE",
    }
    max_title_width = max(20, width - 40)
    for status in [TaskStatus.IN_PROGRESS, TaskStatus.BLOCKED, TaskStatus.READY, TaskStatus.DONE]:
        rows = grouped.get(status, [])
        if not rows:
            continue
        label = group_labels[status]
        if not compact:
            header_text = f"{rule}{rule} {label} {rule * (width - len(label) - 4)}"
            lines.append((header_text[:width], "dim"))
        for index, row in enumerate(rows):
            branch = "\\-" if ascii_mode and index == len(rows) - 1 else "+-" if ascii_mode else "└─" if index == len(rows) - 1 else "├─"
            title = _truncate(row.title, max_title_width)
            meta = row.meta_text or ""
            line = f"{branch} {row.glyph} {row.task_id:<5} {row.status_label:<12} {row.actor_display:<10} {title}"
            if meta and not compact:
                remaining = width - len(line) - 1
                if remaining > 10:
                    line += " " + meta[:remaining]
            lines.append((line, row.style))
            if row.cp_gauge:
                rail = " " if index == len(rows) - 1 else "|" if ascii_mode else "│"
                cp_line = f"{rail}    cp {row.cp_gauge}"
                if row.cp_timeline and show_timeline:
                    remaining = width - len(cp_line) - 2
                    if remaining > 10:
                        cp_line += "  " + row.cp_timeline[:remaining]
                lines.append((cp_line, "green"))
            if row.blocker:
                rail = " " if index == len(rows) - 1 else "|" if ascii_mode else "│"
                blocker_prefix = "! " if ascii_mode else ""
                lines.append((f"{rail}    {blocker_prefix}blocker: {row.blocker}", "red"))
            if row.dependency_text:
                rail = " " if index == len(rows) - 1 else "|" if ascii_mode else "│"
                lines.append((f"{rail}    {row.dependency_text}", "yellow"))
            if row.guessed_text:
                rail = " " if index == len(rows) - 1 else "|" if ascii_mode else "│"
                child = "\\-" if ascii_mode else "└─"
                lines.append((f"{rail}    {child} {row.guessed_text}", "dim"))
    return lines


def _observed_lines(
    observed_commits: list[CommitInfo],
    *,
    ascii_mode: bool,
    width: int,
    compact: bool,
    show_log: bool,
) -> list[tuple[str, str]]:
    lines: list[tuple[str, str]] = []
    if not show_log:
        return lines
    if not observed_commits:
        return lines
    rule = "-" if ascii_mode else "─"
    if not compact:
        lines.append((rule * width, "dim"))
        lines.append((f"OBSERVED  {len(observed_commits)} commits since fork", "dim"))
    else:
        lines.append((f"{len(observed_commits)} observed commits", "dim"))
        return lines
    for commit in observed_commits[:10]:
        sha = commit.sha[:7]
        line = f"{'>' if ascii_mode else '⏵'} {sha}  {commit.author_email:<20}  \"{commit.subject[:40]}\""
        lines.append((line, "dim"))
    return lines


def _styled_lines(
    *,
    project_title: str,
    tasks: list[Task],
    actors: list[Actor],
    observed_commits: list[CommitInfo],
    cp_summaries: dict[str, CpSummary],
    mode: str,
    ascii_mode: bool,
    layout: WatchLayoutConfig,
    show_timeline: bool,
    show_log: bool,
) -> list[tuple[str, str]]:
    width = layout.width
    lines: list[tuple[str, str]] = []
    lines.extend(_header_lines(project_title, mode, ascii_mode=ascii_mode, width=width))
    lines.extend(_summary_lines(tasks, mode, ascii_mode=ascii_mode, width=width))
    grouped = build_grouped_rows(
        tasks,
        actors=actors,
        observed_commits=observed_commits,
        cp_summaries=cp_summaries,
        ascii_mode=ascii_mode,
        show_timeline=show_timeline,
    )
    task_lines = _task_group_lines(
        grouped,
        ascii_mode=ascii_mode,
        width=layout.task_pane_width if layout.show_activity_panel else width,
        compact=layout.compact,
        show_timeline=show_timeline,
    )
    if layout.show_activity_panel:
        activity_lines = build_activity_lines(
            actors, tasks, cp_summaries, ascii_mode=ascii_mode, width=layout.activity_pane_width
        )
        lines.extend(_merge_panels(task_lines, activity_lines, width))
    else:
        lines.extend(task_lines)
    lines.extend(_observed_lines(observed_commits, ascii_mode=ascii_mode, width=width, compact=layout.compact, show_log=show_log))
    return lines


def _merge_panels(
    left: list[tuple[str, str]],
    right: list[tuple[str, str]],
    width: int,
) -> list[tuple[str, str]]:
    merged: list[tuple[str, str]] = []
    max_left = 0
    for text, _ in left:
        max_left = max(max_left, len(text))
    left_width = min(max_left + 2, width // 2)
    right_start = left_width + 1
    for i in range(max(len(left), len(right))):
        left_text = left[i][0] if i < len(left) else ""
        right_text = right[i][0] if i < len(right) else ""
        left_style = left[i][1] if i < len(left) else ""
        right_style = right[i][1] if i < len(right) else ""
        pad = left_width - len(left_text)
        combined = left_text + " " * max(1, pad) + right_text
        if right_text and left_text:
            merged.append((combined, f"{left_style};{right_style}" if left_style and right_style else (left_style or right_style)))
        elif left_text:
            merged.append((left_text, left_style))
        else:
            merged.append((" " * right_start + right_text, right_style))
    return merged


def _render_rich(lines: list[tuple[str, str]]) -> str:
    from rich.console import Console

    sink = StringIO()
    console = Console(
        file=sink,
        record=True,
        force_terminal=True,
        color_system="truecolor",
        width=get_terminal_size((96, 24)).columns,
    )
    for text, style in lines:
        console.print(text, style=style or None)
    return console.export_text(styles=True).rstrip("\n")
