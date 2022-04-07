from enum import unique
from pytz import timezone
from sqlalchemy.orm import backref
from sqlalchemy.sql.expression import nullslast
from datetime import datetime
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import time

# user note database
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# post user database
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=True)
    date_posted = db.Column(db.Text, nullable=False)
    img = db.Column(db.Text, unique=False, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    img1 = db.Column(db.Text, unique=False, nullable=False)
    name1 = db.Column(db.Text, nullable=False)
    mimetype1 = db.Column(db.Text, nullable=False)
    img2 = db.Column(db.Text, unique=False, nullable=False)
    name2 = db.Column(db.Text, nullable=False)
    mimetype2 = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    interests = db.relationship('Interest')


# internet service provider
class Internet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    os = db.Column(db.String(100), nullable=False)
    datetime_login = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# post of interest
class Interest(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post_user = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# user information
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    contact = db.Column(db.Text)
    password = db.Column(db.String(150))
    img = db.Column(db.Text, unique=False, nullable=True)
    name = db.Column(db.Text, nullable=True)
    mimetype = db.Column(db.Text, nullable=True)
    notes = db.relationship('Note')
    posts = db.relationship('Post')
    interests = db.relationship('Interest')
    internet = db.relationship('Internet')


