import uuid
from datetime import datetime
from flask import jsonify
from models import Account, Transaction  # Assuming these are ORM models
from sqlalchemy.exc import IntegrityError
from config import Config

class BankingService:
    def create_account(self, user_id, initial_balance=0):
        """Create a new bank account for a user."""
        account_id = str(uuid.uuid4())
        account = Account(id=account_id, user_id=user_id, balance=initial_balance, created_at=datetime.utcnow())
        
        try:
            account.save()  # Save to the database
            return jsonify({'message': 'Account created successfully', 'account_id': account_id}), 201
        except IntegrityError:
            return jsonify({'error': 'Account already exists for this user'}), 409

    def deposit(self, account_id, amount):
        """Deposit money into a bank account."""
        if amount <= 0:
            return jsonify({'error': 'Deposit amount must be positive'}), 400
        
        account = Account.get_by_id(account_id)
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        account.balance += amount
        account.save()
        
        transaction = Transaction(account_id=account_id, amount=amount, transaction_type='deposit', created_at=datetime.utcnow())
        transaction.save()
        
        return jsonify({'message': 'Deposit successful', 'new_balance': account.balance}), 200

    def withdraw(self, account_id, amount):
        """Withdraw money from a bank account."""
        if amount <= 0:
            return jsonify({'error': 'Withdrawal amount must be positive'}), 400
        
        account = Account.get_by_id(account_id)
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        if account.balance < amount:
            return jsonify({'error': 'Insufficient funds'}), 400
        
        account.balance -= amount
        account.save()
        
        transaction = Transaction(account_id=account_id, amount=amount, transaction_type='withdrawal', created_at=datetime.utcnow())
        transaction.save()
        
        return jsonify({'message': 'Withdrawal successful', 'new_balance': account.balance}), 200

    def get_balance(self, account_id):
        """Retrieve the current balance of a bank account."""
        account = Account.get_by_id(account_id)
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        return jsonify({'account_id': account_id, 'balance': account.balance}), 200

    def get_transaction_history(self, account_id):
        """Retrieve the transaction history for a bank account."""
        account = Account.get_by_id(account_id)
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        transactions = Transaction.get_by_account_id(account_id)
        return jsonify({'account_id': account_id, 'transactions': transactions}), 200

    def transfer(self, from_account_id, to_account_id, amount):
        """Transfer money between two bank accounts."""
        if amount <= 0:
            return jsonify({'error': 'Transfer amount must be positive'}), 400
        
        from_account = Account.get_by_id(from_account_id)
        to_account = Account.get_by_id(to_account_id)
        
        if not from_account or not to_account:
            return jsonify({'error': 'One or both accounts not found'}), 404
        
        if from_account.balance < amount:
            return jsonify({'error': 'Insufficient funds in the source account'}), 400
        
        # Perform the transfer
        from_account.balance -= amount
        to_account.balance += amount
        
        from_account.save()
        to_account.save()
        
        # Log transactions
        transaction_out = Transaction(account_id=from_account_id, amount=amount, transaction_type='transfer_out', created_at=datetime.utcnow())
        transaction_in = Transaction(account_id=to_account_id, amount=amount, transaction_type='transfer_in', created_at=datetime.utcnow())
        
        transaction_out.save()
        transaction_in.save()
        
        return jsonify({'message': 'Transfer successful', 'new_balance_from': from_account.balance, 'new_balance_to': to_account.balance}), 200
