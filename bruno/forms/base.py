from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import Optional, DataRequired


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
