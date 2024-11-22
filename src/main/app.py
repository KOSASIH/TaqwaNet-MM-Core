from flask import Flask
from config import Config
from logger import setup_logging
from middleware.auth import AuthMiddleware
from middleware.error_handling import ErrorHandlingMiddleware
from middleware.rate_limiting import RateLimitingMiddleware

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Set up logging
setup_logging()

# Register middleware
app.wsgi_app = RateLimitingMiddleware(app.wsgi_app)
app.wsgi_app = ErrorHandlingMiddleware(app.wsgi_app)
app.wsgi_app = AuthMiddleware(app.wsgi_app)

# Import routes
from routes import user_routes, transaction_routes, investment_routes

# Register blueprints
app.register_blueprint(user_routes)
app.register_blueprint(transaction_routes)
app.register_blueprint(investment_routes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
