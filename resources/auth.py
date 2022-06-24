import json
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
            user = UserStorage.get_user(data.get('email'))
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
        data = json.loads(req.stream.read())

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
        data = json.loads(req.stream.read())
        
        if not data.get('email') or not data.get('password') or not data.get('mobile'):
            resp.status = falcon.HTTP_400
            resp.media = {
                "error": "Email, Mobile and password are required!"
            }
        else:
            user = UserStorage().create_user(data)
            resp.status = falcon.HTTP_201
            resp.media = user


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