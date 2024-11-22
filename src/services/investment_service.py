from datetime import datetime
from flask import jsonify
from models import Investment, User  # Assuming these are ORM models
from sqlalchemy.exc import IntegrityError

class InvestmentService:
    def create_investment(self, user_id, amount, investment_type, duration_months):
        """Create a new investment for a user."""
        investment = Investment(
            user_id=user_id,
            amount=amount,
            investment_type=investment_type,
            duration_months=duration_months,
            created_at=datetime.utcnow()
        )
        
        try:
            investment.save()  # Save to the database
            return jsonify({'message': 'Investment created successfully', 'investment_id': investment.id}), 201
        except IntegrityError:
            return jsonify({'error': 'Investment already exists for this user'}), 409

    def get_investment_summary(self, user_id):
        """Retrieve a summary of all investments for a user."""
        investments = Investment.get_by_user_id(user_id)
        total_invested = sum(investment.amount for investment in investments)
        total_returns = sum(self.calculate_returns(investment.id)['returns'] for investment in investments)
        
        return jsonify({
            'user_id': user_id,
            'total_invested': total_invested,
            'total_returns': total_returns,
            'investments': investments
        }), 200

    def calculate_returns(self, investment_id):
        """Calculate returns for a specific investment."""
        investment = Investment.get_by_id(investment_id)
        if not investment:
            return jsonify({'error': 'Investment not found'}), 404
        
        # Example return calculation logic based on investment type and duration
        if investment.investment_type == 'fixed':
            returns = investment.amount * (1 + 0.05 * investment.duration_months / 12)  # 5% annual return
        elif investment.investment_type == 'stocks':
            returns = investment.amount * (1 + 0.10 * investment.duration_months / 12)  # 10% annual return
        else:
            returns = investment.amount  # No returns for other types
        
        return jsonify({'investment_id': investment_id, 'returns': returns}), 200

    def get_investment_details(self, investment_id):
        """Retrieve details of a specific investment."""
        investment = Investment.get_by_id(investment_id)
        if not investment:
            return jsonify({'error': 'Investment not found'}), 404
        
        return jsonify({'investment_id': investment.id, 'details': investment}), 200

    def withdraw_investment(self, investment_id):
        """Withdraw an investment and calculate returns."""
        investment = Investment.get_by_id(investment_id)
        if not investment:
            return jsonify({'error': 'Investment not found'}), 404
        
        returns = self.calculate_returns(investment_id)['returns']
        
        # Logic to handle the withdrawal process
        investment.delete()  # Assuming this method exists to remove the investment
        return jsonify({'message': 'Investment withdrawn successfully', 'returns': returns}), 200
