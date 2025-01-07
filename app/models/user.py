""" user Data """
from app.extension import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    hashed_password = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
