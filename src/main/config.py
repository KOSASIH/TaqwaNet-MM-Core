import os

class Config:
    SECRET_KEY = os.environ.get('APP_SECRET_KEY') or 'a_default_secret_key'
    DEBUG = os.environ.get('APP_ENV') == 'development'
    DATABASE_URI = f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"
    RATE_LIMIT = os.environ.get('RATE_LIMIT') or '100/hour'
    AI_MODEL_ENDPOINT = os.environ.get('AI_MODEL_ENDPOINT')
    BLOCKCHAIN_URL = os.environ.get('BLOCKCHAIN_URL')
