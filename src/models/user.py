from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base  # Assuming you have a Base class for SQLAlchemy models

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    transactions = relationship("Transaction", back_populates="user")
    investments = relationship("Investment", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")

    def __repr__(self):
        return f"<User (id={self.id}, username={self.username}, email={self.email})>"
