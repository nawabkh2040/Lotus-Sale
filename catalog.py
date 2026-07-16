"""
Local dummy product catalog for Lotus Electronics.

The live product-detail API token is expired, so comparison, recommendation and
order features read from this in-memory catalog instead. Product field names match
what `tools/product_search_tool.py` returns (product_id, product_name, product_mrp,
product_url, product_image, features) so the frontend renders everything the same
way. Some IDs intentionally overlap the real search results (e.g. 39422, 39831).
"""

from typing import Any, Dict, List, Optional

_IMG = "https://cdn.lotuselectronics.com/webpimages"

# Each product: numeric-string product_id, price is an int (rupees).
_CATALOG: List[Dict[str, Any]] = [
    {
        "product_id": "39422",
        "product_name": "Redmi 14C 5G (4GB RAM, 64GB Storage) Stargaze Black",
        "brand": "Redmi",
        "category": "smartphone",
        "price": 9499,
        "image": f"{_IMG}/7045810IM.webp",
        "specs": {
            "Display": "6.88 inch HD+ 120Hz",
            "Processor": "Snapdragon 4s Gen 2",
            "RAM": "4GB",
            "Storage": "64GB",
            "Battery": "5160 mAh",
            "Rear Camera": "50MP",
            "Network": "5G",
            "Warranty": "1 Year",
        },
        "features": ["5G connectivity", "120Hz display", "50MP camera", "5160 mAh battery"],
    },
    {
        "product_id": "39831",
        "product_name": "Redmi A5 4G (4GB RAM, 128GB ROM) Jaisalmer Gold",
        "brand": "Redmi",
        "category": "smartphone",
        "price": 7499,
        "image": f"{_IMG}/718961IM.webp",
        "specs": {
            "Display": "6.88 inch HD+ 120Hz",
            "Processor": "Octa Core",
            "RAM": "4GB",
            "Storage": "128GB",
            "Battery": "5200 mAh",
            "Rear Camera": "32MP",
            "Network": "4G",
            "Warranty": "1 Year",
        },
        "features": ["128GB storage", "Large 5200 mAh battery", "32MP camera", "Octa Core"],
    },
    {
        "product_id": "40089",
        "product_name": "Samsung Galaxy A26 5G (6GB RAM, 128GB Storage) White",
        "brand": "Samsung",
        "category": "smartphone",
        "price": 21557,
        "image": f"{_IMG}/722651IM.webp",
        "specs": {
            "Display": "6.7 inch Super AMOLED 120Hz",
            "Processor": "Exynos 1380",
            "RAM": "6GB",
            "Storage": "128GB",
            "Battery": "5000 mAh",
            "Rear Camera": "50MP OIS",
            "Network": "5G",
            "Warranty": "1 Year",
        },
        "features": ["Super AMOLED display", "50MP OIS camera", "5G", "IP67 water resistant"],
    },
    {
        "product_id": "38210",
        "product_name": "OnePlus Nord CE4 Lite 5G (8GB RAM, 128GB Storage) Mega Blue",
        "brand": "OnePlus",
        "category": "smartphone",
        "price": 19999,
        "image": f"{_IMG}/731201IM.webp",
        "specs": {
            "Display": "6.67 inch AMOLED 120Hz",
            "Processor": "Snapdragon 695",
            "RAM": "8GB",
            "Storage": "128GB",
            "Battery": "5500 mAh",
            "Rear Camera": "50MP",
            "Network": "5G",
            "Warranty": "1 Year",
        },
        "features": ["8GB RAM", "5500 mAh battery", "80W fast charge", "AMOLED 120Hz"],
    },
    {
        "product_id": "38455",
        "product_name": "iPhone 15 (128GB) Blue",
        "brand": "Apple",
        "category": "smartphone",
        "price": 65999,
        "image": f"{_IMG}/700011IM.webp",
        "specs": {
            "Display": "6.1 inch Super Retina XDR",
            "Processor": "A16 Bionic",
            "RAM": "6GB",
            "Storage": "128GB",
            "Battery": "3349 mAh",
            "Rear Camera": "48MP Dual",
            "Network": "5G",
            "Warranty": "1 Year",
        },
        "features": ["A16 Bionic chip", "48MP camera", "Dynamic Island", "iOS 17"],
    },
    {
        "product_id": "41002",
        "product_name": "Samsung 108cm (43 inch) 4K Ultra HD Smart LED TV",
        "brand": "Samsung",
        "category": "television",
        "price": 32990,
        "image": f"{_IMG}/650101IM.webp",
        "specs": {
            "Screen Size": "43 inch",
            "Resolution": "4K Ultra HD",
            "Panel": "LED",
            "Refresh Rate": "60Hz",
            "Smart OS": "Tizen",
            "HDMI Ports": "3",
            "Warranty": "1 Year",
        },
        "features": ["4K Ultra HD", "Tizen Smart TV", "HDR10+", "3 HDMI ports"],
    },
    {
        "product_id": "41055",
        "product_name": "LG 139cm (55 inch) 4K OLED Smart TV",
        "brand": "LG",
        "category": "television",
        "price": 99990,
        "image": f"{_IMG}/651201IM.webp",
        "specs": {
            "Screen Size": "55 inch",
            "Resolution": "4K Ultra HD",
            "Panel": "OLED",
            "Refresh Rate": "120Hz",
            "Smart OS": "webOS",
            "HDMI Ports": "4",
            "Warranty": "1 Year",
        },
        "features": ["OLED panel", "120Hz refresh", "Dolby Vision IQ", "webOS"],
    },
    {
        "product_id": "42010",
        "product_name": "HP Pavilion 15 (Intel Core i5, 16GB RAM, 512GB SSD)",
        "brand": "HP",
        "category": "laptop",
        "price": 61990,
        "image": f"{_IMG}/660301IM.webp",
        "specs": {
            "Processor": "Intel Core i5 13th Gen",
            "RAM": "16GB",
            "Storage": "512GB SSD",
            "Display": "15.6 inch FHD",
            "Graphics": "Intel Iris Xe",
            "OS": "Windows 11",
            "Warranty": "1 Year",
        },
        "features": ["13th Gen Core i5", "16GB RAM", "512GB SSD", "FHD display"],
    },
    {
        "product_id": "42077",
        "product_name": "Lenovo IdeaPad Slim 3 (AMD Ryzen 5, 8GB RAM, 512GB SSD)",
        "brand": "Lenovo",
        "category": "laptop",
        "price": 46990,
        "image": f"{_IMG}/661101IM.webp",
        "specs": {
            "Processor": "AMD Ryzen 5 7530U",
            "RAM": "8GB",
            "Storage": "512GB SSD",
            "Display": "15.6 inch FHD",
            "Graphics": "AMD Radeon",
            "OS": "Windows 11",
            "Warranty": "1 Year",
        },
        "features": ["Ryzen 5", "8GB RAM", "512GB SSD", "Lightweight"],
    },
    {
        "product_id": "43001",
        "product_name": "LG 1.5 Ton 5 Star Dual Inverter Split AC",
        "brand": "LG",
        "category": "ac",
        "price": 42990,
        "image": f"{_IMG}/670101IM.webp",
        "specs": {
            "Capacity": "1.5 Ton",
            "Star Rating": "5 Star",
            "Type": "Split Inverter",
            "Compressor": "Dual Inverter",
            "Cooling": "18000 BTU",
            "Warranty": "1 Yr unit, 10 Yr compressor",
        },
        "features": ["5 Star rating", "Dual Inverter", "Copper condenser", "Low noise"],
    },
    {
        "product_id": "43044",
        "product_name": "Voltas 1.5 Ton 3 Star Split AC",
        "brand": "Voltas",
        "category": "ac",
        "price": 32990,
        "image": f"{_IMG}/671201IM.webp",
        "specs": {
            "Capacity": "1.5 Ton",
            "Star Rating": "3 Star",
            "Type": "Split Inverter",
            "Compressor": "Inverter",
            "Cooling": "17500 BTU",
            "Warranty": "1 Yr unit, 10 Yr compressor",
        },
        "features": ["3 Star", "Turbo cooling", "Copper condenser", "Anti-dust filter"],
    },
    {
        "product_id": "44012",
        "product_name": "boAt Airdopes 141 Wireless Earbuds",
        "brand": "boAt",
        "category": "audio",
        "price": 1499,
        "image": f"{_IMG}/680101IM.webp",
        "specs": {
            "Type": "TWS Earbuds",
            "Battery": "42 Hrs playback",
            "Driver": "8mm",
            "Bluetooth": "5.1",
            "Charging": "Type-C",
            "Warranty": "1 Year",
        },
        "features": ["42H playback", "ENx tech", "Low latency", "IPX4"],
    },
]

