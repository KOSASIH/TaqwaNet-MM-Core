# src/security/zero_trust.py

import hashlib
import time
from collections import defaultdict

class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = self.hash_password(password)
        self.access_level = 1  # Default access level
        self.last_login = None

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == self.hash_password(password)

class ZeroTrustModel:
    def __init__(self):
        self.users = {}
        self.access_logs = defaultdict(list)

    def register_user(self, username, password):
        if username in self.users:
            raise Exception("User  already exists.")
        self.users[username] = User(username, password)

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and user.check_password(password):
            user.last_login = time.time()
            return True
        return False

    def authorize_access(self, username, resource, required_access_level):
        user = self.users.get(username)
        if user and user.access_level >= required_access_level:
            self.log_access_attempt(username, resource, success=True)
            return True
        self.log_access_attempt(username, resource, success=False)
        return False

    def log_access_attempt(self, username, resource, success):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        self.access_logs[username].append({
            'resource': resource,
            'timestamp': timestamp,
            'success': success
        })

    def get_access_logs(self, username):
        return self.access_logs.get(username, [])

if __name__ == "__main__":
    # Example usage
    zero_trust = ZeroTrustModel()

    # Register users
    zero_trust.register_user("alice", "password123")
    zero_trust.register_user("bob", "securepassword")

    # Authenticate users
    if zero_trust.authenticate_user("alice", "password123"):
        print("Alice authenticated successfully.")
    else:
        print("Alice authentication failed.")

    # Authorize access to resources
    if zero_trust.authorize_access("alice", "resource_1", required_access_level=1):
        print("Alice has access to resource_1.")
    else:
        print("Alice does not have access to resource_1.")

    # Log access attempts
    print("Access logs for Alice:")
    for log in zero_trust.get_access_logs("alice"):
        print(log)
