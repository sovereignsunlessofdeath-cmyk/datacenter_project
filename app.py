from flask import Flask
import os

# 1. Initialize the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "super_secret_local_key_12345")

# 2. Import the individual feature Controllers (Blueprints)
from routes.auth import bp as auth_bp
from routes.tickets import bp as tickets_bp
from routes.orders import bp as orders_bp
from routes.admin import bp as admin_bp
from routes.settings import bp as settings_bp

# 3. Register the Blueprints so the web links work
app.register_blueprint(auth_bp)
app.register_blueprint(tickets_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(settings_bp)

if __name__ == "__main__":
    # Local development runner configuration
    app.run(debug=True, host="0.0.0.0", port=5000)