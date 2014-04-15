import sqlite3
from client import Client
from time import time


class BlockedUserException(Exception):
    pass


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
                    balance REAL DEFAULT 0,
                    blocked_time INTEGER)'''

        login_attempts_query = '''CREATE TABLE IF NOT EXISTS
                                login_attempts(
                                attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                client_id INTEGER,
                                status TEXT,
                                login_timestamp INTEGER)'''

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
        if self.is_user_blocked(username):
            raise BlockedUserException("User is blocked!")

        select_query = """SELECT id, username, balance
                          FROM clients
                          WHERE username = ? AND password = ?
                          LIMIT 1"""
        login_status = "fail"
        result = None

        password = password_obj.to_sha1()

        self.cursor.execute(select_query, (username, password))
        user = self.cursor.fetchone()

        if user:
            login_status = "success"
            result = Client(user[0], user[1], user[2])

        self.create_login_attempt(username, login_status)

        if self.should_block_user(username):
            self.block_user(username)

        return result

    def get_id_by_username(self, username):
        query = "SELECT id FROM clients WHERE username = ?"
        result = self.cursor.execute(query, (username, ))
        result = result.fetchone()

        if result is not None:
            return result[0]

    def create_login_attempt(self, username, status):
        attempt_query = """INSERT INTO
                           login_attempts(client_id, status, login_timestamp)
                           VALUES(?, ?, ?)
                        """

        user_id = self.get_id_by_username(username)

        if user_id is None:
            return False

        current_timestamp = int(time())

        self.cursor.execute(attempt_query,
                           (user_id, status, current_timestamp))
        self.conn.commit()

        return True

    def block_user(self, username):
        user_id = self.get_id_by_username(username)

        if user_id is None:
            return False

        current_timestamp = int(time())
        block_user_query = """UPDATE clients
                              SET blocked_time = ?
                              WHERE id = ?"""

        self.cursor.execute(block_user_query, (current_timestamp, user_id))
        self.conn.commit()

        return True

    def should_block_user(self, username):
        user_id = self.get_id_by_username(username)

        if user_id is None:
            return False

        should_block_query = """SELECT status FROM login_attempts
                                WHERE client_id = ?
                                ORDER BY attempt_id DESC
                                LIMIT 5
                             """

        rows = self.cursor.execute(should_block_query, (user_id, )).fetchall()
        count_fails = 0

        for row in rows:
            if row[0] == "fail":
                count_fails += 1

        return count_fails >= 5

    def is_user_blocked(self, username):
        user_id = self.get_id_by_username(username)

        if user_id is None:
            return False

        blocked_query = """SELECT blocked_time FROM clients WHERE id = ?"""
        result = self.cursor.execute(blocked_query, (user_id,)).fetchone()

        if result is None or result[0] is None:
            return False
        blocked_time = result[0]
        now = int(time())

        return blocked_time + 300 >= now
