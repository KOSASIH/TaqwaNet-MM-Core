# seed_db.py - Database seeding script

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import User, Transaction, Investment  # Adjust the import based on your project structure
from mocks.mock_user import generate_mock_users
from mocks.mock_transaction import generate_mock_transactions
from mocks.mock_investment import generate_mock_investments

def main():
    # Database connection string
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///mydatabase.db')
    
    # Create a database engine
    engine = create_engine(DATABASE_URL)
    
    # Create a configured "Session" class
    Session = sessionmaker(bind=engine)
    
    # Create a session
    session = Session()

    # Seed users
    print("Seeding users...")
    users = generate_mock_users(num_users=10)
    for user_data in users:
        user = User(**user_data)
        session.add(user)

    # Seed transactions
    print("Seeding transactions...")
    for user in users:
        transactions = generate_mock_transactions(num_transactions=5, user_id=user['id'])
        for transaction_data in transactions:
            transaction = Transaction(**transaction_data)
            session.add(transaction)

    # Seed investments
    print("Seeding investments...")
    for user in users:
        investments = generate_mock_investments(num_investments=3, user_id=user['id'])
        for investment_data in investments:
            investment = Investment(**investment_data)
            session.add(investment)

    # Commit the session
    session.commit()
    print("Seeding completed successfully!")

if __name__ == '__main__':
    main()
