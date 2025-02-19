from flask import Blueprint, request, jsonify
from .models.reminder import Reminder, db

# Create a Blueprint for your routes
reminder_bp = Blueprint('reminder', __name__)

@reminder_bp.route('/createReminder', methods=['POST'])
def create_reminder():
    data = request.get_json()  # Get the JSON data from the request

    # Validate the incoming data
    if not data or 'user_email' not in data or 'start_date' not in data or 'end_date' not in data or 'huts' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    # Create reminders for each hut in the huts array
    reminders = []
    for hut_id in data['huts']:
        new_reminder = Reminder(
            user_email=data['user_email'],
            start_date=data['start_date'],  # Ensure this is in the correct format (YYYY-MM-DD)
            end_date=data['end_date'],        # Ensure this is in the correct format (YYYY-MM-DD)
            hut_id=hut_id
        )
        reminders.append(new_reminder)

    # Add the new reminders to the session and commit
    db.session.add_all(reminders)
    db.session.commit()

    return jsonify({'message': 'Reminders created successfully', 'reminder_ids': [reminder.id for reminder in reminders]}), 201
