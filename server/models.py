from flask_login import UserMixin


def load_class_User(db):

    class User(UserMixin,db.Model):
        __tablename__ = "user"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(250), nullable=False)
        username = db.Column(db.String(250), nullable=False, unique=True)
        password = db.Column(db.String(1000), nullable=False)
        img = db.Column(db.String(1000), nullable=False)

    return User