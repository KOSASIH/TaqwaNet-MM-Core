# src/security/encryption.py

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os
import hashlib

class Encryption:
    def __init__(self, key=None):
        """Initialize the Encryption class with a key."""
        if key:
            self.key = self._derive_key(key)
        else:
            self.key = get_random_bytes(32)  # AES-256

    def _derive_key(self, password):
        """Derive a key from a password using PBKDF2."""
        salt = os.urandom(16)
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return salt + key  # Store salt with the key

    def encrypt(self, plaintext):
        """Encrypt the plaintext using AES encryption."""
        cipher = AES.new(self.key[16:], AES.MODE_GCM)  # Use the derived key
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')

    def decrypt(self, encrypted_text):
        """Decrypt the encrypted text using AES decryption."""
        data = base64.b64decode(encrypted_text.encode('utf-8'))
        nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
        cipher = AES.new(self.key[16:], AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')

    def get_key(self):
        """Return the base64 encoded key."""
        return base64.b64encode(self.key).decode('utf-8')

    @staticmethod
    def load_key(encoded_key):
        """Load the key from a base64 encoded string."""
        return base64.b64decode(encoded_key.encode('utf-8'))

    def save_key(self, filename='encryption_key.key'):
        """Save the encryption key to a file."""
        with open(filename, 'wb') as key_file:
            key_file.write(self.key)

    @staticmethod
    def load_key_from_file(filename='encryption_key.key'):
        """Load the encryption key from a file."""
        with open(filename, 'rb') as key_file:
            return key_file.read()

# Example usage
if __name__ == "__main__":
    # Initialize encryption with a password
    password = "secure_password"
    encryption = Encryption(password)

    # Encrypt some data
    plaintext = "This is a secret message."
    encrypted = encryption.encrypt(plaintext)
    print("Encrypted:", encrypted)

    # Decrypt the data
    decrypted = encryption.decrypt(encrypted)
    print("Decrypted:", decrypted)

    # Save the key to a file
    encryption.save_key()

    # Load the key from a file
    loaded_key = Encryption.load_key_from_file()
    print("Loaded Key:", base64.b64encode(loaded_key).decode('utf-8'))
