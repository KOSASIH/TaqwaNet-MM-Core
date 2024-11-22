from flask import Blueprint, request, jsonify
from src.models.notification import Notification
from src import db

notification_controller = Blueprint('notification_controller', __name__)

@notification_controller.route('/notifications', methods=['POST'])
def create_notification():
    data = request.json
    if not data or 'user_id' not in data or 'message' not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_notification = Notification.create_notification(data['user_id'], data['message'])
    db.session.add(new_notification)
    db.session.commit()
    return jsonify(new_notification.get_notification_summary()), 201

@notification_controller.route('/notifications/<int:notification_id>', methods=['GET'])
def get_notification(notification_id):
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({"error": "Notification not found"}), 404
    return jsonify(notification.get_notification_summary()), 200

@notification_controller.route('/notifications/<int:notification_id>', methods=['PUT'])
def update_notification(notification_id):
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    data = request.json
    if 'message' in data:
        notification.message = data['message']
    db.session.commit()
    return jsonify(notification.get_notification_summary()), 200

@notification_controller.route('/notifications/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    db .session.delete(notification)
    db.session.commit()
    return jsonify({"message": "Notification deleted successfully"}), 204
