from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from datetime import date, datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key_change_this'
DATA_FILE = 'data.json'

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Admin credentials
ADMIN_ACCOUNTS = {
    'Damilare@Citidata': 'Damilare',
    'Mr Godwin@Admin': 'Admin',
    'Mr Andie@Admin': 'Admin'
}

# Load data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        "staff": [],
        "menu": [],
        "orders": {},
        "tickets": [],
        "ticket_categories": ["Network Issue", "Hardware Problem", "Software Bug", "Password Reset", "Other"]
    }

# Save data to file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Search and rank food by popularity
def search_and_rank_food(data, search_term):
    """
    Search for food items and rank by popularity (most ordered first)
    """
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

# Send email notification for ticket response
def send_ticket_response_email(staff_email, ticket_id, status, response_message):
    """
    Send email notification when ticket is responded to
    """
    try:
        subject = f"Ticket #{ticket_id} - Response from IT Team"
        
        body = f"""
Hello,

Your support ticket has been responded to.

Ticket ID: #{ticket_id}
Current Status: {status}

Response from IT Team:
{response_message}

Please log back into the system to view more details.

Best regards,
Data Centre IT Team
        """
        
        message = MIMEMultipart()
        message['From'] = EMAIL_ADDRESS
        message['To'] = staff_email
        message['Subject'] = subject
        
        message.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)
        
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

# ============== LOGIN ROUTES ==============

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in ADMIN_ACCOUNTS and ADMIN_ACCOUNTS[username] == password:
            session['user'] = username
            session['role'] = 'admin'
            return redirect(url_for('admin'))
        else:
            return render_template('login_admin.html', error='Invalid username or password')
    
    return render_template('login_admin.html')

