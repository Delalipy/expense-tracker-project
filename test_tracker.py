"""test_tracker.py - Unit tests for the shared core."""

import unittest
from expense import Expense
from tracker import ExpenseTracker
import os
import tempfile
import storage

class TestStorage(unittest.TestCase):
    """Tests for saving and loading CSV files (FR-08, FR-09)."""

    def setUp(self):
        folder = tempfile.mkdtemp()  # a throwaway folder, so real files are not touched
        self.expense_file = os.path.join(folder, "expenses.csv")
        self.budget_file = os.path.join(folder, "budgets.csv")

    def test_save_then_load_expenses(self):
        expenses = [Expense(12.5, "16/11/2026", "Food", "Tesco"),
                    Expense(2.0, "17/11/2026", "Transport", "")]
        storage.save_expenses(expenses, self.expense_file)
        loaded = storage.load_expenses(self.expense_file)
        self.assertEqual([e.to_list() for e in loaded], [e.to_list() for e in expenses])

    def test_missing_file_gives_empty_list(self):
        self.assertEqual(storage.load_expenses(self.expense_file), [])

    def test_broken_rows_are_skipped(self):
        with open(self.expense_file, "w", encoding="utf-8") as file:
            file.write("amount,date,category,note\n")
            file.write("abc,16/11/2026,Food,bad amount\n")
            file.write("5,16/11/2026\n")
            file.write("3,16/11/2026,Food,good row\n")
        loaded = storage.load_expenses(self.expense_file)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].note, "good row")

    def test_save_then_load_budgets(self):
        storage.save_budgets({"11/2026": 750.0}, self.budget_file)
        self.assertEqual(storage.load_budgets(self.budget_file), {"11/2026": 750.0})

    def test_note_with_comma_survives(self):
        storage.save_expenses([Expense(4.0, "16/11/2026", "Food", "milk, bread")], self.expense_file)
        self.assertEqual(storage.load_expenses(self.expense_file)[0].note, "milk, bread")
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


class TestSearch(unittest.TestCase):
    """Tests for search and filter (FR-10, FR-11)."""

    def setUp(self):
        self.tracker = ExpenseTracker()
        self.tracker.add_expense("12.50", "16/11/2026", "Food", "Tesco lunch")
        self.tracker.add_expense("2", "16/11/2026", "Transport", "Bus")
        self.tracker.add_expense("30", "03/10/2026", "Food", "Aldi")

    def test_nothing_given_returns_all(self):
        self.assertEqual(len(self.tracker.search()), 3)

    def test_by_category(self):
        self.assertEqual(len(self.tracker.search(category="food")), 2)

    def test_by_month(self):
        self.assertEqual(len(self.tracker.search(month="11/2026")), 2)

    def test_by_category_and_month(self):
        results = self.tracker.search(category="Food", month="11/2026")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].note, "Tesco lunch")

    def test_keyword_any_capitals(self):
        results = self.tracker.search(keyword="TESCO")
        self.assertEqual(len(results), 1)
class TestSort(unittest.TestCase):
    """Tests for bubble sort (FR-12)."""

    def setUp(self):
        self.tracker = ExpenseTracker()
        self.tracker.add_expense("30", "03/10/2026", "Food", "Aldi")
        self.tracker.add_expense("2", "16/11/2026", "Transport", "Bus")
        self.tracker.add_expense("12.50", "01/02/2025", "Food", "Tesco")

    def test_sort_by_amount(self):
        amounts = [e.amount for e in self.tracker.sort_by("amount")]
        self.assertEqual(amounts, [2.0, 12.5, 30.0])

    def test_sort_by_date_checks_year_first(self):
        dates = [e.date for e in self.tracker.sort_by("date")]
        self.assertEqual(dates, ["01/02/2025", "03/10/2026", "16/11/2026"])

    def test_same_result_as_python_sorted(self):
        expected = sorted(e.amount for e in self.tracker.expenses)
        amounts = [e.amount for e in self.tracker.sort_by("amount")]
        self.assertEqual(amounts, expected)

    def test_empty_list(self):
        self.assertEqual(ExpenseTracker().sort_by("date"), [])

    def test_bad_field(self):
        with self.assertRaises(ValueError):
            self.tracker.sort_by("colour")

class TestCategoryTotals(unittest.TestCase):
    """Tests for category totals (FR-15)."""

    def setUp(self):
        self.tracker = ExpenseTracker()
        self.tracker.add_expense("12.50", "16/11/2026", "Food", "Tesco")
        self.tracker.add_expense("30", "17/11/2026", "Food", "Aldi")
        self.tracker.add_expense("2", "16/11/2026", "Transport", "Bus")
        self.tracker.add_expense("100", "03/10/2026", "Bills", "Electric")

    def test_all_months(self):
        totals = self.tracker.totals_by_category()
        self.assertEqual(totals, {"Food": 42.5, "Transport": 2.0, "Bills": 100.0})

    def test_one_month(self):
        totals = self.tracker.totals_by_category("11/2026")
        self.assertEqual(totals, {"Food": 42.5, "Transport": 2.0})

    def test_month_with_no_expenses(self):
        self.assertEqual(self.tracker.totals_by_category("01/2026"), {})

    def test_totals_add_up_to_overall_total(self):
        totals = self.tracker.totals_by_category()
        self.assertEqual(round(sum(totals.values()), 2), self.tracker.total())


class TestBudget(unittest.TestCase):
    """Tests for budgets and budget status (FR-13, FR-14)."""

    def setUp(self):
        self.tracker = ExpenseTracker()
        self.tracker.set_budget("11/2026", "100")

    def test_set_budget_saved_in_dictionary(self):
        self.assertEqual(self.tracker.budgets, {"11/2026": 100.0})

    def test_month_without_leading_zero(self):
        self.tracker.set_budget("1/2026", "50")
        self.assertIn("01/2026", self.tracker.budgets)

    def test_bad_month(self):
        with self.assertRaises(ValueError):
            self.tracker.set_budget("13/2026", "100")

    def test_status_ok(self):
        self.tracker.add_expense("50", "16/11/2026", "Food")
        result = self.tracker.budget_status("11/2026")
        self.assertEqual(result["status"], "OK")
        self.assertEqual(result["left"], 50.0)

    def test_status_warning_at_80_percent(self):
        self.tracker.add_expense("80", "16/11/2026", "Food")
        self.assertEqual(self.tracker.budget_status("11/2026")["status"], "WARNING")

    def test_status_over(self):
        self.tracker.add_expense("120", "16/11/2026", "Rent")
        result = self.tracker.budget_status("11/2026")
        self.assertEqual(result["status"], "OVER")
        self.assertEqual(result["left"], -20.0)

    def test_other_months_not_counted(self):
        self.tracker.add_expense("500", "16/10/2026", "Rent")
        self.assertEqual(self.tracker.budget_status("11/2026")["spent"], 0)

    def test_no_budget_set(self):
        with self.assertRaises(ValueError):
            self.tracker.budget_status("12/2026")

class TestDateFix(unittest.TestCase):
    """Dates typed without zeros are stored with them (found while testing the GUI)."""

    def test_date_gets_leading_zeros(self):
        tracker = ExpenseTracker()
        expense = tracker.add_expense("120", "12/3/2009", "Bills")
        self.assertEqual(expense.date, "12/03/2009")

    def test_short_date_found_by_month_search(self):
        tracker = ExpenseTracker()
        tracker.add_expense("120", "12/3/2009", "Bills")
        self.assertEqual(len(tracker.search(month="03/2009")), 1)


if __name__ == "__main__":
    unittest.main()