"""Simulate /clear: process A writes phase status; process B recovers from files only."""

from __future__ import annotations

from pathlib import Path

from conftest import run_script


def test_survives_clear(workdir: Path) -> None:
    init = run_script("init-session.sh", cwd=workdir)
    assert init.returncode == 0, init.stderr

    # Process A — marks phase 1 complete, then "exits" (no shared memory).
    proc_a = run_script("phase-status.sh", "1", "complete", cwd=workdir)
    assert proc_a.returncode == 0, proc_a.stderr
    assert "[phase-status] Phase 1 -> complete in ./task_plan.md" in proc_a.stdout

    # Process B — fresh subprocess, only the directory is shared.
    proc_b = run_script("check-complete.sh", cwd=workdir)
    assert proc_b.returncode == 0, proc_b.stderr
    assert "Task in progress (1/5 phases complete)" in proc_b.stdout
