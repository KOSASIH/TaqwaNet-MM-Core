import unittest
from src.models.transaction import Transaction  # Adjust the import based on your project structure

class TestTransactionModel(unittest.TestCase):
    def setUp(self):
        self.transaction = Transaction(amount=100, transaction_type='deposit')

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.amount, 100)
        self.assertEqual(self.transaction.transaction_type, 'deposit')

    def test_transaction_repr(self):
        self.assertEqual(repr(self.transaction), "Transaction(amount=100, type='deposit')")

if __name__ == '__main__':
    unittest.main()
