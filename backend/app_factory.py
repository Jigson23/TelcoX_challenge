# Author: Ing. Jigson Contreras
# Email: supercontreras-ji@hotmail.com
from __future__ import annotations

import os
import socket
from logging.config import dictConfig
from typing import Any, Dict

from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError

from flask import Flask, jsonify
from flask_cors import CORS
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


def _can_connect(host: str, port: int, timeout: float = 1.0) -> bool:
    """Verifica si se puede establecer una conexión TCP al host y puerto especificados."""
    try:
        with socket.create_connection((host, port), timeout):
            return True
    except OSError:
        return False


def _is_fallback_enabled(app: Flask) -> bool:
    """Determina si se debe habilitar el uso de la base de datos de respaldo."""
    env_override = app.config.get("DB_FALLBACK_ENABLED")
    if env_override is None:
        raw_value = os.getenv("DB_FALLBACK_ENABLED")
        if raw_value is None:
            return app.config.get("FLASK_ENV") != "production"
        return raw_value.lower() not in {"0", "false", "no"}
    return bool(env_override)


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
    fallback_uri = app.config.get("DEFAULT_SQLALCHEMY_DATABASE_URI", "sqlite:///telcox.db")

    try:
        url = make_url(uri)
    except ArgumentError:
        url = None

    if url and url.host and url.get_backend_name() in {"mysql"}:
        port = int(url.port or 3306)
        if _is_fallback_enabled(app) and not _can_connect(url.host, port):
            app.logger.warning(
                "No se pudo conectar a %s:%s. Se usará la base de datos SQLite de respaldo en %s.",
                url.host,
                port,
                fallback_uri,
            )
            uri = fallback_uri

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
    configure_cors(app)

    register_blueprints(app)
    register_error_handlers(app)

    app.logger.debug("Aplicación inicializada con la configuración: %s", app.config)
    return app


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(consumption_bp)


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        response = {"mensaje": error.description or "Error HTTP"}
        return jsonify(response), error.code or 500

    @app.errorhandler(Exception)
    def handle_exception(error: Exception): 
        app.logger.exception("Excepción no controlada: %s", error)
        response = {"mensaje": "Error interno del servidor"}
        return jsonify(response), 500


def configure_cors(app: Flask) -> None:
    """Configura CORS para permitir el acceso desde el frontend."""

    origins = app.config.get("CORS_ORIGINS") or os.getenv("CORS_ORIGINS")
    if origins:
        allowed_origins = [origin.strip() for origin in origins.split(",") if origin.strip()]
    else:
        allowed_origins = ["*"]

    supports_credentials = app.config.get("CORS_SUPPORTS_CREDENTIALS")
    if supports_credentials is None:
        supports_credentials = allowed_origins != ["*"]

    CORS(
        app,
        resources={r"/api/*": {"origins": allowed_origins}},
        supports_credentials=supports_credentials,
    )


__all__ = ["create_app", "configure_logging", "configure_database", "configure_cors"]
