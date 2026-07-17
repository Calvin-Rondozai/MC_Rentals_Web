from app.models import Setting
from app.utils import whatsapp_link, tel_link


def register_helpers(app):
    @app.context_processor
    def inject_globals():
        whatsapp_number = Setting.get("whatsapp_number", "")
        phone_number = Setting.get("phone_number", "")
        currency_symbol = Setting.get("currency_symbol", "$")
        return dict(
            site_name=app.config["SITE_NAME"],
            site_tagline=app.config["SITE_TAGLINE"],
            whatsapp_number=whatsapp_number,
            phone_number=phone_number,
            currency_symbol=currency_symbol,
        )

    @app.template_filter("currency")
    def currency_filter(value):
        symbol = Setting.get("currency_symbol", "$")
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
