import logging

import psycopg2
from credentials import *

from User import User


class Database:

    def __init__(self, user=PG_USER, password=PG_PSSWRD, host=PG_HOST, port=PG_PORT, database=PG_DATABASE):
        """Creating Database"""
        self.connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        self.cursor = self.connection.cursor()

    def close(self):
        """Closing database"""
        self.cursor.close()
        self.connection.close()

    def get_menu(self):
        query = '''SELECT * FROM main_menu'''
        try:
            self.cursor.execute(query)
            res = self.cursor.fetchall()
            print(res)
            if res:
                return res
        except Exception as e:
            print(e)
        return []

    def add_user(self, user: User):
        try:
            fields = ['email', 'password_hash']
            field_str = ', '.join(fields)
            query = f"""INSERT INTO users ({field_str}) VALUES (%s, %s) RETURNING id, registration_date"""
            record_to_insert = (user.email, user.password_hash)
            self.cursor.execute(query, record_to_insert)
            print('Executed')
            result = self.cursor.fetchone()
            user.user_id = result[0]
            user.dt_of_registration = result[1]
            self.connection.commit()
            return True
        except:
            logging.exception("Can't create new user", exc_info=True)
            self.connection.rollback()

