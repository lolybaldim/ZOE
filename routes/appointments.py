from datetime import datetime, date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.appointment import Appointment
from models.user import User

appointments_bp = Blueprint("appointments", __name__)


@appointments_bp.route("/appointments", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        appt_date = request.form.get("date")
        appt_time = request.form.get("time")
        reason = request.form.get("reason", "").strip()
        doctor_id = request.form.get("doctor_id")

        if not all([appt_date, appt_time, reason]):
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for("appointments.index"))

        parsed_date = datetime.strptime(appt_date, "%Y-%m-%d").date()
        if parsed_date < date.today():
            flash("Cannot book appointments in the past.", "danger")
            return redirect(url_for("appointments.index"))

        conflict = Appointment.query.filter_by(
            patient_id=current_user.id, date=parsed_date
        ).filter(Appointment.status.in_(["pending", "confirmed"])).first()

        if conflict:
            flash("You already have an appointment on this date.", "warning")
            return redirect(url_for("appointments.index"))

        appt = Appointment(
            patient_id=current_user.id,
            doctor_id=int(doctor_id) if doctor_id else None,
            date=parsed_date,
            time=datetime.strptime(appt_time, "%H:%M").time(),
            reason=reason,
        )
        db.session.add(appt)
        db.session.commit()
        flash("Appointment booked successfully!", "success")
        return redirect(url_for("appointments.index"))

    appointments = (Appointment.query.filter_by(patient_id=current_user.id)
                    .order_by(Appointment.date.desc()).all())
    doctors = User.query.filter_by(role="doctor", is_active=True).all()
    return render_template("appointments.html", appointments=appointments,
                           doctors=doctors, today=date.today())


@appointments_bp.route("/appointments/<int:appt_id>/cancel", methods=["POST"])
@login_required
def cancel(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    if appt.patient_id != current_user.id and current_user.role not in ["admin", "doctor"]:
        flash("Not authorized.", "danger")
        return redirect(url_for("appointments.index"))
    appt.status = "cancelled"
    db.session.commit()
    flash("Appointment cancelled.", "info")
    return redirect(url_for("appointments.index"))
