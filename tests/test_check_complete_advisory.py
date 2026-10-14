"""check-complete.sh (no flag) is advisory and reports 0/5 after init."""

from __future__ import annotations

from pathlib import Path

from conftest import run_script


def test_check_complete_advisory(workdir: Path) -> None:
    init = run_script("init-session.sh", cwd=workdir)
    assert init.returncode == 0, init.stderr

    result = run_script("check-complete.sh", cwd=workdir)
    assert result.returncode == 0, result.stderr
    assert (
        "[planning-with-files] Task in progress (0/5 phases complete). "
        "Update progress.md before stopping."
    ) in result.stdout
