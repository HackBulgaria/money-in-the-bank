import unittest
import sys

sys.path.append("..")

from password import Password


class PasswordTest(unittest.TestCase):
    def setUp(self):
        self.p = Password("Radorado1234@")

    """docstring for PasswordTest"""
    def test_to_sha1(self):
        self.assertEqual('4293b365e7ca8d7914fda1524abd754bc1ca6235',
                         self.p.to_sha1())

    def test_to_plain(self):
        plain = "LQLQLLQLQ"
        p = Password(plain)

        self.assertEqual(plain, p.get_plain())

    def test_to_string(self):
        self.assertEqual('4293b365e7ca8d7914fda1524abd754bc1ca6235',
                         str(self.p))
