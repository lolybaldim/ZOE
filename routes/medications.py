import json
from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.medication import Medication, MedicationLog

medications_bp = Blueprint("medications", __name__)


@medications_bp.route("/medications", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        dosage = request.form.get("dosage", "").strip()
        frequency = request.form.get("frequency", "daily")
        reminder_times = request.form.getlist("reminder_times")
        instructions = request.form.get("instructions", "").strip()

        if not name or not dosage:
            flash("Medication name and dosage are required.", "danger")
            return redirect(url_for("medications.index"))

        med = Medication(user_id=current_user.id, name=name, dosage=dosage,
                         frequency=frequency, instructions=instructions,
                         reminder_times=json.dumps(reminder_times) if reminder_times else None)
        db.session.add(med)
        db.session.commit()
        flash(f"{name} added to your medications.", "success")
        return redirect(url_for("medications.index"))

    medications = Medication.query.filter_by(user_id=current_user.id, is_active=True).all()
    today_logs = {
        log.medication_id for log in
        MedicationLog.query.join(Medication)
        .filter(Medication.user_id == current_user.id, MedicationLog.log_date == date.today())
        .all()
    }
    return render_template("medications.html", medications=medications, today_logs=today_logs)


@medications_bp.route("/medications/<int:med_id>/take", methods=["POST"])
@login_required
def mark_taken(med_id):
    med = Medication.query.filter_by(id=med_id, user_id=current_user.id).first_or_404()
    db.session.add(MedicationLog(medication_id=med.id))
    db.session.commit()
    return jsonify({"success": True, "message": f"{med.name} marked as taken."})


@medications_bp.route("/medications/<int:med_id>/deactivate", methods=["POST"])
@login_required
def deactivate(med_id):
    med = Medication.query.filter_by(id=med_id, user_id=current_user.id).first_or_404()
    med.is_active = False
    db.session.commit()
    flash(f"{med.name} removed from active medications.", "info")
    return redirect(url_for("medications.index"))
