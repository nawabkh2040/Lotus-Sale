"""Tools: place a dummy order and track an existing order.

The current chat session id is injected via `set_current_session()` (called by
chat.py before running the graph) so `place_order` can attribute the order to the
right session without the LLM needing to know it.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool

import catalog
import store

# Set per-request by chat.py so place_order can tie the order to a session.
_current_session_id: Optional[str] = None


def set_current_session(session_id: Optional[str]) -> None:
    global _current_session_id
    _current_session_id = session_id


class PlaceOrderInput(BaseModel):
    product_id: int = Field(..., description="The product id the customer wants to order")


class TrackOrderInput(BaseModel):
    order_id: str = Field(
        ..., description="The order id to track, e.g. LOTUS1001 (with or without the LOTUS prefix)"
    )


@tool("place_order", args_schema=PlaceOrderInput, return_direct=False)
def place_order_tool(product_id: int) -> Dict[str, Any]:
    """
    Place an order for a product and return a trackable order confirmation.

    Use when the customer wants to buy/order a specific product (extract the
    product_id from previous results). Returns the new order id, status and a
    delivery timeline the customer can track later.
    """
    product = catalog.get_product_view(product_id)
    if not product:
        return {"error": f"Product {product_id} is not available to order right now."}
    order = store.create_order(_current_session_id, product)
    return order


@tool("track_order", args_schema=TrackOrderInput, return_direct=False)
def track_order_tool(order_id: str) -> Dict[str, Any]:
    """
    Track the status of an existing order by its order id (e.g. LOTUS1001).

    Returns the current status, order/delivery dates and a stage-by-stage timeline.
    """
    order = store.get_order(order_id)
    if not order:
        return {"error": f"No order found with id {order_id}. Please check the order id."}
    return order
