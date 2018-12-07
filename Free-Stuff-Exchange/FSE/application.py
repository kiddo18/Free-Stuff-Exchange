import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from validate_email import validate_email
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from helpers import apology, login_required, lookup, usd

# Upload images in /inventory
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/Uploaded_images')
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

# Helper function
def nameInventory(inventory, items):
    for count,i in enumerate(inventory):
        for k in items:
            if i["itemTypeId"] == k["itemTypeId"]:
                inventory[count]['itemTypeId'] = k['itemTypeName']
    return inventory


@app.route("/")
@login_required
def index():
    # Inventory is a table that has all the user's items
    inventory = db.execute("SELECT itemId, ownerId, itemTypeId, itemName, itemDesc, itemImage FROM inventory WHERE ownerId = :user_id", user_id = session["user_id"])

    lookFor = db.execute("SELECT DISTINCT userId, itemLookFor, username FROM lookFor JOIN users ON lookFor.userId = users.id  WHERE userId = :user_id", user_id = session["user_id"])

    items = db.execute("SELECT * FROM Items")
    inventory = nameInventory(inventory,items)
    for count, i in enumerate(lookFor):
        for k in items:
            if i["itemLookFor"] == k["itemTypeId"]:
                lookFor[count]['itemLookFor'] = k['itemTypeName']
    return render_template("index.html", inventory=inventory,lookFor=lookFor)


@app.route("/listItem")
@login_required
def listItem():
    """This lists all the items currently registered"""
    # Get data from database
    #inventory = db.execute("SELECT * FROM inventory WHERE ownerId != :user_id", user_id = session["user_id"])
    inventory_all = db.execute("SELECT * FROM inventory JOIN users ON inventory.ownerId = users.id WHERE inventory.ownerId != :user_id", user_id = session["user_id"])
    username = db.execute("SELECT username from users")
    items = db.execute("SELECT * FROM Items")
    inventory_all = nameInventory(inventory_all,items)
    return render_template("listItem.html", inventory = inventory_all)


@app.route("/match")
@login_required
def match():

    # Get data from database
    lookFor = db.execute("SELECT DISTINCT userId, itemLookFor FROM lookFor")

    inventory_match = db.execute("SELECT DISTINCT ownerId, itemTypeId, itemName, itemImage, itemDesc FROM inventory INNER JOIN lookFor ON inventory.itemTypeId = lookFor.itemLookFor WHERE lookFor.userId == :user_id AND inventory.ownerID != :user_id", user_id = session["user_id"])
    items = db.execute("SELECT * FROM Items")
    owners = db.execute("SELECT username, id FROM users")
    for count,i in enumerate(inventory_match):
        for k in owners:
            if k["id"] == i["ownerId"]:
                inventory_match[count]["ownerId"] = k["username"]
    print("")
    print(inventory_match)
    print("")

    inventory_match = nameInventory(inventory_match,items)
    return render_template("match.html", inventory_match=inventory_match)


@app.route("/inventory", methods=["GET", "POST"])
@login_required
def inventory():
    """ Users input item to give away
    Content: Drop-down menu, itemName, itemDescription """
    if request.method == "POST":
        # Check if valid input
        try:
            itemTypeId = request.form.get("itemTypeId")
            itemName = request.form.get("itemName")
            itemDesc = request.form.get("itemDesc")
        except:
            return apology("Please choose an item type you want to input into inventory")


        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No image file selected')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return apology("No image file uploaded")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Insert into inventory table in sqlite
        inventory_insert = db.execute("INSERT INTO inventory (ownerId, itemTypeId, itemName, itemDesc, itemImage) VALUES (:userId, :itemTypeId, :itemName, :itemDesc, :itemImage)",
                                    userId=session["user_id"], itemTypeId=itemTypeId, itemName=itemName, itemDesc=itemDesc, itemImage=filename)


        # Return to index.html when successfully executed
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Display form & drop-down menu
        Items = db.execute("SELECT DISTINCT itemTypeName, itemTypeId FROM Items")
        return render_template("inventory.html", Items=Items)


# Helper function for image upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/lookFor", methods=["GET", "POST"])
@login_required
def lookFor():
    """Users input items into lookfor table
    Content: Dropdown menu + Submit button"""

    # We need a check condition that checks that the user hasnt already entered that item too look for already

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check if valid input

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
        return redirect("/match")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        print("")
        print("This went through GET")
        print("")
        # Display form
        Items = db.execute("SELECT DISTINCT itemTypeName, itemTypeId FROM Items")
        return render_template("lookFor.html", Items=Items)


@app.route("/deleteLookFor", methods=["POST"])
@login_required
def deleteLookFor():

    itemLookFor = request.form.get("itemLookFor")
    userId = request.form.get("userId")
    items = db.execute("SELECT * FROM Items")
    for i in items:
        if i["itemTypeName"] == itemLookFor:
            itemLookFor = i["itemTypeId"]
    # Get data from database
    # lookFor = db.execute("SELECT * FROM lookFor")
    deleteitem = db.execute("DELETE FROM lookFor WHERE itemLookFor = :itemLookFor", itemLookFor=itemLookFor )
    return redirect("/")


@app.route("/deleteInventory", methods=["POST"])
@login_required
def deleteInventory():
    itemId = request.form.get("itemId")

    # Get data from database
    # lookFor = db.execute("SELECT * FROM lookFor")
    deleteitem = db.execute("DELETE FROM inventory WHERE itemId = :itemId", itemId=itemId)
    return redirect("/")


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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        is_valid = validate_email(request.form.get("username"))
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide email", 400)

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
        elif not is_valid:
            return apology("must provide valid email", 400)
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


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)