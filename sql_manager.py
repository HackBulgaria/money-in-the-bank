import sqlite3
from client import Client
from time import time


class SqlManager():
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_clients_table()

    def create_clients_table(self):
        create_clients_query = '''create table if not exists
            clients(id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT,
                    balance REAL DEFAULT 0)'''

        login_attempts_query = '''CREATE TABLE IF NOT EXISTS
                                login_attempts(
                                attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                client_id INTEGER,
                                status TEXT,
                                timestamp int)'''

        self.cursor.execute(create_clients_query)
        self.cursor.execute(login_attempts_query)

    def change_pass(self, new_pass_obj, logged_user):
        update_sql = """UPDATE clients
                        SET password = ?
                        WHERE id = ?"""

        new_pass = new_pass_obj.to_sha1()

        self.cursor.execute(update_sql, (new_pass, logged_user.get_id()))
        self.conn.commit()

    def register(self, username, password_obj):
        insert_sql = """INSERT INTO clients (username, password)
                        VALUES (?, ?)"""
        password = password_obj.to_sha1()
        self.cursor.execute(insert_sql, (username, password))
        self.conn.commit()

    def login(self, username, password_obj):
        select_query = """SELECT id, username, balance
                          FROM clients
                          WHERE username = ? AND password = ?
                          LIMIT 1"""

        password = password_obj.to_sha1()

        self.cursor.execute(select_query, (username, password))
        user = self.cursor.fetchone()

        if(user):
            return Client(user[0], user[1], user[2])
        else:
            return None

    def get_id_by_username(self, username):
        query = "SELECT id FROM clients WHERE username = ?"
        result = self.cursor.execute(query, (username, ))
        result = result.fetchone()

        if result is not None:
            return result[0]

    def create_login_attempt(self, username, status):
        attempt_query = """INSERT INTO
                           login_attempts(client_id, status, timestamp)
                           VALUES(?, ?, ?)
                        """

        user_id = self.get_id_by_username(username)

        if user_id is None:
            return False

        timestamp = int(time())

        self.cursor.execute(attempt_query, (user_id, status, timestamp))
        self.conn.commit()

        return True
