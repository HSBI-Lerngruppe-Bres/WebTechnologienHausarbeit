from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    usertype_id = db.Column(
        db.Integer, db.ForeignKey('usertype.id'), nullable=True)
    owned_games = db.relationship('Game', backref='owner', lazy=True)

    def __repr__(self):
        return f'User{self.username}'

    def get_id(self):
        return self.id


class UserType(db.Model):
    __tablename__ = 'usertype'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True)
    users = db.relationship('User', backref='usertype', lazy=True)

    def __repr__(self):
        return f'UserType(name={self.name})'


players_games = db.Table('players_games',
                         db.Column('game_id', db.Integer, db.ForeignKey(
                             'game.id'), primary_key=True),
                         db.Column('user_id', db.Integer, db.ForeignKey(
                             'user.id'), primary_key=True)
                         )


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    players = db.relationship(
        'User', secondary=players_games, backref=db.backref('games', lazy='dynamic'))
    public = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'Game(id={self.id}, title={self.name})'
