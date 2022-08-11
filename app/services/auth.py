import calendar
import datetime

import jwt
from flask_restx import abort

from app.constants import JWT_SECRET, JWT_ALGORITHM
from app.container import user_service
from app.services.user import UserService


def generate_tokens(username, password, is_refresh=False) -> dict:
    user = user_service.get_username(username)
    if user is None:
        raise abort(404)
    if not is_refresh:
        if not user_service.compare_password(user[1], password):
            abort(401)
    data = {
        "username": user[0],
        "password": user[1],
        "role": user[2]
    }

    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
    days180 = datetime.datetime.utcnow() + datetime.timedelta(days=180)
    data["exp"] = calendar.timegm(days180.timetuple())
    refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
    tokens = {"access_token": access_token, "refresh_token": refresh_token}

    return tokens

def approve_refresh_token(refresh_token):
    data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithm=[JWT_ALGORITHM])
    username = data.get("username")

    return generate_tokens(username, None, is_refresh=True)
