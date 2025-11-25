# Import and create a db object:
from flask_sqlalchemy import SQLAlchemy

# Initialize the db object without passing the app instance yet (done in app.py)
db = SQLAlchemy()

# Models
class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Movie(db.Model):

    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String, nullable=False)

    # Link Movie to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # The ORM relationship
    # Relationship: Creates the 'user' attribute (movie.user) and the 'movies'
    # list on the User model (backref='movies').
    user = db.relationship('User', backref='movies')