"""test_manager.py - Unit tests for the shared core."""

import unittest
from expense import Expense
from tracker import ExpenseTracker


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

class TestChecks(unittest.TestCase):
    """Tests for checking input (FR-02, FR-03, FR-04)."""

    def setUp(self):
        self.tracker = ExpenseTracker()

    def test_bad_amounts_rejected(self):
        for bad in ["abc", "0", "-5", "999999"]:
            with self.assertRaises(ValueError):
                self.tracker.check_amount(bad)

    def test_good_amounts_cleaned(self):
        self.assertEqual(self.tracker.check_amount("£12.50"), 12.5)
        self.assertEqual(self.tracker.check_amount("12.345"), 12.35)
        self.assertEqual(self.tracker.check_amount("1,250"), 1250)

    def test_bad_dates_rejected(self):
        for bad in ["31/02/2026", "22/22/22", "01/01/1999", "2026-11-16"]:
            with self.assertRaises(ValueError):
                self.tracker.check_date(bad)

    def test_good_date_accepted(self):
        self.assertEqual(self.tracker.check_date("16/11/2026"), "16/11/2026")

    def test_category_any_capitals(self):
        self.assertEqual(self.tracker.check_category("food"), "Food")

    def test_bad_category_rejected(self):
        for bad in ["Holiday", ""]:
            with self.assertRaises(ValueError):
                self.tracker.check_category(bad)


class TestAddEditDelete(unittest.TestCase):
    """Tests for adding, editing, deleting and the total (FR-01, FR-05, FR-06, FR-07)."""

    def setUp(self):
        self.tracker = ExpenseTracker()
        self.tracker.add_expense("12.50", "16/11/2026", "food", "Lunch")
        self.tracker.add_expense("2", "16/11/2026", "Transport", "Bus")

    def test_add(self):
        self.assertEqual(len(self.tracker.expenses), 2)
        self.assertEqual(self.tracker.expenses[0].category, "Food")

    def test_add_bad_input_adds_nothing(self):
        with self.assertRaises(ValueError):
            self.tracker.add_expense("abc", "16/11/2026", "Food")
        self.assertEqual(len(self.tracker.expenses), 2)

    def test_total(self):
        self.assertEqual(self.tracker.total(), 14.5)

    def test_edit(self):
        self.tracker.edit_expense(1, "20", "16/11/2026", "Food", "Dinner")
        self.assertEqual(self.tracker.expenses[0].amount, 20)
        self.assertEqual(self.tracker.expenses[0].note, "Dinner")

    def test_edit_bad_amount_rejected(self):
        with self.assertRaises(ValueError):
            self.tracker.edit_expense(1, "abc", "16/11/2026", "Food")
        self.assertEqual(self.tracker.expenses[0].amount, 12.5)

    def test_delete(self):
        self.tracker.delete_expense(2)
        self.assertEqual(len(self.tracker.expenses), 1)

    def test_wrong_number_rejected(self):
        for bad in [0, 3, "x"]:
            with self.assertRaises(ValueError):
                self.tracker.delete_expense(bad)

if __name__ == "__main__":
    unittest.main()