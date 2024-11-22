import unittest
from src.security.secure_storage import SecureStorage  # Adjust the import based on your project structure

class TestSecureStorage(unittest.TestCase):
    def setUp(self):
        self.storage = SecureStorage(storage_file='test_secure_storage.json')

    def test_store_and_retrieve(self):
        self.storage.store('test_key', 'test_value')
        retrieved_value = self.storage.retrieve('test_key')
        self.assertEqual(retrieved_value, 'test_value')

    def test_encryption(self):
        encrypted_value = self.storage.encrypt('test_value')
        self.assertNotEqual(encrypted_value, 'test_value')

    def test_decryption(self):
        encrypted_value = self.storage.encrypt('test_value')
        decrypted_value = self.storage.decrypt(encrypted_value)
        self.assertEqual(decrypted_value, 'test_value')

if __name__ == '__main__':
    unittest.main()
