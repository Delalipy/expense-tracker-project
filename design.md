# Expense Tracker – Design

This document explains how the Expense Tracker is built and why.
Requirement numbers (FR-01, NFR-01 …) refer to `requirements.md`.

## 1. What the app does

The app helps one person keep track of their spending. It has **six features**, and each one works in both the text version and the GUI version:

| # | Feature | Requirements |
|---|---|---|
| 1 | Add an expense (amount, date, category, note) | FR-01 to FR-04 |
| 2 | View all expenses, with the total | FR-05 |
| 3 | Edit or delete an expense | FR-06, FR-07 |
| 4 | Search and filter (by category, month or keyword) | FR-10, FR-11 |
| 5 | Sort by date or by amount | FR-12 |
| 6 | Monthly budget and summary (spent, left, totals per category) | FR-13 to FR-15 |

Expenses and budgets are saved in files, so nothing is lost when the program closes (FR-08, FR-09).

## 2. How the program is organised

The program is split into two parts:

- **The core** does the real work: it checks input, does the calculations and saves the data.
- **Two front ends** talk to the user: the text version and the GUI. They only ask questions and show results.

```
   Text version          GUI version
     (cli.py)              (gui.py)
         \                   /
          \                 /
           v               v
         ExpenseTracker (tracker.py)    <- checks, sorting, searching, budgets
              |               |
              v               v
         Expense           storage.py   <- saves and loads the CSV files
       (expense.py)
```

**Why I chose this design**

- Both versions use the same core, so they always have **the same features**, which the brief asks for (FR-16, FR-17).
- I only write each rule once. If I fix a bug in the core, it is fixed in both versions.
- The core has no `input()` or `print()`, so I can test it with unit tests (NFR-03).

**Files**

| File | What it does |
|---|---|
| `expense.py` | The `Expense` class: one expense |
| `storage.py` | Functions that save and load the CSV files |
| `tracker.py` | The `ExpenseTracker` class: all the rules and calculations |
| `cli.py` | The text version (menu). Run with `python cli.py` |
| `gui.py` | The GUI version (Tkinter). Run with `python gui.py` |
| `test_tracker.py` | Unit tests for the core |

## 3. Classes

There are two main classes.

**`Expense`**: stores one expense.

| Part | What it is |
|---|---|
| `amount` | The money spent, e.g. `12.5` |
| `date` | The date as text, DD/MM/YYYY, e.g. `"16/11/2026"` |
| `category` | One of: Food, Transport, Rent, Bills, Shopping, Other |
| `note` | Optional extra detail, e.g. `"Lunch"` |
| `to_list()` | Returns the expense as a list, ready to save as one row of the CSV file |

**`ExpenseTracker`**: holds all the expenses and does the work.

| Method | What it does |
|---|---|
| `add_expense(...)` | Checks the input, then adds a new expense and saves |
| `edit_expense(number, ...)` | Checks the input, then replaces an expense and saves |
| `delete_expense(number)` | Removes an expense and saves |
| `search(category, month, keyword)` | Returns the expenses that match |
| `sort_by(field)` | Returns the expenses sorted by date or amount (bubble sort) |
| `total(expenses)` | Adds up the amounts |
| `totals_by_category(month)` | Total spent in each category for a month |
| `set_budget(month, amount)` | Saves the budget for a month |
| `budget_status(month)` | Returns spent, left and OK / WARNING / OVER |

## 4. Data structures

| Data structure | What I use it for | Why it suits the problem |
|---|---|---|
| **List** | All the expenses, e.g. `[expense1, expense2, …]` | Keeps expenses in order. Each one has a position (index), which I use to edit or delete it. Easy to loop through and sort. |
| **Dictionary** | Budgets, e.g. `{"11/2026": 750.0}` | Each month has one budget, so the month is a natural key. Finding a month's budget is instant; no searching needed. |
| **Dictionary** | Totals per category, e.g. `{"Food": 45.0, "Rent": 440.0}` | One pass through the expenses adds each amount to its category. |

## 5. Algorithms

### 5.1 Bubble sort (FR-12)

Sorts the expenses by date or by amount. I wrote it myself instead of using Python's `sorted()`, to show how sorting works.

**The idea:** go through the list comparing each pair of neighbours. If they are in the wrong order, swap them. After each pass, the biggest item has "bubbled" to the end. Repeat until no swaps are needed.

**Example** (sorting amounts `[30, 10, 20]`):

```
Pass 1:  [30, 10, 20] -> swap 30 and 10 -> [10, 30, 20]
         [10, 30, 20] -> swap 30 and 20 -> [10, 20, 30]
Pass 2:  [10, 20, 30] -> no swaps -> finished
```

**Steps**

```
bubble_sort(items):
    repeat:
        swapped = False
        for each position i from 0 to the second-last item:
            if items[i] is bigger than items[i + 1]:
                swap them
                swapped = True
    until swapped is False
    return items
```

**Sorting dates:** dates like `"16/11/2026"` cannot be compared as text (`"02/01/2027"` would come before `"16/11/2026"`). So before comparing, each date is turned into `(year, month, day)`, e.g. `(2026, 11, 16)`, which compares correctly.

**Why bubble sort:** it is simple, easy to check by hand, and fast enough for a personal expense list (hundreds of items). Its weakness is that it gets slow with very large lists (it is O(n²)). In my evaluation I explain that a faster sort such as merge sort would be better for thousands of expenses.

### 5.2 Linear search (FR-11)

To search by keyword, the program checks each expense one by one and keeps the ones whose note or category contains the keyword. Upper and lower case are ignored, so `tesco` finds `Tesco`.

