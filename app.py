import os
from flask import Flask, render_template
from extensions import db, login_manager, migrate, mail, bcrypt
from config import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please sign in to access this page."
    login_manager.login_message_category = "info"

    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.patients import patients_bp
    from routes.appointments import appointments_bp
    from routes.medications import medications_bp
    from routes.emergency import emergency_bp
    from routes.ai_chat import ai_chat_bp
    from routes.hospitals import hospitals_bp
    from routes.admin import admin_bp
    from routes.education import education_bp
    from routes.analytics import analytics_bp
    from routes.reports import reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(medications_bp)
    app.register_blueprint(emergency_bp)
    app.register_blueprint(ai_chat_bp)
    app.register_blueprint(hospitals_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(education_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(reports_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
