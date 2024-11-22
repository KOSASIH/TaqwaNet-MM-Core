import uuid
from datetime import datetime
from typing import List, Dict, Any

class LoanRequest:
    def __init__(self, borrower: str, amount: float, interest_rate: float, duration_months: int):
        self.id: str = str(uuid.uuid4())
        self.borrower: str = borrower
        self.amount: float = amount
        self.interest_rate: float = interest_rate
        self.duration_months: int = duration_months
        self.status: str = "Pending"  # Status can be Pending, Approved, or Rejected
        self.created_at: datetime = datetime.now()

    def approve(self):
        """Approve the loan request."""
        self.status = "Approved"

    def reject(self):
        """Reject the loan request."""
        self.status = "Rejected"

    def get_details(self) -> Dict[str, Any]:
        """Get details of the loan request."""
        return {
            "id": self.id,
            "borrower": self.borrower,
            "amount": self.amount,
            "interest_rate": self.interest_rate,
            "duration_months": self.duration_months,
            "status": self.status,
            "created_at": self.created_at
        }

class P2PLendingService:
    def __init__(self):
        self.loan_requests: Dict[str, LoanRequest] = {}

    def create_loan_request(self, borrower: str, amount: float, interest_rate: float, duration_months: int) -> LoanRequest:
        """Create a new loan request."""
        loan_request = LoanRequest(borrower, amount, interest_rate, duration_months)
        self.loan_requests[loan_request.id] = loan_request
        return loan_request

    def get_loan_request(self, loan_request_id: str) -> LoanRequest:
        """Retrieve a loan request by its ID."""
        return self.loan_requests.get(loan_request_id)

    def approve_loan_request(self, loan_request_id: str) -> LoanRequest:
        """Approve a loan request."""
        loan_request = self.get_loan_request(loan_request_id)
        if loan_request:
            loan_request.approve()
            return loan_request
        raise Exception("Loan request not found.")

    def reject_loan_request(self, loan_request_id: str) -> LoanRequest:
        """Reject a loan request."""
        loan_request = self.get_loan_request(loan_request_id)
        if loan_request:
            loan_request.reject()
            return loan_request
        raise Exception("Loan request not found.")

    def get_all_loan_requests(self) -> List[LoanRequest]:
        """Retrieve a list of all loan requests."""
        return list(self.loan_requests.values())

    def get_loan_request_status(self, loan_request_id: str) -> str:
        """Get the status of a specific loan request."""
        loan_request = self.get_loan_request(loan_request_id)
        if loan_request:
            return loan_request.status
        raise Exception("Loan request not found.")

# Example usage
if __name__ == "__main__":
    lending_service = P2PLendingService()

    # Create a new loan request
    loan_request = lending_service.create_loan_request(
        borrower="John Doe",
        amount=10000.0,
        interest_rate=5.0,
        duration_months=12
    )

    print(f"Created loan request: {loan_request.get_details()}")

    # Approve the loan request
    approved_request = lending_service.approve_loan_request(loan_request.id)
    print(f"Approved loan request: {approved_request.get_details()}")

    # List all loan requests
    all_requests = lending_service.get_all_loan_requests()
    print("All Loan Requests:")
    for request in all_requests:
        print(request.get_details())
