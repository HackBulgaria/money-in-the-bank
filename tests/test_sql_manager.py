import sys
import unittest

sys.path.append("..")

from sql_manager import SqlManager
from password import Password
import os


class SqlManagerTests(unittest.TestCase):

    def setUp(self):
        self.db_file = "bank_test.db"
        self.sql_manager = SqlManager(self.db_file)
        self.sql_manager.register('Tester', Password('Radorado1234@'))

    def tearDown(self):
        os.remove(self.db_file)

    def test_register(self):
        p = Password('Radorado1234@')
        self.sql_manager.register('Dinko', p)
        count_sql = """SELECT Count(*)
                       FROM clients
                       WHERE
                        username = ? AND password = ?
                    """
        self.sql_manager.cursor.execute(count_sql, ('Dinko', str(p)))
        users_count = self.sql_manager.cursor.fetchone()

        self.assertEqual(users_count[0], 1)

    def test_register_password_should_not_be_plain_text(self):
        plain = "asd"
        p = Password(plain)
        self.sql_manager.register("Test", p)

        password_sql = """SELECT password
                          FROM clients
                          WHERE username = ?
                          LIMIT 1
                       """
        db_password = self.sql_manager.cursor.execute(password_sql,
                                                      ("Test", ))
        self.assertNotEqual(plain, db_password)

    def test_login(self):
        p = Password('Radorado1234@')
        logged_user = self.sql_manager.login('Tester', p)
        self.assertEqual(logged_user.get_username(), 'Tester')

    def test_login_with_sql_injection(self):
        p = Password("Radorado1234@whatever")
        logged_user = self.sql_manager.login("' OR 1 = 1 --", p)
        self.assertIsNone(logged_user)

    def test_login_wrong_password(self):
        p = Password("Radorado1234@wrong")
        logged_user = self.sql_manager.login('Tester', p)
        self.assertFalse(logged_user)

    def test_change_password(self):
        p = Password("Radorado1234@")
        logged_user = self.sql_manager.login('Tester', p)
        new_password = Password("Radorado1234@12345")
        self.sql_manager.change_pass(new_password, logged_user)

        new_pass = self.sql_manager.login('Tester', new_password)
        self.assertEqual(new_pass.get_username(), 'Tester')

    def test_get_id_by_username(self):
        result = self.sql_manager.get_id_by_username("Tester")
        self.assertEqual(1, result)

    def test_get_id_by_username_not_found(self):
        result = self.sql_manager.get_id_by_username("Tester Not Found")
        self.assertIsNone(result)

    def test_create_login_attempt(self):
        result = self.sql_manager.create_login_attempt("Tester", "login")
        self.assertTrue(result)

    def test_is_user_blocked_for_non_existent_user(self):
        result = self.sql_manager.is_user_blocked("OMGOMGOMG")
        self.assertFalse(result)

    def test_is_user_blocked_without_any_logins(self):
        result = self.sql_manager.is_user_blocked("Tester")
        self.assertFalse(result)

    def test_should_block_user_with_no_login_attempts(self):
        result = self.sql_manager.should_block_user("Tester")
        self.assertFalse(result)

    def test_should_block_user_after_6_wrong_attempts(self):
        wrong_password = Password("Wrong_Password1234@")

        for i in range(6):
            self.sql_manager.login("Tester", wrong_password)

        result = self.sql_manager.should_block_user("Tester")
        self.assertTrue(result)

    @unittest.skip
    def test_is_user_blocked_after_6_attempts(self):
        wrong_password = Password("Wrong_Password1234@")

        for i in range(6):
            self.sql_manager.login("Tester", wrong_password)

        result = self.sql_manager.is_user_blocked("Tester")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
