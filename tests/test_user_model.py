import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        user0 = User(password='test')
        self.assertTrue(user0.password_hash is not None)

    def test_no_password_getter(self):
        user0 = User(password='test')
        with self.assertRaises(AttributeError):
            user0.password

    def test_password_verification(self):
        user0 = User(password='test')
        self.assertTrue(user0.verify_password('test'))
        self.assertFalse(user0.verify_password('test0'))

    def test_password_random(self):
        user0 = User(password='test')
        user1 = User(password='test')
        self.assertFalse(user0.password_hash == user1.password_hash)