# Fast lookup by id
_BY_ID: Dict[str, Dict[str, Any]] = {p["product_id"]: p for p in _CATALOG}


def _fmt_price(price: int) -> str:
    return f"₹{price:,.0f}"


def _public_view(p: Dict[str, Any]) -> Dict[str, Any]:
    """Shape a catalog record into the product object the frontend expects."""
    return {
        "product_id": p["product_id"],
        "product_name": p["product_name"],
        "product_mrp": _fmt_price(p["price"]),
        "product_image": p["image"],
        "product_url": f"https://www.lotuselectronics.com/product/{p['product_id']}",
        "features": p["features"],
    }


def get_product(product_id: Any) -> Optional[Dict[str, Any]]:
    """Return the raw catalog record for an id, or None."""
    return _BY_ID.get(str(product_id))


def get_product_view(product_id: Any) -> Optional[Dict[str, Any]]:
    """Return the frontend-facing product object for an id, or None."""
    p = get_product(product_id)
    return _public_view(p) if p else None


def find_by_category(category: str, budget: Optional[float] = None) -> List[Dict[str, Any]]:
    cat = (category or "").lower().strip()
    matches = [p for p in _CATALOG if p["category"] == cat]
    if budget:
        matches = [p for p in matches if p["price"] <= float(budget)]
    return matches


