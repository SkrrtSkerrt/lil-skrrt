"""Public API paths for the Lil Skrrt dashboard auth gate.

These endpoints are intentionally read-only and safe to expose without the
session token so the dashboard can probe liveness and render basic catalog
information.
"""

from __future__ import annotations

PUBLIC_API_PATHS = frozenset(
    {
        "/api/status",
        "/api/dashboard/plugins",
        "/api/messaging/platforms",
        "/api/model/info",
    }
)
