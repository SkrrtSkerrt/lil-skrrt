from pathlib import Path

from hermes_cli.default_soul import DEFAULT_SOUL_MD


def test_docker_soul_matches_canonical_template():
    docker_soul = Path(__file__).resolve().parents[1] / "docker" / "SOUL.md"
    assert docker_soul.read_text(encoding="utf-8") == DEFAULT_SOUL_MD
