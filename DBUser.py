import logging

from Database import Database
from User import User
import re


class DBUser:

    def __init__(self, user: User = None, db: Database = None):
        self.user = user
        self.db = db

    def create(self, user: User = None):
        user = user if user else self.user
        adding_result = self.db.add_user(user)
        if not adding_result:
            logging.error('Error on creating of  user')
        return adding_result

    @property
    def can_be_created(self):
        return True
