import os
import json
import threading
import urllib.request
import urllib.error

def _send_email_worker(to_email, ticket_id, new_status, response_message):
    """
    Background worker that routes notifications using Brevo's Web API over Port 443.
    Bypasses Render's outbound SMTP firewall blocks effortlessly.
    """
    api_key = os.environ.get("BREVO_API_KEY")
    sender_email = "oluwadamilareoshodi@gmail.com"  # Your verified sender email

    if not api_key:
        print("LOG: Email notification skipped. BREVO_API_KEY is missing from environment variables.")
        return

    # 1. Build Brevo's expected JSON payload structure
    payload = {
        "sender": {"name": "CitiData Helpdesk", "email": sender_email},
        "to": [{"email": to_email}],
        "subject": f"Update on your IT Support Ticket #{ticket_id} [{new_status}]",
        "htmlContent": f"""
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
    }

    # 2. Package the HTTP Request over secure Port 443
    url = "https://api.brevo.com/v3/smtp/email"
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('api-key', api_key)
    req.add_header('Content-Type', 'application/json')

    try:
        print(f"Routing secure web API mail request via Brevo to notify {to_email}...")
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status in [200, 201, 202]:
                print(f"SUCCESS: Notification email sent via Brevo API web stream to: {to_email}")
            else:
                print(f"LOG: Brevo responded with status code: {response.status}")
                
    except urllib.error.HTTPError as http_err:
        error_body = http_err.read().decode('utf-8')
        print(f"ERROR: Brevo Web API delivery failed. Status {http_err.code}: {error_body}")
    except Exception as e:
        print(f"ERROR: Web routing email fallback failed. Reason: {e}")


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