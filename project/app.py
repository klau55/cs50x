import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date, timedelta
import time
from helpers import apology, login_required
import operator
import ast

# Configure application
app = Flask(__name__)



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index(): # THIS WILL BE MAIN PAGE

    # CHECK CURRENT TIME
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    minnow = datetime.now()
    users = db.execute("SELECT id, username FROM users")

    # GET USERNAME
    for user in users:
        if user["id"] == session["user_id"]:
            user_transfer = user["username"]

    # UPDATE THE TIME TO USER CHOSEN TIME
    if request.method == "POST":
        if request.args:
            now = datetime.strptime(request.args["date"], '%Y-%m-%d')
            date = now.strftime('%Y-%m-%d')

        # GET RESERVATION TIMES LIST
        db.execute("INSERT INTO reservations (username, datetime, forbidden) VALUES (?,?,?)", user_transfer, request.form.get("birthday"), request.form.get("timetable"))
        buffer = db.execute("SELECT DISTINCT forbidden FROM reservations WHERE datetime=?", request.form.get("birthday"))

        # MUTE UNAVAILABLE TIMES
        forbidden = []
        for i in buffer:
            forbidden.append(i["forbidden"])
        flash("Time reserved!")
        return render_template("index.html", date=now, forbidden=forbidden, mindate=minnow)

    else:
        if request.args:
            now = datetime.strptime(request.args["date"], '%Y-%m-%d')
            date = now.strftime('%Y-%m-%d')

        buffer = db.execute("SELECT DISTINCT forbidden FROM reservations WHERE datetime=?", date)
        forbidden = []
        for i in buffer:
            forbidden.append(i["forbidden"])

        return render_template("index.html", date=now, forbidden=forbidden, mindate=minnow)


#CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);
#CREATE TABLE sqlite_sequence(name,seq);
#CREATE TABLE reservations ( id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, datetime DATETIME NOT NULL, forbidden INTEGER NOT NULL);


@app.route("/myreservations",methods=["GET", "POST"])
@login_required
def myreservations():
    if request.method == "GET":

        # GET USERNAME
        users = db.execute("SELECT id, username FROM users")
        for user in users:
            if user["id"] == session["user_id"]:
                user_transfer = user["username"]

        # DELETE RESERVATIONS OLDER THAN TODAY
        PdateBuffer = datetime.today() - timedelta(days=1)
        PreviousDate = PdateBuffer.strftime('%Y-%m-%d')
        print("DDDDDD")
        print(PreviousDate)
        db.execute("DELETE FROM reservations WHERE datetime <= ?", PreviousDate)

        # GET ACTUAL RESERVATIONS FROM DATABASE AND SORT THEM
        reservations = db.execute("SELECT DISTINCT username,datetime,forbidden FROM reservations WHERE username=?", user_transfer)
        reservations.sort(key=operator.itemgetter('datetime'))


        return render_template("myreservations.html",reservations=reservations)

    if request.method == "POST":

        # DELETE THE RESERVATION IF CANCEL BUTTON GETS PRESSED
        i = request.form.get("cancel") # {'username': 'klau2', 'datetime': '2023-03-16', 'forbidden': 2}
        s = ast.literal_eval(i)
        db.execute("DELETE FROM reservations WHERE username=? AND datetime=? AND forbidden=?", s["username"], s["datetime"], s["forbidden"])

        # GET USERNAME
        users = db.execute("SELECT id, username FROM users")
        for user in users:
            if user["id"] == session["user_id"]:
                user_transfer = user["username"]

        # UPDATE RESERVATIONS TABLE
        reservations = db.execute("SELECT DISTINCT username,datetime,forbidden FROM reservations WHERE username=?", user_transfer)
        reservations.sort(key=operator.itemgetter('datetime'))

        flash("Reservation cancelled!")
        return render_template("myreservations.html",reservations=reservations)



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
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hashedPassword)

        # Remember which user has logged in
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")









