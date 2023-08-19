from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, find_email, find_long
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import validators
#if you store hash of a password you cant know what the oriinal password is AKA what hashes to it
auth = Blueprint('auth', __name__)
#by default without list of methods can only accept get
@auth.route('/login', methods =['GET', 'POST'])
def login():
    data = request.form # request has stuff sent form has form stuff
    #data is a dictionary of vars and their values set by form
    #get doesnt send anothing(not clicking submit)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        check = find_email(email)
        if check:
            #might have to do user.password instead of current
            if check_password_hash(check["password"], password):
                flash('Logged in successfully!', category ='success')
                login_user(User(check), remember=True)
                return redirect(url_for('views.home'))
                #redirects to homepage if you login successfully
            else:
                flash('Incorrect password, try again.', category = 'error')
        else:
            flash('Email does not exist.', category = 'error')

    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods =['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        check= find_email(email)

        valid =  validators.email(email)
        if check:
            flash('Email already exists', category = 'error')
        elif not valid: 
            flash('Email is not valid', category = 'error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category = 'error')
            #flashses message and sends category need to display messages
        elif len(firstName) < 3:
            flash('First Name must be greater than 2 characters.', category = 'error')
        elif password2 != password1:
            flash('Passwords must match', category = 'error')
        elif len(password1) < 7:
            flash('Password must be greater than 6 characters.', category = 'error')
        else:
            # add user to database
            
            #make sure yyou add user password with hash
            hashed_password = generate_password_hash(password1)
            user_data = {
                'email': email, 
                'firstName': firstName, 
                'password': hashed_password
            }
            db.Users.insert_one(user_data)
            user = User(user_data)
            login_user(user, remember=True)
            flash('Account Created!', category = 'success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user = current_user)




