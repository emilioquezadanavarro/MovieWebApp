# 🎬 MovieWeb App: Multi-User Movie Management

This project is a complete, multi-user web application built with Python and Flask. It demonstrates the full lifecycle of data management, from user creation and external API fetching to secure database interactions and elegant front-end display. The project applies strong software engineering principles, including Separation of Concerns and robust error handling.

<img width="1467" height="484" alt="Screenshot 2025-12-02 at 09 47 24" src="https://github.com/user-attachments/assets/afe46a35-1fd8-4934-9aef-b2b8fb558a67" />

# ✨ Key Features

- Multi-User Management: Users can be created and selected, and their data is isolated.

# Full CRUD (Create, Read, Update, Delete):

- Create: Fetches movie data from the OMDb API and saves the new record linked to the specific user.

- Read: Displays a personalized list of movies for the selected user.

- Update: Allows modification of the movie title (and can be extended for other fields).

- Delete: Removes a movie record from the user's list.

- Data Architecture (ORM): Uses Flask-SQLAlchemy with an efficient One-to-Many relationship between User and Movie models.

# Security & Efficiency:

- API Key is secured using environment variables (python-dotenv).

- Database operations use targeted ORM queries (no inefficient loading of the entire movie list).

- Robust Error Handling: Includes custom error pages for 404 (Not Found) and 500 (Internal Server Error), and uses Flask flash() for user feedback on API errors and invalid data.

- Aesthetics (Retro Style): Utilizes custom CSS for a consistent, high-contrast, digital retro/vaporwave aesthetic.

# 🛠️ Technology Stack

- Backend Framework: Python / Flask

- Database ORM: Flask-SQLAlchemy

- Database: SQLite3 (data/movies.db)

- Templating: Jinja2

- API: OMDb API (requests library)

- Dependencies: requests, SQLAlchemy, python-dotenv

# 🚀 Setup and Installation

# 1. Prerequisites

Python 3.x

An active virtual environment (python3 -m venv venv).

# 2. Installation

Clone the Repository:

git clone https://github.com/emilioquezadanavarro/MovieWebApp.git

Activate Environment and Install:

source venv/bin/activate  # macOS/Linux (or correct command for your shell)
pip install -r requirements.txt


# 3. API Key Configuration

Create .env file: In the root of your project directory, create a file named .env.

Add Key: Add your OMDb API key:

OMDB_API_KEY="YOUR_ACTUAL_OMDB_API_KEY_HERE"


# 4. Database Initialization

The application handles creating the schema automatically upon the first run, provided the /data folder exists.

# 5. Running the Application

python app.py

# 6. The application will be accessible at http://127.0.0.1:5000/.

# 🧭 Application Routes

# The MoviWeb application is structured around six RESTful routes:

- / (GET): Serves as the application's home screen, displaying a list of all registered users and the form to create a new user identity.

- /users (POST): Handles the form submission from the home page to add a new user record to the database.

- /users/<int:user_id>/movies (GET): The main display route. Loads the selected user's personalized list of movies.

- /users/<int:user_id>/movies (POST): Handles the form submission from the movie list page, fetching external data from the OMDb API and saving the new movie record to the user's list.

- /users/<int:user_id>/movies/<int:movie_id>/update (GET / POST): A combined route that displays the specific update form (GET) and processes the submission to modify the movie's title in the database (POST).

- /users/<int:user_id>/movies/<int:movie_id>/delete (POST): A secure, POST-only route used to remove a specific movie record from the database.

# 📝 License

This project was created for educational purposes at Masterschool.
