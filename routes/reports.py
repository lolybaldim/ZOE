from datetime import date
from flask import Blueprint, send_file, flash, redirect, url_for
from flask_login import login_required, current_user
from models.consultation import Consultation
from models.appointment import Appointment
from models.medication import Medication
from utils.pdf_generator import generate_patient_report

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/report/download")
@login_required
def download():
    patient = current_user.patient_profile
    if not patient:
        flash("Please complete your health profile first.", "warning")
        return redirect(url_for("patients.profile"))

    consultations = (
        Consultation.query
        .filter_by(user_id=current_user.id)
        .order_by(Consultation.created_at.desc())
        .all()
    )
    appointments = (
        Appointment.query
        .filter_by(patient_id=current_user.id)
        .order_by(Appointment.date.desc())
        .all()
    )
    medications = Medication.query.filter_by(user_id=current_user.id, is_active=True).all()

    pdf_buffer = generate_patient_report(
        current_user, patient, consultations, appointments, medications
    )

    filename = f"ZOE_Report_{current_user.last_name}_{date.today().isoformat()}.pdf"
    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )
