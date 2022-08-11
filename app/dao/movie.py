from flask import request
from app.dao.model.movie import Movie

class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, mid):
        """ Возврат фильмов по id """
        return self.session.query(Movie).filter(Movie.id == mid).one()

    def get_all(self):
        """ Возврат фильмов по условиям """
        movies_query = self.session.query(Movie)
        args = request.args

        director_id = args.get('director_id')
        if director_id is not None:
            movies_query = self.session.query(Movie).filter(Movie.director_id == director_id)
        genre_id = args.get('genre_id')
        if genre_id is not None:
            movies_query = self.session.query(Movie).filter(Movie.genre_id == genre_id)
        year = args.get('year')
        if year is not None:
            movies_query = self.session.query(Movie).filter(Movie.year == year)

        movies = movies_query.all()

        return movies

    def create(self, data):
        """ Внесение в список нового фильма """
        new_movie = Movie(**data)
        self.session.add(new_movie)
        self.session.commit()
        return new_movie

    def update(self, update_movie):
        """ Обновление данных по фильму """
        self.session.add(update_movie)
        self.session.commit()
        return update_movie

    def delete(self, mid):
        """ Удаление фильма из списка по id """
        movie = self.session.query(Movie).filter(Movie.id == mid).first()
        if not movie:
            return "", 404
        self.session.delete(movie)
        self.session.commit()
        return "Ok", 204
