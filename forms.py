from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, EqualTo

class UserRegistrationForm(FlaskForm):
    """Form to register a user."""

    username = StringField("Username", validators=[
        InputRequired(),
        Length(max=20, message="Must be less than 20 characters.")
        ])
    email = StringField("Email", validators=[
        InputRequired(),
        Email(message="Must be a valid email address."),
        Length(max=50, message="Must be less than 50 characters.")
        ])
    first_name = StringField("First Name", validators=[
        InputRequired(),
        Length(max=30, message="Must be less than 30 characters.")
        ])
    last_name = StringField("Last Name", validators=[
        InputRequired(),
        Length(max=30, message="Must be less than 30 characters.")
        ])
    password = PasswordField("Password", validators=[
        InputRequired(),
        Length(min=8, message="Must be at least 8 characters.")
        ])
    password_confirm = PasswordField("Confirm Password", validators=[
        InputRequired(),
        EqualTo(fieldname="password", message="Passwords do not  match.")
        ])

class UserLoginForm(FlaskForm):
    """Form to login user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Form to create feedback."""

    title = StringField("title", validators=[
        InputRequired(),
        Length(max=100, message="Must be less than 100 characters.")
        ])
    content = TextAreaField("content", validators=[InputRequired()])