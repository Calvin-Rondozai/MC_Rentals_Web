from datetime import datetime, date

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class Admin(UserMixin, db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class House(db.Model):
    __tablename__ = "houses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    property_type = db.Column(db.String(30), nullable=False, default="house")  # house, apartment, room, cottage
    price = db.Column(db.Float, nullable=False)
    price_period = db.Column(db.String(20), nullable=False, default="month")  # month, week, night

    bedrooms = db.Column(db.Integer, default=0)
    bathrooms = db.Column(db.Integer, default=0)

    location = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(255))

    has_water = db.Column(db.Boolean, default=False)
    has_electricity = db.Column(db.Boolean, default=False)
    has_backup_power = db.Column(db.Boolean, default=False)
    has_wifi = db.Column(db.Boolean, default=False)
    has_security = db.Column(db.Boolean, default=False)
    has_parking = db.Column(db.Boolean, default=False)
    is_furnished = db.Column(db.Boolean, default=False)
    other_amenities = db.Column(db.Text)

    status = db.Column(db.String(20), nullable=False, default="available")  # available, occupied

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    images = db.relationship(
        "HouseImage", backref="house", cascade="all, delete-orphan", order_by="HouseImage.position"
    )
    occupants = db.relationship("Occupant", backref="house", cascade="all, delete-orphan")

    @property
    def primary_image(self):
        for img in self.images:
            if img.is_primary:
                return img
        return self.images[0] if self.images else None

    @property
    def amenity_list(self):
        items = []
        if self.has_water:
            items.append(("water", "Water Supply"))
        if self.has_electricity:
            items.append(("electricity", "Electricity"))
        if self.has_backup_power:
            items.append(("backup-power", "Backup Power / Generator"))
        if self.has_wifi:
            items.append(("wifi", "Wi-Fi Ready"))
        if self.has_security:
            items.append(("security", "Security"))
        if self.has_parking:
            items.append(("parking", "Parking"))
        if self.is_furnished:
            items.append(("furnished", "Furnished"))
        return items


class HouseImage(db.Model):
    __tablename__ = "house_images"

    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey("houses.id"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    position = db.Column(db.Integer, default=0)


class Occupant(db.Model):
    __tablename__ = "occupants"

    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey("houses.id"), nullable=False)

    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(150))

    move_in_date = db.Column(db.Date, nullable=False, default=date.today)
    lease_end_date = db.Column(db.Date)
    rent_amount = db.Column(db.Float)

    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_active(self):
        return self.lease_end_date is None or self.lease_end_date >= date.today()


class Setting(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.String(255))

    @staticmethod
    def get(key, default=None):
        row = Setting.query.filter_by(key=key).first()
        return row.value if row else default

    @staticmethod
    def set(key, value):
        row = Setting.query.filter_by(key=key).first()
        if row:
            row.value = value
        else:
            row = Setting(key=key, value=value)
            db.session.add(row)
        db.session.commit()
