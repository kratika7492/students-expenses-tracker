# ============================================================
#  STUDENT EXPENSE TRACKER  -  MEMBER 1 : PYTHON
#  File: expense_logic.py
#
#  ALL the logic of the project is in this file.
#  Only plain Python is used: variables, functions, if/elif/else,
#  for/while loops, break, lists, tuples, sets, dictionaries,
#  counting, sum, max, min, searching, sorting, reversing.
# ============================================================


# ------------------------------------------------------------
#  1. DATA  (where everything is stored)
# ------------------------------------------------------------

# TUPLE  -> the categories never change, so a tuple is perfect
CATEGORIES = ("Food", "Travel", "Stationery", "Entertainment", "Other")

MAX_AMOUNT = 10000000          # biggest amount we accept (1 crore)

# LIST of DICTIONARIES -> every expense is one dictionary
# Example: {"id": 1, "category": "Food", "amount": 80.0, "note": "Lunch"}
expenses = []

# DICTIONARY -> settings of the program
settings = {"budget": 10000.0}


# ------------------------------------------------------------
#  2. SMALL HELPER FUNCTIONS
# ------------------------------------------------------------

def is_valid_number(text):
    """Return True if text looks like 80 or 80.5 (only digits and at most one dot)."""
    if text == "":
        return False

    dots = 0
    digits = 0
    for ch in text:                       # check every character
        if ch == ".":
            dots = dots + 1
        elif ch in "0123456789":
            digits = digits + 1
        else:
            return False                  # letter, space, symbol ... not a number

    if dots > 1 or digits == 0:           # "1.2.3" or "." are not numbers
        return False
    return True


def amount_to_text(amount):
    """80.0 -> '80'   and   80.5 -> '80.5'"""
    if amount == int(amount):
        return str(int(amount))
    return str(amount)


def format_money(amount):
    """80.0 -> '₹80', 10000 -> '₹10,000', 80.5 -> '₹80.50', -500 -> '-₹500'"""
    sign = ""
    if amount < 0:
        sign = "-"
        amount = -amount
    if amount == int(amount):
        return sign + "₹" + format(int(amount), ",")
    return sign + "₹" + format(amount, ",.2f")


def check_amount(amount_text):
    """
    Validate an amount typed by the user.
    Returns a TUPLE: (ok, message, amount)
    """
    amount_text = amount_text.strip()

    if amount_text == "":
        return (False, "Please enter an amount.", 0)

    if amount_text[0] == "-":                          # starts with minus sign
        if is_valid_number(amount_text[1:]):
            return (False, "Amount cannot be negative.", 0)
        return (False, "Please enter a valid amount (example: 80 or 80.50).", 0)

    if not is_valid_number(amount_text):
        return (False, "Please enter a valid amount (example: 80 or 80.50).", 0)

    amount = round(float(amount_text), 2)              # keep 2 decimal places

    if amount <= 0:
        return (False, "Amount must be greater than zero.", 0)
    if amount > MAX_AMOUNT:
        return (False, "Amount is too large. Maximum is ₹1,00,00,000.", 0)

    return (True, "OK", amount)


def get_new_id(expense_list):
    """New id = (biggest id in the list) + 1.  For an empty list the id is 1."""
    biggest = 0
    for e in expense_list:
        if e["id"] > biggest:
            biggest = e["id"]
    return biggest + 1


# ------------------------------------------------------------
#  3. ADD AND DELETE
# ------------------------------------------------------------

def add_expense(category, amount_text, note):
    """
    Validate the input and add a new expense.
    Returns a TUPLE: (ok, message)
    """
    category = category.strip()
    amount_text = amount_text.strip()
    note = note.strip()[:40]                            # keep note short (40 letters)

    # ---- validation with if / elif ----
    if category == "" and amount_text == "":
        return (False, "Empty expense. Please choose a category and enter an amount.")
    if category == "":
        return (False, "Please select a category.")
    if category not in CATEGORIES:
        return (False, "Invalid category.")

    ok, message, amount = check_amount(amount_text)     # TUPLE ASSIGNMENT
    if ok == False:
        return (False, message)

    # ---- everything is fine: build the dictionary and store it ----
    new_expense = {
        "id": get_new_id(expenses),
        "category": category,
        "amount": amount,
        "note": note,
    }
    expenses.append(new_expense)
    return (True, "Expense added: " + category + " " + format_money(amount))


