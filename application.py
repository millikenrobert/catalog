# Import libraries
from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, SportsItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
from string import lower
import requests

# Launch app
app = Flask(__name__)

# Declare constants
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Category Udacity"

# Create db connection
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token (adapted from Udacity Full Stack)
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# Google login (adapted from Udacity Full Stack)


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

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already \
            connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User functions - Create user


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# User functions - Get user object


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# User functions - return user ID


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# Google disconnect code


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % \
        access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Show the Categories
@app.route('/')
@app.route('/categories')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))

    for c in categories:
        print("ID: %s Name: %s" % (c.id, c.name))

    if 'username' not in login_session:
        return render_template('public_categories.html',
                               categories=categories)
    else:
        return render_template('auth_categories.html',
                               categories=categories)

# Show the sports items


@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/items/')
def showItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(category.user_id)
    items = session.query(SportsItem).filter_by(category_id=category_id).all()
    if 'username' not in login_session or creator.id != \
            login_session['user_id']:
        return render_template('public_items.html', items=items,
                               category=category, creator=creator)
    else:
        return render_template("auth_items.html", items=items,
                               category=category, creator=creator)

# show recent items added


@app.route('/categories/recentItems/')
def showNew():
    items = session.query(SportsItem).order_by(desc(SportsItem.id))
    return render_template('recentItems.html', items=items)


# Create sports items
@app.route('/categories/<int:category_id>/items/new/', methods=['GET',
                                                                'POST'])
def addItems(category_id):
    if 'username' not in login_session:
        return redirect('/login')

    category = session.query(Category).filter_by(id=category_id).one()

    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction() {alert('Not authorised to add \
        Sports Item to this category');}</script><body onload='myFunction()'>"

    if request.method == 'POST':
        newItem = SportsItem(name=request.form['name'],
                             description=request.form[
                             'description'], category=category,
                             user_id=category.user_id)
        session.add(newItem)
        session.commit()
        flash('New %s Item Successfully Created' % (newItem.name))
        print("sdfsd")
        return redirect(url_for('showItems', category_id=category_id))

    else:
        return render_template('newItem.html', category_id=category_id)


# Create sports categories

@app.route('/categories/new/', methods=['GET', 'POST'])
def addCategory():
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')

# Edit items


@app.route('/categories/<int:category_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')

    editedItem = session.query(SportsItem).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()

    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction() {alert('Not authorised to \
        edit this Sports Item');}</script><body onload='myFunction()'>"

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']

        session.add(editedItem)
        session.commit()
        flash('Item Edited')
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('editItem.html', category_id=category_id,
                               item_id=item_id, item=editedItem)


# Delete a item
@app.route('/categories/<int:category_id>/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')

    deleteItem = session.query(SportsItem).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()

    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction() {alert('Not authorised to \
        delete this Sports Item');}</script><body onload='myFunction()'>"

    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash('Item Deleted')
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteItem.html', item=deleteItem)

# Disconnect based on provider


@app.route('/logout')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))

# JSON APIs

# get all items from category


@app.route('/api/categories/<int:category_id>/items/JSON')
def sportsItemJSON(category_id):
    items = session.query(SportsItem).filter_by(category_id=category_id).all()
    return jsonify(SportsItem=[i.serialize for i in items])

# get s single item from category


@app.route('/api/categories/<int:category_id>/items/<int:item_id>/JSON')
def allItemsJSON(category_id, item_id):
    item = session.query(SportsItem).filter_by(id=item_id).one()
    return jsonify(SportsItem=item.serialize)

# get all categories


@app.route('/api/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
