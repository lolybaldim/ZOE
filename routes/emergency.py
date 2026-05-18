from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from extensions import db
from models.emergency import Emergency

emergency_bp = Blueprint("emergency", __name__)


@emergency_bp.route("/emergency")
@login_required
def index():
    return render_template("emergency.html")


@emergency_bp.route("/emergency/log", methods=["POST"])
@login_required
def log_emergency():
    data = request.get_json()
    emergency = Emergency(
        user_id=current_user.id,
        trigger_text=data.get("trigger_text", ""),
        urgency_level=data.get("urgency_level", "Emergency"),
        ai_response=data.get("ai_response", ""),
    )
    db.session.add(emergency)
    db.session.commit()
    return jsonify({"success": True, "id": emergency.id})
