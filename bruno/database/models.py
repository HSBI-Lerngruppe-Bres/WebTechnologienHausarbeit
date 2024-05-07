from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __columnname__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    usertype_id = db.Column(db.Integer, db.ForeignKey('usertype.id'), nullable=True)
        
    def __repr__(self):
        return f'User{self.username}'

    def get_id(self):
        return self.id
    
class UserType(db.Model):
    __tablename__ = 'usertype'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True)
    users = db.relationship('User', backref='usertype', lazy=True)