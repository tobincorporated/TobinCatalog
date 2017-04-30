from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Product, User
from flask import session as login_session
import random
import string

# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Product Catalog Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///productcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id
    login_session['access_token'] = credentials.access_token

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id']=user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getCategoryFromProduct(product_id):
    product = session.query(Product).filter_by(id=product_id).one()
    category = session.query(Category).filter_by(id=product.category_id).one()
    return category.name


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None



@app.route('/disconnect')
def disconnect():
    if 'username' not in login_session:
        return redirect('/login')
    access_token = login_session['access_token']
    print '-------------------------------------------'
    print 'In disconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ( 'https://accounts.google.com/o/oauth2/revoke?token=%s' %
            login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is %s' % result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
    	del login_session['picture']
    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'
        return render_template('logout.html')
    else:
    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response


# JSON APIs to view Category Information
@app.route('/category/<int:category_id>/product/JSON')
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    products = session.query(Product).filter_by(
        category_id=category_id).all()
    return jsonify(Products=[i.serialize for i in products])


@app.route('/category/<int:category_id>/product/<int:product_id>/JSON')
def productJSON(category_id, product_id):
    My_Product = session.query(Product).filter_by(id=product_id).one()
    return jsonify(Product=My_Product.serialize)


@app.route('/category/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


# Show all categories
@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    newProducts = session.query(Product).order_by(desc(Product.id)).slice(0,10)
    if 'username' not in login_session:
        return render_template('publiccategories.html', categories=categories,
        newProducts = newProducts)
    else:
        return render_template('categories.html', categories = categories,
        newProducts = newProducts)

# Create a new category
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'],
                                   user_id = login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newcategory.html')

# Edit a category
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    creator = getUserInfo(editedCategory.user_id)
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showCategories'))
    else:
        return render_template('editcategory.html', category=editedCategory)


# Delete a category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one()
    if categoryToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction(){alert('You are not authorized to delete this category.');}</script><body onload='myFunction()''>"


    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('deletecategory.html', category=categoryToDelete)

# Show a category
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/product/')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    products = session.query(Product).filter_by(
        category_id=category_id).all()
    creator = getUserInfo(category.user_id)
    if 'username' not in login_session or creator.id != login_session['user_id']: # login_session.get('user_id'): #
        return render_template('publiccategory.html', creator=creator, products=products, category=category)
    return render_template('category.html', products=products, category=category, creator = creator)

# Show a category
@app.route('/category/<int:category_id>/<int:product_id>')
def showProduct(category_id,product_id):
    category = session.query(Category).filter_by(id=category_id).one()
    product = session.query(Product).filter_by(id=product_id).one()
    creator = product.user_id
    if 'username' not in login_session or creator != login_session['user_id']: # login_session.get('user_id'): #
        return render_template('publicproduct.html', creator=creator, product=product, category=category)
    return render_template('product.html', product=product, category=category, creator = creator)


# Create a new product
@app.route('/category/<int:category_id>/product/new/', methods=['GET', 'POST'])
def newProduct(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newProduct = Product(name=request.form['name'],
                           description=request.form['description'], price=request.form['price'],
                           user_id = login_session['user_id'],
                           category_id=category_id)
        session.add(newProduct)
        session.commit()
        flash('New %s Product Successfully Created' % (newProduct.name))
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('newproduct.html', category_id=category_id)

# Edit a product product
@app.route('/category/<int:category_id>/product/<int:product_id>/edit', methods=['GET', 'POST'])
def editProduct(category_id, product_id):
    if 'username' not in login_session:
        return redirect('/login')

    editedProduct = session.query(Product).filter_by(id=product_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(category.user_id)
    if login_session['user_id'] != category.user_id:
        return redirect(url_for('showCategory', category_id=category_id))
    if request.method == 'POST':
        if request.form['name']:
            editedProduct.name = request.form['name']
        if request.form['description']:
            editedProduct.description = request.form['description']
        if request.form['price']:
            editedProduct.price = request.form['price']
        session.add(editedProduct)
        session.commit()
        flash('Category Product Successfully Edited')
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('editproduct.html', category_id=category_id, product_id=product_id, product=editedProduct)


# Delete a product
@app.route('/category/<int:category_id>/product/<int:product_id>/delete', methods=['GET', 'POST'])
def deleteProduct(category_id, product_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    productToDelete = session.query(Product).filter_by(id=product_id).one()
    if request.method == 'POST':
        session.delete(productToDelete)
        session.commit()
        flash('Category Product Successfully Deleted')
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('deleteproduct.html', product=productToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
