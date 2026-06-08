import os
import threading
import resend

# Initialize Resend using the Secret Key we set up on Render
resend.api_key = os.environ.get("RESEND_API_KEY")

def _send_email_worker(to_email, ticket_id, new_status, response_message):
    """
    Background worker that connects to Resend's API over HTTP (Port 443).
    Bypasses Render's firewall completely.
    """
    if not resend.api_key:
        print("LOG: Email notification skipped. RESEND_API_KEY is not configured.")
        return

    # Crafting clean HTML body for the staff member's email
    html_body = f"""
    <h2>Hello,</h2>
    <p>An IT Administrator has updated the status of your support ticket <strong>#{ticket_id}</strong>.</p>
    <hr style="border: 1px solid #eee;" />
    <p><strong>[Current Status]:</strong> <span style="color: #2b6cb0;">{new_status}</span></p>
    <p><strong>[Admin Response]:</strong></p>
    <blockquote style="background: #f7fafc; border-left: 4px solid #cbd5e0; padding: 10px; margin: 10px 0;">
        {response_message}
    </blockquote>
    <hr style="border: 1px solid #eee;" />
    <p>You can view full details by logging into the CitiData Center Portal.</p>
    <br>
    <p>Best regards,<br><strong>CitiData Centre IT Support Team</strong></p>
    """

    try:
        print(f"Connecting to Resend API to notify {to_email}...")
        resend.Emails.send({
            "from": "CitiData Helpdesk <onboarding@resend.dev>",
            "to": to_email,
            "subject": f"Update on your IT Support Ticket #{ticket_id} [{new_status}]",
            "html": html_body
        })
        print(f"SUCCESS: Notification email sent via Resend to: {to_email}")
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
