from __future__ import annotations

from pathlib import Path

import pytest

from scripts import scan_secrets


def test_scan_text_detects_likely_secret_without_value_in_key() -> None:
    value = "github_pat_" + "A" * 82

    findings = scan_secrets.scan_text("demo.txt", f"token={value}\n")

    assert findings
    rendered = findings[0].key()
    assert findings[0].kind == "github_fine_grained_pat"
    assert value not in rendered
    assert "fp=" not in rendered


def test_scan_text_ignores_obvious_placeholders() -> None:
    text = "OPENAI_API_KEY=sk-test-" + "A" * 40

    assert scan_secrets.scan_text("demo.txt", text) == []


def test_allowlist_update_round_trip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = tmp_path
    finding = scan_secrets.Finding("demo.txt", 3, "openai_like_key", "abc123")

    scan_secrets.write_allowlist(root, [finding])

    assert scan_secrets.load_allowlist(root) == {finding.key()}
