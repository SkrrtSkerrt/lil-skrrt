"""Fallback auth middleware used when the OAuth dashboard package is absent."""

from __future__ import annotations


async def gated_auth_middleware(request, call_next):
    """No-op gate used by the compatibility package.

    The legacy session-token middleware in ``hermes_cli.web_server`` still
    enforces access control for /api/ routes that are not listed in
    ``PUBLIC_API_PATHS``.
    """
    return await call_next(request)
