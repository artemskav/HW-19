from flask import request, abort
from flask_restx import Namespace, Resource

from app.services.auth import generate_tokens, approve_refresh_token

auth_ns = Namespace("auth")

@auth_ns.route("/")
class AuthsView(Resource):
    def post(self):
        data = request.json

        username = data.get('username', None)
        password = data.get('password', None)
        if username == None or password == None:
            abort(401)
        tokens = generate_tokens(username, password)
        return tokens, 201

    def put(self):
        data = request.json
        token = data.get("refresh_token")

        tokens = approve_refresh_token(token)
        return tokens, 201

