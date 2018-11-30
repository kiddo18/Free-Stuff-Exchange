import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
def nameInventory(inventory, items):
    for count,i in enumerate(inventory):
        for k in items:
            if i["itemTypeId"] == k["itemTypeId"]:
                inventory[count]['itemTypeId'] = k['itemTypeName']
    return inventory
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config is a dicitonary that contains the directions for flask to follow necessary


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd
#so basically this makes it so that {% can do something | call filter here %} and this will basically execute the function as much as you need
#example below

# {% for x in mylist | reverse % }

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
#this line just
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    # Inventory object is a table that has all the user's items
    inventory = db.execute("SELECT ownerId, itemTypeId, itemName, itemDesc FROM inventory WHERE ownerId = :user_id", user_id = session["user_id"])

    lookFor = db.execute("SELECT DISTINCT itemLookFor FROM lookFor WHERE userId = :user_id", user_id = session["user_id"])

    items = db.execute("SELECT * FROM Items")
    print("")
    print(items)
    print("")
    for count,i in enumerate(inventory):
        for k in items:
            if i["itemTypeId"] == k["itemTypeId"]:
                inventory[count]['itemTypeId'] = k['itemTypeName']
    print("")
    print(inventory)
    print("")
    for count, i in enumerate(lookFor):
        for k in items:
            if i["itemLookFor"] == k["itemTypeId"]:
                lookFor[count]['itemLookFor'] = k['itemTypeName']
    return render_template("index.html", inventory=inventory,lookFor=lookFor)
    #for i in inventory:
        #itemType db.execute("SELECT itemTypeId FROM Items WHERE itemType", itemType = i["itemType"])
    # First database has

    # User id for item

    # We need to get inventory data from a database
    #inventory = db.execute("%%%% HAVING id = :user_id", user_id=session["user_id"])
    # We need to get lookfor data from the database
    #lookFor = db.execute("%%%% HAVING id = :user_id", user_id=session["user_id"])
    # Get data from database

    #This function is for users who want to give away items with no exchange
    #for k in lookFor:
        #look for and display another user who has the item you are looking for
    #    UsersGive = #Select the item that the user wants from
        #We need to display a name, image of the item

    # we need to get a match between the item type in the item database and a looking for user who has an item that we want.
    #pass the link to pages for UserWant and UserGive)
    # need to add a way for users to easily register an item Item.html


    '''
    stocks = db.execute("SELECT id, symbol, company_name, SUM(shares), price, total FROM history GROUP BY symbol HAVING id = :user_id",
                          user_id=session["user_id"])
    # Grand Total calculation
    grand_total = 0
    # Update real-time stock prices and total
    for i in stocks:
        stock_price = (lookup(i["symbol"]))["price"]
        stock_total = stock_price * i["SUM(shares)"]

        quote_price_update = db.execute("UPDATE history SET price = :price, total = :total WHERE symbol = :symbol",
                                        price=stock_price, total=stock_total, symbol=i["symbol"])
        grand_total += stock_total

    # Retrieve cash from users table
    #cash_users = db.execute("SELECT cash FROM users WHERE id = :user_id",
    #                      user_id=session["user_id"])
    return render_template("index.html", stocks = stocks, cash=cash_users[0]["cash"], grand_total=grand_total)
    '''
@app.route("/listItem")
@login_required
def listItem():
    """This lists all the items currently registered"""
    # Get data from database
    inventory = db.execute("SELECT * FROM inventory WHERE ownerId != :user_id", user_id = session["user_id"])
    items = db.execute("SELECT * FROM Items")
    inventory = nameInventory(inventory,items)
    return render_template("listItem.html", inventory = inventory)




@app.route("/match")
@login_required
def match():
    """This lists all the items currently registered"""
    
    # Get data from database
    lookFor = db.execute("SELECT * FROM lookFor")

    inventory = db.execute("SELECT * FROM inventory INNER JOIN lookFor ON inventory.itemTypeId = lookFor.itemLookFor HAVING ownerId != :user_id ", user_id = session["user_id"])
    items = db.execute("SELECT * FROM Items")
    
    
    inventory = nameInventory(inventory,items)
    return render_template("match.html", inventory = inventory)



