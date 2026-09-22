# Optional: automatic checks.   Run with:   python test_project.py
# It tries all the important conditions and prints PASS or FAIL.

import expense_logic as logic
from app import app

passed = 0
failed = 0


def check(name, condition):
    global passed, failed
    if condition:
        passed = passed + 1
        print("PASS ", name)
    else:
        failed = failed + 1
        print("FAIL ", name)


def reset(budget=10000.0):
    logic.expenses.clear()
    logic.settings["budget"] = budget


# ---------------- ZERO / ONE / MANY EXPENSES ----------------
reset()
d = logic.get_dashboard()
check("zero expenses: total is 0", d["total_text"] == "₹0")
check("zero expenses: count is 0", d["count"] == 0)
check("zero expenses: highest shows '-'", d["highest_text"] == "-" and d["lowest_text"] == "-")
check("zero expenses: no category rows", d["category_rows"] == [])
check("zero expenses: status is under control", d["status_message"] == "Budget is under control.")
check("zero expenses: sort works", logic.sort_expenses([], "low") == [])

logic.add_expense("Food", "80", "Lunch")
d = logic.get_dashboard()
check("one expense: highest = lowest", d["highest_text"] == d["lowest_text"] == "₹80 (Food)")
check("one expense: total 80", d["total_text"] == "₹80")
check("one expense: sort works", len(logic.sort_expenses(logic.expenses, "high")) == 1)

reset()
logic.add_expense("Food", "80", "Lunch")
logic.add_expense("Travel", "40", "Bus")
logic.add_expense("Stationery", "50", "Notebook")
logic.add_expense("Entertainment", "100", "Movie")
d = logic.get_dashboard()
check("sample: total 270", d["total_text"] == "₹270")
check("sample: remaining 9,730", d["remaining_text"] == "₹9,730")
check("sample: 4 transactions", d["count"] == 4)
check("sample: highest 100", d["highest_text"] == "₹100 (Entertainment)")
check("sample: lowest 40", d["lowest_text"] == "₹40 (Travel)")
check("sample: 4 category rows", len(d["category_rows"]) == 4)

# ---------------- SORTING ----------------
amounts_low = [e["amount"] for e in logic.sort_expenses(logic.expenses, "low")]
amounts_high = [e["amount"] for e in logic.sort_expenses(logic.expenses, "high")]
check("sort low to high", amounts_low == [40, 50, 80, 100])
check("sort high to low", amounts_high == [100, 80, 50, 40])
check("sort category A-Z", [e["category"] for e in logic.sort_expenses(logic.expenses, "category")]
      == ["Entertainment", "Food", "Stationery", "Travel"])
check("newest first", [e["id"] for e in logic.sort_expenses(logic.expenses, "newest")] == [4, 3, 2, 1])
check("oldest first", [e["id"] for e in logic.sort_expenses(logic.expenses, "oldest")] == [1, 2, 3, 4])
check("sorting does not change stored list", [e["id"] for e in logic.expenses] == [1, 2, 3, 4])

# ---------------- SAME AMOUNT / SAME CATEGORY ----------------
reset()
logic.add_expense("Food", "50", "A")
logic.add_expense("Food", "50", "B")
logic.add_expense("Travel", "50", "C")
d = logic.get_dashboard()
check("same amount: highest is first one", logic.find_highest(logic.expenses)["note"] == "A")
check("same amount: lowest is first one", logic.find_lowest(logic.expenses)["note"] == "A")
check("same amount: sort keeps order", [e["note"] for e in logic.sort_expenses(logic.expenses, "low")] == ["A", "B", "C"])
check("same category: added together", d["category_rows"][0]["name"] == "Food" and d["category_rows"][0]["total_text"] == "₹100")
check("same category: count is 2", d["category_rows"][0]["count"] == 2)
check("unique categories (set)", logic.get_unique_categories(logic.expenses) == {"Food", "Travel"})

# ---------------- SEARCH ----------------
reset()
logic.add_expense("Food", "80", "Lunch")
logic.add_expense("Travel", "40", "Bus ticket")
kind, msg, found = logic.search_expenses(logic.expenses, "food")
check("search category (any case)", kind == "ok" and len(found) == 1)
kind, msg, found = logic.search_expenses(logic.expenses, "TICKET")
check("search note (any case)", len(found) == 1 and found[0]["category"] == "Travel")
kind, msg, found = logic.search_expenses(logic.expenses, "80")
check("search amount", len(found) == 1)
kind, msg, found = logic.search_expenses(logic.expenses, "pizza")
check("search no result", kind == "error" and msg == "No matching expense." and found == [])
kind, msg, found = logic.search_expenses(logic.expenses, "   ")
check("search empty", kind == "error" and msg == "Please enter something to search." and len(found) == 2)
kind, msg, found = logic.search_expenses([], "food")
check("search with no expenses", kind == "error" and found == [])

