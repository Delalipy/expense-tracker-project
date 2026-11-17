# playground.py - trying out a text menu that uses the Expense class

import csv
from datetime import datetime
from expense import Expense

CATEGORIES = ["Food", "Transport", "Rent", "Bills", "Shopping", "Other"]


def ask_amount():
    """Keep asking until the user types a number above 0."""
    while True:
        text = input("Amount (£): ").replace("£", "").strip()
        try:
            amount = float(text)
        except ValueError:
            print("That is not a number. Try again, e.g. 12.50")
            continue
        if amount <= 0:
            print("Amount must be more than 0.")
            continue
        return amount


def ask_date():
    """Keep asking until the user types a real date in DD/MM/YYYY."""
    while True:
        text = input("Date (DD/MM/YYYY): ").strip()
        try:
            datetime.strptime(text, "%d/%m/%Y")
            return text
        except ValueError:
            print("Not a real date. Use DD/MM/YYYY, e.g. 16/11/2026")


def ask_category():
    """Keep asking until the user types one of the categories (any capitals)."""
    print("Categories:", ", ".join(CATEGORIES))
    while True:
        text = input("Category: ").strip().capitalize()
        if text in CATEGORIES:
            return text
        print("Please choose one of the categories listed.")


def show_total(expenses):
    """Add up all the amounts and print the total."""
    total = 0
    for expense in expenses:
        total = total + expense.amount
    print(f"Total spent: £{total:.2f}")


def save_to_csv(expenses):
    """Try saving the expenses to a CSV file."""
    with open("playground_test.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["amount", "date", "category", "note"])
        for expense in expenses:
            writer.writerow(expense.to_list())
    print(f"Saved {len(expenses)} expenses to playground_test.csv")


expenses = []

while True:
    print("\n=== EXPENSE TRACKER (test) ===")
    print("1. Add an expense")
    print("2. List expenses")
    print("3. Show total")
    print("4. Save to CSV")
    print("0. Exit")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        amount = ask_amount()
        date = ask_date()
        category = ask_category()
        note = input("Note (optional): ")
        expenses.append(Expense(amount, date, category, note))
        print("Expense added.")
    elif choice == "2":
        if not expenses:
            print("No expenses yet.")
        for number, expense in enumerate(expenses, start=1):
            print(number, expense)
    elif choice == "3":
        show_total(expenses)
    elif choice == "4":
        save_to_csv(expenses)
    elif choice == "0":
        print("Goodbye!")
        break
    else:
        print("Please enter a number from the menu.")