import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the application"""
    SECRET_KEY = 'your_secret_key_change_this'
    DEBUG = True
    DATA_FILE = 'data.json'
    
    # Email settings
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_SMTP_SERVER = 'smtp.gmail.com'
    EMAIL_SMTP_PORT = 465
    
    # Admin credentials
    ADMIN_ACCOUNTS = {
        'Damilare@Citidata': 'Damilare',
        'Mr Godwin@Admin': 'Admin',
        'Mr Andie@Admin': 'Admin'
    }