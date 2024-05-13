from . import db
from flask_login import UserMixin
from datetime import datetime, timezone


class Player(db.Model, UserMixin):
    __tablename__ = "player"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey(
        'game.id'))
    last_active = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'Player(id={self.id}, name={self.name})'

    def get_id(self):
        return self.id


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    public = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'Game(id={self.id}, name={self.name})'
