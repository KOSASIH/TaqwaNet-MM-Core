from flask import Blueprint, request, jsonify
from src.models.community import Community
from src import db

community_controller = Blueprint('community_controller', __name__)

@community_controller.route('/communities', methods=['POST'])
def create_community():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_community = Community.create_community(data['name'], data.get('description'))
    db.session.add(new_community)
    db.session.commit()
    return jsonify(new_community.get_community_summary()), 201

@community_controller.route('/communities/<int:community_id>', methods=['GET'])
def get_community(community_id):
    community = Community.query.get(community_id)
    if not community:
        return jsonify({"error": "Community not found"}), 404
    return jsonify(community.get_community_summary()), 200

@community_controller.route('/communities/<int:community_id>', methods=['PUT'])
def update_community(community_id):
    community = Community.query.get(community_id)
    if not community:
        return jsonify({"error": "Community not found"}), 404

    data = request.json
    if 'name' in data:
        community.name = data['name']
    if 'description' in data:
        community.description = data['description']
    db.session.commit()
    return jsonify(community.get_community_summary()), 200

@community_controller.route('/communities/<int:community_id>', methods=['DELETE'])
def delete_community(community_id):
    community = Community.query.get(community_id)
    if not community:
        return jsonify({"error": "Community not found"}), 404

    db.session.delete(community)
    db.session.commit()
    return jsonify({"message": "Community deleted successfully"}), 204
