from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from app.extensions import db
from app.forms import HouseForm, OccupantForm, SettingsForm, AdminCreateForm
from app.models import House, HouseImage, Occupant, Setting, Admin
from app.utils import save_house_image, delete_house_image

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@login_required
def dashboard():
    houses = House.query.order_by(House.created_at.desc()).all()
    stats = {
        "total": len(houses),
        "available": sum(1 for h in houses if h.status == "available"),
        "occupied": sum(1 for h in houses if h.status == "occupied"),
        "occupants": Occupant.query.count(),
    }
    return render_template("admin/dashboard.html", houses=houses, stats=stats)


HOUSE_FIELDS = [
    "title",
    "description",
    "property_type",
    "price",
    "price_period",
    "bedrooms",
    "bathrooms",
    "location",
    "address",
    "has_water",
    "has_electricity",
    "has_backup_power",
    "has_wifi",
    "has_security",
    "has_parking",
    "is_furnished",
    "other_amenities",
    "status",
]


def _apply_house_form(house, form):
    for field_name in HOUSE_FIELDS:
        setattr(house, field_name, getattr(form, field_name).data)

    files = request.files.getlist("images")
    uploaded = [f for f in files if f and f.filename]
    if uploaded:
        existing_count = len(house.images)
        for i, file_storage in enumerate(uploaded):
            filename = save_house_image(file_storage)
            image = HouseImage(
                house=house,
                filename=filename,
                is_primary=(existing_count == 0 and i == 0),
                position=existing_count + i,
            )
            db.session.add(image)


@admin_bp.route("/houses/new", methods=["GET", "POST"])
@login_required
def house_new():
    form = HouseForm()
    if form.validate_on_submit():
        house = House()
        _apply_house_form(house, form)
        db.session.add(house)
        db.session.commit()
        flash(f'"{house.title}" was added successfully.', "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/house_form.html", form=form, house=None)


@admin_bp.route("/houses/<int:house_id>/edit", methods=["GET", "POST"])
@login_required
def house_edit(house_id):
    house = House.query.get_or_404(house_id)
    form = HouseForm(obj=house)
    if form.validate_on_submit():
        _apply_house_form(house, form)
        db.session.commit()
        flash(f'"{house.title}" was updated.', "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/house_form.html", form=form, house=house)


@admin_bp.route("/houses/<int:house_id>/delete", methods=["POST"])
@login_required
def house_delete(house_id):
    house = House.query.get_or_404(house_id)
    for image in house.images:
        delete_house_image(image.filename)
    title = house.title
    db.session.delete(house)
    db.session.commit()
    flash(f'"{title}" was deleted.', "info")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/houses/<int:house_id>/toggle-status", methods=["POST"])
@login_required
def house_toggle_status(house_id):
    house = House.query.get_or_404(house_id)
    house.status = "occupied" if house.status == "available" else "available"
    db.session.commit()
    flash(f'"{house.title}" is now marked {house.status}.', "success")
    return redirect(request.referrer or url_for("admin.dashboard"))


@admin_bp.route("/houses/<int:house_id>/images/<int:image_id>/delete", methods=["POST"])
@login_required
def image_delete(house_id, image_id):
    image = HouseImage.query.filter_by(id=image_id, house_id=house_id).first_or_404()
    was_primary = image.is_primary
    delete_house_image(image.filename)
    db.session.delete(image)
    db.session.flush()
    if was_primary:
        next_image = HouseImage.query.filter_by(house_id=house_id).order_by(HouseImage.position).first()
        if next_image:
            next_image.is_primary = True
    db.session.commit()
    flash("Image removed.", "info")
    return redirect(url_for("admin.house_edit", house_id=house_id))


@admin_bp.route("/houses/<int:house_id>/images/<int:image_id>/make-primary", methods=["POST"])
@login_required
def image_make_primary(house_id, image_id):
    HouseImage.query.filter_by(house_id=house_id).update({"is_primary": False})
    image = HouseImage.query.filter_by(id=image_id, house_id=house_id).first_or_404()
    image.is_primary = True
    db.session.commit()
    flash("Cover photo updated.", "success")
    return redirect(url_for("admin.house_edit", house_id=house_id))


