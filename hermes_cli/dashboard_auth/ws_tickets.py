"""In-memory websocket ticket helpers for the fallback dashboard auth layer."""

from __future__ import annotations

import secrets
from dataclasses import dataclass


class TicketInvalid(Exception):
    pass


@dataclass(frozen=True)
class _TicketRecord:
    ticket: str


_TICKETS: set[str] = set()


def mint_ticket(user_id: str, provider: str) -> str:
    ticket = secrets.token_urlsafe(24)
    _TICKETS.add(ticket)
    return ticket


def consume_ticket(ticket: str) -> None:
    if ticket not in _TICKETS:
        raise TicketInvalid("unknown or expired ticket")
    _TICKETS.remove(ticket)
