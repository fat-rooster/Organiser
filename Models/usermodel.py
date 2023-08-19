
from Utilities.Db_utilities import get_user

def hash(x):
    return x

class User:
    def __init__(self, user_id):
        self.username = get_user(user_id)
        self.id = user_id
    
    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id
    class query:
        @staticmethod
        def get(user_id):
            return User(user_id)

