"""Tool: browse products from the local Lotus catalog by category/budget.

Used so the assistant can always show real products even when the live vector
search is unavailable or returns nothing. Backed by `catalog.py`.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool

import catalog


class BrowseInput(BaseModel):
    category: Optional[str] = Field(
        None,
        description="Category to browse, e.g. smartphone, television, laptop, ac, audio",
    )
    budget: Optional[float] = Field(
        None, description="Maximum budget in rupees, e.g. 30000"
    )


@tool("browse_catalog", args_schema=BrowseInput, return_direct=False)
def browse_catalog_tool(
    category: Optional[str] = None, budget: Optional[float] = None
) -> List[Dict[str, Any]]:
    """
    Browse products available in the Lotus in-store catalog.

    Use this to show products when the customer wants to browse a category, or as a
    fallback when search_products returns no results. Provide a category and/or a
    budget. Returns a list of product objects (put them in the "products" field).
    """
    products = catalog.browse(category=category, budget=budget)
    if not products:
        return {"error": "No products found in the catalog for those preferences."}
    return products
