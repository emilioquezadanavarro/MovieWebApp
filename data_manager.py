from models import db, User, Movie

class DataManager():

    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        pass

    def get_movies(self, user_id):
        pass

    def add_movie(self, movie):
        pass

    def update_movie(self, movie_id, new_title):
        pass

    def delete_movie(self, movie_id):
        pass
