from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime
from database.db import load_data, save_data, get_ticket_by_id, get_staff_by_name
from database.models import create_ticket
from backend.services.email_service import send_ticket_response_email
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
    
    # 1. Capture the manually forced email address from the HTML form
    user_email = request.form.get('user_email', '').strip()
    
    # 2. Generate the base ticket object using model blueprint logic
    ticket = create_ticket(
        request.form['name'],
        request.form['department'],
        request.form['category'],
        request.form['description']
    )
    
    # 3. Inject unique key attributes into the document store dictionary
    ticket['id'] = len(data["tickets"]) + 1
    ticket['submitted_email'] = user_email  # Saves the manually provided email
    
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
            
            # 4. Fetch the staff fallback record if available
            staff_member = get_staff_by_name(data, ticket['name'])
            
            # 5. Determine the best recipient email target (Preferring manual input)
            recipient_email = ticket.get('submitted_email') or (staff_member.get('email') if staff_member else None)
            
            # Trigger our backend utility service to email the user safely
            if recipient_email:
                try:
                    send_ticket_response_email(recipient_email, ticket_id, new_status, response_message)
                except Exception as mail_error:
                    print(f"Network email notification skipped: {mail_error}")
            else:
                print(f"LOG: Could not send notification for Ticket #{ticket_id}. No valid target email found.")
            
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