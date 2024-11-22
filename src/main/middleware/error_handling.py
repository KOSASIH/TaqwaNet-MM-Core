from flask import jsonify
import logging

class ErrorHandlingMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except Exception as e:
            # Log the error
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            # Create a structured JSON response
            response = jsonify({
                'error': {
                    'message': 'An unexpected error occurred.',
                    'details': str(e)  # Optionally include error details for debugging
                }
            })
            response.status_code = 500  # Internal Server Error
            return response(environ, start_response)

# Example of how to use the middleware in the application
# In app.py, you would initialize it like this:
# app.wsgi_app = ErrorHandlingMiddleware(app.wsgi_app)
