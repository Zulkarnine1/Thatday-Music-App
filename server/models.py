from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

def load_class_User(db):

    class User(UserMixin,db.Model):
        __tablename__ = "user"
        id = db.Column(db.Integer, primary_key=True, unique=True)
        name = db.Column(db.String(250), nullable=False)
        username = db.Column(db.String(250), nullable=False, unique=True)
        password = db.Column(db.String(1000), nullable=False)
        img = db.Column(db.String(1000), nullable=False)

    return User


def load_class_Playlist(db):

    class Playlist(db.Model):
        __tablename__ = "playlist"
        id = db.Column(db.Integer, primary_key=True, unique=True)
        date = db.Column(db.String(250), nullable=False, unique=True)
        link = db.Column(db.String(5000), nullable=False)

    return Playlist


def load_class_Card(db):

    class Card(db.Model):
        __tablename__ = "card"
        id = db.Column(db.Integer, primary_key=True, unique=True)
        title = db.Column(db.String(5000), nullable=False)
        dateformatted = db.Column(db.String(500), nullable=False)
        date = db.Column(db.String(250), nullable=False)
        by = db.Column(db.String(250), nullable=False)
        playlist = db.Column(db.String(5000), nullable=False)
        quote = db.Column(db.String(250), nullable=False)
        img = db.Column(db.String(5000), nullable=False)
        likes = db.Column(db.Integer, nullable=False)
        children = relationship("User")
        creator = db.Column(db.Integer,  ForeignKey("user.id"),nullable=False)

    return Card