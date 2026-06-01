from flask import Flask
import os
from config import Config

# 1. These are your new clean architectural imports!
from backend.routes.auth import bp as auth_bp
from backend.routes.tickets import bp as tickets_bp
from backend.routes.orders import bp as orders_bp
from backend.routes.admin import bp as admin_bp
from backend.routes.settings import bp as settings_bp

def create_app():
    # Tell Flask exactly where your new frontend assets and HTML files live
    app = Flask(__name__, 
                template_folder='frontend/templates', 
                static_folder='frontend/static')
    
    app.config.from_object(Config)

    # 2. Register your modular blueprints with the main app instance
    app.register_blueprint(auth_bp)
    app.register_blueprint(tickets_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(settings_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)