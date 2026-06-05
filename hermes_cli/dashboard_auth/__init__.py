"""Compatibility dashboard-auth package for the Hermes web server.

The original project references a dedicated ``hermes_cli.dashboard_auth``
package for the OAuth gate. Some test and runtime paths only need a small
subset of that surface area, so this package provides a lightweight fallback
that keeps imports working when the full auth plugin set is absent.
"""

from __future__ import annotations

from .public_paths import PUBLIC_API_PATHS
from .routes import router


class _AuthProvider:
    def __init__(self, name: str):
        self.name = name


def list_providers() -> list[_AuthProvider]:
    """Return discovered dashboard auth providers.

    The fallback build does not ship any OAuth providers, so this returns an
    empty list. The web server already handles the no-provider case by
    refusing non-loopback binds when auth is required.
    """
    return []


__all__ = ["PUBLIC_API_PATHS", "list_providers", "router"]
