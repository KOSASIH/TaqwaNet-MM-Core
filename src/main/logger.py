import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    log_file = os.environ.get('LOG_FILE', 'app.log')
    logging.basicConfig(level=logging.INFO)
    handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=10)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
