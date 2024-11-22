# mocks/mock_user.py

from faker import Faker

fake = Faker()

def generate_mock_user(user_id=1):
    """Generate a mock user data."""
    return {
        'id': user_id,
        'username': fake.user_name(),
        'email': fake.email(),
        'password': fake.password(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'created_at': fake.date_time_this_year(),
        'updated_at': fake.date_time_this_year(),
    }

def generate_mock_users(num_users=5):
    """Generate a list of mock users."""
    return [generate_mock_user(user_id=i) for i in range(1, num_users + 1)]
