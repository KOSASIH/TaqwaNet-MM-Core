from flask import jsonify
from datetime import datetime
from models import UserActivity, EventLog  # Assuming these are ORM models
from sqlalchemy.exc import IntegrityError

class AnalyticsService:
    def log_user_activity(self, user_id, activity_type, details):
        """Log a user's activity."""
        activity = UserActivity(
            user_id=user_id,
            activity_type=activity_type,
            details=details,
            timestamp=datetime.utcnow()
        )
        
        try:
            activity.save()  # Save to the database
            return jsonify({'message': 'User  activity logged successfully', 'activity_id': activity.id}), 201
        except IntegrityError:
            return jsonify({'error': 'Failed to log user activity'}), 500

    def log_event(self, event_name, event_data):
        """Log a specific event."""
        event = EventLog(
            event_name=event_name,
            event_data=event_data,
            timestamp=datetime.utcnow()
        )
        
        try:
            event.save()  # Save to the database
            return jsonify({'message': 'Event logged successfully', 'event_id': event.id}), 201
        except IntegrityError:
            return jsonify({'error': 'Failed to log event'}), 500

    def get_user_activity(self, user_id):
        """Retrieve all activities for a specific user."""
        activities = UserActivity.get_by_user_id(user_id)  # Assuming this method fetches activities by user ID
        return jsonify({'user_id': user_id, 'activities': activities}), 200

    def get_event_logs(self):
        """Retrieve all logged events."""
        events = EventLog.get_all()  # Assuming this method fetches all events
        return jsonify({'events': events}), 200

    def get_activity_summary(self, user_id):
        """Get a summary of user activities."""
        activities = UserActivity.get_by_user_id(user_id)
        summary = {
            'total_activities': len(activities),
            'last_activity': activities[-1].timestamp if activities else None,
            'activity_types': self._count_activity_types(activities)
        }
        return jsonify({'user_id': user_id, 'summary': summary}), 200

    def _count_activity_types(self, activities):
        """Count the occurrences of each activity type."""
        activity_count = {}
        for activity in activities:
            activity_count[activity.activity_type] = activity_count.get(activity.activity_type, 0) + 1
        return activity_count

    def delete_user_activity(self, activity_id):
        """Delete a specific user activity."""
        activity = UserActivity.get_by_id(activity_id)
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        activity.delete()  # Assuming this method exists to remove the activity
        return jsonify({'message': 'User  activity deleted successfully'}), 200

    def delete_event_log(self, event_id):
        """Delete a specific event log."""
        event = EventLog.get_by_id(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        event.delete()  # Assuming this method exists to remove the event
        return jsonify({'message': 'Event log deleted successfully'}), 200
