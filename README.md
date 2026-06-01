# Data Centre Management System

A web-based application for managing food orders and IT support tickets at a data centre.

## Features

✅ **Food Order System**
- Staff can order food for the next day
- Search and filter menu items by popularity
- Admin can view all orders and manage the menu

✅ **IT Helpdesk Ticketing System**
- Staff submit support tickets for IT issues
- Admin responds to tickets with email notifications
- Track ticket status (Open → In Progress → Resolved)
- Manage ticket categories

✅ **User Management**
- Admin login with credentials
- Staff login with name and email registration
- Profile management for staff

## Project Structure

datacenter_project/
│
├── config.py                 # Central environment and application configurations
├── requirements.txt          # Python dependencies
├── wsgi.py                   # Production gateway entry point for Render (Gunicorn)
│
├── backend/                  # --- BACKEND CORE LAYER ---
│   ├── __init__.py           # Initializes the Flask app & registers blueprints
│   │
│   ├── routes/               # --- CONTROLLERS / ROUTING LAYER ---
│   │   ├── auth.py           # Login/logout routes
│   │   ├── orders.py         # Food order routes
│   │   ├── tickets.py        # IT ticket routes
│   │   ├── admin.py          # Admin dashboard core
│   │   └── settings.py       # Settings and system management
│   │
│   └── services/             # --- SERVICE LAYER ---
│       └── email_service.py  # SMTP email transmission worker logic
│
├── database/                 # --- DATA PERSISTENCE LAYER ---
│   ├── data.json             # Flat-file database storage 
│   ├── db.py                 # Core file read/write logic (load_data, save_data)
│   └── models.py             # Data constructors (create_ticket, create_order)
│
└── frontend/                 # --- FRONTEND PRESENTATION LAYER ---
    ├── static/               # Browser assets (CSS, UI Images, JS scripts)
    │   ├── css/
    │   └── js/
    └── templates/            # Clean UI view templates
        ├── index.html
        ├── login_admin.html
        ├── login_staff.html
        └── ...
        
## Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS
- **Database:** JSON (data.json)
- **Email:** SMTP (Gmail)
- **Deployment:** Render

## Installation

### Requirements
- Python 3.14.4+
- Flask 3.1.3
- Werkzeug 3.1.8
- python-dotenv 1.0.0

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/sovereignsunlessofdeath-cmyk/datacenter_project.git
cd datacenter_project

Install dependencies
pip install --break-system-packages -r requirements.txt

Create .env file
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

Run the Application
python app.py

Access the app
Open browser: http://localhost:5000
Admin login: Damilare@Citidata / Damilare
Staff login: Any staff name (e.g., "Damilare")
Admin Credentials
Username
Password
Damilare@Citidata
Damilare
Mr Godwin@Admin
Admin
Mr Andie@Admin
Admin
Features Walkthrough
Staff User
Login → Enter name → Add email (first time only)
Order Food → Search menu → Select food → Submit
Submit Ticket → Describe issue → Submit
Profile → Update email
Admin User
Dashboard → View tomorrow's orders
Manage Staff → Add/remove staff members
Manage Menu → Add/remove food items
View Tickets → Respond to tickets → Send emails
View Orders → History of all orders
Email Notifications
When admin responds to a ticket:
Staff receives email with ticket response
Email includes ticket ID, status, and response message
Staff can then log in to view details
Deployment
The project is deployed on Render.com:
Live URL: https://datacenter-project.onrender.com
Auto-deployment: Pushes to GitHub automatically trigger redeploy

Deploy Updates
git add .
git commit -m "Your message"
git push origin main
Wait 2-3 minutes for automatic deployment.

Project Author
Damilare - SIWES Intern at CitiData Centre
Date Created
May 2026
Notes
Data is stored in JSON format (suitable for small projects)
For production, consider using a real database (PostgreSQL, MongoDB)
Email requires Gmail App Password (not regular password)
Free Render instance may have 50-second startup delay

Last Updated: May 21, 2026
Save this as `README.md` in your `datacenter_project` folder.

Now push to Git:
git add .
git commit -m "Add comprehensive README documentation"
git push origin main

Done!