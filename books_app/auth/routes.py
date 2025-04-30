from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from books_app.models import Book, Author, Genre, User
from books_app.auth.forms import SignUpForm, LoginForm

# Import app and db from events_app package so that we can run app
from books_app.extensions import app, db, bcrypt

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    # initialize a SignUpForm instance from forms.py
    form = SignUpForm()
    
    # If the form is valid,
    if form.validate_on_submit():
        # Generate a hashed passowrd using bcrypt library
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        # Create a new User with given username and hashed password
        user = User(
            username = form.username.data,
            password = hashed_password
        )
        
        # Commit to database
        db.session.add(user)
        db.session.commit()
        
        # Flash a success message to the user
        flash('Account created successfully')
        # Redirect to login page
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        # This would allow user to go back where they were before
        next_page = request.args.get('next')
        
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    # TODO: Fill out this route!
    pass
