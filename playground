"""expense.py - The Expense class: holds the details of one expense."""


class Expense:
    """One expense: how much, when, what type, and an optional note."""

    def __init__(self, amount, date, category, note=""):
        """Create an expense.

        amount   -- a number, e.g. 12.5
        date     -- text in the format DD/MM/YYYY, e.g. "10/11/2026"
        category -- one of the six categories, e.g. "Food"
        note     -- optional extra detail, e.g. "Lunch"
        """
        self.amount = amount
        self.date = date
        self.category = category
        self.note = note

    def to_list(self):
        """Return the expense as a list, ready to save as one CSV row."""
        return [self.amount, self.date, self.category, self.note]

    def __str__(self):
        """Return a readable line, used when the expense is printed."""
        return f"{self.date} | {self.category} | £{self.amount:.2f} | {self.note}"