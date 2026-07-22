import os
import warnings

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

_secret_key = os.environ.get("SECRET_KEY")
if not _secret_key:
    warnings.warn(
        "SECRET_KEY environment variable is not set — falling back to an insecure "
        "development key. Set SECRET_KEY before deploying to production.",
        RuntimeWarning,
    )
    _secret_key = "dev-secret-key-change-me-in-production"


class Config:
    SECRET_KEY = _secret_key
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(INSTANCE_DIR, "mcproperties.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload

    SITE_NAME = "MC Rentals"
    SITE_TAGLINE = "Find. Buy. Rent. Invest."

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("FORCE_SECURE_COOKIES", "false").lower() == "true"
