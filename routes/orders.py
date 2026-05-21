from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import date, timedelta
from database.db import load_data, save_data, get_staff_by_name
from database.models import create_order

bp = Blueprint('orders', __name__)

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session or session.get('role') != 'staff':
        return redirect(url_for('auth.login_staff'))
    
    data = load_data()
    staff_member = get_staff_by_name(data, session.get('user'))
    
    if not staff_member:
        return redirect(url_for('auth.login_staff'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if email:
            staff_member['email'] = email
            save_data(data)
            return redirect(url_for('orders.order'))
        else:
            return render_template('profile.html', 
                                   staff_name=session.get('user'),
                                   email=staff_member['email'],
                                   error='Email cannot be empty')
    
    return render_template('profile.html', 
                           staff_name=session.get('user'),
                           email=staff_member['email'])

@bp.route('/order')
def order():
    if 'user' not in session:
        return redirect(url_for('auth.login_staff'))
    
    data = load_data()
    tomorrow = str(date.today() + timedelta(days=1))
    return render_template('order.html',
                           menu=data["menu"],
                           tomorrow=tomorrow,
                           username=session.get('user'))

@bp.route('/submit_order', methods=['POST'])
def submit_order():
    if 'user' not in session:
        return redirect(url_for('auth.login_staff'))
    
    data = load_data()
    tomorrow = str(date.today() + timedelta(days=1))
    staff_name = session.get('user')
    food_choice = request.form['food_choice']
    
    if tomorrow not in data["orders"]:
        data["orders"][tomorrow] = []
    
    for order in data["orders"][tomorrow]:
        if order["name"] == staff_name:
            order["food"] = food_choice
            save_data(data)
            return redirect(url_for('orders.order_confirmation'))
    
    data["orders"][tomorrow].append(create_order(staff_name, food_choice))
    save_data(data)
    return redirect(url_for('orders.order_confirmation'))

@bp.route('/confirmation')
def order_confirmation():
    return render_template('confirmation.html')

@bp.route('/order_history')
def order_history():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login_admin'))
    
    data = load_data()
    orders = data["orders"]
    return render_template('order_history.html', orders=orders, username=session.get('user'))

@bp.route('/search_food', methods=['GET', 'POST'])
def search_food():
    if 'user' not in session:
        return redirect(url_for('auth.login_staff'))
    
    data = load_data()
    search_results = []
    search_query = ""
    
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        if search_query:
            search_results = search_and_rank_food(data, search_query)
    
    return render_template('search_food.html', 
                           results=search_results, 
                           search_query=search_query,
                           username=session.get('user'))

def search_and_rank_food(data, search_term):
    """Search for food items and rank by popularity"""
    search_term = search_term.lower().strip()
    
    if not search_term:
        return []
    
    # Count how many times each food was ordered
    food_count = {}
    for orders in data["orders"].values():
        for order in orders:
            food = order["food"]
            food_count[food] = food_count.get(food, 0) + 1
    
    # Find matching foods
    matching_foods = []
    for food in data["menu"]:
        if search_term in food.lower():
            matching_foods.append({
                "name": food,
                "times_ordered": food_count.get(food, 0)
            })
    
    # Sort by times ordered (most popular first)
    matching_foods.sort(key=lambda x: x["times_ordered"], reverse=True)
    
    return matching_foods