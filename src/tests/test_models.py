import unittest
from src.models import User, Transaction, Investment  # Adjust the import based on your project structure

class TestModels(unittest.TestCase):
    def test_user_model(self):
        user = User(username='testuser', password='securepassword')
        self.assertTrue(user.check_password('securepassword'))

    def test_transaction_model(self):
        transaction = Transaction(amount=100, transaction_type='deposit')
        self.assertEqual(transaction.amount, 100)

    def test_investment_model(self):
        investment = Investment(amount=1000, investment_type='stocks')
        self.assertEqual(investment.investment_type, 'stocks')

if __name__ == '__main__':
    unittest.main()
