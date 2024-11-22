from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Compliance(Base):
    __tablename__ = 'compliance_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    compliance_type = Column(String(100), nullable=False)  # e.g., 'KYC', 'AML', 'Tax Compliance'
    status = Column(Boolean, default=False)  # True if compliant, False otherwise
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = Column(String(255), nullable=True)  # Optional notes regarding compliance

    # Relationships
    user = relationship("User ", back_populates="compliance_records")

    def __repr__(self):
        return f"<Compliance(id={self.id}, user_id={self.user_id}, compliance_type={self.compliance_type}, status={self.status})>"

    def is_valid(self):
        """Validate the compliance record."""
        if not self.compliance_type:
            return False
        return True

    def get_compliance_summary(self):
        """Return a summary of the compliance record."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "compliance_type": self.compliance_type,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "notes": self.notes
        }

    def update_status(self, status, notes=None):
        """Update the compliance status and optional notes."""
        self.status = status
        if notes:
            self.notes = notes
