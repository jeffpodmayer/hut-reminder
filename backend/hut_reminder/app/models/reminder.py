from . import db

reminder_hut = db.Table('reminder_hut',
    db.Column('reminder_id', db.Integer, db.ForeignKey('reminders.id'), primary_key=True),
    db.Column('hut_id', db.Integer, db.ForeignKey('huts.id'), primary_key=True)
)

class Reminder(db.Model):
    __tablename__ = 'reminders'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    # Many to many relationship with huts
    huts = db.relationship('Hut', secondary=reminder_hut, backref=db.backref('reminders', lazy='dynamic'))