from flask import Blueprint, render_template, current_app

hospitals_bp = Blueprint("hospitals", __name__)


@hospitals_bp.route("/hospitals")
def index():
    maps_key = current_app.config.get("MAPS_API_KEY", "")
    return render_template("hospitals.html", maps_api_key=maps_key)
