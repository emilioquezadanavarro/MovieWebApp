from models import db, User, Movie

class DataManager():
    """
    Manages all database interactions for the application using the SQLAlchemy ORM.
    Separates the data logic from the web application logic (app.py).

    """

    def create_user(self, name):
        """
        Adds a new User record to the database.
        Args:
            name (str): The name of the new user.

        """

        # Create a Python User object
        new_user = User(name=name)

        # Stage the object for insertion
        db.session.add(new_user)

        # Commit the changes
        db.session.commit()

    def get_users(self):
        """
        Retrieves all User records from the database.
        Returns:
            A list of all User objects.

        """
        # Query all User objects
        users = User.query.all()
        return users

    def get_movies(self, user_id):
        """
        Retrieves a specific User object and their list of movies.
        Args:
            user_id (int): The primary key ID of the user.
        Returns:
            tuple: (User object, list of Movie objects) or (None, []) if user is not found.

        """

        # Fetch the User by primary key
        user = User.query.get(user_id)

        if user:

            # Leverage the 'movies' attribute created by the backref relationship
            movies = user.movies
            return user, movies

        return None, []

    def add_movie(self, name, director, year, poster_url, user_id):
        """
        Adds a new Movie record to the database and links it to a user.
        Args:
            name (str): Movie title.
            director (str): Movie director.
            year (int): Release year.
            poster_url (str): URL to the movie poster.
            user_id (int): The ID of the owner (Foreign Key).

        """

        # Create the Movie object using all required attributes
        movie_to_add = Movie(name=name, director=director, year=year, poster_url=poster_url,user_id=user_id)

        # Stage and commit the changes
        db.session.add(movie_to_add)
        db.session.commit()

    def update_movie(self, movie_id, new_title):
        """
        Updates the name (title) of an existing movie.

        Args:
            movie_id (int): Primary key of the movie to update.
            new_title (str): The new title for the movie.
        Returns:
            bool: True if updated, False if movie not found.
        """

        # Find the movie by primary key.
        movie_to_update = Movie.query.get(movie_id)

        if movie_to_update:

            # Modify the attribute of the Python object
            movie_to_update.name = new_title

            # Commit the changes
            db.session.commit()
            return True

        return False

    def delete_movie(self, movie_id):
        """
        Deletes a movie record from the database.

        Args:
            movie_id (int): Primary key of the movie to delete.
        Returns:
            bool: True if deleted, False if movie not found.

        """

        # Find the movie by primary key
        movie_to_delete = Movie.query.get(movie_id)

        if movie_to_delete:

            # Stage the object for deletion
            db.session.delete(movie_to_delete)

            #Commit the changes
            db.session.commit()
            return True

        return False
