"""init-session.sh (zero args) creates legacy root planning files."""

from __future__ import annotations

from pathlib import Path

from conftest import run_script


def test_init_legacy(workdir: Path) -> None:
    result = run_script("init-session.sh", cwd=workdir)
    assert result.returncode == 0, result.stderr
    for name in ("task_plan.md", "findings.md", "progress.md"):
        assert (workdir / name).is_file(), name

    plan = (workdir / "task_plan.md").read_text(encoding="utf-8")
    assert "in_progress" in plan
    assert "pending" in plan
    # Phase 1 in_progress; Phases 2–5 pending (template at pin).
    assert plan.count("pending") >= 4
