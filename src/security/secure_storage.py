# src/security/secure_storage.py

from cryptography.fernet import Fernet
import os
import json

class SecureStorage:
    def __init__(self, storage_file='secure_storage.json'):
        """Initialize the SecureStorage class."""
        self.storage_file = storage_file
        self.key = self.load_or_generate_key()
        self.fernet = Fernet(self.key)
        self.data = self.load_data()

    def load_or_generate_key(self):
        """Load the encryption key from a file or generate a new one."""
        if os.path.exists('secret.key'):
            with open('secret.key', 'rb') as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open('secret.key', 'wb') as key_file:
                key_file.write(key)
            return key

    def load_data(self):
        """Load the stored data from the JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                encrypted_data = json.load(file)
                return {k: self.decrypt(v) for k, v in encrypted_data.items()}
        return {}

    def save_data(self):
        """Save the data to the JSON file."""
        with open(self.storage_file, 'w') as file:
            encrypted_data = {k: self.encrypt(v) for k, v in self.data.items()}
            json.dump(encrypted_data, file)

    def encrypt(self, plaintext):
        """Encrypt the plaintext data."""
        return self.fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext):
        """Decrypt the ciphertext data."""
        return self.fernet.decrypt(ciphertext.encode()).decode()

    def store(self, key, value):
        """Store a key-value pair securely."""
        self.data[key] = value
        self.save_data()

    def retrieve(self, key):
        """Retrieve a value by key."""
        return self.data.get(key, None)

# Example usage
if __name__ == "__main__":
    secure_storage = SecureStorage()

    # Store sensitive data
    secure_storage.store('username', 'admin')
    secure_storage.store('password', 'supersecretpassword')

    # Retrieve sensitive data
    username = secure_storage.retrieve('username')
    password = secure_storage.retrieve('password')

    print("Retrieved Username:", username)
    print("Retrieved Password:", password)
