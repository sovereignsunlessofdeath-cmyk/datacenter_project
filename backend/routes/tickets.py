from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime
from database.db import load_data, save_data, get_ticket_by_id, get_staff_by_name
from database.models import create_ticket
from backend.routes.email_service import send_ticket_response_email
from backend.middleware.auth_guard import login_required, admin_required

bp = Blueprint('tickets', __name__)

@bp.route('/submit_support_ticket')
@login_required  # Restricts ticket submission views to authenticated users
def submit_support_ticket():
    data = load_data()
    return render_template('submit_ticket.html', 
                           categories=data["ticket_categories"],
                           username=session.get('user'))

@bp.route('/submit_ticket', methods=['POST'])
@login_required
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

@bp.route('/tickets')
@admin_required  # Restricts full ticketing database view exclusively to admins
def tickets():
    data = load_data()
    tickets = data["tickets"]
    return render_template('tickets.html', 
                           tickets=tickets,
                           categories=data["ticket_categories"],
                           username=session.get('user'))

@bp.route('/respond_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@admin_required
def respond_ticket(ticket_id):
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
            
            # Fetch the staff member's email details
            staff_member = get_staff_by_name(data, ticket['name'])
            
            # Trigger our backend utility service to email the user safely
            if staff_member and staff_member.get('email'):
                try:
                    send_ticket_response_email(staff_member['email'], ticket_id, new_status, response_message)
                    pass
                except Exception as mail_error:
                    print(f"Network email notification skipped: {mail_error}")
            
            return redirect(url_for('tickets.tickets'))
    
    return render_template('respond_ticket.html', ticket=ticket, username=session.get('user'))

@bp.route('/update_ticket/<int:ticket_id>/<string:status>')
@admin_required
def update_ticket(ticket_id, status):
    data = load_data()
    ticket = get_ticket_by_id(data, ticket_id)
    
    if ticket:
        ticket["status"] = status
        if status == "Resolved":
            ticket["date_resolved"] = str(datetime.now())
        save_data(data)
        
    return redirect(url_for('tickets.tickets'))

@bp.route('/delete_ticket/<int:ticket_id>')
@admin_required
def delete_ticket(ticket_id):
    data = load_data()
    data["tickets"] = [t for t in data["tickets"] if t["id"] != ticket_id]
    save_data(data)
    return redirect(url_for('tickets.tickets'))