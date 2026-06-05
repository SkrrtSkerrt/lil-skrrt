"""Minimal audit log surface for websocket ticket validation."""

from __future__ import annotations

from enum import Enum


class AuditEvent(str, Enum):
    WS_TICKET_REJECTED = "ws_ticket_rejected"


def audit_log(*args, **kwargs):
    """Compatibility no-op audit logger."""
    return None
