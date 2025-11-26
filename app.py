from flask import Flask, render_template, request, flash, redirect, url_for
from data_manager import DataManager
from models import db, User, Movie
import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Constants for API
API_KEY = os.environ.get('OMDB_API_KEY')
API_URL = "http://omdbapi.com/"

# Setting up flask app
app = Flask(__name__)

# Setting up SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a_very_secret_key_for_flashing_messages'

# Link the database and the app. This is the reason you need to import db from models
db.init_app(app)

# Create an object of your DataManager class
data_manager = DataManager()

# Routes
@app.route('/')
def index():

    users = data_manager.get_users()
    return render_template('index.html', users=users)

@app.route('/users', methods=['POST'])
def add_user():

    # Retrieve the input name
    username = request.form.get('username')

    if username:

        data_manager.create_user(username)

        # Success message using flash function
        flash(f"The user '{username}' was successfully added")

        # Redirect the user to the GET Route
        return redirect(url_for('index'))

    else:
        # Name field is missing - display error
        flash('Field is mandatory.', 'error')
        return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):

    user, movies = data_manager.get_movies(user_id)

    if user is None:

        # Error message - display error
        flash(f"User not found!" , "error")

        # Redirect the user to the GET Route
        return redirect(url_for('index'))

    return render_template('movies.html',user=user ,movies=movies)

@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie_to_user():
    pass

@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie_title_on_user_list():
    pass

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie_on_user_list():
    pass

# Creating the data base with ORM
def create_database_tables():
    """Creates the database file and all tables defined in models."""
    print("Attempting to create database tables...")

    # db.create_all() MUST be called within the Flask Application Context
    # try/except block for robustness.
    try:
        with app.app_context():

            db.create_all()
            print("Database tables created or already exist.")

    except Exception as e:

        print(f"ERROR: Failed to create database tables. Reason: {e}")

# Standard Flask Run Block
if __name__ == '__main__':

    # Call the setup function to ensure the database file and tables are ready
    # This should be run at least once to initialize the tables, then comment it out.

    #create_database_tables() # <-- Comment this line out after first successful run

    app.run(host="127.0.0.1", port=5000, debug=True)