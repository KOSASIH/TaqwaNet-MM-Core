from flask import Blueprint, request, jsonify
from src.models.investment import Investment
from src import db

investment_controller = Blueprint('investment_controller', __name__)

@investment_controller.route('/investments', methods=['POST'])
def create_investment():
    data = request.json
    if not data or 'user_id' not in data or 'amount' not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_investment = Investment.create_investment(data['user_id'], data['amount'], data.get('investment_type'))
    db.session.add(new_investment)
    db.session.commit()
    return jsonify(new_investment.get_investment_summary()), 201

@investment_controller.route('/investments/<int:investment_id>', methods=['GET'])
def get_investment(investment _id):
    investment = Investment.query.get(investment_id)
    if not investment:
        return jsonify({"error": "Investment not found"}), 404
    return jsonify(investment.get_investment_summary()), 200

@investment_controller.route('/investments/<int:investment_id>', methods=['PUT'])
def update_investment(investment_id):
    investment = Investment.query.get(investment_id)
    if not investment:
        return jsonify({"error": "Investment not found"}), 404

    data = request.json
    if 'amount' in data:
        investment.amount = data['amount']
    if 'investment_type' in data:
        investment.investment_type = data['investment_type']
    db.session.commit()
    return jsonify(investment.get_investment_summary()), 200

@investment_controller.route('/investments/<int:investment_id>', methods=['DELETE'])
def delete_investment(investment_id):
    investment = Investment.query.get(investment_id)
    if not investment:
        return jsonify({"error": "Investment not found"}), 404

    db.session.delete(investment)
    db.session.commit()
    return jsonify({"message": "Investment deleted successfully"}), 204
