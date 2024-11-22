import unittest
from src.controllers.user_controller import UserController  # Adjust the import based on your project structure

class TestUser Controller(unittest.TestCase):
    def setUp(self):
        self.controller = UserController()

    def test_get_user(self):
        user = self.controller.get_user('testuser')
 self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')

    def test_delete_user(self):
        result = self.controller.delete_user('testuser')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
