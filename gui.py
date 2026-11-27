"""gui.py - The Tkinter window version of the Expense Tracker (FR-17).

It only shows things and reads boxes. All the rules live in tracker.py.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tracker import ExpenseTracker, CATEGORIES
import storage


class ExpenseApp:
    """The main window."""

    def __init__(self, root):
        """Load saved data, then build the form, the table and the buttons."""
        self.tracker = ExpenseTracker()
        self.tracker.expenses = storage.load_expenses()
        self.tracker.budgets = storage.load_budgets()
        self.editing = None  # the number of the expense being edited, or None
        self.root = root
        self.root.title("Expense Tracker")

        # ---------- Form (top) ----------
        form = ttk.LabelFrame(root, text="Add or edit an expense", padding=10)
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

        self.add_button = ttk.Button(form, text="Add", command=self.submit_form)
        self.add_button.grid(row=4, column=1, pady=5)

        # ---------- Table (middle) ----------
        table_frame = ttk.LabelFrame(root, text="Your expenses", padding=10)
        table_frame.pack(padx=10, pady=(0, 10), fill="both", expand=True)

        columns = ("number", "date", "category", "amount", "note")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        for column, width in zip(columns, (60, 90, 90, 80, 160)):
            self.table.heading(column, text=column.capitalize())
            self.table.column(column, width=width)
        self.table.pack(fill="both", expand=True)

        buttons = ttk.Frame(table_frame)
        buttons.pack(pady=(5, 0))
        ttk.Button(buttons, text="Edit selected", command=self.start_edit).pack(side="left", padx=5)
        ttk.Button(buttons, text="Delete selected", command=self.delete_expense).pack(side="left", padx=5)

        # ---------- Message line (bottom) ----------
        self.message = ttk.Label(root, text="")
        self.message.pack(pady=(0, 10))

        self.refresh_table()

    # ---------- Helpers ----------

    def refresh_table(self):
        """Empty the table, then fill it again from the tracker's list."""
        for row in self.table.get_children():
            self.table.delete(row)
        for number, expense in enumerate(self.tracker.expenses, start=1):
            self.table.insert("", tk.END, iid=str(number),
                              values=(number, expense.date, expense.category,
                                      f"£{expense.amount:.2f}", expense.note))
        self.message.config(text=f"{len(self.tracker.expenses)} expenses   |   "
                                 f"Total: £{self.tracker.total():.2f}")

    def save(self):
        """Write the expenses and budgets to their CSV files."""
        storage.save_expenses(self.tracker.expenses)
        storage.save_budgets(self.tracker.budgets)

    def clear_form(self):
        """Empty the form and put the button back to Add."""
        self.amount_box.delete(0, tk.END)
        self.date_box.delete(0, tk.END)
        self.category_box.set("")
        self.note_box.delete(0, tk.END)
        self.editing = None
        self.add_button.config(text="Add")

    def selected_number(self):
        """Return the number of the row clicked in the table, or None."""
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("No expense selected", "Click an expense in the table first.")
            return None
        return int(selected[0])

    # ---------- Button actions ----------

    def submit_form(self):
        """Add a new expense, or save changes to the one being edited."""
        try:
            if self.editing is None:
                self.tracker.add_expense(self.amount_box.get(), self.date_box.get(),
                                         self.category_box.get(), self.note_box.get())
            else:
                self.tracker.edit_expense(self.editing, self.amount_box.get(), self.date_box.get(),
                                          self.category_box.get(), self.note_box.get())
        except ValueError as error:
            messagebox.showerror("Cannot save expense", str(error))
            return
        self.save()
        self.clear_form()
        self.refresh_table()

    def start_edit(self):
        """Copy the selected expense into the form so it can be changed."""
        number = self.selected_number()
        if number is None:
            return
        expense = self.tracker.expenses[number - 1]
        self.clear_form()
        self.amount_box.insert(0, f"{expense.amount:.2f}")
        self.date_box.insert(0, expense.date)
        self.category_box.set(expense.category)
        self.note_box.insert(0, expense.note)
        self.editing = number
        self.add_button.config(text="Save changes")

    def delete_expense(self):
        """Delete the selected expense after asking to confirm."""
        number = self.selected_number()
        if number is None:
            return
        if messagebox.askyesno("Delete expense", f"Delete expense number {number}?"):
            self.tracker.delete_expense(number)
            self.save()
            self.clear_form()
            self.refresh_table()


if __name__ == "__main__":
    root = tk.Tk()
    ExpenseApp(root)
    root.mainloop()