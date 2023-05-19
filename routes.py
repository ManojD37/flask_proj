from . import app
from flask import render_template, request, redirect, url_for
from .models import User
from . import db
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Check if a user with the same username already exists
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            error = 'Username already exists. Please choose a different username.'
            return render_template('signup.html', error=error)

        # Create a new user instance
        new_user = User(name=name, email=email, username=username, password=password)

        # Add the new user to the session and commit to the database
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the home page after successful signup
        return redirect(url_for('home'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in the database
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            # User exists, login successful
            return redirect(url_for('home'))
        else:
            # Invalid credentials, redirect to login page with an error message
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')
