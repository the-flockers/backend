# Interfacing between web APIs and internal ORS APIs

import os

import requests
from flask import Blueprint, request

from flaskr.auth import login_required

bp = Blueprint("ors", __name__, url_prefix="/ors")


# check the health of the internal ORS instance
@bp.route("/health", methods=["GET"])
def health():
    ors_url = os.environ.get("ORS_URL", "http://localhost:8082")
    try:
        res = requests.get(f"{ors_url}/ors/v2/health")
        if res.status_code == 200:
            return {"status": "ok"}, 200
        else:
            return {"status": "not ok"}, 503
    except requests.exceptions.RequestException:
        return {"status": "not ok"}, 503


# @login_required
@bp.route("/directions", methods=["POST"])
def directions():
    data = request.get_json()
    if not data or "coordinates" not in data:
        return {"error": "Missing 'coordinates' in JSON payload"}, 400

    coordinates = data["coordinates"]
    profile = data.get("profile", "driving-car")

    ors_url = os.environ.get("ORS_URL", "http://localhost:8082")
    try:
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        }
        res = requests.post(
            f"{ors_url}/ors/v2/directions/{profile}",
            json={"coordinates": coordinates},
            headers=headers,
        )
        return res.json(), res.status_code
    except requests.exceptions.RequestException as e:
        return {
            "error": "Failed to connect to internal ORS routing service",
            "details": str(e),
        }, 503
