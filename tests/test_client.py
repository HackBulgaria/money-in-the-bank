import sys
import unittest
sys.path.append("..")

from client import Client


class ClientTests(unittest.TestCase):

    def setUp(self):
        self.test_client = Client(1, "Ivo", 200000.00)

    def test_client_id(self):
        self.assertEqual(self.test_client.get_id(), 1)

    def test_client_name(self):
        self.assertEqual("Ivo", self.test_client.get_username())

    def test_client_balance(self):
        self.assertEqual(self.test_client.get_balance(), 200000.00)

if __name__ == '__main__':
    unittest.main()