# ---------------- VALIDATION ----------------
reset()
bad = [
    ("", "", "Empty expense. Please choose a category and enter an amount."),
    ("", "50", "Please select a category."),
    ("Food", "", "Please enter an amount."),
    ("Food", "   ", "Please enter an amount."),
    ("Food", "0", "Amount must be greater than zero."),
    ("Food", "0.00", "Amount must be greater than zero."),
    ("Food", "-20", "Amount cannot be negative."),
    ("Food", "abc", "Please enter a valid amount (example: 80 or 80.50)."),
    ("Food", "12abc", "Please enter a valid amount (example: 80 or 80.50)."),
    ("Food", "1.2.3", "Please enter a valid amount (example: 80 or 80.50)."),
    ("Food", ".", "Please enter a valid amount (example: 80 or 80.50)."),
    ("Food", "1e5", "Please enter a valid amount (example: 80 or 80.50)."),
    ("Food", "nan", "Please enter a valid amount (example: 80 or 80.50)."),
    ("Food", "²", "Please enter a valid amount (example: 80 or 80.50)."),
    ("Food", "9" * 400, "Amount is too large. Maximum is ₹1,00,00,000."),
    ("Pizza", "50", "Invalid category."),
]
for cat, amt, expected in bad:
    ok, msg = logic.add_expense(cat, amt, "")
    check("invalid input rejected: " + repr(cat) + " / " + repr(amt[:12]), ok == False and msg == expected)
check("nothing was stored for bad input", len(logic.expenses) == 0)

ok, msg = logic.add_expense("Food", "80.5", "")
check("decimal amount accepted", ok and logic.expenses[0]["amount"] == 80.5)
check("decimal shown with 2 places", logic.format_money(80.5) == "₹80.50")
ok, msg = logic.add_expense("  Travel  ", " 40 ", "x" * 100)
check("spaces are trimmed, long note cut", ok and logic.expenses[1]["amount"] == 40 and len(logic.expenses[1]["note"]) == 40)

# ---------------- DELETE ----------------
reset()
ok, msg = logic.delete_expense("1")
check("delete with no expenses", ok == False and msg == "No expenses to delete.")
logic.add_expense("Food", "80", "A")
logic.add_expense("Travel", "40", "B")
ok, msg = logic.delete_expense("1")
check("delete first", ok and len(logic.expenses) == 1 and logic.expenses[0]["note"] == "B")
ok, msg = logic.delete_expense("99")
check("delete unknown id", ok == False and msg == "Expense not found.")
ok, msg = logic.delete_expense("abc")
check("delete invalid id", ok == False and msg == "Invalid expense selected.")
ok, msg = logic.delete_expense("")
check("delete empty id", ok == False)
ok, msg = logic.delete_expense("2")
check("delete last expense", ok and len(logic.expenses) == 0)
d = logic.get_dashboard()
check("after deleting all: dashboard is empty but fine", d["count"] == 0 and d["total_text"] == "₹0")
logic.add_expense("Food", "10", "new")
check("new id after deleting all starts at 1", logic.expenses[0]["id"] == 1)
logic.add_expense("Food", "10", "new2")
logic.delete_expense("1")
logic.add_expense("Food", "10", "new3")
check("ids never repeat while others exist", logic.expenses[1]["id"] == 3)

# ---------------- BUDGET STATUS ----------------
def status(total, budget):
    return logic.get_budget_status(total, budget)[0]

check("0% -> under control", status(0, 10000) == "Budget is under control.")
check("69.9% -> under control", status(6990, 10000) == "Budget is under control.")
check("70% -> approaching", status(7000, 10000) == "⚠ You are approaching your budget.")
check("89% -> approaching", status(8900, 10000) == "⚠ You are approaching your budget.")
check("89.5% -> approaching", status(8950, 10000) == "⚠ You are approaching your budget.")
check("90% -> close to limit", status(9000, 10000) == "⚠ You are close to your budget limit.")
check("100% (equal) -> close to limit", status(10000, 10000) == "⚠ You are close to your budget limit.")
check("100.01% -> exceeded", status(10000.01, 10000) == "🚨 Budget exceeded!")
check("budget 0, no spending -> asks to set budget", "₹0" in status(0, 0))
check("budget 0, some spending -> exceeded", "exceeded" in status(50, 0))

reset(100)
logic.add_expense("Food", "100", "")
d = logic.get_dashboard()
check("spending equals budget: remaining is 0", d["remaining_text"] == "₹0" and d["remaining_label"] == "Remaining")
logic.add_expense("Food", "50", "")
d = logic.get_dashboard()
check("over budget: label + amount", d["remaining_label"] == "Over budget by" and d["remaining_text"] == "₹50")
check("over budget: bar stops at 100", d["bar_value"] == 100 and d["percent"] == 150)

