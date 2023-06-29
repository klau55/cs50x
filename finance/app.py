import os
#  API_KEY=pk_45d7fac34b354a0f8dabca395b1040d9
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    users = db.execute("SELECT id, username, cash FROM users")
    for user in users:
        if user["id"] == session["user_id"]:
            user_transfer = user["username"]
            id_transfer = user["id"]
            cash_transfer = user["cash"]

    # check if symbol amount is not 0
    db.execute("DELETE FROM stocks WHERE amount=?", 0)

    text = {}
    text = db.execute("SELECT * FROM stocks WHERE holder=?", user_transfer)

    quotes = {}
    calc = 0
    data_case = []
    for i in text:
        quotes = (lookup(i["symbol"]))
        quotes.update(i)
        data_case.append(quotes)

    for row in data_case:
        calc = calc + (row["price"] * row["amount"])

    return render_template("index.html", data_case=data_case, cash=cash_transfer, calc=calc)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide a valid symbol", 400)
        if lookup(request.form.get("symbol")) == None:
            return apology("must provide a real stock symbol", 400)
        if not request.form.get("shares"):
            return apology("must provide a real shares amount", 400)

        shares = request.form.get("shares")
        try:
            int(shares)
        except ValueError:
            return apology("must provide a real shares amount", 400)
        if int(shares) < 0:
            return apology("must provide a real shares amount", 400)

        quotes = {}
        users = {}
        shares_amount = float(request.form.get("shares"))
        username = session["user_id"]
        quotes = dict(lookup(request.form.get("symbol")))
        # {'name': 'Agilent Technologies Inc.', 'price': 143.11, 'symbol': 'A'}
        shares_price = quotes["price"] * shares_amount
        priceForOutput = float(quotes["price"])
        users = db.execute("SELECT id, username, cash FROM users")

        for user in users:
            if user["id"] == session["user_id"]:
                user_transfer = user["username"]
                id_transfer = user["id"]
                cash_transfer = user["cash"]
                if user["cash"] < shares_price:
                    return apology("Insufficient funds", 403)
        # INSERT SHARES INTO PORTFOLIO

         # HISTORY
        dt = datetime.now()
        db.execute("INSERT INTO history (symbol, amount, price, timestamp, username) VALUES (?,?,?,?,?)",
                   request.form.get("symbol"), request.form.get("shares"), quotes["price"], dt, user_transfer)

        # IF USER ALREADY HAS THIS SYMBOL
        if len(db.execute("SELECT * FROM stocks WHERE holder=? AND symbol=?", user_transfer, quotes['symbol'])) > 0:

            old_amount = {}
            old_amount = db.execute("SELECT amount FROM stocks WHERE holder=? AND symbol=?", user_transfer, quotes['symbol'])
            # [{'amount': 1}]

            new_amount = int(old_amount[0]['amount']) + int(shares_amount)

            db.execute("UPDATE stocks SET amount=? WHERE holder=? AND symbol=?", new_amount, user_transfer, quotes['symbol'])
            return redirect("/")
        else:
            # IF USER DIDNT HAVE THIS SYMBOL
            db.execute("INSERT INTO stocks(holder,symbol,amount) VALUES (?,?,?)", user_transfer, quotes['symbol'], shares_amount)
        # COUNT NEW USER BALANCE
        new_balance = float(cash_transfer) - shares_price
        db.execute("UPDATE users SET cash=? WHERE id=?", new_balance, id_transfer)
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    users = db.execute("SELECT id, username, cash FROM users")

    for user in users:
        if user["id"] == session["user_id"]:
            user_transfer = user["username"]

    data = db.execute("SELECT * FROM history WHERE username=?", user_transfer)

    return render_template("history.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide a stock symbol", 400)
        quotes = {}
        if lookup(request.form.get("symbol")) == None:
            return apology("must provide a real stock symbol", 400)
        quotes = dict(lookup(request.form.get("symbol")))

        return render_template("quoted.html", text=quotes)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure username is available
        request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 0:
            return apology("username already taken", 400)
        # Ensure passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Hash password and insert data into table
        hashedPassword = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        db.execute("INSERT INTO users (username, hash, cash) VALUES (?, ?, 10000.00)", request.form.get("username"), hashedPassword)

        # Remember which user has logged in
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    users = db.execute("SELECT id, username, cash FROM users")

    for user in users:
        if user["id"] == session["user_id"]:
            user_transfer = user["username"]

    ava_stocks = db.execute("SELECT symbol, amount FROM stocks WHERE holder=?", user_transfer)

    # [{'symbol': 'A', 'amount': 2}, {'symbol': 'AAPL', 'amount': 1}]
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        elif not request.form.get("shares"):
            return apology("must provide amount", 400)

        for amount in ava_stocks:
            if amount["symbol"] == request.form.get("symbol"):
                if amount["amount"] < int(request.form.get("shares")):
                    return apology("you dont have enough stocks", 400)
                elif amount["amount"] >= int(request.form.get("shares")):
                    new_stock_amount = amount["amount"] - int(request.form.get("shares"))
                    print(new_stock_amount)

        quotes = lookup(request.form.get("symbol"))
       # {'name': 'Agilent Technologies Inc.', 'price': 140.755, 'symbol': 'A'}

        # HISTORY
        dt = datetime.now()
        db.execute("INSERT INTO history (symbol, amount, price, timestamp, username) VALUES (?,?,?,?,?)",
                   request.form.get("symbol"), (int(request.form.get("shares")) * (-1)), quotes["price"], dt, user_transfer)

        money_back = quotes["price"] * int(request.form.get("shares"))
        db.execute("UPDATE stocks SET amount=? WHERE holder=? AND symbol=?",
                   new_stock_amount, user_transfer, request.form.get("symbol"))

        new_cash = db.execute("SELECT cash FROM users WHERE username=?", user_transfer)

        new_cash = new_cash[0]["cash"] + float(money_back)

        db.execute("UPDATE users SET cash=? WHERE username=?", new_cash, user_transfer)
        return redirect("/")
