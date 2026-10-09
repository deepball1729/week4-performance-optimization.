"""Baseline implementation: intentionally inefficient sales-data aggregation."""
from __future__ import annotations

def summarize_sales(records: list[dict]) -> dict:
    """Return total revenue and revenue by product category.

    Each record has: category (str), quantity (int), unit_price (float).
    This baseline repeatedly scans the full input once for every category.
    """
    categories = []
    for record in records:
        if record["category"] not in categories:
            categories.append(record["category"])

    total_revenue = 0.0
    revenue_by_category = {}
    for record in records:
        total_revenue += record["quantity"] * record["unit_price"]

    for category in categories:
        category_revenue = 0.0
        for record in records:
            if record["category"] == category:
                category_revenue += record["quantity"] * record["unit_price"]
        revenue_by_category[category] = round(category_revenue, 2)

    return {
        "record_count": len(records),
        "total_revenue": round(total_revenue, 2),
        "revenue_by_category": revenue_by_category,
    }

def make_dataset(size: int = 20_000, category_count: int = 80) -> list[dict]:
    """Generate deterministic synthetic data without external files."""
    return [
        {
            "category": f"category_{(i * 17 + i // 7) % category_count:03d}",
            "quantity": (i % 9) + 1,
            "unit_price": ((i * 13) % 997) / 10 + 0.99,
        }
        for i in range(size)
    ]

if __name__ == "__main__":
    data = make_dataset()
    print(summarize_sales(data))