reset(0)
d = logic.get_dashboard()
check("budget zero, no expenses: no crash", d["percent"] == 0)
logic.add_expense("Food", "10", "")
d = logic.get_dashboard()
check("budget zero, with expense: no crash", d["level"] == "danger")

# ---------------- SET BUDGET ----------------
reset()
check("set budget ok", logic.set_budget("5000")[0] and logic.settings["budget"] == 5000)
check("set budget to zero allowed", logic.set_budget("0")[0] and logic.settings["budget"] == 0)
check("set budget empty rejected", logic.set_budget("")[0] == False)
check("set budget negative rejected", logic.set_budget("-5") == (False, "Budget cannot be negative."))
check("set budget letters rejected", logic.set_budget("abc")[0] == False)
check("set budget huge rejected", logic.set_budget("9" * 400)[0] == False)
check("failed budget keeps old value", logic.settings["budget"] == 0)

# ---------------- REVERSE ----------------
check("reverse_list", logic.reverse_list([1, 2, 3]) == [3, 2, 1] and logic.reverse_list([]) == [])

# ---------------- MONEY FORMAT ----------------
check("format 10000", logic.format_money(10000) == "₹10,000")
check("format 0", logic.format_money(0) == "₹0")
check("format negative", logic.format_money(-500) == "-₹500")
check("float sums are rounded", logic.calculate_total([{"amount": 0.1}, {"amount": 0.2}]) == 0.3)

# ---------------- THE WEBSITE ----------------
reset()
client = app.test_client()

page = client.get("/")
html = page.data.decode("utf-8")
check("home page loads (empty)", page.status_code == 200 and "STUDENT EXPENSE TRACKER" in html)
check("empty page says no expenses", "No expenses found." in html and "No expenses yet." in html)

r = client.post("/add", data={"category": "Food", "amount": "80", "note": "Lunch"}, follow_redirects=True)
html = r.data.decode("utf-8")
check("add via website works", "Expense added: Food ₹80" in html and "Lunch" in html)
r = client.post("/add", data={"category": "Travel", "amount": "40", "note": "Bus"}, follow_redirects=True)
r = client.post("/add", data={"category": "Food", "amount": "abc", "note": ""}, follow_redirects=True)
html = r.data.decode("utf-8")
check("bad amount via website shows message", "Please enter a valid amount" in html and "message error" in html)
check("bad amount not stored", len(logic.expenses) == 2)
r = client.post("/add", data={}, follow_redirects=True)
check("empty POST does not crash", r.status_code == 200 and "Empty expense" in r.data.decode("utf-8"))

html = client.get("/?search=food&action=search").data.decode("utf-8")
check("search via website", "Found 1 matching expense(s)." in html and "Bus" not in html)
html = client.get("/?search=pizza&action=search").data.decode("utf-8")
check("search no result via website", "No matching expense." in html)
html = client.get("/?search=&action=search").data.decode("utf-8")
check("empty search via website", "Please enter something to search." in html and "Lunch" in html)
html = client.get("/?sort=high&action=sort").data.decode("utf-8")
check("sort via website", html.index("Lunch") < html.index("Bus"))
html = client.get("/?sort=hacker&action=sort").data.decode("utf-8")
check("unknown sort option does not crash", "Lunch" in html)
html = client.get("/?msg=<script>alert(1)</script>&kind=evil").data.decode("utf-8")
check("message is escaped, kind is cleaned", "<script>alert(1)" not in html and 'class="message ok"' in html)

r = client.post("/budget", data={"budget": "100"}, follow_redirects=True)
html = r.data.decode("utf-8")
check("set budget via website", "Monthly budget set to ₹100" in html and "Budget exceeded" in html)
r = client.post("/budget", data={"budget": "-1"}, follow_redirects=True)
check("bad budget via website", "Budget cannot be negative." in r.data.decode("utf-8"))

r = client.post("/delete", data={"expense_id": "1"}, follow_redirects=True)
check("delete via website", "Deleted: Food ₹80" in r.data.decode("utf-8") and len(logic.expenses) == 1)
r = client.post("/delete", data={"expense_id": "1"}, follow_redirects=True)
check("delete same id twice does not crash", "Expense not found." in r.data.decode("utf-8"))
r = client.post("/delete", data={"expense_id": "2"}, follow_redirects=True)
check("delete last expense via website", len(logic.expenses) == 0 and "No expenses found." in r.data.decode("utf-8"))
r = client.post("/delete", data={}, follow_redirects=True)
check("delete with nothing does not crash", r.status_code == 200)
check("unknown page is 404", client.get("/nothing").status_code == 404)

print()
print("Passed:", passed, "  Failed:", failed)
