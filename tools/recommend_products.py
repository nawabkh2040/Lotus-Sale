"""Tool: recommend products from the local catalog by category/budget/similarity."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool

import catalog


class RecommendInput(BaseModel):
    category: Optional[str] = Field(
        None,
        description="Product category to recommend from, e.g. smartphone, television, "
        "laptop, ac, audio",
    )
    budget: Optional[float] = Field(
        None, description="Maximum budget in rupees, e.g. 20000"
    )
    based_on_product_id: Optional[int] = Field(
        None,
        description="Recommend products similar to this product id (from previous results)",
    )


@tool("recommend_products", args_schema=RecommendInput, return_direct=False)
def recommend_products_tool(
    category: Optional[str] = None,
    budget: Optional[float] = None,
    based_on_product_id: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Recommend suitable products to the customer.

    Use when the user asks for suggestions, alternatives, "what else", "recommend
    me...", or "something similar". Provide a category and/or budget, or a
    based_on_product_id to find similar items. Returns a list of recommended
    product objects.
    """
    recs = catalog.recommend(
        based_on_id=based_on_product_id, category=category, budget=budget
    )
    if not recs:
        return {"error": "No matching products found for those preferences."}
    return recs