@app.route("/item", methods=["GET", "POST"])
@login_required
def item():
    """We are posting an item to the data base through a form"""

    #a lot of this is checking that we have a valid item, a picture, and a description
    # ways to check valid
    # maybe we set a max number of items that each user can have

    #inventory = db.execute("Insert an ITEM Name, ITEM Type, ITEM OWNER ID, ITEM DESC, ITEM PIC id")

    # return redirect("/") once an item is added
    return redirect("/")

    # if the function is not valid return it to the /item page

@app.route("/registerItemToGive", methods=["GET", "POST"])
@login_required
def registerItemToGive():
    """ Users input item to give away 
    Content: Drop-down menu, itemName, itemDescription """
    if request.method == "POST":
        # Check if valid input
        try:
            itemTypeId = request.form.get("itemTypeId")
            
        except:
            return apology("Please choose an item type you are looking for")
        
        # INSERT INTO
        inventory_insert = db.execute("INSERT INTO inventory (ownerId, itemTypeId, itemName, itemDesc) VALUES (:userId, :itemTypeId, :itemName, :itemDesc)",
                                    userId=session["user_id"], itemTypeId=itemTypeId, itemName=itemName, itemDesc=itemDesc)

        # Return to index.html
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        print("")
        print("This did not work ")
        print("")
        # Display form
        Items = db.execute("SELECT DISTINCT itemTypeName, itemTypeId FROM Items")
        return render_template("lookFor.html", Items=Items)


@app.route("/lookFor", methods=["GET", "POST"])
@login_required
     """Users input items into lookfor table
    Content: Dropdown menu + Submit button"""
    # We need a check condition that checks that the user hasnt already entered that item too look for already
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check if valid input
        print("")
        print("This work wooo ")
        print

        try:
            itemTypeId = request.form.get("itemTypeId")
        except:
            return apology("Please choose an item type you are looking for")

        print("")
        print(itemTypeId)
        print("")

        # INSERT INTO
        lookFor_insert = db.execute("INSERT INTO lookFor (userId, itemLookFor) VALUES (:userId, :itemLookFor)",
                                    userId=session["user_id"], itemLookFor=itemTypeId)

        # Return to index.html
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        print("")
        print("This went through GET")
        print("")
        # Display form
        Items = db.execute("SELECT DISTINCT itemTypeName, itemTypeId FROM Items")
        return render_template("lookFor.html", Items=Items)


'''
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Store and make value of shares an integer
        shares = request.form.get("shares")

        # check if valid input
        try:
            quote = lookup(request.form.get("symbol"))
            shares = int(request.form.get("shares"))
        except:
            return apology("Please enter symbol and shares")

        # if quote is empty return apology
        if not quote:
            return apology("Please enter a valid symbol", 400)

        # if shares is empty
        if not shares or shares <= 0:
            return apology("enter the quantity of shares", 400)

        # Ensure number of shares is a positive integer
        #if (not int(shares)) or (int(shares) < 0) or isinstance(shares, float):
        #    return apology("Please enter a positive value for shares", 400)

        # Retrieve stock quote
        quote = lookup(request.form.get("symbol"))

        # Ensure stock symbol exists
        if not quote:
            return apology("Stock does not exist!", 400)
        else:
            price = quote["price"]
            # Retrieve remaining cash amount from db
            cash_users = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=session["user_id"])
            cash = cash_users[0]["cash"]

            # Ensure user has enough cash
            if cash < (price * int(shares)):
                return apology("Not enough cash", 400)
            else:
                # Update history & transaction tables
                history_insert = db.execute("INSERT INTO history (id, symbol, shares, price, company_name) VALUES (:id, :symbol, :shares, :price, :company_name)",
                                        id=session["user_id"], symbol = quote["symbol"], shares = shares, price = price, company_name=quote["name"])
                #transaction_insert = db.execute("INSERT INTO transaction (id, symbol, shares, price, name) VALUES (:id, :symbol, :shares, :price, :name)",
                #                        id=session["user_id"], symbol = quote["symbol"], shares = shares, price = price, name=quote["name"])

                # Update cash
                cash = cash - (price * int(shares))

                # Update cash in users table
                users_update = db.execute("UPDATE users SET cash = :cash WHERE id = :user_id",
                                        cash=cash, user_id=session["user_id"])
                # Retrieve remaining cash amount from users table
                #cash_users1 = db.execute("SELECT cash FROM users WHERE id = :user_id",
                #          user_id=session["user_id"])
                # Successful purchase

                return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Display form
        return render_template("buy.html")
'''



