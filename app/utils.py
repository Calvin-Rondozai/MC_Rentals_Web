import os
import re
import uuid

from flask import current_app
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps, UnidentifiedImageError


def save_house_image(file_storage, max_dimension=1600):
    """Save an uploaded image to disk with a unique name, normalize orientation
    and cap its longest side so listing pages stay fast. Returns the stored filename.

    Raises UnidentifiedImageError if the upload isn't actually a readable image
    (extension alone is not proof of content) — callers should catch this and
    skip the file rather than let it 500 the request.
    """
    original_name = secure_filename(file_storage.filename)
    ext = original_name.rsplit(".", 1)[-1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    destination = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_name)

    try:
        image = Image.open(file_storage)
        image = ImageOps.exif_transpose(image)
        if image.mode in ("RGBA", "P") and ext in ("jpg", "jpeg"):
            image = image.convert("RGB")
        image.thumbnail((max_dimension, max_dimension))
        image.save(destination)
    except OSError as exc:
        raise UnidentifiedImageError(f"Could not read '{file_storage.filename}' as an image") from exc

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
