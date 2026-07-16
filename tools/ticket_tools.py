"""Tool: raise a support ticket for a customer.

Collects name, phone and the issue, saves the ticket to SQLite, and returns a
confirmation the customer can reference. The current chat session is shared via
order_tools.set_current_session (already called by chat.py each turn).
"""

from typing import Any, Dict
from pydantic import BaseModel, Field
from langchain_core.tools import tool

import store
from tools import order_tools


class RaiseTicketInput(BaseModel):
    name: str = Field(..., description="The customer's name")
    phone: str = Field(..., description="The customer's phone number")
    issue: str = Field(..., description="A short description of the problem or query")


@tool("raise_ticket", args_schema=RaiseTicketInput, return_direct=False)
def raise_ticket_tool(name: str, phone: str, issue: str) -> Dict[str, Any]:
    """
    Raise a support ticket for the customer.

    Only call this AFTER you have collected the customer's name, phone number, and a
    short description of their issue. Returns the created ticket (with a ticket id)
    which you should confirm to the customer.
    """
    if not name or not phone or not issue:
        return {"error": "I still need the name, phone number and a short description of the issue."}

    session_id = order_tools._current_session_id
    ticket = store.create_ticket(session_id, name, phone, issue)
    return ticket
