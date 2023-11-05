from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .models import Meeting, Participant
from flask import request, jsonify
from . import db
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

# Get all meetings route
@views.route('/meetings', methods=['GET'])
@login_required
def list_meetings():
    meetings = Meeting.query.all()
    return render_template('list-meetings.html', meetings=meetings)

# Create a new meeting route
@views.route('/meeting', methods=['GET', 'POST'])
def create_meeting():
    if request.method == 'POST':
        subject = request.form.get('subject')
        date = request.form.get('date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        participants = request.form.getlist('participants')

        if not subject or not date or not start_time or not end_time:
            return jsonify({"message": "Entries are not completed!"}), 400

        new_meeting = Meeting(
            subject=subject,
            date=date,
            start_time=start_time,
            end_time=end_time
        )

        if participants:
            participant_ids = [int(id) for id in participants]
            participants = Participant.query.filter(Participant.id.in_(participant_ids)).all()
            new_meeting.participants = participants

        db.session.add(new_meeting)
        db.session.commit()

        return redirect(url_for('views.create_meeting'))

    participants = Participant.query.all()
    return render_template('create-meeting.html', participants=participants)


#Get a meeting by id
@views.route('/meeting/<int:id>', methods=['GET'])
def get_meeting(id):
    meeting = Meeting.query.get(id)
    if not meeting:
        return jsonify({"message": "Meeting not found!"}), 404

    participants = Participant.query.all()

    return render_template('update-meeting.html', meeting=meeting, participants=participants)

#Update a meeting by id
@views.route('/update-meeting/<int:id>', methods=['GET', 'POST'])
def update_meeting(id):
    meeting = Meeting.query.get(id)

    if not meeting:
        return jsonify({"message": "Meeting not found!"}), 404

    participants = Participant.query.all()  

    if request.method == 'POST':
        subject = request.form.get('subject')
        date = request.form.get('date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        participants_selected = request.form.getlist('participants')

        if not subject or not date or not start_time or not end_time:
            return jsonify({"message": "Entries are not completed!"}), 400

        if subject:
            meeting.subject = subject
        if date:
            meeting.date = date
        if start_time:
            meeting.start_time = start_time
        if end_time:
            meeting.end_time = end_time

        if participants_selected:
            participant_ids = [int(id) for id in participants_selected]
            participants = Participant.query.filter(Participant.id.in_(participant_ids)).all()

            meeting.participants = participants

        db.session.commit()

        return redirect(url_for('views.list_meetings', id=meeting.id))

    return render_template('update-meeting.html', meeting=meeting, participants=participants)

#Delete a Meeting
@views.route('/meetings/<int:id>', methods=['POST'])
def delete_meeting(id):
    meeting = Meeting.query.get(id)

    if not meeting:
        return jsonify({"message": "Meeting not found!"}), 404

    db.session.delete(meeting)
    db.session.commit()

    return redirect(url_for('views.list_meetings'))

#Create a participant
@views.route('/participant', methods=['GET', 'POST'])
def create_participant():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        if not name or not email:
            return jsonify({"message": "Entries are not completed!"}), 400

        new_participant = Participant(
            name=name,
            email=email,
        )

        db.session.add(new_participant)
        db.session.commit()

        return redirect(url_for('views.create_participant'))

    meetings = Meeting.query.all()
    return render_template('create-participant.html', meetings=meetings)

#Update a participant
@views.route('/participant/<int:id>', methods=['PUT'])
def update_participant(id):
    participant = Participant.query.get(id)

    if not participant:
        return jsonify({"message": "Cannot find the participant"}, 404)

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        if not name or not email:
            return jsonify({"message": "Entries are not completed!"}, 400)

        participant.name = name
        participant.email = email

        db.session.commit()

        return redirect(url_for('views.update_participant', id=id))

    meetings = Meeting.query.all() 
    return render_template('update-participant.html', participant=participant)

#Delete a participant
@views.route('/participant/<int:id>', methods=['DELETE'])
def delete_participant(id):
    participant = Participant.query.get(id)

    if not participant:
        return jsonify({"message": "Cannot find the participant"}, 404)

    db.session.delete(participant)
    db.session.commit()

    return redirect(url_for('views.participants'))