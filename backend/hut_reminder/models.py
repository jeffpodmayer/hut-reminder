from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Hut Table
class Hut(db.Model):
  __tablename__ = 'huts'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  # DB Relationship
  availability = db.relationship('Availability', backref='hut', lazy=True)
  reminders = db.relationship('Reminder', backref='hut',lazy=True)


# Availabilty Table
class Availability(db.Model):
  __tablename__ = 'availability'
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date, nullable=False)
  is_vacant = db.Column(db.Boolean, default=True, nullable=False)
  # Foreign Key
  hut_id = db.Column(db.Integer, db.ForeignKey('huts.id'), nullable=False)


# Reminder Table
class Reminder(db.Model):
  __tablename__ = 'reminders'
  id = db.Column(db.Integer, primary_key=True)
  user_email = db.Column(db.String(120), nullable=False)
  start_date = db.Column(db.Date, nullable=False)
  end_date = db.Column(db.Date, nullable=False)
  # Foreign Key
  hut_id = db.Column(db.Integer, db.ForeignKey('huts.id'), nullable=False)

