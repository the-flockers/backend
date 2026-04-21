# Interface for ALPR data

import os

from flask import Blueprint, send_file
from flask_cors import CORS

bp = Blueprint("alpr", __name__, url_prefix="/alpr")

# Allow localhost origins in development mode
allowed_origins = ["https://deflock.opencodingsociety.com"]
if os.getenv("DEV_MODE") == "true":
    allowed_origins.extend(["http://127.0.0.1:4000", "http://localhost:4000"])

CORS(bp, origins=allowed_origins)

ALPR_LOCATIONS = "san_diego_alprs.geojson"


# Get ALPR locations
@bp.route("/locations", methods=["GET"])
def locations():
    return send_file(ALPR_LOCATIONS)


@bp.route("/count", methods=["GET"])
def count():
    return str(932)
