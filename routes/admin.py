from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.user import User
from models.appointment import Appointment
from models.emergency import Emergency
from models.consultation import Consultation

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ["admin", "doctor"]:
            flash("Access denied.", "danger")
            return redirect(url_for("dashboard.home"))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/")
@login_required
@admin_required
def index():
    total_users = User.query.filter_by(is_active=True).count()
    total_appointments = Appointment.query.count()
    unacknowledged = Emergency.query.filter_by(acknowledged=False).count()
    recent_consultations = (Consultation.query.order_by(Consultation.created_at.desc())
                            .limit(10).all())
    return render_template("admin/dashboard.html", total_users=total_users,
                           total_appointments=total_appointments,
                           unacknowledged_emergencies=unacknowledged,
                           recent_consultations=recent_consultations)


@admin_bp.route("/users")
@login_required
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=all_users)


@admin_bp.route("/users/<int:user_id>/toggle", methods=["POST"])
@login_required
@admin_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("Cannot deactivate your own account.", "warning")
        return redirect(url_for("admin.users"))
    user.is_active = not user.is_active
    db.session.commit()
    flash(f"User {'activated' if user.is_active else 'deactivated'}.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/appointments")
@login_required
@admin_required
def appointments():
    all_appts = (Appointment.query.order_by(Appointment.date.desc(), Appointment.time.desc())
                 .all())
    return render_template("admin/appointments.html", appointments=all_appts)


@admin_bp.route("/appointments/<int:appt_id>/update", methods=["POST"])
@login_required
@admin_required
def update_appointment(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    appt.status = request.form.get("status", appt.status)
    appt.notes = request.form.get("notes", appt.notes)
    db.session.commit()
    flash("Appointment updated.", "success")
    return redirect(url_for("admin.appointments"))


@admin_bp.route("/emergencies")
@login_required
@admin_required
def emergencies():
    all_emergencies = Emergency.query.order_by(Emergency.created_at.desc()).all()
    return render_template("admin/emergencies.html", emergencies=all_emergencies)


@admin_bp.route("/emergencies/<int:em_id>/acknowledge", methods=["POST"])
@login_required
@admin_required
def acknowledge_emergency(em_id):
    emergency = Emergency.query.get_or_404(em_id)
    emergency.acknowledged = True
    emergency.acknowledged_by = current_user.id
    emergency.acknowledged_at = datetime.utcnow()
    db.session.commit()
    return jsonify({"success": True})
