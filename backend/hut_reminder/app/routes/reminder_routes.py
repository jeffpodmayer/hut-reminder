from flask import Blueprint, request, jsonify
from ..models.reminder import Reminder, db
from ..models.hut import Hut
from datetime import datetime

reminder_bp = Blueprint('reminder', __name__)

@reminder_bp.route('/create-reminder', methods=['POST'])
def create_reminder():
    data = request.get_json()
    
    try: 
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
        huts = Hut.query.filter(Hut.id.in_(data['huts'])).all()
        
        new_reminder = Reminder(
            user_email=data['user_email'],
            start_date=start_date,
            end_date=end_date,
            huts=huts
        )
        
        db.session.add(new_reminder)
        db.session.commit()
        
        return jsonify({'message': 'Reminder created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@reminder_bp.route('/get-reminders/<email>', methods=['GET'])
def get_reminders_by_email(email):
    try: 
        reminders = Reminder.query.filter_by(user_email=email).all()
        
        grouped_reminders = {}
        
        for reminder in reminders:
            key = f"{reminder.start_date.strftime('%Y-%m-%d')}_{reminder.end_date.strftime('%Y-%m-%d')}"
            
            if key not in grouped_reminders:
                grouped_reminders[key] = {
                    'id': reminder.id,
                    'user_email': reminder.user_email,
                    'start_date': reminder.start_date.strftime('%Y-%m-%d'),
                    'end_date': reminder.end_date.strftime('%Y-%m-%d'),
                    'hut_names': [],
                    'hut_ids': []
                }
            
            for hut in reminder.huts:
                if hut.name not in grouped_reminders[key]['hut_names']:
                    grouped_reminders[key]['hut_names'].append(hut.name)
                    grouped_reminders[key]['hut_ids'].append(hut.id)
        
        reminders_list = list(grouped_reminders.values())
        
        return jsonify(reminders_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reminder_bp.route('/delete-reminder/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    try:
        reminder = Reminder.query.get_or_404(reminder_id)
        db.session.delete(reminder)
        db.session.commit()
        return jsonify({'message': 'Reminder deleted successfully'}), 200
    except Exception as e:
        print(f"Error deleting reminder: {str(e)}")
        return jsonify({'error': str(e)}), 500

@reminder_bp.route('/update-reminder/<int:reminder_id>', methods=['PUT'])
def update_reminder(reminder_id):
    try:
        reminder = Reminder.query.get_or_404(reminder_id)
        data = request.get_json()

        if 'start_date' in data:
            reminder.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        if 'end_date' in data:
            reminder.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
        if 'hut_id' in data:
            reminder.hut_id = data['hut_id']

        db.session.commit()
        return jsonify({'message': 'Reminder updated successfully'}), 200
    except Exception as e:
        print(f"Error updating reminder: {str(e)}")
        return jsonify({'error': str(e)}), 500

