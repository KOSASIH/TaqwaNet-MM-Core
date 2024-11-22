from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class CrowdfundingProject(Base):
    __tablename__ = 'crowdfunding_projects'

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    owner_id = Column(String, ForeignKey('users.id'), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)
    status = Column(String, default='Ongoing')  # Ongoing, Funded, Expired

    owner = relationship("User ", back_populates="projects")

    def donate(self, amount: float):
        """Process a donation to the project."""
        if self.status != 'Ongoing':
            raise Exception("Project funding period has ended or project is funded.")
        if amount <= 0:
            raise ValueError("Donation amount must be greater than zero.")
        
        self.current_amount += amount
        if self.current_amount >= self.target_amount:
            self.status = 'Funded'
        return self.current_amount

    def get_status(self) -> str:
        """Get the current status of the project."""
        if self.current_amount >= self.target_amount:
            return "Funded"
        elif datetime.utcnow() > self.end_date:
            self.status = "Expired"
            return "Expired"
        return "Ongoing"

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    projects = relationship("CrowdfundingProject", back_populates="owner")

    def __repr__(self):
        return f"<User (username={self.username}, email={self.email})>"