@admin_bp.route("/houses/<int:house_id>/occupants")
@login_required
def occupants_list(house_id):
    house = House.query.get_or_404(house_id)
    return render_template("admin/occupants.html", house=house)


@admin_bp.route("/houses/<int:house_id>/occupants/new", methods=["GET", "POST"])
@login_required
def occupant_new(house_id):
    house = House.query.get_or_404(house_id)
    form = OccupantForm()
    if form.validate_on_submit():
        occupant = Occupant(house=house)
        form.populate_obj(occupant)
        db.session.add(occupant)
        house.status = "occupied"
        db.session.commit()
        flash(f"{occupant.full_name} added as an occupant of {house.title}.", "success")
        return redirect(url_for("admin.occupants_list", house_id=house.id))
    return render_template("admin/occupant_form.html", form=form, house=house, occupant=None)


@admin_bp.route("/occupants/<int:occupant_id>/edit", methods=["GET", "POST"])
@login_required
def occupant_edit(occupant_id):
    occupant = Occupant.query.get_or_404(occupant_id)
    form = OccupantForm(obj=occupant)
    if form.validate_on_submit():
        form.populate_obj(occupant)
        db.session.commit()
        flash(f"{occupant.full_name}'s record was updated.", "success")
        return redirect(url_for("admin.occupants_list", house_id=occupant.house_id))
    return render_template("admin/occupant_form.html", form=form, house=occupant.house, occupant=occupant)


@admin_bp.route("/occupants/<int:occupant_id>/delete", methods=["POST"])
@login_required
def occupant_delete(occupant_id):
    occupant = Occupant.query.get_or_404(occupant_id)
    house_id = occupant.house_id
    name = occupant.full_name
    db.session.delete(occupant)
    db.session.commit()
    flash(f"{name}'s record was removed.", "info")
    return redirect(url_for("admin.occupants_list", house_id=house_id))


@admin_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        Setting.set("whatsapp_number", form.whatsapp_number.data.strip())
        Setting.set("phone_number", form.phone_number.data.strip())
        Setting.set("currency_symbol", form.currency_symbol.data.strip())
        flash("Settings saved.", "success")
        return redirect(url_for("admin.settings"))

    if request.method == "GET":
        form.whatsapp_number.data = Setting.get("whatsapp_number", "")
        form.phone_number.data = Setting.get("phone_number", "")
        form.currency_symbol.data = Setting.get("currency_symbol", "$")

    return render_template("admin/settings.html", form=form)


@admin_bp.route("/admins", methods=["GET", "POST"])
@login_required
def admins():
    form = AdminCreateForm()
    if form.validate_on_submit():
        if Admin.query.filter_by(username=form.username.data.strip()).first():
            flash("That username is already taken.", "error")
        else:
            admin = Admin(username=form.username.data.strip())
            admin.set_password(form.password.data)
            db.session.add(admin)
            db.session.commit()
            flash(f"Admin account '{admin.username}' created.", "success")
            return redirect(url_for("admin.admins"))

    all_admins = Admin.query.order_by(Admin.created_at).all()
    return render_template("admin/admins.html", form=form, admins=all_admins)


@admin_bp.route("/admins/<int:admin_id>/delete", methods=["POST"])
@login_required
def admin_delete(admin_id):
    if Admin.query.count() <= 1:
        flash("You can't delete the only remaining admin account.", "error")
        return redirect(url_for("admin.admins"))
    if admin_id == current_user.id:
        flash("You can't delete your own account while logged in.", "error")
        return redirect(url_for("admin.admins"))

    target = Admin.query.get_or_404(admin_id)
    db.session.delete(target)
    db.session.commit()
    flash(f"Admin account '{target.username}' was removed.", "info")
    return redirect(url_for("admin.admins"))
