from flask import request
from flask_restx import Resource, Namespace

from app.container import director_service
from app.dao.model.director import DirectorSchema
from app.decorators import admin_required, auth_required

director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        all_directors = director_service.get_all()
        return directors_schema.dump(all_directors), 200

    @admin_required
    def post(self):
        req_json = request.json
        director_service.create(req_json)
        return "", 201


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    @auth_required
    def get(self, did: int):
        try:
            director = director_service.get_one(did)
            return director_schema.dump(director), 200
        except Exception:
            return "", 404

    @admin_required
    def put(self, did: int):
        req_json = request.json
        director_service.update(did, req_json)
        return "", 204

    @admin_required
    def delete(self, did: int):
        director_service.delete(did)
        return "", 204

