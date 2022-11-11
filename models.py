from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

def connect_db(app):
  db.app = app 
  db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(
        db.String,
        primary_key = True
    )
    password = db.Column(
        db.String,
        nullable = False
    )
    email = db.Column(
        db.String,
        nullable = False
    )
    first_name = db.Column(
        db.String,
        nullable = False
    )    
    last_name = db.Column(
        db.String,
        nullable = False
    )