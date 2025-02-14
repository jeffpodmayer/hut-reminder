from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import db, Hut, Availability, Reminder
from .routes.hut_routes import hut_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(hut_routes)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hut_reminder.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return "Hello, Flask!"

    return app
