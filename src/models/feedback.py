from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    feedback_type = Column(String(50), nullable=False)  # e.g., 'bug report', 'feature request', 'general'
    content = Column(Text, nullable=False)  # The actual feedback content
    created_at = Column(DateTime, default=datetime.utcnow)  # When the feedback was submitted
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # When the feedback was last updated

    # Relationships
    user = relationship("User ", back_populates="feedbacks")

    def __repr__(self):
        return f"<Feedback(id={self.id}, user_id={self.user_id}, feedback_type={self.feedback_type})>"

    def is_valid(self):
        """Validate the feedback entry."""
        if not self.feedback_type or not self.content:
            return False
        return True

    def get_feedback_summary(self):
        """Return a summary of the feedback entry."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "feedback_type": self.feedback_type,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def create_feedback(cls, user_id, feedback_type, content):
        """Create a new feedback entry."""
        return cls(user_id=user_id, feedback_type=feedback_type, content=content)