#        return render_template("sell.html", ava_stocks=ava_stocks, success="Success!")
    else:
        return render_template("sell.html", ava_stocks=ava_stocks)


@app.route("/favorites", methods=["GET", "POST"])
@login_required
def favotites():
    """Pick favorits stocks to follow"""
    users = db.execute("SELECT id, username, cash FROM users")

    for user in users:
        if user["id"] == session["user_id"]:
            user_transfer = user["username"]

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide a stock symbol", 403)
     #   quotes = {}
        if lookup(request.form.get("symbol")) == None:
            return apology("must provide a real stock symbol", 403)
        quotes = {}
        dict(lookup(request.form.get("symbol")))

        db.execute("INSERT INTO favorites (username, symbol) VALUES (?,?)", user_transfer, request.form.get("symbol"))
        favs = {}
        data_case = []
        favs = db.execute("SELECT DISTINCT symbol FROM favorites WHERE username=?", user_transfer)
        print(favs)
        for row in favs:
            quotes = lookup(row["symbol"])
            data_case.append(quotes)

        return render_template("favorites.html", quotes=data_case)

    else:
        favs = {}
        data_case = []
        favs = db.execute("SELECT DISTINCT symbol FROM favorites WHERE username=?", user_transfer)
        print(favs)
        for row in favs:
            quotes = lookup(row["symbol"])
            data_case.append(quotes)

        return render_template("favorites.html", quotes=data_case)


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    users = db.execute("SELECT id, username, cash FROM users")
    for user in users:

        if user["id"] == session["user_id"]:
            user_transfer = user["username"]
            db.execute("DELETE FROM favorites WHERE username=?", user_transfer)
            return render_template("favorites.html")

    return render_template("favorites.html")


def is_whole(n):
    return n % 1 == 0
# CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, cash NUMERIC NOT NULL DEFAULT 10000.00);
# CREATE TABLE sqlite_sequence(name,seq);
# CREATE UNIQUE INDEX username ON users (username);

# CREATE TABLE stocks (
# id INTEGER PRIMARY KEY,
# holder TEXT NOT NULL,
# symbol TEXT NOT NULL,
# amount INTEGER NOT NULL);

# CREATE TABLE history (
# id INTEGER PRIMARY KEY,
# symbol TEXT NOT NULL,
# amount INTEGER NOT NULL,
# price NUMERIC NOT NULL,
# timestamp TEXT NOT NULL,
# username TEXT NOT NULL);

# CREATE TABLE favorites (
# id INTEGER PRIMARY KEY,
# username TEXT NOT NULL,
# symbol TEXT NOT NULL);