import json
import os

# This looks up the exact folder where db.py lives, then points one level up to the root project folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, 'data.json')

def load_data():
    """Load data from data.json safely using absolute system paths"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        "staff": [],
        "menu": [],
        "orders": {},
        "tickets": [],
        "ticket_categories": ["Network Issue", "Hardware Problem", "Software Bug", "Password Reset", "Other"]
    }

def save_data(data):
    """Save data to data.json"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_staff_by_name(data, name):
    """Find staff member by name"""
    for staff in data.get('staff', []):
        if staff['name'] == name:
            return staff
    return None

def get_ticket_by_id(data, ticket_id):
    """Find ticket by ID"""
    for ticket in data.get('tickets', []):
        if ticket['id'] == ticket_id:
            return ticket
    return None