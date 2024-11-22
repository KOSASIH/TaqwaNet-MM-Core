from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class LoanRequest(Base):
    __tablename__ = 'loan_requests'

    id = Column(String, primary_key=True)
    borrower_id = Column(String, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    duration_months = Column(Integer, nullable=False)
    status = Column(String, default='Pending')  # Pending, Approved, Rejected
    created_at = Column(DateTime, default=datetime.utcnow)

    borrower = relationship("User ", back_populates="loan_requests")

    def approve(self):
        """Approve the loan request."""
        self.status = "Approved"

    def reject(self):
        """Reject the loan request."""
        self.status = "Rejected"

    def get_details(self):
        """Get details of the loan request."""
        return {
            "id": self.id,
            "borrower": self.borrower.username,
            "amount": self.amount,
            "interest_rate": self.interest_rate,
            "duration_months": self.duration_months,
            "status": self.status,
            "created_at": self.created_at
        }

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    loan_requests = relationship("LoanRequest", back_populates="borrower")

    def __repr__(self):
        return f"<User (username={self.username}, email={self.email})>"
