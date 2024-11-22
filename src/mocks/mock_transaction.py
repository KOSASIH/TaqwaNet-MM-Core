# mocks/mock_transaction.py

from faker import Faker
import random

fake = Faker()

def generate_mock_transaction(transaction_id=1, user_id=1):
    """Generate a mock transaction data."""
    return {
        'id': transaction_id,
        'user_id': user_id,
        'amount': round(random.uniform(10.0, 1000.0), 2),
        'transaction_type': random.choice(['deposit', 'withdrawal']),
        'created_at': fake.date_time_this_year(),
        'status': random.choice(['completed', 'pending', 'failed']),
    }

def generate_mock_transactions(num_transactions=5, user_id=1):
    """Generate a list of mock transactions."""
    return [generate_mock_transaction(transaction_id=i, user_id=user_id) for i in range(1, num_transactions + 1)]
