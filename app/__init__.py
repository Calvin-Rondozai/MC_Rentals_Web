import os

from flask import Flask

from config import Config, INSTANCE_DIR
from app.extensions import db, login_manager, csrf


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(INSTANCE_DIR, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.models import Admin

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Admin, int(user_id))

    from app.routes.public import public_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    from app.template_helpers import register_helpers

    register_helpers(app)

    with app.app_context():
        db.create_all()

    return app
