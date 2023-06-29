import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")
rows = db.execute("SELECT * FROM birthdays")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        name = request.form.get("name")
        if len(name) < 1:
            return render_template("index.html", birthdays=rows, p3="Wrong name format")

        try:
            month = request.form.get("month")
            month = int(month)
        except ValueError:
            return render_template("index.html", birthdays=rows, p3="Wrong month format")

        try:
            day = request.form.get("day")
            day = int(day)
        except ValueError:
            return render_template("index.html", birthdays=rows, p3="Wrong day format")

        if month > 12 or month < 0:
            return render_template("index.html", birthdays=rows, p3="Wrong month format")
        if day > 31 or day < 0:
            return render_template("index.html", birthdays=rows, p3="Wrong day format")
        db.execute("INSERT INTO birthdays(name, month, day) VALUES(?,?,?)", name, month, day)
            # TODO: Add the user's entry into the database
        rows = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=rows, p3="Success!")

    else:
        # rows = db.execute("SELECT * FROM birthdays")

        # TODO: Display the entries in the database on index.html


        rows = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=rows)


