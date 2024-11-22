from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Investment(Base):
    __tablename__ = 'investments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    investment_type = Column(String(50), nullable=False)  # e.g., 'stocks', 'bonds', 'real estate'
    created_at = Column(DateTime, default=datetime.utcnow)
    description = Column(String(255), nullable=True)  # Optional description for the investment

    # Relationships
    user = relationship("User ", back_populates="investments")

    def __repr__(self):
        return f"<Investment(id={self.id}, user_id={self.user_id}, amount={self.amount}, type={self.investment_type})>"

    def is_valid(self):
        """Validate the investment."""
        if self.amount <= 0:
            return False
        if not self.investment_type:
            return False
        return True

    def get_investment_summary(self):
        """Return a summary of the investment."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "investment_type": self.investment_type,
            "created_at": self.created_at.isoformat(),
            "description": self.description
        }
