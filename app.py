from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash, make_response
from flask import session as login_session

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User, Category, Book

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import random
import string
import httplib2
import json
import requests
import config

app = Flask(__name__)

CLIENT_ID = config.CLIENT_ID
APPLICATION_NAME = config.APP_NAME

# Connect to the database and create database session
engine = create_engine(config.DB_CONNECT)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def getCategories():
    return session.query(Category)

''' ******************************* HOME PAGE **************************** '''


@app.route('/')
@app.route('/home/')
def showHomePage():
    recentBooks = session.query(Book).order_by(desc(Book.id)).limit(5).all()
    return render_template(
        'home.html', recentBooks=recentBooks, categories=getCategories())

''' ******************************* CATEGORY ***************************** '''


@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/books/')
def showCategory(category_id):
    # Show contents of the category
    category = session.query(Category).filter_by(id=category_id).one()
    books = session.query(Book).filter_by(category_id=category_id).all()
    return render_template(
                'category.html',
                books=books,
                category=category,
                categories=getCategories())


@app.route('/category/add/', methods=['GET', 'POST'])
def addNewCategory():
    # Add a new category to the catalog
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'],
                               user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash('new category %s was added to the catalog' % (newCategory.name))
        return redirect(url_for('showCategory', category_id=newCategory.id))
    else:
        return render_template(
                    'addcategory.html',
                    categories=getCategories())


@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    # Edit the name of the category
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    if login_session['user_id'] != category.user_id:
        flash('you are not authorized to edit this category')
        return redirect(url_for('showCategory', category_id=category_id))
    if request.method == 'POST':
        category.name = request.form['name']
        session.add(category)
        session.commit()
        flash('changes were saved')
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template(
                    'editcategory.html',
                    category=category,
                    categories=getCategories())


@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    # Delete the category and its books from the catalog
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    books = session.query(Book).filter_by(category_id=category_id).all()
    if login_session['user_id'] != category.user_id:
        flash('you are not authorized to delete this category')
        return redirect(url_for('showCategory', category_id=category_id))
    if request.method == 'POST':
        if books:
            for book in books:
                session.delete(book)
        session.delete(category)
        session.commit()
        flash('category was deleted from the catalog')
        return redirect(url_for('showHomePage'))
    else:
        return render_template(
                    'deletecategory.html',
                    category=category,
                    categories=getCategories())

''' ******************************** BOOK ******************************** '''


@app.route('/category/<int:category_id>/books/<int:book_id>/')
def showBook(category_id, book_id):
    # Show details of the book
    book = session.query(Book).filter_by(id=book_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    contributor = session.query(User).filter_by(id=book.user_id).one()
    return render_template(
                'book.html',
                book=book,
                contributor=contributor,
                category=category,
                categories=getCategories())


@app.route('/category/<int:category_id>/books/add/', methods=['GET', 'POST'])
def addNewBook(category_id):
    # Add a new book to the category
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newBook = Book(title=request.form['title'],
                       author=request.form['author'],
                       description=request.form['description'],
                       category_id=category_id,
                       user_id=login_session['user_id'])
        session.add(newBook)
        session.commit()
        flash('new book %s was added to the catalog' % (newBook.title))
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template(
                    'addbook.html',
                    category=category,
                    categories=getCategories())


@app.route('/category/<int:category_id>/books/<int:book_id>/update/',
           methods=['GET', 'POST'])
def updateBook(category_id, book_id):
    # Update details of the book
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    bookToUpdate = session.query(Book).filter_by(id=book_id).one()
    if login_session['user_id'] != bookToUpdate.user_id:
        flash('you are not authorized to update this book')
        return redirect(
            url_for('showBook', category_id=category_id, book_id=book_id))
    if request.method == 'POST':
        bookToUpdate.category_id = request.form['category']
        bookToUpdate.title = request.form['title']
        bookToUpdate.author = request.form['author']
        bookToUpdate.description = request.form['description']
        session.add(bookToUpdate)
        session.commit()
        flash('changes were saved')
        return redirect(url_for(
                            'showBook',
                            category_id=bookToUpdate.category_id,
                            book_id=book_id))
    else:
        return render_template(
                    'updatebook.html',
                    bookToUpdate=bookToUpdate,
                    currentCategory=category,
                    categories=getCategories())


@app.route('/category/<int:category_id>/books/<int:book_id>/delete/',
           methods=['GET', 'POST'])
def deleteBook(category_id, book_id):
    # Delete the book from the catalog
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    bookToDelete = session.query(Book).filter_by(id=book_id).one()
    if login_session['user_id'] != bookToDelete.user_id:
        flash('you are not authorized to delete this book')
        return redirect(
            url_for('showBook', category_id=category_id, book_id=book_id))
    if request.method == 'POST':
        session.delete(bookToDelete)
        session.commit()
        flash('book was deleted from the catalog')
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template(
                    'deletebook.html',
                    bookToDelete=bookToDelete,
                    category=category,
                    categories=getCategories())

''' ******************************* JSON APIs **************************** '''


@app.route('/json/')
@app.route('/home/json/')
def allCategoriesToJSON():
    categories = session.query(Category).all()
    return jsonify(Categories=[c.serialize for c in categories])


@app.route('/books/json/')
def allBooksToJSON():
    books = session.query(Book).order_by(asc(Book.category_id)).all()
    return jsonify(Books=[book.serialize for book in books])


@app.route('/category/<int:category_id>/json/')
@app.route('/category/<int:category_id>/books/json/')
def categoryToJSON(category_id):
    books = session.query(Book).filter_by(category_id=category_id).all()
    return jsonify(Category=[book.serialize for book in books])


@app.route('/category/<int:category_id>/books/<int:book_id>/json/')
def bookToJSON(category_id, book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    return jsonify(Book=[book.serialize])

''' ******************************* LOGIN ******************************** '''


@app.route('/login')
def showLogin():
    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, client_id=CLIENT_ID)


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

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use
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
    login_session['provider'] = 'google'

    # See if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = '<img class="user_img" src="'+login_session['picture']+'">'
    flash("you are now logged in as %s" % login_session['username'])
    return output


# User helper functions
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

''' ******************************* LOGOUT ******************************* '''


@app.route('/gdisconnect')
def gdisconnect():
    '''
    Revoke a current user's token and reset their login_session'.
    Only disconnect a connected user
    '''
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(
            json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
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
        flash('you have successfully been logged out')
        return redirect(url_for('showHomePage'))
    else:
        flash('you were not logged in')
        return redirect(url_for('showHomePage'))

''' ******************************* START APP **************************** '''
if __name__ == '__main__':
    app.secret_key = config.APP_KEY
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
