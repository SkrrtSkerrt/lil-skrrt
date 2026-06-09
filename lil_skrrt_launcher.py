"""Lil Skrrt launcher entrypoint.

This wrapper lets users launch the agent with:
- ``a lil skrrt``
- ``lil-skrrt``

Both commands hand off to the real Lil Skrrt CLI after stripping the launcher
phrase from argv.
"""

from __future__ import annotations

import sys
from typing import Sequence


def _sanitize_args(argv: Sequence[str]) -> list[str]:
    args = list(argv)
    if len(args) >= 2 and args[0] == "lil" and args[1] == "skrrt":
        return args[2:]
    if len(args) >= 1 and args[0] == "lil-skrrt":
        return args[1:]
    return args


def main() -> int:
    sys.argv = [sys.argv[0], *_sanitize_args(sys.argv[1:])]
    from hermes_cli.main import main as hermes_main

    hermes_main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
