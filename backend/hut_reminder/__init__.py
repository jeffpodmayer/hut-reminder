from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Hut, Availability, Reminder


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hut_reminder.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    print(Hut.__tablename__)
    print(Availability.__tablename__)
    print(Reminder.__tablename__)
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)
