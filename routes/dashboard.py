from datetime import date
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.appointment import Appointment
from models.consultation import Consultation
from models.medication import Medication, MedicationLog

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def home():
    today = date.today()

    upcoming_appointments = (
        Appointment.query
        .filter_by(patient_id=current_user.id)
        .filter(Appointment.date >= today)
        .filter(Appointment.status.in_(["pending", "confirmed"]))
        .order_by(Appointment.date, Appointment.time)
        .limit(5)
        .all()
    )

    recent_consultations = (
        Consultation.query
        .filter_by(user_id=current_user.id)
        .order_by(Consultation.created_at.desc())
        .limit(5)
        .all()
    )

    active_medications = (
        Medication.query
        .filter_by(user_id=current_user.id, is_active=True)
        .all()
    )

    taken_today = (
        MedicationLog.query
        .join(Medication)
        .filter(Medication.user_id == current_user.id, MedicationLog.log_date == today)
        .count()
    )

    return render_template(
        "dashboard.html",
        upcoming_appointments=upcoming_appointments,
        recent_consultations=recent_consultations,
        active_medications=active_medications,
        taken_today=taken_today,
        today=today,
    )
