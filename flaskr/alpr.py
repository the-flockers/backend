# Interface for ALPR data

from flask import Blueprint, send_file

bp = Blueprint("alpr", __name__, url_prefix="/alpr")

ALPR_LOCATIONS = "san_diego_alprs.geojson"


# Get ALPR locations
@bp.route("/locations", methods=["GET"])
def locations():
    return send_file(ALPR_LOCATIONS)
