"""storage.py - Saving and loading expenses and budgets as CSV files (FR-08, FR-09)."""

import csv
import os
from expense import Expense


def save_expenses(expenses, file_path="expenses.csv"):
    """Write every expense to the CSV file, one row each."""
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["amount", "date", "category", "note"])  # header row
        for expense in expenses:
            writer.writerow(expense.to_list())


def load_expenses(file_path="expenses.csv"):
    """Read the CSV file and return a list of Expense objects.

    No file yet (first run) gives an empty list. Broken rows are skipped.
    """
    expenses = []
    if not os.path.exists(file_path):
        return expenses
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # skip the header row
        for row in reader:
            try:
                expenses.append(Expense(float(row[0]), row[1], row[2], row[3]))
            except (ValueError, IndexError):
                continue  # broken row, skip it
    return expenses


def save_budgets(budgets, file_path="budgets.csv"):
    """Write the budgets dictionary to the CSV file."""
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["month", "amount"])
        for month in budgets:
            writer.writerow([month, budgets[month]])


def load_budgets(file_path="budgets.csv"):
    """Read the budgets CSV file and return a dictionary, e.g. {"11/2026": 750.0}."""
    budgets = {}
    if not os.path.exists(file_path):
        return budgets
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            try:
                budgets[row[0]] = float(row[1])
            except (ValueError, IndexError):
                continue
    return budgets