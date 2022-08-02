import datetime
from werkzeug.security import generate_password_hash


class User:
    # id: int
    # login: str
    # password_hash: str
    # email: str
    # phone_number: str
    # dt_of_registration: datetime.datetime

    def __init__(self,
                 user_id: int = None,
                 email: str = None,
                 password: str = None,
                 password_hash: str = None):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.password_hash = password_hash if password_hash else generate_password_hash(password)


