"""Opt-in --gated init and check-complete.sh --gate decision JSON."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from conftest import run_script


def test_gate_opt_in(workdir: Path) -> None:
    today = date.today().isoformat()
    slug = f"{today}-gated-run"
    plan_dir = workdir / ".planning" / slug

    init = run_script("init-session.sh", "--gated", "Gated Run", cwd=workdir)
    assert init.returncode == 0, init.stderr

    for name in (
        "task_plan.md",
        "findings.md",
        "progress.md",
        ".mode",
        ".nonce",
        ".attestation",
        ".stop_blocks",
    ):
        assert (plan_dir / name).is_file(), name
    assert (workdir / ".planning" / ".active_plan").is_file()
    assert "autonomous gate" in (plan_dir / ".mode").read_text(encoding="utf-8")

    blocked = run_script(
        "check-complete.sh",
        "--gate",
        cwd=workdir,
        input_text="{}",
    )
    assert blocked.returncode == 0, blocked.stderr
    lines = [ln for ln in blocked.stdout.strip().splitlines() if ln.strip()]
    assert len(lines) == 1, blocked.stdout
    payload = json.loads(lines[0])
    assert payload.get("decision") == "block"
    assert "Phase 1" in json.dumps(payload) or "in_progress" in json.dumps(payload)

    stop_active = run_script(
        "check-complete.sh",
        "--gate",
        cwd=workdir,
        input_text='{"stop_hook_active": true}',
    )
    assert stop_active.returncode == 0, stop_active.stderr
    assert '"decision"' not in stop_active.stdout

    for n in range(1, 6):
        phase = run_script(
            "phase-status.sh",
            str(n),
            "complete",
            cwd=workdir,
            env={"PLAN_ID": slug},
        )
        assert phase.returncode == 0, phase.stderr

    done = run_script(
        "check-complete.sh",
        "--gate",
        cwd=workdir,
        input_text="{}",
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == ""
