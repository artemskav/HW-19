from flask import request
from flask_restx import Resource, Namespace

from app.container import user_service
from app.dao.model.user import UserSchema
from app.decorators import admin_required, auth_required

user_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/')
class UsersView(Resource):
    @auth_required
    def get(self):
        all_users = user_service.get_all()
        return users_schema.dump(all_users), 200

    @admin_required
    def post(self):
        req_json = request.json
        user_service.create(req_json)
        return "", 201


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    def get(self, uid: int):
        try:
            user = user_service.get_one(uid)
            return user_schema.dump(user), 200
        except Exception:
            return "", 404

    @admin_required
    def put(self, uid: int):
        req_json = request.json
        user_service.update(uid, req_json)
        return "", 204

    @admin_required
    def delete(self, uid: int):
        user_service.delete(uid)
        return "", 204
