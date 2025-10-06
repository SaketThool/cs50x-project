
import csv
import os
from pprint import pprint
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)
app.jinja_env.filters["usd"] = usd

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def load_data():
    with open("data/worldcups.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

@app.route("/")
@login_required
def index():
    # user_id = session["user_id"]
    cups = load_data()
    # pprint(cups)
    return render_template("index.html", cups=cups)

@app.route("/year/<int:year>")
def details(year):
    # pprint(year)
    cups = load_data()
    cup = next((c for c in cups if int(c["year"]) == year), None)
    return render_template("details.html", cup=cup)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol or not shares:
            return apology("must provide symbol and shares")

        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except:
            return apology("shares must be a positive integer")

        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)

        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        cost = quote["price"] * shares

        if cash < cost:
            return apology("can't afford")

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, user_id)

        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price, type)
            VALUES (?, ?, ?, ?, 'buy')
        """, user_id, quote["symbol"], shares, quote["price"])

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    transactions = db.execute("""
        SELECT symbol, shares, price, type, timestamp
        FROM transactions
        WHERE user_id = ?
        ORDER BY timestamp ASC
    """, user_id)
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("must provide username and password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")

        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol")

        return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("must fill out all fields")

        if password != confirmation:
            return apology("passwords do not match")

        hash_pw = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pw)
        except:
            return apology("username already exists")

        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
        session["user_id"] = user_id
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = session["user_id"]
    symbols = db.execute("""
        SELECT symbol FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING SUM(shares) > 0
    """, user_id)

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol or not shares:
            return apology("must provide symbol and shares")

        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except:
            return apology("shares must be a positive integer")

        owned = db.execute("""
            SELECT SUM(shares) as total_shares FROM transactions
            WHERE user_id = ? AND symbol = ?
        """, user_id, symbol)[0]["total_shares"]

        if owned is None or shares > owned:
            return apology("not enough shares")

        quote = lookup(symbol)
        proceeds = quote["price"] * shares

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", proceeds, user_id)
        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price, type)
            VALUES (?, ?, ?, ?, 'sell')
        """, user_id, symbol, -shares, quote["price"])

        return redirect("/")
    else:
        return render_template("sell.html", symbols=[row["symbol"] for row in symbols])


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current = request.form.get("current")
        new = request.form.get("new")
        confirm = request.form.get("confirm")

        if not current or not new or not confirm:
            return apology("All fields are required")

        if new != confirm:
            return apology("New passwords do not match")

        user_id = session["user_id"]
        user = db.execute("SELECT hash FROM users WHERE id = ?", user_id)[0]

        if not check_password_hash(user["hash"], current):
            return apology("Current password is incorrect")

        new_hash = generate_password_hash(new)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, user_id)

        flash("Password updated successfully!")
        return redirect("/")
    else:
        return render_template("change_password.html")
