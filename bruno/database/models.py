from . import db
from flask_login import UserMixin
from datetime import datetime, timezone


class Player(db.Model, UserMixin):
    __tablename__ = "player"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey(
        'game.id'))
    is_game_owner = db.Column(db.Boolean, default=False, nullable=False)
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
    joinable = db.Column(db.Boolean, default=True, nullable=False)
    settings_starting_card_amount = db.Column(db.Integer, default=7)
    settings_black_card_finish = db.Column(db.Boolean, default=True)
    settings_black_on_black = db.Column(db.Boolean, default=False)
    settings_plus_two_stacking = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'Game(id={self.id}, name={self.name})'


class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Integer, nullable=True)
    type = db.Column(db.String(20), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Card(id={self.id}, color={self.color}, value={self.value}, type={self.type})'
