from flask import Flask
from config import Config
from routes import auth, orders, tickets, admin, settings

app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(orders.bp)
app.register_blueprint(tickets.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(settings.bp)

if __name__ == '__main__':
    app.run(debug=True)