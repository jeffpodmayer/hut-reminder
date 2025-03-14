from . import db

class Hut(db.Model):
    __tablename__ = 'huts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)