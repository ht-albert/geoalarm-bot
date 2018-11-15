
from geoalarm.app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    tg_id = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.username

    def create(user):
        pass
