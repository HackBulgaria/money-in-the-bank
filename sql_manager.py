import sqlite3
from client import Client


class SqlManager():
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_clients_table(self):
        create_query = '''create table if not exists
            clients(id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT,
                    balance REAL DEFAULT 0,
                    message TEXT)'''

        self.cursor.execute(create_query)

    def change_message(self, new_message, logged_user):
        update_sql = """UPDATE clients
                        SET message = '%s'
                        WHERE id = '%s'"""
        update_sql = update_sql % (new_message, logged_user.get_id())
        self.cursor.execute(update_sql)
        self.conn.commit()
        logged_user.set_message(new_message)

    def change_pass(self, new_pass, logged_user):
        update_sql = """UPDATE clients
                        SET password = '%s'
                        WHERE id = '%s'"""
        update_sql = update_sql % (new_pass, logged_user.get_id())
        self.cursor.execute(update_sql)
        self.conn.commit()

    def register(self, username, password):
        insert_sql = "insert into clients (username, password) values ('%s', '%s')" % (username, password)
        self.cursor.execute(insert_sql)
        self.conn.commit()

    def login(self, username, password):
        select_query = "SELECT id, username, balance, message FROM clients WHERE username = '%s' AND password = '%s' LIMIT 1" % (username, password)

        self.cursor.execute(select_query)
        user = self.cursor.fetchone()

        if(user):
            return Client(user[0], user[1], user[2], user[3])
        else:
            return False
