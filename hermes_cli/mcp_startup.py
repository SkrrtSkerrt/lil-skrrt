"""Compatibility helpers for deferred MCP discovery startup.

The CLI imports this module to kick off MCP tool discovery in the background
and to wait for that discovery before rendering tool/status output.

The repo already has the actual discovery implementation in tools.mcp_tool;
this module just provides the small startup surface cli.py expects.
"""

from __future__ import annotations

import logging
import threading
from typing import Optional

from tools.mcp_tool import discover_mcp_tools

logger = logging.getLogger(__name__)

_DISCOVERY_THREAD: Optional[threading.Thread] = None
_DISCOVERY_LOCK = threading.Lock()
_DISCOVERY_STARTED = False


def _run_discovery() -> None:
    try:
        discover_mcp_tools()
    except Exception:
        logger.debug("MCP background discovery failed", exc_info=True)


def start_background_mcp_discovery(*, logger: logging.Logger | None = None, thread_name: str = "mcp-discovery") -> None:
    """Start MCP tool discovery in a background daemon thread if needed."""
    del logger  # compatibility parameter; the module logger handles diagnostics.
    global _DISCOVERY_THREAD, _DISCOVERY_STARTED
    with _DISCOVERY_LOCK:
        if _DISCOVERY_STARTED and _DISCOVERY_THREAD and _DISCOVERY_THREAD.is_alive():
            return
        _DISCOVERY_STARTED = True
        thread = threading.Thread(target=_run_discovery, name=thread_name, daemon=True)
        _DISCOVERY_THREAD = thread
        thread.start()


def wait_for_mcp_discovery(timeout: float | None = None) -> None:
    """Wait for any in-flight MCP discovery thread to finish.

    If discovery was never started, this is a cheap no-op.
    """
    thread = _DISCOVERY_THREAD
    if thread is None:
        return
    thread.join(timeout=timeout)
