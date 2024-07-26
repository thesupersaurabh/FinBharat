import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, inr
import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["inr"] = inr

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database configuration
DATABASE = 'finbharat.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    conn = get_db_connection()
    
    # Fetch transaction data
    transaction_db = conn.execute(
        "SELECT symbol, SUM(shares) AS shares, price FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
        (user_id,)
    ).fetchall()

    # Fetch cash data
    cash_db = conn.execute("SELECT cash FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()

    # Debug output
    print("Transaction DB:", transaction_db)
    print("Cash DB:", cash_db)

    if cash_db is None:
        # Handle error if cash_db is None
        flash("Error fetching cash balance.")
        return redirect("/")

    cash = cash_db["cash"]

    # Ensure cash is properly formatted and converted to INR
    cash = cash if cash is not None else 0
    cash_inr = inr(cash)  # Use the custom inr filter to format cash

    if not transaction_db:
        no_stocks_message = "You don't have any stocks in your portfolio."
        return render_template("index.html", no_stocks_message=no_stocks_message, cash=cash_inr)

    return render_template("index.html", database=transaction_db, cash=cash_inr)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol and shares are provided
        if not symbol:
            return apology("Must provide symbol")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Invalid number of shares")

        stock = lookup(symbol.upper())
        if stock is None:
            return apology("Symbol doesn't exist")

        shares = int(shares)
        transaction_value = shares * stock["price"]

        user_id = session["user_id"]
        conn = get_db_connection()
        user_cash_db = conn.execute("SELECT cash FROM users WHERE id = ?", (user_id,)).fetchone()
        user_cash = user_cash_db["cash"]

        if user_cash < transaction_value:
            conn.close()
            return apology("Not Enough Money")

        updt_cash = user_cash - transaction_value
        date = datetime.datetime.now()

        # Update the user's cash balance
        conn.execute("UPDATE users SET cash = ? WHERE id = ?", (updt_cash, user_id))

        # Record the transaction in the transactions table
        conn.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                     (user_id, stock["symbol"], shares, stock["price"], date))
        conn.commit()
        conn.close()

        flash("Bought!!")
        return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    conn = get_db_connection()
    transactions_db = conn.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    return render_template("history.html", transactions=transactions_db)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            return apology("Must provide username", 403)

        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            return apology("Must provide password", 403)

        # Query database for username
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()
        conn.close()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Must give symbol")

        stock = lookup(symbol.upper())
        if stock is None:
            return apology("Symbol doesn't exist")

        return render_template("quoted.html", name=stock["name"], price=stock["price"], symbol=stock["symbol"])

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Provide username")
        if not password:
            return apology("Provide password")
        if not confirmation:
            return apology("Provide confirmation")
        if password != confirmation:
            return apology("Passwords do not match")

        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            conn.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            conn.close()
            return apology("Username already exists")

        flash("Registered successfully! You can now log in.")
        return redirect("/login")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        conn = get_db_connection()
        symbols_user = conn.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
            (user_id,)
        ).fetchall()
        symbols = [row["symbol"] for row in symbols_user]
        conn.close()
        return render_template("sell.html", symbols=symbols)
    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Must give symbol")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Invalid number of shares")

        shares = int(shares)  # Convert shares to integer
        stock = lookup(symbol.upper())
        if stock is None:
            return apology("Symbol not found")

        user_id = session["user_id"]
        conn = get_db_connection()
        user_shares = conn.execute(
            "SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ?",
            (user_id, symbol)
        ).fetchone()["total_shares"]

        if user_shares < shares:
            conn.close()
            return apology("Not enough shares to sell")

        transaction_value = shares * stock["price"]
        user_cash = conn.execute("SELECT cash FROM users WHERE id = ?", (user_id,)).fetchone()["cash"]

        # Update user's cash balance and transactions
        updt_cash = user_cash + transaction_value
        date = datetime.datetime.now()

        conn.execute("UPDATE users SET cash = ? WHERE id = ?", (updt_cash, user_id))
        conn.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                     (user_id, symbol, -shares, stock["price"], date))
        conn.commit()
        conn.close()

        flash("Sold!!")
        return redirect("/")

@app.route("/about")
def about():
    return render_template("/about.html")
