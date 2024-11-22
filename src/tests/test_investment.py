import unittest
from src.models.investment import Investment  # Adjust the import based on your project structure

class TestInvestmentModel(unittest.TestCase):
    def setUp(self):
        self.investment = Investment(amount=1000, investment_type='stocks')

    def test_investment_creation(self):
        self.assertEqual(self.investment.amount, 1000)
        self.assertEqual(self.investment.investment_type, 'stocks')

    def test_investment_repr(self):
        self.assertEqual(repr(self.investment), "Investment(amount=1000, type='stocks')")

if __name__ == '__main__':
    unittest.main()
