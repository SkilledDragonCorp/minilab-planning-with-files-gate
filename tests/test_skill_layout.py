"""Skill frontmatter and layout bans."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), path
    end = text.find("\n---\n", 4)
    assert end != -1, path
    data = yaml.safe_load(text[4:end])
    assert isinstance(data, dict), path
    return data


def test_skill_layout() -> None:
    assert not (REPO_ROOT / ".cursor" / "skills").exists()
    assert not (REPO_ROOT / ".agents" / "skills").exists()

    for rel in (
        ".claude/skills/planning-with-files/SKILL.md",
        ".claude/skills/plan-survives-clear/SKILL.md",
    ):
        path = REPO_ROOT / rel
        assert path.is_file(), rel
        meta = _frontmatter(path)
        assert "name" in meta and meta["name"], rel
        assert "description" in meta and meta["description"], rel
