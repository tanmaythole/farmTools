import falcon
from db.models.UserModel import Users
from sqlobject import *
from utils.auth import hash_password

class UserStorage:

    def create_user(self, data):
        """
        Create a New User
        """

        is_exist = list(Users.select(Users.q.email==data.get('email')))

        if len(is_exist)>0:
            raise falcon.HTTPBadRequest(title="User alredy exist with this email.")

        try:
            data['password'] = hash_password(data.get('password')).decode('utf-8')
            user = Users(**data)
            return user.get_dict()
        except Exception as e:
            raise falcon.HTTPBadRequest(title=str(e))

    @staticmethod
    def get_user(email):
        user = Users.select(Users.q.email==email)
        return user