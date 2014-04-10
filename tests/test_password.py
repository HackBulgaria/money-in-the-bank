import unittest
import sys

sys.path.append("..")

from password import Password


class PasswordTest(unittest.TestCase):
    def setUp(self):
        self.p = Password("radorado")

    """docstring for PasswordTest"""
    def test_to_sha1(self):
        self.assertEqual('a4b63a5cc956327ffca0a877517a4866aa3f7022',
                         self.p.to_sha1())

    def test_to_string(self):
        self.assertEqual('a4b63a5cc956327ffca0a877517a4866aa3f7022',
                         str(self.p))
