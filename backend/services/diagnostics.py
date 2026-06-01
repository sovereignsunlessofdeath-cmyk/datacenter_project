import os
import json
from database.db import load_data

def run_system_diagnostics():
    """
    Runs an automated suite of checks against the application's core resources.
    Returns a dictionary containing the status of each component.
    """
    results = {
        "status": "Healthy",
        "timestamp": True,
        "checks": {}
    }
    
    # 1. Test Database / JSON File Access
    try:
        data = load_data()
        # Verify core database keys exist
        required_keys = ["tickets", "staff", "ticket_categories", "orders"]
        missing_keys = [key for key in required_keys if key not in data]
        
        if missing_keys:
            results["checks"]["database"] = {
                "status": "Degraded",
                "message": f"data.json loaded, but missing structural keys: {missing_keys}"
            }
        else:
            results["checks"]["database"] = {
                "status": "Healthy",
                "message": f"Successfully read data.json. Found {len(data.get('tickets', []))} tickets and {len(data.get('staff', []))} staff members."
            }
    except Exception as e:
        results["checks"]["database"] = {
            "status": "Unhealthy",
            "message": f"CRITICAL: Failed to read database file. Error: {str(e)}"
        }

    # 2. Test Architecture Directory Structure
    critical_paths = {
        "Frontend Templates": "frontend/templates",
        "Frontend Static": "frontend/static",
        "Database Folder": "database",
        "Routes Folder": "backend/routes"
    }
    
    structure_errors = []
    for name, path in critical_paths.items():
        if not os.path.exists(path):
            structure_errors.append(f"Missing directory: {path}")
            
    if structure_errors:
        results["checks"]["file_structure"] = {
            "status": "Degraded",
            "message": f"Structure anomalies found: {', '.join(structure_errors)}"
        }
    else:
        results["checks"]["file_structure"] = {
            "status": "Healthy",
            "message": "All critical MVC architecture directories exist perfectly."
        }

    # 3. Test Email Notification Network Availability
    # We check if SMTP credentials exist in configuration without actually sending an email
    try:
        smtp_user = os.environ.get("SMTP_USER") or "Not Configured"
        if smtp_user == "Not Configured":
            results["checks"]["email_service"] = {
                "status": "Warning",
                "message": "SMTP credentials missing from environment variables. Email notifications will be skipped."
            }
        else:
            results["checks"]["email_service"] = {
                "status": "Healthy",
                "message": f"SMTP mail subsystem configured under user: {smtp_user}"
            }
    except Exception as e:
        results["checks"]["email_service"] = {
            "status": "Unhealthy",
            "message": f"Email service verification failed: {str(e)}"
        }

    # If any underlying check is not Healthy, downgrade the global status
    for check_name, check_data in results["checks"].items():
        if check_data["status"] in ["Unhealthy", "Degraded"]:
            results["status"] = "Unhealthy"
            break

    return results