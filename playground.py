# playground.py - trying out a text menu that uses the Expense class

from expense import Expense


def show_total(expenses):
    """Add up all the amounts and print the total."""
    total = 0
    for expense in expenses:
        total = total + expense.amount
    print(f"Total spent: £{total:.2f}")


expenses = []

while True:
    print("\n=== EXPENSE TRACKER (test) ===")
    print("1. Add an expense")
    print("2. List expenses")
    print("3. Show total")
    print("0. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        try:
            amount = float(input("Amount (£): "))
        except ValueError:
            print("That is not a number.")
            continue
        date = input("Date (DD/MM/YYYY): ")
        category = input("Category: ")
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
    elif choice == "0":
        print("Goodbye!")
        break
    else:
        print("Please enter a number from the menu.")