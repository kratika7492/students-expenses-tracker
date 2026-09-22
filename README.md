# 💰 STUDENT EXPENSE TRACKER
**B.Tech 1st-year Python project · 2 members · Python + one HTML page**

| | Member 1 — PYTHON | Member 2 — HTML |
|---|---|---|
| Files | `expense_logic.py` | `templates/index.html` |
| Job | Every calculation, condition, loop, search, sort, validation | The website: header, navigation, dashboard, forms, tables |
| Extra (tiny) | `app.py` is the connector — under 80 lines, **no logic** (see section 7) | |

```
student_expense_tracker_lite/
├── expense_logic.py        ← PART 1 · MEMBER 1 · all Python
├── templates/
│   └── index.html          ← PART 2 · MEMBER 2 · the website
├── app.py                  ← connector (Flask), no project logic
└── test_project.py         ← optional: 108 automatic checks
```

---

## 1. Project overview

A student types daily expenses (Food ₹80, Travel ₹40 …). The website instantly shows total spending, highest and lowest expense, number of transactions, category-wise spending, remaining budget, a budget warning, and a history table with search, sort and delete.

**Everything is calculated by Python. Nothing is hard-coded.** The HTML page only displays the values Python sends.

## 2. Features

- Add expense (category, amount, optional note) with full validation
- Delete expense
- Total spent · highest · lowest · number of transactions
- Category-wise spending (with share %)
- Monthly budget (changeable), remaining amount, "over budget by" amount
- Budget status: under control / approaching / close to limit / exceeded
- Search by category, note or amount (not case sensitive)
- Sort: newest, oldest, amount low→high, amount high→low, category A→Z
- Friendly messages instead of crashes: "Please enter a valid amount.", "No matching expense.", "No expenses found."

Data is kept in a Python list while the program runs (no database). Stopping the server clears it — good for a clean demo.

## 3. How Python is used (Member 1)

| Need | Python concept | Function in `expense_logic.py` |
|---|---|---|
| Store all expenses | **List** of **dictionaries** | `expenses = []` |
| Fixed category names | **Tuple** | `CATEGORIES` |
| Unique categories | **Set** | `get_unique_categories()` |
| Budget setting | **Dictionary** | `settings` |
| Check amount is a number | **for loop**, **if/elif/else**, Boolean | `is_valid_number()`, `check_amount()` |
| Add / delete | Functions, list `append`, `del`, **linear search + break** | `add_expense()`, `delete_expense()` |
| Total | **Summation** | `calculate_total()` |
| Number of transactions | **Counting** | `count_transactions()` |
| Highest / lowest | **Maximum / Minimum** | `find_highest()`, `find_lowest()` |
| Category-wise spending | Nested loops + set + tuple | `get_category_totals()` |
| Search | **Searching** | `search_expenses()` |
| Sort | **Bubble sort**, **tuple assignment** (swap) | `sort_expenses()`, `should_swap()` |
| Newest first | **Reversing** with a **while loop** | `reverse_list()` |
| Budget warning | **if / elif / else** | `get_budget_status()` |

No `sorted()`, `max()`, `min()`, `sum()`, lambda, classes or list comprehensions are used, so every line can be explained.

## 4. How HTML is used (Member 2)

`index.html` is one page with these sections: **header**, **navigation** (jump links), **dashboard**, **category summary**, **add-expense form**, **search & sort**, **history table**.

