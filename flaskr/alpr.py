# Interface for ALPR data

from flask import Blueprint, send_file
from flask_cors import CORS

bp = Blueprint("alpr", __name__, url_prefix="/alpr")
CORS(bp, origins=["https://deflock.opencodingsociety.com"])

ALPR_LOCATIONS = "san_diego_alprs.geojson"


# Get ALPR locations
@bp.route("/locations", methods=["GET"])
def locations():
    return send_file(ALPR_LOCATIONS)
