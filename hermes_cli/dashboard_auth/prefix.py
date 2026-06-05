"""Prefix normalization helpers for dashboard reverse-proxy support."""

from __future__ import annotations


def normalise_prefix(raw: str | None) -> str:
    if not raw:
        return ""
    prefix = raw.strip()
    if not prefix or prefix == "/":
        return ""
    if not prefix.startswith("/"):
        prefix = "/" + prefix
    return prefix.rstrip("/")
