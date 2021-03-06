from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy import desc, Index
class TSVector(sa.types.TypeDecorator):
    impl = TSVECTOR

LIKES = None
SAVED = None

def get_LIKES_table(db):
    global LIKES
    LIKES = db.Table("likes",
                     db.Column("uid",db.Integer, db.ForeignKey("user.id")),
                     db.Column("card_id",db.Integer, db.ForeignKey("card.id")))
    return LIKES


def get_SAVED_table(db):
    global SAVED
    SAVED = db.Table("saves",
                     db.Column("uid",db.Integer, db.ForeignKey("user.id")),
                     db.Column("card_id",db.Integer, db.ForeignKey("card.id")))
    return SAVED


def load_class_User(db):

    class User(UserMixin,db.Model):
        __tablename__ = "user"
        id = db.Column(db.Integer, primary_key=True, unique=True)
        name = db.Column(db.String(250), nullable=False)
        username = db.Column(db.String(250), nullable=False, unique=True)
        password = db.Column(db.String(1000), nullable=False)
        img = db.Column(db.String(1000), nullable=False)
        moto = db.Column(db.String(80), nullable=False)
        liked_cards = db.relationship("Card", secondary=LIKES, backref=db.backref("users_liked",lazy="dynamic"))
        saved_cards = db.relationship("Card", secondary=SAVED, backref=db.backref("users_saved",lazy="dynamic"))


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

        __ts_vector__ = db.Column(TSVector(),db.Computed("to_tsvector('english', title || ' ' || quote)",persisted=True))
        __table_args__ = (Index('ix_card___ts_vector__',__ts_vector__, postgresql_using='gin'),)




    return Card