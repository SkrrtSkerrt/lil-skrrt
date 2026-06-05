"""Compatibility helpers for CLI /compress partial compaction.

The CLI and TUI call into this module for a small set of helpers:
- parse_partial_compress_args()
- split_history_for_partial_compress()
- rejoin_compressed_head_and_tail()

This file keeps those imports stable while implementing the minimal behavior
expected by the existing command flow and tests.
"""

from __future__ import annotations

from typing import Any, Iterable, Optional, Sequence, Tuple


def parse_partial_compress_args(raw_args: str) -> tuple[bool, int, Optional[str]]:
    """Parse `/compress` arguments.

    Returns `(partial, keep_last, focus_topic)` where:
    - `partial` is True for `here` mode
    - `keep_last` defaults to 2 in `here` mode
    - `focus_topic` is the free-form remainder for focused compression
    """
    text = (raw_args or "").strip()
    if not text:
        return False, 0, None

    tokens = text.split()
    if tokens[0].lower() != "here":
        return False, 0, text or None

    partial = True
    keep_last = 2
    tokens = tokens[1:]
    if tokens:
        first = tokens[0]
        try:
            keep_last = int(first)
            tokens = tokens[1:]
        except ValueError:
            pass
    focus_topic = " ".join(tokens).strip() or None
    return partial, keep_last, focus_topic


def split_history_for_partial_compress(
    history: Sequence[dict[str, Any]], keep_last: int
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split a transcript into a compressible head and a verbatim tail.

    The tail begins at the start of the most recent `keep_last` user turns so
    the preserved portion remains a clean exchange boundary.
    """
    if keep_last <= 0:
        return list(history), []

    user_turns = 0
    split_index = len(history)
    for idx in range(len(history) - 1, -1, -1):
        role = str(history[idx].get("role", ""))
        if role == "user":
            user_turns += 1
            if user_turns == keep_last:
                split_index = idx
                break
    if split_index <= 0 or split_index >= len(history):
        return list(history), []
    return list(history[:split_index]), list(history[split_index:])


def rejoin_compressed_head_and_tail(
    compressed_head: Sequence[dict[str, Any]],
    tail: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Append a preserved tail to compressed content while keeping roles sane."""
    head = list(compressed_head)
    tail_list = list(tail)
    if not head:
        return tail_list
    if not tail_list:
        return head

    last_role = str(head[-1].get("role", ""))
    while tail_list and str(tail_list[0].get("role", "")) == last_role:
        tail_list.pop(0)
    return head + tail_list
