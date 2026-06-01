from flask import Blueprint, render_template, session
from datetime import date, timedelta
from database.db import load_data
from backend.middleware.auth_guard import admin_required

bp = Blueprint('admin', __name__)

@bp.route('/admin')
@admin_required  # The security checkpoint guard we just designed
def admin_dashboard():
    data = load_data()
    tomorrow = str(date.today() + timedelta(days=1))
    tomorrow_orders = data.get("orders", {}).get(tomorrow, [])
    staff_names = [s['name'] for s in data.get("staff", [])]
    
    return render_template('admin.html', 
                           orders=tomorrow_orders, 
                           staff=staff_names, 
                           menu=data.get("menu", []), 
                           tomorrow=tomorrow,
                           username=session.get('user'))