import bcrypt
import jwt
from config import app_config

def hash_password(password):
    """
    Genrate hash of password using bcrypt
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    """
    Verify the password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def generate_jwt_token(user):
    """
    Generate Jwt Token by taking user data
    """
    payload = {
        "user": user['id']
    }
    secret = app_config.JWT_SECRET_KEY
    algo = 'HS256'
    token = jwt.encode(
        payload=payload,
        key=secret,
        algorithm=algo
    )
    return token