
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