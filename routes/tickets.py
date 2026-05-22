from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime

# Fixed path address styles - no more missing import lines!
from ..database.db import load_data, save_data, get_ticket_by_id, get_staff_by_name
from ..database.models import create_ticket
from ..database.email_service import send_ticket_response_email

bp = Blueprint('tickets', __name__)

@bp.route('/submit_support_ticket')
def submit_support_ticket():
    if 'user' not in session:
        return redirect(url_for('auth.login_staff'))
    
    data = load_data()
    return render_template('submit_ticket.html', 
                           categories=data["ticket_categories"],
                           username=session.get('user'))

@bp.route('/tickets')
def tickets():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login_admin'))
    
    data = load_data()
    tickets = data["tickets"]
    return render_template('tickets.html', 
                           tickets=tickets,
                           categories=data["ticket_categories"],
                           username=session.get('user'))

@bp.route('/submit_ticket', methods=['POST'])
def submit_ticket():
    data = load_data()
    ticket = create_ticket(
        request.form['name'],
        request.form['department'],
        request.form['category'],
        request.form['description']
    )
    ticket['id'] = len(data["tickets"]) + 1
    data["tickets"].append(ticket)
    save_data(data)
    return redirect(url_for('tickets.submit_support_ticket'))

@bp.route('/respond_ticket/<int:ticket_id>', methods=['GET', 'POST'])
def respond_ticket(ticket_id):
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login_admin'))
    
    data = load_data()
    ticket = get_ticket_by_id(data, ticket_id)
    
    if not ticket:
        return redirect(url_for('tickets.tickets'))
    
    if request.method == 'POST':
        response_message = request.form.get('response_message', '').strip()
        new_status = request.form.get('status', ticket['status'])
        
        if response_message:
            ticket['status'] = new_status
            if new_status == "Resolved":
                ticket['date_resolved'] = str(datetime.now())
            
            save_data(data)
            
            staff_member = get_staff_by_name(data, ticket['name'])
            
            if staff_member and staff_member['email']:
                # The safety net block catching Render's network blocks
                try:
                    send_ticket_response_email(staff_member['email'], ticket_id, new_status, response_message)
                except Exception as mail_error:
                    # Keeps the web app running even if the cloud server blocks email ports
                    print(f"Network email notification skipped: {mail_error}")
            
            return redirect(url_for('tickets.tickets'))
    
    return render_template('respond_ticket.html', ticket=ticket, username=session.get('user'))

@bp.route('/update_ticket/<int:ticket_id>/<string:status>')
def update_ticket(ticket_id, status):
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login_admin'))
    
    data = load_data()
    ticket = get_ticket_by_id(data, ticket_id)
    
    if ticket:
        ticket["status"] = status
        if status == "Resolved":
            ticket["date_resolved"] = str(datetime.now())
    
    save_data(data)
    return redirect(url_for('tickets.tickets'))

@bp.route('/delete_ticket/<int:ticket_id>')
def delete_ticket(ticket_id):
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login_admin'))
    
    data = load_data()
    data["tickets"] = [t for t in data["tickets"] if t["id"] != ticket_id]
    save_data(data)
    return redirect(url_for('tickets.tickets'))