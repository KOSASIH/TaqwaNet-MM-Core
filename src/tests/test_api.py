import unittest
from flask import Flask
from src.api import create_app  # Adjust the import based on your project structure

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_users(self):
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        response = self.client.post('/api/users', json={'username': 'newuser', 'password': 'newpassword'})
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
