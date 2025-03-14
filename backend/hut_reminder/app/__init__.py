from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import db, Hut, Availability, Reminder
from .routes.hut_routes import hut_routes
from .routes.reminder_routes import reminder_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(hut_routes)
    app.register_blueprint(reminder_bp)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hut_reminder.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()

    @app.route('/')
    def home():
        return "Hello, Flask!"

# Debug: Print all registered routes
    print("Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")
    return app
