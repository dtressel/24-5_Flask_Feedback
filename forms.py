from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo

class UserRegistrationForm(FlaskForm):
    """Form to register a user."""

    username = StringField("Username", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email(message="Must be a valid email address.")])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, message="Must be at least 8 characters.")])
    password_confirm = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo(fieldname="password", message="Passwords do not  match.")])

class UserLoginForm(FlaskForm):
    """Form to login user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])