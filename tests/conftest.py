"""Shared helpers for planning-with-files lab tests."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_SCRIPTS = REPO_ROOT / ".claude" / "skills" / "planning-with-files" / "scripts"


@pytest.fixture(scope="session", autouse=True)
def _ensure_skill_installed() -> None:
    skill_md = REPO_ROOT / ".claude" / "skills" / "planning-with-files" / "SKILL.md"
    if not skill_md.is_file():
        subprocess.run(
            ["bash", str(REPO_ROOT / "scripts" / "install-skill.sh")],
            cwd=REPO_ROOT,
            check=True,
            env={**os.environ, "DISABLE_TELEMETRY": "1", "DO_NOT_TRACK": "1"},
        )
    assert skill_md.is_file(), f"missing {skill_md}"
    assert not (REPO_ROOT / ".agents" / "skills").exists()
    assert not (REPO_ROOT / ".cursor" / "skills").exists()


@pytest.fixture
def workdir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Isolated cwd with HOME=tmp_path so scripts never touch the real home."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    return tmp_path


def run_script(
    name: str,
    *args: str,
    cwd: Path,
    env: dict[str, str] | None = None,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    script = SKILL_SCRIPTS / name
    assert script.is_file(), f"missing skill script {script}"
    merged = {**os.environ, "HOME": str(cwd), "DISABLE_TELEMETRY": "1", "DO_NOT_TRACK": "1"}
    if env:
        merged.update(env)
    return subprocess.run(
        ["bash", str(script), *args],
        cwd=cwd,
        env=merged,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
