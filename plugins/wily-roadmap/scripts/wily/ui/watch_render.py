"""Pure renderer for `wily status` and `wily watch`."""

from __future__ import annotations

from dataclasses import dataclass

from ..models import Actor, Task, TaskStatus
from ..observation import CommitInfo, guess_task_id, match_actor
from ..progress import CpSummary

GLYPHS = {
    TaskStatus.DONE: "✓ done",
    TaskStatus.IN_PROGRESS: "▶ in_progress",
    TaskStatus.READY: "ready",
    TaskStatus.BLOCKED: "blocked",
}


@dataclass
class WatchRow:
    task_id: str
    glyph: str
    actor_display: str
    title: str
    cp_gauge: str = ""
    blocker: str | None = None
    guessed_text: str | None = None


def build_rows(
    tasks: list[Task],
    *,
    actors: list[Actor],
    observed_commits: list[CommitInfo],
    cp_summaries: dict[str, CpSummary],
) -> list[WatchRow]:
    rows: list[WatchRow] = []
    for task in tasks:
        cp = cp_summaries.get(task.id)
        gauge = ""
        if cp and cp.total:
            blocks = "▓" * cp.done + "░" * max(cp.total - cp.done, 0)
            current = f" cp:{cp.current_cp}" if cp.current_cp else ""
            gauge = f"[{blocks} {cp.done}/{cp.total} cp]{current}"
        rows.append(
            WatchRow(
                task_id=task.id,
                glyph=GLYPHS[task.status],
                actor_display=task.actor or task.assignee or "-",
                title=task.title,
                cp_gauge=gauge,
                blocker=task.blocker,
            )
        )
    for commit in observed_commits:
        if commit.trailers.get("Wily-Task"):
            continue
        actor = match_actor(actors, email=commit.author_email, name=commit.author_name)
        guessed = guess_task_id(tasks, commit.files)
        rows.append(
            WatchRow(
                task_id="-",
                glyph="⏵ observed",
                actor_display=actor.id if actor else "unknown",
                title=commit.subject,
                guessed_text=f"guessed task: {guessed} (no trailer)" if guessed else "no scope match",
            )
        )
    return rows


def render_watch(
    *,
    project_title: str,
    tasks: list[Task],
    actors: list[Actor],
    observed_commits: list[CommitInfo],
    cp_summaries: dict[str, CpSummary],
    mode: str,
) -> str:
    lines = [f"Project: {project_title or '(untitled)'}", "─" * 69]
    for row in build_rows(
        tasks,
        actors=actors,
        observed_commits=observed_commits,
        cp_summaries=cp_summaries,
    ):
        line = f"{row.task_id:<5} {row.glyph:<14} {row.actor_display:<8} {row.title}"
        if row.cp_gauge:
            line += " " + row.cp_gauge
        lines.append(line)
        if row.blocker:
            lines.append(f"      blocker: {row.blocker}")
        if row.guessed_text:
            lines.append(f"      └ {row.guessed_text}")
    lines.append("")
    actor_summary = "  ·  ".join(
        f"{actor.id} {actor.git_author_emails[0]}" if actor.git_author_emails else actor.id
        for actor in actors
    )
    lines.append(f"actors: {actor_summary}")
    lines.append(f"mode: {mode}")
    return "\n".join(lines)
