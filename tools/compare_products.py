"""Tool: compare two (or more) products spec-by-spec from the local catalog."""

from typing import Any, Dict, List
from pydantic import BaseModel, Field
from langchain_core.tools import tool

import catalog


class CompareInput(BaseModel):
    product_ids: List[int] = Field(
        ...,
        description="List of exactly two product IDs to compare, e.g. [39422, 39831]",
    )


@tool("compare_products", args_schema=CompareInput, return_direct=False)
def compare_products_tool(product_ids: List[int]) -> Dict[str, Any]:
    """
    Compare two products side by side using the Lotus catalog.

    Provide two product_ids (extract them from the previous search results in the
    conversation). Returns a structured comparison with a spec-by-spec table, the
    key differences, and a short verdict on value for money.
    """
    if not product_ids or len(product_ids) < 2:
        return {"error": "Please provide two product IDs to compare."}
    result = catalog.compare(product_ids[0], product_ids[1])
    return result
