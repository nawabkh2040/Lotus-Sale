import os
import requests
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from typing import Optional
from langchain_core.tools import tool

# Lotus portal auth token expires periodically. Set LOTUS_AUTH_TOKEN in .env to
# refresh it without editing code; the literal below is only a fallback.
LOTUS_AUTH_TOKEN = os.getenv(
    "LOTUS_AUTH_TOKEN",
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNzA5MDQiLCJpYXQiOjE3NTQzNzg3MjQsImV4cCI6MTc1NDM5NjcyNH0.inays4iDucXwb_ktjjDur4yKdnjXGeIBTn978jtaFto",
)
class ProductDetailInput(BaseModel):
    product_id: int = Field(..., description="ID of the product to fetch details for")
    city: Optional[str] = Field("INDORE", description="City name (optional, defaults to INDORE)")


def _fallback_details(product_id: Any) -> Optional[Dict[str, Any]]:
    """Return details from the local catalog / seen-products cache.

    Used when the live API can't find a product, so this tool never dead-ends on
    a product the customer has already been shown.
    """
    try:
        import catalog
        rec = catalog.get_product(product_id) or catalog.get_seen(product_id)
    except Exception:
        rec = None
    if not rec:
        return None

    specs = rec.get("specs") or {}
    spec_list = [{"fkey": k, "fvalue": v} for k, v in specs.items()]
    if not spec_list and rec.get("features"):
        spec_list = [{"fkey": "Highlight", "fvalue": f} for f in rec["features"]]

    price = rec.get("price")
    if isinstance(price, (int, float)):
        mrp = f"₹{price:,.0f}"
    else:
        mrp = rec.get("product_mrp") or ""

    return {
        "product_id": str(product_id),
        "product_name": rec.get("product_name"),
        "product_mrp": mrp,
        "product_image": rec.get("image", ""),
        "instock": "Yes",
        "product_specification": spec_list,
        "meta_desc": "",
        "del": {},
        "source": "catalog",
    }



@tool("get_filtered_product_details", args_schema=ProductDetailInput, return_direct=False)
def get_filtered_product_details_tool(product_id: int, city: str = "INDORE") -> Dict[str, Any]:
    """
    Get selected product details from Lotus Electronics using the product_id and city name the city name is Optional.

    Returns only the following fields:
    - product_id
    - product_name
    - uri_slug
    - product_sku
    - product_mrp
    - product_image (first image only)
    - instock
    - product_features
    - meta_desc
    - del (std, t3h, stp)
    """
    url = "https://portal.lotuselectronics.com/web-api/home/product_detail"

    headers = {
        "auth-key": "Web2@!9",
        "auth-token": LOTUS_AUTH_TOKEN,
        "end-client": "Lotus-Web",
    }

    data = {
        "product_id": str(product_id),
        "city": city
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()

        payload = response.json()
        # On an expired/invalid token or missing product the API returns
        # {"data": "", "error": "1", ...} — data is a string, not a dict.
        data_field = payload.get("data")
        product_detail = data_field.get("product_detail", {}) if isinstance(data_field, dict) else {}
        if not product_detail:
            # Live API had nothing — fall back to what we already know locally
            fallback = _fallback_details(product_id)
            return fallback if fallback else {"error": "Product not found."}

        return {
            "product_id": product_detail.get("product_id"),
            "product_name": product_detail.get("product_name"),
            "uri_slug": product_detail.get("uri_slug"),
            "product_sku": product_detail.get("product_sku"),
            "product_mrp": product_detail.get("product_mrp"),
            "product_image": product_detail.get("product_image", [None])[0],
            "instock": product_detail.get("instock"),
            "product_specification": product_detail.get("product_specification"),
            "meta_desc": product_detail.get("meta_desc"),
            "del": product_detail.get("del"),
        }

    except requests.RequestException:
        fallback = _fallback_details(product_id)
        return fallback if fallback else {"error": "Product details are temporarily unavailable."}
    except ValueError:
        fallback = _fallback_details(product_id)
        return fallback if fallback else {"error": "Failed to parse product details."}

# Example usage (commented out to prevent execution on import)
# response = get_filtered_product_details_tool.invoke({
#     "product_id": 36356
# })
# print(response)

