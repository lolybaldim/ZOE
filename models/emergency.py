from datetime import datetime
from extensions import db


class Emergency(db.Model):
    __tablename__ = "emergencies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    trigger_text = db.Column(db.Text, nullable=False)
    urgency_level = db.Column(db.String(20), nullable=False)
    ai_response = db.Column(db.Text, nullable=True)
    acknowledged = db.Column(db.Boolean, default=False)
    acknowledged_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    acknowledged_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    acknowledger = db.relationship("User", foreign_keys=[acknowledged_by], lazy=True)
