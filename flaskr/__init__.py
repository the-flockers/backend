import os

from flask import Flask
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    # Allow localhost origins in development mode
    allowed_origins = ["https://deflock.opencodingsociety.com"]
    if os.getenv("DEV_MODE") == "true":
        allowed_origins.extend(["http://127.0.0.1:4000", "http://localhost:4000"])
    CORS(app, origins=allowed_origins)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    from . import alpr, auth, dashboard, db, ors

    db.init_app(app)

    app.register_blueprint(alpr.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(ors.bp)

    return app
