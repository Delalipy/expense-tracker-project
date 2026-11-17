# Expense Tracker – Requirements

Each requirement has an ID, a priority and the test that proves it is met.
Priority uses MoSCoW: **M** = Must, **S** = Should, **C** = Could.
Every functional requirement applies to both the text version and the GUI version.

## Functional requirements

### Recording expenses

| ID | Requirement | Priority | How it will be tested |
|---|---|---|---|
| FR-01 | The user can add an expense with an amount, a date (DD/MM/YYYY), a category and an optional note. | M | Add `12.50`, `16/11/2026`, `Food`, `Lunch`. The expense appears in the list and the number of expenses goes up by 1. |
| FR-02 | The amount must be a number above 0 and up to £100,000. `£` and commas are allowed. It is rounded to 2 decimal places. | M | `abc`, `0`, `-5` and `999999` are rejected. `£12.50` is stored as `12.5`; `12.345` as `12.35`; `1,250` as `1250`. |
| FR-03 | The date must be a real date in the format DD/MM/YYYY, from 01/01/2000. | M | `31/02/2026`, `22/22/22` and `01/01/1999` are rejected. `16/11/2026` is accepted. |
| FR-04 | The category must be one of: Food, Transport, Rent, Bills, Shopping, Other. Capitals do not matter. | M | `Holiday` and a blank category are rejected. `food` is accepted and saved as `Food`. |
| FR-05 | The user can view all expenses with date, category, amount (£, 2 decimal places) and note, and the total. | M | With £12.50 and £2.00 saved, both are listed and the total shows `£14.50`. |
| FR-06 | The user can edit an existing expense. New values are checked the same way as in FR-02 to FR-04. | M | Change an amount from `10` to `20`: the list shows `£20.00`. Changing it to `abc` is rejected. |
| FR-07 | The user can delete an expense after confirming. | M | Delete and confirm: the expense is gone. Delete and say no: it is still there. |

### Saving and loading

| ID | Requirement | Priority | How it will be tested |
|---|---|---|---|
| FR-08 | Every add, edit and delete is saved straight away to `expenses.csv`, and saved expenses are loaded when the program starts. | M | Add an expense, close the program and open it again: the expense is still there. |
| FR-09 | If `expenses.csv` does not exist, the program starts with an empty list and no error. | M | Delete `expenses.csv` and start the program: it opens normally with 0 expenses. |

### Searching and sorting

| ID | Requirement | Priority | How it will be tested |
|---|---|---|---|
| FR-10 | The user can filter expenses by category, by month (MM/YYYY), or both. | M | With expenses in October and November, filtering by `Food` and `11/2026` shows only November food expenses. |
| FR-11 | The user can search by a keyword in the note or category. Capitals do not matter. | S | Searching `tesco` finds an expense with the note `Tesco`. |
| FR-12 | The user can sort expenses by date or by amount, using the program's own bubble sort. | M | The bubble sort result matches Python's `sorted()` for a normal list, an empty list, a one-item list and an already-sorted list. |

### Budget and summary

| ID | Requirement | Priority | How it will be tested |
|---|---|---|---|
| FR-13 | The user can set a budget for a month. It must be a number above 0. Budgets are saved to `budgets.csv`. | M | Set £750 for `11/2026`: it is still there after a restart. `abc` and `-10` are rejected. |
| FR-14 | For a chosen month, the system shows the amount spent, the amount left, and the status: **OK** below 80%, **WARNING** from 80% to 100%, **OVER** above 100%. | M | Budget £100: spending £50 shows OK, £85 shows WARNING, £105 shows OVER. |
| FR-15 | For a chosen month, the system shows the total spent in each category. | S | With £10 and £5 Food and £100 Rent in 11/2026: Food `£15.00`, Rent `£100.00`. |

### Two versions

| ID | Requirement | Priority | How it will be tested |
|---|---|---|---|
| FR-16 | The text version provides FR-01 to FR-15 through a numbered menu. A wrong menu choice asks again. | M | Each feature is run from the menu. Typing `9` or `x` at the menu asks again without crashing. |
| FR-17 | The GUI version provides FR-01 to FR-15 in a Tkinter window. | M | Each feature is run in the GUI. A table in the report shows every feature working in both versions. |

## Non-functional requirements

| ID | Requirement | Priority | How it will be tested |
|---|---|---|---|
| NFR-01 | **Usability:** error messages say what is wrong and how to fix it. | S | Check every error message against the list in `design.md`. |
| NFR-02 | **Reliability:** the program never crashes on wrong input. | M | Enter every wrong input from FR-02 to FR-04 and FR-13, plus wrong menu choices: the program keeps running. |
| NFR-03 | **Maintainability:** all the rules are in the core (`tracker.py`, `storage.py`), with no `input()` or `print()` there. Every class and function has a docstring. | M | Search the core files for `input(` and `print(`; check each function has a docstring. |
| NFR-04 | **Portability:** the program needs only Python 3 and its standard library (including Tkinter). | M | Run it from a fresh download on Windows with no extra installs. |
| NFR-05 | **Testability:** every functional requirement has at least one automated or manual test, listed by ID in the test table. | M | Check that every FR number appears in the test table. |
| NFR-06 | **Data integrity:** a broken row in a CSV file is skipped instead of crashing the program. | S | Add an incomplete row to `expenses.csv` by hand and start the program: it loads the other rows. |
