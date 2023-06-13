from flask import Flask, request, g, session, abort, make_response, json
import setup_db as set
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from re import match
import os

app = Flask(__name__)
app.secret_key = "soooo secret"
app.config.update(SESSION_COOKIE_SAMESITE='Strict')
class Config(object):
    # Since SQLAlchemy 1.4.x has removed support for the 'postgres://' URI scheme,
    # update the URI to the postgres database to use the supported 'postgresql://' scheme
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, 'instance', 'app.db')}"

def get_db():
    if not hasattr(g, "_database"):
        print("create connection")
        g._database = sqlite3.connect(DATABASE)
    return g._database


@app.teardown_appcontext
def teardown_db(error):
    """Closes the database at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        print("close connection")
        db.close()


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/products", methods=["GET"])
def get_products():
    db = get_db()
    return set.get_products(db)


@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    db = get_db()
    return set.get_product_by_id(db, id)


def createImagePath(extension):
    number = 1
    while True:
        imgpath = f'static/src/images/products/productimg{number}{extension}'
        if not os.path.isfile(imgpath):
            return imgpath
        number += 1


def checkAdmin():
    userid = session.get("userid")
    if userid:
        user = set.get_user_by_id(get_db(), userid)
        return user["role"] == "admin"
    return False


@app.route("/products", methods=["POST"])
def add_product():
    db = get_db()
    if not checkAdmin():
        return make_response({"message": "UNAUTHORIZED ACCESS"}, 401)
    name = request.form.get("name")
    price = request.form.get("price")
    if price:
        price = float(price)
    else:
        return make_response({"message": "Name cannot be empty and price must be positive"}, 400)
    if not name or price <= 0:
        return make_response({"message": "Name cannot be empty and price must be positive"}, 400)
    shortdesc = request.form.get("shortdesc")
    desc = request.form.get("desc")
    image = request.files.get('image')
    if not image:
        return make_response({"message": "No image selected"}, 400)
    extension = os.path.splitext(image.filename)[1].lower()
    if extension != ".jpg" and extension != ".png":
        return make_response({"message": "invalid file extension"}, 400)
    if request.content_length > 100000:
        return make_response({"message": "Image must be less than 100kb"}, 400)
    imgpath = createImagePath(extension)
    ok = set.insert_product(db, name, price, imgpath, shortdesc, desc)
    if ok != -1:
        image.save(imgpath)
        return make_response({"message": f"Added product {name}"}, 200)
    return make_response({"message": "sql error"}, 500)


@app.route("/products/<int:productid>", methods=["PUT"])
def edit_product(productid):
    db = get_db()
    if not checkAdmin():
        return make_response({"message": "UNAUTHORIZED ACCESS"}, 401)
    name = request.form.get("name")
    price = request.form.get("price")
    if price:
        price = float(price)
    else:
        return make_response({"message": "Name cannot be empty and price must be positive"}, 400)
    if not name or price <= 0:
        return make_response({"message": "Name cannot be empty and price must be positive"}, 400)
    shortdesc = request.form.get("shortdesc")
    desc = request.form.get("desc")
    imagepath = request.form.get("imagepath")
    image = request.files.get('image')
    if image:
        extension = os.path.splitext(image.filename)[1].lower()
        if extension != ".jpg" and extension != ".png":
            return make_response({"message": "invalid file extension"}, 400)
        if request.content_length > 100000:
            return make_response({"message": "Image must be less than 100kb"}, 400)
        ok = set.update_product(
            db, name, price, imagepath, shortdesc, desc, productid)
        if ok != -1:
            image.save(imagepath)
            return make_response({"message": "Succsesfully edited product"}, 200)
        return make_response({"message": "sql error"}, 500)
    ok = set.update_product(db, name, price, imagepath,
                            shortdesc, desc, productid)
    if ok != -1:
        return make_response({"message": "Succsesfully edited product"}, 200)
    return make_response({"message": "sql error"}, 500)


@app.route("/products/<int:productid>", methods=["DELETE"])
def delete_roduct(productid):
    db = get_db()
    if not checkAdmin():
        return make_response({"message": "UNAUTHORIZED ACCESS"}, 401)
    product = set.get_product_by_id(db, productid)
    ok = set.delete_product(db, productid)
    if ok != -1:
        try:
            os.remove(product["imgpath"])
        except FileNotFoundError:
            pass
        return make_response({"message": "Successfully deleted product"}, 200)
    return make_response({"message": "sql error"}, 500)


def valid_login(username, password):
    db = get_db()
    pwh = set.get_hash_for_login(db, username)
    if not pwh:
        return False
    if pwh:
        return check_password_hash(pwh, password)
    return False


@app.route("/check_login", methods=["GET"])
def check_login():
    userid = session.get("userid")
    if userid:
        return set.get_user_by_id(get_db(), userid)
    return make_response({"message": "Not logged in"}, 200)


@app.route("/login", methods=["POST"])
def login():
    user = request.get_json()
    if valid_login(user["username"], user["password"]):
        data = set.get_user_by_name(get_db(), user["username"])
        if data["userid"]:
            session["userid"] = data["userid"]
            return data
    return make_response({"message": "Invalid username or password"}, 401)


def checkPassword(password):
    regex = r"^(?=.*[A-Za-z])[A-Za-z0-9]{5,}$"
    return bool(match(regex, password))


def checkUsername(username):
    regex = r"^[a-zA-Z0-9]{3,10}$"
    return bool(match(regex, username))


@app.route("/signup", methods=["POST"])
def signup():
    db = get_db()
    user = request.get_json()
    if checkPassword(user["password"]) and checkUsername(user["username"]):
        pwh = generate_password_hash(user["password"])
        userid = set.add_user(db, user["username"], pwh)
        if userid != -1:
            if request.cookies.get("cart"):
                cart = json.loads(request.cookies.get("cart"))
                for item in cart:
                    set.insert_into_cart(
                        db, userid, item["productid"], item["quantity"])

            session["userid"] = userid
            response = make_response({
                "username": user["username"],
                "userid": userid
            })
            response.delete_cookie("cart")
            return response
        else:
            return make_response({"message": "Username is already taken"}, 409)
    elif not checkPassword(user["password"]):
        return make_response({"message": "Password must have at least 5 characters, one letter and only contain letters and numbers"}, 409)
    elif not checkUsername(user["username"]):
        return make_response({"message": "Username must be between 3-10 characters and only contain letters and numbers"}, 409)


@app.route("/logout", methods=["GET"])
def logout():
    userid = session.get("userid")
    if userid:
        session.pop("userid")
        return make_response({"message": "logged out user {}".format(userid)})
    return make_response({"message": "No user to log out"})


@app.route("/cart", methods=["GET"])
def get_cart():
    db = get_db()
    userid = session.get("userid")
    if userid:
        return set.get_cart_by_id(db, userid)
    if request.cookies.get("cart"):
        cart = json.loads(request.cookies.get("cart"))
        for item in cart:
            item["product"] = set.get_product_by_id(db, item["productid"])
        return cart
    else:
        return []


def find_index(arr, key, value):
    for index, item in enumerate(arr):
        if item.get(key) == value:
            return index
    return -1


@app.route("/cart/<int:productid>", methods=["PUT"])
def add_to_cart(productid):
    userid = session.get("userid")
    data = request.get_json()
    quantity = max(1, min(data["quantity"], 99))
    if userid:
        db = get_db()
        set.insert_into_cart(db, userid, productid, quantity)
        return make_response({"message": "Added item to user cart"}, 200)

    cartItem = {"productid": productid, "quantity": quantity}
    if not request.cookies.get("cart"):
        response = make_response("created cart")
        response.set_cookie("cart", json.dumps([cartItem]))
        return response
    cart = json.loads(request.cookies.get("cart"))
    index = find_index(cart, "productid", productid)
    if index == -1:
        cart.append(cartItem)
    else:
        cart[index] = cartItem
    response = make_response("Added item to cookie cart")
    response.set_cookie("cart", json.dumps(cart))
    return response


@app.route("/cart/<int:productid>", methods=["DELETE"])
def remove_from_cart(productid):
    userid = session.get("userid")
    if userid:
        set.remove_from_cart(get_db(), userid, productid)
        return make_response({"message": "Successfully removed item from cart"}, 200)
    cart = json.loads(request.cookies.get("cart"))
    if not cart:
        return make_response({"message": "Could not remove item from cart"}, 400)
    else:
        index = find_index(cart, "productid", productid)
        if index == -1:
            return make_response({"message": "Could not remove item from cart"}, 400)
        else:
            del cart[index]
            response = make_response("Removed item from cookie cart")
            response.set_cookie("cart", json.dumps(cart))
            return response


@app.route("/order", methods=["POST"])
def add_order():
    userid = session.get("userid")
    data = request.get_json()
    products = data.get("products")
    if not products:
        return make_response({"message": "No products ordered"}, 400)
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    email = data.get("email")
    street = data.get("street")
    city = data.get("city")
    postcode = data.get("postcode")
    if not (firstname and lastname and  email and  street and  city and postcode):
        return make_response({"message": "You must fill all the fields"}, 400)
    emailregex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not match(emailregex,email):
        return make_response({"message":"Invalid email format. Use the format: email@example.org"},400)
    if not match(r"^\d{4}$",str(postcode)):
        return make_response({"message":"Postal code must be four digits"},400)
    ok = set.insert_into_orders(
        get_db(), firstname, lastname, email, street, city, postcode, json.dumps(products))
    if ok != -1:
        response = make_response({"message": "Order confirmed"}, 200)
        if userid:
            set.remove_all_from_cart(get_db(), userid)
        else:
            response.delete_cookie("cart")
        return response
    return make_response({"message": "Order failed"}, 400)


if __name__ == "__main__":
    app.run()
