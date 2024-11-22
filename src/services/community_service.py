from datetime import datetime
from flask import jsonify
from models import CommunityEvent, CommunityMember  # Assuming these are ORM models
from sqlalchemy.exc import IntegrityError

class CommunityService:
    def create_event(self, title, description, date, location, organizer_id):
        """Create a new community event."""
        event = CommunityEvent(
            title=title,
            description=description,
            date=date,
            location=location,
            organizer_id=organizer_id,
            created_at=datetime.utcnow()
        )
        
        try:
            event.save()  # Save to the database
            return jsonify({'message': 'Event created successfully', 'event_id': event.id}), 201
        except IntegrityError:
            return jsonify({'error': 'Event with this title already exists'}), 409

    def get_event_details(self, event_id):
        """Retrieve details of a specific community event."""
        event = CommunityEvent.get_by_id(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        return jsonify({'event_id': event.id, 'details': event}), 200

    def list_events(self):
        """List all community events."""
        events = CommunityEvent.get_all()  # Assuming this method fetches all events
        return jsonify({'events': events}), 200

    def register_member(self, user_id, community_id):
        """Register a new member to a community."""
        member = CommunityMember(user_id=user_id, community_id=community_id, joined_at=datetime.utcnow())
        
        try:
            member.save()  # Save to the database
            return jsonify({'message': 'Member registered successfully', 'member_id': member.id}), 201
        except IntegrityError:
            return jsonify({'error': 'Member already exists in this community'}), 409

    def get_member_details(self, member_id):
        """Retrieve details of a specific community member."""
        member = CommunityMember.get_by_id(member_id)
        if not member:
            return jsonify({'error': 'Member not found'}), 404
        
        return jsonify({'member_id': member.id, 'details': member}), 200

    def list_members(self, community_id):
        """List all members of a specific community."""
        members = CommunityMember.get_by_community_id(community_id)  # Assuming this method fetches members by community
        return jsonify({'community_id': community_id, 'members': members}), 200

    def delete_event(self, event_id):
        """Delete a community event."""
        event = CommunityEvent.get_by_id(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        event.delete()  # Assuming this method exists to remove the event
        return jsonify({'message': 'Event deleted successfully'}), 200

    def delete_member(self, member_id):
        """Remove a member from a community."""
        member = CommunityMember.get_by_id(member_id)
        if not member:
            return jsonify({'error': 'Member not found'}), 404
        
        member.delete()  # Assuming this method exists to remove the member
        return jsonify({'message': 'Member removed successfully'}), 200
