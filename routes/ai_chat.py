from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.consultation import Consultation
from models.emergency import Emergency
from utils.gemma_api import get_health_response

ai_chat_bp = Blueprint("ai_chat", __name__)


@ai_chat_bp.route("/ai-chat")
@login_required
def index():
    recent = (Consultation.query.filter_by(user_id=current_user.id)
              .order_by(Consultation.created_at.desc()).limit(10).all())
    return render_template("ai_chat.html", recent_consultations=recent)


@ai_chat_bp.route("/ai-chat/send", methods=["POST"])
@login_required
def send():
    data = request.get_json()
    message = data.get("message", "").strip()
    language = data.get("language", current_user.language or "en")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    result = get_health_response(message, language)

    db.session.add(Consultation(user_id=current_user.id, symptoms=message,
                                ai_response=result["response"],
                                urgency_level=result["urgency"], language=language))

    if result["urgency"] in ["High", "Emergency"]:
        db.session.add(Emergency(user_id=current_user.id, trigger_text=message,
                                 urgency_level=result["urgency"], ai_response=result["response"]))

    db.session.commit()
    return jsonify({"response": result["response"], "urgency": result["urgency"],
                    "is_emergency": result["urgency"] == "Emergency"})
