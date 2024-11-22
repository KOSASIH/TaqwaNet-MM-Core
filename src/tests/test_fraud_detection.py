import unittest
from src.services.fraud_detection_service import FraudDetectionService
from src.models.transaction import Transaction

class TestFraudDetectionService(unittest.TestCase):

    def setUp(self):
        self.fraud_service = FraudDetectionService()

    def test_detect_fraudulent_transaction(self):
        # Create a sample transaction that is likely fraudulent
        transaction = Transaction(amount=10000, user_id=1, location="Suspicious Location", timestamp="2023-10-01T12:00:00Z")
        result = self.fraud_service.detect_fraud(transaction)
        self.assertTrue(result, "The transaction should be flagged as fraudulent.")

    def test_non_fraudulent_transaction(self):
        # Create a sample transaction that is not fraudulent
        transaction = Transaction(amount=100, user_id=1, location="Normal Location", timestamp="2023-10-01T12:00:00Z")
        result = self.fraud_service.detect_fraud(transaction)
        self.assertFalse(result, "The transaction should not be flagged as fraudulent.")

    def test_multiple_transactions(self):
        transactions = [
            Transaction(amount=5000, user_id=1, location="Normal Location", timestamp="2023-10-01T12:00:00Z"),
            Transaction(amount=20000, user_id=1, location="Suspicious Location", timestamp="2023-10-01T12:00:00Z"),
        ]
        results = [self.fraud_service.detect_fraud(tx) for tx in transactions]
        self.assertEqual(results, [False, True], "The results should match the expected fraud detection outcomes.")

if __name__ == '__main__':
    unittest.main()
