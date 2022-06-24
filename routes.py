import falcon
from middleware.AuthMiddleware import AuthMiddleware
from resources.auth import Auth

def get_app():
    application = falcon.App()

    application.add_middleware(AuthMiddleware())

    application.add_route('/api/auth/register/', Auth())
    application.add_route('/api/auth/login/', Auth())
    application.add_route('/api/auth/user/change-password/', Auth(), suffix="change_password")

    return application