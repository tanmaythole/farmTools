import json
import re
import falcon
from db.Storage.UserStorage import UserStorage
from utils.auth import check_password, generate_jwt_token

class Auth:
    """
    Authentication API
    """

    def _authenticate(self, req, resp, data):
        """
        Authenticate user and generate jwt
        """
        
        if not data.get('email') or not data.get('password'):
            resp.status = falcon.HTTP_400
            resp.media = {
                "error": "Invalid Credentials!"
            }
        else:
            user = UserStorage.get_user_by_email(data.get('email'))
            if user.count()>0 and check_password(data.get('password'), user[0].password):
                user = user[0].get_dict()
                user['token'] = generate_jwt_token(user)
                resp.status = falcon.HTTP_200
                resp.media = user
            else:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "error": "Invalid Credentials!"
                }
                        

    def login(self, req, resp):
        """
        Login a User
        """
        data = json.loads(req.stream.read(req.content_length or 0))

        if not data.get('email') or not data.get('password'):
            resp.status = falcon.HTTP_400
            resp.media = {
                "error": "Email and Password both fields required!"
            }
        else:
            self._authenticate(req, resp, data)
            

    def register(self, req, resp):
        """
        Register a User
        """
        data = json.loads(req.stream.read(req.content_length))
        
        if not data.get('email') or not data.get('password') or not data.get('mobile'):
            resp.status = falcon.HTTP_400
            resp.media = {
                "error": "Email, Mobile and password are required!"
            }
        else:
            try:
                user = UserStorage().create_user(data)
                resp.status = falcon.HTTP_201
                resp.media = user
            except Exception as e:
                resp.status = e.status
                resp.media = e.title


    def on_post(self, req, resp):
        """
        POST request for auth
        """
        if req.path == '/api/auth/register/':
            self.register(req, resp)
        elif req.path == '/api/auth/login/':
            self.login(req, resp)
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                "error": "Requested URL not found!"
            }

    def on_put_change_password(self, req, resp):
        """
        Change Password of User
        """
        curr_user = req.context.get('curr_user')
        req_data = json.loads(req.stream.read())
        print(curr_user['id'])
        user = UserStorage().get_user(id=curr_user['id'])
        
        if not req_data.get('new_password') or not req_data.get('curr_password'):
            resp.status = falcon.HTTP_400
            resp.media = {
                "error": "All fields are required!"
            }
        elif check_password(req_data.get('curr_password'), user.password):
            UserStorage().change_password(user.id, req_data.get('new_password'))
            resp.status = falcon.HTTP_200
            resp.media = {
                "success": "Password Changed Successfully!"
            }
        else:
            resp.status = falcon.HTTP_400
            resp.media = {
                "success": "Invalid Password!"
            }