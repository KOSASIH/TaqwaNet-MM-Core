# mocks/mock_feedback.py

from faker import Faker

fake = Faker()

def generate_mock_feedback(feedback_id=1, user_id=1):
    """Generate a mock feedback data."""
    return {
        'id': feedback_id,
        'user_id': user_id,
        'content': fake.sentence(nb_words=10),
        'rating': random.randint(1, 5),  # Rating from 1 to 5
        'created_at': fake.date_time_this_year(),
    }

def generate_mock_feedbacks(num_feedbacks=5, user_id=1):
    """Generate a list of mock feedback."""
    return [generate_mock_feedback(feedback_id=i, user_id=user_id) for i in range(1, num_feedbacks + 1)]