def recommend(
    based_on_id: Optional[Any] = None,
    category: Optional[str] = None,
    budget: Optional[float] = None,
    exclude: Optional[List[Any]] = None,
    limit: int = 4,
) -> List[Dict[str, Any]]:
    """Recommend products by category/budget, or similar to a given product."""
    exclude_ids = {str(x) for x in (exclude or [])}

    base = get_product(based_on_id) if based_on_id else None
    if base:
        category = category or base["category"]
        exclude_ids.add(base["product_id"])
        # Default budget window around the base product if none supplied
        if budget is None:
            budget = base["price"] * 1.6

    if category:
        pool = find_by_category(category, budget)
    else:
        pool = [p for p in _CATALOG if (budget is None or p["price"] <= float(budget))]

    pool = [p for p in pool if p["product_id"] not in exclude_ids]
    # Cheapest-first tends to read as good value in a sales context
    pool.sort(key=lambda p: p["price"])
    return [_public_view(p) for p in pool[:limit]]


def compare(id_a: Any, id_b: Any) -> Dict[str, Any]:
    """Build a spec-by-spec comparison of two products.

    Returns a dict with name/vs_name, a human-readable `differences` list, a
    `spec_table` (rows of {feature, a, b}) and a simple `verdict`. Falls back
    gracefully when an id is unknown.
    """
    a = get_product(id_a)
    b = get_product(id_b)
    if not a or not b:
        missing = id_a if not a else id_b
        return {"error": f"Product {missing} is not in our catalog for comparison."}

    keys: List[str] = list(a["specs"].keys())
    for k in b["specs"]:
        if k not in keys:
            keys.append(k)

    spec_table = []
    differences = []
    spec_table.append({"feature": "Price", "a": _fmt_price(a["price"]), "b": _fmt_price(b["price"])})
    for k in keys:
        av = a["specs"].get(k, "-")
        bv = b["specs"].get(k, "-")
        spec_table.append({"feature": k, "a": av, "b": bv})
        if av != bv and av != "-" and bv != "-":
            differences.append(f"{k}: {a['brand']} has {av} vs {b['brand']} {bv}")

    cheaper = a if a["price"] <= b["price"] else b
    verdict = (
        f"{cheaper['product_name']} is the more budget-friendly option at "
        f"{_fmt_price(cheaper['price'])}."
    )

    return {
        "name": a["product_name"],
        "vs_name": b["product_name"],
        "price_a": _fmt_price(a["price"]),
        "price_b": _fmt_price(b["price"]),
        "image_a": a["image"],
        "image_b": b["image"],
        "differences": differences or ["Both products share very similar specifications."],
        "spec_table": spec_table,
        "verdict": verdict,
    }
