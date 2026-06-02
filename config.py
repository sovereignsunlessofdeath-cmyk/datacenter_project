import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the application"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_change_this')
    DEBUG = True
    DATA_FILE = 'data.json'
    
    # Email settings (Updated to match your Render Secrets perfectly!)
    EMAIL_ADDRESS = os.getenv('SMTP_USER')
    EMAIL_PASSWORD = os.getenv('SMTP_PASSWORD')
    EMAIL_SMTP_SERVER = 'smtp.gmail.com'
    EMAIL_SMTP_PORT = 587  # Switched to 587 to match our secure background TLS setup
    
    # Admin credentials
    ADMIN_ACCOUNTS = {
        'Damilare@Citidata': 'Damilare',
        'Mr Godwin@Admin': 'Admin',
        'Mr Andie@Admin': 'Admin'
    }