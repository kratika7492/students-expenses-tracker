# ============================================================
#  STUDENT EXPENSE TRACKER  -  CONNECTOR (tiny file)
#  File: app.py
#
#  This file has NO project logic.
#  Its only job: take what the user typed in the HTML page,
#  hand it to expense_logic.py (Member 1), and send the results
#  back to index.html (Member 2).
#
#  Run:   python app.py      then open   http://127.0.0.1:5000
# ============================================================

from flask import Flask, render_template, request, redirect, url_for
import expense_logic as logic

app = Flask(__name__)


# ---------- Main page (dashboard + search + sort + history) ----------
@app.route("/")
def home():
    keyword = request.args.get("search", "")       # text in the search box
    sort_by = request.args.get("sort", "newest")   # chosen sort option
    action = request.args.get("action", "")        # which button was pressed
    message = request.args.get("msg", "")          # message after add/delete/budget
    kind = request.args.get("kind", "ok")          # "ok" or "error"

    if kind != "ok" and kind != "error":
        kind = "ok"

    rows = logic.expenses                          # by default show all expenses

    # search (Python does the searching)
    if keyword.strip() != "" or action == "search":
        kind, message, rows = logic.search_expenses(logic.expenses, keyword)

    # sort (Python does the sorting)
    rows = logic.sort_expenses(rows, sort_by)

    return render_template(
        "index.html",
        d=logic.get_dashboard(),                   # all dashboard numbers
        expenses=logic.prepare_rows(rows),         # rows for the history table
        categories=logic.CATEGORIES,               # options of the category list
        message=message,
        kind=kind,
        keyword=keyword,
        sort_by=sort_by,
    )


# ---------- Add expense ----------
@app.route("/add", methods=["POST"])
def add():
    ok, message = logic.add_expense(
        request.form.get("category", ""),
        request.form.get("amount", ""),
        request.form.get("note", ""),
    )
    return redirect(url_for("home", msg=message, kind="ok" if ok else "error"))


# ---------- Delete expense ----------
@app.route("/delete", methods=["POST"])
def delete():
    ok, message = logic.delete_expense(request.form.get("expense_id", ""))
    return redirect(url_for("home", msg=message, kind="ok" if ok else "error"))

# ---------- Change budget ----------
@app.route("/budget", methods=["POST"])
def budget():
    ok, message = logic.set_budget(request.form.get("budget", ""))
    return redirect(url_for("home", msg=message, kind="ok" if ok else "error"))


if __name__ == "__main__":
    app.run(debug=True)
