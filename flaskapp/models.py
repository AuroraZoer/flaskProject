from flaskapp import db
from datetime import datetime


class User(db.Model):
    full_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), primary_key=True)
    reservations = db.relationship('Reservation', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {} with email {}>'.format(self.username, self.email)


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), db.ForeignKey('user.email'))
    package = db.Column(db.String(120))
    arrival_date = db.Column(db.DateTime, default=datetime.utcnow)
    num_of_people = db.Column(db.Integer)
    boarding = db.Column(db.Boolean)
    sight_seeing = db.Column(db.Boolean)
    discount_coupon_used = db.Column(db.Boolean)

    def __repr__(self):
        return '<Reservation {} for {}>'.format(self.id, self.user_email)

