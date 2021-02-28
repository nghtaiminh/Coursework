from flask import *
import sqlite3
from flask.helpers import url_for
import os


app = Flask(__name__)
app.secret_key = 'dev_key'


@app.route('/')
def root():
    """
    Display home page and handles save email in session
    :return: None
    """
    loggedIn, firstName, nItems = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products')
        itemData = cur.fetchall()
        cur.execute('SELECT categoryId, name FROM categories')
        categoryData = cur.fetchall()
    itemData = parse(itemData, len(itemData))
    return render_template('home.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, nItems=nItems, categoryData=categoryData)


@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')


@app.route('/login_validation', methods=['POST', 'GET'])
def login_validation():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if validate(email, password):
            session['email'] = email
            return redirect(url_for('root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)


@app.route('/searchBar')
def searchBar():
    loggedIn, firstName, nItems = getLoginDetails()
    product_name = request.args.get('searchQuery')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT productID, name, price FROM products WHERE name LIKE '%{}%'".format(product_name))
        itemData = cur.fetchall()
    conn.close()
    itemData = parse(itemData, 3)
    return render_template('searchResult.html', keywords=product_name, itemData=itemData, loggedIn=loggedIn, firstName=firstName, nItems=nItems)


@app.route('/searching')
def searching():
    searchQuery = request.args.get('searchQuery')
    return redirect(url_for('searchBar', searchQuery=searchQuery))


@app.route("/productDescription")
def productDescription():
    loggedIn, firstName, nItems = getLoginDetails()
    productId = request.args.get('productId')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT productId, name, price, description, image, stock FROM products WHERE productId = '{}' ".format(productId))
        productData = cur.fetchone()
    conn.close()
    return render_template("productDescription.html", data=productData, loggedIn=loggedIn, firstName=firstName, nItems=nItems)


@app.route("/logout")
def logout():
    """
    Logs the user out by popping email from session
    """
    session.pop('email', None)
    return redirect(url_for('root'))


@app.errorhandler(404)
def page_not_found(e):
    app.logger.info(f"Page not found: {request.url}")
    return render_template("404.html"), 404


"""
NOT IMPLEMENT YET
@app.route("/displayCategory")
@app.route("/addToCart")
@app.route("/cart")
@app.route("/orders")
@app.route("/profile")
"""

# UTILITIES
def getLoginDetails():
    """
    Get personal info
    :return: is login, first name, number of items in cart
    """
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            isLogin = False
            firstName = ''
            nItems = 0
        else:
            isLogin = True
            cur.execute("SELECT userId, firstName FROM users WHERE email = '" + session['email'] + "'")
            userId, firstName = cur.fetchone()
            cur.execute("SELECT count(productId) FROM cart WHERE userId = " + str(userId))
            nItems = cur.fetchone()[0]
    conn.close()
    return (isLogin, firstName, nItems)


def parse(data, n_col):
    """
    Parse the fetched data from database array
    :param data: Result Set
    :param n_col: number of columns of the table
    :return: array contains each record
    """
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(n_col):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans


def validate(email, password):
    """
    :return: True if the credentials is matched with the database, False otherwise.
    """
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute(
        """SELECT * FROM users WHERE email='{}' AND password='{}';""".format(email, password))
    data = cur.fetchone()
    if data is None:
        return False
    return True


if __name__ == '__main__':
    app.run(debug=True)
