from flaskapp import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    reservations = db.relationship('Reservation', backref='user', lazy='dynamic')
    profile = db.relationship('Profile', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    birthday = db.Column(db.DateTime, default=datetime.utcnow)
    marital_status = db.Column(db.String(10))  # 'Single' or 'Married'
    gender = db.Column(db.String(10))  # 'Male', 'Female', or 'Other'
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    traveled_countries = db.Column(db.String(255))  # Could be a list or a string
    profile_picture = db.Column(db.String(255))  # Path to the image
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Profile for user {}, gender: {}, birthday: {}>'.format(self.user_id, self.gender, self.birthday)


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package = db.Column(db.String(120))
    arrival_date = db.Column(db.DateTime, default=datetime.utcnow)
    num_of_people = db.Column(db.Integer)
    boarding = db.Column(db.Boolean)
    sight_seeing = db.Column(db.Boolean)
    discount_coupon_used = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Reservation {}>'.format(self.id)
