"""Application factory and global configuration for the Flask app."""
from __future__ import annotations

from logging.config import dictConfig
from typing import Any, Dict

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from backend.routes.consumption import consumption_bp


DEFAULT_LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        }
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["wsgi"],
    },
}


def configure_logging(config: Dict[str, Any] | None = None) -> None:
    """Initialise the logging configuration."""
    logging_config = config or DEFAULT_LOGGING_CONFIG
    dictConfig(logging_config)


def create_app(config: Dict[str, Any] | None = None) -> Flask:
    """Create and configure a Flask application instance."""
    configure_logging()

    app = Flask(__name__)

    if config:
        app.config.update(config)

    register_blueprints(app)
    register_error_handlers(app)

    app.logger.debug("Application initialised with config: %s", app.config)
    return app


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(consumption_bp)


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):  # type: ignore[override]
        response = {"error": error.description or "HTTP error"}
        return jsonify(response), error.code or 500

    @app.errorhandler(Exception)
    def handle_exception(error: Exception):  # type: ignore[override]
        app.logger.exception("Unhandled exception: %s", error)
        response = {"error": "Internal server error"}
        return jsonify(response), 500


__all__ = ["create_app", "configure_logging"]
