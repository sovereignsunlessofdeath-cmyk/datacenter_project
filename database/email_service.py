import os
import smtplib
from email.mime.text import MIMEText

def send_ticket_response_email(to_email, ticket_id, status, response_message):
    # This reads the keys directly from your Render environment setup
    sender_email = os.environ.get('EMAIL_ADDRESS')
    sender_password = os.environ.get('EMAIL_PASSWORD')
    
    # Constructing the raw email details
    subject = f"IT Ticket #{ticket_id} Update"
    body = f"Hello,\n\nYour ticket status has been updated to: {status}.\n\nAdmin Message:\n{response_message}\n\nBest regards,\nIT Support Team"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        # Standard Gmail secure connection configurations
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls() # Secure connection layer
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            print(f"SUCCESS: Notification email sent to {to_email}")
    except Exception as e:
        print(f"ERROR: Email failed to send. Reason: {e}")