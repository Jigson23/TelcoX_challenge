"""Factoría de aplicación y configuración global para el servicio Flask."""
from __future__ import annotations

import os
from logging.config import dictConfig
from typing import Any, Dict

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from backend.models import db
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


def configure_database(app: Flask) -> None:
    """Configura la conexión a la base de datos y registra SQLAlchemy."""

    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    uri = app.config.get("SQLALCHEMY_DATABASE_URI") or os.getenv("SQLALCHEMY_DATABASE_URI")
    if not uri:
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "3306")
        database = os.getenv("DB_NAME")
        if user and password and database:
            uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        else:
            uri = app.config.get("DEFAULT_SQLALCHEMY_DATABASE_URI", "sqlite:///telcox.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = uri

    db.init_app(app)


def configure_logging(config: Dict[str, Any] | None = None) -> None:
    """Inicializa la configuración de logging."""
    logging_config = config or DEFAULT_LOGGING_CONFIG
    dictConfig(logging_config)


def create_app(config: Dict[str, Any] | None = None) -> Flask:
    """Crea y configura una instancia de la aplicación Flask."""
    app = Flask(__name__)

    if config:
        app.config.update(config)

    configure_logging(app.config.get("LOGGING_CONFIG"))
    configure_database(app)

    register_blueprints(app)
    register_error_handlers(app)

    app.logger.debug("Aplicación inicializada con la configuración: %s", app.config)
    return app


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(consumption_bp)


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):  # type: ignore[override]
        response = {"mensaje": error.description or "Error HTTP"}
        return jsonify(response), error.code or 500

    @app.errorhandler(Exception)
    def handle_exception(error: Exception):  # type: ignore[override]
        app.logger.exception("Excepción no controlada: %s", error)
        response = {"mensaje": "Error interno del servidor"}
        return jsonify(response), 500


__all__ = ["create_app", "configure_logging", "configure_database"]
