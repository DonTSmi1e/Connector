from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(50))
    description = db.Column(db.String(200))
    admin = db.Column(db.Integer)
    ban = db.Column(db.Integer)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer)
    title = db.Column(db.String(30))
    content = db.Column(db.String(1500))
    active = db.Column(db.DateTime)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)
    content = db.Column(db.String(100))
