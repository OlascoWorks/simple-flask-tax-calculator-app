from flask import Blueprint, url_for, render_template, request, flash, redirect
from flask_login import login_required, current_user
from .models import User, Calculations
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        amount = request.form.get('amount')
        percent = request.form.get('tax-percent')
        
        if len(amount) < 1:
            flash('Please input an amount', category='error')
            return redirect(url_for('views.home'))
        elif len(percent) < 1:
            flash('Please input a tax percentage', category='error')
            return redirect(url_for('views.home'))
        else:
            #check for valid input
            try:
                result = int((int(percent)/100) *int(amount))
                bal = int(int(amount) -int(result))
                new_calculation = Calculations(tax=result, balance=bal, user_id=current_user.id)
                db.session.add(new_calculation)
                db.session.commit()
                return render_template('home.html', tax=result, balance=bal)
            except ValueError:
                flash('Please make sure to put in valid inputs', category='error')
                return render_template('home.html')
    
    return render_template('home.html', user=current_user)
    
@views.route('/history')
@login_required
def history():
    return render_template('history.html', user=current_user)