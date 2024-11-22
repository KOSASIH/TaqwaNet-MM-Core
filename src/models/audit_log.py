from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action = Column(String(255), nullable=False)  # Description of the action performed
    timestamp = Column(DateTime, default=datetime.utcnow)  # When the action was performed
    details = Column(String(500), nullable=True)  # Optional details about the action

    # Relationships
    user = relationship("User ", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(id={self.id}, user_id={self.user_id}, action={self.action}, timestamp={self.timestamp})>"

    def get_log_summary(self):
        """Return a summary of the audit log entry."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details
        }

    @classmethod
    def create_log(cls, user_id, action, details=None):
        """Create a new audit log entry."""
        return cls(user_id=user_id, action=action, details=details)
