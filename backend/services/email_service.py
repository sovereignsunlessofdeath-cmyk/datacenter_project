import os
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def _send_email_worker(to_email, ticket_id, new_status, response_message):
    """
    Background worker that connects to Gmail via Port 587 using STARTTLS.
    This bypasses Render's outbound firewall blocks on the Free Tier!
    """
    sender_email = os.environ.get("SMTP_USER")
    sender_password = os.environ.get("SMTP_PASSWORD")  # Your 16-character Gmail App Password

    if not sender_email or not sender_password:
        print("LOG: Email notification skipped. SMTP credentials are missing from environment variables.")
        return

    # 1. Setup the Email Enveloping and Headers
    msg = MIMEMultipart()
    msg['From'] = f"CitiData Helpdesk <{sender_email}>"
    msg['To'] = to_email
    msg['Subject'] = f"Update on your IT Support Ticket #{ticket_id} [{new_status}]"

    # 2. Craft the Beautiful HTML Body Structure
    html_body = f"""
    <html>
    <body>
        <h2>Hello,</h2>
        <p>An IT Administrator has updated the status of your support ticket <strong>#{ticket_id}</strong>.</p>
        <hr style="border: 1px solid #eee;" />
        <p><strong>[Current Status]:</strong> <span style="color: #2b6cb0; font-weight: bold;">{new_status}</span></p>
        <p><strong>[Admin Response]:</strong></p>
        <blockquote style="background: #f7fafc; border-left: 4px solid #cbd5e0; padding: 10px; margin: 10px 0; font-style: italic;">
            {response_message}
        </blockquote>
        <hr style="border: 1px solid #eee;" />
        <p>You can view full details by logging into the CitiData Center Portal.</p>
        <br>
        <p>Best regards,<br><strong>CitiData Centre IT Support Team</strong></p>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_body, 'html'))

    # 3. Connect to Google's Mail Servers via STARTTLS (Port 587)
    try:
        print(f"Connecting to Gmail via STARTTLS (Port 587) to notify {to_email}...")
        
        # Switch to standard SMTP + port 587
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=10) as server:
            server.starttls()  # Upgrade the connection to secure encryption
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            print(f"SUCCESS: Notification email sent via Gmail to: {to_email}")
            
    except Exception as e:
        print(f"ERROR: Background email delivery failed. Reason: {e}")


def send_ticket_response_email(to_email, ticket_id, new_status, response_message):
    """
    Spawns a clean background thread so the admin dashboard page loads instantly.
    """
    email_thread = threading.Thread(
        target=_send_email_worker,
        args=(to_email, ticket_id, new_status, response_message)
    )
    email_thread.daemon = True
    email_thread.start()