from flask import Blueprint
from .models import Meeting, Participant
from flask import request, jsonify
from . import db

api = Blueprint('api', __name__)

#Get all meetings
@api.route('/meetings', methods = ['GET'])
def get_meetings():
    meetings = Meeting.query.all()
    meeting_data = [{"id": meeting.id, "subject": meeting.subject} for meeting in meetings]
    return jsonify(meeting_data)

#Create a meeting
@api.route('/meetings', methods = ['POST'])
def create_meeting():
    data = request.get_json()
    if not data or 'subject' not in data or 'date' not in data or 'start_time' not in data or 'end_time' not in data:
        return jsonify({"message" : "Incomplete data"}), 400
    
    new_meeting = Meeting(
        subject = data['subject'],
        date = data['date'],
        start_time = data['start_time'],
        end_time = data['end_time']
    )
    
    db.session.add(new_meeting)
    db.session.commit()
    
    return jsonify({"message": "Meeting created successfully", "id": new_meeting.id}), 201

#Get a meeting by id
@api.route('/meetings/<int:id>', methods = ['GET'])
def get_meeting(id):
    meeting = Meeting.query.get(id)
    if not meeting:
        return jsonify({"message" : "No meeting found"}), 404
    
    #Get participants for the meeting
    participants = [{"id": participant.id, "name": participant.name, "email": participant.email} for participant in meeting.participants]
    
    meeting_data = {
        "id": meeting.data,
        "subject": meeting.subject,
        "date": str(meeting.date),
        "start_time": str(meeting.start_time),
        "end_time": str(meeting.end_time),
        "participants": participants
        }
    
    return jsonify(meeting_data), 200

@api.route('/meetings/<int:id>', methods = ['PUT'])
def update_meeting(id):
    data = request.get_json()
    meeting = Meeting.query.get(id)
    
    if not meeting:
        return jsonify({"message": "No meeting found"}), 404
    
    if data and 'subject' in data:
        meeting.subject = data['subject']
    if data and 'date' in data:
        meeting.date = data['date']
    if data and 'start_time' in data:
        meeting.start_time = data['start_time']
    if data and 'end_time' in data:
        meeting.end_time = data['end_time']
    
    db.session.commit()
    
    return jsonify({"message": "Meeting updated successfully"}), 200

#Delete a Meeting
@api.route('/meetings/<int:id>', methods = ['DELETE'])
def update_meeting(id):
    meeting = Meeting.query.get(id)
    
    if not meeting:
        return jsonify({"message": "No meeting found"}), 404
    
    db.session.delete(meeting)
    db.session.commit()
    
    return jsonify({"message": "Meeting deleted successfully"}), 200
    
#Get all participants
@api.route('/participants', methods = ['GET'])
def get_participants():
    participants = Participant.query.all()
    participant_data = [{"id": participant.id, "name": participant.name, "email": participant.email} for participant in participants]
    return jsonify(participant_data)

#Create a participant
@api.route('/participants', methods = ['POST'])
def create_participant():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data or 'meeting_id' not in data:
        return jsonify({"message": "Incomplete participant"}), 400
    
    new_participant = Participant(
        name = data['name'],
        email = data['email'],
        meeting_id = data['meeting_id']
    )
    
    db.session.add(new_participant)
    db.session.commit()
    
    return jsonify({"message": "New participant created successfully", "id": new_participant.id}), 201

#Update a participant
@api.route('/participants/<int:id>', methods = ['PUT'])
def update_participant(id):
    data = request.get_json()
    participant = Participant.query.get(id)
    
    if not participant:
        return jsonify({"message": "Participant not found"}), 404
    
    if data and 'name' in data:
        participant.name = data['name']
    if data and 'email' in data:
        participant.email = data['email']
    if data and 'meeting_id' in data:
        participant.meeting_id = data['meeting_id']
    
    db.session.commit()
    
    return jsonify({"message": "Participant Updated Successfully"}), 200

#Delete a participant
@api.route('/participants/<int:id>', methods = ['DELETE'])
def delete_participant(id):
    participant = Participant.query.get(id)
    
    if not participant:
        return jsonify({"message": "participant not found"}), 404
    
    db.session.delete(participant)
    db.session.commit()
    
    return jsonify({"message": "Participant deleted successfully"}), 200