def delete_expense(expense_id_text):
    """
    Delete the expense with the given id.
    Returns a TUPLE: (ok, message)
    """
    text = expense_id_text.strip()

    if len(expenses) == 0:
        return (False, "No expenses to delete.")
    if not is_valid_number(text) or "." in text or len(text) > 9:
        return (False, "Invalid expense selected.")

    expense_id = int(text)

    # ---- linear SEARCH for the position of this id ----
    position = -1
    for i in range(len(expenses)):
        if expenses[i]["id"] == expense_id:
            position = i
            break                                        # found it, stop the loop

    if position == -1:
        return (False, "Expense not found.")

    removed = expenses[position]
    del expenses[position]                               # remove from the list
    return (True, "Deleted: " + removed["category"] + " " + format_money(removed["amount"]))


# ------------------------------------------------------------
#  4. CALCULATIONS  (summation, counting, maximum, minimum)
# ------------------------------------------------------------

def calculate_total(expense_list):
    """SUMMATION"""
    total = 0
    for e in expense_list:
        total = total + e["amount"]
    return round(total, 2)


def count_transactions(expense_list):
    """COUNTING"""
    count = 0
    for e in expense_list:
        count = count + 1
    return count


def find_highest(expense_list):
    """MAXIMUM - returns the expense with the biggest amount (or None if list is empty)."""
    if len(expense_list) == 0:
        return None
    highest = expense_list[0]
    for e in expense_list:
        if e["amount"] > highest["amount"]:              # '>' keeps the first one if amounts are equal
            highest = e
    return highest


def find_lowest(expense_list):
    """MINIMUM - returns the expense with the smallest amount (or None if list is empty)."""
    if len(expense_list) == 0:
        return None
    lowest = expense_list[0]
    for e in expense_list:
        if e["amount"] < lowest["amount"]:
            lowest = e
    return lowest


def get_unique_categories(expense_list):
    """SET - removes duplicate categories automatically."""
    unique = set()
    for e in expense_list:
        unique.add(e["category"])
    return unique


def get_category_totals(expense_list):
    """
    Category-wise spending.
    Returns a list of TUPLES: (category, total, number_of_expenses)
    Only categories that really have expenses are included.
    """
    unique = get_unique_categories(expense_list)
    result = []
    for cat in CATEGORIES:                               # fixed order from the tuple
        if cat in unique:
            total = 0
            count = 0
            for e in expense_list:
                if e["category"] == cat:
                    total = total + e["amount"]
                    count = count + 1
            result.append((cat, round(total, 2), count))
    return result


# ------------------------------------------------------------
#  5. SEARCH, REVERSE AND SORT
# ------------------------------------------------------------

def search_expenses(expense_list, keyword):
    """
    SEARCH by category, note or amount (not case sensitive).
    Returns a TUPLE: (kind, message, matching_list)
    kind is "ok" or "error" (used for the colour of the message).
    """
    keyword = keyword.strip().lower()

    if keyword == "":
        return ("error", "Please enter something to search.", expense_list)
    if len(expense_list) == 0:
        return ("error", "No expenses found. Add an expense first.", [])

    found = []
    for e in expense_list:
        if (keyword in e["category"].lower()
                or keyword in e["note"].lower()
                or keyword in amount_to_text(e["amount"])):
            found.append(e)

    if len(found) == 0:
        return ("error", "No matching expense.", [])
    return ("ok", "Found " + str(len(found)) + " matching expense(s).", found)


def reverse_list(items):
    """REVERSING a list using a while loop."""
    reversed_items = []
    i = len(items) - 1
    while i >= 0:
        reversed_items.append(items[i])
        i = i - 1
    return reversed_items


def should_swap(a, b, sort_by):
    """Bubble sort helper: True if expense a must come AFTER expense b."""
    if sort_by == "low":                                 # small amount first
        return a["amount"] > b["amount"]
    if sort_by == "high":                                # big amount first
        return a["amount"] < b["amount"]
    if sort_by == "category":                            # A to Z
        return a["category"] > b["category"]
    return False


def sort_expenses(expense_list, sort_by):
    """
    SORTING. Returns a NEW list; the stored list is not changed.
      "newest"   -> newest first (reverse of the stored order)  [default]
      "oldest"   -> oldest first (stored order)
      "low"      -> amount low to high   (bubble sort)
      "high"     -> amount high to low   (bubble sort)
      "category" -> category A to Z      (bubble sort)
    """
    result = expense_list[:]                             # make a copy

    if sort_by == "oldest":
        return result

    if sort_by in ("low", "high", "category"):
        n = len(result)
        for i in range(n - 1):                           # BUBBLE SORT
            for j in range(n - 1 - i):
                if should_swap(result[j], result[j + 1], sort_by):
                    result[j], result[j + 1] = result[j + 1], result[j]   # TUPLE ASSIGNMENT (swap)
        return result

    return reverse_list(result)                          # "newest" (default)


# ------------------------------------------------------------
#  6. BUDGET
# ------------------------------------------------------------

