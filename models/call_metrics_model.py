from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CallMetrics(db.Model):
    __tablename__ = "call_record"

    id = db.Column(db.String(64), primary_key=True)
    call_id = db.Column(db.Integer)
    clinic_name = db.Column(db.String(200))
    call_timestamp = db.Column(db.String(100))
    primary_intent = db.Column(db.String(200))
    secondary_intents = db.Column(db.Text)
    detected_intents = db.Column(db.Text)
    workflow_events = db.Column(db.Text)
    workflow_summary = db.Column(db.Text)
    completion_data = db.Column(db.Text)
    blocker_data = db.Column(db.Text)
    final_output = db.Column(db.Text)
    created_at = db.Column(db.String(100))
    transcript = db.Column(db.Text)
