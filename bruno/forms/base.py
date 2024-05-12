from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import Optional, DataRequired, Length


class CreateGameForm(FlaskForm):
    game_name = StringField('Game Name', validators=[DataRequired()])
    public = BooleanField('Public')
    password = PasswordField('Password', validators=[
                             Optional()])
    submit = SubmitField('Create Game')

    def __init__(self, *args, **kwargs):
        super(CreateGameForm, self).__init__(*args, **kwargs)
        if not self.game_name.data:
            self.game_name.data = f"{kwargs.get(
                'username', '')}'s Game"


class JoinGameForm(FlaskForm):
    hashed_game_id = StringField('Game Code', validators=[DataRequired(), Length(
        min=5, max=10, message="Game code must be between 5 and 10 characters long.")])
    submit = SubmitField('Join Game')
