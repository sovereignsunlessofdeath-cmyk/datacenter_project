from flask import Blueprint, render_template, request, redirect, url_for, session
from database.db import load_data, save_data
from database.models import create_staff
from backend.middleware.auth_guard import admin_required

bp = Blueprint('settings', __name__)

@bp.route('/settings')
@admin_required  # Intercepts unauthorized attempts globally
def settings():
    data = load_data()
    staff_names = [s['name'] for s in data["staff"]]
    return render_template('settings.html', 
                           staff=staff_names, 
                           menu=data["menu"],
                           categories=data["ticket_categories"],
                           username=session.get('user'))

@bp.route('/add_staff', methods=['POST'])
@admin_required
def add_staff():
    data = load_data()
    name = request.form['staff_name'].strip()
    
    staff_exists = any(s['name'] == name for s in data["staff"])
    
    if name and not staff_exists:
        data["staff"].append(create_staff(name, ""))
        save_data(data)
    return redirect(url_for('settings.settings'))

@bp.route('/remove_staff/<string:name>')
@admin_required
def remove_staff(name):
    data = load_data()
    data["staff"] = [s for s in data["staff"] if s['name'] != name]
    save_data(data)
    return redirect(url_for('settings.settings'))

@bp.route('/add_food', methods=['POST'])
@admin_required
def add_food():
    data = load_data()
    food = request.form['food_item'].strip()
    if food and food not in data["menu"]:
        data["menu"].append(food)
        save_data(data)
    return redirect(url_for('settings.settings'))

@bp.route('/remove_food/<string:food>')
@admin_required
def remove_food(food):
    data = load_data()
    if food in data["menu"]:
        data["menu"].remove(food)
        save_data(data)
    return redirect(url_for('settings.settings'))

@bp.route('/add_category', methods=['POST'])
@admin_required
def add_category():
    data = load_data()
    category = request.form['category_name'].strip()
    if category and category not in data["ticket_categories"]:
        data["ticket_categories"].append(category)
        save_data(data)
    return redirect(url_for('settings.settings'))

@bp.route('/remove_category/<string:category>')
@admin_required
def remove_category(category):
    data = load_data()
    if category in data["ticket_categories"]:
        data["ticket_categories"].remove(category)
        save_data(data)
    return redirect(url_for('settings.settings'))