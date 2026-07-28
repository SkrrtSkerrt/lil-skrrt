from pathlib import Path

import yaml

from tools.skills_sync import _discover_bundled_skills


REPO_ROOT = Path(__file__).resolve().parents[2]
BUNDLED_SKILLS = REPO_ROOT / "skills"


def _frontmatter(skill_name: str) -> dict:
    skill_path = BUNDLED_SKILLS / "software-development" / skill_name / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    frontmatter = text.split("---", 2)[1]
    return yaml.safe_load(frontmatter)


def test_caveman_is_bundled_as_default_skill():
    names = {name for name, _path in _discover_bundled_skills(BUNDLED_SKILLS)}
    meta = _frontmatter("caveman")

    assert "caveman" in names
    assert meta["name"] == "caveman"
    assert "Ultra-compressed communication mode" in meta["description"]


def test_ponytail_is_bundled_as_default_skill():
    names = {name for name, _path in _discover_bundled_skills(BUNDLED_SKILLS)}
    meta = _frontmatter("ponytail")

    assert "ponytail" in names
    assert meta["name"] == "ponytail"
    assert "laziest solution that actually works" in meta["description"]
