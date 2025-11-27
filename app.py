from flask import Flask, render_template, request, flash, redirect, url_for
from data_manager import DataManager
from models import db, User, Movie
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import requests

# Load the environment variables from .env file
load_dotenv()

# Constants for API
API_KEY = os.environ.get('OMDB_API_KEY')
API_URL = "http://omdbapi.com/"

# Helper function for API calls
def fetch_movie_data(title):
    """
    Fetches data for a movie from OMDb.
    """

    try:

        params = {
            "t": title,
            "apikey": API_KEY
        }
        response = requests.get(API_URL, params=params)
        response.raise_for_status() # Raise an error in case of 404, 500

        data = response.json()

        #Check if API found the movie
        if data.get('Response') == 'True':
            return data
        else:
            print("No movie data found")
            return None

    except requests.exceptions.RequestException as e:
        # Handle network errors
        print(f"Connection error: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Could not decode API response")
        return None

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
def add_movie_to_user(user_id):

    movie_title_input = request.form.get('movie_title')
    movie_data = fetch_movie_data(movie_title_input)

    if movie_data is None:
        flash("Movie not found or API error.", 'error')
        return redirect(url_for('user_movies', user_id=user_id))

    try:
        name = movie_data.get('Title')
        director = movie_data.get('Director')
        year = int(movie_data.get('Year'))

        # Validation Check to ensure year is reasonable
        if year < 1888 or year > datetime.now().year:

            # We raise a ValueError so the execution jumps to the except block
            raise ValueError("Year is out of range")  # Custom error for invalid year range

        poster_url = movie_data.get('Poster')

        # Handle N/A poster data
        if poster_url == 'N/A':
            poster_url = 'https://via.placeholder.com/200x300?text=No+Poster'

    except (ValueError, TypeError):
        # Catches failures from int() conversion OR our custom ValueError
        flash("Error: Movie data received from API was invalid or year is outside a valid range", 'error')
        return redirect(url_for('user_movies', user_id=user_id))

    # Save to database using DataManager
    data_manager.add_movie(name, director, year, poster_url,user_id)

    # Success feedback
    flash(f"Movie '{name}' added successfully!", 'success')

    # Redirect to the GET route
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['GET','POST'])
def update_movie_title_on_user_list(user_id, movie_id):

    # Fetch data for display (GET) or verification (POST)
    user, movies = data_manager.get_movies(user_id)

    if user is None:
        flash("User not found", 'error')
        return redirect(url_for('index'))

    # Using next function to find the match and stops immediately. Otherwise, returns None
    movie_to_update = next((m for m in movies if m.id == movie_id), None)

    if movie_to_update is None:
        flash("Movie not found in this user's list.", 'error')
        return redirect(url_for('user_movies', user_id=user_id))

    # --- Handle POST Request (Form Submission) ---
    if request.method == 'POST':
        new_title = request.form.get('new_title')

        if not new_title:
            flash("New title cannot be empty.", 'error')
            return redirect(url_for('user_movies', user_id=user_id))

        # Call DataManager to update the record
        success = data_manager.update_movie(movie_id, new_title)

        if success:
            flash(f"Movie '{new_title}' updated successfully!", 'success')
        else:
            flash("Error updating movie.", 'error')

        # Redirect back to the movie list
        return redirect(url_for('user_movies', user_id=user_id))

    # --- Handle GET Request (Display Form) ---
    # If not a POST, render the form using the fetched movie data
    return render_template('update_movie.html', user=user, movie=movie_to_update)

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