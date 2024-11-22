import unittest
from src.services.user_service import UserService  # Adjust the import based on your project structure

class TestUser Service(unittest.TestCase):
    def setUp(self):
        self.service = UserService()

    def test_create_user(self):
        user = self.service.create_user('testuser', 'securepassword')
        self.assertEqual(user.username, 'testuser')

if __name__ == '__main__':
    unittest.main()
