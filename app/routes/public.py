from flask import Blueprint, render_template, request
from sqlalchemy import or_

from app.models import House

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    featured = (
        House.query.filter_by(status="available")
        .order_by(House.created_at.desc())
        .limit(6)
        .all()
    )
    stats = {
        "total": House.query.count(),
        "available": House.query.filter_by(status="available").count(),
        "locations": House.query.with_entities(House.location).distinct().count(),
    }
    return render_template("index.html", featured=featured, stats=stats)


@public_bp.route("/listings")
def listings():
    query = House.query

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
            "min_price": request.args.get("min_price", ""),
            "max_price": request.args.get("max_price", ""),
            "bedrooms": request.args.get("bedrooms", ""),
            "q": q,
        },
    )


@public_bp.route("/listings/<int:house_id>")
def house_detail(house_id):
    house = House.query.get_or_404(house_id)
    related = (
        House.query.filter(House.id != house.id, House.location == house.location, House.status == "available")
        .limit(3)
        .all()
    )
    return render_template("house_detail.html", house=house, related=related)
