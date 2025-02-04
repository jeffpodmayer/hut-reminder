from . import db

class Availability(db.Model):
    __tablename__ = 'availability'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    is_vacant = db.Column(db.Boolean, default=True, nullable=False)
    # Foreign Key
    hut_id = db.Column(db.Integer, db.ForeignKey('huts.id'), nullable=False) 