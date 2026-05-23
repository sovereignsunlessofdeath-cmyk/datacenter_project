from flask import Blueprint, render_template, request, redirect, url_for, session
from config import Config
from database.db import load_data, save_data, get_staff_by_name

bp = Blueprint('auth', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in Config.ADMIN_ACCOUNTS and Config.ADMIN_ACCOUNTS[username] == password:
            session['user'] = username
            session['role'] = 'admin'
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return render_template('login_admin.html', error='Invalid username or password')
    
    return render_template('login_admin.html')

@bp.route('/login_staff', methods=['GET', 'POST'])
def login_staff():
    data = load_data()
    if request.method == 'POST':
        staff_name = request.form['staff_name'].strip()
        
        # Check if staff exists in the database
        staff_member = get_staff_by_name(data, staff_name)
        
        if staff_member:
            session['user'] = staff_name
            session['role'] = 'staff'
            
            # If email is empty, redirect to profile to add email
            if not staff_member.get('email'):
                return redirect(url_for('orders.profile'))
            
            # Updated to 'order_food' to perfectly match your blueprint target function
            return redirect(url_for('orders.order_food'))
        else:
            staff_names = [s['name'] for s in data.get('staff', [])]
            return render_template('login_staff.html', staff=staff_names, error='Staff name not found')
    
    staff_names = [s['name'] for s in data.get('staff', [])]
    return render_template('login_staff.html', staff=staff_names)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))