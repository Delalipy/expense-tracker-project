"""test_manager.py - Unit tests for the shared core."""

import unittest
from expense import Expense


class TestExpense(unittest.TestCase):
    """Tests for the Expense class (FR-01)."""

    def test_stores_details(self):
        expense = Expense(12.5, "10/11/2026", "Food", "Lunch")
        self.assertEqual(expense.amount, 12.5)
        self.assertEqual(expense.category, "Food")

    def test_note_is_optional(self):
        expense = Expense(2.0, "10/11/2026", "Transport")
        self.assertEqual(expense.note, "")

    def test_to_list_gives_csv_row(self):
        expense = Expense(12.5, "10/11/2026", "Food", "Lunch")
        self.assertEqual(expense.to_list(), [12.5, "10/11/2026", "Food", "Lunch"])

    def test_printed_format(self):
        expense = Expense(12.5, "10/11/2026", "Food", "Lunch")
        self.assertEqual(str(expense), "10/11/2026 | Food | £12.50 | Lunch")


if __name__ == "__main__":
    unittest.main()