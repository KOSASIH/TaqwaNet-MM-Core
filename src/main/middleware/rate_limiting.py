from flask import request, jsonify
import time
from collections import defaultdict
from config import Config

class RateLimitingMiddleware:
    def __init__(self, app):
        self.app = app
        self.visitors = defaultdict(list)  # Store timestamps of requests for each IP
        self.rate_limit = self.parse_rate_limit(Config.RATE_LIMIT)  # Parse rate limit from config

    def parse_rate_limit(self, rate_limit):
        """Parse the rate limit string (e.g., '100/hour') into a count and period."""
        count, period = rate_limit.split('/')
        count = int(count)
        if period == 'hour':
            return count, 3600  # 1 hour in seconds
        elif period == 'minute':
            return count, 60  # 1 minute in seconds
        else:
            raise ValueError("Unsupported rate limit period. Use 'hour' or 'minute'.")

    def __call__(self, environ, start_response):
        ip = environ.get('REMOTE_ADDR')  # Get the client's IP address
        current_time = time.time()  # Get the current time
        limit_count, limit_period = self.rate_limit

        # Clean up the timestamps for the current IP
        self.visitors[ip] = [t for t in self.visitors[ip] if t > current_time - limit_period]

        # Check if the request exceeds the rate limit
        if len(self.visitors[ip]) >= limit_count:
            response = jsonify({'error': 'Rate limit exceeded. Try again later.'})
            response.status_code = 429  # Too Many Requests
            return response(environ, start_response)

        # Record the current request timestamp
        self.visitors[ip].append(current_time)
        return self.app(environ, start_response)

# Example of how to use the middleware in the application
# In app.py, you would initialize it like this:
# app.wsgi_app = RateLimitingMiddleware(app.wsgi_app)
