# Interface for ALPR data

import os

from flask import Blueprint, current_app, send_file

bp = Blueprint("alpr", __name__, url_prefix="/alpr")


# Get ALPR locations
@bp.route("/locations", methods=["GET"])
def locations():
    filepath = os.path.join(current_app.root_path, "san_diego_alprs.geojson")
    return send_file(filepath)


@bp.route("/count", methods=["GET"])
def count():
    return str(932)
