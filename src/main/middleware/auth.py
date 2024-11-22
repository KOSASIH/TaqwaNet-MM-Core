from flask import request, jsonify
import jwt
from functools import wraps
from config import Config
from datetime import datetime, timedelta

# Function to generate a new JWT token
def generate_token(user_id, user_role):
    payload = {
        'sub': user_id,
        'role': user_role,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

# Decorator to protect routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            # Decode the token
            data = jwt.decode(token.split(" ")[1], Config.SECRET_KEY, algorithms=["HS256"])
            request.user_id = data['sub']
            request.user_role = data['role']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

# Middleware class for authentication
class AuthMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Custom authentication logic can be added here
        return self.app(environ, start_response)

# Example usage of the token generation function
def create_user_token(user_id, user_role):
    token = generate_token(user_id, user_role)
    return token
