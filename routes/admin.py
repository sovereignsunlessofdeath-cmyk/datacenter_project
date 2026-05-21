from flask import Blueprint, render_template, redirect, url_for, session
from datetime import date, timedelta
from database.db import load_data

bp = Blueprint('admin', __name__)

@bp.route('/admin')
def admin_dashboard():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login_admin'))
    
    data = load_data()
    tomorrow = str(date.today() + timedelta(days=1))
    tomorrow_orders = data["orders"].get(tomorrow, [])
    staff_names = [s['name'] for s in data["staff"]]
    
    return render_template('admin.html', 
                           orders=tomorrow_orders, 
                           staff=staff_names, 
                           menu=data["menu"], 
                           tomorrow=tomorrow,
                           username=session.get('user'))