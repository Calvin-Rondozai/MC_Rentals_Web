from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    TextAreaField,
    FloatField,
    IntegerField,
    SelectField,
    BooleanField,
    PasswordField,
    DateField,
    MultipleFileField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Password", validators=[DataRequired()])


class AdminCreateForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match")]
    )


class HouseForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=150)])
    description = TextAreaField("Description", validators=[DataRequired()])
    property_type = SelectField(
        "Property Type",
        choices=[("house", "House"), ("apartment", "Apartment"), ("room", "Room"), ("cottage", "Cottage")],
        validators=[DataRequired()],
    )
    price = FloatField("Price", validators=[DataRequired(), NumberRange(min=0)])
    price_period = SelectField(
        "Billing Period",
        choices=[("month", "Per Month"), ("week", "Per Week"), ("night", "Per Night")],
        validators=[DataRequired()],
    )
    bedrooms = IntegerField("Bedrooms", validators=[Optional(), NumberRange(min=0)], default=0)
    bathrooms = IntegerField("Bathrooms", validators=[Optional(), NumberRange(min=0)], default=0)

    location = StringField("Location / Area", validators=[DataRequired(), Length(max=150)])
    address = StringField("Full Address (optional)", validators=[Optional(), Length(max=255)])

    has_water = BooleanField("Water Supply")
    has_electricity = BooleanField("Electricity")
    has_backup_power = BooleanField("Backup Power / Generator")
    has_wifi = BooleanField("Wi-Fi Ready")
    has_security = BooleanField("Security")
    has_parking = BooleanField("Parking")
    is_furnished = BooleanField("Furnished")
    other_amenities = TextAreaField("Other Amenities (optional)", validators=[Optional()])

    status = SelectField(
        "Availability Status", choices=[("available", "Available"), ("occupied", "Occupied")], validators=[DataRequired()]
    )

    images = MultipleFileField(
        "Photos", validators=[FileAllowed(["png", "jpg", "jpeg", "webp"], "Images only (png, jpg, jpeg, webp)")]
    )


class OccupantForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(max=150)])
    phone = StringField("Phone Number", validators=[DataRequired(), Length(max=30)])
    email = StringField("Email (optional)", validators=[Optional(), Email(), Length(max=150)])
    move_in_date = DateField("Move-in Date", validators=[DataRequired()])
    lease_end_date = DateField("Lease End Date (optional)", validators=[Optional()])
    rent_amount = FloatField("Agreed Rent (optional)", validators=[Optional(), NumberRange(min=0)])
    notes = TextAreaField("Notes (optional)", validators=[Optional()])


class SettingsForm(FlaskForm):
    whatsapp_number = StringField(
        "WhatsApp Number (international format, e.g. 27821234567)", validators=[DataRequired(), Length(max=20)]
    )
    phone_number = StringField("Phone Number (for calls, e.g. +27821234567)", validators=[DataRequired(), Length(max=20)])
    currency_symbol = StringField("Currency Symbol (e.g. $, R, £, KES)", validators=[DataRequired(), Length(max=6)])

    legal_business_name = StringField(
        "Registered Business Name (optional, shown on Privacy Policy / Terms)", validators=[Optional(), Length(max=150)]
    )
    legal_address = TextAreaField(
        "Registered / Physical Business Address (shown on Privacy Policy / Terms)", validators=[Optional(), Length(max=500)]
    )
    legal_email = StringField(
        "Contact Email for Privacy & Legal Requests", validators=[Optional(), Email(), Length(max=150)]
    )
