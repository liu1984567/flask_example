import unittest
from app.models import User, Role, AnonymousUser, RolePermissionCode
from app import db, create_app

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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

    def test_roles_permission(self):
        Role.init_roles()
        users = User.query.all()
        user0 = User(email='test@126.com', password='test')
        self.assertTrue(user0.can(RolePermissionCode.USER))
        self.assertFalse(user0.can(RolePermissionCode.MODERATOR))
        self.assertFalse(user0.can(RolePermissionCode.ADMINISTRATOR))

    def test_anonymouruser(self):
        user0 = AnonymousUser()
        self.assertFalse(user0.can(RolePermissionCode.USER))
        self.assertFalse(user0.can(RolePermissionCode.MODERATOR))
