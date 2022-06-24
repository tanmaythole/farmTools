import falcon
import jwt
from config import app_config
from db.models.UserModel import Users

class AuthMiddleware:
    """
    Auth Middleware
    """

    def _decrypt_token(self, token):
        """
        Decrypt the jwt token
        """
        try:
            payload = jwt.decode(
                token,
                app_config.JWT_SECRET_KEY,
                algorithms="HS256"
            )
            user = Users.get(payload['user']).get_dict()
            return user
        except Exception as e:
            print(str(e))
            return False

    def process_request(self, req, resp):
        if '/login/' in req.path or '/register/' in req.path:
            return

        token = req.get_header('Authorization').split(" ")[1]

        if token is None:
            raise falcon.HTTPUnauthorized(
                "Auth Token Required",
                "Please login with your credentials to continue the request."
            )
        
        user = self._decrypt_token(token)
        if not user:
            raise falcon.HTTPUnauthorized(
                "Invalid Token",
                "The provided auth token is not valid. Please request a new token and try again."
            )
        else:
            req.context['curr_user'] = user