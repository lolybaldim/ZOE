from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.patient import Patient

patients_bp = Blueprint("patients", __name__)


@patients_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    patient = current_user.patient_profile
    if not patient:
        patient = Patient(user_id=current_user.id)
        db.session.add(patient)
        db.session.commit()

    if request.method == "POST":
        from datetime import datetime
        dob_str = request.form.get("date_of_birth")
        patient.date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
        patient.gender = request.form.get("gender")
        patient.blood_type = request.form.get("blood_type")
        patient.allergies = request.form.get("allergies")
        patient.chronic_conditions = request.form.get("chronic_conditions")
        patient.emergency_contact_name = request.form.get("emergency_contact_name")
        patient.emergency_contact_phone = request.form.get("emergency_contact_phone")
        patient.address = request.form.get("address")
        patient.phone = request.form.get("phone")
        current_user.first_name = request.form.get("first_name", current_user.first_name)
        current_user.last_name = request.form.get("last_name", current_user.last_name)
        db.session.commit()
        flash("Health profile updated successfully.", "success")
        return redirect(url_for("patients.profile"))

    return render_template("profile.html", patient=patient)
