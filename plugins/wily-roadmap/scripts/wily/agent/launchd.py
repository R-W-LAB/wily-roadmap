"""macOS launchd integration for wily-agent."""

from __future__ import annotations

import plistlib
from pathlib import Path


LABEL = "com.wily.roadmap.agent"


def foreground_command(
    *,
    python_executable: str,
    plugin_root: Path,
    registry_path: Path,
    config_path: Path,
    once: bool = False,
) -> list[str]:
    command = [
        python_executable,
        str(plugin_root / "scripts" / "wily.py"),
        "agent",
        "dev",
        "--registry",
        str(registry_path),
        "--config",
        str(config_path),
        "--offline-ok",
    ]
    if once:
        command.append("--once")
    return command


def launchd_plist(
    *,
    label: str,
    python_executable: str,
    plugin_root: Path,
    registry_path: Path,
    config_path: Path,
    log_dir: Path,
) -> str:
    payload = {
        "Label": label,
        "ProgramArguments": foreground_command(
            python_executable=python_executable,
            plugin_root=plugin_root,
            registry_path=registry_path,
            config_path=config_path,
        ),
        "RunAtLoad": True,
        "KeepAlive": True,
        "StandardOutPath": str(log_dir / "stdout.log"),
        "StandardErrorPath": str(log_dir / "stderr.log"),
    }
    return plistlib.dumps(payload, sort_keys=True).decode("utf-8")
