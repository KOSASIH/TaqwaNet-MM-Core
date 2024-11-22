from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class TransactionType(enum.Enum):
    CREDIT = "credit"
    DEBIT = "debit"
    TRANSFER = "transfer"

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)  # Using Enum for transaction types
    created_at = Column(DateTime, default=datetime.utcnow)
    description = Column(String(255), nullable=True)  # Optional description for the transaction

    # Relationships
    user = relationship("User ", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, amount={self.amount}, type={self.transaction_type})>"

    def is_valid(self):
        """Validate the transaction."""
        if self.amount <= 0:
            return False
        if self.transaction_type not in TransactionType:
            return False
        return True

    def get_transaction_summary(self):
        """Return a summary of the transaction."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "transaction_type": self.transaction_type.value,
            "created_at": self.created_at.isoformat(),
            "description": self.description
        }
