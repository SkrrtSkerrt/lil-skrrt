from __future__ import annotations

import sys
import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_compatibility_entrypoints_route_to_cli_main() -> None:
    """Every user-facing alias must support normal CLI flags before provider setup."""
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text())
    scripts = data["project"]["scripts"]

    assert scripts["hermes"] == "hermes_cli.main:main"
    assert scripts["hermes-agent"] == "hermes_cli.main:main"
    assert scripts["lil-skrrt"] == "lil_skrrt_launcher:main"
    assert scripts["a"] == "lil_skrrt_launcher:main"


def test_zh_windows_native_doc_tracks_current_install_layout() -> None:
    doc = (
        REPO_ROOT
        / "website/i18n/zh-Hans/docusaurus-plugin-content-docs/current/user-guide/windows-native.md"
    ).read_text()

    assert "SkrrtSkerrt/hermes-agent" not in doc
    assert "%LOCALAPPDATA%\\lil-skrrt" not in doc
    assert "%USERPROFILE%\\.hermes" not in doc
    assert "HermesGateway" not in doc
    assert "%LOCALAPPDATA%\\hermes\\hermes-agent\\venv\\Scripts" in doc
    assert "LilSkrrtGateway" in doc
