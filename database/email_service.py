import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

def send_ticket_response_email(staff_email, ticket_id, status, response_message):
    """
    Send email notification when ticket is responded to
    """
    try:
        if not Config.EMAIL_ADDRESS or not Config.EMAIL_PASSWORD:
            print("Email credentials not configured")
            return False
            
        if not staff_email:
            print("Staff email not provided")
            return False
        
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
        message['From'] = Config.EMAIL_ADDRESS
        message['To'] = staff_email
        message['Subject'] = subject
        
        message.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP_SSL(Config.EMAIL_SMTP_SERVER, Config.EMAIL_SMTP_PORT) as server:
            server.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)
            server.send_message(message)
        
        print(f"Email sent to {staff_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False