- `<form>`, `<input>`, `<select>`, `<button>` collect what the user types.
- `<table>` shows categories and history.
- `<progress>` draws the budget bar.
- Three tiny template tools from Flask show Python's results:
  - `{{ d.total_text }}` → print a value from Python
  - `{% for e in expenses %} … {% endfor %}` → repeat for every expense (like Python's `for`)
  - `{% if message %} … {% endif %}` → show only if there is something to show (like Python's `if`)
- No JavaScript at all. The amount box is a *text* box on purpose, so wrong input (like `abc`) reaches Python and Python's validation is what you demonstrate.

## 5. Member 1 — complete Python code
→ file **`expense_logic.py`** (about 470 lines including comments; every function has a comment saying which syllabus topic it uses).
You can test it without the website: `python expense_logic.py`

## 6. Member 2 — complete HTML code
→ file **`templates/index.html`**. Small `<style>` block inside for colours and layout.

## 7. How to connect and run the two parts

`app.py` is the only "glue". It has no calculations. It does three things: **(1)** reads what the user typed, **(2)** calls a function from `expense_logic.py`, **(3)** sends the result to `index.html`.

```
User types in form ──► app.py ──► expense_logic.py (Python decides / calculates)
                                        │
User sees the page ◄── index.html ◄─────┘   (HTML just shows the results)
```

| Website action | Route in `app.py` | Python function called |
|---|---|---|
| Open page | `/` | `get_dashboard()`, `search_expenses()`, `sort_expenses()`, `prepare_rows()` |
| Add Expense button | `/add` | `add_expense()` |
| Delete button | `/delete` | `delete_expense()` |
| Set Budget button | `/budget` | `set_budget()` |

**Steps to run**

```bash
pip install flask
cd student_expense_tracker_lite
python app.py
```
Open **http://127.0.0.1:5000** in the browser. Press `Ctrl + C` in the terminal to stop.

Optional: `python test_project.py` runs 108 checks (expected last line: `Passed: 108   Failed: 0`).

## 8. Sample input

Set budget to `10000`, then add:

| Category | Amount | Note |
|---|---|---|
| Food | 80 | Lunch |
| Travel | 40 | Bus |
| Stationery | 50 | Notebook |
| Entertainment | 100 | Movie |

## 9. Expected output

```
Monthly Budget: ₹10,000

Total Spent: ₹270        Remaining: ₹9,730      Transactions: 4
Highest Expense: ₹100 (Entertainment)    Lowest Expense: ₹40 (Travel)

Budget is under control.        [▓░░░░░░░░░]  2.7% of the budget used

Category-wise spending          Food ₹80 · Travel ₹40 · Stationery ₹50 · Entertainment ₹100

History (newest first)          4 Entertainment ₹100 · 3 Stationery ₹50 · 2 Travel ₹40 · 1 Food ₹80
```

Now change the budget to `300` → 90% used → **"⚠ You are close to your budget limit."**
Change it to `200` → **"🚨 Budget exceeded!"** and the box changes to *Over budget by ₹70*.

## 10. Testing of important conditions

Try each row in the browser. The last column is what must happen.

| # | Condition | What to do | Expected result |
|---|---|---|---|
| 1 | Zero expenses | Open the page fresh | Total ₹0, Highest `-`, "No expenses found.", no crash |
| 2 | One expense | Add Food 80 | Highest and lowest are both ₹80 |
| 3 | Many expenses | Add 8–10 | Totals and table update correctly |
| 4 | Same amount | Add two expenses of ₹50 | Both shown; highest = the first ₹50 added; sort keeps their order |
| 5 | Same category | Add Food twice | Category summary shows one Food row with the combined total and 2 transactions |
| 6 | Empty form | Click Add with nothing filled | "Empty expense. Please choose a category and enter an amount." |
| 7 | Empty category | Amount 50, no category | "Please select a category." |
| 8 | Empty amount | Category only | "Please enter an amount." |
| 9 | Amount 0 | Type `0` | "Amount must be greater than zero." |
| 10 | Negative | Type `-20` | "Amount cannot be negative." |
| 11 | Invalid | Type `abc`, `12abc`, `1.2.3` | "Please enter a valid amount (example: 80 or 80.50)." |
| 12 | Decimal | Type `80.5` | Accepted, shown as ₹80.50 |
| 13 | Empty search | Click Search with empty box | "Please enter something to search." (all expenses still shown) |
| 14 | Search, no result | Search `pizza` | "No matching expense." |
| 15 | Search works | Search `food` (or `FOOD`) | Only Food expenses shown |
| 16 | Sort | Try all 5 options | Order changes correctly; stored data unchanged |
| 17 | Delete | Delete one row | Row disappears; totals update |
| 18 | Delete last expense | Delete until empty | Back to empty state, no crash |
| 19 | Spending = budget | Budget 270, spend 270 | "close to your budget limit", Remaining ₹0 (not "exceeded") |
| 20 | Spending > budget | Budget 200, spend 270 | "🚨 Budget exceeded!", Over budget by ₹70 |
| 21 | Budget = 0 | Set budget `0` | Message "Budget is ₹0…" (or "exceeded" if you have expenses); no division-by-zero crash |
| 22 | Bad budget | Set `-5` or `abc` | Error message; old budget kept |

Budget boundaries: below 70 % → under control · 70 %–89.9 % → approaching · 90 %–100 % → close to limit · above 100 % → exceeded.

## 11. Python syllabus concepts used

| Syllabus topic | Where |
|---|---|
| Variables, data types, expressions, statements | Everywhere — `total = total + e["amount"]`, `percent = total / budget * 100` |
| Tuple assignment | `ok, message, amount = check_amount(...)` · swap in sort: `a[j], a[j+1] = a[j+1], a[j]` |
| Operators (arithmetic, comparison, logical, `in`) | `+ - * /`, `> >= ==`, `and or not`, `cat in unique` |
| Functions, parameters, arguments, return | All ~20 functions |
| Boolean values | `is_valid_number()` returns True/False |
| if / if-else / if-elif-else | `check_amount()`, `get_budget_status()` |
| for loop | `calculate_total()`, `find_highest()`, `is_valid_number()` |
| while loop | `reverse_list()` |
| break | `delete_expense()` — stop when the id is found |
| continue | *Not needed in this project* — see viva question 20 |
| Lists | `expenses`, `found`, `result` |
| Tuples | `CATEGORIES`, function results such as `(True, "OK", amount)` |
| Sets | `get_unique_categories()` |
| Dictionaries | each expense, `settings`, the dashboard |
| Counting / Summation | `count_transactions()` / `calculate_total()` |
| Maximum / Minimum | `find_highest()` / `find_lowest()` |
| Searching | `search_expenses()`, position search in `delete_expense()` |
| Sorting | bubble sort in `sort_expenses()` |
| Reversing | `reverse_list()` |
| Removing duplicates | The set in `get_unique_categories()` removes repeated categories |

**A few small things beyond the syllabus — be ready to explain them:** `import`, `float()`/`int()`/`round()`, string methods `.strip()`, `.lower()`, string slicing `[:40]`, `format()` for commas in money (₹10,000), and the Flask connector.

## 12. Viva questions and answers

**A. Project**

1. **What does your project do?** It is a website where a student records daily expenses and sees total, highest, lowest, category-wise spending, remaining budget and a budget warning.
2. **Who did what?** Member 1 wrote all the Python in `expense_logic.py`. Member 2 wrote the HTML page. A small `app.py` connects them.
3. **Where is the real work done — Python or HTML?** Python. HTML only shows the values Python sends.
4. **Why is Flask used?** A browser cannot run our Python file directly. Flask is a thin connector that passes form data to our functions and sends the results to the HTML page. It has no project logic.
5. **Where is data stored?** In the list `expenses` while the program runs. There is no database, so it resets when the server stops.

**B. Data structures**

6. **Why a list of dictionaries?** A list keeps many expenses in order; a dictionary keeps the related details of one expense together (id, category, amount, note).
7. **Why is `CATEGORIES` a tuple?** The categories are fixed and must not change while the program runs; tuples cannot be changed.
8. **Where do you use a set and why?** `get_unique_categories()` — a set stores each category only once, so duplicates are removed automatically. We use it to decide which categories to show in the summary.
9. **Where do you use tuple assignment?** `ok, message, amount = check_amount(text)` and the swap `a[j], a[j+1] = a[j+1], a[j]` in bubble sort.
10. **Why do functions return tuples like `(True, "Expense added")`?** One function can then return both the result (worked or not) and the message to show.

**C. Algorithms**

11. **How do you find the highest expense?** Start with the first expense as "highest", loop through all, and replace it whenever a bigger amount is found. Lowest is the same with `<`.
12. **What if two expenses have the same amount?** We use `>` (not `>=`), so the first one found stays as the highest/lowest.
13. **How does total work?** Start `total = 0`, add each amount inside a for loop (summation).
14. **How do you count transactions?** A counter starts at 0 and increases by 1 for every expense.
15. **Explain your sorting.** Bubble sort: compare neighbours and swap if they are in the wrong order; repeat until sorted. `should_swap()` decides what "wrong order" means for each option.
16. **Does sorting change the stored list?** No. We first make a copy with `expense_list[:]` and sort the copy.
17. **How is "newest first" done?** `reverse_list()` builds a new list from the last item to the first using a while loop.
18. **How does search work?** Loop through all expenses; if the keyword (lower-case) is inside the category, note or amount text, add it to a `found` list.
19. **How does delete find the expense?** Linear search through the list for the matching id. When found, we remember the position, `break`, and `del` that position.
20. **Where do you use `break` and `continue`?** `break` is used in `delete_expense()`. `continue` is not needed here; if asked, we can show it would skip invalid items in a loop (for example skipping blank notes).

**D. Conditions and validation**

21. **How do you check the budget?** `get_budget_status()` uses if/elif/else: above budget → exceeded; ≥ 90 % → close to limit; ≥ 70 % → approaching; else under control.
22. **What if spending exactly equals the budget?** It is 100 %, not more than the budget, so the message is "close to your budget limit" and remaining is ₹0.
23. **What if the budget is zero?** Dividing by zero would crash the program, so we check `budget <= 0` first and show a message instead.
24. **How do you stop wrong amounts like `abc`, `-5`, `0`?** `is_valid_number()` checks every character; `check_amount()` then uses if statements to reject empty, invalid, zero and negative values with a message. The program never crashes.
25. **Why is the amount input a text box, not a number box?** So invalid input reaches Python and our own validation handles it.
26. **Why do you use `.strip()` and `.lower()`?** `.strip()` removes extra spaces; `.lower()` makes search ignore capital letters.

**E. Website**

27. **What do `{{ }}` and `{% %}` mean in the HTML?** `{{ }}` prints a value sent by Python; `{% %}` holds a simple `for` or `if` that works like Python's.
28. **How does the Delete button know which expense to delete?** Each row has a hidden input holding the expense id; the form sends it to Python.

## Presentation script (about 3 minutes)

**Member 1:** "Good morning. Our project is the **Student Expense Tracker** — a website that helps students record daily spending and stay within a budget. I handled all the **Python**. Expenses are stored as a **list of dictionaries**; categories are a **tuple**; unique categories use a **set**. Total is **summation**, transactions is **counting**, highest and lowest are **maximum and minimum** loops. Search is a loop over the list, sorting is **bubble sort**, and newest-first uses **reversing**. The budget message uses **if / elif / else**, and bad input like empty, zero, negative or letters is checked so the program never crashes."

**Member 2:** "I made the **HTML** page: header, navigation, dashboard, add-expense form, category table, search-and-sort box and history table. The page does no calculation — it only displays what Python sends. A small Flask file connects the form to Python's functions."

*(Live demo)* "Let's add Food ₹80, Travel ₹40, Stationery ₹50, Entertainment ₹100. Total ₹270, remaining ₹9,730, highest ₹100. Now a wrong amount — `abc` — the message appears, no crash. Let's search 'food', sort high to low, delete one entry — totals update. Finally I'll lower the budget to ₹200 — 'Budget exceeded!'"

**Both:** "Thank you. We are ready for your questions."
