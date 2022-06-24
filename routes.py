import falcon
from resources.auth import Auth

def get_app():
    application = falcon.App()

    application.add_route('/api/auth/register/', Auth())
    application.add_route('/api/auth/login/', Auth())

    return application