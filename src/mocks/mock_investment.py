# mocks/mock_investment.py

from faker import Faker
import random

fake = Faker()

def generate_mock_investment(investment_id=1, user_id=1):
    """Generate a mock investment data."""
    return {
        'id': investment_id,
        'user_id': user_id,
        'amount': round(random.uniform(100.0, 10000.0), 2),
        'investment_type': random.choice(['stocks', 'bonds', 'real estate', 'cryptocurrency']),
        'created_at': fake.date_time_this_year(),
        'status': random.choice(['active', 'closed']),
    }

def generate_mock_investments(num_investments=5, user_id=1):
    """Generate a list of mock investments."""
    return [generate_mock_investment(investment_id=i, user_id=user_id) for i in range(1, num_investments + 1)]
