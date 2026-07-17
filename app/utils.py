import os
import re
import uuid

from flask import current_app
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps


def allowed_file(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


def save_house_image(file_storage, max_dimension=1600):
    """Save an uploaded image to disk with a unique name, normalize orientation
    and cap its longest side so listing pages stay fast. Returns the stored filename."""
    original_name = secure_filename(file_storage.filename)
    ext = original_name.rsplit(".", 1)[-1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    destination = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_name)

    image = Image.open(file_storage)
    image = ImageOps.exif_transpose(image)
    if image.mode in ("RGBA", "P") and ext in ("jpg", "jpeg"):
        image = image.convert("RGB")

    image.thumbnail((max_dimension, max_dimension))
    image.save(destination)

    return unique_name


def delete_house_image(filename):
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(path):
        os.remove(path)


def whatsapp_link(number, message=""):
    digits = re.sub(r"[^\d]", "", number or "")
    if not digits:
        return "#"
    if message:
        from urllib.parse import quote

        return f"https://wa.me/{digits}?text={quote(message)}"
    return f"https://wa.me/{digits}"


def tel_link(number):
    digits = re.sub(r"[^\d+]", "", number or "")
    return f"tel:{digits}" if digits else "#"
