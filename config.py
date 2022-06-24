import os
from dotenv import load_dotenv

load_dotenv()

class Development(object):
    """
    Development Environment Configuration
    """
    DEBUG = True
    TESTING = False
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

if os.getenv('ENVIRONMENT')=='development':
    app_config = Development