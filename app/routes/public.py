from flask import Blueprint, render_template, request
from sqlalchemy import or_, func, case
from sqlalchemy.orm import selectinload

from app.extensions import db
from app.models import House

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    featured = (
        House.query.options(selectinload(House.images))
        .filter_by(status="available")
        .order_by(House.created_at.desc())
        .limit(6)
        .all()
    )

    total, available, locations = db.session.query(
        func.count(House.id),
        func.sum(case((House.status == "available", 1), else_=0)),
        func.count(func.distinct(House.location)),
    ).first()

    stats = {
        "total": total or 0,
        "available": available or 0,
        "locations": locations or 0,
    }
    return render_template("index.html", featured=featured, stats=stats)


@public_bp.route("/listings")
def listings():
    query = House.query.options(selectinload(House.images))

    property_type = request.args.get("type", "").strip()
    status = request.args.get("status", "").strip()
    location = request.args.get("location", "").strip()
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    bedrooms = request.args.get("bedrooms", type=int)
    q = request.args.get("q", "").strip()

    if property_type:
        query = query.filter(House.property_type == property_type)
    if status:
        query = query.filter(House.status == status)
    if location:
        query = query.filter(House.location.ilike(f"%{location}%"))
    if min_price is not None:
        query = query.filter(House.price >= min_price)
    if max_price is not None:
        query = query.filter(House.price <= max_price)
    if bedrooms is not None:
        query = query.filter(House.bedrooms >= bedrooms)
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(House.title.ilike(like), House.description.ilike(like), House.location.ilike(like))
        )

    houses = query.order_by(House.created_at.desc()).all()
    locations = [row[0] for row in House.query.with_entities(House.location).distinct().order_by(House.location)]

    return render_template(
        "listings.html",
        houses=houses,
        locations=locations,
        filters={
            "type": property_type,
            "status": status,
            "location": location,
            "min_price": "" if min_price is None else min_price,
            "max_price": "" if max_price is None else max_price,
            "bedrooms": "" if bedrooms is None else str(bedrooms),
            "q": q,
        },
    )


@public_bp.route("/listings/<int:house_id>")
def house_detail(house_id):
    house = House.query.options(selectinload(House.images)).filter_by(id=house_id).first_or_404()
    related = (
        House.query.options(selectinload(House.images))
        .filter(House.id != house.id, House.location == house.location, House.status == "available")
        .limit(3)
        .all()
    )
    return render_template("house_detail.html", house=house, related=related)


@public_bp.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy_policy.html")


@public_bp.route("/terms")
def terms():
    return render_template("terms.html")
