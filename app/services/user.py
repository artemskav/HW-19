import base64
import hashlib
import hmac

from app.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from app.dao.user import UserDAO


class UserService:

    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_username(self, username):
        return self.dao.get_username(username)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        data['password'] = self.generate_password(data.get('password'))
        return self.dao.create(data)

    def update(self, uid, data):
        user = self.get_one(uid)
        user.username = data.get('username')
        user.password = self.generate_password(data.get('password'))
        user.role = data.get('role')
        self.dao.update(user)

    def delete(self, uid):
        return self.dao.delete(uid)

    # def get_hash(self, password):
    #     return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), PWD_HASH_SALT,
    #                                PWD_HASH_ITERATIONS).decode("utf-8", "ignore")

    def generate_password(self, password):
        hash_digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                          PWD_HASH_SALT, PWD_HASH_ITERATIONS)
        return base64.b64encode(hash_digest)

    def compare_password(self, pwd_by_bd, pwd_on_test) -> bool:
        decoded_digest = base64.b64decode(pwd_by_bd)

        hash_digest = hashlib.pbkdf2_hmac('sha256', pwd_on_test.encode('utf-8'),
                                          PWD_HASH_SALT, PWD_HASH_ITERATIONS)
        return hmac.compare_digest(decoded_digest, hash_digest)
#       return pwd_by_bd == pwd_on_test
