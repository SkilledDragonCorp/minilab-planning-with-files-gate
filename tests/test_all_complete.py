"""All five phases complete → check-complete reports 5/5."""

from __future__ import annotations

from pathlib import Path

from conftest import run_script


def test_all_complete(workdir: Path) -> None:
    init = run_script("init-session.sh", cwd=workdir)
    assert init.returncode == 0, init.stderr

    for n in range(1, 6):
        result = run_script("phase-status.sh", str(n), "complete", cwd=workdir)
        assert result.returncode == 0, result.stderr

    check = run_script("check-complete.sh", cwd=workdir)
    assert check.returncode == 0, check.stderr
    assert "ALL PHASES COMPLETE (5/5)" in check.stdout
