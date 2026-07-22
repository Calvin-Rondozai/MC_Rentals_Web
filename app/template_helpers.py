from flask import g

from app.models import Setting
from app.utils import whatsapp_link, tel_link


def _cached_settings():
    """Settings are read from the DB at most once per request, no matter how
    many times the currency filter runs across a page of house cards."""
    if "site_settings" not in g:
        g.site_settings = {
            "whatsapp_number": Setting.get("whatsapp_number", ""),
            "phone_number": Setting.get("phone_number", ""),
            "currency_symbol": Setting.get("currency_symbol", "$"),
            "legal_business_name": Setting.get("legal_business_name", ""),
            "legal_address": Setting.get("legal_address", ""),
            "legal_email": Setting.get("legal_email", ""),
        }
    return g.site_settings


def register_helpers(app):
    @app.context_processor
    def inject_globals():
        settings = _cached_settings()
        return dict(
            site_name=app.config["SITE_NAME"],
            site_tagline=app.config["SITE_TAGLINE"],
            **settings,
        )

    @app.template_filter("currency")
    def currency_filter(value):
        symbol = _cached_settings()["currency_symbol"]
        try:
            return f"{symbol}{value:,.0f}"
        except (TypeError, ValueError):
            return value

    @app.template_filter("whatsapp_url")
    def whatsapp_url_filter(number, message=""):
        return whatsapp_link(number, message)

    @app.template_filter("tel_url")
    def tel_url_filter(number):
        return tel_link(number)
