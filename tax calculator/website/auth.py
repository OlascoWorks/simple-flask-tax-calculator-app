from flask import Blueprint, render_template, flash, request, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pass')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password or email', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('email does not exist', category='error')
            return redirect(url_for('auth.login'))
        
    
    return render_template('login.html', user=current_user)
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    
@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('Username')
        email = request.form.get('email')
        password1 = request.form.get('pass1')
        password2 = request.form.get('pass2')
        
        #check for input validity
        user = User.query.filter_by(email=email).first()
        if user:
            flash('email already exists', category='error')
            return redirect(url_for('auth.sign_up'))
        elif len(name) < 2:
            flash('Username is too short', category='error')
            return redirect(url_for('auth.sign_up'))
        elif password1 != password2:
            flash('Passwords do not match', category='error')
            return redirect(url_for('auth.sign_up'))
        elif len(password1) < 7:
            flash('Password must be at least 6 characters', category='error')
            return redirect(url_for('auth.sign_up'))
        else:
            flash('account created successfully', category='success')
            new_user = User(name=name, email=email, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            
    
    return render_template('signup.html', user=current_user)