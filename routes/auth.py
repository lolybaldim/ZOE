from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, bcrypt
from models.user import User
from models.patient import Patient

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))
    return render_template("index.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "patient")

        if not all([first_name, last_name, email, password]):
            flash("All fields are required.", "danger")
            return render_template("signup.html")

        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "danger")
            return render_template("signup.html")

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(first_name=first_name, last_name=last_name,
                    email=email, password_hash=hashed, role=role)
        db.session.add(user)
        db.session.flush()

        if role == "patient":
            db.session.add(Patient(user_id=user.id))

        db.session.commit()
        login_user(user)
        flash(f"Welcome to ZOE, {first_name}! Your account has been created.", "success")
        return redirect(url_for("dashboard.home"))

    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        user = User.query.filter_by(email=email).first()
        if user and user.is_active and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            session["language"] = user.language
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard.home"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("auth.login"))


@auth_bp.route("/set-language/<lang>")
@login_required
def set_language(lang):
    if lang in ["en", "fr", "ar", "sw"]:
        current_user.language = lang
        db.session.commit()
        session["language"] = lang
    return redirect(request.referrer or url_for("dashboard.home"))
