from datetime import datetime
from extensions import db


class Consultation(db.Model):
    __tablename__ = "consultations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    urgency_level = db.Column(db.String(20), nullable=False)
    language = db.Column(db.String(10), default="en")
    summary = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