def set_budget(budget_text):
    """Change the monthly budget. Returns a TUPLE: (ok, message). Budget 0 is allowed."""
    text = budget_text.strip()

    if text == "":
        return (False, "Please enter a budget amount.")
    if text[0] == "-":
        return (False, "Budget cannot be negative.")
    if not is_valid_number(text):
        return (False, "Please enter a valid budget (example: 10000).")

    amount = round(float(text), 2)
    if amount > MAX_AMOUNT:
        return (False, "Budget is too large. Maximum is ₹1,00,00,000.")

    settings["budget"] = amount
    return (True, "Monthly budget set to " + format_money(amount))


def get_budget_status(total, budget):
    """
    BUDGET WARNING using if / elif / else.
    Returns a TUPLE: (message, level, percent_used)
    level is "good", "warn" or "danger" (used for the colour on the page).
    """
    # Budget is zero -> we must not divide by zero
    if budget <= 0:
        if total > 0:
            return ("🚨 Budget exceeded! Your budget is ₹0.", "danger", 0)
        return ("Budget is ₹0. Please set a budget above zero.", "warn", 0)

    percent = total / budget * 100

    if total > budget:
        message = "🚨 Budget exceeded!"
        level = "danger"
    elif percent >= 90:                                  # 90% to 100%
        message = "⚠ You are close to your budget limit."
        level = "warn"
    elif percent >= 70:                                  # 70% to 89%
        message = "⚠ You are approaching your budget."
        level = "warn"
    else:                                                # below 70%
        message = "Budget is under control."
        level = "good"

    return (message, level, round(percent, 1))


# ------------------------------------------------------------
#  7. READY-MADE DATA FOR THE WEBSITE
#     (the HTML page only has to show these values)
# ------------------------------------------------------------

def prepare_rows(expense_list):
    """Turn expenses into rows that are ready to show in an HTML table."""
    rows = []
    for e in expense_list:
        note = e["note"]
        if note == "":
            note = "-"
        row = {
            "id": e["id"],
            "category": e["category"],
            "note": note,
            "amount_text": format_money(e["amount"]),
        }
        rows.append(row)
    return rows


def get_dashboard():
    """Calculate everything shown on the dashboard and return it as ONE dictionary."""
    budget = settings["budget"]
    total = calculate_total(expenses)
    count = count_transactions(expenses)
    highest = find_highest(expenses)
    lowest = find_lowest(expenses)
    remaining = round(budget - total, 2)
    message, level, percent = get_budget_status(total, budget)

    # ---- highest / lowest text ----
    if highest == None:
        highest_text = "-"
        lowest_text = "-"
    else:
        highest_text = format_money(highest["amount"]) + " (" + highest["category"] + ")"
        lowest_text = format_money(lowest["amount"]) + " (" + lowest["category"] + ")"

    # ---- remaining or over budget ----
    if remaining >= 0:
        remaining_label = "Remaining"
        remaining_text = format_money(remaining)
    else:
        remaining_label = "Over budget by"
        remaining_text = format_money(-remaining)

    # ---- progress bar can not go above 100 ----
    bar_value = percent
    if bar_value > 100:
        bar_value = 100

    # ---- category rows ----
    category_rows = []
    for cat, cat_total, cat_count in get_category_totals(expenses):   # TUPLE unpacking
        share = round(cat_total / total * 100)                       # total > 0 here
        category_rows.append({
            "name": cat,
            "total_text": format_money(cat_total),
            "count": cat_count,
            "share": share,
        })

    dashboard = {
        "budget_text": format_money(budget),
        "budget_input": amount_to_text(budget),
        "total_text": format_money(total),
        "remaining_label": remaining_label,
        "remaining_text": remaining_text,
        "count": count,
        "highest_text": highest_text,
        "lowest_text": lowest_text,
        "status_message": message,
        "level": level,
        "percent": percent,
        "bar_value": bar_value,
        "category_rows": category_rows,
    }
    return dashboard


# ------------------------------------------------------------
#  Run this file directly to try the logic WITHOUT the website:
#      python expense_logic.py
# ------------------------------------------------------------
if __name__ == "__main__":
    print(add_expense("Food", "80", "Lunch"))
    print(add_expense("Travel", "40", "Bus"))
    print(add_expense("Stationery", "50", "Notebook"))
    print(add_expense("Entertainment", "100", "Movie"))
    print(add_expense("Food", "abc", ""))
    print("Total   :", format_money(calculate_total(expenses)))
    print("Highest :", find_highest(expenses))
    print("Lowest  :", find_lowest(expenses))
    print("Sorted  :", [e["amount"] for e in sort_expenses(expenses, "high")])
    print("Status  :", get_budget_status(calculate_total(expenses), settings["budget"]))
