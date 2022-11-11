from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Calculations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tax = db.Column(db.String(1000))
    balance = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(20))
    calculations = db.relationship('Calculations')