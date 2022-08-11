from flask import request
from flask_restx import Resource, Namespace

from app.container import movie_service
from app.dao.model.movie import MovieSchema
from app.decorators import admin_required, auth_required

movie_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@movie_ns.route('/')
class MoviesView(Resource):
    @auth_required
    def get(self):

        movies = movie_service.get_all()

        return movies_schema.dump(movies), 200

    @admin_required
    def post(self):
        req_json = request.json
        movie_service.create(req_json)
        return "", 201

@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    @auth_required
    def get(self, mid: int):
        try:
            movie = movie_service.get_one(mid)
            return movie_schema.dump(movie), 200
        except Exception:
            return "", 404

    @admin_required
    def put(self, mid: int):
        req_json = request.json
        movie_service.update(mid, req_json)
        return "", 204

    @admin_required
    def delete(self, mid: int):
        movie_service.delete(mid)
        return "", 204
