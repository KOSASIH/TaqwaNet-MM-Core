import unittest
from src.models.user import User  # Adjust the import based on your project structure

class TestUser Model(unittest.TestCase):
    def setUp(self):
        self.user = User(username='testuser', password='securepassword')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('securepassword'))

    def test_user_repr(self):
        self.assertEqual(repr(self.user), "User (username='testuser')")

if __name__ == '__main__':
    unittest.main()
