"""Optimized implementation: single-pass sales-data aggregation."""
from __future__ import annotations

def summarize_sales(records: list[dict]) -> dict:
    """Return the same summary as the baseline using one pass over records."""
    total_revenue = 0.0
    revenue_by_category = {}

    for record in records:
        category = record["category"]
        revenue = record["quantity"] * record["unit_price"]
        total_revenue += revenue
        revenue_by_category[category] = revenue_by_category.get(category, 0.0) + revenue

    return {
        "record_count": len(records),
        "total_revenue": round(total_revenue, 2),
        "revenue_by_category": {
            category: round(revenue, 2)
            for category, revenue in revenue_by_category.items()
        },
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
