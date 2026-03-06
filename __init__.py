import logging
import time
from logging.handlers import RotatingFileHandler
from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_mail import Mail
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)
cache = Cache()
mail = Mail()
bcrypt = Bcrypt()


def create_app(config_name="development"):
    app = Flask(__name__)

    from app.config import config
    app.config.from_object(config[config_name])

    if config_name == "production":
        config[config_name].validate()

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Logging
    _setup_logging(app)

    # Request timing + logging middleware
    @app.before_request
    def start_timer():
        g.start = time.monotonic()

    @app.after_request
    def log_request(response):
        if request.path == "/api/v1/health":
            return response  # skip health check noise
        duration_ms = round((time.monotonic() - g.start) * 1000, 2)
        app.logger.info(
            "%s %s %s %sms",
            request.method,
            request.path,
            response.status_code,
            duration_ms,
        )
        return response

    # Security headers
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "connect-src 'self';"
        )
        return response

    # Blueprints
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix="/api/v1")

    from app.api.v1.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/api/v1/admin")

    # Global error handlers
    _register_error_handlers(app)

    return app


def _setup_logging(app):
    import os
    level = getattr(logging, app.config["LOG_LEVEL"].upper(), logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler (rotating, 5MB max, keep 3 backups)
    os.makedirs("logs", exist_ok=True)
    file_handler = RotatingFileHandler(
        app.config["LOG_FILE"], maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    app.logger.setLevel(level)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)


def _register_error_handlers(app):
    from app.utils.responses import error
    from flask import jsonify

    @app.errorhandler(400)
    def bad_request(e):
        return error("Bad request", 400)

    @app.errorhandler(404)
    def not_found(e):
        return error("Resource not found", 404)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return error("Method not allowed", 405)

    @app.errorhandler(429)
    def rate_limited(e):
        return error("Too many requests — please slow down", 429)

    @app.errorhandler(500)
    def server_error(e):
        app.logger.error("Internal server error: %s", str(e), exc_info=True)
        return error("Internal server error", 500)