@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Get data from database
    stocks = db.execute("SELECT symbol, company_name, shares, price, timestamp FROM history WHERE id = :user_id",
                          user_id=session["user_id"])
    return render_template("history.html", stocks = stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # retrieve stock quote
        quote = lookup(request.form.get("symbol"))
        # Ensure stock symbol exists
        if not quote:
            return apology("Stock does not exist!", 400)
        else:
        # Display stock quote
            return render_template("quoted.html",
            company_name = quote["name"], price = quote["price"],
            symbol = quote["symbol"])

    # User reached route via GET (as by clicking a link or via redirect)
    elif request.method == "GET":
        # Display form
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

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

        # Ensure password_confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        # Ensure password has Require users' passwords to have some number of letters, numbers, and/or symbols.

        # Ensure password and password_confirmation match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("Password and password confirmation don't match!", 400)

        # Query database for username
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash_password)",
                          username=request.form.get("username"),
                          hash_password=generate_password_hash(request.form.get("password")))
        # Ensure username is unique
        if not result:
            return apology("Username already exists!", 400)

        # Remember which user has logged in (cookie)
        session["user_id"] = result

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Get data from database
    stocks = db.execute("SELECT id, symbol, company_name, SUM(shares), price, total FROM history GROUP BY symbol HAVING id = :user_id",
                              user_id=session["user_id"])
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Retrieve shares to sell
        stock_shares_sell = int(request.form.get("shares"))

        # Retrieve stock symbol
        stock_symbol = request.form.get("symbol")

        # Retrieve info of that stock
        stock = db.execute("SELECT id, symbol, company_name, SUM(shares), price, total FROM history GROUP BY symbol HAVING id = :user_id AND symbol = :symbol",
                        user_id=session["user_id"], symbol = stock_symbol)
        stock_price = stock[0]["price"]
        stock_shares_owned = stock[0]["SUM(shares)"]

        # Ensure number of shares is a positive integer
        if stock_shares_sell < 0 or stock_shares_sell > stock_shares_owned:
            return apology("Please enter a valid number of shares to sell!", 400)

        # Ensure stock symbol was chosen
        if not stock_symbol:
            return apology("Please choose a stock symbol!", 400)
        else:

            # Retrieve remaining cash amount from db
            cash_users = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=session["user_id"])
            cash = cash_users[0]["cash"]

            # Update history table
            history_insert = db.execute("INSERT INTO history (id, symbol, shares, price, company_name) VALUES (:id, :symbol, :shares, :price, :company_name)",
                                        id=session["user_id"], symbol = stock_symbol, shares = (-stock_shares_sell), price = stock_price, company_name=stock[0]["name"])
            #transaction_insert = db.execute("INSERT INTO transaction (id, symbol, shares, price, name) VALUES (:id, :symbol, :shares, :price, :name)",
            #                            id=session["user_id"], symbol = stock_symbol, shares = (-stock_shares_sell), price = stock_price, name=stock[0]["name"])

            # Delete stock's history
            #if stock_shares_sell == stock_shares_owned:
            #    history_delete = db.execute("DELETE FROM history WHERE symbol = :symbol", symbol=stock_symbol)

            # Update cash
            #cash = cash + (float(stock_price) * float(stock_shares_sell))

            # Update cash in users table
            users_update = db.execute("UPDATE users SET cash = :cash WHERE id = :user_id",
                                    cash=cash, user_id=session["user_id"])
            # Retrieve new cash amoung from users table
            cash_users = db.execute("SELECT cash FROM users WHERE id = :user_id",
                                    user_id=session["user_id"])
            # Successful purchase
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    elif request.method == "GET":
        # Display form
        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
