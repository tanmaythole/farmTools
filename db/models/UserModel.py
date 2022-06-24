from db import conn
from sqlobject import *

class Users(SQLObject):
    """
    User Model
    """

    _connection = conn
    first_name = StringCol(notNone=True)
    last_name = StringCol(notNone=True)
    email = StringCol(length=50, notNone=True, unique=True)
    mobile = IntCol(notNone=True, unique=True)
    password = StringCol()
    is_verified = BoolCol(default=False)
    created_at = DateTimeCol().now()
    modified_at = DateTimeCol().now()

    def get_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "mobile": self.mobile,
            "is_verified": self.is_verified,
            "created_at": str(self.created_at),
            "modified_at": str(self.created_at)
        }

Users.createTable(ifNotExists=True)