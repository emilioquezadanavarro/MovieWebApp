from flask import Flask
from data_manager import DataManager
from models import db, User, Movie
import os

# Setting up flask app
app = Flask(__name__)

# Setting up SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Link the database and the app. This is the reason you need to import db from models
db.init_app(app)

# Create an object of your DataManager class
data_manager = DataManager()

# Routes
@app.route('/')
def home():
    return "Welcome to MoviWeb App!"

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