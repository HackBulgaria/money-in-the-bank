import unittest
import sys

sys.path.append("..")

from password import Password, PasswordValidator
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
