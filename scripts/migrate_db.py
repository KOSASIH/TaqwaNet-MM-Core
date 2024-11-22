# migrate_db.py - Database migration script

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base  # Adjust the import based on your project structure

def main():
    # Database connection string
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///mydatabase.db')
    
    # Create a database engine
    engine = create_engine(DATABASE_URL)
    
    # Create a configured "Session" class
    Session = sessionmaker(bind=engine)
    
    # Create a session
    session = Session()

    # Run migrations
    print("Running migrations...")
    Base.metadata.create_all(engine)
    
    print("Migrations completed successfully!")

if __name__ == '__main__':
    main()
