import os
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def _send_email_worker(to_email, ticket_id, new_status, response_message):
    """
    Internal background worker. This connects to Gmail's SMTP servers
    and sends the update message directly to the staff member's email.
    """
    sender_email = os.environ.get("SMTP_USER")
    sender_password = os.environ.get("SMTP_PASSWORD")  # Must be a 16-character Gmail App Password

    if not sender_email or not sender_password:
        print("LOG: Email notification skipped. SMTP credentials are not configured in environment variables.")
        return

    # 1. Build the email headers
    msg = MIMEMultipart()
    msg['From'] = f"CitiData Helpdesk <{sender_email}>"
    msg['To'] = to_email
    msg['Subject'] = f"Update on your IT Support Ticket #{ticket_id} [{new_status}]"

    # 2. Craft the message body for the staff member
    body = f"""Hello,

An IT Administrator has updated the status of your support ticket #{ticket_id}.

--------------------------------------------------
[Current Status]: {new_status}
[Admin Response]:
{response_message}
--------------------------------------------------

You can view the full details of your request by logging into the CitiData Center Portal.

Best regards,
CitiData Centre IT Support Team
"""
    msg.attach(MIMEText(body, 'plain'))

    # 3. Establish the secure connection to Gmail
    try:
        print(f"Connecting to Gmail SSL to notify {to_email}...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            print(f"SUCCESS: Notification email sent to staff member at: {to_email}")
    except Exception as e:
        print(f"ERROR: Background email delivery failed. Reason: {e}")


def send_ticket_response_email(to_email, ticket_id, new_status, response_message):
    """
    Call this function from your routes. It instantly spawns a background thread 
    to send the email so your web page loads instantly without lag.
    """
    email_thread = threading.Thread(
        target=_send_email_worker,
        args=(to_email, ticket_id, new_status, response_message)
    )
    email_thread.daemon = True
    email_thread.start()