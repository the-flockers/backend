# Interfacing between web APIs and internal ORS APIs

import requests
from flask import Blueprint

bp = Blueprint("ors", __name__, url_prefix="/ors")


# check the health of the internal ORS instance
@bp.route("/health", methods=["GET"])
def health():
    try:
        res = requests.get("http://localhost:8082/")
        if res.status_code == 200:
            return {"status": "ok"}, 200
        else:
            return {"status": "not ok"}, 503
    except requests.exceptions.RequestException:
        return {"status": "not ok"}, 503
