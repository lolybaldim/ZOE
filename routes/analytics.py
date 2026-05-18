from datetime import date, timedelta
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from extensions import db
from models.consultation import Consultation
from models.appointment import Appointment
from models.medication import Medication, MedicationLog

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics")
@login_required
def index():
    return render_template("analytics.html")


@analytics_bp.route("/analytics/data")
@login_required
def data():
    today = date.today()
    thirty_days_ago = today - timedelta(days=30)

    # Symptom/consultation trend (last 30 days)
    consultations = (
        db.session.query(
            func.date(Consultation.created_at).label("day"),
            func.count().label("count")
        )
        .filter(
            Consultation.user_id == current_user.id,
            Consultation.created_at >= thirty_days_ago,
        )
        .group_by(func.date(Consultation.created_at))
        .all()
    )

    # Appointment history (last 6 months)
    six_months_ago = today - timedelta(days=180)
    appointments = (
        db.session.query(
            func.to_char(Appointment.date, "YYYY-MM").label("month"),
            func.count().label("count")
        )
        .filter(
            Appointment.patient_id == current_user.id,
            Appointment.date >= six_months_ago,
        )
        .group_by(func.to_char(Appointment.date, "YYYY-MM"))
        .order_by(func.to_char(Appointment.date, "YYYY-MM"))
        .all()
    )

    # Medication adherence (last 7 days)
    week_ago = today - timedelta(days=7)
    total_doses = (
        Medication.query
        .filter_by(user_id=current_user.id, is_active=True)
        .count()
    ) * 7
    taken_doses = (
        MedicationLog.query
        .join(Medication)
        .filter(
            Medication.user_id == current_user.id,
            MedicationLog.log_date >= week_ago,
        )
        .count()
    )

    adherence_rate = round((taken_doses / total_doses * 100) if total_doses > 0 else 0, 1)

    return jsonify({
        "consultations": [{"day": str(r.day), "count": r.count} for r in consultations],
        "appointments": [{"month": r.month, "count": r.count} for r in appointments],
        "adherence": {
            "taken": taken_doses,
            "missed": max(0, total_doses - taken_doses),
            "rate": adherence_rate,
        },
    })
