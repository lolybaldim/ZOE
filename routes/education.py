from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from utils.gemma_api import get_education_response

education_bp = Blueprint("education", __name__)

HEALTH_TOPICS = [
    {"id": "maternal", "title": "Maternal & Pregnancy Health", "icon": "🤱"},
    {"id": "hygiene", "title": "Hygiene & Sanitation", "icon": "🧼"},
    {"id": "nutrition", "title": "Nutrition & Diet", "icon": "🥗"},
    {"id": "prevention", "title": "Disease Prevention", "icon": "🛡️"},
    {"id": "mental", "title": "Mental Health", "icon": "🧠"},
    {"id": "child", "title": "Child Health", "icon": "👶"},
]


@education_bp.route("/education")
@login_required
def index():
    return render_template("education.html", topics=HEALTH_TOPICS)


@education_bp.route("/education/ask", methods=["POST"])
@login_required
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()
    language = data.get("language", current_user.language or "en")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    response = get_education_response(question, language)
    return jsonify({"response": response})
