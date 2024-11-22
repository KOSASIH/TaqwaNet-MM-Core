from flask import Blueprint, request, jsonify
from src.models.transaction import Transaction
from src import db

transaction_controller = Blueprint('transaction_controller', __name__)

@transaction_controller.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.json
    if not data or 'user_id' not in data or 'amount' not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_transaction = Transaction.create_transaction(data['user_id'], data['amount'], data.get('description'))
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify(new_transaction.get_transaction_summary()), 201

@transaction_controller.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify(transaction.get_transaction_summary()), 200

@transaction_controller.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    data = request.json
    if 'amount' in data:
        transaction.amount = data['amount']
    if 'description' in data:
        transaction.description = data['description']
    db.session.commit()
    return jsonify(transaction.get_transaction_summary()), 200

@transaction_controller.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction deleted successfully"}), 204
