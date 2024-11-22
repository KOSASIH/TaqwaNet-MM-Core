import os
import pyotp
import time
from flask import request, jsonify, session
from functools import wraps

# Configuration for 2FA
OTP_SECRET_KEY = os.environ.get("OTP_SECRET_KEY", "your_default_secret_key")  # Replace with a secure key
OTP_VALIDITY_PERIOD = 30  # OTP validity in seconds

def generate_otp(secret):
    """Generate a time-based OTP."""
    totp = pyotp.TOTP(secret)
    return totp.now()

def verify_otp(secret, otp):
    """Verify the provided OTP against the secret."""
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)

def two_factor_required(f):
    """Decorator to enforce 2FA on protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if '2fa_authenticated' not in session or not session['2fa_authenticated']:
            return jsonify({"message": "Two-Factor Authentication required."}), 403
        return f(*args, **kwargs)
    return decorated_function

def send_otp(user):
    """Send OTP to the user via their preferred method (e.g., SMS, email)."""
    # Here you would implement the logic to send the OTP to the user
    # For example, using an SMS gateway or email service
    secret = user['otp_secret']  # Retrieve the user's OTP secret from the database
    otp = generate_otp(secret)
    
    # Simulate sending OTP (replace with actual sending logic)
    print(f"Sending OTP {otp} to user {user['email']}")
    
    return otp

def verify_user_otp(user, otp):
    """Verify the user's OTP and set the session variable if successful."""
    secret = user['otp_secret']  # Retrieve the user's OTP secret from the database
    if verify_otp(secret, otp):
        session['2fa_authenticated'] = True
        return True
    return False

# Example usage in a Flask application
from flask import Flask, request

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "your_flask_secret_key")

@app.route('/login', methods=['POST'])
def login():
    """Login endpoint."""
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Authenticate user (replace with actual authentication logic)
    user = authenticate_user(username, password)
    
    if user:
        # Send OTP to the user
        send_otp(user)
        return jsonify({"message": "OTP sent to your registered email/phone."}), 200
    return jsonify({"message": "Invalid credentials."}), 401

@app.route('/verify_otp', methods=['POST'])
def verify_otp_route():
    """Verify OTP endpoint."""
    otp = request.json.get('otp')
    username = request.json.get('username')
    
    # Retrieve user from the database (replace with actual retrieval logic)
    user = get_user_by_username(username)
    
    if user and verify_user_otp(user, otp):
        return jsonify({"message": "2FA successful, you are now logged in."}), 200
    return jsonify({"message": "Invalid OTP."}), 403

@app.route('/protected', methods=['GET'])
@two_factor_required
def protected_route():
    """A protected route that requires 2FA."""
    return jsonify({"message": "This is a protected route."}), 200

def authenticate_user(username, password):
    """Mock authentication function (replace with actual logic)."""
    # Simulate a user with an OTP secret
    return {
        "username": username,
        "email": f"{username}@example.com",
        "otp_secret": OTP_SECRET_KEY  # In a real application, this should be unique per user
    }

def get_user_by_username(username):
    """Mock user retrieval function (replace with actual logic)."""
    return authenticate_user(username, "dummy_password")  # Simulate user retrieval

if __name__ == '__main__':
    app.run(debug=True)
