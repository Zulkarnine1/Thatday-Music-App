from flask_sqlalchemy import SQLAlchemy

class DBConfig:

    def __init__(self, app):
        self.app = app


    def connect(self, link):
        try:
            self.app.config['SQLALCHEMY_DATABASE_URI'] = link
            self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            self.db = SQLAlchemy(self.app)
            return (self.db,self.app)
        except Exception as e:
            print(e)
            return None, self.app

