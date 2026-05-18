from datetime import datetime
from flask_login import UserMixin
from extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="patient")
    language = db.Column(db.String(10), nullable=False, default="en")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient_profile = db.relationship("Patient", backref="user", uselist=False, lazy=True,
                                      foreign_keys="Patient.user_id")
    appointments = db.relationship("Appointment", backref="patient", lazy=True,
                                   foreign_keys="Appointment.patient_id")
    medications = db.relationship("Medication", backref="user", lazy=True)
    consultations = db.relationship("Consultation", backref="user", lazy=True)
    emergencies = db.relationship("Emergency", backref="user", lazy=True,
                                   foreign_keys="Emergency.user_id")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<User {self.email}>"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
