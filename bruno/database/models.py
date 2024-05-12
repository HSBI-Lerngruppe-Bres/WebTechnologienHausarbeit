from . import db
from flask_login import UserMixin


class Player(db.Model, UserMixin):
    __tablename__ = "player"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    owned_games = db.relationship('Game', backref='owner', lazy=True)

    def __repr__(self):
        return f'User(id={self.id}, name={self.name})'

    def get_id(self):
        return self.id


players_games = db.Table('players_games',
                         db.Column('game_id', db.Integer, db.ForeignKey(
                             'game.id'), primary_key=True),
                         db.Column('player_id', db.Integer, db.ForeignKey(
                             'player.id'), primary_key=True)
                         )


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(
        'player.id'), nullable=False)
    players = db.relationship(
        'Player', secondary=players_games, backref=db.backref('games', lazy='dynamic'))
    public = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'Game(id={self.id}, name={self.name})'
