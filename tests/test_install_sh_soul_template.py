from pathlib import Path

from hermes_cli.default_soul import DEFAULT_SOUL_MD


def test_install_sh_contains_canonical_soul_template():
    install_sh = Path(__file__).resolve().parents[1] / "scripts" / "install.sh"
    content = install_sh.read_text(encoding="utf-8")
    assert DEFAULT_SOUL_MD in content
