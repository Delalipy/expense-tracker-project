"""tracker.py - The ExpenseTracker class: all the rules and calculations.

This file has no input() or print(), so it can be tested on its own (NFR-03).
"""

from datetime import date, datetime
from expense import Expense

CATEGORIES = ["Food", "Transport", "Rent", "Bills", "Shopping", "Other"]
MAX_AMOUNT = 100000                  # largest amount allowed, to catch typing mistakes
EARLIEST_DATE = datetime(2000, 1, 1)  # dates before this are almost certainly typos


class ExpenseTracker:
    """Holds all the expenses and does the work."""

    def __init__(self):
        """Start with no expenses and no budgets."""
        self.expenses = []   # a list of Expense objects
        self.budgets = {}    # a dictionary, e.g. {"11/2026": 750.0}

    # Checking input (FR-02 to FR-04) 

    def check_amount(self, text):
        """Turn the text into an amount, or raise ValueError if it is not allowed."""
        text = str(text).replace("£", "").replace(",", "").strip()
        try:
            amount = float(text)
        except ValueError:
            raise ValueError("That is not a number. Try again, e.g. 12.50")
        if amount <= 0:
            raise ValueError("Amount must be more than 0.")
        if amount > MAX_AMOUNT:
            raise ValueError("Amount is too large. The maximum is £100,000.")
        return round(amount, 2)

    def check_date(self, text):
        """Check the date is real, in DD/MM/YYYY, and not before 01/01/2000."""
        text = text.strip()
        try:
            date = datetime.strptime(text, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Not a real date. Use DD/MM/YYYY, e.g. 16/11/2026")
        if date < EARLIEST_DATE:
            raise ValueError("Date must be on or after 01/01/2000.")
        return date.strftime("%d/%m/%Y")  # fixing date. turns 12/3/2009 into 12/03/2009

    def check_category(self, text):
        """Check the category is one of the six. Capitals do not matter."""
        category = text.strip().capitalize()
        if category not in CATEGORIES:
            raise ValueError("Please choose one of: " + ", ".join(CATEGORIES))
        return category

    def get_index(self, number):
        """Turn the number shown to the user (1, 2, 3...) into a list position (0, 1, 2...)."""
        try:
            number = int(number)
        except ValueError:
            raise ValueError("Please enter an expense number, e.g. 1")
        if number < 1 or number > len(self.expenses):
            raise ValueError(f"There is no expense number {number}.")
        return number - 1

    #  Add, edit, delete (FR-01, FR-06, FR-07) 

    def add_expense(self, amount, date, category, note=""):
        """Check the input, then add a new expense to the list."""
        amount = self.check_amount(amount)
        date = self.check_date(date)
        category = self.check_category(category)
        expense = Expense(amount, date, category, note.strip())
        self.expenses.append(expense)
        return expense

    def edit_expense(self, number, amount, date, category, note=""):
        """Check the new input, then replace the expense with that number."""
        index = self.get_index(number)
        amount = self.check_amount(amount)
        date = self.check_date(date)
        category = self.check_category(category)
        self.expenses[index] = Expense(amount, date, category, note.strip())
        return self.expenses[index]

    def delete_expense(self, number):
        """Remove the expense with that number and return it."""
        index = self.get_index(number)
        return self.expenses.pop(index)

    # Totals (FR-05) 

    def total(self, expenses=None):
        """Add up the amounts. With no list given, add up all the expenses."""
        if expenses is None:
            expenses = self.expenses
        total = 0
        for expense in expenses:
            total = total + expense.amount
        return round(total, 2)

            # ---------- Search and filter (FR-10, FR-11) ----------

    def search(self, category="", month="", keyword=""):
        """Return the expenses that match. Leave a box empty to ignore it.

        category -- e.g. "Food" (capitals do not matter)
        month    -- e.g. "11/2026"
        keyword  -- a word to find in the note or category, e.g. "tesco"
        """
        results = []
        for expense in self.expenses:
            if category and expense.category.lower() != category.strip().lower():
                continue  # wrong category, skip it
            if month and expense.date[3:] != month.strip():
                continue  # wrong month, skip it
            if keyword:
                word = keyword.strip().lower()
                if word not in expense.note.lower() and word not in expense.category.lower():
                    continue  # keyword not found, skip it
            results.append(expense)
        return results

    # ---------- Sorting (FR-12) ----------

    def sort_key(self, expense, field):
        """Return the value used to compare two expenses when sorting."""
        if field == "amount":
            return expense.amount
        day, month, year = expense.date.split("/")
        return (int(year), int(month), int(day))  # year first, so dates sort correctly

    def sort_by(self, field="date"):
        """Sort the expenses by "date" or "amount" using bubble sort (smallest first)."""
        if field not in ("date", "amount"):
            raise ValueError("You can only sort by date or amount.")
        items = self.expenses
        n = len(items)
        for i in range(n - 1):
            swapped = False
            for j in range(n - 1 - i):
                if self.sort_key(items[j], field) > self.sort_key(items[j + 1], field):
                    items[j], items[j + 1] = items[j + 1], items[j]  # swap the pair
                    swapped = True
            if not swapped:
                break  # nothing moved, so the list is already sorted
        return items

        # ---------- Category totals (FR-15) ----------

    def totals_by_category(self, month=""):
        """Add up the spending for each category. Give a month (MM/YYYY) to count only that month."""
        totals = {}  # a dictionary, e.g. {"Food": 42.5, "Transport": 2.0}
        for expense in self.search(month=month):
            if expense.category in totals:
                totals[expense.category] = totals[expense.category] + expense.amount
            else:
                totals[expense.category] = expense.amount
        for category in totals:
            totals[category] = round(totals[category], 2)
        return totals
    # ---------- Budget (FR-13, FR-14) ----------

    def check_month(self, text):
        """Check the month is real and in MM/YYYY, e.g. 11/2026."""
        try:
            month = datetime.strptime(text.strip(), "%m/%Y")
        except ValueError:
            raise ValueError("Not a real month. Use MM/YYYY, e.g. 11/2026")
        return month.strftime("%m/%Y")  # turns 1/2026 into 01/2026

    def set_budget(self, month, amount):
        """Save a spending limit for one month in the budgets dictionary."""
        month = self.check_month(month)
        self.budgets[month] = self.check_amount(amount)
        return self.budgets[month]

    def budget_status(self, month):
        """Compare the month's spending with its budget: OK, WARNING or OVER."""
        month = self.check_month(month)
        if month not in self.budgets:
            raise ValueError(f"No budget set for {month}.")
        budget = self.budgets[month]
        spent = self.total(self.search(month=month))
        percent = spent / budget * 100
        if percent > 100:
            status = "OVER"
        elif percent >= 80:
            status = "WARNING"
        else:
            status = "OK"
        return {"budget": budget, "spent": spent,
                "left": round(budget - spent, 2), "status": status}


    