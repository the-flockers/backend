# Interfaces ALPR information requests (i.e., locations and counts).

import os

from flask import Blueprint, current_app, send_file

bp = Blueprint("alpr", __name__, url_prefix="/alpr")


@bp.route("/locations", methods=["GET"])
def locations():
    """gets alpr locations, returned as a .geojson file"""
    filepath = os.path.join(current_app.root_path, "san_diego_alprs.geojson")
    return send_file(filepath)


# TODO: use actual counts stored in file appended after extract_cameras.py
@bp.route("/count", methods=["GET"])
def count():
    """gets alpr count, returned as an integer parsed as a string"""
    return str(932)
