
# Expense Tracker – Requirements
Each requirement has an ID, a priority and the test that proves it is met.
Priority uses MoSCoW: **M** = Must, **S** = Should, **C** = Could.
"Both" means the requirement applies to the text version and the GUI version
### Recording expenses
| ID | Requirement | Priority | How it will be tested |
|---|---|---|---|
| FR-01 | The user can input an expense with an amount, a date (DD/MM/YYYY), a category and an optional note. | M | Add `12.50`, `10/11/2026`, `Food`, `Lunch`. The expense appears in the list and the number of expenses goes up by 1. |
| FR-02 | The amount must be a number greater than 0. A `£` sign is allowed. Invalid amounts are rejected with a clear message. | M | `abc`, `0` and `-5` are rejected with a message. `£10.50` is accepted and stored as `10.50`. |
| FR-03 | The date must be a real date in the format DD/MM/YYYY. In the text version the user types the date; in the GUI the user can also pick it from a drop-down calendar (date picker). | M | `31/02/2026` and `2026-11-10` are rejected. `10/11/2026` is accepted. In the GUI, picking a day from the calendar fills in the date correctly. |
| FR-04 | The category must be one of: Food, Transport, Rent, Bills, Shopping, Other. More categories may be added if time allows. | M | A blank category and `Holiday` are rejected. `Bills` is accepted. |
| FR-05 | The system lists all expenses, newest first, showing date, category, amount (£, 2 decimal places) and note. | M | Add expenses dated 01/11/2026 and 20/11/2026. The 20/11/2026 expense is shown first. |
| FR-06 | The user can edit any field of an existing expense. Edited values are validated in the same way as new ones. | M | Change an amount from `10` to `20`: the list shows `£20.00`. Changing it to `abc` is rejected. |
| FR-07 | The user can delete an expense after confirming. Cancelling keeps it. | M | Delete and confirm: the expense is gone. Delete and cancel: it is still there. |
### Saving and loading

| ID | Requirement | Priority | How it will be tested |
|---|---|---|---|
| FR-08 | Every add, edit and delete is saved straight away to `expenses.csv`, and saved expenses are loaded when the program starts. | M | Add an expense, close the program, open it again: the expense is still there. |
| FR-09 | If `expenses.csv` does not exist, the program starts with an empty list and no error. | M | Delete `expenses.csv` and start the program: it opens normally with 0 expenses. |

### Finding and sorting

| ID | Requirement | Priority | How it will be tested |
|---|---|---|---|
| FR-10 | The user can filter expenses by month (MM/YYYY), by category, or by both together. | M | With expenses in October and November, filtering by `11/2026` and `Food` shows only November food expenses. |
| FR-11 | The user can search by a keyword in the note or the category. The search ignores upper and lower case. | S | Searching `tesco` finds an expense with the note `Tesco`. |
| FR-12 | The user can sort expenses by date or by amount, in ascending or descending order, using the program's own merge sort. | M | The merge sort result matches Python's `sorted()` for a normal list, an empty list, a one-item list and an already-sorted list. |
| FR-13 | The program finds all expenses in a given month using binary search on the date-sorted list. | M | For several months, binary search returns the same expenses as checking every expense one by one. |

### Totals and budgets

| ID | Requirement | Priority | How it will be tested |
|---|---|---|---|
| FR-14 | The system shows the total of the listed expenses, the total for a month, and the total for each category in a month. | M | With £10 and £5 Food and £100 Rent in 11/2026: month total `£115.00`; Rent `£100.00`; Food `£15.00`. |
| FR-15 | The user can set a budget plan for a month with an amount for each category. Empty boxes count as 0; at least one amount must be above 0; negative or non-numeric amounts are rejected. Plans are saved to `budgets.csv`. | M | Plan Rent `440`, Food `150`: the monthly budget is `£590.00` and is still there after a restart. `abc` and `-10` are rejected. |
| FR-16 | The user can plan next month's budget before that month starts. | S | On 10/11/2026, a plan can be saved for 12/2026. |
| FR-17 | The user can copy the most recent earlier plan into a new month's plan. | C | With a plan saved for 10/2026, copying into 12/2026 fills the same amounts. |
| FR-18 | The system shows the budget status for a month: **OK** below 80%, **WARNING** from 80% to 100%, **OVER** above 100%, and **NONE** when no plan exists. | M | Plan £100: spending £50 gives OK, £85 gives WARNING, £105 gives OVER. A month with no plan gives NONE. |
| FR-19 | The system lists any category where spending is above its planned amount. | S | Plan Food £20 and spend £30: Food is listed as over plan. |
| FR-20 | When the program starts, it reminds the user if the current month has no plan, or, from the 25th, if next month has no plan. | S | With no plan for this month, a reminder appears. With this month planned on the 10th, no reminder appears. On the 26th with next month unplanned, a reminder for next month appears. |

### Insights, export and undo

| ID | Requirement | Priority | How it will be tested |
|---|---|---|---|
| FR-21 | For a chosen month, the system reports: the biggest category and its share of spending, the percentage change from last month, categories that changed by 20% or more, and the average spend per day. | S | With £100 in October and £150 in November, the report says spending is 50% higher than last month. |
| FR-22 | The user can export the currently listed expenses to a CSV file they name. The file has a header row. | S | Export 3 filtered expenses: the file has 1 header row and 3 data rows and opens in Excel. |
| FR-23 | The user can undo the last add, edit or delete, and can undo several times in a row. If there is nothing to undo, a message says so. | S | Add, then undo: the expense is gone. Delete, then undo: it is back. Undo with no changes: "Nothing to undo". |
