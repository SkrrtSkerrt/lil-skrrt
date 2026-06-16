from pathlib import Path

from hermes_cli.default_soul import DEFAULT_SOUL_MD


def test_install_ps1_contains_canonical_soul_template():
    install_ps1 = Path(__file__).resolve().parents[1] / "scripts" / "install.ps1"
    content = install_ps1.read_text(encoding="utf-8")
    assert DEFAULT_SOUL_MD in content
