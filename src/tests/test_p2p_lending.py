import unittest
from src.services.p2p_lending_service import P2PLendingService
from src.models.p2p_loan import P2PLoan

class TestP2PLendingService(unittest.TestCase):

    def setUp(self):
        self.lending_service = P2PLendingService()

    def test_create_loan_request(self):
        loan_request = P2PLoan(amount=5000, borrower_id=1, interest_rate=5.0)
        result = self.lending_service.create_loan_request(loan_request)
        self.assertTrue(result, "The loan request should be created successfully.")

    def test_fund_loan_request(self):
        loan_request = P2PLoan(amount=5000, borrower_id=1, interest_rate=5.0)
        self.lending_service.create_loan_request(loan_request)
        result = self.lending_service.fund_loan(loan_request.id, 5000)
        self.assertTrue(result, "The loan request should be funded successfully.")

    def test_loan_repayment(self):
        loan_request = P2PLoan(amount=5000, borrower_id=1, interest_rate=5.0)
        self.lending_service.create_loan_request(loan_request)
        self.lending_service.fund_loan(loan_request.id, 5000)
        repayment_result = self.lending_service.repay_loan (loan_request.id, 5000)
        self.assertTrue(repayment_result, "The loan should be marked as repaid successfully.")

if __name__ == '__main__':
    unittest.main()
