"""Correctness tests comparing baseline and optimized behavior."""
import unittest
from original import summarize_sales as original_summary
from optimized import summarize_sales as optimized_summary, make_dataset

class SummaryTests(unittest.TestCase):
    def assertEquivalent(self, records):
        self.assertEqual(original_summary(records), optimized_summary(records))

    def test_empty_input(self):
        self.assertEquivalent([])

    def test_single_record(self):
        self.assertEquivalent([{"category": "books", "quantity": 2, "unit_price": 3.5}])

    def test_multiple_categories(self):
        self.assertEquivalent([
            {"category": "books", "quantity": 2, "unit_price": 3.5},
            {"category": "food", "quantity": 4, "unit_price": 1.25},
            {"category": "books", "quantity": 1, "unit_price": 10.0},
        ])

    def test_generated_dataset(self):
        self.assertEquivalent(make_dataset(250, 12))

    def test_record_count_and_totals(self):
        result = optimized_summary([
            {"category": "x", "quantity": 3, "unit_price": 2.0},
            {"category": "y", "quantity": 1, "unit_price": 5.0},
        ])
        self.assertEqual(result["record_count"], 2)
        self.assertEqual(result["total_revenue"], 11.0)
        self.assertEqual(result["revenue_by_category"], {"x": 6.0, "y": 5.0})

if __name__ == "__main__":
    unittest.main()
