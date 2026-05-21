from datetime import datetime

def create_ticket(name, department, category, description):
    """Create a new ticket object"""
    return {
        "id": None,  # Will be set when added to list
        "name": name,
        "department": department,
        "category": category,
        "description": description,
        "status": "Open",
        "date_created": str(datetime.now()),
        "date_resolved": None
    }

def create_order(name, food):
    """Create a new order object"""
    return {
        "name": name,
        "food": food
    }

def create_staff(name, email=""):
    """Create a new staff object"""
    return {
        "name": name,
        "email": email
    }