import unittest
import sys

sys.path.append("..")

from password import Password, PasswordValidator, PasswordNotStrongException
from client import Client


class TestPasswordValidator(unittest.TestCase):
    """docstring for TestPasswordValidator"""
    def setUp(self):
        self.user = Client(1, "Rado", 0)
        self.short_password = Password("short")
        self.weak_password = Password("weak_password")

    def test_password_validator_validate_short_password(self):
        validator = PasswordValidator(self.short_password, self.user)
        self.assertFalse(validator.validate())

    def test_password_validator_validate_capital_letter(self):
        validator = PasswordValidator(self.weak_password, self.user)
        self.assertFalse(validator.validate())

    def test_password_validator_validate_number(self):
        passwd = Password("Weak_password")
        validator = PasswordValidator(passwd, self.user)
        self.assertFalse(validator.validate())

    def test_password_validator_validate_special(self):
        passwd = Password("Weakpassword1")
        validator = PasswordValidator(passwd, self.user)

        self.assertFalse(validator.validate())

    def test_password_validator_validate_name_in_pass(self):
        user = Client(1, "lqlq", 0)
        p = Password("lqlqOMG11!!")
        validator = PasswordValidator(p, user)

        self.assertFalse(validator.validate())

    def test_password_that_is_valid(self):
        user = Client(1, "lqlq", 0)
        p = Password("radoradoOMG11!!")
        validator = PasswordValidator(p, user)

        self.assertTrue(validator.validate())

    def test_validate_with_exception(self):
        validator = PasswordValidator(self.weak_password, self.user)
        with self.assertRaises(PasswordNotStrongException):
            validator.validate_with_exception()