@app.route('/login_staff', methods=['GET', 'POST'])
def login_staff():
    data = load_data()
    if request.method == 'POST':
        staff_name = request.form['staff_name']
        
        if staff_name in data['staff']:
            session['user'] = staff_name
            session['role'] = 'staff'
            return redirect(url_for('order'))
        else:
            return render_template('login_staff.html', staff=data['staff'], error='Staff name not found')
    
    return render_template('login_staff.html', staff=data['staff'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ============== ADMIN DASHBOARD ==============

@app.route('/admin')
def admin():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_admin'))
    
    data = load_data()
    tomorrow = str(date.today() + timedelta(days=1))
    tomorrow_orders = data["orders"].get(tomorrow, [])
    return render_template('admin.html', 
                           orders=tomorrow_orders, 
                           staff=data["staff"], 
                           menu=data["menu"], 
                           tomorrow=tomorrow,
                           username=session.get('user'))

# ============== FOOD ORDER ROUTES ==============

@app.route('/order')
def order():
    if 'user' not in session:
        return redirect(url_for('login_staff'))
    
    data = load_data()
    tomorrow = str(date.today() + timedelta(days=1))
    return render_template('order.html',
                           menu=data["menu"],
                           tomorrow=tomorrow,
                           username=session.get('user'))

@app.route('/submit_order', methods=['POST'])
def submit_order():
    if 'user' not in session:
        return redirect(url_for('login_staff'))
    
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
            return redirect(url_for('order_confirmation'))
    
    data["orders"][tomorrow].append({
        "name": staff_name,
        "food": food_choice
    })
    save_data(data)
    return redirect(url_for('order_confirmation'))

@app.route('/confirmation')
def order_confirmation():
    return render_template('confirmation.html')

@app.route('/order_history')
def order_history():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_admin'))
    
    data = load_data()
    orders = data["orders"]
    return render_template('order_history.html', orders=orders, username=session.get('user'))

@app.route('/search_food', methods=['GET', 'POST'])
def search_food():
    if 'user' not in session:
        return redirect(url_for('login_staff'))
    
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

# ============== STAFF TICKET SUBMISSION ==============

@app.route('/submit_support_ticket')
def submit_support_ticket():
    if 'user' not in session:
        return redirect(url_for('login_staff'))
    
    data = load_data()
    return render_template('submit_ticket.html', 
                           categories=data["ticket_categories"],
                           username=session.get('user'))

# ============== IT HELPDESK ROUTES ==============

@app.route('/tickets')
def tickets():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_admin'))
    
    data = load_data()
    tickets = data["tickets"]
    return render_template('tickets.html', 
                           tickets=tickets,
                           categories=data["ticket_categories"],
                           username=session.get('user'))

@app.route('/submit_ticket', methods=['POST'])
def submit_ticket():
    data = load_data()
    ticket = {
        "id": len(data["tickets"]) + 1,
        "name": request.form['name'],
        "department": request.form['department'],
        "category": request.form['category'],
        "description": request.form['description'],
        "status": "Open",
        "date_created": str(datetime.now()),
        "date_resolved": None
    }
    data["tickets"].append(ticket)
    save_data(data)
    return redirect(url_for('submit_support_ticket'))

@app.route('/respond_ticket/<int:ticket_id>', methods=['GET', 'POST'])
def respond_ticket(ticket_id):
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_admin'))
    
    data = load_data()
    ticket = None
    
    for t in data["tickets"]:
        if t["id"] == ticket_id:
            ticket = t
            break
    
    if not ticket:
        return redirect(url_for('tickets'))
    
    if request.method == 'POST':
        response_message = request.form.get('response_message', '').strip()
        new_status = request.form.get('status', ticket['status'])
        
        if response_message:
            ticket['status'] = new_status
            if new_status == "Resolved":
                ticket['date_resolved'] = str(datetime.now())
            
            save_data(data)
            
            # Send email notification
            staff_email = ticket['name'].lower().replace(' ', '.') + '@company.com'
            send_ticket_response_email(staff_email, ticket_id, new_status, response_message)
            
            return redirect(url_for('tickets'))
    
    return render_template('respond_ticket.html', ticket=ticket, username=session.get('user'))

@app.route('/update_ticket/<int:ticket_id>/<string:status>')
def update_ticket(ticket_id, status):
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_admin'))
    
    data = load_data()
    for ticket in data["tickets"]:
        if ticket["id"] == ticket_id:
            ticket["status"] = status
            if status == "Resolved":
                ticket["date_resolved"] = str(datetime.now())
    save_data(data)
    return redirect(url_for('tickets'))

@app.route('/delete_ticket/<int:ticket_id>')
def delete_ticket(ticket_id):
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_admin'))
    
    data = load_data()
    data["tickets"] = [t for t in data["tickets"] if t["id"] != ticket_id]
    save_data(data)
    return redirect(url_for('tickets'))

# ============== SETTINGS ROUTES ==============

@app.route('/settings')
def settings():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_admin'))
    
    data = load_data()
    return render_template('settings.html', 
                           staff=data["staff"], 
                           menu=data["menu"],
                           categories=data["ticket_categories"],
                           username=session.get('user'))

@app.route('/add_staff', methods=['POST'])
def add_staff():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_admin'))
    
    data = load_data()
    name = request.form['staff_name'].strip()
    if name and name not in data["staff"]:
        data["staff"].append(name)
    save_data(data)
    return redirect(url_for('settings'))

@app.route('/remove_staff/<string:name>')
def remove_staff(name):
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_admin'))
    
    data = load_data()
    if name in data["staff"]:
        data["staff"].remove(name)
    save_data(data)
    return redirect(url_for('settings'))

@app.route('/add_food', methods=['POST'])
def add_food():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_admin'))
    
    data = load_data()
    food = request.form['food_item'].strip()
    if food and food not in data["menu"]:
        data["menu"].append(food)
    save_data(data)
    return redirect(url_for('settings'))

@app.route('/remove_food/<string:food>')
def remove_food(food):
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_admin'))
    
    data = load_data()
    if food in data["menu"]:
        data["menu"].remove(food)
    save_data(data)
    return redirect(url_for('settings'))

@app.route('/add_category', methods=['POST'])
def add_category():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_admin'))
    
    data = load_data()
    category = request.form['category_name'].strip()
    if category and category not in data["ticket_categories"]:
        data["ticket_categories"].append(category)
    save_data(data)
    return redirect(url_for('settings'))

@app.route('/remove_category/<string:category>')
def remove_category(category):
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_admin'))
    
    data = load_data()
    if category in data["ticket_categories"]:
        data["ticket_categories"].remove(category)
    save_data(data)
    return redirect(url_for('settings'))

if __name__ == '__main__':
    app.run(debug=True)