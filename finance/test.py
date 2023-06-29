quotes = {}
users = {}
username = klau1
quotes = dict(lookup(request.form.get("symbol")))
shares_price = 9000
users = db.execute("SELECT username, cash FROM users")

for user in users:
    if users.username == username:
        #               if users[user]["cash"] < shares_price:
        return apology("Insufficient funds", 403)