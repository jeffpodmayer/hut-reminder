from flask import Blueprint, request, jsonify
from ..models.reminder import Reminder, db
from datetime import datetime

reminder_bp = Blueprint('reminder', __name__)

@reminder_bp.route('/createReminder', methods=['POST'])
def create_reminder():
    data = request.get_json()  # Get the JSON data from the request
    print("Received reminder data")

    try: 
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    if not data or 'user_email' not in data or 'start_date' not in data or 'end_date' not in data or 'huts' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    reminders = []
    for hut_id in data['huts']:
        new_reminder = Reminder(
            user_email=data['user_email'],
            start_date=start_date,  
            end_date=end_date,        
            hut_id=hut_id
        )
        reminders.append(new_reminder)

    # Add the new reminders to the session and commit
    db.session.add_all(reminders)
    db.session.commit()

    return jsonify({'message': 'Reminders created successfully'}), 201

@reminder_bp.route('/getRemindersByEmail', methods=['GET'])
def get_reminders_by_email():
    print('Getting All user reminders')
    return jsonify({'message': 'Reminders fetched successfully'}), 200
