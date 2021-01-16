from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    description = db.Column(db.Text())
    year_exp = db.Column(db.Integer)
    country = db.Column(db.String(3))
    location = db.Column(db.String(20))
    email = db.Column(db.String(100))
    services = db.Column(db.JSON)
    education = db.Column(db.JSON)
    experience = db.Column(db.JSON)
