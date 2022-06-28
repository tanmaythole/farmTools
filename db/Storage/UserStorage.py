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
            raise falcon.HTTPBadRequest(title="User already exist with this email.")
        
        if len(str(data.get('mobile'))) != 10:
            raise falcon.HTTPBadRequest("Mobile number not valid!")

        try:
            data['password'] = hash_password(data.get('password')).decode('utf-8')
            user = Users(**data)
            return user.get_dict()
        except Exception as e:
            raise falcon.HTTPBadRequest(title=str(e))

    @staticmethod
    def get_user_by_email(email):
        user = Users.select(Users.q.email==email)
        return user
    
    def get_user(self, id):
        """
        Get User
        """
        user = Users.get(id=id)
        return user

    def update_user(self, user_id, data={}):
        """
        Update User
        """
        user = self.get_user(user_id)
        user_dict = user.get_dict()
        pass

    def change_password(self, user_id, password):
        """
        Change Password of User
        """
        user = self.get_user(user_id)
        try:
            user.set(
                password=hash_password(password).decode('utf-8')
            )
            return user
        except Exception as e:
            raise falcon.HTTPBadRequest(str(e))