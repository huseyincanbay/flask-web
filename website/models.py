from . import db

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable = False)
    end_time = db.Column(db.Time, nullable = False)
    participants = db.relationship('Participant', backref = 'meeting', lazy = True, cascade='all, delete-orphan')

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable = False)
