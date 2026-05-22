# Interfaces between web APIs handled by this backend and the ORS instance

import os

import requests
from flask import Blueprint, Response, request

# from flaskr.auth import login_required

bp = Blueprint("ors", __name__, url_prefix="/ors")


@bp.route("/health", methods=["GET"])
def health():
    """
    Checks the health of the internal ORS instance.

    Returns:
        json: status of the server ("ok" or "not ok")
    """
    ors_url = os.environ.get("ORS_URL", "http://localhost:8082")
    try:
        res = requests.get(f"{ors_url}/ors/v2/health")
        if res.status_code == 200:
            return {"status": "ok"}, 200
        else:
            return {"status": "not ok"}, 503
    except requests.exceptions.RequestException:
        return {"status": "not ok"}, 503


# login should be required here, but CORS handles most of the security anyway
# @login_required
@bp.route("/directions", methods=["POST"])
def directions():
    """
    fetches navigational data from the internal ORS instance

    args:
        request: Contains the web request data to be passed to the backend

    returns:
        json: navigational directions for specified restrictions
    """
    data = request.get_json()
    if not data or "coordinates" not in data:
        return {"error": "Missing 'coordinates' in JSON payload"}, 400

    coordinates = data["coordinates"]
    profile = data.get("profile", "driving-car")
    payload = {"coordinates": coordinates}

    if "options" in data:
        payload["options"] = data["options"]

    ors_url = os.environ.get("ORS_URL", "http://localhost:8082")
    try:
        # basically, just pass the requested data from the web request made by the FE
        # into the internal ORS instance
        res = requests.post(
            f"{ors_url}/ors/v2/directions/{profile}/geojson",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        # then return that response
        return Response(
            res.content,
            status=res.status_code,
            content_type=res.headers.get("Content-Type", "application/json"),
        )
    except requests.exceptions.RequestException as e:
        return {
            "error": "Failed to connect to ORS service",
            "details": str(e),
        }, 503
