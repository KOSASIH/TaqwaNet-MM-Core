from flask import Blueprint, jsonify
from src.models.transaction import Transaction
from src.models.investment import Investment
from src import db

analytics_controller = Blueprint('analytics_controller', __name__)

@analytics_controller.route('/analytics/transactions', methods=['GET'])
def get_transaction_statistics():
    total_transactions = Transaction.query.count()
    total_amount = db.session.query(db.func.sum(Transaction.amount)).scalar() or 0
    return jsonify({
        "total_transactions": total_transactions,
        "total_amount": total_amount
    }), 200

@analytics_controller.route('/analytics/investments', methods=['GET'])
def get_investment_statistics():
    total_investments = Investment.query.count()
    total_invested_amount = db.session.query(db.func.sum(Investment.amount)).scalar() or 0
    return jsonify({
        "total_investments": total_investments,
        "total_invested_amount": total_invested_amount
    }), 200

@analytics_controller.route('/analytics/users', methods=['GET'])
def get_user_statistics():
    total_users = User.query.count()
    return jsonify({
        "total_users": total_users
    }), 200
