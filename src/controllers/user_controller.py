from flask import Blueprint, request, jsonify
from src.models.user import User
from src import db

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_user = User.create_user(data['username'], data['email'], data.get('password'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.get_user_summary()), 201

@user_controller.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User  not found"}), 404
    return jsonify(user.get_user_summary()), 200

@user_controller.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User  not found"}), 404

    data = request.json
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    db.session.commit()
    return jsonify(user.get_user_summary()), 200

@user_controller.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User  not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User  deleted successfully"}), 204
