import os
import smtplib
from email.mime.text import MIMEText

def send_ticket_response_email(to_email, ticket_id, status, response_message):
    # Pull credentials from Render and strip any accidental spaces
    sender_email = os.environ.get('EMAIL_ADDRESS', '').strip()
    sender_password = os.environ.get('EMAIL_PASSWORD', '').strip()
    
    # Build the email
    subject = f"IT Ticket #{ticket_id} Update"
    body = f"Hello,\n\nYour ticket status has been updated to: {status}.\n\nAdmin Message:\n{response_message}\n\nBest regards,\nIT Support Team"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        # Using SMTP_SSL and port 465 is much safer on cloud environments like Render
        print("Connecting securely to Gmail via SSL...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            print(f"SUCCESS: Notification email sent to {to_email}")
    except Exception as e:
        print(f"ERROR: Email failed to send. Reason: {e}")