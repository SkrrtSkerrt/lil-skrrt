#!/usr/bin/env python3
"""Repository secret scanner with redacted output.

This is intentionally dependency-free so CI can run it before project setup.
It scans tracked text files, reports only path/line/kind/fingerprint, and keeps
raw candidate values out of logs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf",
    ".zip", ".gz", ".tgz", ".xz", ".7z", ".mp4", ".mov", ".webm",
    ".sqlite", ".db", ".lock", ".woff", ".woff2", ".ttf",
}

ALLOW_HINTS = (
    "example", "placeholder", "dummy", "fake", "fixture", "sample",
    "your_", "your-", "<", ">", "***", "redacted", "xxxx", "token-here",
    "sk-test", "sk-fake", "not-a-real", "mock", "000000", "123456",
)

PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("github_classic_pat", re.compile(r"gh[pousr]_[A-Za-z0-9_]{36,}")),
    ("github_fine_grained_pat", re.compile(r"github_pat_[A-Za-z0-9_]{40,}")),
    ("openai_like_key", re.compile(r"\bsk-[A-Za-z0-9_-]{32,}\b")),
    ("anthropic_like_key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{32,}\b")),
    ("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("telegram_bot_token", re.compile(r"\b\d{6,12}:[A-Za-z0-9_-]{30,}\b")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private_key_header", re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA |PGP )?PRIVATE KEY-----")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
)

ASSIGNMENT_PATTERN = re.compile(
    r"(?i)\b(?:api[_-]?key|token|secret|password|private[_-]?key|client[_-]?secret)\b"
    r"\s*[:=]\s*[\"']?([A-Za-z0-9_./+=:-]{24,})"
)


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    kind: str
    fingerprint: str

    def key(self) -> str:
        # Keep allowlist entries stable across harmless line-number churn.
        return f"{self.path}:{self.kind}:{self.fingerprint}"


def repo_root() -> Path:
    out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    return Path(out)


def git_tracked_files(root: Path) -> list[Path]:
    out = subprocess.check_output(["git", "ls-files"], cwd=root, text=True)
    return [Path(line) for line in out.splitlines() if line]


def entropy(value: str) -> float:
    if not value:
        return 0.0
    return -sum((value.count(ch) / len(value)) * math.log2(value.count(ch) / len(value)) for ch in set(value))


def fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:16]


def plausible_secret(value: str, line: str) -> bool:
    low = f"{value} {line}".lower()
    if any(hint in low for hint in ALLOW_HINTS):
        return False
    if len(set(value)) < 8:
        return False
    return True


def scan_text(path: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if len(line) > 20_000:
            continue
        for kind, pattern in PATTERNS:
            for match in pattern.finditer(line):
                value = match.group(0)
                if plausible_secret(value, line):
                    findings.append(Finding(path, line_no, kind, fingerprint(value)))
        for match in ASSIGNMENT_PATTERN.finditer(line):
            value = match.group(1).strip().strip("\"'")
            if len(value) >= 24 and entropy(value) >= 3.6 and plausible_secret(value, line):
                findings.append(Finding(path, line_no, "high_entropy_secret_assignment", fingerprint(value)))
    return findings


def load_allowlist(root: Path) -> set[str]:
    path = root / ".secret-scan-allowlist.json"
    if not path.exists():
        return set()
    data = json.loads(path.read_text())
    entries = data.get("allowlist", [])
    return {str(item) for item in entries}


def write_allowlist(root: Path, findings: list[Finding]) -> None:
    path = root / ".secret-scan-allowlist.json"
    payload = {
        "comment": "Fingerprints for reviewed non-secret fixtures/placeholders. Do not add real secrets here.",
        "allowlist": sorted(f.key() for f in findings),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def scan_tree(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for rel in git_tracked_files(root):
        if rel.suffix.lower() in SKIP_EXTENSIONS:
            continue
        full = root / rel
        try:
            raw = full.read_bytes()
        except OSError:
            continue
        if b"\0" in raw[:4096]:
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("utf-8", "replace")
        findings.extend(scan_text(str(rel), text))
    return sorted(set(findings), key=lambda f: (f.path, f.line, f.kind, f.fingerprint))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan tracked files for likely committed secrets without printing secret values.")
    parser.add_argument("--update-allowlist", action="store_true", help="rewrite .secret-scan-allowlist.json with current findings")
    args = parser.parse_args(argv)

    root = repo_root()
    findings = scan_tree(root)
    if args.update_allowlist:
        write_allowlist(root, findings)
        print(f"updated .secret-scan-allowlist.json with {len(findings)} reviewed fingerprints")
        return 0

    allowed = load_allowlist(root)
    unreviewed = [finding for finding in findings if finding.key() not in allowed]
    stale = sorted(allowed - {finding.key() for finding in findings})

    if unreviewed:
        print(f"Secret scan failed: {len(unreviewed)} unreviewed finding(s). Values are not printed.")
        for finding in unreviewed[:200]:
            print(f"{finding.path}:{finding.line}: {finding.kind} fp={finding.fingerprint}")
        if len(unreviewed) > 200:
            print(f"... {len(unreviewed) - 200} more")
        print("If this is a reviewed fixture, run: python scripts/scan_secrets.py --update-allowlist")
        return 1

    if stale:
        print(f"Secret scan warning: {len(stale)} stale allowlist entr{'y' if len(stale) == 1 else 'ies'}.")
        print("Run: python scripts/scan_secrets.py --update-allowlist")

    print(f"Secret scan passed: {len(findings)} reviewed finding(s), 0 unreviewed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
