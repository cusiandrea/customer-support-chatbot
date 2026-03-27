import json
import uuid
from datetime import datetime
from typing import Dict, List

from app.config import TICKETS_PATH


def generate_ticket_id() -> str:
    short_id = str(uuid.uuid4()).split("-")[0].upper()
    return f"TCK-{short_id}"


def load_existing_tickets() -> List[Dict]:
    """
    Load existing tickets from the local JSON file.
    If the file does not exist yet, return an empty list.
    """
    if not TICKETS_PATH.exists():
        return []

    with open(TICKETS_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []


def save_ticket(ticket: Dict) -> None:
    """
    Append a new ticket to the local JSON file.
    """
    TICKETS_PATH.parent.mkdir(parents=True, exist_ok=True)

    tickets = load_existing_tickets()
    tickets.append(ticket)

    with open(TICKETS_PATH, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2, ensure_ascii=False)


def generate_handoff_message(user_query: str, category: str, reason: str) -> Dict:
    ticket = {
        "ticket_id": generate_ticket_id(),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": category,
        "status": "open",
        "reason_for_handoff": reason,
        "customer_request": user_query
    }

    save_ticket(ticket)

    customer_message = (
        "Your request has been forwarded to a human support agent and a support ticket has been opened.\n\n"
        f"**Ticket ID:** {ticket['ticket_id']}\n"
        f"**Category:** {ticket['category']}\n"
        f"**Status:** {ticket['status']}\n\n"
        "A support agent will review your case as soon as possible. "
        "Please keep your ticket ID for future reference."
    )

    return {
        "customer_message": customer_message,
        "ticket": ticket
    }