# Data Centre Management System 🚀

A comprehensive, web-based internal management portal built for managing daily food orders and IT support tickets at the **PetrodatCentre** facility in Magboro, Ogun State. 

This system helps streamline facility operations by providing a lightweight interface for staff requests and an administrative hub for ticket management with automated background email communication.

---

## ✨ Features

### 🍔 Food Order System
* **Pre-ordering Infrastructure:** Staff can submit food orders efficiently for the following work day.
* **Menu Discovery:** Search and filter active menu options by popularity indicators.
* **Kitchen Dashboard:** Administrators can view aggregated daily order reports and real-time menu availability controls.

### 🎫 IT Helpdesk Ticketing System
* **Issue Submission:** Staff can log operational IT or facility tickets with varying categories.
* **Non-Blocking Notifications:** When administrators resolve or update a ticket, an asynchronous, threaded email process uses a secure connection (TLS Port 587) to send updates straight to the staff member's inbox instantly without locking up the user interface.
* **State Tracking:** Track ticket workflows seamlessly from `Open` ➔ `In Progress` ➔ `Resolved`.

### 👥 User & Profile Management
* **Dual-Authentication Core:** Custom logic separating access layers for General Facility Staff vs. Authenticated Management Admins.
* **Profile Syncing:** Staff register instantly via name and maintain up-to-date contact details via an interactive profile console.

---

## 📁 Project Structure

```text
datacenter_project/
│
├── config.py                 # Central environment and application configurations
├── requirements.txt          # Python application dependencies
├── wsgi.py                   # Production gateway entry point for Gunicorn
│
├── backend/                  # --- BACKEND CORE LAYER ---
│   ├── __init__.py           # Initializes the Flask app & registers blueprints
│   │
│   ├── routes/               # --- CONTROLLERS / ROUTING LAYER ---
│   │   ├── auth.py           # Login and logout authentication pipelines
│   │   ├── orders.py         # Food order creation and processing routes
│   │   ├── tickets.py        # IT ticket workflow lifecycle routes
│   │   ├── admin.py          # Admin dashboard aggregator logic
│   │   └── settings.py       # Settings and system management configurations
│   │
│   └── services/             # --- SERVICE LAYER ---
│       └── email_service.py  # Asynchronous non-blocking SMTP email pipeline
│
├── database/                 # --- DATA PERSISTENCE LAYER ---
│   ├── data.json             # Flat-file database storage engine
│   ├── db.py                 # File I/O serialization logic (load_data/save_data)
│   └── models.py             # Struct data constructors (create_ticket/create_order)
│
└── frontend/                 # --- FRONTEND PRESENTATION LAYER ---
    ├── static/               # Browser client assets (CSS, UI Images, JS scripts)
    │   ├── css/
    │   └── js/
    └── templates/            # Clean UI Jinja2 view templates
        ├── index.html
        ├── login_admin.html
        ├── login_staff.html
        └── ...

🛠️ Technologies Used
Backend Engine: Python, 
FlaskFrontend Design: HTML, CSS
Database Ledger: Structured JSON Flat File (data.json)
Transport Protocol: SMTP (Gmail Secure TLS Layer)
Cloud Infrastructure: Render (Automated Delivery Web Worker)

⚙️ Installation & Local Setup
System Prerequisites
Python 3.10+
Flask 3.1.3
Werkzeug 3.1.8
python-dotenv

Step-by-Step Environment Run
1. Clone the Repository:

Bash

git clone [https://github.com/sovereignsunlessofdeath-cmyk/datacenter_project.git](https://github.com/sovereignsunlessofdeath-cmyk/datacenter_project.git)
cd datacenter_project

2. Install Application Dependencies:
Bashpip install -r requirements.txt
(Note: Use pip install --break-system-packages -r requirements.txt if your operating system explicitly requires an external system flag).

3. Establish a Local Configuration File:
Create a file named .env in the root directory of the project and insert your development credentials:

Plaintext

SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_16_character_app_password

4. Execute the Application:

Bash

python config.py

Open your browser and navigate to: http://localhost:5000

🔐 Administrative Access Controls
The following credentials grant full administrative authorization to the core control dashboards:
Administrative Username      Password
Damilare@Citidata            Damilare
Mr Godwin@Admin              Admin
Mr Andie@Admin               Admin

🚀 Production Deployment on Render
This portal is structured to run live inside a Render Web Service environment container.

💼 Secure Secrets Management
To prevent sensitive email accounts and application vectors from being checked into open source repositories on GitHub, the production app uses Render's Secret Files:
1.Open your Render Dashboard and select your service.
2.Go to the Environment tab on the left-hand menu.
3.Click Create Secret File.
4.Set the filename explicitly to .env.
5.Paste your production variables inside the content section:

Plaintext

SMTP_USER=oluwadamilareoshodi@gmail.com
SMTP_PASSWORD=xygvjsqazmqywmtv

6. Click Save Changes. This instantly fires off a rolling, secure update.

📦 Quick Version Control Deployment Flow
Any changes pushed directly to your source control repository will automatically coordinate a fresh, updated container build on Render:

Bash

git add .
git commit -m "doc: refine system readme architecture"
git push origin main

📝 Authors & Project MetadataProject Author:

 Damilare – SIWES Intern at CitiData CentreDevelopment Date: May 2026Database Note: Data persistence is structured on optimized flat JSON formatting suitable for facility prototyping. Future scaling operations can transition the data layer to a managed PostgreSQL cluster natively.