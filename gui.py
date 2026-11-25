"""gui.py - The Tkinter window version of the Expense Tracker (FR-17).

It only shows things and reads boxes. All the rules live in tracker.py.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tracker import ExpenseTracker, CATEGORIES


class ExpenseApp:
    """The main window."""

    def __init__(self, root):
        """Build the window and its add-expense form."""
        self.tracker = ExpenseTracker()
        self.root = root
        self.root.title("Expense Tracker")

        form = ttk.LabelFrame(root, text="Add an expense", padding=10)
        form.pack(padx=10, pady=10, fill="x")

        ttk.Label(form, text="Amount (£)").grid(row=0, column=0, sticky="w")
        self.amount_box = ttk.Entry(form, width=15)
        self.amount_box.grid(row=0, column=1, pady=2)

        ttk.Label(form, text="Date (DD/MM/YYYY)").grid(row=1, column=0, sticky="w")
        self.date_box = ttk.Entry(form, width=15)
        self.date_box.grid(row=1, column=1, pady=2)

        ttk.Label(form, text="Category").grid(row=2, column=0, sticky="w")
        self.category_box = ttk.Combobox(form, values=CATEGORIES, state="readonly", width=12)
        self.category_box.grid(row=2, column=1, pady=2)

        ttk.Label(form, text="Note (optional)").grid(row=3, column=0, sticky="w")
        self.note_box = ttk.Entry(form, width=15)
        self.note_box.grid(row=3, column=1, pady=2)

        ttk.Button(form, text="Add", command=self.add_expense).grid(row=4, column=1, pady=5)

        self.message = ttk.Label(root, text="No expenses yet.")
        self.message.pack(pady=(0, 10))

    def add_expense(self):
        """Read the boxes, ask the tracker to add the expense, and show the result."""
        try:
            expense = self.tracker.add_expense(self.amount_box.get(), self.date_box.get(),
                                               self.category_box.get(), self.note_box.get())
        except ValueError as error:
            messagebox.showerror("Cannot add expense", str(error))
            return
        self.message.config(text=f"Added: {expense}   |   Total: £{self.tracker.total():.2f}")
        self.amount_box.delete(0, tk.END)
        self.note_box.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    ExpenseApp(root)
    root.mainloop()