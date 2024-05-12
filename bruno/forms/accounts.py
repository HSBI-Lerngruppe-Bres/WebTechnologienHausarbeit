from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class CreateUserForm(FlaskForm):
    """The login form
    """
    username = StringField('Player Name', validators=[
                           DataRequired(), Length(min=4, max=20)])
    submit = SubmitField('Login')
