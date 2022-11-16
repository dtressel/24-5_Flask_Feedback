from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
  db.app = app 
  db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(
        db.String(20),
        primary_key = True
    )
    password = db.Column(
        db.String,
        nullable = False
    )
    email = db.Column(
        db.String(50),
        nullable = False
    )
    first_name = db.Column(
        db.String(30),
        nullable = False
    )    
    last_name = db.Column(
        db.String(30),
        nullable = False
    )
    feedbacks = db.relationship('Feedback', cascade="all, delete")

    @classmethod
    def create_user(cls, username, password, email, first_name, last_name):
        """Creates user after successful registration."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')

        return cls(
            username=username,
            password=hashed_utf8,
            email=email,
            first_name=first_name,
            last_name=last_name
            )

    @classmethod
    def authenticate_user(cls, username, password):
        """Authenticates user on log in and returns user instance"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
        )
    title = db.Column(
        db.String(100),
        nullable = False,
    )
    content = db.Column(
        db.String,
        nullable = False
    )
    username = db.Column(
        db.String,
        db.ForeignKey('users.username'),
        nullable = False
    )
    user = db.relationship('User')