from flask import Blueprint, request, jsonify
from ..models.reminder import Reminder, db
from ..models.hut import Hut
from datetime import datetime

reminder_bp = Blueprint('reminder', __name__)

@reminder_bp.route('/create-reminder', methods=['POST'])
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

@reminder_bp.route('/get-reminders/<email>', methods=['GET'])
def get_reminders_by_email(email):
    try: 
        # Join Reminder with Hut table
        reminders = db.session.query(Reminder, Hut)\
            .join(Hut, Reminder.hut_id == Hut.id)\
            .filter(Reminder.user_email == email)\
            .all()

        reminders_list = []
        for reminder, hut in reminders:
            reminders_list.append({
                'id': reminder.id, 
                'user_email': reminder.user_email,
                'start_date': reminder.start_date.strftime('%Y-%m-%d'),
                'end_date': reminder.end_date.strftime('%Y-%m-%d'),      
                'hut_name': hut.name
            })
        return jsonify(reminders_list), 200
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500
