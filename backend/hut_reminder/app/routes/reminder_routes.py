from flask import Blueprint, request, jsonify
from ..models.reminder import Reminder, db

# Create a Blueprint for your routes
reminder_bp = Blueprint('reminder', __name__)

@reminder_bp.route('/createReminder', methods=['POST'])
def create_reminder():
    print("Received request")
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
        print(new_reminder)

    # Add the new reminders to the session and commit
    # db.session.add_all(reminders)
    # db.session.commit()

    return jsonify({'message': 'Reminders created successfully', 'reminder_ids': [reminder.id for reminder in reminders]}), 201

# @reminder_bp.route('/getReminders', methods=['GET'])
# def get_reminders_by_email():
#     user_email = request.args.get('user_email')  # Get the user_email from query parameters

#     # Validate the incoming email
#     if not user_email:
#         return jsonify({'error': 'Missing user_email parameter'}), 400

#     # Query the database for reminders associated with the user_email
#     reminders = Reminder.query.filter_by(user_email=user_email).all()

#     # Serialize the reminders into a list of dictionaries
#     reminders_list = [
#         {
#             'id': reminder.id,
#             'user_email': reminder.user_email,
#             'start_date': reminder.start_date.isoformat(),  # Convert date to string
#             'end_date': reminder.end_date.isoformat(),      # Convert date to string
#             'hut_id': reminder.hut_id
#         }
#         for reminder in reminders
#     ]

#     return jsonify({'reminders': reminders_list}), 200
